# REQUIEM GLOSSARY

Version: 0.4

Status: DRAFT


---

# 1. Purpose


REQUIEM Glossary defines the official terminology used across the REQUIEM ecosystem and Memory Core documentation.


The purpose of this document is to prevent ambiguity between different concepts and ensure that all system components use the same definitions.


This document is the foundation for future architecture, knowledge models and multi-project support.


Decisions referenced as FD-B1 … FD-B8 are defined in REQUIEM_FOUNDATION_DECISIONS.md.


---

# 2. Core principle


The same word must represent the same concept across REQUIEM.


Documentation, code, proposals and knowledge records must use the definitions from this glossary.


If a new concept appears, it must be defined before becoming part of trusted documentation.


Existing CP-006 formats keep their field names until migration (for example the snapshot fields project.name and project.target). Such differences are listed as transitional deviations in REQUIEM_FOUNDATION_DECISIONS.md, section 12.


---

# 3. Ecosystem terms


## REQUIEM Ecosystem


Definition:

The complete development environment containing projects, the REQUIEM Engine, tools and Memory Core.


Structure:


REQUIEM

├── Projects

├── Engine

├── Tools

└── Memory Core



"Engine" in this structure means the REQUIEM Engine. External game engines are environments, not parts of the ecosystem.


REQUIEM Ecosystem is the highest organizational level.


---

## Memory Core System


Definition:

The implemented Memory Core: code of its layers, formats and rules.


The Memory Core System is not a project.


Its knowledge is System Knowledge.


---

## Memory Core Instance


Definition:

A single installation of the Memory Core System that serves one or more projects.


An instance contains:

- Memory Core System components;
- configuration;
- System Knowledge;
- Ecosystem Knowledge;
- Shared Knowledge;
- registered projects.


An instance is not a project.


---

## Memory Core Development Project


Definition:

The project in which the Memory Core System is developed.


It contains the development state, milestones, versions and roadmap of Memory Core.


It is a project like any other project (FD-B8).


---

# 4. Project terms


## Project


Definition:

An independent development subject owned by REQUIEM and observed and supported by Memory Core.


Memory Core does not control projects.


A project has:

- stable identity;
- own files;
- own observations;
- own history;
- own knowledge.


Examples:

- REQUIEM Application;
- REQUIEM Mod Pack;
- Memory Core Development Project.


A project is not defined by its folder name.


---

## Project ID


Definition:

A permanent identifier assigned to a project.


Rules:

- must remain stable;
- must not depend on filesystem location;
- must not change after registration.


The format of project IDs is not decided yet (FD open item O5).


---

## Project Kind


Definition:

A classification describing what type of project exists.


Examples:

- application;
- game modification;
- game;
- tool;
- library;
- engine.


"game" is a project kind only for a game developed inside REQUIEM. An external game such as S.T.A.L.K.E.R. 2 is an environment.


---

## Environment


Definition:

An external or supporting system in which a project operates.


REQUIEM does not own environments.


Examples:

- S.T.A.L.K.E.R. 2;
- Unreal Engine;
- operating system;
- framework;
- runtime environment.


An environment is not a project and does not own knowledge (FD-B3, FD-B7).


---

## Environment Reference


Definition:

A link from a project to an environment in which the project operates.


A reference does not transfer ownership.


The identity of the referenced environment (name, version) is Ecosystem Knowledge.


Project-specific usage and modifications of the environment are Project Knowledge of the referencing project (FD-B7).


---

# 5. Development system terms


## Engine


Definition:

A system that provides execution capabilities for a project.


Two cases exist:

- external engine (for example Unreal Engine) — an environment;
- REQUIEM Engine — part of the REQUIEM ecosystem.


Engine is not Memory Core.


Memory Core may observe information from engines but does not control them.


---

## REQUIEM Engine


Definition:

The internal execution system of REQUIEM.


It is different from external engines used by projects.


Its scope and its relation to the engine contracts in requiem-tauri (src/core/contracts/) are not decided (FD open item O6).


---

## Tool


Definition:

A development utility that assists projects or Memory Core.


Examples:

- editors;
- build tools;
- automation utilities.


---

## Adapter


Definition:

A controlled connection layer between an external system and Memory Core.


Examples:

- Engine Adapter;
- Tool Adapter;
- Project Adapter.


Adapters provide information. They may be a proposal source. They do not create trusted knowledge directly.


Adapters are not implemented.


---

# 6. Memory Core process terms


## Observation


Definition:

Collected information about a project state.


Examples:

- files;
- metadata;
- hashes;
- structural facts.


Observation answers:

"What exists?"


---

## Snapshot


Definition:

A recorded state of a project at a specific moment.


A snapshot contains observed information that can be reproduced and verified.


In CP-006 snapshots are created by the scanner (SNAP-NNN).


---

## Fact


Definition:

A verified piece of information derived from observation.


A fact must have:

- source;
- evidence;
- origin observation (a snapshot, or a future adapter observation).


Facts describe reality, not interpretation.


---

## Evidence


Definition:

Verifiable data that supports a fact, a finding or a proposal (for example a file hash, a snapshot ID, a change record entry).


---

## Change


Definition:

A difference detected between two snapshots.


A change is a historical fact.


---

## Change Record


Definition:

A structured description of a detected change (CHG-NNN).


It describes what changed, not why.


The only human content is the review decision and the review note.


---

## Analysis


Definition:

A deterministic interpretation of changes using rules and trusted knowledge.


Analysis produces findings only: classifications, rule matches, warnings and evidence (FD-B1).


Analysis does not create proposals.

Analysis does not modify memory or knowledge.


---

## Finding


Definition:

A result of Analysis: a rule match with its rule identifier, the change record entries it is based on, and evidence.


A finding is not a proposal and not knowledge.

A proposal source may use findings as evidence.


---

## Discovery


Definition:

A future process that inspects facts and produces knowledge proposals.


Discovery never creates trusted knowledge.


Discovery is not implemented.


---

## Context Update


Definition:

The implemented process that transfers approved change records into memory records through a context update proposal (CU-NNN), human review and manual apply (DEC-010, DEC-011).


In DEC-009 and DEC-010, "project memory" means the CP-006 Memory Core storage (database/, context/, README.md). This historical wording is preserved in those records. It does not mean the knowledge of a registered project.


---

## Memory Record


Definition:

A record stored by Memory Core, for example an event, a decision, a checkpoint record or a marked state block.


Every memory record belongs to one ownership level (FD-B4). In CP-006 records of different levels share one storage (REQUIEM_FOUNDATION_DECISIONS.md, section 12).


---

## Change Analysis Flow


Definition:

The implemented CP-006 flow from observation to context update:


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



It is the change flow of FD-B1.


---

## Knowledge Formation Flow


Definition:

The future flow in which knowledge becomes trusted:


Facts, Findings (evidence)

↓

Proposal source (Discovery, adapter, AI assistant, human operator)

↓

Knowledge Proposal

↓

Human Review

↓

Trusted Knowledge



It is the knowledge flow of FD-B1.


The Change Analysis Flow and the Knowledge Formation Flow are separate. They are connected only through evidence (facts and findings) and through Analysis reading knowledge.


---

## Event


Definition:

A record of an important occurrence in database/events.json (EVENT-NNN).


---

## Decision (DEC)


Definition:

A recorded architectural decision (status ACTIVE) in database/decisions.json (DEC-NNN).


Every decision has an ownership level (FD-B4).


---

## Checkpoint


Definition:

A recovery point (DEC-005).


The relation between checkpoints and version records of Memory Core is not decided (FD open item O3).


---

## Provenance


Definition:

The origin of a knowledge element: source, proposal, approver, approval date and evidence.


---

## Revision


Definition:

A numbered version of a knowledge collection. Previous revisions are preserved.


---

# 7. Knowledge terms


## Knowledge


Definition:

Structured understanding about the Memory Core System, the REQUIEM ecosystem, reusable experience or a project.


Knowledge explains meaning, relationships and purpose.


Every knowledge element has exactly one ownership level (FD-B4).


---

## Knowledge Ownership Level


Definition:

The level that owns a knowledge element.


Levels:

- System Knowledge;
- Ecosystem Knowledge;
- Shared Knowledge;
- Project Knowledge.


There is no environment ownership level (FD-B7).


---

## System Knowledge


Definition:

Knowledge about the Memory Core System: architecture rules, system DEC decisions, section 5 of the development protocol (Memory Core rules), formats.


---

## Ecosystem Knowledge


Definition:

Knowledge about REQUIEM as a whole: identity, global principles, terminology, the development protocol except section 5, ecosystem DEC decisions, identity of known environments.


---

## Shared Knowledge


Definition:

Reusable knowledge between projects.


Examples:

- development patterns;
- reusable solutions;
- general experience.


Shared Knowledge must not contain project-specific paths, files or private project decisions.


The term "Global Knowledge" is not used.


---

## Project Knowledge


Definition:

Knowledge belonging to one specific project.


Examples:

- project architecture;
- component relationships;
- project decisions;
- project-specific usage and modifications of referenced environments.


---

## Architecture Knowledge


Definition:

Project Knowledge describing project structure, systems, components and relationships (FD-B5).


Architecture Knowledge is not a copy of files.


---

## Resource Binding


Definition:

A link between a knowledge element and project files.


Resource Binding is Project Knowledge. It may contain project-specific paths.


It is the concept behind the zone paths of the current architecture map prototype (FD-B5).


Its final definition belongs to Knowledge Model v1.


---

## Trusted Knowledge


Definition:

A knowledge element with knowledge status TRUSTED: it passed human review and can be used as a reliable source.


Trusted Knowledge cannot appear automatically.


---

# 8. Proposal terms


## Proposal


Definition:

A suggested change to memory or knowledge waiting for human review.


A proposal contains:

- suggested change;
- evidence;
- source;
- reason.


Proposal sources:

- Discovery (future);
- adapters (future);
- AI assistants;
- human operators.


Analysis is not a proposal source.


Proposal types:

- Context Update Proposal;
- Knowledge Proposal.


---

## Context Update Proposal


Definition:

An implemented proposal (CU-NNN) that changes memory records: the marked snapshot state blocks in README.md and context/REQUIEM_CONTEXT.md, and database/events.json (DEC-011; transitional deviation 2 in REQUIEM_FOUNDATION_DECISIONS.md, section 12).


---

## Knowledge Proposal


Definition:

A proposal that adds, changes or deprecates knowledge elements.


Flow:


Proposal source (Discovery, adapter, AI assistant, human operator)

↓

Knowledge Proposal

↓

Human Review

↓

Trusted Knowledge



Knowledge proposals are not implemented.


---

# 9. Status terms


A status word is always read together with its object type (FD-B2).


## Document statuses


DRAFT — document under development; not project truth.

REVIEW — document complete enough for evaluation; changes require human decision.

APPROVED — document formally accepted as trusted documentation; requires an explicit approval record: approver, date, approved version (REQUIEM_DOCUMENT_REGISTRY.md, section 3).

SUPERSEDED — document replaced by a newer approved document; preserved in history.


---

## Knowledge statuses


PROPOSED — knowledge element suggested, not yet reviewed.

TRUSTED — knowledge element accepted by human review.

DEPRECATED — knowledge element no longer valid; preserved in history.


Knowledge elements do not use APPROVED or SUPERSEDED.


---

## Operational record statuses


Change record (CHG): PENDING_REVIEW, APPROVED, REJECTED.

Context update proposal (CU): PROPOSED, APPROVED, REJECTED, APPLIED, STALE.


These statuses are defined in REQUIEM_CHANGE_RECORD_MODEL.md and REQUIEM_CONTEXT_UPDATE_MODEL.md and remain unchanged.


---

## Implementation State


Definition:

Whether a component described by a document exists in code.


Values:

- not implemented;
- implemented (with component version);
- not applicable (documents that do not describe a component).


Implementation state is not a document status.


---

# 10. Authority terms


## Human Review


Definition:

The process where a person evaluates and decides on:

- change records;
- context update proposals;
- knowledge proposals;
- documents.


Human decision is required before memory changes and before knowledge becomes trusted.


---

# 11. Memory Core principles


The glossary follows these principles:


## Separation

Facts, interpretation and knowledge are different layers.


## Human authority

Important knowledge requires approval.


## Project independence

Memory Core must support multiple projects.


## Reproducibility

Knowledge must be based on verified information.


## Controlled evolution

Memory grows through approved changes.


---

# 12. Future expansion


This glossary will evolve with REQUIEM.


New terms must be added before new architecture layers depend on them.


---

END OF DOCUMENT
