# REQUIEM AI WORKFLOW

Version: 1.0 Draft

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

# END OF WORKFLOW