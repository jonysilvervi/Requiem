# REQUIEM DECISION LOG

Version: 1.0 Draft

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