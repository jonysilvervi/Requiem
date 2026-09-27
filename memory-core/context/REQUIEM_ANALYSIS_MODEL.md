# REQUIEM ANALYSIS MODEL

Version: 0.2

Document Type:
Analysis Definition

Purpose:
Define how REQUIEM Memory Core analyzes a change record with deterministic rules.

Status:
Implemented — Analysis Layer v0.1 (analysis/analyzer.py), checkpoint CP-006.

The architecture map (analysis/architecture_map.json) is a DRAFT template without zones. Its format and requirements are defined here (section 10). Its content is approved separately (DEC-017).

---

# 1. PURPOSE

Analysis answers:

"What does this change mean?"

In v0.1 this means:

- which part of the project architecture each changed file belongs to (zone);
- which type of file it is (category);
- which known rules match the recorded changes (findings).

Analysis helps a human review a change record (CHG).

Analysis does not decide.

---

# 2. CORE PRINCIPLE

Analysis produces rule matches derived from recorded facts.

Every finding:

- names the rule that produced it;
- lists the change record entries it is based on;
- contains the facts (evidence) that matched the rule.

Analysis does not store:

- evaluations (good / bad, safe / dangerous);
- recommendations;
- assumptions about file content;
- free text that was not written by a human in the rules file.

A file that no rule matches is never forced into a zone or a category.

It gets the reserved value "unmapped" (zone) or "uncategorized" (category).

This follows the principle of DEC-007 (DEC-018).

The same inputs always give the same result content.

Only the "generated" field differs between runs.

---

# 3. POSITION IN MEMORY CORE

```
Observation     scanner/scanner.py                 — creates snapshots
↓
Storage         database/project_snapshot.json
                database/snapshots/SNAP-NNN.json
↓
Comparison      comparison/comparator.py           — reports/latest_comparison.json
↓
Change Report   change_report/change_reporter.py   — review/changes/CHG-NNN (PENDING_REVIEW)
↓
Analysis        analysis/analyzer.py               — this model
↓
Human review    CHG approved / rejected
↓
Context Update  context_update/context_updater.py
↓
CU proposal     review/context_updates/CU-NNN (PROPOSED)
↓
Human review
↓
CU approved / rejected
↓
Manual apply    --apply CU-NNN
```

Analysis Layer is an isolated, read-only, advisory layer (DEC-015).

It:

- reads one change record, the two snapshots of that record, the rules file and the architecture map;
- writes only reports/latest_analysis.json and reports/latest_analysis.md;
- never writes to database/, context/, review/, README.md or CHANGELOG.md;
- never modifies change records, context update proposals, the rules file or the architecture map;
- does not read project files (requiem-tauri);
- does not read identity, state, decisions, events or checkpoints;
- does not run the scanner, the comparator, the change reporter or the context updater;
- is not run by any of them;
- is not an input of the Context Update Layer;
- does not use AI;
- is not integrated with Tauri.

The step "Analysis before Human review" is procedural in v0.1 (DEC-014).

The change reporter does not require an analysis before --approve or --reject.

---

# 4. RUNNING

The analyzer uses paths relative to the analysis directory.

It must be started from inside:

analysis/

Commands:

```
python analyzer.py
python analyzer.py --record CHG-005
```

Without arguments:

The change record with the highest number in review/changes/ is analyzed.

With --record:

The given change record is analyzed.

Settings are read only from:

analysis/analysis_config.json

Review cycle with analysis:

```
change_report/   python change_reporter.py
analysis/        python analyzer.py
                 read reports/latest_analysis.md
change_report/   python change_reporter.py --approve CHG-NNN --note "text"
```

---

# 5. INPUT

## 5.1 Configuration

File:

analysis/analysis_config.json

```json
{
  "input": {
    "changes_directory": "../review/changes",
    "current_snapshot": "../database/project_snapshot.json",
    "snapshot_history_directory": "../database/snapshots",
    "rules": "analysis_rules.json",
    "architecture_map": "architecture_map.json"
  }
}
```

The configuration contains input paths only.

Output paths are fixed in the code (section 15) and cannot be changed by configuration.

## 5.2 Change record

- review/changes/CHG-NNN.json (read-only);
- any status: PENDING_REVIEW, APPROVED or REJECTED;
- the .md file of the record is not read.

## 5.3 Snapshots

- "from" and "to" of the change record;
- an id is searched in database/snapshots/ first, then in the current snapshot;
- read-only.

## 5.4 Rules

- analysis/analysis_rules.json (read-only);
- format: section 9.

## 5.5 Architecture map

- analysis/architecture_map.json (read-only);
- format and requirements: section 10.

---

# 6. CHECKS

Checks are made in this order.

Any failure aborts the analysis (section 14).

1. Configuration is valid.
2. Arguments are valid (--record has the format CHG-NNN).
3. Rules file is valid (section 9).
4. Architecture map is valid (section 10).
5. Record selection:
   - with --record: the file review/changes/CHG-NNN.json exists;
   - without arguments: at least one file CHG-NNN.json exists; the highest number is selected.
6. Change record is valid:
   - format "requiem-change-record", format_version "0.1";
   - id equals the file name;
   - status is PENDING_REVIEW, APPROVED or REJECTED;
   - review.decision is null for PENDING_REVIEW and equals the status otherwise;
   - comparison.id has the format CMP-NNN-NNN; comparison.result_sha256 is a hash;
   - from.id and to.id have the format SNAP-NNN and are different; source_sha256 values are hashes;
   - project.name and project.target are non-empty strings;
   - summary contains nine non-negative integers;
   - no_changes equals (added + removed + modified + unverified = 0);
   - entry ids are CHG-NNN/1, CHG-NNN/2, … without gaps;
   - entry classes are added, removed, modified or unverified;
   - entries are ordered by class (added, removed, modified, unverified), then by path;
   - every path appears in one entry only;
   - area of every entry equals its first path segment, or "(root)";
   - entry fields match REQUIEM_CHANGE_RECORD_MODEL.md, section 7;
   - a hash is 64 lowercase hexadecimal characters; null is allowed only in unverified entries;
   - a modified entry has two different hashes;
   - the number of entries per class equals the summary;
   - areas equal the counts recomputed from entries;
   - warnings is a list of strings.
7. Project:
   - architecture_map.project equals the project of the change record.
8. Snapshots:
   - both snapshots are found;
   - the SHA-256 of each snapshot file equals the source_sha256 recorded in the change record;
   - each snapshot is valid JSON, its id equals the expected id, its project equals the project of the change record, its file paths are unique.
9. Entries agree with snapshots:
   - summary.files_from and summary.files_to equal the number of files in the snapshots;
   - summary.directories_from and summary.directories_to equal statistics.total_directories;
   - added: path exists only in "to"; size, extension, modified and hash equal the "to" snapshot;
   - removed: path exists only in "from"; size, extension, modified and hash equal the "from" snapshot;
   - modified: path exists in both; from / to size, modified and hash equal the snapshots;
   - unverified: presence equals the snapshots; each non-null side equals its snapshot.

Snapshot content was fully validated by the Comparison Layer.

The SHA-256 check confirms that the snapshots are the same files.

---

# 7. CLASSIFICATION

Every entry of the change record receives exactly one category and exactly one zone.

Classification uses only the path.

Path matching is exact and case-sensitive.

Wildcards and regular expressions are not used.

## 7.1 Category — type of file

Source: categories in analysis_rules.json.

Rule:

1. categories are checked in the order they are listed;
2. a category matches if:
   - the final path segment equals one of its "names", or
   - the path ends with one of its "suffixes";
3. the first matching category is used;
4. no match → "uncategorized".

## 7.2 Zone — part of the project architecture

Source: zones in architecture_map.json.

A zone path is either:

- a directory prefix — ends with "/" (for example "src/core/contracts/");
- an exact file path — does not end with "/" (for example "index.html").

Rule:

1. a zone path equal to the file path → that zone;
2. otherwise the longest directory prefix that the file path starts with → that zone;
3. no match → "unmapped".

A directory prefix "src/core/" matches "src/core/index.js".

It does not match "src/core.zip".

Every zone path string is unique in the map, so the result is always unique.

---

# 8. SIGNALS AND FINDINGS

## 8.1 Signal kinds

Signal kinds are fixed in the code (DEC-018).

The rules file enables them and sets their level, text and parameters.

A rules file with an unknown kind is refused.

| Kind | Evaluated on | One finding per | Parameters |
|---|---|---|---|
| unverified | unverified entries | all such entries | — |
| attention_zone | entries in a zone with attention: true | zone | — |
| generated_zone | entries in a zone with generated: true | zone | — |
| paired_files | a pair of file names in one directory | directory | first, second |
| rename_candidate | removed + added entries with the same hash | hash | — |
| case_candidate | removed + added entries whose paths are equal after Unicode case folding | folded path | — |
| new_top_level | added entries under a first path segment that has no file in "from" | folder | — |
| empty_file | added or modified entries with "to" size 0 | entry | — |
| size_delta | modified entries with a large size change | entry | min_bytes, min_ratio |
| category_changed | entries of the given classes and categories | category | categories, classes |
| unmapped | entries with zone "unmapped" | all such entries | — |
| uncategorized | entries with category "uncategorized" | all such entries | — |

Kinds without parameters may appear in the rules file at most once.

paired_files, size_delta and category_changed may appear more than once, each with its own id.

## 8.2 Evaluation rules

unverified

- entries of class unverified.

attention_zone, generated_zone

- entries of any class whose zone has attention: true (respectively generated: true).

paired_files

- a file counts as changed if it has an entry of class added, removed or modified;
- for each directory where exactly one of <directory>/first and <directory>/second is changed → a finding;
- if the other file of the pair is unverified, no finding is made for that directory and a warning is added;
- evidence states whether the unchanged file exists in the "to" snapshot.

rename_candidate

- added and removed entries are grouped by hash;
- a group with at least one removed and at least one added entry → a finding;
- it is a candidate: equal content under a different path, not a confirmed rename.

case_candidate

- added and removed entries are grouped by the case-folded path;
- a group with at least one removed and at least one added entry → a finding.

A rename that also changes letter case produces both findings.

new_top_level

- an added entry whose path contains "/";
- its first segment is the folder;
- no file of the "from" snapshot starts with "<folder>/" → the folder is new.

Empty directories are not visible (snapshots list files only).

empty_file

- added or modified entries whose "to" size is 0.

size_delta

- modified entries;
- delta = to.size − from.size;
- match when |delta| ≥ min_bytes and (from.size = 0 or |delta| / from.size ≥ min_ratio).

category_changed

- entries whose class is in "classes" and whose category is in "categories".

unmapped, uncategorized

- entries with the reserved zone or category.

A disabled signal (enabled: false) is validated but not evaluated.

## 8.3 Findings

Fields:

- finding: ANL-NNN/F-k (k = position, starting from 1);
- rule: the signal id;
- kind: the signal kind;
- level: info | notice | attention — copied from the rules file;
- text: copied from the rules file;
- entries: the change record entry ids the finding is based on (never empty, ascending);
- evidence: facts of the match (section 8.4).

Order:

- by signal, in the order of the rules file;
- inside a signal, by the smallest entry number of the finding.

The level is set by a human in the rules file.

It is a display priority, not an evaluation of the change.

## 8.4 Evidence

| Kind | Evidence |
|---|---|
| unverified | paths |
| attention_zone | zone |
| generated_zone | zone |
| paired_files | directory, changed (file name), other (file name), other_exists_in_to (true / false) |
| rename_candidate | hash, removed (paths), added (paths) |
| case_candidate | folded_path, removed (paths), added (paths) |
| new_top_level | folder |
| empty_file | path |
| size_delta | path, from_size, to_size, delta |
| category_changed | category |
| unmapped | paths |
| uncategorized | paths |

Paths in evidence are sorted.

---

# 9. RULES FILE

File:

analysis/analysis_rules.json

The rules file is generic.

It contains no project-specific paths.

Project-specific knowledge belongs to the architecture map.

## 9.1 Format

```json
{
  "format": "requiem-analysis-rules",
  "format_version": "0.1",
  "revision": 1,

  "categories": [
    { "id": "manifest", "name": "Dependency manifest", "names": ["package.json", "Cargo.toml"], "suffixes": [] }
  ],

  "signals": [
    {
      "id": "S-PAIR-NPM",
      "kind": "paired_files",
      "enabled": true,
      "level": "notice",
      "text": "package.json and package-lock.json did not change together.",
      "params": { "first": "package.json", "second": "package-lock.json" }
    }
  ]
}
```

## 9.2 Validation

- format and format_version as above;
- revision is an integer ≥ 1;
- category id: lowercase letters, digits and "-"; unique; "uncategorized" is reserved;
- category name: non-empty string;
- names: file names without "/"; suffixes: non-empty strings without "/";
- a category has at least one name or suffix;
- signal id: "S-" followed by uppercase letters, digits and "-"; unique;
- kind: one of section 8.1;
- enabled: true or false;
- level: info, notice or attention;
- text: non-empty string;
- params exactly as required by the kind:
  - paired_files: first and second — different file names without "/";
  - size_delta: min_bytes — integer ≥ 1; min_ratio — number > 0;
  - category_changed: categories — non-empty list of existing category ids; classes — non-empty subset of added, removed, modified, unverified;
  - other kinds: params is an empty object.

## 9.3 Default rule set v0.1

This rule set is part of this model and is approved with it.

Categories (order matters):

| # | id | names | suffixes |
|---|---|---|---|
| 1 | manifest | package.json, Cargo.toml | — |
| 2 | lockfile | package-lock.json, Cargo.lock, yarn.lock, pnpm-lock.yaml | — |
| 3 | vcs | .gitignore, .gitattributes | — |
| 4 | tool-config | — | .config.js, .config.ts, .config.mjs, .config.cjs, .conf.json |
| 5 | source | — | .js, .jsx, .ts, .tsx, .mjs, .cjs, .rs, .py |
| 6 | style | — | .css, .scss, .sass, .less |
| 7 | markup | — | .html |
| 8 | data | — | .json, .toml, .yaml, .yml |
| 9 | documentation | — | .md, .txt |
| 10 | image | — | .png, .svg, .ico, .icns, .jpg, .jpeg, .gif, .webp |
| 11 | archive | — | .zip, .7z, .rar, .tar, .gz |

Check against SNAP-003 (62 files): every file receives a category, 0 uncategorized.

source 22, image 19, data 5, tool-config 4, manifest 2, lockfile 2, vcs 2, style 2, archive 2, markup 1, documentation 1.

"tool-config" is listed before "source" and "data", so vite.config.js and src-tauri/tauri.conf.json are tool-config, not source or data.

Signals (order = order in the report):

| id | kind | level | params | text |
|---|---|---|---|---|
| S-UNVERIFIED | unverified | attention | — | File content could not be verified (null hash). |
| S-ATTENTION-ZONE | attention_zone | attention | — | Changes in a zone marked for attention in the architecture map. |
| S-PAIR-NPM | paired_files | notice | package.json / package-lock.json | package.json and package-lock.json did not change together. |
| S-PAIR-CARGO | paired_files | notice | Cargo.toml / Cargo.lock | Cargo.toml and Cargo.lock did not change together. |
| S-RENAME-CANDIDATE | rename_candidate | notice | — | Removed and added files have identical content. |
| S-CASE-CANDIDATE | case_candidate | notice | — | Removed and added paths differ only in letter case. |
| S-NEW-TOP-LEVEL | new_top_level | notice | — | A new top-level folder appeared. |
| S-EMPTY-FILE | empty_file | notice | — | File size is 0 bytes. |
| S-ARCHIVE | category_changed | notice | categories: archive; classes: added, modified | An archive file was added or modified in the project tree. |
| S-UNMAPPED | unmapped | notice | — | Paths are not covered by the architecture map. |
| S-SIZE-DELTA | size_delta | info | min_bytes: 10240; min_ratio: 0.5 | File size changed significantly. |
| S-GENERATED-ZONE | generated_zone | info | — | Changes in a zone of generated files. |
| S-UNCATEGORIZED | uncategorized | info | — | File type is not covered by the categories. |

---

# 10. ARCHITECTURE MAP

File:

analysis/architecture_map.json

The architecture map describes where the parts of the project architecture are located.

It is project truth.

It is written and approved by a human (DEC-017).

It is not part of this model and is approved separately.

## 10.1 Format

```json
{
  "format": "requiem-architecture-map",
  "format_version": "0.1",
  "revision": 1,
  "status": "DRAFT",
  "approved": null,

  "project": {
    "name": "REQUIEM",
    "target": "requiem-tauri"
  },

  "zones": [
    {
      "id": "example-zone",
      "name": "Example zone",
      "description": "What this part of the project is.",
      "paths": ["example/"],
      "attention": false,
      "generated": false
    }
  ]
}
```

The zone above is a format example, not map content.

## 10.2 Validation

- format and format_version as above;
- revision is an integer ≥ 1;
- status is DRAFT or APPROVED;
- approved is null for DRAFT and a date "YYYY-MM-DD" for APPROVED;
- project.name and project.target are non-empty strings;
- zones is a list (it may be empty);
- zone id: lowercase letters, digits and "-"; unique; "unmapped" is reserved;
- name and description: non-empty strings;
- paths: non-empty list;
- attention and generated: true or false;
- a zone path:
  - is relative to the project root and uses "/" separators;
  - does not start with "/" and does not contain "\", "./", "../" or "//";
  - is not empty;
  - ends with "/" for a directory prefix; otherwise it is an exact file path;
- every zone path string is unique in the whole map.

## 10.3 Requirements for map content

1. The map describes only the project that the snapshots describe (project.name / project.target).
2. Zones follow the approved architecture documentation. They do not invent structure.
3. Every top-level folder and every root file of the current snapshot should belong to a zone. Paths left unmapped are listed by the analysis (coverage, S-UNMAPPED).
4. attention: true is set only for zones where any change needs human attention during review. The choice is made by the approver.
5. generated: true is set only for zones that contain files generated by tools.
6. The map contains descriptions only. It does not contain evaluations, instructions or recommendations.
7. The map does not describe Memory Core itself.
8. Every change of the map increments revision.
9. status APPROVED and the approval date are set only by a human.
10. AI may prepare a draft only on request. A draft has status DRAFT.
11. The analyzer never modifies the map.

The analyzer accepts a DRAFT map and a map with no zones.

Both produce a warning (section 13).

---

# 11. RESULT STRUCTURE

File:

reports/latest_analysis.json

Example (shortened; illustrative data — zone ids are examples, not the approved map):

```json
{
  "format": "requiem-analysis",
  "format_version": "0.1",
  "id": "ANL-005",
  "generated": "2026-09-25T10:00:00",
  "status": "COMPLETED",

  "change_record": {
    "id": "CHG-005",
    "status": "PENDING_REVIEW",
    "record_sha256": "…",
    "facts_sha256": "…",
    "comparison_id": "CMP-004-005"
  },
  "from": { "id": "SNAP-004", "source_sha256": "…" },
  "to":   { "id": "SNAP-005", "source_sha256": "…" },
  "project": { "name": "REQUIEM", "target": "requiem-tauri" },

  "rules": { "revision": 1, "sha256": "…" },
  "architecture_map": { "revision": 1, "status": "APPROVED", "sha256": "…" },

  "entries": [
    { "entry": "CHG-005/1", "class": "modified", "path": "src/core/contracts/UserIntent.js",
      "category": "source", "zone": "core-contracts" },
    { "entry": "CHG-005/2", "class": "modified", "path": "package.json",
      "category": "manifest", "zone": "project-root" }
  ],

  "findings": [
    {
      "finding": "ANL-005/F-1",
      "rule": "S-ATTENTION-ZONE",
      "kind": "attention_zone",
      "level": "attention",
      "text": "Changes in a zone marked for attention in the architecture map.",
      "entries": ["CHG-005/1"],
      "evidence": { "zone": "core-contracts" }
    },
    {
      "finding": "ANL-005/F-2",
      "rule": "S-PAIR-NPM",
      "kind": "paired_files",
      "level": "notice",
      "text": "package.json and package-lock.json did not change together.",
      "entries": ["CHG-005/2"],
      "evidence": { "directory": "", "changed": "package.json",
                    "other": "package-lock.json", "other_exists_in_to": true }
    }
  ],

  "summary": {
    "classes": { "added": 0, "removed": 0, "modified": 2, "unverified": 0, "unchanged": 60 },
    "zones": [
      { "zone": "core-contracts", "added": 0, "removed": 0, "modified": 1, "unverified": 0 },
      { "zone": "project-root", "added": 0, "removed": 0, "modified": 1, "unverified": 0 }
    ],
    "categories": [
      { "category": "manifest", "added": 0, "removed": 0, "modified": 1, "unverified": 0 },
      { "category": "source", "added": 0, "removed": 0, "modified": 1, "unverified": 0 }
    ],
    "size_delta": { "added": 0, "removed": 0, "modified": 42, "total": 42, "unverified_excluded": 0 },
    "findings": { "attention": 1, "notice": 1, "info": 0 }
  },

  "coverage": {
    "files": 62,
    "zones": [ { "zone": "core-contracts", "files": 6 } ],
    "unmapped": 0,
    "unmapped_paths": [],
    "categories": [ { "category": "source", "files": 22 } ],
    "uncategorized": 0,
    "uncategorized_paths": []
  },

  "warnings": []
}
```

Field notes:

- id: ANL-<number of the change record>, derived from the record;
- generated: local time of the run, without time zone;
- status: COMPLETED or COMPLETED_WITH_WARNINGS;
- change_record.status: status of the record at the time of the analysis;
- change_record.record_sha256: SHA-256 of the record file at the time of the analysis. It changes when the record is reviewed, because review rewrites the file;
- change_record.facts_sha256: SHA-256 of the facts of the record. It does not change on review (section 11.1);
- rules.sha256, architecture_map.sha256: SHA-256 of the files used;
- entries: every entry of the change record, in the same order, with its category and zone;
- summary.classes: copied from the change record summary;
- summary.zones: only zones with entries; in map order, then "unmapped";
- summary.categories: only categories with entries; in rules order, then "uncategorized";
- summary.size_delta: added = sum of added sizes; removed = minus the sum of removed sizes; modified = sum of (to.size − from.size); unverified entries are excluded and counted;
- coverage: all files of the "to" snapshot, not only changed files; zones and categories with at least one file; paths sorted.

## 11.1 facts_sha256

SHA-256 of the UTF-8 bytes of a JSON serialization of an object with the keys

id, comparison, from, to, project, summary, no_changes, areas, entries

copied from the change record, serialized with sorted keys, without spaces (separators "," and ":") and without escaping non-ASCII characters.

status, review and warnings are not included.

## 11.2 Self-check (before writing)

- every entry of the change record appears exactly once in entries, with the same id, class and path;
- the sum of each class over summary.zones equals the class count of the change record;
- the sum of each class over summary.categories equals the class count of the change record;
- every entry id referenced by a finding exists;
- summary.findings equals the number of findings per level;
- coverage: the sum of zone files plus unmapped equals coverage.files; the same for categories.

---

# 12. REPORT

File:

reports/latest_analysis.md

Sections:

- analysis id, generated time, status, project;
- a fixed note: "Findings are rule matches, not evaluations. Analysis does not approve or reject changes.";
- source (change record id, status at analysis, record_sha256, facts_sha256, comparison, snapshots from / to);
- rules and map (revision, sha256; map status);
- summary (classes, findings per level, size delta);
- FINDINGS — attention, then notice, then info; each: finding id, rule, text, entries with paths, evidence;
- entries (entry, class, path, category, zone);
- zones;
- categories;
- coverage (counts, unmapped paths, uncategorized paths);
- warnings;
- how to review (only when the change record is PENDING_REVIEW):

```
change_report/   python change_reporter.py --approve CHG-NNN --note "text"
change_report/   python change_reporter.py --reject CHG-NNN --note "text"
```

---

# 13. STATUS AND WARNINGS

The analysis completes with status COMPLETED_WITH_WARNINGS if at least one warning exists.

Warnings:

- "Architecture map is DRAFT (not approved)." — map status is DRAFT;
- "Architecture map has no zones." — zones is empty;
- "<CHG-NNN> is not the latest change record (latest: <CHG-MMM>)." — --record names an older record;
- "Change record is REJECTED." — the analyzed record is rejected;
- "<rule> not evaluated for directory '<directory>': <file> is unverified." — paired_files skipped;
- "Change record: <warning>" — every warning of the change record, in its order.

---

# 14. ABORT RULES

The analysis is aborted and nothing is written if:

- analysis_config.json is not found or is invalid;
- --record has an invalid format;
- the rules file is not found, is not valid JSON or is invalid (section 9.2);
- the architecture map is not found, is not valid JSON or is invalid (section 10.2);
- there is no change record (without arguments), or the given record file is not found;
- the change record is not valid JSON or is invalid (section 6, check 6);
- the architecture map belongs to another project;
- a snapshot is not found, cannot be read, is not valid JSON, has an unexpected id or belongs to another project;
- a snapshot SHA-256 differs from the change record;
- entries do not agree with the snapshots (section 6, check 9);
- the self-check fails.

On abort:

- the message starts with "Memory Core analysis aborted:";
- exit code is 1;
- existing reports are left untouched.

---

# 15. STORAGE RULE

Only the latest analysis result is stored (DEC-016):

```
reports/latest_analysis.json
reports/latest_analysis.md
```

These paths are fixed in the code.

Each run replaces both files.

History of analysis results is not created:

- no database/analysis/;
- no review/analysis/;
- no ANL files in other locations.

An analysis result can be rebuilt from:

- the change record;
- the two snapshots;
- the rules file;
- the architecture map.

The result records the SHA-256 of all four inputs.

Write procedure:

1. both files are fully written to .tmp files;
2. each .tmp file replaces its target file.

A final report file is never partially written.

---

# 16. LIMITATIONS OF v0.1

- Analysis works on metadata only (path, size, time, hash). It cannot say what changed inside a file.
- One change record per run. There is no analysis across several records (for example, how often a file changes).
- Rename and case candidates are candidates. Copies of one file produce one group.
- Path matching is case-sensitive; wildcards are not supported.
- The category of a file depends on the order of categories in the rules file.
- Only the latest result is kept. A result made with an older rules or map revision is lost after the next run.
- After a new change record, or after a change of the rules file or the map, the report is outdated until the analyzer is run again.
- Analysis is not enforced before review. The change reporter does not check that an analysis exists.
- Entries are checked against the snapshots, but an entry removed from a change record together with a matching change of its summary and areas is not detected.
- New folders are detected from file paths only; empty directories are not visible.
- The two report files are replaced one after another: if a failure happens between the two replacements, the JSON file is new and the .md file is old. Each file is complete.
- The analyzer must be started from inside analysis/.

---

# 17. NOT PART OF v0.1

- impact analysis;
- dependency graph;
- analysis of file content;
- reading project files;
- AI analysis;
- history of analysis results;
- analysis as an input of Context Update;
- writing to project memory;
- reading identity, state, decisions, events or checkpoints;
- evaluations and recommendations;
- automatic approval or rejection;
- enforcement of analysis before review;
- UI;
- application integration.

END OF ANALYSIS MODEL
