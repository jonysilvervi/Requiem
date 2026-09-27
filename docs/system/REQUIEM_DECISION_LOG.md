# REQUIEM DECISION LOG

Version: 1.1 Draft

Document Type:
Architecture Decision Record

Purpose:
Record important decisions made during REQUIEM development and preserve the reasoning behind them.

---

# 1. PURPOSE

The Decision Log stores important architectural and project decisions.

The goal is to preserve not only what exists, but why it exists.

A system without recorded decisions loses context over time.

---

# DECISION #001

## Topic

Documentation as the permanent project memory.

---

## Decision

REQUIEM documentation is considered the primary source of project continuity.

Chat history, individual AI sessions, and temporary conversations are not considered reliable long-term storage.

---

## Reason

AI sessions can disappear, change, or become unavailable.

The project must remain understandable independently from previous conversations.

---

## Impact

All important architectural decisions, states, and workflows should be preserved inside REQUIEM documentation.

---

# DECISION #002

## Topic

AI responsibility separation.

---

## Decision

REQUIEM uses separated AI roles:

GPT:
Architect.

Claude:
Executor.

Gemini:
Support Intelligence.

---

## Reason

Different AI systems have different strengths.

A clear responsibility model prevents conflicting decisions and uncontrolled workflows.

---

## Impact

AI systems cooperate through defined roles instead of competing responsibilities.

---

# DECISION #003

## Topic

GPT architectural authority.

---

## Decision

GPT is responsible for final evaluation of significant architectural changes.

---

## Reason

The project requires a single architectural direction.

Supporting AI systems may provide analysis and suggestions, but do not replace architectural decisions.

---

## Impact

Major changes require architectural review.

---

# DECISION #004

## Topic

Claude implementation authority.

---

## Decision

Claude operates as the implementation executor.

Claude creates and modifies systems according to approved requirements.

---

## Reason

Implementation and architecture should remain separate responsibilities.

---

## Impact

Claude focuses on execution quality while preserving architectural boundaries.

---

# DECISION #005

## Topic

Gemini role limitation.

---

## Decision

Gemini operates as Support Intelligence.

Gemini provides:

- documentation analysis;
- research;
- visual review;
- context support.

Gemini does not independently make architectural decisions.

---

## Reason

Support analysis and final decisions require different responsibilities.

---

## Impact

Gemini can identify risks and inconsistencies while GPT maintains architectural control.

---

# DECISION #006

## Topic

Automation philosophy.

---

## Decision

REQUIEM automation should automate awareness, not every action.

---

## Reason

Excessive automation creates unnecessary complexity and workflow overhead.

---

## Impact

AI involvement depends on change significance.

Small changes should remain lightweight.

Important changes receive deeper analysis.

---

# DECISION #007

## Topic

Automation is not a replacement for architecture.

---

## Decision

Automation systems may observe, analyze, and suggest.

They do not independently define project direction.

---

## Reason

Long-term system integrity requires controlled architectural decisions.

---

## Impact

Future automation must preserve human and architectural oversight.

---

# DECISION #008

## Topic

Repository as the single source of truth.

---

## Decision

All REQUIEM documentation lives in the GitHub repository jonysilvervi/Requiem.

Documents are no longer passed between AI sessions as archives.

Changes are made as commits. The human owner approves changes by merging them.

---

## Reason

Archives passed between chats were lost, duplicated and went out of date.

A repository keeps one current version, a full history of every change, and is readable by every AI role.

---

## Impact

Every AI session starts from the repository (README.md, then docs/system/REQUIEM_ACTIVE_SESSION.md).

Memory Core documents are stored under memory-core/. Ecosystem documents are stored under docs/.

---

# DECISION #009

## Topic

Memory Core development paused.

---

## Decision

Memory Core development is paused since 2026-09-27.

The last document in progress, REQUIEM_KNOWLEDGE_MODEL.md, stays at version 0.5 (DRAFT) with a recorded resume point.

The implemented Memory Core layers (checkpoint CP-006) remain usable as they are.

---

## Reason

Project continuity, the main purpose of Memory Core, is now provided by the repository and the documentation.

The remaining Memory Core work (Knowledge Model completion, storage format, migration, AI connection) is large and does not block current development.

---

## Impact

No new Memory Core work starts without an explicit request of the human owner.

The resume point is recorded at the top of memory-core/context/REQUIEM_KNOWLEDGE_MODEL.md.

---

# DECISION #010

## Topic

Execution Engine (PowerShell) and architecture documentation frozen.

---

## Decision

The Execution Engine (PowerShell) remains FROZEN.

New architecture documentation is frozen: no new architecture documents are started until the human owner decides otherwise.

Documentation maintenance continues: REQUIEM_ACTIVE_SESSION.md is updated at the end of every work session; the Decision Log and Changelog are updated when a decision is made or a milestone is reached.

---

## Reason

Active work moves to the Visual Core. Frozen areas keep their current state and do not change underneath it.

---

## Impact

Work on frozen areas requires an explicit decision of the human owner.

---

# DECISION #011

## Topic

Active work stream: REQUIEM Visual Core.

---

## Decision

The active work stream is the REQUIEM Visual Core — the visual environment of the ecosystem.

The Phase 1 restrictions on visual work are lifted for the Visual Core:

- REQUIEM_PHASE_1_IMPLEMENTATION_PLAN_v0.2.md, section 10 (UI polishing, glass effects, dashboards, terminal interface);
- REQUIEM_PHASE_1_CORE_SKELETON_SPEC_v0.3.md, section 15 (full Visual Core UI);
- REQUIEM_CURRENT_STATE_SNAPSHOT.md, section 13 (dashboard cards).

The architecture boundaries remain in force:

- the Visual Core owns presentation only; it does not execute system actions, does not modify game files, MO2 or other external environments, and does not contain environment-specific logic (REQUIEM_PHASE_1_CORE_SKELETON_SPEC_v0.3.md, sections 3 and 7);
- the interface must not contain fake buttons pretending to control systems, or fake monitoring systems (REQUIEM_CURRENT_STATE_SNAPSHOT.md, sections 4 and 13);
- intelligence is not a chat widget (REQUIEM_PHASE_1_CORE_SKELETON_SPEC_v0.3.md, section 4).

---

## Reason

The Visual Core is the owner's priority. The Execution Engine is frozen, and project continuity is secured by the repository.

---

## Impact

Visual tasks are reviewed against the architecture boundaries above, not against the Phase 1 visual restrictions.

---

# DECISION #012

## Topic

Phase 1 stays open.

---

## Decision

Phase 1 (Core Skeleton) is not closed, although its success criteria are met in code (docs/app/REQUIEM_CURRENT_STATE_SNAPSHOT.md, section 9).

The foundation is polished to real quality first. Phase 1 is closed by a separate decision of the human owner.

---

## Reason

The owner's standard: everything that can be brought to real quality is brought to it before the phase is closed.

---

## Impact

Visual Core work (Decision #011) happens inside Phase 1.

---

# FUTURE DECISIONS

Future important decisions should be added using this format:

## Topic

---

## Decision

---

## Reason

---

## Impact

---

# END OF DECISION LOG