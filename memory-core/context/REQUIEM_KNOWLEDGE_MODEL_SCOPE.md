# REQUIEM KNOWLEDGE MODEL SCOPE

Version: 0.3

Status: DRAFT


---

# 1. Purpose


This document defines the scope and boundaries of Knowledge Model v1.


The purpose is to define what Knowledge Model v1 is responsible for before the full model is created.


Knowledge Model v1 is the next architectural stage after the Memory Core v0.7 Foundation.


This document does not define Knowledge Model v1 itself.


Basis:

- REQUIEM_FOUNDATION_DECISIONS.md v0.4 (FD-B1 … FD-B8);
- REQUIEM_GLOSSARY.md v0.4 (terms);
- REQUIEM_INSTANCE_MODEL.md v0.3;
- REQUIEM_DOCUMENT_REGISTRY.md (document statuses and rules);
- CP-006 architecture (implemented layers and DEC-001 … DEC-018).


---

# 2. Nature of Knowledge Model


Knowledge Model v1 is a logical model.


It defines:

- concepts;
- entities;
- relationships;
- rules for ownership, lifecycle and authority.


It is not a processing layer.

It does not observe, compare, analyze or update anything.


Processes use the concepts of Knowledge Model:

- Analysis may read knowledge (section 4.11);
- Knowledge Proposals change knowledge through human review (section 4.9).


Storage format and schema are out of scope (decision of 2026-09-25).

Knowledge Model v1 does not define files, file formats, schemas, serialization or storage locations.


---

# 3. Position relative to Memory Core flows


Two separate flows exist (FD-B1).


## 3.1 Change Analysis Flow (CP-006, implemented)


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



Knowledge Model v1 does not change this flow.


## 3.2 Knowledge Formation Flow (future)


Facts, Findings (evidence)

↓

Proposal source (Discovery, adapter, AI assistant, human operator)

↓

Knowledge Proposal

↓

Human Review

↓

Trusted Knowledge (knowledge status TRUSTED)



Knowledge Model v1 defines the concepts used in this flow. It does not implement the flow.


## 3.3 Connection between the flows


The flows are connected only in two ways:

- facts and findings can be used as evidence in Knowledge Proposals;
- Analysis can read knowledge (section 4.11).


Analysis never creates or changes knowledge (FD-B1, DEC-015).

Knowledge Proposals never change change records (CHG) or context update proposals (CU).


---

# 4. Knowledge Model v1 responsibilities


Knowledge Model v1 must define the items of this section.


Where approved documents already decide a rule, Knowledge Model v1 must follow it. These rules are listed as constraints.


## 4.1 Facts


Knowledge Model v1 must define how facts are used by knowledge.


Constraints:

- a fact is verified information derived from observation (Glossary);
- a fact has source, evidence, origin observation (a snapshot, or a future adapter observation) and time of observation;
- facts are not knowledge elements: they are verified by observation and hash, not by human review, and have no knowledge status;
- existing CP-006 facts (snapshots SNAP-NNN, change record entries CHG-NNN/k) are referenced, not redefined; their formats remain defined by the layer models (REQUIEM_SNAPSHOT_MODEL.md, REQUIEM_COMPARISON_MODEL.md, REQUIEM_CHANGE_RECORD_MODEL.md).


## 4.2 Evidence


Knowledge Model v1 must define which evidence a knowledge element and a knowledge proposal require.


Constraints:

- evidence is verifiable data that supports a fact, a finding or a proposal (Glossary);
- examples: file hash, snapshot ID, change record entry, analysis finding, a section of an APPROVED document;
- a DRAFT document cannot be evidence for trusted knowledge (REQUIEM_DOCUMENT_REGISTRY.md, rule 2);
- a human decision is not evidence; it is authority and is recorded in provenance (section 4.3).


## 4.3 Provenance


Knowledge Model v1 must define the provenance of every knowledge element.


Constraints:

- provenance records source, proposal, approver, approval date and evidence (Glossary);
- the human review decision is recorded in provenance, not as evidence.


## 4.4 Entities


Knowledge Model v1 must define entity types for each ownership level.


Minimum expected entity types (final list is decided by Knowledge Model v1):

| Ownership level | Entity types |
|---|---|
| Project Knowledge | system, subsystem, component, resource binding (link between a knowledge element and project files), project decision, project-specific usage or modification of an environment |
| Ecosystem Knowledge | environment identity (name, version) |
| Shared Knowledge | pattern, solution, experience |
| System Knowledge | to be decided (section 4.13) |


Constraints:

- environment identity belongs to Ecosystem Knowledge (FD-B7);
- a project references an environment; the reference is a relationship, not an entity (section 4.5);
- an environment is not a project and does not own knowledge (FD-B3, FD-B7);
- project identity follows REQUIEM_INSTANCE_MODEL.md, section 9; projects are registered by human approval (section 15 there); Knowledge Model v1 references projects by this identity and does not redefine it.


## 4.5 Relationships


Knowledge Model v1 must define the relationship vocabulary and relationship rules.


Candidate relationship types (final vocabulary is decided by Knowledge Model v1):

- contains;
- depends_on;
- affects;
- references;
- generated_by.


Constraints:

- a relationship is a knowledge element: it has an owner, a knowledge status and provenance;
- a project may reference an environment identity (FD-B6, FD-B7);
- a project may use Shared Knowledge (FD-B6);
- a reference does not transfer ownership (FD-B6);
- relationships from one project to another project are not defined by Knowledge Model v1 (open item O2);
- "affects" records approved knowledge; it is not a computed impact (impact analysis is out of scope).


Knowledge Model v1 must define which relationship types are allowed inside one ownership level and which across levels.


## 4.6 Identifiers


Knowledge Model v1 must define how knowledge elements, relationships and knowledge proposals are identified.


Constraints:

- identifiers are stable and are not reused;
- identifiers do not depend on file paths or folder names;
- identifiers are unique within their owner;
- the dependency on the project ID format (open item O5) must be stated.


## 4.7 Ownership rules


Knowledge Model v1 must define ownership rules.


Constraints:

- every knowledge element has exactly one ownership level (FD-B4);
- Architecture Knowledge is Project Knowledge and belongs to exactly one project (FD-B5);
- environment identity is Ecosystem Knowledge; project-specific usage and modifications of an environment are Project Knowledge (FD-B7);
- System, Ecosystem and Shared Knowledge contain no project-specific paths;
- one project's knowledge does not become another project's knowledge automatically (REQUIEM_INSTANCE_MODEL.md, section 10);
- Project Knowledge becomes Shared Knowledge only through human review, without project-specific content (FD-B7 rule 4).


## 4.8 Knowledge lifecycle


Knowledge Model v1 must define the lifecycle of knowledge elements and revisions.


Constraints:

- knowledge statuses are PROPOSED → TRUSTED → DEPRECATED (FD-B2);
- knowledge elements do not use APPROVED or SUPERSEDED;
- a knowledge element becomes TRUSTED only through human review, with evidence and provenance;
- DEPRECATED elements are preserved;
- previous revisions are preserved; states cannot silently disappear.


Knowledge Model v1 must define what one knowledge element is and what one revision is.


## 4.9 Proposal lifecycle


Knowledge Model v1 must define the lifecycle of Knowledge Proposals.


Constraints:

- the proposal lifecycle is separate from the knowledge lifecycle;
- a rejected proposal item does not become a knowledge element;
- proposal sources are Discovery, adapters, AI assistants and human operators (FD-B1);
- Analysis is not a proposal source (FD-B1);
- every proposal records its source; proposals from AI assistants are marked as such;
- Knowledge Proposals are separate from context update proposals (CU); CU remains limited by DEC-011.


## 4.10 Approval authority


Knowledge Model v1 must define who performs the human review for each ownership level.


Constraints:

- only a human can make knowledge TRUSTED (Glossary, Trusted Knowledge);
- for Project Knowledge, the project owner is the human responsible for approving the project's knowledge (REQUIEM_INSTANCE_MODEL.md, section 9);
- promotion to Shared Knowledge requires human review (FD-B7 rule 4).


## 4.11 Analysis usage rules


Knowledge Model v1 must define how Analysis may use knowledge.


Constraints:

- Analysis reads knowledge; it never creates or changes knowledge (FD-B1, DEC-015);
- only TRUSTED knowledge is used as trusted context;
- Knowledge Model v1 must state whether PROPOSED knowledge may be shown by Analysis, and how it is marked;
- Knowledge Model v1 must define which knowledge concepts can classify changed files (the role that zones have in the prototype);
- changes to the analyzer are out of scope (section 5).


## 4.12 Replacement and conflict handling


Knowledge Model v1 must define:

- how a knowledge element is replaced (new revision or deprecation);
- how conflicting knowledge proposals are handled;
- how conflicting TRUSTED knowledge elements are handled.


Constraints:

- nothing is overwritten silently;
- history is preserved.


## 4.13 Relation to existing Memory Records


Knowledge Model v1 must define whether existing Memory Records are represented as knowledge elements, referenced by knowledge elements, or remain Memory Records outside the model.


Existing Memory Records:

- DEC-001 … DEC-018 (database/decisions.json);
- database/identity.json;
- database/events.json;
- database/checkpoints.json;
- database/state.json.


Constraints:

- the ownership levels of current records follow FD-B4 and FD-B8;
- existing records are not changed or renumbered by Knowledge Model v1;
- the transitional deviations of REQUIEM_FOUNDATION_DECISIONS.md, section 12, remain until migration is approved.


---

# 5. Out of scope


Knowledge Model v1 does not include:


## Storage format and schema

No files, file formats, schemas, serialization or storage locations (decision of 2026-09-25).


## Implementation

No code architecture or programming implementation.


## Storage migration

Existing storage remains unchanged (REQUIEM_FOUNDATION_DECISIONS.md, sections 11–12).


## CP-006 layer changes

No changes to the scanner, comparator, change reporter, analyzer or context updater, including a new Analysis version and new Context Update operations.


## Impact analysis

Knowledge Model v1 does not compute or predict the impact of changes.


## Discovery systems

Discovery is a future process.


## Automatic knowledge generation

Knowledge is not generated automatically, including by AI. Rules for AI behavior are outside this model. AI assistants are only a marked proposal source (section 4.9).


## Adapter implementation

Adapters are not implemented.


## Shared Knowledge promotion implementation

The promotion rule is decided (FD-B7 rule 4). Its implementation is outside this model.


## Project-to-project relationships

Deferred (open item O2).


---

# 6. Existing documents and data affected


| Item | Registry | Relation to Knowledge Model v1 |
|---|---|---|
| REQUIEM_ARCHITECTURE_KNOWLEDGE_MODEL.md | DOC-013, DRAFT | overlapping concepts of architecture knowledge |
| REQUIEM_ARCHITECTURE_MAP_MODEL.md | DOC-014, DRAFT | overlapping concepts of the architecture map |
| REQUIEM_ARCHITECTURE_MAP_FORMAT.md | DOC-015, DRAFT | concepts overlap; its format part is outside Knowledge Model v1 (section 5) |
| REQUIEM_ARCHITECTURE_MAP_USAGE.md | DOC-016, DRAFT | overlapping rules for use of the map |
| REQUIEM_KNOWLEDGE_FLOW_MODEL.md | DOC-012, DRAFT | overlapping knowledge lifecycle |
| REQUIEM_ANALYSIS_MODEL.md, section 10 | DOC-009, DRAFT | zone format of the prototype, read by analyzer v0.1 |
| analysis/architecture_map.json revision 2 | data record, prototype | content describes the ecosystem and Memory Core; not project knowledge (FD-B5) |


Rules:

1. None of these items is deleted (REQUIEM_DOCUMENT_REGISTRY.md, rule 4).

2. The role of each item is decided together with the approval of Knowledge Model v1, not after it, so that no two approved definitions of the same knowledge exist at the same time.

3. A document becomes SUPERSEDED only when an approved document replaces it (REQUIEM_DOCUMENT_REGISTRY.md, section 3).

4. Knowledge Model v1 does not define a format. Therefore REQUIEM_ANALYSIS_MODEL.md section 10 and the format part of REQUIEM_ARCHITECTURE_MAP_FORMAT.md cannot be replaced by Knowledge Model v1 alone. Their replacement requires a separately approved format specification.

5. REQUIEM_ANALYSIS_MODEL.md section 10 and analysis/architecture_map.json revision 2 stay unchanged and remain in use by analyzer v0.1 until a separately approved change.

6. REQUIEM_MEMORY_ARCHITECTURE.md (DOC-010) and REQUIEM_MEMORY_CORE_MODEL.md (DOC-011) are not affected by this scope; they remain under open item O7.


---

# 7. Architecture Map transition


The current Architecture Map is a prototype (FD-B5).


Knowledge Model v1 must determine whether the Architecture Map:

- becomes part of Knowledge Model;
- becomes a specialized view of project knowledge;
- remains a separate format.


Every option is bounded by:

- FD-B5: an architecture map describes Project Knowledge of exactly one project;
- section 2: Knowledge Model v1 defines concepts only; any map format requires a separate format specification;
- section 6, rule 5: analyzer v0.1 continues to read the current file without change until a separately approved change.


---

# 8. Human authority


Knowledge Model v1 does not create trusted knowledge.


Knowledge becomes TRUSTED only through human review (Glossary, FD-B1).


---

# 9. Development order


Document lifecycle (FD-B2):


Knowledge Model Scope: DRAFT → REVIEW → APPROVED

↓

Knowledge Model v1: DRAFT → REVIEW → APPROVED, together with the decisions of section 6



Knowledge lifecycle (FD-B2):


Knowledge elements are created only through Knowledge Proposals:

PROPOSED → human review → TRUSTED



Storage format, implementation, Analysis changes and migration require separate approved documents. They are not ordered by this scope.


---

# 10. Dependencies and open items


Depends on:

- REQUIEM_FOUNDATION_DECISIONS.md v0.4;
- REQUIEM_GLOSSARY.md v0.4;
- REQUIEM_INSTANCE_MODEL.md v0.3;
- REQUIEM_DOCUMENT_REGISTRY.md.


Open items that affect Knowledge Model v1:

| Item | Effect |
|---|---|
| O2 | project-to-project relationships are excluded |
| O5 | identifiers must state their dependency on the project ID format (section 4.6) |
| O7 | partly addressed by section 6 (DOC-012 … DOC-016); DOC-010 and DOC-011 remain open |


---

# 11. Terms introduced by this document


These terms were introduced by this document and are defined in REQUIEM_GLOSSARY.md v0.4 (REQUIEM_GLOSSARY.md, section 2). The glossary is authoritative for their definitions.


Glossary v0.4 is DRAFT. Approval of this document requires approval of Glossary v0.4.


## Change Analysis Flow

The implemented CP-006 flow from observation to context update (section 3.1). Same as the change flow of FD-B1.


## Knowledge Formation Flow

The future flow from evidence through a Knowledge Proposal and human review to Trusted Knowledge (section 3.2). Same as the knowledge flow of FD-B1.


## Resource Binding

A candidate entity type of Project Knowledge: a link between a knowledge element and project files. It is the concept behind the zone paths of the current prototype. Its final definition belongs to Knowledge Model v1.


---

# 12. Final goal


Knowledge Model v1 should provide a stable foundation for REQUIEM to understand complex multi-project ecosystems while preserving:

- history;
- ownership;
- evidence;
- human control.


END OF DOCUMENT
