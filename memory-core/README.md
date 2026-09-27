# REQUIEM MEMORY CORE

Version: 0.5

Document Type:
Project Overview

Purpose:
Provide a development continuity system for the REQUIEM ecosystem.

---

# 1. IDENTITY

REQUIEM Memory Core is an intelligent project memory and continuity system.

Its purpose is preserving:

- project understanding;
- architectural decisions;
- current state;
- development history;
- recovery capability.

Memory Core is not a simple documentation folder.

It is a structured memory layer for REQUIEM development.

---

# 2. CURRENT PROJECT POSITION

Main project:

REQUIEM

Application:

requiem-tauri

Technology:

- Tauri
- React
- Vite
- Tailwind CSS

Current Memory Core version:

0.6

Current Memory Core stage:

Analysis Layer v0.1 completed (checkpoint CP-006).

Component versions:

- Scanner: v0.2
- State Snapshot System: v0.1
- Comparison Layer: v0.1
- Change Report Layer: v0.1
- Context Update Layer: v0.1
- Analysis Layer: v0.1

Note:

The "Version" line at the top of each document is the version of that document, not the version of Memory Core.

---

# 3. MEMORY CORE STRUCTURE

Current structure:

```
requiem-memory-core/
├── README.md
├── CHANGELOG.md
├── config/
│   └── memory.config.json
├── context/
│   ├── REQUIEM_CONTEXT.md
│   ├── REQUIEM_SNAPSHOT_MODEL.md
│   ├── REQUIEM_COMPARISON_MODEL.md
│   ├── REQUIEM_CHANGE_RECORD_MODEL.md
│   ├── REQUIEM_CONTEXT_UPDATE_MODEL.md
│   └── REQUIEM_ANALYSIS_MODEL.md
├── protocols/
│   └── REQUIEM_DEVELOPMENT_PROTOCOL.md
├── database/
│   ├── identity.json
│   ├── state.json
│   ├── decisions.json
│   ├── events.json
│   ├── checkpoints.json
│   ├── project_snapshot.json
│   └── snapshots/
├── scanner/
│   ├── scanner.py
│   ├── scanner_config.json
│   └── backup_v0.1_old_scanner/
├── comparison/
│   ├── comparator.py
│   └── comparison_config.json
├── change_report/
│   ├── change_reporter.py
│   └── change_report_config.json
├── context_update/
│   ├── context_updater.py
│   └── context_update_config.json
├── analysis/
│   ├── analyzer.py
│   ├── analysis_config.json
│   ├── analysis_rules.json
│   └── architecture_map.json
├── reports/
│   ├── latest_scan.md
│   ├── latest_comparison.json
│   ├── latest_comparison.md
│   ├── latest_analysis.json
│   └── latest_analysis.md
├── review/
│   ├── changes/
│   ├── context_updates/
│   └── backups/
└── checkpoints/
```

reports/latest_comparison.json and reports/latest_comparison.md are created by the first comparator run.

reports/latest_analysis.json and reports/latest_analysis.md are created by the first analyzer run.

review/ and its subdirectories are created by the first run of the change reporter and the context updater.

---

# 4. EXISTING COMPONENTS

## config

Current file:

- memory.config.json

Purpose:

Global Memory Core settings.

Current status:

This file is not read by any code yet.


## database

Contains project memory.

Current files:

- identity.json
- state.json
- decisions.json
- events.json
- checkpoints.json
- project_snapshot.json — current project snapshot;
- snapshots/ — preserved previous snapshots (SNAP-NNN.json).

events.json contains Memory Core milestones and project change events.

Project change events are added only by --apply of an APPROVED context update (DEC-010).

Current snapshot state:

<!-- MEMORY:SNAPSHOT_STATE:BEGIN -->
- current snapshot: SNAP-003;
- preserved history: SNAP-001, SNAP-002.
<!-- MEMORY:SNAPSHOT_STATE:END -->

The block between the markers is updated by the Context Update Layer.


## context

Contains AI context packages and model definitions.

Current files:

- REQUIEM_CONTEXT.md
- REQUIEM_SNAPSHOT_MODEL.md
- REQUIEM_COMPARISON_MODEL.md
- REQUIEM_CHANGE_RECORD_MODEL.md
- REQUIEM_CONTEXT_UPDATE_MODEL.md
- REQUIEM_ANALYSIS_MODEL.md


## protocols

Contains AI development rules.

Current file:

- REQUIEM_DEVELOPMENT_PROTOCOL.md


## scanner

Observation and snapshot storage layer.

Current files:

- scanner.py (v0.2)
- scanner_config.json
- backup_v0.1_old_scanner/ — backup copy of scanner v0.1 and its config.

Purpose:

Detect current project state and preserve it as a snapshot.


## comparison

Comparison layer.

Isolated read-only layer (DEC-006).

Current files:

- comparator.py (v0.1)
- comparison_config.json

Purpose:

Compare two stored snapshots and answer:

"What changed between these states?"

Capabilities:

- compares the current snapshot with the previous one, or any explicit pair;
- classifies every file as added, removed, modified, unchanged or unverified;
- files with null hash are classified as unverified (DEC-007);
- validates both snapshots and stops without writing anything if a snapshot is invalid, missing or belongs to another project;
- writes the latest result atomically to reports/ (DEC-008).

It does not:

- write to database/;
- run the scanner;
- read or modify project files;
- modify documentation;
- evaluate changes.

Format and rules are defined in:

context/REQUIEM_COMPARISON_MODEL.md


## change_report

Change Report Layer.

Current files:

- change_reporter.py (v0.1)
- change_report_config.json

Purpose:

Turn the latest comparison result into a change record (CHG-NNN) and let a human approve or reject it.

Capabilities:

- verifies the comparison result and the SHA-256 of both snapshots;
- keeps records in a chain: CHG.from equals the previous CHG.to (DEC-012);
- creates a record also when there are no changes (DEC-013);
- groups changed files by top-level folder;
- review: --approve / --reject with an optional note; a reviewed record cannot be changed.

It writes only to review/changes/ (DEC-009).

It does not modify project memory.

Format and rules are defined in:

context/REQUIEM_CHANGE_RECORD_MODEL.md


## context_update

Context Update Layer.

Current files:

- context_updater.py (v0.1)
- context_update_config.json

Purpose:

Prepare controlled updates of project context from APPROVED change records and apply them only after human approval.

Operations (DEC-011):

- snapshot_state — the marked "Current snapshot state" block in README.md and context/REQUIEM_CONTEXT.md;
- event — a new record in database/events.json (only for a change record with a review note).

Never changed:

identity.json, decisions.json, checkpoints.json, state.json.

Project memory is changed only by a manual --apply of an APPROVED proposal, after hash verification and backup (DEC-010).

It writes proposals to review/context_updates/ and backups to review/backups/.

Format and rules are defined in:

context/REQUIEM_CONTEXT_UPDATE_MODEL.md


## analysis

Analysis Layer.

Isolated, read-only, advisory layer (DEC-015).

Current files:

- analyzer.py (v0.1)
- analysis_config.json
- analysis_rules.json — categories and signals (generic, no project paths)
- architecture_map.json — zones of the project; DRAFT template without zones

Purpose:

Analyze one change record with deterministic rules and answer:

"What does this change mean?"

Position (DEC-014):

after Change Report, before Human review of the change record.

Capabilities:

- analyzes the latest change record, or any record with --record;
- verifies the change record, the SHA-256 of both snapshots and the agreement of entries with the snapshots;
- gives every changed file one category (type of file) and one zone (part of the architecture);
- a file that no rule matches gets "uncategorized" or "unmapped" and is never forced into a class (DEC-018);
- reports findings of fixed signal kinds; every finding names its rule, its entries and its evidence;
- shows how the architecture map covers the "to" snapshot;
- writes only reports/latest_analysis.json and reports/latest_analysis.md (DEC-016).

It does not:

- read project files;
- write to database/, context/ or review/;
- modify change records, proposals, rules or the map;
- approve or reject changes;
- evaluate changes or give recommendations;
- use AI.

The architecture map is project truth. It is written and approved by a human (DEC-017).

Format and rules are defined in:

context/REQUIEM_ANALYSIS_MODEL.md


## review

Human review area.

Outside project memory (DEC-009).

Contents:

- changes/ — change records CHG-NNN (.json, .md);
- context_updates/ — context update proposals CU-NNN (.json, .md);
- backups/ — copies of target files made before each apply (CU-NNN/).

Backups are restore copies of one proposal. They are not checkpoints (DEC-005).

Files in review/ are not deleted.


## reports

Contains the latest scan report, the latest comparison result and the latest analysis result.

Current files:

- latest_scan.md — created by the scanner;
- latest_comparison.json — created by the comparator;
- latest_comparison.md — created by the comparator;
- latest_analysis.json — created by the analyzer;
- latest_analysis.md — created by the analyzer.

Each run replaces the previous file.


## checkpoints

Directory exists and is currently empty.

Checkpoint records are currently stored in:

database/checkpoints.json

Snapshots and checkpoints are separate concepts (DEC-005).

---

# 5. IMPORTANT ARCHITECTURAL RULES

Memory Core:

- observes before making conclusions;
- does not silently modify project history;
- does not replace human decisions;
- preserves historical context.

---

# 6. CURRENT SCANNER STATE

Scanner v0.2:

Capabilities:

- scans project files;
- collects file metadata (path, size, extension, modification time);
- computes SHA-256 hash of every file;
- creates project snapshot (database/project_snapshot.json);
- preserves the previous snapshot in database/snapshots/ before writing a new one;
- writes the snapshot atomically;
- stops without writing anything if the existing snapshot file is invalid or unknown;
- creates scan report (reports/latest_scan.md).

Note:

Scanner does not compare snapshots.

Comparison is performed by the separate Comparison Layer (comparison/).

Scanner and Comparison Layer do not call each other.

---

# 7. RUNNING THE SCANNER

The scanner uses paths relative to the scanner directory.

It must be started from inside:

scanner/

Command:

```
python scanner.py
```

Scanner settings are read only from:

scanner/scanner_config.json

The "scan" section of scanner_config.json (track_files, track_directories, track_dependencies) is not read by the scanner yet.

---

# 8. RUNNING THE COMPARATOR

The comparator uses paths relative to the comparison directory.

It must be started from inside:

comparison/

Commands:

```
python comparator.py
python comparator.py --from SNAP-001 --to SNAP-003
```

Without arguments:

The current snapshot is compared with the nearest older snapshot in database/snapshots/.

With arguments:

--from and --to must be given together.

Result:

- reports/latest_comparison.json
- reports/latest_comparison.md

Comparator settings are read only from:

comparison/comparison_config.json

---

# 9. RUNNING THE CHANGE REPORTER

It must be started from inside:

change_report/

Commands:

```
python change_reporter.py
python change_reporter.py --approve CHG-001 --note "text"
python change_reporter.py --reject CHG-001 --note "text"
```

Without arguments:

A change record is created from reports/latest_comparison.json.

Settings are read only from:

change_report/change_report_config.json

---

# 10. RUNNING THE ANALYZER

It must be started from inside:

analysis/

Commands:

```
python analyzer.py
python analyzer.py --record CHG-001
```

Without arguments:

The change record with the highest number in review/changes/ is analyzed.

Result:

- reports/latest_analysis.json
- reports/latest_analysis.md

Settings are read only from:

analysis/analysis_config.json

Rules and map:

- analysis/analysis_rules.json
- analysis/architecture_map.json

---

# 11. RUNNING THE CONTEXT UPDATER

It must be started from inside:

context_update/

Commands:

```
python context_updater.py
python context_updater.py --approve CU-001
python context_updater.py --approve CU-001 --exclude OP-2
python context_updater.py --reject CU-001 --note "text"
python context_updater.py --apply CU-001
```

Without arguments:

A proposal is prepared from APPROVED change records.

Settings are read only from:

context_update/context_update_config.json

Full cycle:

```
scanner/          python scanner.py
comparison/       python comparator.py
change_report/    python change_reporter.py
analysis/         python analyzer.py
                  read reports/latest_analysis.md
change_report/    python change_reporter.py --approve CHG-NNN --note "text"
context_update/   python context_updater.py
context_update/   python context_updater.py --approve CU-NNN
context_update/   python context_updater.py --apply CU-NNN
```

Each approval is a human decision.

---

# 12. CURRENT TASK

Completed stage:

Analysis Layer v0.1.

Current direction:

Architecture map preparation and approval.

Status:

Direction only.

analysis/architecture_map.json is a DRAFT template without zones. Until an approved map exists, every file is "unmapped".

The map is written and approved by a human (DEC-017).

---

# 13. RESTRICTIONS

Do not:

- add AI integration;
- create UI;
- integrate with Tauri;
- redesign Memory Core architecture;
- change existing memory model.

---

# 14. DEVELOPMENT PRINCIPLE

Memory Core is built gradually.

The priority order:

1. Reliability.
2. Understanding.
3. Automation.
4. Intelligence.

---

END OF DOCUMENT
