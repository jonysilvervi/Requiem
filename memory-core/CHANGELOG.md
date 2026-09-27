# REQUIEM MEMORY CORE CHANGELOG

Version: 0.5

Document Type:
Change History

Purpose:
Record completed Memory Core development milestones.

---

# 2026-09-24 — Documentation synchronized with Memory Core v0.6

Added documents:

- context/REQUIEM_ANALYSIS_MODEL.md — Analysis Layer v0.1 definition: position, input, checks, classification, signals and findings, rules file, architecture map format and requirements, result structure, report, warnings, abort rules, storage rule, limitations.

Updated documents:

- README.md — Memory Core version 0.6, checkpoint CP-006, analysis/ component, reports/latest_analysis.*, running the analyzer (new section 10; following sections renumbered), analyzer step in the full cycle, current direction;
- context/REQUIEM_CONTEXT.md — structure, analysis results not stored in database/, status after Analysis Layer v0.1, pipeline with Analysis before human review, current direction, known issue 5 partly resolved, known issue 9 note, known issues 12 and 13 added, next development step;
- protocols/REQUIEM_DEVELOPMENT_PROTOCOL.md — implemented layers and their order (section 5), current task rule;
- context/REQUIEM_COMPARISON_MODEL.md — position in Memory Core (Change Report and Analysis instead of "not implemented"), note on rename and case candidates in section 13;
- context/REQUIEM_CHANGE_RECORD_MODEL.md — position in Memory Core (Analysis before human review), Analysis reads change records read-only;
- context/REQUIEM_SNAPSHOT_MODEL.md — references to REQUIEM_ANALYSIS_MODEL.md.

Document versions:

- each updated document: version + 0.1;
- REQUIEM_ANALYSIS_MODEL.md: 0.1 -> 0.2 (status changed to implemented; DEC references added).

Updated memory records:

- database/state.json — current focus, completed work, active task and next actions (architecture map preparation and approval);
- database/decisions.json — DEC-014, DEC-015, DEC-016, DEC-017, DEC-018 added;
- database/events.json — EVENT-009 added;
- database/checkpoints.json — CP-006 added.

Not changed:

- code (scanner/, comparison/, change_report/, context_update/, analysis/);
- analysis/analysis_rules.json, analysis/architecture_map.json (DRAFT template without zones);
- snapshots (database/project_snapshot.json, database/snapshots/);
- database/identity.json;
- config/;
- review/;
- reports/;
- context/REQUIEM_CONTEXT_UPDATE_MODEL.md;
- text between the MEMORY:SNAPSHOT_STATE markers.

Existing records were not renumbered.

Result:

Documentation matches the checkpoint Memory Core v0.6 (CP-006).

---

# 2026-09-24 — Analysis Layer v0.1 Completed

Implemented:

- analysis of one change record (default: the latest; or --record CHG-NNN), of any review status;
- verification of the change record, of both snapshot hashes and of the agreement of entries with the snapshots;
- classification of every changed file: category (rules file) and zone (architecture map); "uncategorized" / "unmapped" when no rule matches;
- 12 fixed signal kinds: unverified, attention_zone, generated_zone, paired_files, rename_candidate, case_candidate, new_top_level, empty_file, size_delta, category_changed, unmapped, uncategorized;
- findings with rule, entries and evidence; summary by class, zone and category; size delta; coverage of the "to" snapshot;
- facts_sha256: binding to the facts of the change record that does not change on review;
- warnings: DRAFT map, map without zones, older record, rejected record, skipped paired rule, change record warnings;
- self-check before writing; atomic writing of reports/latest_analysis.json and reports/latest_analysis.md.

Architecture:

- DEC-014, DEC-015, DEC-016, DEC-017, DEC-018.

Components:

- analysis/analyzer.py v0.1;
- analysis/analysis_config.json;
- analysis/analysis_rules.json — default rule set v0.1 (11 categories, 13 signals);
- analysis/architecture_map.json — DRAFT template without zones.

Verification:

Windows (real project):

- ANL-001 created from CHG-001 (SNAP-001 -> SNAP-003);
- status COMPLETED_WITH_WARNINGS (expected warnings for the DRAFT architecture map);
- findings: attention 0 | notice 1 | info 0;
- reports/latest_analysis.json and reports/latest_analysis.md created;
- no database, review or context files changed.

Test run on a copy of the project (Linux, Python 3.11) — 78 checks passed:

- real data: CHG-001 analyzed; record_sha256 equals the value stored in CU-001; all 62 files of SNAP-003 categorized; determinism (equal content except "generated");
- synthetic history created by the real scanner, comparator and change reporter (SNAP-004 to SNAP-007, CHG-002 to CHG-005): all 12 signal kinds; longest prefix and exact path rules; paired rule skipped for an unverified file; analysis with the project folder absent;
- facts_sha256 unchanged after review; latest record by default; record without changes; older and rejected records; disabled signal; rules file with UTF-8 BOM and CRLF;
- aborts without writing (33 cases): configuration, arguments, rules file, architecture map, change record, snapshots;
- isolation: only reports/latest_analysis.json and reports/latest_analysis.md created; no .tmp files left.

Result:

A change record can be analyzed by deterministic rules before human review, without changing project memory.

Memory Core version after this milestone: 0.6 (checkpoint CP-006).

---

# 2026-09-24 — Documentation synchronized with Memory Core v0.5

Added documents:

- context/REQUIEM_CHANGE_RECORD_MODEL.md — Change Report Layer v0.1 definition: checks, chain rules, record structure, entries, review, report, abort rules, storage rule, limitations;
- context/REQUIEM_CONTEXT_UPDATE_MODEL.md — Context Update Layer v0.1 definition: operations and targets, preparation, markers, proposal structure, review, apply, report, abort rules, storage rule, limitations.

Updated documents:

- README.md — Memory Core version 0.5, checkpoint CP-005, change_report/, context_update/ and review/ components, running the change reporter and the context updater, full cycle, current direction, snapshot state markers;
- context/REQUIEM_CONTEXT.md — structure, database notes, status after Change Report and Context Update v0.1, pipeline with human review steps, current direction, known issue 4 note, known issues 10 and 11 added, snapshot state markers;
- protocols/REQUIEM_DEVELOPMENT_PROTOCOL.md — implemented layers note (section 5), current task rule.

Markers:

- <!-- MEMORY:SNAPSHOT_STATE:BEGIN --> / <!-- MEMORY:SNAPSHOT_STATE:END --> inserted around the "Current snapshot state" block in README.md and context/REQUIEM_CONTEXT.md. The text of the blocks was not changed.

Updated memory records:

- database/state.json — current focus, completed work, active task and next actions (Analysis Layer preparation);
- database/decisions.json — DEC-009, DEC-010, DEC-011, DEC-012, DEC-013 added;
- database/events.json — EVENT-007, EVENT-008 added (EVENT-006 was added earlier by the Context Update Layer);
- database/checkpoints.json — CP-005 added.

Not changed:

- code (scanner/, comparison/, change_report/, context_update/);
- snapshots (database/project_snapshot.json, database/snapshots/);
- database/identity.json;
- config/;
- review/;
- context/REQUIEM_SNAPSHOT_MODEL.md, context/REQUIEM_COMPARISON_MODEL.md.

Existing records were not renumbered.

Result:

Documentation matches the checkpoint Memory Core v0.5 (CP-005).

---

# 2026-09-24 — Context Update Layer v0.1 Completed

Implemented:

- proposals CU-NNN from APPROVED change records (review/context_updates/);
- two operations: snapshot_state (marked blocks in README.md and context/REQUIEM_CONTEXT.md) and event (database/events.json);
- hard-coded targets; identity, decisions, checkpoints and state are never targets;
- review: --approve (with --exclude) / --reject;
- manual --apply of an APPROVED proposal: hash verification of change records, snapshot and targets; backup in review/backups/CU-NNN/; atomic writing; restore from backup on failure; STALE status when data changed since preparation.

Architecture:

- DEC-009, DEC-010, DEC-011.

Components:

- context_update/context_updater.py v0.1;
- context_update/context_update_config.json.

Verification:

Windows (real project):

- CU-001 created from CHG-001, approved and applied;
- EVENT-006 added to database/events.json;
- backup created: review/backups/CU-001/database/events.json;
- identity.json, state.json, decisions.json, checkpoints.json were not modified.

Test run on a copy of the project (Linux, Python 3.11) — 26 checks passed:

- event only on real data (snapshot_state already up to date); one open proposal at a time; apply refused before approval; apply changes only the target file, keeps its format, creates an exact backup; second apply refused;
- snapshot_state and events after a new snapshot; excluded event leaves no gap in numbering; only the marked block is changed;
- STALE on a target edit, a new scan or a change record edit; forbidden targets and operation kinds refused; PENDING and REJECTED change records not used; missing markers; restore from backup on a write failure; argument checks.

Result:

Approved changes can reach project context only through human approval and a manual apply.

---

# 2026-09-24 — Change Report Layer v0.1 Completed

Implemented:

- change records CHG-NNN from reports/latest_comparison.json (review/changes/);
- verification of the comparison result and of both snapshot hashes;
- chain rule: CHG.from equals the previous CHG.to; duplicate pairs refused;
- records also when there are no changes;
- grouping of changed files by top-level folder;
- review: --approve / --reject with an optional note; reviewed records cannot be changed.

Architecture:

- DEC-009, DEC-012, DEC-013.

Components:

- change_report/change_reporter.py v0.1;
- change_report/change_report_config.json.

Verification:

Windows (real project):

- CHG-001 created from CMP-001-003 (SNAP-001 -> SNAP-003: Added 0 | Removed 0 | Modified 1 | Unchanged 61 | Unverified 0);
- CHG-001 approved.

Test run on a copy of the project (Linux, Python 3.11) — 24 checks passed:

- record from real data; duplicate refused; approve, reject, approve without note; reviewed record immutable;
- chain continuation after a new scan; no_changes record; chain break with command hint; older comparison refused;
- unverified entries;
- aborts without writing: missing, invalid or unsupported comparison; outdated comparison; self-comparison; tampered summary; corrupted record; different project; invalid review commands.

Result:

Comparison facts are preserved as reviewed change history.

---

# 2026-09-24 — Documentation synchronized with Memory Core v0.4

Added documents:

- context/REQUIEM_COMPARISON_MODEL.md — Comparison Layer v0.1 definition: input pair, classification rules, result structure, report, abort rules, warnings, storage rule, limitations.

Updated documents:

- README.md — Memory Core version 0.4, checkpoint CP-004, comparison/ component, running the comparator, reports/ files, current direction;
- context/REQUIEM_CONTEXT.md — structure, status after Comparison Layer v0.1, pipeline, current direction, known issues 1 and 3 resolved, known issue 5 clarified, known issue 9 added;
- context/REQUIEM_SNAPSHOT_MODEL.md — reference to REQUIEM_COMPARISON_MODEL.md;
- protocols/REQUIEM_DEVELOPMENT_PROTOCOL.md — current task rule.

Updated memory records:

- database/state.json — current focus, completed work, active task and next actions after Comparison Layer v0.1;
- database/decisions.json — DEC-006, DEC-007, DEC-008 added;
- database/events.json — EVENT-005 added;
- database/checkpoints.json — CP-004 added.

Not changed:

- code (scanner/, comparison/);
- snapshots (database/project_snapshot.json, database/snapshots/);
- database/identity.json;
- config/.

Existing records were not renumbered (DEC-004 and EVENT-003 remain absent).

Result:

Documentation matches the checkpoint Memory Core v0.4 (CP-004).

---

# 2026-09-24 — Comparison Layer v0.1 Completed

Implemented:

- comparison of two stored snapshots (default: current and previous; or an explicit pair with --from / --to);
- file classification: added, removed, modified, unchanged, unverified;
- unverified class for files with null hash (DEC-007);
- snapshot validation and project compatibility check;
- self-check of classification totals;
- atomic writing of the latest result (reports/latest_comparison.json, reports/latest_comparison.md).

Architecture:

- isolated read-only layer (DEC-006);
- only the latest result is stored, in reports/ (DEC-008);
- scanner not changed.

Components:

- comparison/comparator.py v0.1;
- comparison/comparison_config.json.

Verification:

Windows (real project data):

- SNAP-002 -> SNAP-003: Added 0 | Removed 0 | Modified 1 | Unchanged 61 | Unverified 0;
- SNAP-001 -> SNAP-002: Added 0 | Removed 0 | Modified 0 | Unchanged 62 | Unverified 0;
- SNAP-001 -> SNAP-003: Added 0 | Removed 0 | Modified 1 | Unchanged 61 | Unverified 0.

Test run on a copy of the project (Linux, Python 3.11) — 13 checks passed:

- the three real snapshot pairs above, with the same results;
- added, removed, modified, unchanged, unverified (synthetic snapshots);
- aborts without writing: corrupted snapshot (invalid JSON; equal hash with different size), invalid hash, different projects, missing snapshot.

Result:

REQUIEM Memory Core can now detect what changed between stored project states.

Memory Core version after this milestone: 0.4 (checkpoint CP-004).

---

# 2026-09-24 — Documentation synchronized with Memory Core v0.3

Updated documents:

- README.md — Memory Core version 0.3, real directory structure, scanner v0.2 capabilities, how to run the scanner, current task (Comparison Layer);
- context/REQUIEM_CONTEXT.md — current status after State Snapshot System v0.1, current task, known issues;
- context/REQUIEM_SNAPSHOT_MODEL.md — snapshot history location, "environment" block, null hash rule, broken formatting fixed;
- protocols/REQUIEM_DEVELOPMENT_PROTOCOL.md — current task rule.

Not changed:

- code;
- config/ and database/ files.

Result:

Documentation matches the checkpoint Memory Core v0.3 (CP-003).

---

# 2026-09-24 — State Snapshot System v0.1 Completed

Implemented:

- project state snapshot generation;
- historical snapshot preservation;
- SHA-256 file verification;
- metadata collection;
- atomic snapshot writing;
- separation of project identity and machine environment.


Result:

REQUIEM Memory Core can now preserve verified historical project states.

Components:

- scanner.py v0.2 (scanner v0.1 kept in scanner/backup_v0.1_old_scanner/).

Verification:

- SNAP-001 created;
- SNAP-002 created, SNAP-001 preserved in database/snapshots/;
- SNAP-003 created, SNAP-002 preserved in database/snapshots/;
- the modification of src/App.jsx is recorded in SNAP-003 (new size, time and hash compared to SNAP-002). Comparison is not automatic yet.

Memory Core version after this milestone: 0.3 (checkpoint CP-003).

---

END OF DOCUMENT