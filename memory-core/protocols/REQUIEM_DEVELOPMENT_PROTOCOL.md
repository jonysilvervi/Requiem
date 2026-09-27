# REQUIEM DEVELOPMENT PROTOCOL

Version: 0.5

Document Type:
AI Development Rules

Purpose:
Define rules for AI-assisted development inside REQUIEM ecosystem.

---

# 1. ROLE OF AI

AI is an implementation and analysis assistant.

AI does not own project truth.

The source of truth:

- approved documentation;
- project files;
- confirmed decisions.

---

# 2. BEFORE IMPLEMENTATION

Before modifying anything AI must:

1. Understand current architecture.
2. Identify affected files.
3. Explain planned changes.
4. Confirm compatibility with existing rules.

---

# 3. CHANGE PRINCIPLE

Every modification must answer:

What changes?

Why changes?

What is affected?

What can break?

---

# 4. PROHIBITED ACTIONS

AI must not:

- redesign architecture without approval;
- delete historical information;
- silently modify critical memory;
- add unnecessary dependencies;
- merge unrelated systems.

---

# 5. MEMORY CORE RULES

Memory Core layers:

```
Observation
↓
Storage
↓
Comparison
↓
Analysis
↓
Decision
```


Layers must remain separated.

Implemented layers (Memory Core 0.6):

- Observation — scanner (v0.2);
- Storage — snapshots (v0.1);
- Comparison — comparator (v0.1);
- Change Report — change_reporter (v0.1);
- Analysis — analyzer (v0.1);
- Context Update — context_updater (v0.1).

Order of implemented layers (DEC-014):

```
Comparison → Change Report → Analysis → Human review → Context Update
```

Change Report and Context Update do not perform analysis.

Analysis is advisory: it does not approve, reject or change memory (DEC-015).

Decision is made by a human: review of change records (CHG) and approval and manual apply of context updates (CU).

---

# 6. CODE CHANGES

When implementing:

AI must provide:

- changed files;
- reason for each change;
- testing method;
- possible risks.

---

# 7. CURRENT TASK RULE

Completed:

- Memory Core State Snapshot System v0.1;
- Memory Core Comparison Layer v0.1;
- Memory Core Change Report Layer v0.1;
- Memory Core Context Update Layer v0.1;
- Memory Core Analysis Layer v0.1.

Current direction:

Architecture map preparation and approval.

Status:

Direction only.

The architecture map is written and approved by a human (DEC-017).

AI may prepare a draft only on request.

Not:

- AI analysis;
- UI;
- application integration.

---

# FINAL RULE

Build understanding first.

Automate second.

Add intelligence last.

END OF PROTOCOL