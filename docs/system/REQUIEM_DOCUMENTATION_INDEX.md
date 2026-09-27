# REQUIEM DOCUMENTATION INDEX

Version: 1.2

Purpose:
Define the structure and navigation of REQUIEM documentation, the REQUIEM information standard, and the registry of allocated identifiers (Decision #014).

---

# DOCUMENTATION HIERARCHY

All documentation lives in the repository jonysilvervi/Requiem (Decision #008):

| Folder | Content |
|---|---|
| docs/system/ | documentation navigation, decisions, history, active session, ecosystem roadmap |
| docs/ai/ | AI roles, workflows, automation concepts |
| docs/app/ | REQUIEM Application: current state, phase documents |
| memory-core/ | Memory Core system, its documents and data |
| docs/memory-core-legacy/ | superseded Memory Core v0.1 concept documents (history only) |

---

# AI SESSION READING ORDER

Before working:

1. README.md (repository root)
2. docs/system/REQUIEM_ACTIVE_SESSION.md
3. REQUIEM_AI_MASTER_CONTEXT.md
4. REQUIEM_AI_SESSION_PROTOCOL.md
5. REQUIEM_CURRENT_STATE_SNAPSHOT.md
6. Relevant architecture documents
7. Task-specific documentation

---

# DOCUMENT PRIORITY

## Highest Priority

Current State and Decision Records.

## Medium Priority

Architecture and Phase Documents.

## Supporting Priority

Additional notes and research.

---

# REQUIEM INFORMATION STANDARD

Established by Decision #014 [ED-014].

## A. Namespaces

| Prefix | Object |
|---|---|
| `AREA-` | administrative tracking area |
| `ED-` | ecosystem decision in docs/system/REQUIEM_DECISION_LOG.md |
| `TASK-` | implementation or documentation task |
| `STEP-` | stable step of an accepted plan |
| `Q-` | tracked question |
| `ISS-` | tracked issue or finding |

`SES-` is not part of the identifier set. REQUIEM_ACTIVE_SESSION.md is a replace-in-place current-state document; individual sessions are not persisted as standalone records. Git history and the Changelog already preserve the session and change chronology.

## B. Permanent allocation

Once allocated, an identifier is never reused.

Resolved, rejected, completed, superseded or obsolete objects keep their identifiers.

Every new identifier is added to the section ALLOCATED IDENTIFIERS below before it is used.

## C. AREA

AREA is administrative tracking metadata. It is not:

- an architecture layer;
- a Project ID;
- a new ecosystem object type.

AREA identifiers do not resolve Foundation open item O5 (Project ID format) or O6 (REQUIEM Engine scope). Memory Core System and Memory Core Development Project remain distinct subjects (FD-B8).

## D. ED

`ED-NNN` maps exactly to `Decision #NNN` in REQUIEM_DECISION_LOG.md. Example: `ED-013` = ecosystem Decision #013.

`ED-013` is NOT `DEC-013`. `DEC-` remains the existing Memory Core decision namespace (memory-core/database/decisions.json). The two namespaces identify different objects.

## E. Preserved existing identifiers

These identifier systems remain unchanged and are not renamed or migrated:

`DEC-`, `DOC-`, `FD-B`, `CP-`, `CHG-`, `SNAP-`, `CU-`, `ANL-`, `EVENT-`, and open items `O1` through `O7`.

## F. Status systems

A status word is always read together with its object type (FD-B2).

| Object | Statuses |
|---|---|
| AREA | `ACTIVE`, `FROZEN`, `PAUSED`, `PLANNED`, `DONE` |
| TASK | `PROPOSED`, `SPECIFIED`, `IN PROGRESS`, `AWAITING CHECK`, `DONE`, `REJECTED` |
| Document | as defined by memory-core/context/REQUIEM_DOCUMENT_REGISTRY.md, section 3 |

Document Status and Object Status are separate properties. A document describing a task can be DRAFT while the task is SPECIFIED.

## G. New-file passport

Every new standalone documentation file created after ED-014 starts with:

```
ID:
Type:
Document Status:
Area:
Updated:
```

When the document represents an object with its own lifecycle, it also contains:

```
Object Status:
```

Container or reference files that do not represent an ID-bearing object use `ID: N/A`. An unrelated identifier is never invented only to fill the passport.

## H. Reference syntax

| Target | Form |
|---|---|
| documentation | `FILE.md, section N` |
| application code | `requiem-tauri: path/to/file, line N` |
| tracked object | `[ED-014]`, `[TASK-001]`, `[Q-001]` |

---

# ALLOCATED IDENTIFIERS

The single canonical allocation list for `AREA-`, `ED-`, `TASK-`, `STEP-`, `Q-` and `ISS-`. It prevents reuse and records identity only. Detailed state stays in the source document of each object.

## AREA

| ID | Object | Notes |
|---|---|---|
| AREA-VC | REQUIEM Visual Core | |
| AREA-EE | Execution Engine (PowerShell) | does not resolve O6 |
| AREA-MC | Memory Core | covers Memory Core work; Memory Core System and Memory Core Development Project stay distinct (FD-B8) |
| AREA-MP | REQUIEM Mod Pack | |
| AREA-RE | REQUIEM Engine | does not resolve O6 |
| AREA-TL | Tools | |

## ED

Source: docs/system/REQUIEM_DECISION_LOG.md. Not related to Memory Core `DEC-` records.

| ID | Maps to |
|---|---|
| ED-001 | Decision #001 |
| ED-002 | Decision #002 |
| ED-003 | Decision #003 |
| ED-004 | Decision #004 |
| ED-005 | Decision #005 |
| ED-006 | Decision #006 |
| ED-007 | Decision #007 |
| ED-008 | Decision #008 |
| ED-009 | Decision #009 |
| ED-010 | Decision #010 |
| ED-011 | Decision #011 |
| ED-012 | Decision #012 |
| ED-013 | Decision #013 |
| ED-014 | Decision #014 |

## TASK

| ID | Object | Area | Status | Related | Source | Specification |
|---|---|---|---|---|---|---|
| TASK-001 | R0 migration step 1 — L0 SHELL + static dark theme + calibrated color tokens | AREA-VC | SPECIFIED | STEP-R0-01 | docs/app/R0_MIGRATION_PLAN.md, section Steps, step 1 | docs/app/tasks/TASK-001_R0_STEP1_L0_SHELL.md |

## STEP

Source: docs/app/R0_MIGRATION_PLAN.md, section Steps.

| ID | Object |
|---|---|
| STEP-R0-01 | L0 SHELL + theme + tokens |
| STEP-R0-02 | L1 NAVIGATION |
| STEP-R0-03 | L2 WORKSPACE |
| STEP-R0-04 | L4 SYSTEM (safe part) |
| STEP-R0-05 | L3 INTELLIGENCE |
| STEP-R0-06 | Cleanup |

## Q

| ID | Object | Related | Source |
|---|---|---|---|
| Q-001 | Location of the PowerShell Execution Engine code | ISS-006 | docs/system/REQUIEM_ACTIVE_SESSION.md, section OPEN QUESTIONS; docs/app/NOTES.md, finding 6 |

## ISS

Source: docs/app/NOTES.md, section "Open findings for the owner", findings 1–7.

| ID | Object | Finding | Related |
|---|---|---|---|
| ISS-001 | Visual prototype is not connected | 1 | |
| ISS-002 | Legacy dependencies are back | 2 | |
| ISS-003 | Leftover template files, empty file and stray folder | 3 | |
| ISS-004 | Empty folders are not stored by git | 4 | |
| ISS-005 | Implementation Plan references the old Core Skeleton spec version | 5 | |
| ISS-006 | PowerShell bridge is a stub; the real Execution Engine location is open | 6 | Q-001 |
| ISS-007 | PowerShell bridge inserts action input without escaping; must be fixed before real input is used | 7 | |

---

# END OF INDEX