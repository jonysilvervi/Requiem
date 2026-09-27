# REQUIEM COMPARISON MODEL

Version: 0.2

Document Type:
Comparison Definition

Purpose:
Define how REQUIEM Memory Core compares two project state snapshots.

---

# 1. PURPOSE

Comparison answers:

"What changed between these states?"

Comparison works only with existing snapshot data.

Comparison is not an analysis.

It does not decide whether a change is good or bad.

---

# 2. CORE PRINCIPLE

Comparison produces facts derived from facts.

It does not store:

- assumptions;
- conclusions;
- recommendations.

The same pair of snapshots always gives the same result content.

Only the "generated" field differs between runs.

---

# 3. POSITION IN MEMORY CORE

```
Observation   scanner/scanner.py            — creates snapshots
↓
Storage       database/project_snapshot.json
              database/snapshots/SNAP-NNN.json
↓
Comparison    comparison/comparator.py       — this model
↓
Change Report change_report/change_reporter.py — REQUIEM_CHANGE_RECORD_MODEL.md
↓
Analysis      analysis/analyzer.py           — REQUIEM_ANALYSIS_MODEL.md
↓
Decision      — human
```

Comparison Layer is an isolated read-only layer (DEC-006).

It:

- reads snapshots only;
- never writes to database/;
- does not run the scanner;
- is not run by the scanner;
- does not read or modify project files;
- does not modify documentation;
- does not use AI;
- is not integrated with Tauri.

---

# 4. RUNNING

The comparator uses paths relative to the comparison directory.

It must be started from inside:

comparison/

Commands:

```
python comparator.py
python comparator.py --from SNAP-001 --to SNAP-003
```

Settings are read only from:

comparison/comparison_config.json

---

# 5. INPUT — SNAPSHOT PAIR

Default pair (no arguments):

- to: current snapshot (database/project_snapshot.json);
- from: the snapshot with the highest number in database/snapshots/ that is lower than the number of "to".

Explicit pair:

- --from SNAP-NNN --to SNAP-NNN;
- both arguments must be given together;
- an id is searched in database/snapshots/ first, then in the current snapshot.

Order:

- "from" must not be newer than "to" (by snapshot number);
- the same snapshot on both sides is allowed (every file is unchanged).

---

# 6. CLASSIFICATION

Comparison key:

path

Classification is decided by content hash.

Rules are applied in this order:

| Condition | Class |
|---|---|
| hash is null in "from" or in "to" | unverified |
| path exists only in "to" | added |
| path exists only in "from" | removed |
| path exists in both, hashes differ | modified |
| path exists in both, hashes equal | unchanged |

Unverified rule (DEC-007):

A file with null hash on either side is classified as unverified.

It is never forced into added, removed, modified or unchanged.

Every file appears in exactly one class.

---

# 7. FILE ENTRIES

added / removed

- path, size, extension, modified, hash.

modified

- path;
- changed_fields;
- from: size, modified, hash;
- to: size, modified, hash.

unchanged

- path;
- changed_fields.

A file whose hash is equal but whose modification time differs stays unchanged.

Its changed_fields contains "modified".

unverified

- path;
- presence: both | from_only | to_only;
- reason: hash_null_from | hash_null_to | hash_null_both;
- from: size, extension, modified, hash — or null if absent;
- to: size, extension, modified, hash — or null if absent.

changed_fields

Fields compared for files present in both snapshots:

size, extension, modified, hash.

changed_fields lists the fields whose values differ.

---

# 8. RESULT STRUCTURE

File:

reports/latest_comparison.json

Example (SNAP-002 → SNAP-003, shortened):

```json
{
  "format": "requiem-comparison",
  "format_version": "0.1",
  "id": "CMP-002-003",
  "generated": "2026-09-24T12:00:00",
  "status": "COMPLETED",

  "from": {
    "id": "SNAP-002",
    "created": "2026-09-24T11:15:00",
    "source": "database/snapshots/SNAP-002.json",
    "source_sha256": "…"
  },
  "to": {
    "id": "SNAP-003",
    "created": "2026-09-24T11:17:54",
    "source": "database/project_snapshot.json",
    "source_sha256": "…"
  },

  "project": {
    "name": "REQUIEM",
    "target": "requiem-tauri"
  },

  "environment": {
    "same_machine_path": true,
    "same_platform": true
  },

  "summary": {
    "added": 0,
    "removed": 0,
    "modified": 1,
    "unchanged": 61,
    "unverified": 0,
    "files_from": 62,
    "files_to": 62,
    "directories_from": 32,
    "directories_to": 32
  },

  "changes": {
    "added": [],
    "removed": [],
    "modified": [
      {
        "path": "src/App.jsx",
        "changed_fields": ["size", "modified", "hash"],
        "from": { "size": 41427, "modified": "2026-09-22T13:38:57", "hash": "1407b41e…" },
        "to":   { "size": 41430, "modified": "2026-09-24T11:17:12", "hash": "f0bc0179…" }
      }
    ],
    "unchanged": [
      { "path": ".gitignore", "changed_fields": [] }
    ],
    "unverified": []
  },

  "warnings": []
}
```

Field notes:

- id: CMP-<from number>-<to number>, derived from the pair;
- generated: local time of the run, without time zone;
- status: COMPLETED or COMPLETED_WITH_WARNINGS;
- source: snapshot file path relative to the Memory Core root;
- source_sha256: SHA-256 of the snapshot file itself;
- every list in "changes" is sorted by path;
- the unchanged list is complete (every unchanged file is listed).

---

# 9. REPORT

File:

reports/latest_comparison.md

Sections:

- comparison id, generated time, status, project;
- snapshots (from / to: id, created, source);
- summary (count per class, files and directories from → to);
- added, removed (full metadata);
- modified (changed fields, before → after);
- unverified (presence, reason, both sides);
- unchanged (count only; the full list is in latest_comparison.json);
- warnings.

---

# 10. VALIDATION AND ABORT RULES

The comparison is aborted and nothing is written if:

- comparison_config.json is not found or is invalid;
- only one of --from / --to is given;
- a snapshot id has an invalid format;
- a snapshot is not found;
- the history contains no snapshot older than the current one (default pair);
- a snapshot file cannot be read or is not valid JSON;
- the current snapshot is the v0.1 placeholder template;
- a required field is missing or invalid (id, created, project, environment, statistics, files, file fields);
- a history file contains an id different from its file name;
- a path is listed more than once in one snapshot;
- statistics.total_files differs from the number of listed files;
- a hash is neither null nor 64 lowercase hexadecimal characters;
- the snapshots belong to different projects (project.name or project.target differ);
- "from" is newer than "to";
- a file has equal hash but different size (corrupted snapshot);
- the self-check fails.

Self-check (before writing):

```
files_from = removed + modified + unchanged + unverified (present in from)
files_to   = added   + modified + unchanged + unverified (present in to)
```

On abort:

- the message starts with "Memory Core comparison aborted:";
- exit code is 1;
- existing reports are left untouched.

---

# 11. WARNINGS

The comparison completes with status COMPLETED_WITH_WARNINGS if:

- environment.machine_path differs between the snapshots;
- environment.platform differs between the snapshots;
- "from" was created later than "to".

---

# 12. STORAGE RULE

Only the latest comparison result is stored (DEC-008):

```
reports/latest_comparison.json
reports/latest_comparison.md
```

Each run replaces both files.

database/comparisons/ is not created.

A comparison result can always be rebuilt from the stored snapshots.

Write procedure:

1. both files are fully written to .tmp files;
2. each .tmp file replaces its target file.

A final report file is never partially written.

---

# 13. LIMITATIONS OF v0.1

- A renamed or moved file appears as removed + added. (Analysis Layer v0.1 reports such pairs as candidates: S-RENAME-CANDIDATE, S-CASE-CANDIDATE.)
- A change of letter case in a path appears as removed + added.
- Directories are compared only by count (snapshots do not list directory paths).
- A change of the scanner ignore list cannot be detected (snapshots do not store it).
- The two report files are replaced one after another: if a failure happens between the two replacements, the JSON file is new and the .md file is old. Each file is complete.
- The comparator must be started from inside comparison/.

---

# 14. NOT PART OF v0.1

- rename detection;
- change evaluation;
- impact analysis;
- comparison history;
- automatic documentation updates;
- AI analysis;
- application integration.

END OF COMPARISON MODEL
