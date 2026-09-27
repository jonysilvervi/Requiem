"""
REQUIEM Memory Core — Comparison Layer v0.1

Compares two stored snapshots and answers:
"What changed between these states?"

Read-only layer:
- reads snapshots from database/ (never writes there);
- does not run the scanner;
- does not touch project files or documentation;
- writes only reports/latest_comparison.json and reports/latest_comparison.md.

Run from inside comparison/:

    python comparator.py
    python comparator.py --from SNAP-001 --to SNAP-003
"""

import os
import re
import sys
import json
import hashlib
import argparse
from datetime import datetime


VERSION = "0.1"

CONFIG_FILE = "comparison_config.json"

RESULT_FORMAT = "requiem-comparison"

SNAPSHOT_ID_PATTERN = re.compile(r"^SNAP-(\d+)$")

HASH_PATTERN = re.compile(r"^[0-9a-f]{64}$")

# Fields compared for files present in both snapshots.
COMPARED_FIELDS = ("size", "extension", "modified", "hash")

STATUS_COMPLETED = "COMPLETED"
STATUS_COMPLETED_WITH_WARNINGS = "COMPLETED_WITH_WARNINGS"

PRESENCE_BOTH = "both"
PRESENCE_FROM_ONLY = "from_only"
PRESENCE_TO_ONLY = "to_only"

REASON_HASH_NULL_FROM = "hash_null_from"
REASON_HASH_NULL_TO = "hash_null_to"
REASON_HASH_NULL_BOTH = "hash_null_both"

# Memory Core root = parent of the comparison/ directory.
MEMORY_CORE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class ComparisonError(Exception):
    """The comparison cannot be completed safely. Nothing has been written."""


# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------

def load_config():
    if not os.path.isfile(CONFIG_FILE):
        raise ComparisonError(
            f"{CONFIG_FILE} not found. "
            "Run the comparator from inside the comparison/ directory."
        )

    try:
        with open(CONFIG_FILE, "r", encoding="utf-8-sig") as file:
            config = json.load(file)
    except (UnicodeDecodeError, json.JSONDecodeError):
        raise ComparisonError(f"{CONFIG_FILE} is not valid JSON.")

    required = {
        "input": ("current_snapshot", "snapshot_history_directory"),
        "output": ("report_directory", "result_name", "report_name"),
    }

    for section, keys in required.items():
        if not isinstance(config.get(section), dict):
            raise ComparisonError(f"{CONFIG_FILE}: section '{section}' is missing.")

        for key in keys:
            if not isinstance(config[section].get(key), str) or not config[section][key]:
                raise ComparisonError(f"{CONFIG_FILE}: '{section}.{key}' is missing.")

    return config


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="REQUIEM Memory Core — Comparison Layer v" + VERSION
    )
    parser.add_argument(
        "--from", dest="from_id", metavar="SNAP-NNN",
        help="older snapshot id (use together with --to)"
    )
    parser.add_argument(
        "--to", dest="to_id", metavar="SNAP-NNN",
        help="newer snapshot id (use together with --from)"
    )
    arguments = parser.parse_args()

    if bool(arguments.from_id) != bool(arguments.to_id):
        raise ComparisonError(
            "--from and --to must be used together (or neither for the default pair)."
        )

    return arguments


# ---------------------------------------------------------------------------
# LOAD (Storage, read-only)
# Reads snapshots. Never writes to database/.
# ---------------------------------------------------------------------------

def snapshot_number(snapshot_id):
    return int(SNAPSHOT_ID_PATTERN.match(snapshot_id).group(1))


def memory_core_relative(path):
    absolute = os.path.abspath(path)

    try:
        relative = os.path.relpath(absolute, MEMORY_CORE_ROOT)
    except ValueError:
        # Different drive on Windows: keep the absolute path.
        relative = absolute

    return relative.replace("\\", "/")


def read_snapshot_file(path):
    """
    Reads the file once.
    Returns (data, source_sha256).
    """

    if not os.path.isfile(path):
        raise ComparisonError(f"{path}: snapshot file not found.")

    try:
        with open(path, "rb") as file:
            raw = file.read()
    except OSError as error:
        raise ComparisonError(f"{path}: cannot be read ({error.strerror}).")

    try:
        data = json.loads(raw.decode("utf-8-sig"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        raise ComparisonError(f"{path}: not valid JSON (corrupted snapshot).")

    return data, hashlib.sha256(raw).hexdigest()


def list_history(history_directory):
    """Returns {snapshot_id: file_path} for SNAP-NNN.json files in history."""

    history = {}

    if not os.path.isdir(history_directory):
        return history

    for name in os.listdir(history_directory):
        stem, extension = os.path.splitext(name)

        if extension == ".json" and SNAPSHOT_ID_PATTERN.match(stem):
            history[stem] = os.path.join(history_directory, name)

    return history


def load_snapshot(path, expected_id=None):
    data, source_sha256 = read_snapshot_file(path)

    if isinstance(data, dict) and set(data.keys()) == {"files"}:
        raise ComparisonError(
            f"{path}: placeholder template, not a snapshot."
        )

    validate_snapshot(data, path)

    if expected_id is not None and data["id"] != expected_id:
        raise ComparisonError(
            f"{path}: contains id {data['id']}, expected {expected_id}."
        )

    return {
        "data": data,
        "path": path,
        "source": memory_core_relative(path),
        "source_sha256": source_sha256,
    }


def resolve_pair(arguments, config):
    current_file = config["input"]["current_snapshot"]
    history = list_history(config["input"]["snapshot_history_directory"])

    if not arguments.from_id:
        # Default pair: current snapshot <- nearest older snapshot in history.
        to_snapshot = load_snapshot(current_file)
        to_number = snapshot_number(to_snapshot["data"]["id"])

        older = [
            snapshot_id for snapshot_id in history
            if snapshot_number(snapshot_id) < to_number
        ]

        if not older:
            raise ComparisonError(
                f"No previous snapshot older than {to_snapshot['data']['id']} in history."
            )

        from_id = max(older, key=snapshot_number)
        from_snapshot = load_snapshot(history[from_id], from_id)

        return from_snapshot, to_snapshot

    return (
        resolve_by_id(arguments.from_id, current_file, history),
        resolve_by_id(arguments.to_id, current_file, history),
    )


def resolve_by_id(snapshot_id, current_file, history):
    if not SNAPSHOT_ID_PATTERN.match(snapshot_id):
        raise ComparisonError(
            f"Invalid snapshot id: {snapshot_id} (expected SNAP-NNN)."
        )

    if snapshot_id in history:
        return load_snapshot(history[snapshot_id], snapshot_id)

    if os.path.isfile(current_file):
        current = load_snapshot(current_file)

        if current["data"]["id"] == snapshot_id:
            return current

    raise ComparisonError(
        f"Snapshot {snapshot_id} not found (neither current snapshot nor history)."
    )


# ---------------------------------------------------------------------------
# VALIDATION
# A snapshot is accepted only if it matches REQUIEM_SNAPSHOT_MODEL.
# ---------------------------------------------------------------------------

def is_int(value):
    return isinstance(value, int) and not isinstance(value, bool)


def validate_snapshot(data, path):

    def fail(message):
        raise ComparisonError(f"{path}: {message}")

    if not isinstance(data, dict):
        fail("snapshot is not a JSON object.")

    if not isinstance(data.get("id"), str) or not SNAPSHOT_ID_PATTERN.match(data["id"]):
        fail("missing or invalid snapshot id.")

    if not isinstance(data.get("created"), str):
        fail("missing 'created'.")

    project = data.get("project")
    if not isinstance(project, dict) \
            or not isinstance(project.get("name"), str) \
            or not isinstance(project.get("target"), str):
        fail("missing or invalid 'project'.")

    environment = data.get("environment")
    if not isinstance(environment, dict) \
            or not isinstance(environment.get("machine_path"), str) \
            or not isinstance(environment.get("platform"), str):
        fail("missing or invalid 'environment'.")

    statistics = data.get("statistics")
    if not isinstance(statistics, dict) \
            or not is_int(statistics.get("total_files")) \
            or not is_int(statistics.get("total_directories")):
        fail("missing or invalid 'statistics'.")

    files = data.get("files")
    if not isinstance(files, list):
        fail("missing or invalid 'files'.")

    seen = set()

    for index, record in enumerate(files):
        where = f"files[{index}]"

        if not isinstance(record, dict):
            fail(f"{where} is not an object.")

        file_path = record.get("path")
        if not isinstance(file_path, str) or not file_path:
            fail(f"{where}: missing or invalid 'path'.")

        where = f"file '{file_path}'"

        if file_path in seen:
            fail(f"{where} is listed more than once.")
        seen.add(file_path)

        if not is_int(record.get("size")) or record["size"] < 0:
            fail(f"{where}: invalid 'size'.")

        if not isinstance(record.get("extension"), str):
            fail(f"{where}: invalid 'extension'.")

        if not isinstance(record.get("modified"), str):
            fail(f"{where}: invalid 'modified'.")

        if "hash" not in record:
            fail(f"{where}: missing 'hash'.")

        file_hash = record["hash"]
        if file_hash is not None and \
                (not isinstance(file_hash, str) or not HASH_PATTERN.match(file_hash)):
            fail(f"{where}: invalid hash (expected 64 lowercase hex characters or null).")

    if statistics["total_files"] != len(files):
        fail(
            f"statistics.total_files is {statistics['total_files']}, "
            f"but {len(files)} files are listed."
        )


def check_compatibility(from_snapshot, to_snapshot):
    """Returns warnings. Raises ComparisonError for incompatible pairs."""

    a = from_snapshot["data"]
    b = to_snapshot["data"]

    if a["project"]["name"] != b["project"]["name"] \
            or a["project"]["target"] != b["project"]["target"]:
        raise ComparisonError(
            "Snapshots belong to different projects: "
            f"{a['id']} = {a['project']['name']}/{a['project']['target']}, "
            f"{b['id']} = {b['project']['name']}/{b['project']['target']}."
        )

    if snapshot_number(a["id"]) > snapshot_number(b["id"]):
        raise ComparisonError(
            f"--from {a['id']} is newer than --to {b['id']}. "
            "The older snapshot must be first."
        )

    warnings = []

    if a["environment"]["machine_path"] != b["environment"]["machine_path"]:
        warnings.append(
            "Different machine_path: "
            f"{a['environment']['machine_path']} -> {b['environment']['machine_path']}."
        )

    if a["environment"]["platform"] != b["environment"]["platform"]:
        warnings.append(
            "Different platform: "
            f"{a['environment']['platform']} -> {b['environment']['platform']}. "
            "Line endings may change hashes."
        )

    if a["id"] != b["id"] and a["created"] > b["created"]:
        warnings.append(
            f"{a['id']} was created after {b['id']} "
            f"({a['created']} > {b['created']})."
        )

    return warnings


# ---------------------------------------------------------------------------
# COMPARISON
# Facts derived from facts. No evaluation.
# ---------------------------------------------------------------------------

def full_record(record):
    return {
        "path": record["path"],
        "size": record["size"],
        "extension": record["extension"],
        "modified": record["modified"],
        "hash": record["hash"],
    }


def side_record(record):
    if record is None:
        return None

    return {
        "size": record["size"],
        "extension": record["extension"],
        "modified": record["modified"],
        "hash": record["hash"],
    }


def change_record(record):
    return {
        "size": record["size"],
        "modified": record["modified"],
        "hash": record["hash"],
    }


def compare_files(from_files, to_files):
    a = {record["path"]: record for record in from_files}
    b = {record["path"]: record for record in to_files}

    changes = {
        "added": [],
        "removed": [],
        "modified": [],
        "unchanged": [],
        "unverified": [],
    }

    for path in sorted(set(a) | set(b)):
        record_a = a.get(path)
        record_b = b.get(path)

        null_from = record_a is not None and record_a["hash"] is None
        null_to = record_b is not None and record_b["hash"] is None

        # 1. Content cannot be verified -> unverified, never forced elsewhere.
        if null_from or null_to:
            if record_a is not None and record_b is not None:
                presence = PRESENCE_BOTH
            elif record_a is not None:
                presence = PRESENCE_FROM_ONLY
            else:
                presence = PRESENCE_TO_ONLY

            if null_from and null_to:
                reason = REASON_HASH_NULL_BOTH
            elif null_from:
                reason = REASON_HASH_NULL_FROM
            else:
                reason = REASON_HASH_NULL_TO

            changes["unverified"].append({
                "path": path,
                "presence": presence,
                "reason": reason,
                "from": side_record(record_a),
                "to": side_record(record_b),
            })
            continue

        # 2. Present in one snapshot only.
        if record_a is None:
            changes["added"].append(full_record(record_b))
            continue

        if record_b is None:
            changes["removed"].append(full_record(record_a))
            continue

        # 3. Present in both, both hashes verified.
        changed_fields = [
            field for field in COMPARED_FIELDS
            if record_a[field] != record_b[field]
        ]

        if record_a["hash"] == record_b["hash"]:
            if record_a["size"] != record_b["size"]:
                raise ComparisonError(
                    f"'{path}': equal hash but different size "
                    f"({record_a['size']} vs {record_b['size']}). "
                    "A snapshot is corrupted."
                )

            changes["unchanged"].append({
                "path": path,
                "changed_fields": changed_fields,
            })
        else:
            changes["modified"].append({
                "path": path,
                "changed_fields": changed_fields,
                "from": change_record(record_a),
                "to": change_record(record_b),
            })

    return changes


def verify_invariants(changes, from_files, to_files):
    in_from = sum(
        1 for item in changes["unverified"]
        if item["presence"] in (PRESENCE_BOTH, PRESENCE_FROM_ONLY)
    )
    in_to = sum(
        1 for item in changes["unverified"]
        if item["presence"] in (PRESENCE_BOTH, PRESENCE_TO_ONLY)
    )

    counted_from = len(changes["removed"]) + len(changes["modified"]) \
        + len(changes["unchanged"]) + in_from
    counted_to = len(changes["added"]) + len(changes["modified"]) \
        + len(changes["unchanged"]) + in_to

    if counted_from != len(from_files) or counted_to != len(to_files):
        raise ComparisonError(
            "Self-check failed: classified files do not add up "
            f"(from {counted_from}/{len(from_files)}, to {counted_to}/{len(to_files)})."
        )


# ---------------------------------------------------------------------------
# RESULT
# ---------------------------------------------------------------------------

def build_result(from_snapshot, to_snapshot, changes, warnings, generated):
    a = from_snapshot["data"]
    b = to_snapshot["data"]

    comparison_id = "CMP-{:03d}-{:03d}".format(
        snapshot_number(a["id"]),
        snapshot_number(b["id"])
    )

    status = STATUS_COMPLETED_WITH_WARNINGS if warnings else STATUS_COMPLETED

    return {
        "format": RESULT_FORMAT,
        "format_version": VERSION,
        "id": comparison_id,
        "generated": generated,
        "status": status,

        "from": {
            "id": a["id"],
            "created": a["created"],
            "source": from_snapshot["source"],
            "source_sha256": from_snapshot["source_sha256"],
        },
        "to": {
            "id": b["id"],
            "created": b["created"],
            "source": to_snapshot["source"],
            "source_sha256": to_snapshot["source_sha256"],
        },

        "project": {
            "name": b["project"]["name"],
            "target": b["project"]["target"],
        },

        "environment": {
            "same_machine_path":
                a["environment"]["machine_path"] == b["environment"]["machine_path"],
            "same_platform":
                a["environment"]["platform"] == b["environment"]["platform"],
        },

        "summary": {
            "added": len(changes["added"]),
            "removed": len(changes["removed"]),
            "modified": len(changes["modified"]),
            "unchanged": len(changes["unchanged"]),
            "unverified": len(changes["unverified"]),
            "files_from": len(a["files"]),
            "files_to": len(b["files"]),
            "directories_from": a["statistics"]["total_directories"],
            "directories_to": b["statistics"]["total_directories"],
        },

        "changes": changes,

        "warnings": warnings,
    }


# ---------------------------------------------------------------------------
# REPORT
# ---------------------------------------------------------------------------

def describe_side(side):
    if side is None:
        return "absent"

    file_hash = side["hash"] if side["hash"] is not None else "null"

    return f"size {side['size']}, modified {side['modified']}, hash {file_hash}"


def create_report(result):
    summary = result["summary"]
    changes = result["changes"]
    lines = []

    lines.append("# REQUIEM MEMORY CORE COMPARISON REPORT")
    lines.append("")
    lines.append(f"Comparison: {result['id']}")
    lines.append(f"Generated: {result['generated']}")
    lines.append(f"Status: {result['status']}")
    lines.append(f"Project: {result['project']['name']} ({result['project']['target']})")
    lines.append("")

    lines.append("## Snapshots")
    lines.append("")
    lines.append("| | ID | Created | Source |")
    lines.append("|---|---|---|---|")
    for label, side in (("From", result["from"]), ("To", result["to"])):
        lines.append(f"| {label} | {side['id']} | {side['created']} | {side['source']} |")
    lines.append("")

    lines.append("## Summary")
    lines.append("")
    lines.append("| Class | Files |")
    lines.append("|---|---|")
    for name in ("added", "removed", "modified", "unchanged", "unverified"):
        lines.append(f"| {name.capitalize()} | {summary[name]} |")
    lines.append("")
    lines.append(f"Files: {summary['files_from']} -> {summary['files_to']}")
    lines.append("")
    lines.append(f"Directories: {summary['directories_from']} -> {summary['directories_to']}")
    lines.append("")

    lines.append("## Added")
    lines.append("")
    if changes["added"]:
        for item in changes["added"]:
            lines.append(f"- `{item['path']}` — {describe_side(item)}")
    else:
        lines.append("- none")
    lines.append("")

    lines.append("## Removed")
    lines.append("")
    if changes["removed"]:
        for item in changes["removed"]:
            lines.append(f"- `{item['path']}` — {describe_side(item)}")
    else:
        lines.append("- none")
    lines.append("")

    lines.append("## Modified")
    lines.append("")
    if changes["modified"]:
        for item in changes["modified"]:
            lines.append(f"- `{item['path']}`")
            lines.append(f"  - changed fields: {', '.join(item['changed_fields'])}")
            for field in ("size", "modified", "hash"):
                before = item["from"][field]
                after = item["to"][field]
                if before != after:
                    lines.append(f"  - {field}: {before} -> {after}")
    else:
        lines.append("- none")
    lines.append("")

    lines.append("## Unverified")
    lines.append("")
    if changes["unverified"]:
        for item in changes["unverified"]:
            lines.append(
                f"- `{item['path']}` — presence: {item['presence']}, reason: {item['reason']}"
            )
            lines.append(f"  - from: {describe_side(item['from'])}")
            lines.append(f"  - to: {describe_side(item['to'])}")
    else:
        lines.append("- none")
    lines.append("")

    lines.append("## Unchanged")
    lines.append("")
    lines.append(
        f"{summary['unchanged']} files. Full list: latest_comparison.json"
    )
    lines.append("")

    lines.append("## Warnings")
    lines.append("")
    if result["warnings"]:
        for warning in result["warnings"]:
            lines.append(f"- {warning}")
    else:
        lines.append("- none")
    lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# WRITE
# Both files are fully written to .tmp first, then replaced.
# A final file is never partially written.
# ---------------------------------------------------------------------------

def write_outputs_atomic(outputs):
    temporaries = []

    try:
        for path, text in outputs:
            temporary = path + ".tmp"

            with open(temporary, "w", encoding="utf-8", newline="\n") as file:
                file.write(text)
                file.flush()
                os.fsync(file.fileno())

            temporaries.append((temporary, path))

    except OSError as error:
        for temporary, _ in temporaries:
            try:
                os.remove(temporary)
            except OSError:
                pass

        raise ComparisonError(
            f"Could not write output ({error}). Existing reports were left untouched."
        )

    for temporary, path in temporaries:
        try:
            os.replace(temporary, path)
        except OSError as error:
            raise ComparisonError(
                f"Could not replace {path} ({error}). "
                f"The complete new version is kept in {temporary}."
            )


# ---------------------------------------------------------------------------

def main():

    config = load_config()

    arguments = parse_arguments()

    # 1. Load and validate both snapshots (read-only).
    from_snapshot, to_snapshot = resolve_pair(arguments, config)

    # 2. Compatibility.
    warnings = check_compatibility(from_snapshot, to_snapshot)

    # 3. Compare.
    from_files = from_snapshot["data"]["files"]
    to_files = to_snapshot["data"]["files"]

    changes = compare_files(from_files, to_files)

    # 4. Self-check.
    verify_invariants(changes, from_files, to_files)

    # 5. Build result and report.
    generated = datetime.now().isoformat(timespec="seconds")

    result = build_result(from_snapshot, to_snapshot, changes, warnings, generated)

    result_text = json.dumps(result, indent=2, ensure_ascii=False) + "\n"

    report_text = create_report(result)

    # 6. Write (only reports/).
    output = config["output"]
    output_directory = output["report_directory"]

    os.makedirs(output_directory, exist_ok=True)

    write_outputs_atomic([
        (os.path.join(output_directory, output["result_name"]), result_text),
        (os.path.join(output_directory, output["report_name"]), report_text),
    ])

    summary = result["summary"]

    print("Memory Core comparison completed.")
    print(f"Comparison {result['id']}: {result['status']}")
    print(
        f"Added: {summary['added']} | Removed: {summary['removed']} | "
        f"Modified: {summary['modified']} | Unchanged: {summary['unchanged']} | "
        f"Unverified: {summary['unverified']}"
    )


if __name__ == "__main__":
    try:
        main()
    except ComparisonError as error:
        print(f"Memory Core comparison aborted: {error}")
        sys.exit(1)
