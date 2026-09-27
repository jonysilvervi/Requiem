"""
REQUIEM Memory Core — Analysis Layer v0.1

Analyzes one change record (CHG-NNN) with deterministic rules:
category and zone of every changed file, and findings of rule matches.
Defined in context/REQUIEM_ANALYSIS_MODEL.md.

Boundaries:
- reads one change record, its two snapshots, the rules file and the
  architecture map (read-only);
- writes only reports/latest_analysis.json and reports/latest_analysis.md
  (paths fixed in the code);
- does not read project files;
- does not read or modify project memory (database/, context/, README);
- does not modify change records, context update proposals, rules or map;
- does not run other layers and is not run by them;
- does not evaluate changes and does not use AI.

Run from inside analysis/:

    python analyzer.py
    python analyzer.py --record CHG-001
"""

import os
import re
import sys
import json
import hashlib
import argparse
from datetime import datetime


VERSION = "0.1"

CONFIG_FILE = "analysis_config.json"

RESULT_FORMAT = "requiem-analysis"
RULES_FORMAT = "requiem-analysis-rules"
MAP_FORMAT = "requiem-architecture-map"
RECORD_FORMAT = "requiem-change-record"
RECORD_FORMAT_VERSION = "0.1"

# Output locations are fixed in the code (storage rule, section 15).
MEMORY_CORE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORT_DIRECTORY = os.path.join(MEMORY_CORE_ROOT, "reports")
RESULT_FILE = os.path.join(REPORT_DIRECTORY, "latest_analysis.json")
REPORT_FILE = os.path.join(REPORT_DIRECTORY, "latest_analysis.md")

SNAPSHOT_ID_PATTERN = re.compile(r"^SNAP-(\d+)$")
COMPARISON_ID_PATTERN = re.compile(r"^CMP-(\d+)-(\d+)$")
RECORD_ID_PATTERN = re.compile(r"^CHG-(\d+)$")
HASH_PATTERN = re.compile(r"^[0-9a-f]{64}$")
CATEGORY_ID_PATTERN = re.compile(r"^[a-z0-9-]+$")
ZONE_ID_PATTERN = re.compile(r"^[a-z0-9-]+$")
SIGNAL_ID_PATTERN = re.compile(r"^S-[A-Z0-9-]+$")
DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")

RECORD_STATUSES = ("PENDING_REVIEW", "APPROVED", "REJECTED")
STATUS_PENDING = "PENDING_REVIEW"
STATUS_REJECTED = "REJECTED"

STATUS_COMPLETED = "COMPLETED"
STATUS_COMPLETED_WITH_WARNINGS = "COMPLETED_WITH_WARNINGS"

MAP_STATUSES = ("DRAFT", "APPROVED")

# Order of entries inside a change record.
ENTRY_CLASSES = ("added", "removed", "modified", "unverified")

SUMMARY_KEYS = (
    "added", "removed", "modified", "unchanged", "unverified",
    "files_from", "files_to", "directories_from", "directories_to",
)

PRESENCE_VALUES = ("both", "from_only", "to_only")
REASON_VALUES = ("hash_null_from", "hash_null_to", "hash_null_both")

ROOT_AREA = "(root)"

UNMAPPED = "unmapped"
UNCATEGORIZED = "uncategorized"

LEVELS = ("attention", "notice", "info")

# Signal kinds are fixed in the code (section 8.1).
KIND_PARAMS = {
    "unverified": None,
    "attention_zone": None,
    "generated_zone": None,
    "paired_files": ("first", "second"),
    "rename_candidate": None,
    "case_candidate": None,
    "new_top_level": None,
    "empty_file": None,
    "size_delta": ("min_bytes", "min_ratio"),
    "category_changed": ("categories", "classes"),
    "unmapped": None,
    "uncategorized": None,
}

# Keys of the change record that form its facts (section 11.1).
FACT_KEYS = (
    "id", "comparison", "from", "to", "project",
    "summary", "no_changes", "areas", "entries",
)


class AnalysisError(Exception):
    """The analysis cannot be completed safely. Nothing has been written."""


# ---------------------------------------------------------------------------
# CONFIG AND ARGUMENTS
# ---------------------------------------------------------------------------

def load_config():
    if not os.path.isfile(CONFIG_FILE):
        raise AnalysisError(
            f"{CONFIG_FILE} not found. "
            "Run the analyzer from inside the analysis/ directory."
        )

    try:
        with open(CONFIG_FILE, "r", encoding="utf-8-sig") as file:
            config = json.load(file)
    except (UnicodeDecodeError, json.JSONDecodeError):
        raise AnalysisError(f"{CONFIG_FILE} is not valid JSON.")

    keys = (
        "changes_directory", "current_snapshot", "snapshot_history_directory",
        "rules", "architecture_map",
    )

    if not isinstance(config, dict) or not isinstance(config.get("input"), dict):
        raise AnalysisError(f"{CONFIG_FILE}: section 'input' is missing.")

    for key in keys:
        if not isinstance(config["input"].get(key), str) or not config["input"][key]:
            raise AnalysisError(f"{CONFIG_FILE}: 'input.{key}' is missing.")

    return config


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="REQUIEM Memory Core — Analysis Layer v" + VERSION
    )
    parser.add_argument(
        "--record", metavar="CHG-NNN",
        help="change record to analyze (default: the latest change record)"
    )
    arguments = parser.parse_args()

    if arguments.record is not None and not RECORD_ID_PATTERN.match(arguments.record):
        raise AnalysisError(f"Invalid change record id: {arguments.record} (expected CHG-NNN).")

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
        raise AnalysisError(f"{label} not found: {path}")

    try:
        with open(path, "rb") as file:
            return file.read()
    except OSError as error:
        raise AnalysisError(f"{label} cannot be read: {path} ({error.strerror}).")


def parse_json(raw, path, label):
    try:
        return json.loads(raw.decode("utf-8-sig"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        raise AnalysisError(f"{label} is not valid JSON: {path}")


def number(pattern, value):
    return int(pattern.match(value).group(1))


def is_int(value):
    return isinstance(value, int) and not isinstance(value, bool)


def is_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def is_hash(value):
    return isinstance(value, str) and HASH_PATTERN.match(value) is not None


def is_text(value):
    return isinstance(value, str) and value != ""


def area_of(path):
    return path.split("/", 1)[0] if "/" in path else ROOT_AREA


def entry_number(entry_id):
    return int(entry_id.rsplit("/", 1)[1])


def safe_print(text):
    """Console output must never fail because of the console encoding."""
    encoding = getattr(sys.stdout, "encoding", None) or "utf-8"
    print(text.encode(encoding, errors="replace").decode(encoding, errors="replace"))


# ---------------------------------------------------------------------------
# RULES FILE (section 9)
# ---------------------------------------------------------------------------

def validate_string_list(value, allow_empty):
    return isinstance(value, list) \
        and (allow_empty or len(value) > 0) \
        and all(is_text(item) for item in value)


def validate_rules(data, path):

    def fail(message):
        raise AnalysisError(f"{path}: {message}")

    if not isinstance(data, dict):
        fail("rules file is not a JSON object.")

    if data.get("format") != RULES_FORMAT:
        fail(f"unknown format (expected '{RULES_FORMAT}').")

    if data.get("format_version") != VERSION:
        fail(f"unsupported format_version (expected '{VERSION}').")

    if not is_int(data.get("revision")) or data["revision"] < 1:
        fail("'revision' must be an integer >= 1.")

    categories = data.get("categories")
    if not isinstance(categories, list):
        fail("missing or invalid 'categories'.")

    category_ids = []

    for index, category in enumerate(categories):
        where = f"categories[{index}]"

        if not isinstance(category, dict):
            fail(f"{where} is not an object.")

        category_id = category.get("id")
        if not isinstance(category_id, str) or not CATEGORY_ID_PATTERN.match(category_id):
            fail(f"{where}: invalid 'id' (lowercase letters, digits and '-').")
        if category_id == UNCATEGORIZED:
            fail(f"{where}: '{UNCATEGORIZED}' is a reserved category id.")
        if category_id in category_ids:
            fail(f"{where}: duplicate category id '{category_id}'.")
        category_ids.append(category_id)

        if not is_text(category.get("name")):
            fail(f"category '{category_id}': missing or invalid 'name'.")

        names = category.get("names")
        suffixes = category.get("suffixes")

        if not validate_string_list(names, True) or any("/" in n for n in names):
            fail(f"category '{category_id}': 'names' must be a list of file names without '/'.")

        if not validate_string_list(suffixes, True) or any("/" in s for s in suffixes):
            fail(f"category '{category_id}': 'suffixes' must be a list of non-empty strings without '/'.")

        if not names and not suffixes:
            fail(f"category '{category_id}': at least one name or suffix is required.")

    signals = data.get("signals")
    if not isinstance(signals, list):
        fail("missing or invalid 'signals'.")

    signal_ids = set()
    single_kinds = set()

    for index, signal in enumerate(signals):
        where = f"signals[{index}]"

        if not isinstance(signal, dict):
            fail(f"{where} is not an object.")

        signal_id = signal.get("id")
        if not isinstance(signal_id, str) or not SIGNAL_ID_PATTERN.match(signal_id):
            fail(f"{where}: invalid 'id' (expected 'S-' followed by uppercase letters, digits and '-').")
        if signal_id in signal_ids:
            fail(f"{where}: duplicate signal id '{signal_id}'.")
        signal_ids.add(signal_id)

        where = f"signal '{signal_id}'"

        kind = signal.get("kind")
        if kind not in KIND_PARAMS:
            fail(f"{where}: unknown kind '{kind}'.")

        if not isinstance(signal.get("enabled"), bool):
            fail(f"{where}: 'enabled' must be true or false.")

        if signal.get("level") not in LEVELS:
            fail(f"{where}: 'level' must be one of {', '.join(LEVELS)}.")

        if not is_text(signal.get("text")):
            fail(f"{where}: missing or invalid 'text'.")

        params = signal.get("params")
        if not isinstance(params, dict):
            fail(f"{where}: 'params' must be an object.")

        expected = KIND_PARAMS[kind]

        if expected is None:
            if params:
                fail(f"{where}: kind '{kind}' takes no parameters (params must be {{}}).")
            if kind in single_kinds:
                fail(f"{where}: kind '{kind}' may appear only once.")
            single_kinds.add(kind)
            continue

        if sorted(params) != sorted(expected):
            fail(f"{where}: params must contain exactly: {', '.join(expected)}.")

        if kind == "paired_files":
            first = params["first"]
            second = params["second"]
            if not is_text(first) or not is_text(second) or "/" in first or "/" in second:
                fail(f"{where}: 'first' and 'second' must be file names without '/'.")
            if first == second:
                fail(f"{where}: 'first' and 'second' must be different.")

        elif kind == "size_delta":
            if not is_int(params["min_bytes"]) or params["min_bytes"] < 1:
                fail(f"{where}: 'min_bytes' must be an integer >= 1.")
            if not is_number(params["min_ratio"]) or params["min_ratio"] <= 0:
                fail(f"{where}: 'min_ratio' must be a number > 0.")

        elif kind == "category_changed":
            chosen = params["categories"]
            classes = params["classes"]
            if not validate_string_list(chosen, False) or len(set(chosen)) != len(chosen) \
                    or any(c not in category_ids for c in chosen):
                fail(f"{where}: 'categories' must be a non-empty list of existing category ids.")
            if not validate_string_list(classes, False) or len(set(classes)) != len(classes) \
                    or any(c not in ENTRY_CLASSES for c in classes):
                fail(f"{where}: 'classes' must be a non-empty subset of {', '.join(ENTRY_CLASSES)}.")

    return data


# ---------------------------------------------------------------------------
# ARCHITECTURE MAP (section 10)
# ---------------------------------------------------------------------------

def is_valid_zone_path(path):
    if not is_text(path):
        return False
    if path.startswith("/"):
        return False
    for forbidden in ("\\", "./", "../", "//"):
        if forbidden in path:
            return False
    return True


def is_valid_date(value):
    if not isinstance(value, str) or not DATE_PATTERN.match(value):
        return False
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        return False
    return True


def validate_map(data, path):

    def fail(message):
        raise AnalysisError(f"{path}: {message}")

    if not isinstance(data, dict):
        fail("architecture map is not a JSON object.")

    if data.get("format") != MAP_FORMAT:
        fail(f"unknown format (expected '{MAP_FORMAT}').")

    if data.get("format_version") != VERSION:
        fail(f"unsupported format_version (expected '{VERSION}').")

    if not is_int(data.get("revision")) or data["revision"] < 1:
        fail("'revision' must be an integer >= 1.")

    status = data.get("status")
    if status not in MAP_STATUSES:
        fail("'status' must be DRAFT or APPROVED.")

    if "approved" not in data:
        fail("missing 'approved'.")

    if status == "DRAFT" and data["approved"] is not None:
        fail("'approved' must be null for a DRAFT map.")

    if status == "APPROVED" and not is_valid_date(data["approved"]):
        fail("'approved' must be a date YYYY-MM-DD for an APPROVED map.")

    project = data.get("project")
    if not isinstance(project, dict) or not is_text(project.get("name")) \
            or not is_text(project.get("target")):
        fail("missing or invalid 'project'.")

    zones = data.get("zones")
    if not isinstance(zones, list):
        fail("missing or invalid 'zones'.")

    zone_ids = set()
    zone_paths = set()

    for index, zone in enumerate(zones):
        where = f"zones[{index}]"

        if not isinstance(zone, dict):
            fail(f"{where} is not an object.")

        zone_id = zone.get("id")
        if not isinstance(zone_id, str) or not ZONE_ID_PATTERN.match(zone_id):
            fail(f"{where}: invalid 'id' (lowercase letters, digits and '-').")
        if zone_id == UNMAPPED:
            fail(f"{where}: '{UNMAPPED}' is a reserved zone id.")
        if zone_id in zone_ids:
            fail(f"{where}: duplicate zone id '{zone_id}'.")
        zone_ids.add(zone_id)

        where = f"zone '{zone_id}'"

        if not is_text(zone.get("name")) or not is_text(zone.get("description")):
            fail(f"{where}: 'name' and 'description' must be non-empty strings.")

        paths = zone.get("paths")
        if not isinstance(paths, list) or not paths:
            fail(f"{where}: 'paths' must be a non-empty list.")

        for zone_path in paths:
            if not is_valid_zone_path(zone_path):
                fail(f"{where}: invalid path {json.dumps(zone_path, ensure_ascii=False)}.")
            if zone_path in zone_paths:
                fail(f"{where}: path '{zone_path}' is listed more than once in the map.")
            zone_paths.add(zone_path)

        if not isinstance(zone.get("attention"), bool) or not isinstance(zone.get("generated"), bool):
            fail(f"{where}: 'attention' and 'generated' must be true or false.")

    return data


# ---------------------------------------------------------------------------
# CHANGE RECORD (read-only, section 6 checks 5-6)
# ---------------------------------------------------------------------------

def list_record_numbers(changes_directory):
    numbers = []

    if not os.path.isdir(changes_directory):
        return numbers

    for name in os.listdir(changes_directory):
        stem, extension = os.path.splitext(name)
        if extension == ".json" and RECORD_ID_PATTERN.match(stem):
            numbers.append(number(RECORD_ID_PATTERN, stem))

    return sorted(numbers)


def select_record(config, requested):
    changes_directory = config["input"]["changes_directory"]
    numbers = list_record_numbers(changes_directory)
    latest = "CHG-{:03d}".format(numbers[-1]) if numbers else None

    if requested is None:
        if latest is None:
            raise AnalysisError(f"No change record found in {changes_directory}.")
        record_id = latest
    else:
        record_id = requested

    path = os.path.join(changes_directory, f"{record_id}.json")

    if not os.path.isfile(path):
        raise AnalysisError(f"Change record {record_id} not found: {path}")

    return record_id, path, latest


def check_side(side, where, keys, allow_null_hash, fail):
    if not isinstance(side, dict):
        fail(f"{where}: invalid file metadata.")

    for key in keys:
        if key not in side:
            fail(f"{where}: missing '{key}'.")

    if not is_int(side["size"]) or side["size"] < 0:
        fail(f"{where}: invalid 'size'.")

    if not isinstance(side["modified"], str):
        fail(f"{where}: invalid 'modified'.")

    if "extension" in keys and not isinstance(side["extension"], str):
        fail(f"{where}: invalid 'extension'.")

    if side["hash"] is None:
        if not allow_null_hash:
            fail(f"{where}: null hash outside the unverified class.")
    elif not is_hash(side["hash"]):
        fail(f"{where}: invalid hash.")


def build_areas(entries):
    areas = {}

    for entry in entries:
        counts = areas.setdefault(entry["area"], {
            "area": entry["area"], "added": 0, "removed": 0, "modified": 0, "unverified": 0,
        })
        counts[entry["class"]] += 1

    return [areas[name] for name in sorted(areas)]


def validate_record(data, path, expected_id):

    def fail(message):
        raise AnalysisError(f"{path}: {message}")

    if not isinstance(data, dict):
        fail("change record is not a JSON object.")

    if data.get("format") != RECORD_FORMAT or data.get("format_version") != RECORD_FORMAT_VERSION:
        fail("unknown change record format or version.")

    if data.get("id") != expected_id:
        fail(f"contains id {data.get('id')}, expected {expected_id}.")

    status = data.get("status")
    if status not in RECORD_STATUSES:
        fail("missing or invalid 'status'.")

    review = data.get("review")
    if not isinstance(review, dict) or not all(k in review for k in ("decision", "reviewed", "note")):
        fail("missing or invalid 'review'.")

    if status == STATUS_PENDING:
        if review["decision"] is not None:
            fail("pending record contains a review decision.")
    elif review["decision"] != status:
        fail("review decision does not match status.")

    comparison = data.get("comparison")
    if not isinstance(comparison, dict) \
            or not isinstance(comparison.get("id"), str) \
            or not COMPARISON_ID_PATTERN.match(comparison["id"]) \
            or not is_hash(comparison.get("result_sha256")):
        fail("missing or invalid 'comparison'.")

    for side in ("from", "to"):
        value = data.get(side)
        if not isinstance(value, dict) or not isinstance(value.get("id"), str) \
                or not SNAPSHOT_ID_PATTERN.match(value["id"]) \
                or not is_hash(value.get("source_sha256")):
            fail(f"missing or invalid '{side}'.")

    if data["from"]["id"] == data["to"]["id"]:
        fail("'from' and 'to' are the same snapshot.")

    project = data.get("project")
    if not isinstance(project, dict) or not is_text(project.get("name")) \
            or not is_text(project.get("target")):
        fail("missing or invalid 'project'.")

    summary = data.get("summary")
    if not isinstance(summary, dict) \
            or not all(is_int(summary.get(k)) and summary[k] >= 0 for k in SUMMARY_KEYS):
        fail("missing or invalid 'summary'.")

    changed = summary["added"] + summary["removed"] + summary["modified"] + summary["unverified"]
    if not isinstance(data.get("no_changes"), bool) or data["no_changes"] != (changed == 0):
        fail("'no_changes' does not match the summary.")

    entries = data.get("entries")
    if not isinstance(entries, list):
        fail("missing or invalid 'entries'.")

    seen = set()
    counts = {name: 0 for name in ENTRY_CLASSES}
    previous_key = None
    full = ("size", "extension", "modified", "hash")
    short = ("size", "modified", "hash")

    for index, entry in enumerate(entries, start=1):
        expected_entry = f"{expected_id}/{index}"

        if not isinstance(entry, dict) or entry.get("entry") != expected_entry:
            fail(f"entry {index}: expected id {expected_entry}.")

        where = f"entry {expected_entry}"

        name = entry.get("class")
        if name not in ENTRY_CLASSES:
            fail(f"{where}: invalid 'class'.")

        entry_path = entry.get("path")
        if not is_text(entry_path):
            fail(f"{where}: missing or invalid 'path'.")

        if entry_path in seen:
            fail(f"'{entry_path}' appears in more than one entry.")
        seen.add(entry_path)

        key = (ENTRY_CLASSES.index(name), entry_path)
        if previous_key is not None and key <= previous_key:
            fail(f"{where}: entries are not ordered by class, then by path.")
        previous_key = key

        if entry.get("area") != area_of(entry_path):
            fail(f"{where}: 'area' does not match the path.")

        if "from" not in entry or "to" not in entry:
            fail(f"{where}: missing 'from' or 'to'.")

        if name == "added":
            if entry["from"] is not None:
                fail(f"{where}: added entry must have from = null.")
            check_side(entry["to"], f"{where} (to)", full, False, fail)

        elif name == "removed":
            if entry["to"] is not None:
                fail(f"{where}: removed entry must have to = null.")
            check_side(entry["from"], f"{where} (from)", full, False, fail)

        elif name == "modified":
            fields = entry.get("changed_fields")
            if not isinstance(fields, list) or not all(isinstance(f, str) for f in fields):
                fail(f"{where}: invalid 'changed_fields'.")
            check_side(entry["from"], f"{where} (from)", short, False, fail)
            check_side(entry["to"], f"{where} (to)", short, False, fail)
            if entry["from"]["hash"] == entry["to"]["hash"]:
                fail(f"{where}: modified entry with equal hashes.")

        else:
            presence = entry.get("presence")
            reason = entry.get("reason")
            if presence not in PRESENCE_VALUES or reason not in REASON_VALUES:
                fail(f"{where}: invalid 'presence' or 'reason'.")

            has_from = entry["from"] is not None
            has_to = entry["to"] is not None
            expected_sides = {
                "both": (True, True), "from_only": (True, False), "to_only": (False, True),
            }[presence]
            if (has_from, has_to) != expected_sides:
                fail(f"{where}: 'presence' does not match 'from' / 'to'.")

            if has_from:
                check_side(entry["from"], f"{where} (from)", full, True, fail)
            if has_to:
                check_side(entry["to"], f"{where} (to)", full, True, fail)

            null_from = has_from and entry["from"]["hash"] is None
            null_to = has_to and entry["to"]["hash"] is None
            expected_reason = (
                "hash_null_both" if null_from and null_to
                else "hash_null_from" if null_from
                else "hash_null_to" if null_to
                else None
            )
            if reason != expected_reason:
                fail(f"{where}: 'reason' does not match the hashes.")

        counts[name] += 1

    for name in ENTRY_CLASSES:
        if counts[name] != summary[name]:
            fail(f"summary.{name} is {summary[name]}, but {counts[name]} entries are listed.")

    if data.get("areas") != build_areas(entries):
        fail("'areas' do not match the entries.")

    warnings = data.get("warnings")
    if not isinstance(warnings, list) or not all(isinstance(w, str) for w in warnings):
        fail("missing or invalid 'warnings'.")


def load_record(record_id, path):
    raw = read_bytes(path, "Change record")
    data = parse_json(raw, path, "Change record")
    validate_record(data, path, record_id)
    return data, sha256_bytes(raw)


def facts_sha256(record):
    facts = {key: record[key] for key in FACT_KEYS}
    text = json.dumps(facts, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return sha256_bytes(text.encode("utf-8"))


# ---------------------------------------------------------------------------
# SNAPSHOTS (read-only, section 6 checks 8-9)
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


def load_snapshot(record, side, config):
    snapshot_id = record[side]["id"]
    path = find_snapshot_file(snapshot_id, config)

    if path is None:
        raise AnalysisError(
            f"Snapshot {snapshot_id} used by {record['id']} is not found "
            "(neither current snapshot nor history)."
        )

    raw = read_bytes(path, "Snapshot")

    if sha256_bytes(raw) != record[side]["source_sha256"]:
        raise AnalysisError(
            f"Snapshot {snapshot_id} ({path}) does not match {record['id']} "
            "(different SHA-256). The snapshot was changed after the change record was created."
        )

    data = parse_json(raw, path, "Snapshot")

    def fail(message):
        raise AnalysisError(f"{path}: {message}")

    if not isinstance(data, dict):
        fail("snapshot is not a JSON object.")

    if data.get("id") != snapshot_id:
        fail(f"contains id {data.get('id')}, expected {snapshot_id}.")

    project = data.get("project")
    if not isinstance(project, dict) \
            or project.get("name") != record["project"]["name"] \
            or project.get("target") != record["project"]["target"]:
        fail(f"belongs to another project than {record['id']}.")

    statistics = data.get("statistics")
    if not isinstance(statistics, dict) or not is_int(statistics.get("total_directories")):
        fail("missing or invalid 'statistics'.")

    files = data.get("files")
    if not isinstance(files, list):
        fail("missing or invalid 'files'.")

    by_path = {}

    for index, item in enumerate(files):
        if not isinstance(item, dict) or not is_text(item.get("path")):
            fail(f"files[{index}]: missing or invalid 'path'.")
        if item["path"] in by_path:
            fail(f"file '{item['path']}' is listed more than once.")
        by_path[item["path"]] = item

    return {
        "id": snapshot_id,
        "source_sha256": record[side]["source_sha256"],
        "total_directories": statistics["total_directories"],
        "files": by_path,
    }


def check_entries_against_snapshots(record, snap_from, snap_to):

    def fail(message):
        raise AnalysisError(f"Entries do not agree with the snapshots: {message}")

    summary = record["summary"]

    if summary["files_from"] != len(snap_from["files"]):
        fail(f"summary.files_from is {summary['files_from']}, {snap_from['id']} lists {len(snap_from['files'])} files.")
    if summary["files_to"] != len(snap_to["files"]):
        fail(f"summary.files_to is {summary['files_to']}, {snap_to['id']} lists {len(snap_to['files'])} files.")
    if summary["directories_from"] != snap_from["total_directories"]:
        fail(f"summary.directories_from differs from {snap_from['id']}.")
    if summary["directories_to"] != snap_to["total_directories"]:
        fail(f"summary.directories_to differs from {snap_to['id']}.")

    full = ("size", "extension", "modified", "hash")
    short = ("size", "modified", "hash")

    def same(side, snapshot_record, keys):
        return all(side.get(key) == snapshot_record.get(key) for key in keys)

    for entry in record["entries"]:
        path = entry["path"]
        in_from = path in snap_from["files"]
        in_to = path in snap_to["files"]
        where = f"{entry['entry']} '{path}'"
        name = entry["class"]

        if name == "added":
            if in_from or not in_to:
                fail(f"{where}: added file must exist only in {snap_to['id']}.")
            if not same(entry["to"], snap_to["files"][path], full):
                fail(f"{where}: metadata differs from {snap_to['id']}.")

        elif name == "removed":
            if not in_from or in_to:
                fail(f"{where}: removed file must exist only in {snap_from['id']}.")
            if not same(entry["from"], snap_from["files"][path], full):
                fail(f"{where}: metadata differs from {snap_from['id']}.")

        elif name == "modified":
            if not in_from or not in_to:
                fail(f"{where}: modified file must exist in both snapshots.")
            if not same(entry["from"], snap_from["files"][path], short):
                fail(f"{where}: 'from' metadata differs from {snap_from['id']}.")
            if not same(entry["to"], snap_to["files"][path], short):
                fail(f"{where}: 'to' metadata differs from {snap_to['id']}.")

        else:
            expected = {
                "both": (True, True), "from_only": (True, False), "to_only": (False, True),
            }[entry["presence"]]
            if (in_from, in_to) != expected:
                fail(f"{where}: presence '{entry['presence']}' differs from the snapshots.")
            if entry["from"] is not None and not same(entry["from"], snap_from["files"][path], full):
                fail(f"{where}: 'from' metadata differs from {snap_from['id']}.")
            if entry["to"] is not None and not same(entry["to"], snap_to["files"][path], full):
                fail(f"{where}: 'to' metadata differs from {snap_to['id']}.")


# ---------------------------------------------------------------------------
# CLASSIFICATION (section 7)
# Path only. Exact, case-sensitive. No wildcards.
# ---------------------------------------------------------------------------

class Classifier:

    def __init__(self, rules, architecture_map):
        self.categories = rules["categories"]
        self.zones = architecture_map["zones"]
        self.zone_by_id = {zone["id"]: zone for zone in self.zones}
        self.exact = {}
        self.prefixes = []

        for zone in self.zones:
            for zone_path in zone["paths"]:
                if zone_path.endswith("/"):
                    self.prefixes.append((zone_path, zone["id"]))
                else:
                    self.exact[zone_path] = zone["id"]

        # Longest prefix first. Prefix strings are unique in the map.
        self.prefixes.sort(key=lambda item: (-len(item[0]), item[0]))

    def category(self, path):
        name = path.rsplit("/", 1)[-1]

        for category in self.categories:
            if name in category["names"]:
                return category["id"]
            if any(path.endswith(suffix) for suffix in category["suffixes"]):
                return category["id"]

        return UNCATEGORIZED

    def zone(self, path):
        if path in self.exact:
            return self.exact[path]

        for prefix, zone_id in self.prefixes:
            if path.startswith(prefix):
                return zone_id

        return UNMAPPED


# ---------------------------------------------------------------------------
# SIGNALS (section 8)
# Each evaluator returns a list of (entry ids, evidence).
# ---------------------------------------------------------------------------

def join_path(directory, name):
    return f"{directory}/{name}" if directory else name


def sorted_ids(entries):
    return sorted((e["entry"] for e in entries), key=entry_number)


def evaluate_unverified(context, signal):
    items = [e for e in context["entries"] if e["class"] == "unverified"]
    if not items:
        return []
    return [(sorted_ids(items), {"paths": sorted(e["path"] for e in items)})]


def evaluate_zone_flag(context, flag):
    results = []

    for zone in context["classifier"].zones:
        if not zone[flag]:
            continue
        items = [e for e in context["entries"] if context["zone"][e["entry"]] == zone["id"]]
        if items:
            results.append((sorted_ids(items), {"zone": zone["id"]}))

    return results


def evaluate_attention_zone(context, signal):
    return evaluate_zone_flag(context, "attention")


def evaluate_generated_zone(context, signal):
    return evaluate_zone_flag(context, "generated")


def evaluate_paired_files(context, signal):
    first = signal["params"]["first"]
    second = signal["params"]["second"]

    changed = {
        e["path"]: e for e in context["entries"]
        if e["class"] in ("added", "removed", "modified")
    }
    unverified = {e["path"] for e in context["entries"] if e["class"] == "unverified"}

    directories = set()
    for path in list(changed) + sorted(unverified):
        directory, _, name = path.rpartition("/")
        if name in (first, second):
            directories.add(directory)

    results = []

    for directory in sorted(directories):
        path_first = join_path(directory, first)
        path_second = join_path(directory, second)
        changed_first = path_first in changed
        changed_second = path_second in changed

        if changed_first == changed_second:
            continue

        changed_path, changed_name, other_path, other_name = (
            (path_first, first, path_second, second) if changed_first
            else (path_second, second, path_first, first)
        )

        if other_path in unverified:
            context["warnings"].append(
                f"{signal['id']} not evaluated for directory '{directory}': {other_path} is unverified."
            )
            continue

        results.append(([changed[changed_path]["entry"]], {
            "directory": directory,
            "changed": changed_name,
            "other": other_name,
            "other_exists_in_to": other_path in context["to_files"],
        }))

    return results


def evaluate_grouped_candidates(context, key_function, key_name):
    groups = {}

    for entry in context["entries"]:
        if entry["class"] in ("added", "removed"):
            groups.setdefault(key_function(entry), []).append(entry)

    results = []

    for key in sorted(groups):
        items = groups[key]
        removed = sorted(e["path"] for e in items if e["class"] == "removed")
        added = sorted(e["path"] for e in items if e["class"] == "added")
        if removed and added:
            results.append((sorted_ids(items), {key_name: key, "removed": removed, "added": added}))

    return results


def evaluate_rename_candidate(context, signal):
    def key(entry):
        side = entry["to"] if entry["class"] == "added" else entry["from"]
        return side["hash"]
    return evaluate_grouped_candidates(context, key, "hash")


def evaluate_case_candidate(context, signal):
    return evaluate_grouped_candidates(context, lambda e: e["path"].casefold(), "folded_path")


def evaluate_new_top_level(context, signal):
    existing = {path.split("/", 1)[0] for path in context["from_files"] if "/" in path}
    groups = {}

    for entry in context["entries"]:
        if entry["class"] == "added" and "/" in entry["path"]:
            folder = entry["path"].split("/", 1)[0]
            if folder not in existing:
                groups.setdefault(folder, []).append(entry)

    return [(sorted_ids(items), {"folder": folder}) for folder, items in sorted(groups.items())]


def evaluate_empty_file(context, signal):
    return [
        ([e["entry"]], {"path": e["path"]})
        for e in context["entries"]
        if e["class"] in ("added", "modified") and e["to"]["size"] == 0
    ]


def evaluate_size_delta(context, signal):
    min_bytes = signal["params"]["min_bytes"]
    min_ratio = signal["params"]["min_ratio"]
    results = []

    for entry in context["entries"]:
        if entry["class"] != "modified":
            continue

        from_size = entry["from"]["size"]
        to_size = entry["to"]["size"]
        delta = to_size - from_size

        if abs(delta) < min_bytes:
            continue
        if from_size != 0 and abs(delta) / from_size < min_ratio:
            continue

        results.append(([entry["entry"]], {
            "path": entry["path"], "from_size": from_size, "to_size": to_size, "delta": delta,
        }))

    return results


def evaluate_category_changed(context, signal):
    categories = signal["params"]["categories"]
    classes = signal["params"]["classes"]
    groups = {}

    for entry in context["entries"]:
        category = context["category"][entry["entry"]]
        if entry["class"] in classes and category in categories:
            groups.setdefault(category, []).append(entry)

    return [(sorted_ids(items), {"category": category}) for category, items in groups.items()]


def evaluate_unmapped(context, signal):
    items = [e for e in context["entries"] if context["zone"][e["entry"]] == UNMAPPED]
    if not items:
        return []
    return [(sorted_ids(items), {"paths": sorted(e["path"] for e in items)})]


def evaluate_uncategorized(context, signal):
    items = [e for e in context["entries"] if context["category"][e["entry"]] == UNCATEGORIZED]
    if not items:
        return []
    return [(sorted_ids(items), {"paths": sorted(e["path"] for e in items)})]


EVALUATORS = {
    "unverified": evaluate_unverified,
    "attention_zone": evaluate_attention_zone,
    "generated_zone": evaluate_generated_zone,
    "paired_files": evaluate_paired_files,
    "rename_candidate": evaluate_rename_candidate,
    "case_candidate": evaluate_case_candidate,
    "new_top_level": evaluate_new_top_level,
    "empty_file": evaluate_empty_file,
    "size_delta": evaluate_size_delta,
    "category_changed": evaluate_category_changed,
    "unmapped": evaluate_unmapped,
    "uncategorized": evaluate_uncategorized,
}


def evaluate_signals(context, rules, analysis_id):
    findings = []

    for signal in rules["signals"]:
        if not signal["enabled"]:
            continue

        results = EVALUATORS[signal["kind"]](context, signal)
        results.sort(key=lambda item: (
            entry_number(item[0][0]),
            json.dumps(item[1], sort_keys=True, ensure_ascii=False),
        ))

        for entry_ids, evidence in results:
            findings.append({
                "finding": None,
                "rule": signal["id"],
                "kind": signal["kind"],
                "level": signal["level"],
                "text": signal["text"],
                "entries": entry_ids,
                "evidence": evidence,
            })

    for index, finding in enumerate(findings, start=1):
        finding["finding"] = f"{analysis_id}/F-{index}"

    return findings


# ---------------------------------------------------------------------------
# SUMMARY AND COVERAGE (section 11)
# ---------------------------------------------------------------------------

def class_counts(entries, key_of, order):
    groups = {}

    for entry in entries:
        key = key_of(entry)
        counts = groups.setdefault(key, {"added": 0, "removed": 0, "modified": 0, "unverified": 0})
        counts[entry["class"]] += 1

    return [
        dict({"key": key}, **groups[key]) for key in order if key in groups
    ]


def build_summary(record, entries, zone_of, category_of, classifier, findings):
    zone_order = [zone["id"] for zone in classifier.zones] + [UNMAPPED]
    category_order = [category["id"] for category in classifier.categories] + [UNCATEGORIZED]

    zones = [
        {"zone": item.pop("key"), **item}
        for item in class_counts(entries, lambda e: zone_of[e["entry"]], zone_order)
    ]
    categories = [
        {"category": item.pop("key"), **item}
        for item in class_counts(entries, lambda e: category_of[e["entry"]], category_order)
    ]

    added = sum(e["to"]["size"] for e in entries if e["class"] == "added")
    removed = -sum(e["from"]["size"] for e in entries if e["class"] == "removed")
    modified = sum(e["to"]["size"] - e["from"]["size"] for e in entries if e["class"] == "modified")

    summary = record["summary"]

    return {
        "classes": {
            "added": summary["added"],
            "removed": summary["removed"],
            "modified": summary["modified"],
            "unverified": summary["unverified"],
            "unchanged": summary["unchanged"],
        },
        "zones": zones,
        "categories": categories,
        "size_delta": {
            "added": added,
            "removed": removed,
            "modified": modified,
            "total": added + removed + modified,
            "unverified_excluded": sum(1 for e in entries if e["class"] == "unverified"),
        },
        "findings": {level: sum(1 for f in findings if f["level"] == level) for level in LEVELS},
    }


def build_coverage(to_files, classifier):
    zone_files = {}
    category_files = {}
    unmapped = []
    uncategorized = []

    for path in to_files:
        zone = classifier.zone(path)
        category = classifier.category(path)

        if zone == UNMAPPED:
            unmapped.append(path)
        else:
            zone_files[zone] = zone_files.get(zone, 0) + 1

        if category == UNCATEGORIZED:
            uncategorized.append(path)
        else:
            category_files[category] = category_files.get(category, 0) + 1

    return {
        "files": len(to_files),
        "zones": [
            {"zone": zone["id"], "files": zone_files[zone["id"]]}
            for zone in classifier.zones if zone["id"] in zone_files
        ],
        "unmapped": len(unmapped),
        "unmapped_paths": sorted(unmapped),
        "categories": [
            {"category": category["id"], "files": category_files[category["id"]]}
            for category in classifier.categories if category["id"] in category_files
        ],
        "uncategorized": len(uncategorized),
        "uncategorized_paths": sorted(uncategorized),
    }


# ---------------------------------------------------------------------------
# SELF-CHECK (section 11.2)
# ---------------------------------------------------------------------------

def self_check(result, record):

    def fail(message):
        raise AnalysisError(f"Self-check failed: {message}")

    record_entries = record["entries"]
    entries = result["entries"]

    if len(entries) != len(record_entries):
        fail("the number of entries differs from the change record.")

    for ours, theirs in zip(entries, record_entries):
        if (ours["entry"], ours["class"], ours["path"]) != \
                (theirs["entry"], theirs["class"], theirs["path"]):
            fail(f"entry {theirs['entry']} differs from the change record.")

    summary = result["summary"]

    for name in ENTRY_CLASSES:
        expected = record["summary"][name]
        if sum(z[name] for z in summary["zones"]) != expected:
            fail(f"zones do not add up to the '{name}' count.")
        if sum(c[name] for c in summary["categories"]) != expected:
            fail(f"categories do not add up to the '{name}' count.")

    known = {e["entry"] for e in entries}

    for finding in result["findings"]:
        if not finding["entries"] or any(entry_id not in known for entry_id in finding["entries"]):
            fail(f"{finding['finding']} refers to an unknown entry.")

    for level in LEVELS:
        if summary["findings"][level] != sum(1 for f in result["findings"] if f["level"] == level):
            fail(f"summary.findings.{level} does not match the findings.")

    coverage = result["coverage"]

    if sum(z["files"] for z in coverage["zones"]) + coverage["unmapped"] != coverage["files"]:
        fail("zone coverage does not add up to the number of files.")

    if sum(c["files"] for c in coverage["categories"]) + coverage["uncategorized"] != coverage["files"]:
        fail("category coverage does not add up to the number of files.")


# ---------------------------------------------------------------------------
# ANALYSIS
# ---------------------------------------------------------------------------

def analyze(record, record_sha256, snap_from, snap_to, rules, rules_sha256,
            architecture_map, map_sha256, latest_id):

    analysis_id = "ANL-{:03d}".format(number(RECORD_ID_PATTERN, record["id"]))
    classifier = Classifier(rules, architecture_map)

    zone_of = {}
    category_of = {}
    entries = []

    for entry in record["entries"]:
        zone_of[entry["entry"]] = classifier.zone(entry["path"])
        category_of[entry["entry"]] = classifier.category(entry["path"])
        entries.append({
            "entry": entry["entry"],
            "class": entry["class"],
            "path": entry["path"],
            "category": category_of[entry["entry"]],
            "zone": zone_of[entry["entry"]],
        })

    # Warnings, in the order of section 13.
    warnings = []

    if architecture_map["status"] == "DRAFT":
        warnings.append("Architecture map is DRAFT (not approved).")

    if not architecture_map["zones"]:
        warnings.append("Architecture map has no zones.")

    if record["id"] != latest_id:
        warnings.append(f"{record['id']} is not the latest change record (latest: {latest_id}).")

    if record["status"] == STATUS_REJECTED:
        warnings.append("Change record is REJECTED.")

    context = {
        "entries": record["entries"],
        "zone": zone_of,
        "category": category_of,
        "classifier": classifier,
        "from_files": snap_from["files"],
        "to_files": snap_to["files"],
        "warnings": warnings,
    }

    findings = evaluate_signals(context, rules, analysis_id)

    for warning in record["warnings"]:
        warnings.append(f"Change record: {warning}")

    result = {
        "format": RESULT_FORMAT,
        "format_version": VERSION,
        "id": analysis_id,
        "generated": now(),
        "status": STATUS_COMPLETED_WITH_WARNINGS if warnings else STATUS_COMPLETED,

        "change_record": {
            "id": record["id"],
            "status": record["status"],
            "record_sha256": record_sha256,
            "facts_sha256": facts_sha256(record),
            "comparison_id": record["comparison"]["id"],
        },
        "from": {"id": snap_from["id"], "source_sha256": snap_from["source_sha256"]},
        "to": {"id": snap_to["id"], "source_sha256": snap_to["source_sha256"]},
        "project": {
            "name": record["project"]["name"],
            "target": record["project"]["target"],
        },

        "rules": {"revision": rules["revision"], "sha256": rules_sha256},
        "architecture_map": {
            "revision": architecture_map["revision"],
            "status": architecture_map["status"],
            "sha256": map_sha256,
        },

        "entries": entries,
        "findings": findings,
        "summary": build_summary(record, record["entries"], zone_of, category_of, classifier, findings),
        "coverage": build_coverage(sorted(snap_to["files"]), classifier),
        "warnings": warnings,
    }

    self_check(result, record)

    return result


# ---------------------------------------------------------------------------
# REPORT (.md, section 12)
# ---------------------------------------------------------------------------

def describe_evidence(evidence):
    parts = []

    for key, value in evidence.items():
        if isinstance(value, list):
            text = ", ".join(f"`{item}`" for item in value) if value else "-"
        elif isinstance(value, bool):
            text = "yes" if value else "no"
        elif key == "directory" and value == "":
            text = "(root)"
        elif isinstance(value, str):
            text = f"`{value}`"
        else:
            text = str(value)
        parts.append(f"{key}: {text}")

    return "; ".join(parts)


def create_report(result):
    lines = []
    record = result["change_record"]
    summary = result["summary"]
    coverage = result["coverage"]
    paths = {e["entry"]: e["path"] for e in result["entries"]}

    lines.append("# REQUIEM MEMORY CORE ANALYSIS REPORT")
    lines.append("")
    lines.append(f"Analysis: {result['id']}")
    lines.append(f"Generated: {result['generated']}")
    lines.append(f"Status: {result['status']}")
    lines.append(f"Project: {result['project']['name']} ({result['project']['target']})")
    lines.append("")
    lines.append("> Findings are rule matches, not evaluations. Analysis does not approve or reject changes.")
    lines.append("")

    lines.append("## Source")
    lines.append("")
    lines.append(f"Change record: {record['id']} (status at analysis: {record['status']})")
    lines.append("")
    lines.append(f"record_sha256: {record['record_sha256']}")
    lines.append("")
    lines.append(f"facts_sha256: {record['facts_sha256']}")
    lines.append("")
    lines.append(f"Comparison: {record['comparison_id']}")
    lines.append("")
    lines.append("| | Snapshot | source_sha256 |")
    lines.append("|---|---|---|")
    lines.append(f"| From | {result['from']['id']} | {result['from']['source_sha256']} |")
    lines.append(f"| To | {result['to']['id']} | {result['to']['source_sha256']} |")
    lines.append("")

    lines.append("## Rules and map")
    lines.append("")
    lines.append(f"Rules: revision {result['rules']['revision']}, sha256 {result['rules']['sha256']}")
    lines.append("")
    lines.append(
        f"Architecture map: revision {result['architecture_map']['revision']}, "
        f"status {result['architecture_map']['status']}, "
        f"sha256 {result['architecture_map']['sha256']}"
    )
    lines.append("")

    lines.append("## Summary")
    lines.append("")
    lines.append("| Class | Files |")
    lines.append("|---|---|")
    for name in ("added", "removed", "modified", "unverified", "unchanged"):
        lines.append(f"| {name.capitalize()} | {summary['classes'][name]} |")
    lines.append("")
    lines.append(
        "Findings: "
        + " | ".join(f"{level} {summary['findings'][level]}" for level in LEVELS)
    )
    lines.append("")
    delta = summary["size_delta"]
    lines.append(
        f"Size delta (bytes): added {delta['added']}, removed {delta['removed']}, "
        f"modified {delta['modified']}, total {delta['total']}; "
        f"unverified excluded: {delta['unverified_excluded']}"
    )
    lines.append("")

    lines.append("## Findings")
    lines.append("")
    if not result["findings"]:
        lines.append("- none")
        lines.append("")
    for level in LEVELS:
        items = [f for f in result["findings"] if f["level"] == level]
        if not items:
            continue
        lines.append(f"### {level.capitalize()}")
        lines.append("")
        for finding in items:
            lines.append(f"- {finding['finding']} [{finding['rule']}] {finding['text']}")
            for entry_id in finding["entries"]:
                lines.append(f"  - {entry_id} `{paths[entry_id]}`")
            lines.append(f"  - evidence: {describe_evidence(finding['evidence'])}")
        lines.append("")

    lines.append("## Entries")
    lines.append("")
    if result["entries"]:
        lines.append("| Entry | Class | Path | Category | Zone |")
        lines.append("|---|---|---|---|---|")
        for entry in result["entries"]:
            lines.append(
                f"| {entry['entry']} | {entry['class']} | `{entry['path']}` | "
                f"{entry['category']} | {entry['zone']} |"
            )
    else:
        lines.append("- none (no changes)")
    lines.append("")

    for title, key, items in (
        ("Zones", "zone", summary["zones"]),
        ("Categories", "category", summary["categories"]),
    ):
        lines.append(f"## {title}")
        lines.append("")
        if items:
            lines.append(f"| {key.capitalize()} | Added | Removed | Modified | Unverified |")
            lines.append("|---|---|---|---|---|")
            for item in items:
                lines.append(
                    f"| {item[key]} | {item['added']} | {item['removed']} | "
                    f"{item['modified']} | {item['unverified']} |"
                )
        else:
            lines.append("- none")
        lines.append("")

    lines.append("## Coverage")
    lines.append("")
    lines.append(f"Files in {result['to']['id']}: {coverage['files']}")
    lines.append("")
    lines.append("| Zone | Files |")
    lines.append("|---|---|")
    for item in coverage["zones"]:
        lines.append(f"| {item['zone']} | {item['files']} |")
    lines.append(f"| {UNMAPPED} | {coverage['unmapped']} |")
    lines.append("")
    lines.append("| Category | Files |")
    lines.append("|---|---|")
    for item in coverage["categories"]:
        lines.append(f"| {item['category']} | {item['files']} |")
    lines.append(f"| {UNCATEGORIZED} | {coverage['uncategorized']} |")
    lines.append("")
    for title, key in (("Unmapped", "unmapped"), ("Uncategorized", "uncategorized")):
        lines.append(f"### {title} paths ({coverage[key]})")
        lines.append("")
        if coverage[key + "_paths"]:
            for path in coverage[key + "_paths"]:
                lines.append(f"- `{path}`")
        else:
            lines.append("- none")
        lines.append("")

    lines.append("## Warnings")
    lines.append("")
    if result["warnings"]:
        for warning in result["warnings"]:
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
        lines.append(f"python change_reporter.py --approve {record['id']} --note \"text\"")
        lines.append(f"python change_reporter.py --reject {record['id']} --note \"text\"")
        lines.append("```")
        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# WRITE (section 15)
# Both files are fully written to .tmp first, then replaced.
# ---------------------------------------------------------------------------

def write_outputs_atomic(outputs):
    temporaries = []

    try:
        os.makedirs(REPORT_DIRECTORY, exist_ok=True)

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

        raise AnalysisError(
            f"Could not write output ({error}). Existing reports were left untouched."
        )

    for temporary, path in temporaries:
        try:
            os.replace(temporary, path)
        except OSError as error:
            raise AnalysisError(
                f"Could not replace {path} ({error}). "
                f"The complete new version is kept in {temporary}."
            )


# ---------------------------------------------------------------------------

def main():

    # 1-2. Configuration and arguments.
    config = load_config()
    arguments = parse_arguments()

    # 3. Rules.
    rules_path = config["input"]["rules"]
    rules_raw = read_bytes(rules_path, "Rules file")
    rules = validate_rules(parse_json(rules_raw, rules_path, "Rules file"), rules_path)

    # 4. Architecture map.
    map_path = config["input"]["architecture_map"]
    map_raw = read_bytes(map_path, "Architecture map")
    architecture_map = validate_map(parse_json(map_raw, map_path, "Architecture map"), map_path)

    # 5-6. Change record (read-only).
    record_id, record_path, latest_id = select_record(config, arguments.record)
    record, record_sha256 = load_record(record_id, record_path)

    # 7. Project.
    if architecture_map["project"]["name"] != record["project"]["name"] \
            or architecture_map["project"]["target"] != record["project"]["target"]:
        raise AnalysisError(
            f"{map_path} belongs to another project than {record_id} "
            f"({architecture_map['project']['name']} / {architecture_map['project']['target']})."
        )

    # 8. Snapshots (read-only).
    snap_from = load_snapshot(record, "from", config)
    snap_to = load_snapshot(record, "to", config)

    # 9. Entries agree with snapshots.
    check_entries_against_snapshots(record, snap_from, snap_to)

    # Analysis and self-check.
    result = analyze(
        record, record_sha256, snap_from, snap_to,
        rules, sha256_bytes(rules_raw),
        architecture_map, sha256_bytes(map_raw),
        latest_id,
    )

    # Write (only reports/latest_analysis.json and .md).
    write_outputs_atomic([
        (RESULT_FILE, json.dumps(result, indent=2, ensure_ascii=False) + "\n"),
        (REPORT_FILE, create_report(result)),
    ])

    findings = result["summary"]["findings"]

    safe_print("Memory Core analysis completed.")
    safe_print(
        f"Analysis {result['id']}: {record_id} ({record['status']}), "
        f"{result['from']['id']} -> {result['to']['id']}"
    )
    safe_print(f"Status: {result['status']}")
    safe_print(
        f"Findings: attention {findings['attention']} | "
        f"notice {findings['notice']} | info {findings['info']}"
    )
    for warning in result["warnings"]:
        safe_print(f"Warning: {warning}")
    safe_print("Report: reports/latest_analysis.md")


if __name__ == "__main__":
    try:
        main()
    except AnalysisError as error:
        safe_print(f"Memory Core analysis aborted: {error}")
        sys.exit(1)
