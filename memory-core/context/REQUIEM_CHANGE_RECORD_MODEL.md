# REQUIEM CHANGE RECORD MODEL

Version: 0.2

Document Type:
Change Record Definition

Purpose:
Define how REQUIEM Memory Core turns a comparison result into a reviewed change record.

---

# 1. PURPOSE

A change record (CHG-NNN) preserves the facts of one comparison:

"What changed between SNAP-A and SNAP-B?"

The comparison result is kept only as the latest report (DEC-008).

A change record keeps these facts as history that a human reviews.

---

# 2. CORE PRINCIPLE

A change record stores facts copied from the comparison result.

It does not store:

- assumptions;
- conclusions;
- evaluations.

The only addition is a mechanical grouping by top-level folder ("area").

The only human content is the review decision and the review note.

---

# 3. POSITION IN MEMORY CORE

```
Comparison      reports/latest_comparison.json
↓
Change Report   change_report/change_reporter.py   — this model
↓
Analysis        analysis/analyzer.py               — REQUIEM_ANALYSIS_MODEL.md
↓
Human review    APPROVED / REJECTED
↓
Context Update  context_update/context_updater.py
```

Change Report Layer:

- reads reports/latest_comparison.json (read-only);
- reads snapshots only to verify their hashes (read-only);
- writes only to review/changes/;
- does not run the comparator or the scanner;
- does not modify project memory (database/, context/, README).

Change records are stored outside project memory (DEC-009).

The Analysis Layer reads change records (read-only) to support the review (DEC-014, DEC-015).

It does not modify them. The change reporter does not require an analysis before --approve or --reject.

---

# 4. RUNNING

The change reporter uses paths relative to the change_report directory.

It must be started from inside:

change_report/

Commands:

```
python change_reporter.py
python change_reporter.py --approve CHG-001 --note "text"
python change_reporter.py --reject CHG-001 --note "text"
```

Settings are read only from:

change_report/change_report_config.json

---

# 5. CREATING A RECORD

Command without arguments.

Input:

reports/latest_comparison.json

Checks (in this order):

1. The comparison result is valid:
   - format "requiem-comparison", format_version "0.1";
   - id, generated, status, from, to, project, summary, changes, warnings are present and valid;
   - every path appears in only one entry;
   - a null hash appears only in the unverified class;
   - a modified entry has two different hashes;
   - summary counts equal the number of listed entries;
   - classified files add up to files_from and files_to.
2. Both snapshots still match the comparison:
   - each snapshot is found by id (history first, then current snapshot);
   - its SHA-256 must equal source_sha256 recorded in the comparison.
3. Every existing change record is valid.
4. Chain rules (DEC-012):
   - "from" and "to" must be different snapshots;
   - the same snapshot pair must not be recorded twice;
   - the project must be the same as in the previous record;
   - "from" must equal "to" of the previous record.

On a chain break the message shows the comparator command that continues the chain, for example:

```
python comparator.py --from SNAP-003 --to SNAP-005
```

A record is created also when there are no changes (DEC-013).

---

# 6. RECORD STRUCTURE

File:

review/changes/CHG-NNN.json

Example (shortened):

```json
{
  "format": "requiem-change-record",
  "format_version": "0.1",
  "id": "CHG-001",
  "created": "2026-09-24T13:50:00",
  "status": "PENDING_REVIEW",
  "review": { "decision": null, "reviewed": null, "note": null },

  "comparison": {
    "id": "CMP-001-003",
    "generated": "2026-09-24T13:09:47",
    "status": "COMPLETED",
    "result_sha256": "…"
  },
  "from": { "id": "SNAP-001", "created": "…", "source_sha256": "…" },
  "to":   { "id": "SNAP-003", "created": "…", "source_sha256": "…" },
  "project": { "name": "REQUIEM", "target": "requiem-tauri" },

  "summary": {
    "added": 0, "removed": 0, "modified": 1, "unchanged": 61, "unverified": 0,
    "files_from": 62, "files_to": 62, "directories_from": 32, "directories_to": 32
  },
  "no_changes": false,

  "areas": [
    { "area": "src", "added": 0, "removed": 0, "modified": 1, "unverified": 0 }
  ],

  "entries": [
    {
      "entry": "CHG-001/1",
      "class": "modified",
      "path": "src/App.jsx",
      "area": "src",
      "changed_fields": ["size", "modified", "hash"],
      "from": { "size": 41427, "modified": "…", "hash": "…" },
      "to":   { "size": 41430, "modified": "…", "hash": "…" }
    }
  ],

  "warnings": []
}
```

Field notes:

- comparison.result_sha256: SHA-256 of reports/latest_comparison.json used for the record;
- summary: copied from the comparison;
- no_changes: true when added, removed, modified and unverified are all 0;
- warnings: a warning for unverified files, then the comparison warnings prefixed "Comparison: ".

---

# 7. ENTRIES

Entries list every changed file.

Unchanged files are not listed (their number is in summary).

Order:

- by class: added, removed, modified, unverified;
- inside a class: by path.

Entry id:

CHG-NNN/k (k = position, starting from 1).

Common fields:

- entry, class, path, area, from, to.

By class:

| Class | from | to | Extra fields |
|---|---|---|---|
| added | null | size, extension, modified, hash | — |
| removed | size, extension, modified, hash | null | — |
| modified | size, modified, hash | size, modified, hash | changed_fields |
| unverified | size, extension, modified, hash — or null | size, extension, modified, hash — or null | presence, reason |

Modified entries have no "extension" because the comparison result does not contain it.

Area:

- the first path segment (for example "src", "src-tauri");
- "(root)" for files in the project root.

areas:

Number of added, removed, modified and unverified entries per area, sorted by area name.

---

# 8. STATUSES AND REVIEW

```
PENDING_REVIEW
↓
APPROVED | REJECTED
```

Review commands:

- --approve CHG-NNN [--note "text"]
- --reject CHG-NNN [--note "text"]

Rules:

- only a PENDING_REVIEW record can be reviewed;
- a reviewed record cannot be changed;
- the note is stored without leading and trailing spaces; an empty note is stored as null;
- review.reviewed stores the review time;
- a record approved without a note will not produce an event in Context Update.

Review rewrites the .json and .md files of the same record only.

Rejected records are not deleted.

---

# 9. REPORT

File:

review/changes/CHG-NNN.md

Sections:

- record id, created, status, project;
- review (decision, reviewed, note);
- source (comparison, snapshots from / to);
- summary (count per class, files and directories from → to, no changes);
- UNVERIFIED FILES (always present, shown before other changes);
- areas;
- added, removed, modified (before → after);
- warnings;
- how to review (only while PENDING_REVIEW).

---

# 10. ABORT RULES

Nothing is written and the exit code is 1 if:

- change_report_config.json is not found or is invalid;
- --approve and --reject are used together;
- --note is used without --approve or --reject;
- the comparison result is missing, not valid JSON, of unknown format or invalid;
- a snapshot is not found or its SHA-256 differs from the comparison;
- an existing change record is invalid;
- a chain rule is broken;
- a record file with the new id already exists;
- a record to review is not found, has an invalid id or is already reviewed.

The message starts with:

"Memory Core change report aborted:"

---

# 11. STORAGE RULE

```
review/changes/CHG-NNN.json
review/changes/CHG-NNN.md
```

- a new id is the highest existing number + 1;
- ids are never reused or renumbered;
- a new record never overwrites an existing file;
- records are never deleted;
- both files are fully written to .tmp files, then each replaces its target.

---

# 12. LIMITATIONS OF v0.1

- A record is approved or rejected as a whole, not per file.
- Manual edits of record files are detected only by structure validation (Context Update also checks record_sha256).
- The two record files are replaced one after another.
- review/changes/ grows without limit.
- Each step of the chain needs a comparison of exactly that snapshot pair.

---

# 13. NOT PART OF v0.1

- per-file review;
- change evaluation;
- automatic approval;
- deletion or archiving of records;
- AI analysis.

END OF CHANGE RECORD MODEL
