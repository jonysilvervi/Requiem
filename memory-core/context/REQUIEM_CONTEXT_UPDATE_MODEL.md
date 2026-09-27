# REQUIEM CONTEXT UPDATE MODEL

Version: 0.1

Document Type:
Context Update Definition

Purpose:
Define how REQUIEM Memory Core prepares, approves and applies controlled updates of project context.

---

# 1. PURPOSE

Context Update turns APPROVED change records into a proposal (CU-NNN):

a list of exact operations on project memory, with "before" and "after".

Project memory is changed only when a human applies an APPROVED proposal.

---

# 2. CORE PRINCIPLE

Context Update does not invent content.

Its content comes only from:

- facts of the stored snapshots;
- facts of approved change records;
- the review note written by a human.

---

# 3. POSITION IN MEMORY CORE

```
Change Report   review/changes/CHG-NNN          — APPROVED only
↓
Context Update  context_update/context_updater.py   — this model
↓
Proposal        review/context_updates/CU-NNN   — PROPOSED
↓
Human review    APPROVED / REJECTED
↓
Manual apply    --apply CU-NNN
↓
Project memory  README.md, context/REQUIEM_CONTEXT.md, database/events.json
```

Context Update Layer:

- reads change records (never modifies them);
- writes proposals to review/context_updates/;
- writes backups to review/backups/;
- changes project memory only through --apply of an APPROVED proposal, after hash verification and backup (DEC-010);
- has only two operations with hard-coded targets (DEC-011).

---

# 4. RUNNING

The context updater uses paths relative to the context_update directory.

It must be started from inside:

context_update/

Commands:

```
python context_updater.py
python context_updater.py --approve CU-001
python context_updater.py --approve CU-001 --exclude OP-2 OP-3
python context_updater.py --reject CU-001 --note "text"
python context_updater.py --apply CU-001
```

--note can be used with --approve and --reject.

Settings are read only from:

context_update/context_update_config.json

---

# 5. OPERATIONS AND TARGETS

Only these operations exist.

Targets are hard-coded in the code and cannot be changed by configuration.

| Operation | Type | Targets |
|---|---|---|
| snapshot_state | replace_marked_block | README.md, context/REQUIEM_CONTEXT.md |
| event | append_record | database/events.json |

Never targets:

- database/identity.json;
- database/decisions.json;
- database/checkpoints.json;
- database/state.json;
- snapshots, protocols, models, CHANGELOG, code.

A proposal with any other operation or target is refused.

---

# 6. PREPARING A PROPOSAL

Command without arguments.

Rules:

1. Only one proposal can be open (PROPOSED or APPROVED) at a time.
2. Eligible change records:
   - status APPROVED;
   - not included in any APPLIED proposal.
   Records of REJECTED or STALE proposals become eligible again.
   PENDING_REVIEW and REJECTED change records are never used.
3. No eligible records → nothing is written.

snapshot_state

- source: the last eligible record;
- proposed only if its "to" is the current snapshot and the current snapshot file has the SHA-256 recorded in the change record;
- for each target the text between the markers is generated from the current snapshot and the history directory;
- a target without valid markers is skipped with a warning;
- a target whose text is already the same is not included (noted in warnings).

event

- one event per eligible record that has a review note;
- a record without a note gets no event (noted in warnings);
- id: highest existing EVENT number + 1, consecutive;
- date: date of the change record review;
- event: "Project changes approved (CHG-NNN, SNAP-A -> SNAP-B): N added, N removed, N modified, N unverified.";
- impact: the review note of the change record.

If no operation remains, nothing is written and the reasons are shown.

---

# 7. MARKERS

snapshot_state changes only the lines between these marker lines:

```
<!-- MEMORY:SNAPSHOT_STATE:BEGIN -->
<!-- MEMORY:SNAPSHOT_STATE:END -->
```

Each marker must appear exactly once, BEGIN before END.

Generated block — README.md:

```
- current snapshot: SNAP-NNN;
- preserved history: SNAP-001, SNAP-002.
```

Generated block — context/REQUIEM_CONTEXT.md:

```
- current snapshot: SNAP-NNN (database/project_snapshot.json);
- preserved history: SNAP-001, SNAP-002 (database/snapshots/);
- project files tracked: N;
- project directories tracked: N.
```

An empty history is written as "none".

Text between the markers must not be edited by hand in another format, otherwise the next proposal shows the difference as a change.

---

# 8. PROPOSAL STRUCTURE

File:

review/context_updates/CU-NNN.json

Example (shortened):

```json
{
  "format": "requiem-context-update",
  "format_version": "0.1",
  "id": "CU-001",
  "created": "…",
  "status": "PROPOSED",
  "change_records": [ { "id": "CHG-002", "record_sha256": "…" } ],

  "operations": [
    {
      "op": "OP-1",
      "type": "replace_marked_block",
      "kind": "snapshot_state",
      "source": "CHG-002",
      "target": "README.md",
      "marker": "SNAPSHOT_STATE",
      "target_sha256": "…",
      "snapshot_sha256": "…",
      "before": "…",
      "after": "…",
      "decision": null
    },
    {
      "op": "OP-2",
      "type": "append_record",
      "kind": "event",
      "source": "CHG-002",
      "target": "database/events.json",
      "target_sha256": "…",
      "record": {
        "id": "EVENT-009",
        "date": "…",
        "event": "Project changes approved (…): …",
        "impact": "<review note>"
      },
      "decision": null
    }
  ],

  "review": { "decision": null, "reviewed": null, "note": null, "excluded": [] },
  "application": { "applied": null, "backup": null, "result_sha256": {} },
  "warnings": []
}
```

Field notes:

- record_sha256: SHA-256 of the change record file at preparation;
- target_sha256: SHA-256 of the target file at preparation;
- snapshot_sha256: SHA-256 of the current snapshot file at preparation;
- decision: include or exclude (set on approval).

---

# 9. STATUSES AND REVIEW

```
PROPOSED
↓
APPROVED | REJECTED
↓
APPLIED | STALE
```

--approve CU-NNN [--exclude OP-N ...]

- only PROPOSED can be approved;
- unknown operation ids are refused;
- excluding all operations is refused (use --reject);
- included events get consecutive ids, so an excluded event leaves no gap.

--reject CU-NNN

- PROPOSED or APPROVED (not applied) can be rejected.

STALE

- set when apply finds that something changed since preparation, or when apply fails.
- a STALE proposal cannot be applied; a new proposal must be prepared.

---

# 10. APPLY

--apply CU-NNN

The proposal must be APPROVED and have included operations; otherwise the command is refused.

Checks (any mismatch → STALE, project memory not changed):

1. every change record exists, is APPROVED and has the recorded record_sha256;
2. if snapshot_state is included: the current snapshot has the recorded snapshot_sha256;
3. every target has the recorded target_sha256;
4. the marked block equals "before"; the event id does not exist yet.

Then:

1. new contents are built in memory and verified
   (events: new list = old list + appended records; markers: block = "after");
2. originals are copied to review/backups/CU-NNN/<target path> and verified byte for byte
   (an existing backup directory is never overwritten);
3. targets are written one by one (.tmp → replace) and read back for verification;
4. on a write failure, already written targets are restored from the backup and the proposal becomes STALE;
5. on success the proposal becomes APPLIED with application.applied, application.backup and application.result_sha256.

Format preservation:

- line endings (LF / CRLF), UTF-8 BOM and final newline of each target are kept;
- events are appended before the closing "]" with the same 2-space indentation; existing lines are not changed;
- only the lines between the markers are changed.

---

# 11. REPORT

File:

review/context_updates/CU-NNN.md

Sections:

- proposal id, created, status, change records;
- review (decision, reviewed, note, excluded);
- operations (before / after, or the event record);
- warnings;
- application (only when APPLIED);
- how to review (only when PROPOSED);
- how to apply (only when APPROVED).

---

# 12. ABORT RULES

The message starts with:

"Memory Core context update aborted:"

The exit code is 1.

Examples:

- context_update_config.json is not found or is invalid;
- more than one of --approve, --reject, --apply is used;
- --exclude is used without --approve, or --note without --approve / --reject;
- a proposal is still open;
- no eligible change records or no operations to propose;
- a proposal or change record is invalid;
- a proposal has a forbidden operation or target;
- a proposal is not in the required status;
- a check of section 10 fails (the proposal becomes STALE).

---

# 13. STORAGE RULE

```
review/context_updates/CU-NNN.json
review/context_updates/CU-NNN.md
review/backups/CU-NNN/<target path>
```

- a new id is the highest existing number + 1;
- ids are never reused or renumbered;
- proposals and backups are never deleted by the layer.

Backups are restore copies of one proposal.

They are not checkpoints (DEC-005).

---

# 14. LIMITATIONS OF v0.1

- Several target files cannot be written as one atomic step; protection is hash verification, backup and restore.
- A scan between preparation and apply makes a proposal with snapshot_state STALE.
- Editing README.md, context/REQUIEM_CONTEXT.md or database/events.json while a proposal is open makes it STALE.
- There is no restore command; a backup is restored by hand.
- snapshot_state is proposed only if the latest approved record ends at the current snapshot.
- database/events.json contains both Memory Core milestones and project change events.
- review/context_updates/ and review/backups/ grow without limit.

---

# 15. NOT PART OF v0.1

- other operations or targets;
- automatic apply;
- restore command;
- AI analysis;
- application integration.

END OF CONTEXT UPDATE MODEL
