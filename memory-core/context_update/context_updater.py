"""
REQUIEM Memory Core — Context Update Layer v0.1

Prepares controlled updates of project context from APPROVED change
records (CHG-NNN) and applies them only after human approval.

Boundaries:
- reads APPROVED change records from review/changes/ (never modifies them);
- writes proposals to review/context_updates/ and backups to review/backups/;
- only two operations exist: snapshot_state and event;
- only three target files can ever be changed (hard-coded, not configurable):
    README.md, context/REQUIEM_CONTEXT.md  (snapshot_state, inside markers)
    database/events.json                   (event, append only)
- project memory is written only by --apply of an APPROVED proposal,
  after hash verification and backup.

Run from inside context_update/:

    python context_updater.py
    python context_updater.py --approve CU-001 [--exclude OP-2 ...] [--note "text"]
    python context_updater.py --reject CU-001 [--note "text"]
    python context_updater.py --apply CU-001
"""

import os
import re
import sys
import json
import hashlib
import argparse
from datetime import datetime


VERSION = "0.1"

CONFIG_FILE = "context_update_config.json"

PROPOSAL_FORMAT = "requiem-context-update"
RECORD_FORMAT = "requiem-change-record"
RECORD_FORMAT_VERSION = "0.1"

SNAPSHOT_ID_PATTERN = re.compile(r"^SNAP-(\d+)$")
RECORD_ID_PATTERN = re.compile(r"^CHG-(\d+)$")
PROPOSAL_ID_PATTERN = re.compile(r"^CU-(\d+)$")
EVENT_ID_PATTERN = re.compile(r"^EVENT-(\d+)$")
OP_ID_PATTERN = re.compile(r"^OP-(\d+)$")
HASH_PATTERN = re.compile(r"^[0-9a-f]{64}$")

# Change record statuses (owned by the Change Report Layer).
RECORD_APPROVED = "APPROVED"
RECORD_STATUSES = ("PENDING_REVIEW", "APPROVED", "REJECTED")

# Proposal statuses.
STATUS_PROPOSED = "PROPOSED"
STATUS_APPROVED = "APPROVED"
STATUS_REJECTED = "REJECTED"
STATUS_APPLIED = "APPLIED"
STATUS_STALE = "STALE"
PROPOSAL_STATUSES = (
    STATUS_PROPOSED, STATUS_APPROVED, STATUS_REJECTED, STATUS_APPLIED, STATUS_STALE
)
OPEN_STATUSES = (STATUS_PROPOSED, STATUS_APPROVED)

DECISION_INCLUDE = "include"
DECISION_EXCLUDE = "exclude"

# ---------------------------------------------------------------------------
# Hard-coded whitelist. Paths are relative to the Memory Core root.
# identity.json, decisions.json, checkpoints.json and state.json are never targets.
# ---------------------------------------------------------------------------

KIND_SNAPSHOT_STATE = "snapshot_state"
KIND_EVENT = "event"

TYPE_REPLACE_MARKED_BLOCK = "replace_marked_block"
TYPE_APPEND_RECORD = "append_record"

README_TARGET = "README.md"
CONTEXT_TARGET = "context/REQUIEM_CONTEXT.md"
EVENTS_TARGET = "database/events.json"

SNAPSHOT_STATE_TARGETS = (README_TARGET, CONTEXT_TARGET)

ALLOWED = {
    KIND_SNAPSHOT_STATE: (TYPE_REPLACE_MARKED_BLOCK, SNAPSHOT_STATE_TARGETS),
    KIND_EVENT: (TYPE_APPEND_RECORD, (EVENTS_TARGET,)),
}

MARKER = "SNAPSHOT_STATE"
MARKER_BEGIN = "<!-- MEMORY:SNAPSHOT_STATE:BEGIN -->"
MARKER_END = "<!-- MEMORY:SNAPSHOT_STATE:END -->"

UTF8_BOM = b"\xef\xbb\xbf"


class ContextUpdateError(Exception):
    """The action cannot be completed safely."""


# ---------------------------------------------------------------------------
# CONFIG AND ARGUMENTS
# ---------------------------------------------------------------------------

def load_config():
    if not os.path.isfile(CONFIG_FILE):
        raise ContextUpdateError(
            f"{CONFIG_FILE} not found. "
            "Run the context updater from inside the context_update/ directory."
        )

    try:
        with open(CONFIG_FILE, "r", encoding="utf-8-sig") as file:
            config = json.load(file)
    except (UnicodeDecodeError, json.JSONDecodeError):
        raise ContextUpdateError(f"{CONFIG_FILE} is not valid JSON.")

    if not isinstance(config.get("memory_core_root"), str) or not config["memory_core_root"]:
        raise ContextUpdateError(f"{CONFIG_FILE}: 'memory_core_root' is missing.")

    required = {
        "input": ("changes_directory", "current_snapshot", "snapshot_history_directory"),
        "output": ("context_updates_directory", "backups_directory"),
    }

    for section, keys in required.items():
        if not isinstance(config.get(section), dict):
            raise ContextUpdateError(f"{CONFIG_FILE}: section '{section}' is missing.")

        for key in keys:
            if not isinstance(config[section].get(key), str) or not config[section][key]:
                raise ContextUpdateError(f"{CONFIG_FILE}: '{section}.{key}' is missing.")

    return config


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="REQUIEM Memory Core — Context Update Layer v" + VERSION
    )
    parser.add_argument("--approve", metavar="CU-NNN", help="approve a proposed context update")
    parser.add_argument("--reject", metavar="CU-NNN", help="reject a context update that is not applied")
    parser.add_argument("--apply", metavar="CU-NNN", help="apply an APPROVED context update")
    parser.add_argument(
        "--exclude", metavar="OP-N", nargs="+",
        help="operations to exclude (used with --approve)"
    )
    parser.add_argument("--note", metavar="TEXT", help="review note (used with --approve or --reject)")
    arguments = parser.parse_args()

    actions = [a for a in (arguments.approve, arguments.reject, arguments.apply) if a]

    if len(actions) > 1:
        raise ContextUpdateError("Use only one of --approve, --reject, --apply.")

    if arguments.exclude and not arguments.approve:
        raise ContextUpdateError("--exclude can be used only with --approve.")

    if arguments.note is not None and not (arguments.approve or arguments.reject):
        raise ContextUpdateError("--note can be used only with --approve or --reject.")

    return arguments


# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------

def now():
    return datetime.now().isoformat(timespec="seconds")


def sha256_bytes(raw):
    return hashlib.sha256(raw).hexdigest()


def is_int(value):
    return isinstance(value, int) and not isinstance(value, bool)


def is_hash(value):
    return isinstance(value, str) and HASH_PATTERN.match(value) is not None


def number(pattern, value):
    return int(pattern.match(value).group(1))


def read_bytes(path, label):
    if not os.path.isfile(path):
        raise ContextUpdateError(f"{label} not found: {path}")

    try:
        with open(path, "rb") as file:
            return file.read()
    except OSError as error:
        raise ContextUpdateError(f"{label} cannot be read: {path} ({error.strerror}).")


def parse_json(raw, path, label):
    try:
        return json.loads(raw.decode("utf-8-sig"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        raise ContextUpdateError(f"{label} is not valid JSON: {path}")


def target_path(config, target):
    return os.path.join(config["memory_core_root"], *target.split("/"))


def decode_text(raw, path):
    """Returns (text with '\\n' newlines, newline, has_bom, ends_with_newline)."""

    has_bom = raw.startswith(UTF8_BOM)
    body = raw[len(UTF8_BOM):] if has_bom else raw

    try:
        text = body.decode("utf-8")
    except UnicodeDecodeError:
        raise ContextUpdateError(f"{path} is not UTF-8 text.")

    newline = "\r\n" if "\r\n" in text else "\n"
    text = text.replace("\r\n", "\n")

    return text, newline, has_bom, text.endswith("\n")


def encode_text(text, newline, has_bom):
    data = text.replace("\n", newline).encode("utf-8")
    return (UTF8_BOM + data) if has_bom else data


# ---------------------------------------------------------------------------
# CHANGE RECORDS (read-only)
# ---------------------------------------------------------------------------

def validate_record(data, path, expected_id):

    def fail(message):
        raise ContextUpdateError(f"{path}: {message}")

    if not isinstance(data, dict):
        fail("change record is not a JSON object.")

    if data.get("format") != RECORD_FORMAT or data.get("format_version") != RECORD_FORMAT_VERSION:
        fail("unknown change record format or version.")

    if data.get("id") != expected_id:
        fail(f"contains id {data.get('id')}, expected {expected_id}.")

    if data.get("status") not in RECORD_STATUSES:
        fail("missing or invalid 'status'.")

    review = data.get("review")
    if not isinstance(review, dict) or not all(k in review for k in ("decision", "reviewed", "note")):
        fail("missing or invalid 'review'.")

    if data["status"] == RECORD_APPROVED:
        if review["decision"] != RECORD_APPROVED or not isinstance(review["reviewed"], str) \
                or len(review["reviewed"]) < 10:
            fail("approved record without a valid review.")

    if review["note"] is not None and not isinstance(review["note"], str):
        fail("invalid review note.")

    for side in ("from", "to"):
        value = data.get(side)
        if not isinstance(value, dict) or not isinstance(value.get("id"), str) \
                or not SNAPSHOT_ID_PATTERN.match(value["id"]) \
                or not is_hash(value.get("source_sha256")):
            fail(f"missing or invalid '{side}'.")

    summary = data.get("summary")
    keys = ("added", "removed", "modified", "unchanged", "unverified", "files_to", "directories_to")
    if not isinstance(summary, dict) or not all(is_int(summary.get(k)) for k in keys):
        fail("missing or invalid 'summary'.")

    if not isinstance(data.get("no_changes"), bool):
        fail("missing or invalid 'no_changes'.")


def load_records(config):
    """Returns {record_id: (record, record_sha256)}."""

    directory = config["input"]["changes_directory"]
    records = {}

    if not os.path.isdir(directory):
        return records

    for name in os.listdir(directory):
        stem, extension = os.path.splitext(name)

        if extension != ".json" or not RECORD_ID_PATTERN.match(stem):
            continue

        path = os.path.join(directory, name)
        raw = read_bytes(path, "Change record")
        data = parse_json(raw, path, "Change record")
        validate_record(data, path, stem)
        records[stem] = (data, sha256_bytes(raw))

    return records


# ---------------------------------------------------------------------------
# PROPOSALS (review/context_updates/)
# ---------------------------------------------------------------------------

def proposal_paths(config, proposal_id):
    directory = config["output"]["context_updates_directory"]

    return (
        os.path.join(directory, f"{proposal_id}.json"),
        os.path.join(directory, f"{proposal_id}.md"),
    )


def validate_proposal(data, path, expected_id):

    def fail(message):
        raise ContextUpdateError(f"{path}: {message}")

    if not isinstance(data, dict):
        fail("proposal is not a JSON object.")

    if data.get("format") != PROPOSAL_FORMAT or data.get("format_version") != VERSION:
        fail("unknown proposal format or version.")

    if data.get("id") != expected_id:
        fail(f"contains id {data.get('id')}, expected {expected_id}.")

    if not isinstance(data.get("created"), str):
        fail("missing 'created'.")

    status = data.get("status")
    if status not in PROPOSAL_STATUSES:
        fail("missing or invalid 'status'.")

    records = data.get("change_records")
    if not isinstance(records, list) or not records:
        fail("missing or invalid 'change_records'.")

    for item in records:
        if not isinstance(item, dict) or not isinstance(item.get("id"), str) \
                or not RECORD_ID_PATTERN.match(item["id"]) or not is_hash(item.get("record_sha256")):
            fail("invalid entry in 'change_records'.")

    operations = data.get("operations")
    if not isinstance(operations, list) or not operations:
        fail("missing or invalid 'operations'.")

    seen = set()

    for op in operations:
        if not isinstance(op, dict) or not isinstance(op.get("op"), str) or not OP_ID_PATTERN.match(op["op"]):
            fail("operation without a valid id.")

        if op["op"] in seen:
            fail(f"operation {op['op']} is listed more than once.")
        seen.add(op["op"])

        kind = op.get("kind")
        if kind not in ALLOWED:
            fail(f"{op['op']}: operation kind '{kind}' is not allowed.")

        allowed_type, allowed_targets = ALLOWED[kind]

        if op.get("type") != allowed_type:
            fail(f"{op['op']}: invalid type for {kind}.")

        if op.get("target") not in allowed_targets:
            fail(f"{op['op']}: target '{op.get('target')}' is not allowed for {kind}.")

        if not is_hash(op.get("target_sha256")):
            fail(f"{op['op']}: missing or invalid 'target_sha256'.")

        if op.get("decision") not in (None, DECISION_INCLUDE, DECISION_EXCLUDE):
            fail(f"{op['op']}: invalid 'decision'.")

        if kind == KIND_SNAPSHOT_STATE:
            if op.get("marker") != MARKER or not isinstance(op.get("before"), str) \
                    or not isinstance(op.get("after"), str) or not is_hash(op.get("snapshot_sha256")):
                fail(f"{op['op']}: invalid snapshot_state operation.")
        else:
            record = op.get("record")
            if not isinstance(record, dict) or set(record) != {"id", "date", "event", "impact"} \
                    or not isinstance(record["id"], str) or not EVENT_ID_PATTERN.match(record["id"]) \
                    or not all(isinstance(record[k], str) and record[k] for k in ("date", "event", "impact")):
                fail(f"{op['op']}: invalid event record.")

    review = data.get("review")
    if not isinstance(review, dict) or not all(k in review for k in ("decision", "reviewed", "note", "excluded")):
        fail("missing or invalid 'review'.")

    application = data.get("application")
    if not isinstance(application, dict) or not all(k in application for k in ("applied", "backup", "result_sha256")):
        fail("missing or invalid 'application'.")

    if not isinstance(data.get("warnings"), list):
        fail("missing or invalid 'warnings'.")


def load_proposals(config):
    directory = config["output"]["context_updates_directory"]
    proposals = []

    if not os.path.isdir(directory):
        return proposals

    for name in os.listdir(directory):
        stem, extension = os.path.splitext(name)

        if extension != ".json" or not PROPOSAL_ID_PATTERN.match(stem):
            continue

        path = os.path.join(directory, name)
        data = parse_json(read_bytes(path, "Proposal"), path, "Proposal")
        validate_proposal(data, path, stem)
        proposals.append(data)

    proposals.sort(key=lambda p: number(PROPOSAL_ID_PATTERN, p["id"]))

    return proposals


def load_proposal(config, proposal_id):
    if not PROPOSAL_ID_PATTERN.match(proposal_id):
        raise ContextUpdateError(f"Invalid proposal id: {proposal_id} (expected CU-NNN).")

    path, _ = proposal_paths(config, proposal_id)

    if not os.path.isfile(path):
        raise ContextUpdateError(f"Proposal {proposal_id} not found.")

    data = parse_json(read_bytes(path, "Proposal"), path, "Proposal")
    validate_proposal(data, path, proposal_id)

    return data


# ---------------------------------------------------------------------------
# SNAPSHOT STATE (facts from the stored snapshots)
# ---------------------------------------------------------------------------

def history_ids(config):
    directory = config["input"]["snapshot_history_directory"]
    ids = []

    if os.path.isdir(directory):
        for name in os.listdir(directory):
            stem, extension = os.path.splitext(name)
            if extension == ".json" and SNAPSHOT_ID_PATTERN.match(stem):
                ids.append(stem)

    return sorted(ids, key=lambda i: number(SNAPSHOT_ID_PATTERN, i))


def read_current_snapshot(config):
    path = config["input"]["current_snapshot"]
    raw = read_bytes(path, "Current snapshot")
    data = parse_json(raw, path, "Current snapshot")

    if not isinstance(data, dict) or not isinstance(data.get("id"), str) \
            or not SNAPSHOT_ID_PATTERN.match(data["id"]) \
            or not isinstance(data.get("statistics"), dict) \
            or not is_int(data["statistics"].get("total_files")) \
            or not is_int(data["statistics"].get("total_directories")):
        raise ContextUpdateError(f"{path}: invalid current snapshot.")

    return data, sha256_bytes(raw)


def snapshot_state_block(target, snapshot_id, history, files, directories):
    """The exact lines between the markers, in the format already used by each document."""

    listed = ", ".join(history) if history else "none"

    if target == README_TARGET:
        lines = [
            f"- current snapshot: {snapshot_id};",
            f"- preserved history: {listed}.",
        ]
    else:
        lines = [
            f"- current snapshot: {snapshot_id} (database/project_snapshot.json);",
            f"- preserved history: {listed} (database/snapshots/);",
            f"- project files tracked: {files};",
            f"- project directories tracked: {directories}.",
        ]

    return "\n".join(lines)


def find_marked_block(text, path):
    """Returns (lines, begin_index, end_index). Markers must appear exactly once each."""

    lines = text.split("\n")
    begins = [i for i, line in enumerate(lines) if line.strip() == MARKER_BEGIN]
    ends = [i for i, line in enumerate(lines) if line.strip() == MARKER_END]

    if len(begins) != 1 or len(ends) != 1 or begins[0] >= ends[0]:
        raise ContextUpdateError(
            f"{path}: markers {MARKER_BEGIN} / {MARKER_END} must appear exactly once, in this order."
        )

    return lines, begins[0], ends[0]


def replace_marked_block(text, path, new_block):
    lines, begin, end = find_marked_block(text, path)
    return "\n".join(lines[:begin + 1] + new_block.split("\n") + lines[end:])


def current_marked_block(text, path):
    lines, begin, end = find_marked_block(text, path)
    return "\n".join(lines[begin + 1:end])


# ---------------------------------------------------------------------------
# EVENTS (append only, format preserved)
# ---------------------------------------------------------------------------

def load_events(raw, path):
    data = parse_json(raw, path, "Events file")

    if not isinstance(data, list) or not all(
            isinstance(e, dict) and isinstance(e.get("id"), str) and EVENT_ID_PATTERN.match(e["id"])
            for e in data):
        raise ContextUpdateError(f"{path}: invalid events file.")

    return data


def append_event(text, path, record):
    """Appends one record before the closing ']' without reformatting the file."""

    stripped = text.rstrip()

    if not stripped.endswith("]"):
        raise ContextUpdateError(f"{path}: events file does not end with ']'.")

    tail = text[len(stripped):]
    body = stripped[:-1].rstrip()

    rendered = "\n".join(
        "  " + line for line in json.dumps(record, indent=2, ensure_ascii=False).split("\n")
    )

    if body.endswith("["):
        new_text = body + "\n" + rendered + "\n]" + tail
    else:
        new_text = body + ",\n" + rendered + "\n]" + tail

    return new_text


# ---------------------------------------------------------------------------
# PREPARE
# ---------------------------------------------------------------------------

def prepare(config):
    proposals = load_proposals(config)

    open_proposals = [p["id"] for p in proposals if p["status"] in OPEN_STATUSES]
    if open_proposals:
        raise ContextUpdateError(
            f"{', '.join(open_proposals)} is still open (PROPOSED or APPROVED). "
            "Apply or reject it before preparing a new proposal."
        )

    records = load_records(config)

    consumed = set()
    for proposal in proposals:
        if proposal["status"] == STATUS_APPLIED:
            consumed.update(item["id"] for item in proposal["change_records"])

    eligible = sorted(
        (rid for rid, (record, _) in records.items()
         if record["status"] == RECORD_APPROVED and rid not in consumed),
        key=lambda rid: number(RECORD_ID_PATTERN, rid)
    )

    if not eligible:
        raise ContextUpdateError(
            "No APPROVED change records waiting for a context update. Nothing was written."
        )

    operations = []
    warnings = []

    # 1. snapshot_state — from the latest eligible record, only if it ends at the current snapshot.
    last_id = eligible[-1]
    last = records[last_id][0]
    snapshot, snapshot_sha256 = read_current_snapshot(config)

    if snapshot["id"] != last["to"]["id"]:
        warnings.append(
            f"snapshot_state not proposed: {last_id} ends at {last['to']['id']}, "
            f"but the current snapshot is {snapshot['id']}."
        )
    elif snapshot_sha256 != last["to"]["source_sha256"]:
        warnings.append(
            f"snapshot_state not proposed: the current snapshot file differs from "
            f"{last['to']['id']} recorded in {last_id}."
        )
    else:
        history = history_ids(config)

        for target in SNAPSHOT_STATE_TARGETS:
            path = target_path(config, target)
            raw = read_bytes(path, "Target file")
            text = decode_text(raw, path)[0]

            try:
                before = current_marked_block(text, path)
            except ContextUpdateError as error:
                warnings.append(f"snapshot_state for {target} not proposed: {error}")
                continue

            after = snapshot_state_block(
                target, snapshot["id"], history,
                snapshot["statistics"]["total_files"],
                snapshot["statistics"]["total_directories"],
            )

            if before == after:
                warnings.append(f"snapshot_state for {target}: already up to date (not included).")
                continue

            operations.append({
                "op": None,
                "type": TYPE_REPLACE_MARKED_BLOCK,
                "kind": KIND_SNAPSHOT_STATE,
                "source": last_id,
                "target": target,
                "marker": MARKER,
                "target_sha256": sha256_bytes(raw),
                "snapshot_sha256": snapshot_sha256,
                "before": before,
                "after": after,
                "decision": None,
            })

    # 2. event — one per eligible record that has a human note.
    events_path = target_path(config, EVENTS_TARGET)
    events_raw = read_bytes(events_path, "Events file")
    events = load_events(events_raw, events_path)
    next_event = max([number(EVENT_ID_PATTERN, e["id"]) for e in events], default=0) + 1

    for rid in eligible:
        record = records[rid][0]
        note = record["review"]["note"]

        if not note or not note.strip():
            warnings.append(f"event for {rid} not proposed: no review note.")
            continue

        s = record["summary"]

        operations.append({
            "op": None,
            "type": TYPE_APPEND_RECORD,
            "kind": KIND_EVENT,
            "source": rid,
            "target": EVENTS_TARGET,
            "target_sha256": sha256_bytes(events_raw),
            "record": {
                "id": "EVENT-{:03d}".format(next_event),
                "date": record["review"]["reviewed"][:10],
                "event": (
                    f"Project changes approved ({rid}, {record['from']['id']} -> {record['to']['id']}): "
                    f"{s['added']} added, {s['removed']} removed, "
                    f"{s['modified']} modified, {s['unverified']} unverified."
                ),
                "impact": note.strip(),
            },
            "decision": None,
        })
        next_event += 1

    if not operations:
        raise ContextUpdateError(
            "No operations to propose. Nothing was written. Reasons: " + " ".join(warnings)
        )

    for index, op in enumerate(operations, start=1):
        op["op"] = f"OP-{index}"

    proposal_id = "CU-{:03d}".format(
        max([number(PROPOSAL_ID_PATTERN, p["id"]) for p in proposals], default=0) + 1
    )

    for path in proposal_paths(config, proposal_id):
        if os.path.exists(path):
            raise ContextUpdateError(f"{path} already exists. Nothing was overwritten.")

    proposal = {
        "format": PROPOSAL_FORMAT,
        "format_version": VERSION,
        "id": proposal_id,
        "created": now(),
        "status": STATUS_PROPOSED,
        "change_records": [
            {"id": rid, "record_sha256": records[rid][1]} for rid in eligible
        ],
        "operations": operations,
        "review": {"decision": None, "reviewed": None, "note": None, "excluded": []},
        "application": {"applied": None, "backup": None, "result_sha256": {}},
        "warnings": warnings,
    }

    os.makedirs(config["output"]["context_updates_directory"], exist_ok=True)
    write_proposal(config, proposal)

    print("Memory Core context update completed.")
    print(f"Proposal {proposal_id}: {STATUS_PROPOSED}")
    print(f"Change records: {', '.join(eligible)}")
    for op in operations:
        print(f"{op['op']}: {op['kind']} -> {op['target']}")
    for warning in warnings:
        print(f"Note: {warning}")


# ---------------------------------------------------------------------------
# REVIEW
# ---------------------------------------------------------------------------

def approve(config, proposal_id, excluded, note):
    proposal = load_proposal(config, proposal_id)

    if proposal["status"] != STATUS_PROPOSED:
        raise ContextUpdateError(f"{proposal_id} is {proposal['status']}. Only PROPOSED can be approved.")

    op_ids = [op["op"] for op in proposal["operations"]]
    excluded = list(dict.fromkeys(excluded or []))

    unknown = [op for op in excluded if op not in op_ids]
    if unknown:
        raise ContextUpdateError(f"Unknown operation(s) in --exclude: {', '.join(unknown)}.")

    if len(excluded) == len(op_ids):
        raise ContextUpdateError("All operations are excluded. Use --reject instead.")

    for op in proposal["operations"]:
        op["decision"] = DECISION_EXCLUDE if op["op"] in excluded else DECISION_INCLUDE

    # Included events get consecutive ids, so an excluded event leaves no gap.
    event_ops = [op for op in proposal["operations"] if op["kind"] == KIND_EVENT]

    if event_ops:
        next_event = min(number(EVENT_ID_PATTERN, op["record"]["id"]) for op in event_ops)

        for op in event_ops:
            if op["decision"] == DECISION_INCLUDE:
                op["record"]["id"] = "EVENT-{:03d}".format(next_event)
                next_event += 1

    proposal["status"] = STATUS_APPROVED
    proposal["review"] = {
        "decision": STATUS_APPROVED,
        "reviewed": now(),
        "note": (note.strip() or None) if note is not None else None,
        "excluded": excluded,
    }

    write_proposal(config, proposal)

    print("Memory Core context update completed.")
    print(f"Proposal {proposal_id}: {STATUS_APPROVED}")
    for op in proposal["operations"]:
        print(f"{op['op']}: {op['decision']}")
    print(f"Apply with: python context_updater.py --apply {proposal_id}")


def reject(config, proposal_id, note):
    proposal = load_proposal(config, proposal_id)

    if proposal["status"] not in OPEN_STATUSES:
        raise ContextUpdateError(
            f"{proposal_id} is {proposal['status']}. Only PROPOSED or APPROVED can be rejected."
        )

    proposal["status"] = STATUS_REJECTED
    proposal["review"] = {
        "decision": STATUS_REJECTED,
        "reviewed": now(),
        "note": (note.strip() or None) if note is not None else None,
        "excluded": proposal["review"].get("excluded", []),
    }

    write_proposal(config, proposal)

    print("Memory Core context update completed.")
    print(f"Proposal {proposal_id}: {STATUS_REJECTED}")


# ---------------------------------------------------------------------------
# APPLY
# ---------------------------------------------------------------------------

def mark_stale(config, proposal, reason):
    proposal["status"] = STATUS_STALE
    proposal["warnings"].append(f"STALE: {reason}")
    write_proposal(config, proposal)

    raise ContextUpdateError(
        f"{proposal['id']} is STALE: {reason} Project memory was not changed. "
        "Prepare a new proposal."
    )


def apply(config, proposal_id):
    proposal = load_proposal(config, proposal_id)

    if proposal["status"] != STATUS_APPROVED:
        raise ContextUpdateError(
            f"{proposal_id} is {proposal['status']}. Only APPROVED proposals can be applied."
        )

    included = [op for op in proposal["operations"] if op["decision"] == DECISION_INCLUDE]

    if not included:
        raise ContextUpdateError(f"{proposal_id} has no included operations.")

    # 1. Change records must be exactly the approved records used for the proposal.
    records = load_records(config)

    for item in proposal["change_records"]:
        if item["id"] not in records:
            mark_stale(config, proposal, f"change record {item['id']} is missing.")

        record, record_sha256 = records[item["id"]]

        if record_sha256 != item["record_sha256"] or record["status"] != RECORD_APPROVED:
            mark_stale(config, proposal, f"change record {item['id']} changed since preparation.")

    # 2. Snapshot must still be the one used for snapshot_state.
    if any(op["kind"] == KIND_SNAPSHOT_STATE for op in included):
        _, snapshot_sha256 = read_current_snapshot(config)

        for op in included:
            if op["kind"] == KIND_SNAPSHOT_STATE and op["snapshot_sha256"] != snapshot_sha256:
                mark_stale(config, proposal, "the current snapshot changed since preparation.")

    # 3. Targets must be byte-identical to the prepared state. Build new contents in memory.
    targets = sorted({op["target"] for op in included})
    originals = {}
    updated = {}

    for target in targets:
        # Defensive whitelist check (also enforced by validation).
        if not any(target in allowed[1] for allowed in ALLOWED.values()):
            raise ContextUpdateError(f"Target {target} is not allowed.")

        path = target_path(config, target)
        raw = read_bytes(path, "Target file")

        for op in included:
            if op["target"] == target and op["target_sha256"] != sha256_bytes(raw):
                mark_stale(config, proposal, f"{target} changed since preparation.")

        text, newline, has_bom, _ = decode_text(raw, path)
        new_text = text

        for op in [o for o in included if o["target"] == target]:
            if op["kind"] == KIND_SNAPSHOT_STATE:
                if current_marked_block(new_text, path) != op["before"]:
                    mark_stale(config, proposal, f"{target}: marked block differs from 'before'.")
                new_text = replace_marked_block(new_text, path, op["after"])
            else:
                existing = load_events(new_text.encode("utf-8"), path)
                if any(e["id"] == op["record"]["id"] for e in existing):
                    mark_stale(config, proposal, f"{op['record']['id']} already exists in {target}.")
                new_text = append_event(new_text, path, op["record"])

        # 4. Verify the new content before anything is written.
        if target == EVENTS_TARGET:
            old_events = load_events(raw, path)
            new_events = load_events(new_text.encode("utf-8"), path)
            added = [op["record"] for op in included if op["target"] == target]
            if new_events != old_events + added:
                raise ContextUpdateError(f"Verification of new {target} failed. Nothing was written.")
        else:
            op = [o for o in included if o["target"] == target][0]
            if current_marked_block(new_text, path) != op["after"]:
                raise ContextUpdateError(f"Verification of new {target} failed. Nothing was written.")

        originals[target] = raw
        updated[target] = encode_text(new_text, newline, has_bom)

    # 5. Backup (never overwritten).
    backup_root = os.path.join(config["output"]["backups_directory"], proposal_id)

    if os.path.exists(backup_root):
        raise ContextUpdateError(f"{backup_root} already exists. Nothing was overwritten.")

    try:
        for target in targets:
            backup_file = os.path.join(backup_root, *target.split("/"))
            os.makedirs(os.path.dirname(backup_file), exist_ok=True)

            with open(backup_file, "xb") as file:
                file.write(originals[target])
                file.flush()
                os.fsync(file.fileno())

            with open(backup_file, "rb") as file:
                if file.read() != originals[target]:
                    raise ContextUpdateError(
                        f"Backup verification failed: {backup_file}. Project memory was not changed."
                    )
    except OSError as error:
        raise ContextUpdateError(f"Backup failed ({error}). Project memory was not changed.")

    # 6. Write targets atomically; restore from backup if any write fails.
    written = []

    try:
        for target in targets:
            write_bytes_atomic(target_path(config, target), updated[target])
            written.append(target)

            with open(target_path(config, target), "rb") as file:
                if file.read() != updated[target]:
                    raise OSError(f"verification of {target} failed after writing")

    except OSError as error:
        restored = []
        not_restored = []
        for target in written:
            try:
                write_bytes_atomic(target_path(config, target), originals[target])
                restored.append(target)
            except OSError:
                not_restored.append(target)

        # The backup directory now exists, so this proposal cannot be applied again.
        proposal["status"] = STATUS_STALE
        proposal["warnings"].append(
            f"STALE: apply failed ({error}). Restored: {', '.join(restored) or '-'}. "
            f"Not restored: {', '.join(not_restored) or '-'}."
        )
        try:
            write_proposal(config, proposal)
        except ContextUpdateError:
            pass

        raise ContextUpdateError(
            f"Apply failed ({error}). Restored from backup: {', '.join(restored) or 'nothing to restore'}. "
            f"NOT restored: {', '.join(not_restored) or 'none'}. Backup: {backup_root}. "
            f"{proposal_id} is STALE. Prepare a new proposal."
        )

    # 7. Record the application.
    proposal["status"] = STATUS_APPLIED
    proposal["application"] = {
        "applied": now(),
        "backup": os.path.relpath(backup_root, config["memory_core_root"]).replace("\\", "/"),
        "result_sha256": {target: sha256_bytes(updated[target]) for target in targets},
    }

    try:
        write_proposal(config, proposal)
    except ContextUpdateError as error:
        raise ContextUpdateError(
            f"Targets were applied, but {proposal_id} could not be marked APPLIED ({error}). "
            f"Backup: {backup_root}"
        )

    print("Memory Core context update completed.")
    print(f"Proposal {proposal_id}: {STATUS_APPLIED}")
    for op in included:
        print(f"{op['op']}: {op['kind']} -> {op['target']}")
    print(f"Backup: {proposal['application']['backup']}")


# ---------------------------------------------------------------------------
# WRITE
# ---------------------------------------------------------------------------

def write_bytes_atomic(path, data):
    temporary = path + ".tmp"

    with open(temporary, "wb") as file:
        file.write(data)
        file.flush()
        os.fsync(file.fileno())

    os.replace(temporary, path)


def write_proposal(config, proposal):
    json_path, md_path = proposal_paths(config, proposal["id"])
    outputs = [
        (json_path, (json.dumps(proposal, indent=2, ensure_ascii=False) + "\n").encode("utf-8")),
        (md_path, create_markdown(proposal).encode("utf-8")),
    ]

    temporaries = []

    try:
        for path, data in outputs:
            temporary = path + ".tmp"
            with open(temporary, "wb") as file:
                file.write(data)
                file.flush()
                os.fsync(file.fileno())
            temporaries.append((temporary, path))
    except OSError as error:
        for temporary, _ in temporaries:
            try:
                os.remove(temporary)
            except OSError:
                pass
        raise ContextUpdateError(f"Could not write proposal ({error}). Existing files were left untouched.")

    for temporary, path in temporaries:
        try:
            os.replace(temporary, path)
        except OSError as error:
            raise ContextUpdateError(
                f"Could not replace {path} ({error}). The complete new version is kept in {temporary}."
            )


# ---------------------------------------------------------------------------
# REPORT (.md)
# ---------------------------------------------------------------------------

def create_markdown(proposal):
    review = proposal["review"]
    application = proposal["application"]
    lines = []

    lines.append("# REQUIEM MEMORY CORE CONTEXT UPDATE")
    lines.append("")
    lines.append(f"Proposal: {proposal['id']}")
    lines.append(f"Created: {proposal['created']}")
    lines.append(f"Status: {proposal['status']}")
    lines.append(f"Change records: {', '.join(item['id'] for item in proposal['change_records'])}")
    lines.append("")

    lines.append("## Review")
    lines.append("")
    lines.append(f"Decision: {review['decision'] or 'pending'}")
    lines.append("")
    lines.append(f"Reviewed: {review['reviewed'] or '-'}")
    lines.append("")
    lines.append(f"Note: {review['note'] if review['note'] else '-'}")
    lines.append("")
    lines.append(f"Excluded: {', '.join(review['excluded']) if review['excluded'] else '-'}")
    lines.append("")

    lines.append("## Operations")
    lines.append("")

    for op in proposal["operations"]:
        lines.append(f"### {op['op']} — {op['kind']} -> {op['target']}")
        lines.append("")
        lines.append(f"Source: {op.get('source', '-')}")
        lines.append("")
        lines.append(f"Decision: {op['decision'] or 'pending'}")
        lines.append("")

        if op["kind"] == KIND_SNAPSHOT_STATE:
            lines.append("Before:")
            lines.append("")
            lines.append("```")
            lines.append(op["before"])
            lines.append("```")
            lines.append("")
            lines.append("After:")
            lines.append("")
            lines.append("```")
            lines.append(op["after"])
            lines.append("```")
        else:
            lines.append("New record (appended):")
            lines.append("")
            lines.append("```json")
            lines.append(json.dumps(op["record"], indent=2, ensure_ascii=False))
            lines.append("```")
        lines.append("")

    lines.append("## Warnings")
    lines.append("")
    if proposal["warnings"]:
        for warning in proposal["warnings"]:
            lines.append(f"- {warning}")
    else:
        lines.append("- none")
    lines.append("")

    if proposal["status"] == STATUS_APPLIED:
        lines.append("## Application")
        lines.append("")
        lines.append(f"Applied: {application['applied']}")
        lines.append("")
        lines.append(f"Backup: {application['backup']}")
        lines.append("")
        for target, digest in application["result_sha256"].items():
            lines.append(f"- {target}: {digest}")
        lines.append("")

    if proposal["status"] == STATUS_PROPOSED:
        lines.append("## How to review")
        lines.append("")
        lines.append("Run from context_update/:")
        lines.append("")
        lines.append("```")
        lines.append(f"python context_updater.py --approve {proposal['id']}")
        lines.append(f"python context_updater.py --approve {proposal['id']} --exclude OP-1")
        lines.append(f"python context_updater.py --reject {proposal['id']} --note \"...\"")
        lines.append("```")
        lines.append("")

    if proposal["status"] == STATUS_APPROVED:
        lines.append("## How to apply")
        lines.append("")
        lines.append("Run from context_update/:")
        lines.append("")
        lines.append("```")
        lines.append(f"python context_updater.py --apply {proposal['id']}")
        lines.append("```")
        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------

def main():

    config = load_config()

    arguments = parse_arguments()

    if arguments.approve:
        approve(config, arguments.approve, arguments.exclude, arguments.note)
    elif arguments.reject:
        reject(config, arguments.reject, arguments.note)
    elif arguments.apply:
        apply(config, arguments.apply)
    else:
        prepare(config)


if __name__ == "__main__":
    try:
        main()
    except ContextUpdateError as error:
        print(f"Memory Core context update aborted: {error}")
        sys.exit(1)
