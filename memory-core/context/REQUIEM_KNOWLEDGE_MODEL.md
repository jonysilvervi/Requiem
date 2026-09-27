# REQUIEM KNOWLEDGE MODEL

Version: 0.4

Status: DRAFT


Coverage: sections 1–8 (Purpose, Scope compliance, Principles, Knowledge Element definition, Ownership, Evidence and Provenance, Lifecycle, Terms introduced by this document). Section 8 registers only the two terms already used by sections 1–7; it does not yet mirror REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, section 11, in full. Remaining REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, section 4 responsibilities, and this document's own remaining outer sections, are not yet written; see section 2.


---

# 1. Purpose


This document is REQUIEM Knowledge Model v1 (DOC-022).


It defines the logical model REQUIEM Memory Core uses to represent, own and evolve knowledge, across every ownership level, as required by REQUIEM_KNOWLEDGE_MODEL_SCOPE.md v0.3.


Basis:


- REQUIEM_KNOWLEDGE_MODEL_SCOPE.md v0.3 (DOC-021, APPROVED);

- REQUIEM_FOUNDATION_DECISIONS.md v0.4 (DOC-020, APPROVED, FD-B1 … FD-B8);

- REQUIEM_GLOSSARY.md v0.4 (DOC-017, APPROVED);

- REQUIEM_INSTANCE_MODEL.md v0.3 (DOC-019, APPROVED);

- REQUIEM_DOCUMENT_REGISTRY.md v0.7 (DOC-018, DRAFT, not approved — cited here as the current dependency for document rules and statuses, not as part of the approved foundation the entries above belong to).


Like REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, this document is a logical model. It does not define storage, does not implement anything, and does not change CP-006 (REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, section 2; REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, section 5).


This is version 0.4, a corrective revision of version 0.3. It corrects the description of open item O7 in section 2.3 and the source cited for preservation of history in section 3 ("Controlled evolution"), as found by the v0.3 audit. It changes no decision of version 0.3 and adds no new section. Version 0.3 applied the confirmed architectural decision of 2026-09-25 that knowledge status belongs to a Knowledge Element, not to a Revision (section 7.1), and recorded the questions the approved documents do not decide as known issues (section 2.3) instead of resolving them. This document does not yet cover every responsibility REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, section 4, assigns to Knowledge Model v1; section 2 below lists what is covered and what remains.


---

# 2. Scope compliance


This section records how this version of Knowledge Model v1 complies with REQUIEM_KNOWLEDGE_MODEL_SCOPE.md v0.3, and what it does not yet cover.


## 2.1 Boundaries observed


- This document defines concepts, entities, relationships and rules for ownership, lifecycle and authority (REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, section 2). It is not a processing layer: it does not observe, compare, analyze or update anything.

- This document does not define files, file formats, schemas, serialization or storage locations (REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, section 2, decision of 2026-09-25).

- This document does not change the Change Analysis Flow (REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, section 3.1); CP-006 (scanner, comparator, change reporter, analyzer, context updater) is not modified (REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, section 5, "CP-006 layer changes").

- This document does not compute or predict impact (REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, section 5, "Impact analysis").

- This document does not implement Discovery, adapters, or automatic knowledge generation, including by AI (REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, section 5).

- Analysis is not a proposal source and does not create or change knowledge in this document (REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, section 3.3; REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, section 4.9; FD-B1).

- This document does not create trusted knowledge; knowledge becomes TRUSTED only through human review (REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, section 8).


## 2.2 REQUIEM_KNOWLEDGE_MODEL_SCOPE.md section 4 responsibilities covered by this version


| Scope section | Responsibility | Status in v0.3 |
|---|---|---|
| 4.1 | Facts | addressed (section 4, by reference: a Knowledge Element is not a Fact) |
| 4.2 | Evidence | partially addressed (section 6 defines what evidence is and the rules for its use; which evidence a Knowledge Proposal requires is not yet defined) |
| 4.3 | Provenance | addressed (section 6) |
| 4.4 | Entities | not yet addressed |
| 4.5 | Relationships | not yet addressed (section 4 states only that a relationship is a knowledge element, per REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, section 4.5) |
| 4.6 | Identifiers | not yet addressed (section 4 states only that every Knowledge Element has an identifier) |
| 4.7 | Ownership rules | addressed (section 5), including the general cross-project rule (section 5.1) |
| 4.8 | Knowledge lifecycle | addressed (section 7); "what one knowledge element is and what one revision is" addressed in section 4 |
| 4.9 | Proposal lifecycle | not yet addressed |
| 4.10 | Approval authority | not yet addressed |
| 4.11 | Analysis usage rules | not yet addressed |
| 4.12 | Replacement and conflict handling | not yet addressed |
| 4.13 | Relation to existing Memory Records | not yet addressed |


Also not yet written are the sections of this document corresponding to:


- REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, section 2 (Nature of Knowledge Model);

- REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, section 3 (Position relative to Memory Core flows);

- REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, section 5 (Out of scope);

- REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, section 6 (Existing documents and data affected);

- REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, section 7 (Architecture Map transition);

- REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, section 8 (Human authority);

- REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, section 9 (Development order);

- REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, section 10 (Dependencies and open items);

- REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, section 12 (Final goal).


REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, section 11 (Terms introduced by this document), is partly addressed: section 8 of this document registers the two terms sections 1–7 already use; it is not yet the complete list REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, section 11, expects once the remaining responsibilities of REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, section 4, are written.


## 2.3 Open items not touched


FD open items O2, O5 and O7 (REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, section 10) are not resolved by this version:


- O2 (project-to-project relationships) is not touched; section 5 of this document binds ownership to one project only, consistent with REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, section 4.5 ("relationships from one project to another project are not defined by Knowledge Model v1").

- O5 (project ID format) is not touched; section 5 references project identity through REQUIEM_INSTANCE_MODEL.md, section 9, without depending on a specific identifier format.

- O7 (the seven DRAFT architecture documents, REQUIEM_DOCUMENT_REGISTRY.md, section 8.3) is not resolved by this version, and REQUIEM_KNOWLEDGE_MODEL_SCOPE.md addresses it only in part (REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, section 10). The role of DOC-012 … DOC-016, together with the other items listed in REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, section 6, is decided together with the approval of this document, not after it (REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, section 6, rule 2); that approval has not happened yet. DOC-010 and DOC-011 are not affected by REQUIEM_KNOWLEDGE_MODEL_SCOPE.md and remain under open item O7 (REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, section 6, rule 6).


Until this document reaches REVIEW and then APPROVED (REQUIEM_DOCUMENT_REGISTRY.md, section 3), it defines no trusted knowledge and does not supersede REQUIEM_ANALYSIS_MODEL.md section 10, DOC-012 … DOC-016, or analysis/architecture_map.json revision 2 (REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, section 6, rules 1 and 3).


Known issues recorded by this version and not resolved by it. REQUIEM_GLOSSARY.md and REQUIEM_KNOWLEDGE_MODEL_SCOPE.md are not modified by this document.


- Knowledge Element lifecycle boundary. The approved documents do not decide at which point a proposal item becomes a Knowledge Element, and whether and when it produces a Revision. REQUIEM_GLOSSARY.md, section 9, defines PROPOSED as "knowledge element suggested, not yet reviewed", and REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, section 4.11, requires a rule for how Analysis shows PROPOSED knowledge; both presuppose Knowledge Elements that exist before human review. REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, section 4.9, states that "a rejected proposal item does not become a knowledge element", and the knowledge statuses include no rejected state (FD-B2). The same boundary applies to a change proposed for an existing Knowledge Element: whether a Revision exists before human review, and what the knowledge status of the Knowledge Element is while that change is under review, is not decided. The boundary belongs to REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, section 4.9 (Proposal lifecycle), and requires a human decision.

- Status after DEPRECATED. Whether DEPRECATED is terminal for a Knowledge Element, or a DEPRECATED Knowledge Element can receive a new Revision and return to use, is not decided by the approved documents. It belongs to REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, section 4.12 (Replacement and conflict handling), and requires a human decision.


---

# 3. Principles


Knowledge Model v1 is built on the principles already established for REQUIEM Memory Core (REQUIEM_GLOSSARY.md, section 11) and the foundation decisions (REQUIEM_FOUNDATION_DECISIONS.md). Every section of this document, including sections written in later versions, is bound by them.


## Separation


Facts, interpretation (Analysis, findings) and knowledge are different layers (FD-B1). A finding is evidence a proposal may use; a finding never becomes knowledge by itself.


## Human authority


Knowledge becomes TRUSTED only through human review (REQUIEM_GLOSSARY.md, "Trusted Knowledge"; REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, section 8). Knowledge Model v1 does not create trusted knowledge itself.


## Ownership


Every knowledge element has exactly one ownership level (FD-B4). Ownership is never inferred; it is assigned, and does not change as the side effect of an unrelated action.


## Reproducibility


Knowledge is based on verified information. Evidence must be checkable independently of the person who proposed it (section 6).


## Controlled evolution


Memory grows only through approved changes. Nothing is overwritten silently; history, including deprecated material, is preserved (REQUIEM_GLOSSARY.md, section 11, "Controlled evolution"; REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, section 4.8; REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, section 4.12; section 7).


## No silent authority change


A knowledge element, like a document (REQUIEM_DOCUMENT_REGISTRY.md, rule 1), cannot silently change its own ownership, evidence or status. Every change of status is a recorded event with provenance (section 6; section 7).


---

# 4. Knowledge Element definition


## 4.1 What a Knowledge Element is


A Knowledge Element is one unit of Knowledge (REQUIEM_GLOSSARY.md, "Knowledge"): structured understanding about the Memory Core System, the REQUIEM ecosystem, reusable experience, or a project, that explains meaning, relationships and purpose.


A Knowledge Element:


- has exactly one ownership level (FD-B4; section 5);

- has exactly one knowledge status at any point (section 7.1);

- has provenance (section 6);

- may be supported by evidence (section 6);

- has an identifier (section 4.4).


A Knowledge Element may be an entity (something that exists: a system, a component, a pattern, an environment identity, and so on) or a relationship between knowledge elements. REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, section 4.5, states that "a relationship is a knowledge element"; this document treats both alike unless stated otherwise. The catalogue of entity types (REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, section 4.4) and the relationship vocabulary (REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, section 4.5) are defined in a later version of this document.


## 4.2 What a Knowledge Element is not


A Knowledge Element is not a Fact. Facts are verified by observation and hash, not by human review, and have no knowledge status (REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, section 4.1). Existing CP-006 facts — snapshots (SNAP-NNN), change record entries (CHG-NNN/k) — are referenced by Knowledge Elements as evidence (section 6); their formats remain defined by REQUIEM_SNAPSHOT_MODEL.md, REQUIEM_COMPARISON_MODEL.md and REQUIEM_CHANGE_RECORD_MODEL.md, and are not redefined here (REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, section 4.1).


A Knowledge Element is not a Finding. A Finding is a rule match produced by Analysis (REQUIEM_GLOSSARY.md, "Finding"); it may be used as evidence for a Knowledge Proposal, but Analysis does not create or change Knowledge Elements (FD-B1; section 2.1).


A Knowledge Element is not a document. Documents (REQUIEM_DOCUMENT_REGISTRY.md) use DRAFT, REVIEW, APPROVED and SUPERSEDED. Knowledge Elements never use those statuses (FD-B2; section 7).


## 4.3 Knowledge Element and Revision


A Knowledge Element is a persistent identity: something REQUIEM has a continuing understanding of. That understanding changes over time; each change is a Revision.


A Revision is one numbered, evidenced and provenanced statement of a Knowledge Element's content, produced by one Knowledge Proposal (section 6; REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, section 4.9, defined in a later version of this document). At which point of a Knowledge Proposal a Revision is created is not decided (section 2.3).


A Revision has no knowledge status of its own. Knowledge status belongs to the Knowledge Element (section 7.1). A Revision is immutable content history: it is created once and is not modified after creation (section 7.2).


A Knowledge Element's history is the ordered sequence of its Revisions. Earlier Revisions are preserved when a later Revision is created; none is silently replaced (REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, section 4.8: "previous revisions are preserved; states cannot silently disappear"). How a Knowledge Element's current content is replaced by a new Revision, and how conflicts between Revisions are handled, is REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, section 4.12 (Replacement and conflict handling), defined in a later version of this document.


Terminology note: REQUIEM_GLOSSARY.md v0.4 currently defines "Revision" as "a numbered version of a knowledge collection." This document uses "Revision" as defined above — a numbered version of one Knowledge Element — as required by REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, section 4.8 ("Knowledge Model v1 must define what one knowledge element is and what one revision is"). This is a narrower and more specific use of the same word, not a contradiction of the current entry, but the REQUIEM_GLOSSARY.md entry should be updated to this definition when Knowledge Model v1 is approved. REQUIEM_GLOSSARY.md is APPROVED at v0.4 and is not amended by this document.


## 4.4 Identifier


Every Knowledge Element has an identifier, and every Revision of it has an identifier that is stable, unique within its owner, and is never reused (REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, section 4.6: "identifiers are stable and are not reused ... unique within their owner"). The full identifier rules, including the dependency on the project ID format (FD open item O5), are defined in a later version of this document (REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, section 4.6).


---

# 5. Ownership


## 5.1 Rule


Every Knowledge Element has exactly one ownership level (FD-B4). The ownership level of an existing Knowledge Element does not change, and no later Revision changes it. There is no exception: Shared Knowledge created from Project Knowledge (section 5.4) is a new Knowledge Element, not a change of ownership of an existing one.


The four ownership levels are System Knowledge, Ecosystem Knowledge, Shared Knowledge and Project Knowledge. They are defined in REQUIEM_GLOSSARY.md, section 7, and REQUIEM_FOUNDATION_DECISIONS.md, section 6 (FD-B4); this document does not redefine them, only the rules for assigning and using them.


Knowledge belonging to one project does not become another project's knowledge automatically (REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, section 4.7; REQUIEM_INSTANCE_MODEL.md, section 10: "One project's knowledge cannot automatically become another project's knowledge."). This is the general rule; section 5.3 states its instance for a project's usage and modifications of an environment (FD-B7 rule 3). This version defines no path by which one project's Knowledge Element becomes another project's Knowledge Element; the approved documents define none. Creating Shared Knowledge from Project Knowledge (section 5.4) is not such a path: it creates a new Knowledge Element at the Shared Knowledge level and does not transfer ownership of an existing project-owned Knowledge Element. This rule is about ownership; it does not decide whether or how one project's Knowledge Elements may reference another project's — that is REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, section 4.5, and remains FD open item O2 (section 2.3).


## 5.2 Architecture Knowledge


Architecture Knowledge is Project Knowledge. It belongs to exactly one project (FD-B5). It must not be mixed with System Knowledge or Ecosystem Knowledge.


The current architecture map prototype (analysis/architecture_map.json revision 2; REQUIEM_ANALYSIS_MODEL.md, section 10) describes the REQUIEM ecosystem and Memory Core, not the Architecture Knowledge of a project in this sense (FD-B5). It is not affected by this document (section 2.3; REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, section 6, rule 5). Its transition, if any, is REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, section 7 (Architecture Map transition), defined in a later version of this document.


## 5.3 Environments


The identity of an environment (name, version) is Ecosystem Knowledge (FD-B7 rule 5), so every project references the same environment identity.


Project-specific usage and modifications of an environment are Project Knowledge of the project that records them (FD-B7 rule 2). Two projects that reference the same environment keep separate Knowledge about their own usage and modifications of it; one project's Knowledge of an environment does not become another project's Knowledge automatically (FD-B7 rule 3; REQUIEM_INSTANCE_MODEL.md, section 10).


An environment does not own Knowledge; there is no environment ownership level (FD-B7).


## 5.4 No project-specific content outside Project Knowledge


System Knowledge, Ecosystem Knowledge and Shared Knowledge contain no project-specific paths, files or private project decisions (FD-B4; REQUIEM_INSTANCE_MODEL.md, section 11).


Project Knowledge becomes Shared Knowledge only through human review, and only after its project-specific content is removed (FD-B7 rule 4). This is not a change of any Knowledge Element's ownership level (section 5.1): it creates a new Shared Knowledge element with its own provenance recording the Project Knowledge element it was generalized from. It does not change the ownership level of the original Project Knowledge element and does not transfer its ownership. The procedure for this promotion is outside this model (REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, section 5, "Shared Knowledge promotion implementation").


## 5.5 Project identity


Project Knowledge is scoped to one project, identified as REQUIEM_INSTANCE_MODEL.md, section 9, defines project identity. This document references that identity and does not redefine it. The format of the project identifier is not decided (FD open item O5), and is not required to define the ownership rules of this section.


---

# 6. Evidence and Provenance


## 6.1 Evidence


Evidence is verifiable data that supports a Fact, a Finding or a Proposal (REQUIEM_GLOSSARY.md, "Evidence"). Examples: a file hash, a snapshot ID, a change record entry, an Analysis finding, a section of an APPROVED document (REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, section 4.2).


Rules:


- a DRAFT document cannot serve as evidence when a Knowledge Element becomes TRUSTED (REQUIEM_DOCUMENT_REGISTRY.md, rule 2; REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, section 4.2);

- a human decision is not evidence; it is authority, and is recorded in Provenance, not in the evidence of a Knowledge Element (section 6.2; REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, section 4.2);

- evidence is referenced, not copied: a Knowledge Element cites the Fact, Finding or document it relies on, rather than restating its content (section 4.2; REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, section 4.1: "existing CP-006 facts ... are referenced, not redefined").


## 6.2 Provenance


Every Knowledge Element, and every Revision of it, has Provenance: the origin of that Revision (REQUIEM_GLOSSARY.md, "Provenance"; REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, section 4.3).


Provenance records:


- source — where the proposed content came from;

- proposal — the Knowledge Proposal that produced this Revision (REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, section 4.9, defined in a later version of this document);

- approver — the human who reviewed it;

- approval date;

- evidence — the evidence (section 6.1) the Revision relies on.


The human review decision itself is recorded in Provenance, not as evidence (REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, section 4.3). Provenance is what carries human authority into a Knowledge Element; evidence is what can be checked independently of that authority (section 3, "Reproducibility").


Approver and approval date are recorded at human review. Which Provenance entries exist before human review depends on the Knowledge Element lifecycle boundary, which is not decided by this version (section 2.3; REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, section 4.9). A rejected proposal item does not become a Knowledge Element (REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, section 4.9: "a rejected proposal item does not become a knowledge element").


---

# 7. Lifecycle


## 7.1 Knowledge status


Knowledge status belongs to a Knowledge Element (FD-B2; REQUIEM_GLOSSARY.md, "Trusted Knowledge"; REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, section 4.8).


A Revision does not have an independent knowledge status (section 4.3).


Knowledge statuses (FD-B2; REQUIEM_GLOSSARY.md, section 9):


PROPOSED → TRUSTED → DEPRECATED


- PROPOSED — a Knowledge Element suggested, not yet reviewed (REQUIEM_GLOSSARY.md, section 9). At which point a proposal item becomes a PROPOSED Knowledge Element is not decided (section 2.3).

- TRUSTED — a Knowledge Element accepted by human review; it passed human review and can be used as a reliable source (REQUIEM_GLOSSARY.md, "Trusted Knowledge").

- DEPRECATED — a Knowledge Element no longer valid; preserved in history, not removed.


Knowledge Elements and their Revisions do not use APPROVED or SUPERSEDED. Those are document statuses only (FD-B2; REQUIEM_DOCUMENT_REGISTRY.md, section 3). A status word is always read together with its object type (FD-B2).


## 7.2 Transition rules and Revision lifecycle


Knowledge status of a Knowledge Element:


- The point at which a proposal item becomes a Knowledge Element with status PROPOSED is not decided by this version (section 2.3; REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, section 4.9).

- A Knowledge Element becomes TRUSTED only through human review, with evidence and Provenance complete (section 6.2; REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, section 4.8; REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, section 8). Only a human can make a Knowledge Element TRUSTED (REQUIEM_GLOSSARY.md, "Trusted Knowledge").

- A rejected proposal item does not become a Knowledge Element (REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, section 4.9: "a rejected proposal item does not become a knowledge element").

- A TRUSTED Knowledge Element becomes DEPRECATED only through an explicit, provenanced decision. Reaching DEPRECATED does not remove the Knowledge Element or its Revisions (REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, section 4.8: "DEPRECATED elements are preserved").

- Whether DEPRECATED is terminal for a Knowledge Element is not decided by this version (section 2.3; REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, section 4.12).


Revision lifecycle (REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, section 4.8):


- A Revision is an immutable content revision of a Knowledge Element (section 4.3).

- A Revision is created once. A created Revision is preserved and is not modified.

- Previous Revisions remain available as historical records (REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, section 4.8: "previous revisions are preserved").

- A Revision has no knowledge status of its own (section 7.1).

- At which point of a Knowledge Proposal a Revision is created is not decided by this version (section 2.3; REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, section 4.9).


## 7.3 Preservation


Previous Revisions are preserved when a Knowledge Element changes, and the knowledge status of a Knowledge Element cannot silently disappear or be overwritten (REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, section 4.8). How a Knowledge Element's current content is replaced by a new Revision, how that affects the knowledge status of the Knowledge Element, and how conflicting Knowledge Proposals and conflicting TRUSTED Knowledge Elements are handled, is REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, section 4.12 (Replacement and conflict handling), defined in a later version of this document.


## 7.4 Use of status


Analysis reads Knowledge; it never creates or changes it (FD-B1; DEC-015). Which knowledge statuses Analysis may show, and how PROPOSED Knowledge is marked when shown, is REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, section 4.11 (Analysis usage rules), defined in a later version of this document.


---

# 8. Terms introduced by this document


These terms are used by sections 1–7 of this document and have no REQUIEM_GLOSSARY.md v0.4 entry that matches their meaning here. Registering them here does not change REQUIEM_GLOSSARY.md; no Glossary edit is made by this document. Following the precedent of REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, section 11, and REQUIEM_GLOSSARY.md version 0.4, REQUIEM_GLOSSARY.md is expected to be updated for these terms before this document can be APPROVED.


This section is not the complete term list REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, section 11, expects of a finished Knowledge Model v1: the remaining responsibilities of REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, section 4 (not yet written, section 2.2), are likely to introduce further terms, for example an entity type catalogue (REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, section 4.4) or a relationship vocabulary (REQUIEM_KNOWLEDGE_MODEL_SCOPE.md, section 4.5). This section registers only the two terms sections 1–7 already use.


## Knowledge Element


One unit of Knowledge (REQUIEM_GLOSSARY.md, "Knowledge"), defined in section 4.1: has exactly one ownership level, exactly one knowledge status at any point, provenance, optional evidence, and an identifier; may be an entity or a relationship.


REQUIEM_GLOSSARY.md has no entry for this term. It is new.


## Revision


One numbered, evidenced and provenanced statement of a Knowledge Element's content, created once and not modified, with no knowledge status of its own, defined in section 4.3.


REQUIEM_GLOSSARY.md v0.4 already has a "Revision" entry: "a numbered version of a knowledge collection." This document uses the same word for a narrower concept — a version of one Knowledge Element, not of a collection (section 4.3, "Terminology note"). A distinct name such as "Element Revision" was considered, to avoid registering two meanings under one word, but was not adopted for this document: sections 1–7 consistently use "Revision" for this narrower meaning, and introducing a second name in this section alone would itself be the kind of terminology inconsistency this section exists to prevent. REQUIEM_GLOSSARY.md's existing "Revision" entry needs to be updated to the definition in section 4.3, not given a second, differently-named entry.


---

END OF v0.4 — PARTIAL (sections 1–8 of Knowledge Model v1; see section 2.2 for what remains)
