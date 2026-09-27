# REQUIEM DOCUMENT REGISTRY

Version: 0.7

Status: DRAFT


Version 0.7 registers DOC-022 (section 8.6) and records the current versions of DOC-004 (0.6) and DOC-022 (0.5). This is a new registration under rule 5, not administrative metadata under rule 10, so version 0.7 requires human approval (rule 8) before this registry returns to APPROVED status. The approval records and approved status of DOC-017 … DOC-021 (sections 8.4, 8.5, 8.6) are unaffected: they describe those documents' own approval, not this registry's.


---

# 1. Purpose


REQUIEM Document Registry defines the official document structure inside the REQUIEM ecosystem.


The purpose of this registry is to track:

- document ownership;
- document purpose;
- document status;
- implementation state;
- authority level;
- knowledge ownership level;
- relationship between documents.


The registry prevents undocumented or conflicting knowledge sources.


Location of this registry:

context/REQUIEM_DOCUMENT_REGISTRY.md


Terms are defined in REQUIEM_GLOSSARY.md. Decisions FD-B1 … FD-B8 are defined in REQUIEM_FOUNDATION_DECISIONS.md.


---

# 2. Core principle


A document does not automatically represent truth.


Every document has:

- purpose;
- owner;
- status;
- implementation state;
- authority level.


Only APPROVED documents may define trusted architecture or system rules.


---

# 3. Document statuses


Document statuses follow FD-B2.


## DRAFT


Document is under development.


Rules:

- can contain proposals;
- can contain unfinished ideas;
- cannot be used as trusted knowledge.


## REVIEW


Document is being evaluated.


Rules:

- content is complete enough for review;
- changes require human decision.


## APPROVED


Document is formally accepted as trusted documentation.


Rules:

- requires an explicit approval record: approver, date, approved version;
- synchronization, inclusion in a checkpoint or implementation of the described component is not approval;
- approval applies to the approved version only; a later version is DRAFT until it is approved;
- can define architecture decisions;
- can be referenced by other systems.


## SUPERSEDED


Document was replaced by a newer approved document.


Historical information remains preserved.


Knowledge statuses (PROPOSED, TRUSTED, DEPRECATED) are not document statuses.


---

# 4. Implementation state


Implementation state is a separate property, not a status (FD-B2).


Values:

- not implemented;
- implemented (with component version);
- not applicable (documents that do not describe a component).


---

# 5. Authority levels


## Level 0 — Informational


Documents describing ideas, explanations or history.

Do not define system rules.


## Level 1 — Model


Documents describing architecture concepts.

Models define structure but require approval before becoming operational rules.


## Level 2 — Decision


Documents and records containing architectural decisions.

Approved decision documents and recorded decisions (status ACTIVE) define what must be followed.


## Level 3 — Operational


Documents directly describing implemented behavior or binding procedures.


Models of implemented layers are Level 3.


---

# 6. Document categories


Categories describe what a document is. Authority levels describe how binding it is.


- Architecture Document — describes system structure.
- Model Document — describes concepts, formats and behavior.
- Decision Document — records decisions.
- Protocol Document — describes development rules and procedures.
- Reference Document — provides overviews, summaries, terminology or history.


---

# 7. Registry structure


Each registered document contains:


Identity:

- document name;
- unique identifier (DOC-NNN);
- version.


Purpose:

- why the document exists.


Authority:

- authority level;
- status;
- implementation state;
- knowledge ownership level (FD-B4).


Relations:

- depends on;
- referenced by.


History:

- approval record (approver, date, approved version), or "none";
- synchronizations and checkpoints;
- superseded versions.


Owner of every document registered below: the human maintainer of REQUIEM.


Creation dates are not recorded in the documents themselves.


---

# 8. Registered documents


## 8.1 Memory Core overview and history


| ID | Document | Version | Category | Level | Status | Implementation | Knowledge level | Approval record | History |
|---|---|---|---|---|---|---|---|---|---|
| DOC-001 | README.md | 0.5 | Reference | 3 | DRAFT | not applicable | System (contains a REQUIEM Application snapshot state block, see FD section 12) | none | synchronized at CP-006 |
| DOC-002 | CHANGELOG.md | 0.5 | Reference | 0 | DRAFT | not applicable | Memory Core Development Project | none | synchronized at CP-006 |
| DOC-003 | context/REQUIEM_CONTEXT.md | 0.6 | Reference | 0 | DRAFT | not applicable | mixed: Ecosystem, System, Memory Core Development Project (FD section 12) | none | synchronized at CP-006 |
| DOC-004 | protocols/REQUIEM_DEVELOPMENT_PROTOCOL.md | 0.6 | Protocol | 3 | DRAFT | not applicable | Ecosystem; section 5: System | none | synchronized at CP-006; 0.6: section 7 records the pause of Memory Core development (2026-09-27) |


REQUIEM_CONTEXT.md summarizes rules defined by DEC records and the protocol. It does not define rules itself (Level 0).


## 8.2 Models of implemented layers


| ID | Document | Version | Category | Level | Status | Implementation | Knowledge level | Approval record | History |
|---|---|---|---|---|---|---|---|---|---|
| DOC-005 | context/REQUIEM_SNAPSHOT_MODEL.md | 0.4 | Model | 3 | DRAFT | implemented (scanner v0.2, snapshots v0.1) | System | none | created for CP-003; synchronized at CP-004, CP-006 |
| DOC-006 | context/REQUIEM_COMPARISON_MODEL.md | 0.2 | Model | 3 | DRAFT | implemented (comparator v0.1) | System | none | created for CP-004; synchronized at CP-006 |
| DOC-007 | context/REQUIEM_CHANGE_RECORD_MODEL.md | 0.2 | Model | 3 | DRAFT | implemented (change_reporter v0.1) | System | none | created for CP-005; synchronized at CP-006 |
| DOC-008 | context/REQUIEM_CONTEXT_UPDATE_MODEL.md | 0.1 | Model | 3 | DRAFT | implemented (context_updater v0.1) | System | none | created for CP-005 |
| DOC-009 | context/REQUIEM_ANALYSIS_MODEL.md | 0.2 | Model | 3 | DRAFT | implemented (analyzer v0.1) | System | version 0.1: approved by the human maintainer, 2026-09-24; version 0.2: none | 0.2 synchronized at CP-006 (status line, DEC references) |


DOC-009: version 0.1 was approved. Version 0.2 changed the status line and added DEC references during the CP-006 synchronization. Version 0.2 is not approved yet (section 3, APPROVED rules).


REQUIEM_ANALYSIS_MODEL.md section 10 (architecture map zone format) is the format of the current prototype (FD-B5). It is expected to be superseded by Knowledge Model v1.


## 8.3 Architecture documents (DRAFT, conflicts recorded)


| ID | Document | Version | Category | Level | Status | Implementation | Knowledge level |
|---|---|---|---|---|---|---|---|
| DOC-010 | context/REQUIEM_MEMORY_ARCHITECTURE.md | 0.2 | Architecture | 1 | DRAFT | not implemented | System |
| DOC-011 | context/REQUIEM_MEMORY_CORE_MODEL.md | 0.1 | Model | 1 | DRAFT | not implemented | System |
| DOC-012 | context/REQUIEM_KNOWLEDGE_FLOW_MODEL.md | 0.1 | Model | 1 | DRAFT | not implemented | System |
| DOC-013 | context/REQUIEM_ARCHITECTURE_KNOWLEDGE_MODEL.md | 0.1 | Model | 1 | DRAFT | not implemented | System |
| DOC-014 | context/REQUIEM_ARCHITECTURE_MAP_MODEL.md | 0.1 | Model | 1 | DRAFT | not implemented | System |
| DOC-015 | context/REQUIEM_ARCHITECTURE_MAP_FORMAT.md | 0.1 | Model | 1 | DRAFT | not implemented | System |
| DOC-016 | context/REQUIEM_ARCHITECTURE_MAP_USAGE.md | 0.1 | Model | 1 | DRAFT | not implemented | System |


Recorded conflicts (resolution: FD open item O7):

| ID | Conflict |
|---|---|
| DOC-010 | Analysis answers "What could this change affect?" (FD-B1, DEC-015); snapshots placed in history/ (actual: database/snapshots/); Architecture Knowledge shown as a processing layer. |
| DOC-011 | "STALKER 2 is a project" (FD-B3); "Documentation" added to the ecosystem structure. |
| DOC-012 | Analysis "evaluates changes", "possible impact", "produces suggestions" (FD-B1); Context Update stores "approved knowledge" (DEC-011). |
| DOC-013 | Hierarchy starts at REQUIEM inside project knowledge (FD-B4); "STALKER 2: Project A" (FD-B3); Analysis results as source of "impact information" (FD-B1). |
| DOC-014 | Analysis shown as producing Architecture Knowledge; Architecture Map shown as a pipeline stage (FD-B1, FD-B5). |
| DOC-015 | Knowledge statuses DRAFT → REVIEW → APPROVED (FD-B2); "Project: STALKER 2" (FD-B3); format differs from DOC-009 section 10 and from the current file. |
| DOC-016 | Analysis used to "understand possible impact" (FD-B1); Architecture Map shown as a pipeline stage; STALKER 2 as project (FD-B3). |


These documents keep status DRAFT until the conflicts are resolved.


## 8.4 v0.7 foundation documents


| ID | Document | Version | Category | Level | Status | Implementation | Knowledge level | Approval record |
|---|---|---|---|---|---|---|---|---|
| DOC-017 | context/REQUIEM_GLOSSARY.md | 0.4 | Reference | 1 | APPROVED | not applicable | Ecosystem | version 0.3: approved by the human maintainer, 2026-09-24; version 0.4: approved by the human maintainer, 2026-09-25 |
| DOC-018 | context/REQUIEM_DOCUMENT_REGISTRY.md | 0.6 | Reference | 1 | APPROVED | not applicable | Ecosystem | version 0.4: approved by the human maintainer, 2026-09-24; version 0.5: not approved separately, contained in 0.6; version 0.6: approved by the human maintainer, 2026-09-25 |
| DOC-019 | context/REQUIEM_INSTANCE_MODEL.md | 0.3 | Model | 1 | APPROVED | not implemented | System | version 0.3: approved by the human maintainer, 2026-09-24 |
| DOC-020 | context/REQUIEM_FOUNDATION_DECISIONS.md | 0.4 | Decision | 2 | APPROVED | not applicable | Ecosystem and System | version 0.4: approved by the human maintainer, 2026-09-24 |


Approved as the v0.7 Foundation on 2026-09-24 by the human maintainer: DOC-017 v0.3, DOC-018 v0.4, DOC-019 v0.3, DOC-020 v0.4.


DOC-017 version 0.4 adds the terms Change Analysis Flow, Knowledge Formation Flow and Resource Binding, introduced by DOC-021. Version 0.4 was approved on 2026-09-25.


DOC-018 version 0.5 added the approval records of this section and section 8.5. Version 0.6 adds rule 10, registers DOC-021 and records DOC-017 version 0.4. Rule 10 changed the rules of this registry, so version 0.6 required approval. Version 0.6 was approved on 2026-09-25. Rule 10 applies from that approval; the changes of version 0.5 are administrative metadata under rule 10.


Approval records of 2026-09-25 were added to version 0.6 as administrative metadata under rule 10. They do not change the meaning, authority or rules of this registry.


DOC-020 is an approved architectural decision document. Its decisions FD-B1 … FD-B8 are not DEC records. Required decisions may now be promoted into DEC records (DOC-020, section 2, open item O1).


Relations:

- DOC-017, DOC-018, DOC-019 depend on DOC-020 (decisions FD-B1 … FD-B8);
- DOC-020 depends on DOC-017 (terms);
- Knowledge Model v1 will depend on DOC-017 … DOC-021.


## 8.5 Current approval state


Approved documents (current version approved):

- DOC-017 REQUIEM_GLOSSARY.md v0.4;
- DOC-018 REQUIEM_DOCUMENT_REGISTRY.md v0.6;
- DOC-019 REQUIEM_INSTANCE_MODEL.md v0.3;
- DOC-020 REQUIEM_FOUNDATION_DECISIONS.md v0.4;
- DOC-021 REQUIEM_KNOWLEDGE_MODEL_SCOPE.md v0.3.


All other registered documents (DOC-001 … DOC-016) are DRAFT.


PROTOCOL section 1 names "approved documentation" as a source of truth. This source now consists of the approved versions listed above. The other sources named there — project files and confirmed decisions — are not changed by this registry. DEC records keep their own status in database/decisions.json.


Status lines inside the approved files DOC-017 v0.4, DOC-019 v0.3, DOC-020 v0.4 and DOC-021 v0.3 read "DRAFT", and DOC-020 section 2 calls itself a DRAFT document. These texts were written before approval. The files were not changed after approval, so that the approved versions stay identical. This registry records the current status.


The status line of this registry was changed to APPROVED as administrative metadata under rule 10.


Approved files are identified by SHA-256 (as delivered for approval):

| Document | Version | Approved | SHA-256 |
|---|---|---|---|
| REQUIEM_FOUNDATION_DECISIONS.md | 0.4 | 2026-09-24 | c736961f2e185700fc011f20a34d80288eceba99dbc4b2c8841ed92de4129fee |
| REQUIEM_GLOSSARY.md | 0.3 | 2026-09-24 | dc7f90ff6b87f93caa2c68235946e406eaba36aa6d4ba0ed29b7f6bec4fdbd6f |
| REQUIEM_INSTANCE_MODEL.md | 0.3 | 2026-09-24 | 69ee18c69abee3295f31608c3fee06f5f9d0473a07c6654039d5686cb71e1e47 |
| REQUIEM_DOCUMENT_REGISTRY.md | 0.4 | 2026-09-24 | 01c47cd7da340885f563b12d079ccbab5f3ad62a5e0b0bbb4d51dc4eba92838f |
| REQUIEM_GLOSSARY.md | 0.4 | 2026-09-25 | 87b6cba9a711b9c7ab7d4adbbb84c2e2116188f4c8569d8afb9c9fa1ea4bd9d1 |
| REQUIEM_DOCUMENT_REGISTRY.md | 0.6 | 2026-09-25 | 28837d15d7e24321d65da9cf39ab90cc53cd40576069709591b4021fab30fe51 |
| REQUIEM_KNOWLEDGE_MODEL_SCOPE.md | 0.3 | 2026-09-25 | 779858338d30ea63a107015f4b618eb1baba79be2809c0afb12cb3c2f692428b |


The registry file with these approval records differs from the approved version 0.6 (SHA-256 above) only by administrative metadata under rule 10.


## 8.6 Knowledge Model documents


| ID | Document | Version | Category | Level | Status | Implementation | Knowledge level | Approval record |
|---|---|---|---|---|---|---|---|---|
| DOC-021 | context/REQUIEM_KNOWLEDGE_MODEL_SCOPE.md | 0.3 | Model | 1 | APPROVED | not implemented | System | version 0.3: approved by the human maintainer, 2026-09-25 |
| DOC-022 | context/REQUIEM_KNOWLEDGE_MODEL.md | 0.5 | Model | 1 | DRAFT | not implemented | System | none |


Relations:

- DOC-021 depends on DOC-017 … DOC-020;
- DOC-021 introduces the terms Change Analysis Flow, Knowledge Formation Flow and Resource Binding, added to DOC-017 version 0.4;
- DOC-022 depends on DOC-017 … DOC-021.


DOC-022 is REQUIEM_KNOWLEDGE_MODEL.md, the document that will define Knowledge Model v1 (REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, section 9: "Knowledge Model v1: DRAFT → REVIEW → APPROVED, together with the decisions of section 6").


Work on DOC-022 is paused since 2026-09-27 at version 0.5, by decision of the human maintainer. Pausing does not change its status; the resume point is at the top of the document.


---

# 9. Registered data records


Data files that carry authority are registered by ownership level (FD-B4, FD-B8). They are not documents.


| File | Content | Authority level | Knowledge level |
|---|---|---|---|
| database/identity.json | REQUIEM identity, current supported environment | 2 | Ecosystem |
| database/decisions.json | DEC-001 … DEC-018 | 2 | DEC-001 … DEC-003: Ecosystem; DEC-005 … DEC-018: System |
| database/state.json | development state | 0 | Memory Core Development Project |
| database/events.json | milestones and one REQUIEM Application change event (EVENT-006) | 0 | mixed (FD section 12) |
| database/checkpoints.json | CP-001 … CP-006 | 0 | Memory Core Development Project |
| analysis/analysis_rules.json | analysis categories and signals | 3 | System |
| analysis/architecture_map.json | revision 2, DRAFT, prototype | 0 | not project knowledge (FD-B5) |


Reports outside the checkpoint (REQUIEM_MEMORY_CORE_AUDIT.md, REQUIEM_MEMORY_CORE_ROADMAP_v0.7.md) are Level 0 and are registered when they are stored in the instance.


---

# 10. Document authority rules


The following rules apply:


1. Documents cannot silently change their own authority.

2. DRAFT documents cannot create trusted knowledge.

3. APPROVED documents require controlled updates.

4. SUPERSEDED documents remain in history.

5. New architecture concepts and new documents require registration.

6. Status and implementation state are recorded separately.

7. A document with recorded conflicts keeps status DRAFT until the conflicts are resolved.

8. Changes of this registry require human review.

9. APPROVED requires an explicit approval record. A document without an approval record is DRAFT.

10. Approval records (approver, date, approved version, SHA-256 of the approved file) and the status entries that follow from them are administrative metadata. Recording them does not require re-approval of this registry, unless the change alters the meaning, authority or rules of this registry. This rule applies from the approval of the first registry version that contains it.


---

# 11. Relationship with Memory Core


Document Registry itself is knowledge about knowledge.


It allows Memory Core to understand:

- which documents exist;
- which documents are trusted;
- which documents require review.


---

# 12. Future development


Future versions may include:

- automatic document validation;
- dependency graph;
- conflict detection;
- version synchronization.


---

END OF DOCUMENT
