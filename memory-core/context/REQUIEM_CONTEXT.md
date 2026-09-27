# REQUIEM CONTEXT

Version: 0.6

Document Type:
AI Context Package

Purpose:
Provide a compact and reliable understanding package of the REQUIEM ecosystem for AI sessions and development continuity.

---

# 1. PROJECT IDENTITY

Project:

REQUIEM


Type:

Premium desktop tactical environment and AI-assisted modding platform.


Core Principle:

> Games are environments. REQUIEM is the intelligence and orchestration layer above them.


Important Rule:

REQUIEM is not a S.T.A.L.K.E.R. 2-only application.

S.T.A.L.K.E.R. 2 is the first supported environment.

The architecture must support future environments without rewriting the foundation.

---

# 2. REQUIEM APPLICATION

Current application:

requiem-tauri


Technology foundation:

- Tauri
- React
- Vite
- Tailwind CSS
- PostCSS


Current application state:

Phase 1 — Architecture Preparation


Current implementation:

The application contains:

- Application Shell structure;
- Core layer structure;
- Contracts layer;
- Initial environment/intelligence/operations boundaries.


Current implementation status:

Architecture skeleton.

Most systems are placeholders.

---

# 3. MEMORY CORE IDENTITY

REQUIEM Memory Core is a development continuity system.

It exists to preserve:

- project understanding;
- architectural decisions;
- current state;
- development history;
- recovery capability.


Memory Core is not:

- a user-facing application feature;
- a replacement for REQUIEM;
- a documentation archive only.

It is a structured memory layer for project development.

---

# 4. MEMORY CORE CURRENT STRUCTURE

```
requiem-memory-core/
├── config        — memory.config.json
├── context       — REQUIEM_CONTEXT.md, REQUIEM_SNAPSHOT_MODEL.md, REQUIEM_COMPARISON_MODEL.md,
│                   REQUIEM_CHANGE_RECORD_MODEL.md, REQUIEM_CONTEXT_UPDATE_MODEL.md,
│                   REQUIEM_ANALYSIS_MODEL.md
├── protocols     — REQUIEM_DEVELOPMENT_PROTOCOL.md
├── database      — memory objects, project_snapshot.json, snapshots/
├── scanner       — scanner.py (v0.2), scanner_config.json, backup_v0.1_old_scanner/
├── comparison    — comparator.py (v0.1), comparison_config.json
├── change_report — change_reporter.py (v0.1), change_report_config.json
├── context_update — context_updater.py (v0.1), context_update_config.json
├── analysis      — analyzer.py (v0.1), analysis_config.json, analysis_rules.json,
│                   architecture_map.json (DRAFT)
├── reports       — latest_scan.md, latest_comparison.json, latest_comparison.md,
│                   latest_analysis.json, latest_analysis.md
├── review        — changes/, context_updates/, backups/
└── checkpoints   — empty
```

---

# 5. MEMORY DATABASE

Current memory objects:

## identity.json

Stores:

- project identity;
- fundamental principles;
- protected information.


## state.json

Stores:

- current phase;
- current focus;
- completed work;
- next actions.


## decisions.json

Stores:

- architectural decisions;
- reasons;
- consequences;
- importance.


## events.json

Stores:

- important project events;
- historical milestones;
- project change events added by the Context Update Layer (only by --apply of an APPROVED proposal, DEC-010).


## checkpoints.json

Stores:

- recovery points;
- stable project states.


## project_snapshot.json

Stores:

- the current project snapshot.

Format is defined in:

context/REQUIEM_SNAPSHOT_MODEL.md


## snapshots/

Stores:

- preserved previous snapshots, one file per snapshot (SNAP-NNN.json).


## Not stored in database

Comparison results are not stored in database/.

Only the latest comparison result is kept in reports/ (DEC-008).

Format is defined in:

context/REQUIEM_COMPARISON_MODEL.md

Change records (CHG) and context update proposals (CU) are not stored in database/.

They are kept in review/, outside project memory (DEC-009).

Formats are defined in:

context/REQUIEM_CHANGE_RECORD_MODEL.md

context/REQUIEM_CONTEXT_UPDATE_MODEL.md

Analysis results are not stored in database/.

Only the latest analysis result is kept in reports/ (latest_analysis.json, latest_analysis.md). No history of analysis results is created (DEC-016).

Format is defined in:

context/REQUIEM_ANALYSIS_MODEL.md

---

# 6. CURRENT MEMORY CORE STATUS

Version:

0.6


Completed:

- Memory Core concept;
- memory structure;
- documentation foundation;
- context package;
- initial scanner (v0.1);
- first project scan;
- State Snapshot System v0.1 (scanner v0.2);
- Comparison Layer v0.1 (comparator v0.1);
- Change Report Layer v0.1 (change_reporter v0.1);
- Context Update Layer v0.1 (context_updater v0.1);
- Analysis Layer v0.1 (analyzer v0.1).


Current snapshot state:

<!-- MEMORY:SNAPSHOT_STATE:BEGIN -->
- current snapshot: SNAP-003 (database/project_snapshot.json);
- preserved history: SNAP-001, SNAP-002 (database/snapshots/);
- project files tracked: 62;
- project directories tracked: 32.
<!-- MEMORY:SNAPSHOT_STATE:END -->

The block between the markers is updated by the Context Update Layer.


Scanner currently provides:

- file discovery;
- file metadata collection;
- SHA-256 file hashing;
- snapshot creation;
- historical snapshot preservation;
- atomic snapshot writing;
- scan reports.


Comparison Layer currently provides:

- comparison of two stored snapshots (default: current and previous; or an explicit pair);
- file classification: added, removed, modified, unchanged, unverified;
- unverified class for files with null hash (DEC-007);
- snapshot validation and project compatibility check;
- latest comparison result in reports/ (latest_comparison.json, latest_comparison.md).

Comparison Layer is an isolated read-only layer (DEC-006).

Scanner and Comparison Layer do not call each other.


Change Report Layer currently provides:

- change records CHG-NNN from the latest comparison result (review/changes/);
- verification of the comparison result and of both snapshot hashes;
- chain rule: CHG.from equals the previous CHG.to (DEC-012);
- records also when there are no changes (DEC-013);
- grouping of changed files by top-level folder;
- human review: APPROVED / REJECTED with an optional note.


Context Update Layer currently provides:

- proposals CU-NNN from APPROVED change records (review/context_updates/);
- two operations only: snapshot_state (marked blocks in README.md and REQUIEM_CONTEXT.md) and event (database/events.json) (DEC-011);
- human review: APPROVED / REJECTED, operations can be excluded;
- manual --apply of an APPROVED proposal with hash verification, backup (review/backups/) and restore on failure (DEC-010).

Analysis Layer currently provides:

- analysis of one change record (default: the latest; or --record CHG-NNN), of any review status;
- verification of the change record, of both snapshot hashes and of the agreement of entries with the snapshots;
- one category (type of file) and one zone (part of the architecture) for every changed file; "uncategorized" / "unmapped" when no rule matches (DEC-018);
- findings of fixed signal kinds; every finding names its rule, its entries and its evidence;
- coverage of the "to" snapshot by the architecture map;
- latest result only, in reports/ (DEC-016).

Analysis Layer is an isolated, read-only, advisory layer (DEC-015).

It is positioned after Change Report and before Human review of the change record (DEC-014).

The architecture map is written and approved by a human (DEC-017). It is currently a DRAFT template without zones.

Change Report and Context Update do not perform analysis.

Project memory is changed only after human approval.


Memory Core does not yet provide:

- approved architecture map;
- impact analysis.

---

# 7. ARCHITECTURAL RULES

Memory Core must:

- observe before making conclusions;
- preserve history;
- protect critical information;
- avoid silent modifications;
- assist human decisions.


Memory Core must not:

- replace human decisions;
- automatically rewrite architecture;
- modify critical memory without approval;
- become part of the application prematurely.

---

# 8. AI COLLABORATION MODEL

AI roles:

## GPT

Role:

Architecture and planning.

Responsibilities:

- define systems;
- validate direction;
- protect principles.


## Claude

Role:

Implementation.

Responsibilities:

- write code;
- execute approved tasks;
- perform technical changes.


## Gemini

Role:

Analysis and support intelligence.

Responsibilities:

- research;
- document analysis;
- additional review.

---

# 9. CURRENT ACTIVE TASK

Current direction:

Architecture map preparation and approval.


Status:

Direction only.

analysis/architecture_map.json is a DRAFT template without zones. Until an approved map exists, every file is "unmapped".

The map is written and approved by a human (DEC-017).


Pipeline:

```
Project
↓
Scanner          — done (v0.2)
↓
Snapshot         — done (v0.1)
↓
Comparison       — done (v0.1)
↓
Change Report    — done (v0.1)
↓
Analysis         — done (v0.1)
↓
Human review     — CHG approved / rejected
↓
Context Update   — done (v0.1)
↓
CU proposal
↓
Human review
↓
CU approved / rejected
↓
Manual apply
```

---

# 10. CURRENT DEVELOPMENT RESTRICTIONS

Do not:

- add AI API integration;
- create UI;
- integrate Memory Core into Tauri;
- redesign existing architecture;
- create autonomous decision making.


Priority order:

1. Reliability.
2. Understanding.
3. Automation.
4. Intelligence.

---

# 11. KNOWN ISSUES

Current known issues:

1. RESOLVED (Comparison Layer v0.1): Scanner does not compare snapshots. Changes between snapshots are visible only by checking the recorded hashes manually.

2. RESOLVED (State Snapshot System v0.1): No historical project snapshots exist.

3. RESOLVED (documentation synchronization for Memory Core v0.4): State files may require synchronization.
   state.json "active_task" and "next_actions" described the foundation stage. They now describe the position after Comparison Layer v0.1.

4. Checkpoint storage model requires clarification.
   Settled: snapshots and checkpoints are separate concepts (DEC-005).
   Open: checkpoint records are stored in database/checkpoints.json, while the checkpoints/ directory exists and is empty; its purpose is not defined.
   Note: review/backups/ contains restore copies of context update proposals. They are not checkpoints.

5. PARTLY RESOLVED (Analysis Layer v0.1): Meaningful change classification.
   Defined (Comparison Layer v0.1): file-level classes — added, removed, modified, unchanged, unverified.
   Defined (Analysis Layer v0.1): category, zone and rule-based findings, from metadata only.
   Open: meaning of a change inside file content; impact analysis.

6. Record numbering has gaps: DEC-004 is absent from decisions.json, EVENT-003 is absent from events.json. Their content is unknown. The existing records were not renumbered.

7. config/memory.config.json is not read by any code yet. It still states version "0.1". The base directory of its relative path "project.root" is not defined.

8. The "scan" section of scanner/scanner_config.json is not read by the scanner yet.

9. Comparison Layer v0.1 has known limitations: renames and letter-case changes in paths appear as removed + added; directories are compared only by count; a change of the scanner ignore list cannot be detected; the two report files are replaced one after another.
   Full list: context/REQUIEM_COMPARISON_MODEL.md, section 13.
   Note: Analysis Layer v0.1 reports removed + added files with identical content, or with paths that differ only in letter case, as candidates (S-RENAME-CANDIDATE, S-CASE-CANDIDATE). The Comparison Layer is not changed.

10. database/events.json contains two kinds of events: Memory Core milestones (added during documentation synchronization) and project change events (added by the Context Update Layer). They share one numbering (EVENT-006 is a project change event).

11. Change Report Layer v0.1 and Context Update Layer v0.1 have known limitations: records are reviewed as a whole; several target files cannot be written as one atomic step (protection: hash verification, backup, restore); a scan or a manual edit of a target between preparation and apply makes a proposal STALE; there is no restore command; review/ grows without limit.
   Full lists: context/REQUIEM_CHANGE_RECORD_MODEL.md, section 12; context/REQUIEM_CONTEXT_UPDATE_MODEL.md, section 14.

12. Analysis Layer v0.1 has known limitations: it works on metadata only (path, size, time, hash); one change record per run; only the latest result is kept; analysis is not enforced before review; the report is outdated after a new change record or a change of the rules or the map.
   Full list: context/REQUIEM_ANALYSIS_MODEL.md, section 16.

13. analysis/architecture_map.json is a DRAFT template without zones. Every file is "unmapped" and every analysis has the warnings "Architecture map is DRAFT (not approved)." and "Architecture map has no zones." until an approved map exists.

---

# 12. NEXT DEVELOPMENT STEP

Direction:

Architecture map preparation and approval.


Not started:

The map content requires human approval (DEC-017).


Already known:

"What exists now" — State Snapshot System v0.1.

"What changed between states" — Comparison Layer v0.1.

"Which changes are accepted" — Change Report Layer v0.1 (human review).

"How accepted changes reach project context" — Context Update Layer v0.1 (human approval and manual apply).

"What a change means (by rules)" — Analysis Layer v0.1 (advisory, before human review).

---

# FINAL PRINCIPLE

The purpose of REQUIEM Memory Core:

> Ensure that REQUIEM never depends on a lost conversation to remain understandable.

END OF CONTEXT
