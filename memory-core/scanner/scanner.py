import os
import re
import sys
import json
import hashlib
import platform
from datetime import datetime


CONFIG_FILE = "scanner_config.json"

SNAPSHOT_ID_PATTERN = re.compile(r"^SNAP-(\d+)$")

HASH_CHUNK_SIZE = 1024 * 1024

STATUS_CREATED = "CREATED"
STATUS_CREATED_WITH_WARNINGS = "CREATED_WITH_WARNINGS"


class SnapshotError(Exception):
    """A snapshot cannot be created safely. Nothing has been written."""


def load_config():
    with open(CONFIG_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


# ---------------------------------------------------------------------------
# OBSERVATION
# Collects facts about the project. Makes no conclusions.
# ---------------------------------------------------------------------------

def file_sha256(path):
    digest = hashlib.sha256()

    with open(path, "rb") as file:
        for chunk in iter(lambda: file.read(HASH_CHUNK_SIZE), b""):
            digest.update(chunk)

    return digest.hexdigest()


def to_timestamp(epoch_seconds):
    return datetime.fromtimestamp(epoch_seconds).isoformat(timespec="seconds")


def scan_directory(path, ignored):
    """
    Walks the project once.

    Returns:
    - files: full paths in the same format as scanner v0.1 (used by the report);
    - records: metadata of every tracked file (used by the snapshot);
    - directories: number of directories below the project root;
    - warnings: facts that could not be verified.
    """

    files = []
    records = []
    directories = 0
    warnings = []

    def on_walk_error(error):
        warnings.append(
            f"{error.filename}: directory unreadable ({error.strerror}), contents not tracked"
        )

    for root, dirs, names in os.walk(path, onerror=on_walk_error):

        dirs[:] = [
            d for d in dirs
            if d not in ignored
        ]

        directories += len(dirs)

        for name in names:
            full_path = os.path.join(root, name)

            files.append(
                full_path.replace("\\", "/")
            )

            relative_path = os.path.relpath(full_path, path).replace("\\", "/")

            try:
                stat = os.stat(full_path)
            except OSError as error:
                warnings.append(
                    f"{relative_path}: metadata unavailable ({error.strerror}), file not tracked"
                )
                continue

            try:
                file_hash = file_sha256(full_path)
            except OSError as error:
                file_hash = None
                warnings.append(
                    f"{relative_path}: content unreadable ({error.strerror}), hash is null"
                )

            records.append({
                "path": relative_path,
                "size": stat.st_size,
                "extension": os.path.splitext(name)[1],
                "modified": to_timestamp(stat.st_mtime),
                "hash": file_hash,
            })

    # Stable order: the same project state always gives the same file list.
    records.sort(key=lambda record: record["path"])

    return files, records, directories, warnings


# ---------------------------------------------------------------------------
# STORAGE
# Stores facts. Never overwrites history silently.
# ---------------------------------------------------------------------------

def is_placeholder(data):
    # The hand-written v0.1 template: {"files": [...]} without an id.
    return isinstance(data, dict) and set(data.keys()) == {"files"}


def read_current_snapshot(snapshot_file):
    """
    Returns (state, snapshot, raw_bytes).

    state:
    - "none": no snapshot file yet;
    - "placeholder": the v0.1 template (approved to be replaced);
    - "snapshot": a real snapshot that must be preserved.
    """

    if not os.path.exists(snapshot_file):
        return "none", None, None

    with open(snapshot_file, "rb") as file:
        raw = file.read()

    try:
        data = json.loads(raw.decode("utf-8-sig"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        raise SnapshotError(
            f"{snapshot_file} is not valid JSON. The file was left untouched."
        )

    if isinstance(data, dict) and SNAPSHOT_ID_PATTERN.match(str(data.get("id", ""))):
        return "snapshot", data, raw

    if is_placeholder(data):
        return "placeholder", None, None

    raise SnapshotError(
        f"{snapshot_file} has unknown content (no valid snapshot id). "
        "The file was left untouched."
    )


def next_snapshot_number(current_snapshot, history_directory):
    numbers = []

    if current_snapshot is not None:
        match = SNAPSHOT_ID_PATTERN.match(current_snapshot["id"])
        numbers.append(int(match.group(1)))

    if os.path.isdir(history_directory):
        for name in os.listdir(history_directory):
            stem, extension = os.path.splitext(name)
            match = SNAPSHOT_ID_PATTERN.match(stem)

            if extension == ".json" and match:
                numbers.append(int(match.group(1)))

    return max(numbers, default=0) + 1


def preserve_snapshot(snapshot_id, raw, history_directory):
    """
    Copies the previous snapshot into history byte for byte.
    An existing history file is never overwritten.
    """

    os.makedirs(history_directory, exist_ok=True)

    target = os.path.join(history_directory, f"{snapshot_id}.json")

    if os.path.exists(target):
        with open(target, "rb") as file:
            existing = file.read()

        if existing == raw:
            # Already preserved (for example by an interrupted earlier run).
            return target

        raise SnapshotError(
            f"{target} already exists with different content. Nothing was overwritten."
        )

    with open(target, "xb") as file:
        file.write(raw)

    with open(target, "rb") as file:
        if file.read() != raw:
            raise SnapshotError(
                f"Verification of {target} failed. The current snapshot was left untouched."
            )

    return target


def write_json_atomic(path, data):
    # Write to a temporary file first, then replace in one step,
    # so a crash never leaves a half-written snapshot.
    temporary = path + ".tmp"

    with open(temporary, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)
        file.write("\n")
        file.flush()
        os.fsync(file.fileno())

    os.replace(temporary, path)


def build_snapshot(snapshot_id, created, project_name, project_path, records, directories):
    absolute_path = os.path.abspath(project_path)

    return {
        "id": snapshot_id,
        "created": created,
        "project": {
            "name": project_name,
            "target": os.path.basename(absolute_path),
        },
        "environment": {
            "machine_path": absolute_path.replace("\\", "/"),
            "platform": platform.system(),
        },
        "statistics": {
            "total_files": len(records),
            "total_directories": directories,
        },
        "files": records,
    }


# ---------------------------------------------------------------------------
# REPORT
# ---------------------------------------------------------------------------

def create_report(files, snapshot_summary):
    report = []

    report.append("# REQUIEM MEMORY CORE SCAN REPORT\n")
    report.append(
        f"Date: {datetime.now()}\n"
    )

    report.append(
        f"Files detected: {len(files)}\n"
    )

    report.append("\n## Snapshot\n")

    for line in snapshot_summary["lines"]:
        report.append(
            f"- {line}\n"
        )

    if snapshot_summary["warnings"]:
        report.append("\n### Warnings\n")

        for warning in snapshot_summary["warnings"]:
            report.append(
                f"- {warning}\n"
            )

    report.append("\n## Files\n")

    for file in files:
        report.append(
            f"- {file}\n"
        )

    return "".join(report)


# ---------------------------------------------------------------------------

def main():

    config = load_config()

    project_path = config["project_path"]

    ignored = config["ignore"]

    project_name = config["project_name"]

    output = config["output"]

    snapshot_file = output["snapshot_file"]

    history_directory = output["snapshot_history_directory"]

    if not os.path.isdir(project_path):
        raise SnapshotError(
            f"Project path not found: {project_path}"
        )

    # 1. Observation.
    created = datetime.now().isoformat(timespec="seconds")

    files, records, directories, warnings = scan_directory(
        project_path,
        ignored
    )

    # 2. Preserve the previous state before anything is written.
    state, current_snapshot, current_raw = read_current_snapshot(snapshot_file)

    snapshot_id = "SNAP-{:03d}".format(
        next_snapshot_number(current_snapshot, history_directory)
    )

    if state == "snapshot":
        preserved_path = preserve_snapshot(
            current_snapshot["id"],
            current_raw,
            history_directory
        )
        preserved_path = preserved_path.replace("\\", "/")
        previous = f"{current_snapshot['id']} (preserved: {preserved_path})"
    elif state == "placeholder":
        previous = "none (placeholder template replaced)"
    else:
        previous = "none"

    # 3. Store the new snapshot.
    snapshot = build_snapshot(
        snapshot_id,
        created,
        project_name,
        project_path,
        records,
        directories
    )

    write_json_atomic(snapshot_file, snapshot)

    # 4. Report.
    status = STATUS_CREATED_WITH_WARNINGS if warnings else STATUS_CREATED

    snapshot_summary = {
        "lines": [
            f"ID: {snapshot_id}",
            f"Created: {created}",
            f"Status: {status}",
            f"Total files: {snapshot['statistics']['total_files']}",
            f"Total directories: {snapshot['statistics']['total_directories']}",
            f"Stored in: {snapshot_file}",
            f"Previous snapshot: {previous}",
        ],
        "warnings": warnings,
    }

    report = create_report(files, snapshot_summary)

    output_directory = output["report_directory"]

    os.makedirs(
        output_directory,
        exist_ok=True
    )

    report_file = os.path.join(
        output_directory,
        output["report_name"]
    )

    with open(
        report_file,
        "w",
        encoding="utf-8"
    ) as file:
        file.write(report)

    print(
        "Memory Core scan completed."
    )

    print(
        f"Snapshot {snapshot_id}: {status}"
    )


if __name__ == "__main__":
    try:
        main()
    except SnapshotError as error:
        print(f"Memory Core scan aborted: {error}")
        sys.exit(1)
