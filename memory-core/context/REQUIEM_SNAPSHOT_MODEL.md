# REQUIEM SNAPSHOT MODEL

Version: 0.4

Document Type:
State Storage Definition

Purpose:
Define how REQUIEM Memory Core represents project state snapshots.

---

# 1. PURPOSE

Snapshot is a frozen representation of project state at a specific moment.

It answers:

"What existed at this point in time?"

Snapshot is not an analysis.

Snapshot is raw project state.

---

# 2. CORE PRINCIPLE

Snapshot stores facts.

It does not store:

- assumptions;
- conclusions;
- recommendations.

Analysis belongs to later layers.

---

# 3. SNAPSHOT LIFECYCLE

```
Project State
↓
Scanner
↓
Snapshot Creation
↓
Snapshot Storage
↓
Comparison
↓
Change Analysis
```

Comparison format and rules are defined in:

context/REQUIEM_COMPARISON_MODEL.md

Analysis format and rules are defined in:

context/REQUIEM_ANALYSIS_MODEL.md

---

# 4. SNAPSHOT LOCATION

Current snapshot:

```
database/project_snapshot.json
```

Snapshot history:

```
database/snapshots/SNAP-NNN.json
```

Before a new snapshot is written, the current snapshot is copied into the history directory.

Snapshots are not stored in the checkpoints/ directory.

Snapshots and checkpoints are separate concepts (DEC-005).

---

# 5. SNAPSHOT STRUCTURE

Example:

```json
{
  "id": "SNAP-001",

  "created": "2026-09-24T10:00:00",

  "project": {
    "name": "REQUIEM",
    "target": "requiem-tauri"
  },

  "environment": {
    "machine_path": "",
    "platform": ""
  },

  "statistics": {
    "total_files": 0,
    "total_directories": 0
  },

  "files": [
    {
      "path": "",
      "size": 0,
      "extension": "",
      "modified": "",
      "hash": ""
    }
  ]
}
```

Snapshot ID format:

SNAP-NNN (for example SNAP-001).

---

# 6. PROJECT AND ENVIRONMENT

project

Describes what is scanned.

It does not depend on the machine.

environment

Describes where the scan was made:

- machine_path: absolute project path on the machine;
- platform: operating system.

Purpose:

Keep project identity separate from machine environment.

---

# 7. FILE INFORMATION

Each tracked file may contain:

Path

Location inside project, relative to the project root, with "/" separators.

Size

File size in bytes.

Purpose:

Detect changes.

Modified

Last modification timestamp.

Purpose:

Detect updates.

Extension

File type.

Purpose:

Classification.

Hash

Content fingerprint (SHA-256).

Purpose:

Confirm real content change.

If the file content cannot be read, hash is null and the scan report contains a warning.

---

# 8. SNAPSHOT RULES

Snapshot must:

- be reproducible;
- preserve previous states;
- not overwrite history silently;
- contain only verified information.

---

# 9. SNAPSHOT VS REPORT

Important separation:

Snapshot:

"What exists."

Report:

"What changed."

Analysis:

"What does it mean."

These are different layers.

The comparison result ("What changed") is defined in:

context/REQUIEM_COMPARISON_MODEL.md

The analysis result ("What does it mean") is defined in:

context/REQUIEM_ANALYSIS_MODEL.md

---

# 10. FUTURE DEVELOPMENT

Future versions may add:

- dependency graph;
- architecture mapping;
- semantic classification;
- AI analysis.

Not part of v0.1.

END OF SNAPSHOT MODEL
