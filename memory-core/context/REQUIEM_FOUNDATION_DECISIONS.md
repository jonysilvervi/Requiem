# REQUIEM FOUNDATION DECISIONS

Version: 0.4

Status: DRAFT


---

# 1. Purpose


This document defines foundational architectural decisions required before creating Knowledge Model v1.


The purpose is to remove ambiguity between:

- REQUIEM ecosystem;
- Memory Core System;
- Memory Core Development Project;
- observed projects;
- environments;
- knowledge ownership.


These decisions define the foundation for Memory Core v0.7 development.


Terms are defined in REQUIEM_GLOSSARY.md.


---

# 2. Decision identifiers


Decisions in this document use identifiers FD-B1 … FD-B8.


This document is a DRAFT architectural decision document.


FD-B1 … FD-B8 are not DEC records and are not converted into DEC records now (open item O1, decided 2026-09-24).


After approval of the v0.7 Foundation, required decisions may be promoted into DEC records (database/decisions.json).


Until the document is approved, its decisions are not project truth (REQUIEM_DOCUMENT_REGISTRY.md, section 2), even when an individual decision is accepted by the human maintainer.


---

# 3. FD-B1 — Analysis and Proposal separation


## Decision


Analysis and Proposal are different concepts.


Analysis interprets verified changes with deterministic rules.


Analysis produces findings only:

- classifications (category, zone);
- findings of rule matches;
- warnings;
- evidence.


Analysis results are reports. They are not proposals and not knowledge.


Analysis does not create proposals.

Analysis does not create or change trusted knowledge.

Analysis does not modify memory.


This decision is consistent with DEC-015 and REQUIEM_ANALYSIS_MODEL.md.


Proposal creation belongs to:

- Architecture Discovery (future);
- adapters (future);
- AI assistants;
- human operators.


A proposal source may use findings as evidence.

A finding never becomes a proposal by itself.


## Flows


Change flow (implemented in CP-006):


Observation

↓

Snapshot

↓

Comparison

↓

Change Record

↓

Analysis → Findings (report)

↓

Human Review (change record)

↓

Context Update (CU proposal → Human Review → manual apply)



Knowledge flow (future):


Facts, Findings (evidence)

↓

Proposal source (Discovery, adapter, AI assistant, human operator)

↓

Knowledge Proposal

↓

Human Review

↓

Trusted Knowledge



---

# 4. FD-B2 — Object status separation


## Decision


Different object types use different status systems.

A status word is always read together with its object type.


## Documents


DRAFT

↓

REVIEW

↓

APPROVED

↓

SUPERSEDED


SUPERSEDED is used for documents only.


APPROVED requires an explicit approval record: approver, date, approved version (REQUIEM_DOCUMENT_REGISTRY.md, section 3).


## Knowledge elements


PROPOSED

↓

TRUSTED

↓

DEPRECATED


DEPRECATED is used for knowledge elements only.

Knowledge elements do not use APPROVED.


## Operational records


Change records (CHG): PENDING_REVIEW, APPROVED, REJECTED.

Context update proposals (CU): PROPOSED, APPROVED, REJECTED, APPLIED, STALE.


These statuses remain unchanged.

Existing operational workflows are preserved.


## Implementation state


Implementation state is a separate property, not a status.


Values:

- not implemented;
- implemented (with component version);
- not applicable (documents that do not describe a component).


A document can be APPROVED and not implemented, or DRAFT and describe an implemented component.


---

# 5. FD-B3 — Project and Environment separation


## Decision


Project and Environment are different concepts.


## Project


A project is an independent development subject owned by REQUIEM and observed and supported by Memory Core.


Memory Core does not control projects.


Projects:

- REQUIEM Application;
- REQUIEM Mod Pack;
- Memory Core Development Project.


## Environment


An environment is an external or supporting system in which a project operates.


REQUIEM does not own environments.


Examples:

- S.T.A.L.K.E.R. 2;
- Unreal Engine;
- operating system;
- runtime environment;
- framework.


A project may interact with an environment without owning it.


Example:


REQUIEM Mod Pack

changes

S.T.A.L.K.E.R. 2 (environment)


This decision is consistent with REQUIEM_CONTEXT.md, section 1 ("Games are environments"), and database/identity.json ("current_supported_environment": "S.T.A.L.K.E.R. 2").


---

# 6. FD-B4 — Knowledge ownership levels


## Decision


Knowledge is separated by ownership level.

Every knowledge element has exactly one ownership level.


## System Knowledge


Knowledge about the Memory Core System: how Memory Core works and which rules it follows.


Examples:

- architecture rules of Memory Core layers;
- system DEC decisions;
- section 5 of the development protocol (Memory Core rules);
- formats and models of Memory Core components.


## Ecosystem Knowledge


Knowledge about REQUIEM as a whole.


Examples:

- identity;
- global principles;
- terminology (glossary);
- development protocol, except section 5;
- ecosystem DEC decisions;
- identity of known environments (FD-B7).


## Shared Knowledge


Reusable knowledge between projects.


Examples:

- patterns;
- solutions;
- experience.


Shared Knowledge contains no project-specific paths, files or private project decisions.


## Project Knowledge


Knowledge belonging to one project.


Examples:

- architecture of the project;
- components;
- project decisions;
- project-specific usage and modifications of referenced environments (FD-B7).


## Current DEC records by ownership level


| Records | Ownership level |
|---|---|
| DEC-001, DEC-002, DEC-003 | Ecosystem Knowledge |
| DEC-005 … DEC-018 | System Knowledge |
| — | Project Knowledge (no project decisions are recorded yet) |


DEC-004 is absent from decisions.json. Its content is unknown (known issue 6).


---

# 7. FD-B5 — Architecture Knowledge ownership


## Decision


Architecture Knowledge is Project Knowledge.

It belongs to exactly one project.


It must not be mixed with System Knowledge or Ecosystem Knowledge.


The current architecture map implementation (analysis/architecture_map.json, zone format of REQUIEM_ANALYSIS_MODEL.md section 10) is an initial prototype.


Revision 2 of analysis/architecture_map.json describes the REQUIEM ecosystem and Memory Core (for example zone "zone-memory"). It is not Architecture Knowledge of any project in the sense of this decision.


The file is not changed by this decision. Analyzer v0.1 continues to read it (current coverage of SNAP-003: 0 of 62 files).


Future Knowledge Model v1 must define:

- entities;
- relationships;
- ownership;
- evidence;
- provenance;
- revisions;
- knowledge status (FD-B2).


---

# 8. FD-B6 — Project relationships


## Decision


Projects may reference environments and Shared Knowledge.


A reference does not transfer ownership.


Projects do not own and do not modify other projects' knowledge.


Example:


REQUIEM Mod Pack

references:

S.T.A.L.K.E.R. 2 (environment)

uses:

Shared Knowledge


References from one project to another project are not decided (section 13, open item O2).


---

# 9. FD-B7 — Knowledge about environments


## Decision


Accepted by the human maintainer on 2026-09-24.


Environment identity belongs to Ecosystem Knowledge.


Project-specific usage and modifications of an environment belong to Project Knowledge of the project that references the environment.


Environments do not own knowledge.

There is no separate "environment knowledge" ownership level.


## Rules


1. A project references an environment; the reference does not make the environment a project.

2. Project-specific usage and modifications of an environment (for example: "the mod pack changes the weapon system of S.T.A.L.K.E.R. 2") belong to the project that records them.

3. Two projects that reference the same environment keep separate knowledge about their own usage and modifications of it. This knowledge of one project does not become another project's knowledge automatically (REQUIEM_INSTANCE_MODEL.md, project isolation).

4. Reusable, project-independent knowledge about an environment can become Shared Knowledge only through human review, without project-specific paths.

5. The identity of an environment (name and version, for example S.T.A.L.K.E.R. 2) is Ecosystem Knowledge, so that all projects reference the same environment consistently. This matches the current location of "current_supported_environment" in database/identity.json.


---

# 10. FD-B8 — Memory Core System and Memory Core Development Project


## Decision


The Memory Core System and the Memory Core Development Project are different subjects.


## Memory Core System


The implemented system: code of the layers, formats, rules.


It is not a project.

Its knowledge is System Knowledge (FD-B4).


## Memory Core Development Project


The development work on Memory Core: current state, focus, milestones, versions, roadmap.


It is a project like any other project (FD-B3).

Its knowledge is Project Knowledge.


## Separation of current records


| Current record | Subject |
|---|---|
| Code of scanner/, comparison/, change_report/, context_update/, analysis/ | Memory Core System |
| Models of implemented layers, development protocol section 5, DEC-005 … DEC-018 | Memory Core System (System Knowledge) |
| database/state.json (focus, completed work, next actions) | Memory Core Development Project |
| database/events.json milestones (EVENT-001, 002, 004, 005, 007, 008, 009) | Memory Core Development Project |
| database/checkpoints.json (CP-001 … CP-006) | Memory Core Development Project |
| Snapshots, CHG-001, CU-001, EVENT-006 (requiem-tauri) | REQUIEM Application |
| database/identity.json, DEC-001 … DEC-003, development protocol except section 5 | REQUIEM Ecosystem (Ecosystem Knowledge) |


The table describes subjects. It does not move any file (section 11).


---

# 11. Storage principle


Future Memory Core architecture must separate data by ownership level:

- system data;
- ecosystem data;
- shared data;
- project data.


Knowledge exists at every level. It is not a separate storage level.


Current storage structure remains unchanged until migration planning is approved.


---

# 12. Migration principle and transitional state


v0.7 does not immediately redesign existing storage.


First:

- define models;
- define ownership;
- define relationships;
- define migration strategy.


Only after approval may existing data structures change.


Until migration, CP-006 contains these known deviations from this document:

1. One store holds System, Ecosystem, Memory Core Development Project and REQUIEM Application data (FD-B4, FD-B8).
2. Context Update writes REQUIEM Application change events and snapshot state into Memory Core documents (README.md, context/REQUIEM_CONTEXT.md) and into database/events.json, which also holds Memory Core Development milestones (DEC-011).
3. analysis/architecture_map.json revision 2 is stored in a Memory Core System folder and describes the ecosystem (FD-B5).
4. Snapshot project identity is "REQUIEM" / "requiem-tauri" (ecosystem name and folder name), not a stable project ID.
5. Checkpoint records CP-001 … CP-006 describe Memory Core versions; DEC-005 defines checkpoints as recovery points (open item O3).


These deviations are accepted until migration is approved. They are not fixed by this document.


---

# 13. Open items


Not decided by this document, except where marked DECIDED:


| ID | Open item |
|---|---|
| O1 | DECIDED (2026-09-24): this document stays a DRAFT architectural decision document; FD-B1 … FD-B8 are not converted into DEC records now; required decisions may be promoted into DEC records after v0.7 Foundation approval (section 2). |
| O2 | References from one project to another project (for example REQUIEM Application working with REQUIEM Mod Pack). |
| O3 | Checkpoint (recovery point, DEC-005) and Release (Memory Core version record) as separate concepts. |
| O4 | Number of Memory Core instances per REQUIEM ecosystem. |
| O5 | Format of project IDs. |
| O6 | Scope of REQUIEM Engine and its relation to the engine contracts in requiem-tauri (src/core/contracts/). |
| O7 | Decision on the seven DRAFT architecture documents that conflict with FD-B1 and FD-B5 (see REQUIEM_DOCUMENT_REGISTRY.md). |


---

# 14. Preparation for Knowledge Model v1


Knowledge Model v1 may be created only after this document is approved.


Knowledge Model v1 must define:

- facts;
- evidence;
- entities;
- relationships;
- references to environments (FD-B7);
- ownership levels (FD-B4);
- provenance;
- proposals;
- trusted knowledge;
- knowledge status (FD-B2);
- revisions.


---

# 15. Final goal


Memory Core must evolve into a universal knowledge system for the REQUIEM ecosystem.


It must support multiple projects while preserving:

- separation;
- history;
- human authority;
- controlled evolution.


END OF DOCUMENT
