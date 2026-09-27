# REQUIEM AI WORKFLOW

Version: 1.1 Draft

Document Type:
AI Collaboration Workflow

Purpose:
Define how different AI systems participate in REQUIEM development.

---

# 1. GENERAL PRINCIPLE

AI systems working with REQUIEM do not replace engineering roles.

They operate inside a defined workflow.

The architecture belongs to the Architect role.

Implementation belongs to the Executor role.

---

# 2. ROLE DISTRIBUTION

## GPT — ARCHITECT

Primary responsibility:

Maintain the integrity of REQUIEM architecture.

GPT is responsible for:

- architectural decisions;
- system analysis;
- documentation;
- planning;
- task preparation;
- reviewing implementations;
- identifying architectural risks.

GPT answers:

"What should be built?"

"Why should it exist?"

"Where does this responsibility belong?"

"Does this strengthen the foundation?"

---

## CLAUDE — EXECUTOR

Primary responsibility:

Implementation of approved tasks.

Claude is responsible for:

- writing code;
- refactoring;
- creating files;
- moving existing code;
- implementing clearly defined changes.

Claude receives:

- current documentation;
- architecture rules;
- exact task description;
- limitations.

Claude answers:

"How can this be implemented correctly?"

---

## GEMINI — SPECIALIST

Optional role.

Gemini may be used for:

- visual analysis;
- image understanding;
- external research;
- specialized tasks.

Gemini does not define architecture.

---

# 3. DEVELOPMENT FLOW

The official workflow:


IDEA

↓

GPT ARCHITECTURE ANALYSIS

↓

DOCUMENTATION UPDATE

↓

TASK SPECIFICATION

↓

CLAUDE IMPLEMENTATION

↓

GPT REVIEW

↓

DOCUMENTATION UPDATE


---

# 4. ARCHITECT RESPONSIBILITY

Before implementation begins:

The Architect must define:

- objective;
- affected layers;
- allowed files;
- forbidden changes;
- expected result;
- validation criteria.

No implementation task should begin without clear ownership.

---

# 5. EXECUTOR RESPONSIBILITY

The Executor must:

- read provided documentation;
- respect existing architecture;
- modify only requested areas;
- avoid unnecessary redesign;
- report changed files.

The Executor must not:

- redefine architecture;
- replace established systems;
- introduce unrelated improvements.

---

# 6. CHANGE PRINCIPLE

Every change must answer:

"Which REQUIEM layer owns this responsibility?"

If no clear owner exists:

The architecture must be discussed before implementation.

---

# 7. DOCUMENTATION PRIORITY

Documentation has priority over assumptions.

If code and documentation disagree:

The discrepancy must be analyzed before changes are made.

---

# 8. PRACTICAL WORKING CYCLE

How the flow of section 3 runs in practice since 2026-09-27 (repository, Claude Code, owner checks).

1. Idea or request — the owner.
2. Analysis — GPT: options and a separate recommendation. The owner decides. Claude records the decision in docs/system/REQUIEM_DECISION_LOG.md.
3. Task specification — GPT writes it. Claude saves it in the repository as a passported file (docs/app/tasks/TASK-NNN_….md) and registers the TASK ID in docs/system/REQUIEM_DOCUMENTATION_INDEX.md.
4. Check — Claude compares the specification with the code and documents and reports every mismatch before any change.
5. Implementation — Claude, on a separate branch: application code in Claude Code on the owner's PC (requiem-tauri/CLAUDE.md); documentation in the repositories.
6. Validation — Claude runs build and start checks and gives the owner a short list of manual checks in Russian. The owner checks the running window by hand.
7. Review — the owner forwards Claude's report to GPT. GPT checks it item by item against the specification.
8. Approval — the owner says "OK" and the branch is merged into main (by the owner on GitHub or by Claude after the OK).
9. Session end — Claude updates docs/system/REQUIEM_ACTIVE_SESSION.md, the ID registry, and when a step is accepted the roadmap (REQUIEM_ROADMAP.md and REQUIEM_ROADMAP.html together).

Exception: small visual tweaks the owner asks for directly (a color, a spacing, a text) skip steps 2–3 and 7 (CLAUDE_IMPLEMENTATION_PROTOCOL.md, Level 0). They still use a branch and the owner's OK.

---

# END OF WORKFLOW