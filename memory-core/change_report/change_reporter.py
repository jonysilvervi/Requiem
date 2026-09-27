"""
REQUIEM Memory Core — Change Report Layer v0.1

Turns the latest comparison result into a structured change record
(CHG-NNN) and lets a human review it.

Boundaries:
- reads reports/latest_comparison.json (read-only);
- reads snapshots only to verify their hashes (read-only);
- writes only to review/changes/;
- does not run the comparator or the scanner;
- does not evaluate changes;
- does not modify project memory (database/, context/, README).

Run from inside change_report/:

    python change_reporter.py
    python change_reporter.py --approve CHG-001 --note "text"
    python change_reporter.py --reject CHG-001 --note "text"
"""

import os
import re
import sys
import json
import hashlib
import argparse
from datetime import datetime


VERSION = "0.1"

CONFIG_FILE = "change_report_config.json"

RECORD_FORMAT = "requiem-change-record"

COMPARISON_FORMAT = "requiem-comparison"
COMPARISON_FORMAT_VERSION = "0.1"

SNAPSHOT_ID_PATTERN = re.compile(r"^SNAP-(\d+)$")
COMPARISON_ID_PATTERN = re.compile(r"^CMP-(\d+)-(\d+)$")
RECORD_ID_PATTERN = re.compile(r"^CHG-(\d+)$")
HASH_PATTERN = re.compile(r"^[0-9a-f]{64}$")

STATUS_PENDING = "PENDING_REVIEW"
STATUS_APPROVED = "APPROVED"
STATUS_REJECTED = "REJECTED"
RECORD_STATUSES = (STATUS_PENDING, STATUS_APPROVED, STATUS_REJECTED)

COMPARISON_STATUSES = ("COMPLETED", "COMPLETED_WITH_WARNINGS")

CLASSES = ("added", "removed", "modified", "unchanged", "unverified")

# Order of entries inside a record.
ENTRY_CLASSES = ("added", "removed", "modified", "unverified")

PRESENCE_VALUES = ("both", "from_only", "to_only")
REASON_VALUES = ("hash_null_from", "hash_null_to", "hash_null_both")

ROOT_AREA = "(root)"


class ChangeReportError(Exception):
    """The action cannot be completed safely. Nothing has been written."""


# ---------------------------------------------------------------------------
# CONFIG AND ARGUMENTS
# ---------------------------------------------------------------------------

def load_config():
    if not os.path.isfile(CONFIG_FILE):
        raise ChangeReportError(
            f"{CONFIG_FILE} not found. "
            "Run the change reporter from inside the change_report/ directory."
        )

    try:
        with open(CONFIG_FILE, "r", encoding="utf-8-sig") as file:
            config = json.load(file)
    except (UnicodeDecodeError, json.JSONDecodeError):
        raise ChangeReportError(f"{CONFIG_FILE} is not valid JSON.")

    required = {
        "input": ("comparison_result", "current_snapshot", "snapshot_history_directory"),
        "output": ("changes_directory",),
    }

    for section, keys in required.items():
        if not isinstance(config.get(section), dict):
            raise ChangeReportError(f"{CONFIG_FILE}: section '{section}' is missing.")

        for key in keys:
            if not isinstance(config[section].get(key), str) or not config[section][key]:
                raise ChangeReportError(f"{CONFIG_FILE}: '{section}.{key}' is missing.")

    return config


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="REQUIEM Memory Core — Change Report Layer v" + VERSION
    )
    parser.add_argument(
        "--approve", metavar="CHG-NNN",
        help="approve a pending change record"
    )
    parser.add_argument(
        "--reject", metavar="CHG-NNN",
        help="reject a pending change record"
    )
    parser.add_argument(
        "--note", metavar="TEXT",
        help="review note (used with --approve or --reject)"
    )
    arguments = parser.parse_args()

    if arguments.approve and arguments.reject:
        raise ChangeReportError("--approve and --reject cannot be used together.")

    if arguments.note is not None and not (arguments.approve or arguments.reject):
        raise ChangeReportError("--note can be used only with --approve or --reject.")

    return arguments


# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------

def now():
    return datetime.now().isoformat(timespec="seconds")


def sha256_bytes(raw):
    return hashlib.sha256(raw).hexdigest()


def read_bytes(path, label):
    if not os.path.isfile(path):
        raise ChangeReportError(f"{label} not found: {path}")

    try:
        with open(path, "rb") as file:
            return file.read()
    except OSError as error:
        raise ChangeReportError(f"{label} cannot be read: {path} ({error.strerror}).")


def parse_json(raw, path, label):
    try:
        return json.loads(raw.decode("utf-8-sig"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        raise ChangeReportError(f"{label} is not valid JSON: {path}")


def number(pattern, value):
    return int(pattern.match(value).group(1))


def is_int(value):
    return isinstance(value, int) and not isinstance(value, bool)


def is_hash(value):
    return isinstance(value, str) and HASH_PATTERN.match(value) is not None


def area_of(path):
    return path.split("/", 1)[0] if "/" in path else ROOT_AREA


# ---------------------------------------------------------------------------
# COMPARISON RESULT (read-only)
# ---------------------------------------------------------------------------

def validate_comparison(data, path):

    def fail(message):
        raise ChangeReportError(f"{path}: {message}")

    if not isinstance(data, dict):
        fail("comparison result is not a JSON object.")

    if data.get("format") != COMPARISON_FORMAT:
        fail(f"unknown format (expected '{COMPARISON_FORMAT}').")

    if data.get("format_version") != COMPARISON_FORMAT_VERSION:
        fail(f"unsupported format_version (expected '{COMPARISON_FORMAT_VERSION}').")

    if not isinstance(data.get("id"), str) or not COMPARISON_ID_PATTERN.match(data["id"]):
        fail("missing or invalid comparison id.")

    if not isinstance(data.get("generated"), str):
        fail("missing 'generated'.")

    if data.get("status") not in COMPARISON_STATUSES:
        fail("missing or invalid 'status'.")

    for side in ("from", "to"):
        value = data.get(side)
        if not isinstance(value, dict) \
                or not isinstance(value.get("id"), str) \
                or not SNAPSHOT_ID_PATTERN.match(value["id"]) \
                or not isinstance(value.get("created"), str) \
                or not isinstance(value.get("source"), str) \
                or not is_hash(value.get("source_sha256")):
            fail(f"missing or invalid '{side}'.")

    project = data.get("project")
    if not isinstance(project, dict) \
            or not isinstance(project.get("name"), str) \
            or not isinstance(project.get("target"), str):
        fail("missing or invalid 'project'.")

    summary = data.get("summary")
    summary_keys = CLASSES + (
        "files_from", "files_to", "directories_from", "directories_to"
    )
    if not isinstance(summary, dict) or not all(is_int(summary.get(k)) for k in summary_keys):
        fail("missing or invalid 'summary'.")

    changes = data.get("changes")
    if not isinstance(changes, dict) or not all(isinstance(changes.get(k), list) for k in CLASSES):
        fail("missing or invalid 'changes'.")

    warnings = data.get("warnings")
    if not isinstance(warnings, list) or not all(isinstance(w, str) for w in warnings):
        fail("missing or invalid 'warnings'.")

    seen = set()

    def check_path(item, where):
        if not isinstance(item, dict) or not isinstance(item.get("path"), str) or not item["path"]:
            fail(f"{where}: missing or invalid 'path'.")
        if item["path"] in seen:
            fail(f"'{item['path']}' appears in more than one entry.")
        seen.add(item["path"])

    def check_side(side, where, with_extension, allow_null_hash):
        if not isinstance(side, dict) or not is_int(side.get("size")) \
                or not isinstance(side.get("modified"), str):
            fail(f"{where}: invalid file metadata.")
        if with_extension and not isinstance(side.get("extension"), str):
            fail(f"{where}: invalid 'extension'.")
        if side.get("hash") is None:
            if not allow_null_hash:
                fail(f"{where}: null hash outside the unverified class.")
        elif not is_hash(side.get("hash")):
            fail(f"{where}: invalid hash.")

    for item in changes["added"] + changes["removed"]:
        check_path(item, "added/removed entry")
        check_side(item, f"'{item['path']}'", True, False)

    for item in changes["modified"]:
        check_path(item, "modified entry")
        if not isinstance(item.get("changed_fields"), list):
            fail(f"'{item['path']}': invalid 'changed_fields'.")
        check_side(item.get("from"), f"'{item['path']}' (from)", False, False)
        check_side(item.get("to"), f"'{item['path']}' (to)", False, False)
        if item["from"]["hash"] == item["to"]["hash"]:
            fail(f"'{item['path']}': modified entry with equal hashes.")

    for item in changes["unchanged"]:
        check_path(item, "unchanged entry")
        if not isinstance(item.get("changed_fields"), list):
            fail(f"'{item['path']}': invalid 'changed_fields'.")

    for item in changes["unverified"]:
        check_path(item, "unverified entry")
        if item.get("presence") not in PRESENCE_VALUES or item.get("reason") not in REASON_VALUES:
            fail(f"'{item['path']}': invalid 'presence' or 'reason'.")
        for side in ("from", "to"):
            if item.get(side) is not None:
                check_side(item[side], f"'{item['path']}' ({side})", True, True)

    for name in CLASSES:
        if summary[name] != len(changes[name]):
            fail(f"summary.{name} is {summary[name]}, but {len(changes[name])} entries are listed.")

    in_from = sum(1 for u in changes["unverified"] if u["presence"] in ("both", "from_only"))
    in_to = sum(1 for u in changes["unverified"] if u["presence"] in ("both", "to_only"))

    counted_from = summary["removed"] + summary["modified"] + summary["unchanged"] + in_from
    counted_to = summary["added"] + summary["modified"] + summary["unchanged"] + in_to

    if counted_from != summary["files_from"] or counted_to != summary["files_to"]:
        fail("classified files do not add up to files_from / files_to.")


def load_comparison(config):
    path = config["input"]["comparison_result"]
    raw = read_bytes(path, "Comparison result")
    data = parse_json(raw, path, "Comparison result")

    validate_comparison(data, path)

    return data, sha256_bytes(raw)


# ---------------------------------------------------------------------------
# SNAPSHOT VERIFICATION (read-only)
# ---------------------------------------------------------------------------

def find_snapshot_file(snapshot_id, config):
    history_file = os.path.join(
        config["input"]["snapshot_history_directory"],
        f"{snapshot_id}.json"
    )

    if os.path.isfile(history_file):
        return history_file

    current_file = config["input"]["current_snapshot"]

    if os.path.isfile(current_file):
        data = parse_json(read_bytes(current_file, "Current snapshot"), current_file, "Current snapshot")

        if isinstance(data, dict) and data.get("id") == snapshot_id:
            return current_file

    return None


def verify_snapshots(comparison, config):
    """The comparison must describe the snapshots stored now, byte for byte."""

    for side in ("from", "to"):
        snapshot_id = comparison[side]["id"]
        path = find_snapshot_file(snapshot_id, config)

        if path is None:
            raise ChangeReportError(
                f"Snapshot {snapshot_id} used by {comparison['id']} is not found "
                "(neither current snapshot nor history)."
            )

        actual = sha256_bytes(read_bytes(path, "Snapshot"))

        if actual != comparison[side]["source_sha256"]:
            raise ChangeReportError(
                f"Snapshot {snapshot_id} ({path}) does not match {comparison['id']} "
                "(different SHA-256). The comparison is outdated or the snapshot was changed. "
                "Run the comparator again."
            )


# ---------------------------------------------------------------------------
# CHANGE RECORDS (review/changes/)
# ---------------------------------------------------------------------------

def validate_record(data, path, expected_id):

    def fail(message):
        raise ChangeReportError(f"{path}: {message}")

    if not isinstance(data, dict):
        fail("change record is not a JSON object.")

    if data.get("format") != RECORD_FORMAT or data.get("format_version") != VERSION:
        fail("unknown change record format or version.")

    if data.get("id") != expected_id:
        fail(f"contains id {data.get('id')}, expected {expected_id}.")

    if not isinstance(data.get("created"), str):
        fail("missing 'created'.")

    status = data.get("status")
    if status not in RECORD_STATUSES:
        fail("missing or invalid 'status'.")

    review = data.get("review")
    if not isinstance(review, dict) or not all(k in review for k in ("decision", "reviewed", "note")):
        fail("missing or invalid 'review'.")

    if status == STATUS_PENDING:
        if review["decision"] is not None or review["reviewed"] is not None:
            fail("pending record contains a review decision.")
    else:
        if review["decision"] != status or not isinstance(review["reviewed"], str):
            fail("review decision does not match status.")

    if review["note"] is not None and not isinstance(review["note"], str):
        fail("invalid review note.")

    comparison = data.get("comparison")
    if not isinstance(comparison, dict) or not isinstance(comparison.get("id"), str) \
            or not is_hash(comparison.get("result_sha256")):
        fail("missing or invalid 'comparison'.")

    for side in ("from", "to"):
        value = data.get(side)
        if not isinstance(value, dict) or not isinstance(value.get("id"), str) \
                or not SNAPSHOT_ID_PATTERN.match(value["id"]) \
                or not is_hash(value.get("source_sha256")):
            fail(f"missing or invalid '{side}'.")

    project = data.get("project")
    if not isinstance(project, dict) \
            or not isinstance(project.get("name"), str) \
            or not isinstance(project.get("target"), str):
        fail("missing or invalid 'project'.")

    if not isinstance(data.get("summary"), dict) \
            or not isinstance(data.get("no_changes"), bool) \
            or not isinstance(data.get("areas"), list) \
            or not isinstance(data.get("entries"), list) \
            or not isinstance(data.get("warnings"), list):
        fail("missing or invalid record content.")


def record_paths(changes_directory, record_id):
    return (
        os.path.join(changes_directory, f"{record_id}.json"),
        os.path.join(changes_directory, f"{record_id}.md"),
    )


def load_records(changes_directory):
    """Returns records sorted by number. Every existing record must be valid."""

    records = []

    if not os.path.isdir(changes_directory):
        return records

    for name in os.listdir(changes_directory):
        stem, extension = os.path.splitext(name)

        if extension != ".json" or not RECORD_ID_PATTERN.match(stem):
            continue

        path = os.path.join(changes_directory, name)
        data = parse_json(read_bytes(path, "Change record"), path, "Change record")
        validate_record(data, path, stem)
        records.append(data)

    records.sort(key=lambda record: number(RECORD_ID_PATTERN, record["id"]))

    return records


def check_chain(comparison, records):
    a = comparison["from"]["id"]
    b = comparison["to"]["id"]

    if a == b:
        raise ChangeReportError(
            f"{comparison['id']} compares {a} with itself. "
            "A change record needs two different snapshots."
        )

    for record in records:
        if record["from"]["id"] == a and record["to"]["id"] == b:
            raise ChangeReportError(
                f"{a} -> {b} is already recorded as {record['id']}. "
                "No new change record was created."
            )

    if not records:
        return

    last = records[-1]
    last_to = last["to"]["id"]

    if last["project"]["name"] != comparison["project"]["name"] \
            or last["project"]["target"] != comparison["project"]["target"]:
        raise ChangeReportError(
            f"{comparison['id']} belongs to another project than {last['id']}."
        )

    if a != last_to:
        if number(SNAPSHOT_ID_PATTERN, b) > number(SNAPSHOT_ID_PATTERN, last_to):
            hint = (
                "Run from comparison/: "
                f"python comparator.py --from {last_to} --to {b}"
            )
        else:
            hint = f"{b} is not newer than {last_to}. There is nothing new to record."

        raise ChangeReportError(
            f"Chain break: the last record {last['id']} ends at {last_to}, "
            f"but {comparison['id']} starts at {a}. {hint}"
        )


# ---------------------------------------------------------------------------
# BUILD RECORD
# Facts only. The only addition is mechanical grouping by top-level folder.
# ---------------------------------------------------------------------------

def side_metadata(side, keys):
    if side is None:
        return None

    return {key: side[key] for key in keys if key in side}


def build_entries(record_id, changes):
    entries = []
    full = ("size", "extension", "modified", "hash")
    short = ("size", "modified", "hash")

    for name in ENTRY_CLASSES:
        for item in sorted(changes[name], key=lambda i: i["path"]):
            entry = {
                "entry": None,
                "class": name,
                "path": item["path"],
                "area": area_of(item["path"]),
            }

            if name == "added":
                entry["from"] = None
                entry["to"] = side_metadata(item, full)
            elif name == "removed":
                entry["from"] = side_metadata(item, full)
                entry["to"] = None
            elif name == "modified":
                entry["changed_fields"] = list(item["changed_fields"])
                entry["from"] = side_metadata(item["from"], short)
                entry["to"] = side_metadata(item["to"], short)
            else:
                entry["presence"] = item["presence"]
                entry["reason"] = item["reason"]
                entry["from"] = side_metadata(item["from"], full)
                entry["to"] = side_metadata(item["to"], full)

            entries.append(entry)

    for index, entry in enumerate(entries, start=1):
        entry["entry"] = f"{record_id}/{index}"

    return entries


def build_areas(entries):
    areas = {}

    for entry in entries:
        counts = areas.setdefault(entry["area"], {
            "area": entry["area"], "added": 0, "removed": 0, "modified": 0, "unverified": 0,
        })
        counts[entry["class"]] += 1

    return [areas[name] for name in sorted(areas)]


def build_record(record_id, comparison, comparison_sha256):
    changes = comparison["changes"]
    summary = comparison["summary"]

    entries = build_entries(record_id, changes)

    no_changes = (
        summary["added"] + summary["removed"] + summary["modified"] + summary["unverified"]
    ) == 0

    warnings = []

    if summary["unverified"]:
        warnings.append(
            f"{summary['unverified']} unverified file(s): content could not be verified (null hash)."
        )

    for warning in comparison["warnings"]:
        warnings.append(f"Comparison: {warning}")

    return {
        "format": RECORD_FORMAT,
        "format_version": VERSION,
        "id": record_id,
        "created": now(),
        "status": STATUS_PENDING,
        "review": {"decision": None, "reviewed": None, "note": None},

        "comparison": {
            "id": comparison["id"],
            "generated": comparison["generated"],
            "status": comparison["status"],
            "result_sha256": comparison_sha256,
        },
        "from": {
            "id": comparison["from"]["id"],
            "created": comparison["from"]["created"],
            "source_sha256": comparison["from"]["source_sha256"],
        },
        "to": {
            "id": comparison["to"]["id"],
            "created": comparison["to"]["created"],
            "source_sha256": comparison["to"]["source_sha256"],
        },
        "project": {
            "name": comparison["project"]["name"],
            "target": comparison["project"]["target"],
        },

        "summary": dict(summary),
        "no_changes": no_changes,

        "areas": build_areas(entries),
        "entries": entries,

        "warnings": warnings,
    }


# ---------------------------------------------------------------------------
# REPORT (.md)
# ---------------------------------------------------------------------------

def describe_side(side):
    if side is None:
        return "absent"

    parts = [f"size {side['size']}", f"modified {side['modified']}"]
    parts.append(f"hash {side['hash'] if side['hash'] is not None else 'null'}")

    return ", ".join(parts)


def create_markdown(record):
    summary = record["summary"]
    review = record["review"]
    lines = []

    lines.append("# REQUIEM MEMORY CORE CHANGE RECORD")
    lines.append("")
    lines.append(f"Record: {record['id']}")
    lines.append(f"Created: {record['created']}")
    lines.append(f"Status: {record['status']}")
    lines.append(f"Project: {record['project']['name']} ({record['project']['target']})")
    lines.append("")

    lines.append("## Review")
    lines.append("")
    lines.append(f"Decision: {review['decision'] or 'pending'}")
    lines.append("")
    lines.append(f"Reviewed: {review['reviewed'] or '-'}")
    lines.append("")
    lines.append(f"Note: {review['note'] if review['note'] else '-'}")
    lines.append("")

    lines.append("## Source")
    lines.append("")
    lines.append(
        f"Comparison: {record['comparison']['id']} "
        f"(generated {record['comparison']['generated']}, {record['comparison']['status']})"
    )
    lines.append("")
    lines.append("| | Snapshot | Created |")
    lines.append("|---|---|---|")
    lines.append(f"| From | {record['from']['id']} | {record['from']['created']} |")
    lines.append(f"| To | {record['to']['id']} | {record['to']['created']} |")
    lines.append("")

    lines.append("## Summary")
    lines.append("")
    lines.append("| Class | Files |")
    lines.append("|---|---|")
    for name in CLASSES:
        lines.append(f"| {name.capitalize()} | {summary[name]} |")
    lines.append("")
    lines.append(f"Files: {summary['files_from']} -> {summary['files_to']}")
    lines.append("")
    lines.append(f"Directories: {summary['directories_from']} -> {summary['directories_to']}")
    lines.append("")
    lines.append(f"No changes: {'yes' if record['no_changes'] else 'no'}")
    lines.append("")

    unverified = [e for e in record["entries"] if e["class"] == "unverified"]
    lines.append("## UNVERIFIED FILES")
    lines.append("")
    if unverified:
        lines.append("Content of these files could not be verified (null hash).")
        lines.append("")
        for entry in unverified:
            lines.append(
                f"- {entry['entry']} `{entry['path']}` — "
                f"presence: {entry['presence']}, reason: {entry['reason']}"
            )
            lines.append(f"  - from: {describe_side(entry['from'])}")
            lines.append(f"  - to: {describe_side(entry['to'])}")
    else:
        lines.append("- none")
    lines.append("")

    lines.append("## Areas")
    lines.append("")
    if record["areas"]:
        lines.append("| Area | Added | Removed | Modified | Unverified |")
        lines.append("|---|---|---|---|---|")
        for area in record["areas"]:
            lines.append(
                f"| {area['area']} | {area['added']} | {area['removed']} | "
                f"{area['modified']} | {area['unverified']} |"
            )
    else:
        lines.append("- none")
    lines.append("")

    for name in ("added", "removed", "modified"):
        lines.append(f"## {name.capitalize()}")
        lines.append("")
        items = [e for e in record["entries"] if e["class"] == name]
        if not items:
            lines.append("- none")
        for entry in items:
            if name == "added":
                lines.append(f"- {entry['entry']} `{entry['path']}` — {describe_side(entry['to'])}")
            elif name == "removed":
                lines.append(f"- {entry['entry']} `{entry['path']}` — {describe_side(entry['from'])}")
            else:
                lines.append(f"- {entry['entry']} `{entry['path']}`")
                lines.append(f"  - changed fields: {', '.join(entry['changed_fields'])}")
                for field in ("size", "modified", "hash"):
                    before = entry["from"][field]
                    after = entry["to"][field]
                    if before != after:
                        lines.append(f"  - {field}: {before} -> {after}")
        lines.append("")

    lines.append("## Warnings")
    lines.append("")
    if record["warnings"]:
        for warning in record["warnings"]:
            lines.append(f"- {warning}")
    else:
        lines.append("- none")
    lines.append("")

    if record["status"] == STATUS_PENDING:
        lines.append("## How to review")
        lines.append("")
        lines.append("Run from change_report/:")
        lines.append("")
        lines.append("```")
        lines.append(f"python change_reporter.py --approve {record['id']} --note \"...\"")
        lines.append(f"python change_reporter.py --reject {record['id']} --note \"...\"")
        lines.append("```")
        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# WRITE
# Both files are fully written to .tmp first, then replaced.
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

        raise ChangeReportError(
            f"Could not write output ({error}). Existing files were left untouched."
        )

    for temporary, path in temporaries:
        try:
            os.replace(temporary, path)
        except OSError as error:
            raise ChangeReportError(
                f"Could not replace {path} ({error}). "
                f"The complete new version is kept in {temporary}."
            )


def record_texts(record, changes_directory):
    json_path, md_path = record_paths(changes_directory, record["id"])

    return [
        (json_path, json.dumps(record, indent=2, ensure_ascii=False) + "\n"),
        (md_path, create_markdown(record)),
    ]


# ---------------------------------------------------------------------------
# ACTIONS
# ---------------------------------------------------------------------------

def create_record(config):
    changes_directory = config["output"]["changes_directory"]

    # 1. Comparison result (read-only) and snapshot verification (read-only).
    comparison, comparison_sha256 = load_comparison(config)
    verify_snapshots(comparison, config)

    # 2. Existing records and chain rule.
    records = load_records(changes_directory)
    check_chain(comparison, records)

    # 3. New record.
    next_number = max(
        [number(RECORD_ID_PATTERN, r["id"]) for r in records], default=0
    ) + 1
    record_id = "CHG-{:03d}".format(next_number)

    for path in record_paths(changes_directory, record_id):
        if os.path.exists(path):
            raise ChangeReportError(f"{path} already exists. Nothing was overwritten.")

    record = build_record(record_id, comparison, comparison_sha256)

    # 4. Write (only review/changes/).
    os.makedirs(changes_directory, exist_ok=True)
    write_outputs_atomic(record_texts(record, changes_directory))

    summary = record["summary"]

    print("Memory Core change report completed.")
    print(f"Change record {record_id}: {record['status']}")
    print(f"{record['from']['id']} -> {record['to']['id']} ({record['comparison']['id']})")
    print(
        f"Added: {summary['added']} | Removed: {summary['removed']} | "
        f"Modified: {summary['modified']} | Unchanged: {summary['unchanged']} | "
        f"Unverified: {summary['unverified']}"
    )
    if record["no_changes"]:
        print("No changes between these snapshots.")


def review_record(config, record_id, decision, note):
    if not RECORD_ID_PATTERN.match(record_id):
        raise ChangeReportError(f"Invalid change record id: {record_id} (expected CHG-NNN).")

    changes_directory = config["output"]["changes_directory"]
    json_path, _ = record_paths(changes_directory, record_id)

    if not os.path.isfile(json_path):
        raise ChangeReportError(f"Change record {record_id} not found.")

    record = parse_json(read_bytes(json_path, "Change record"), json_path, "Change record")
    validate_record(record, json_path, record_id)

    if record["status"] != STATUS_PENDING:
        raise ChangeReportError(
            f"{record_id} is already reviewed ({record['status']}). "
            "A reviewed record cannot be changed."
        )

    if note is not None:
        note = note.strip() or None

    record["status"] = decision
    record["review"] = {
        "decision": decision,
        "reviewed": now(),
        "note": note,
    }

    write_outputs_atomic(record_texts(record, changes_directory))

    print("Memory Core change report completed.")
    print(f"Change record {record_id}: {decision}")

    if decision == STATUS_APPROVED and note is None:
        print("No note: an event will not be proposed for this record.")


# ---------------------------------------------------------------------------

def main():

    config = load_config()

    arguments = parse_arguments()

    if arguments.approve:
        review_record(config, arguments.approve, STATUS_APPROVED, arguments.note)
    elif arguments.reject:
        review_record(config, arguments.reject, STATUS_REJECTED, arguments.note)
    else:
        create_record(config)


if __name__ == "__main__":
    try:
        main()
    except ChangeReportError as error:
        print(f"Memory Core change report aborted: {error}")
        sys.exit(1)
