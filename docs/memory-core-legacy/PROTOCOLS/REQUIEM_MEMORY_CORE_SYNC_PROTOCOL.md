# REQUIEM MEMORY CORE SYNC PROTOCOL

Version: 0.1

Document Type:
State Synchronization Protocol

Purpose:
Define how REQUIEM Memory Core detects, analyzes and synchronizes changes between the real project state and project memory.

---

# 1. SYNC SYSTEM IDENTITY

REQUIEM Memory Core Sync System is responsible for maintaining consistency between:

- real project state;
- stored project memory;
- documentation;
- AI understanding.

Its purpose is preventing information loss and documentation drift.

---

# 2. CORE PRINCIPLE

Memory Core follows the principle:

> The project state should be discovered automatically, while interpretation should remain controlled.

The system must reduce manual tracking.

The system must not require a developer to remember every documentation update.

---

# 3. SYNCHRONIZATION MODEL

The synchronization process consists of:


Detection

↓

Collection

↓

Classification

↓

Analysis

↓

Validation

↓

Memory Update


---

# 4. DETECTION STAGE

Purpose:

Find changes in the project environment.

Possible sources:

- file system;
- repository state;
- configuration;
- dependencies;
- documentation;
- project structure.

Examples:

Detected:

- new file;
- removed file;
- changed architecture document;
- new dependency;
- new system layer.

---

# 5. COLLECTION STAGE

After detecting changes, Memory Core collects related information.

Collected data:

- affected files;
- previous state;
- current state;
- related decisions;
- related documentation.

The system must not analyze isolated changes without context.

---

# 6. CLASSIFICATION STAGE

Every detected change receives an importance category.

## LEVEL 0 — Noise

Examples:

- temporary files;
- generated files;
- insignificant modifications.

Action:

Ignore or store temporarily.

---

## LEVEL 1 — Technical Change

Examples:

- dependency update;
- internal refactoring;
- configuration change.

Action:

Record if relevant.

---

## LEVEL 2 — Structural Change

Examples:

- new module;
- new folder system;
- new project layer.

Action:

Requires analysis.

---

## LEVEL 3 — Architectural Change

Examples:

- changed system boundaries;
- changed core principles;
- modified architecture.

Action:

Requires explicit validation.

---

## LEVEL 4 — Critical Change

Examples:

- modification of Memory Core rules;
- modification of project identity;
- modification of fundamental decisions.

Action:

Maximum protection.

---

# 7. ANALYSIS STAGE

The system evaluates:

## What changed?

Example:

New intelligence module added.

---

## Why did it change?

Source:

- developer decision;
- implementation task;
- experiment.

---

## What does it affect?

Possible impact:

- architecture;
- documentation;
- current state;
- decisions.

---

# 8. AI ANALYSIS PIPELINE

AI systems assist analysis.

The pipeline:


Scanner

↓

Gemini

↓

GPT

↓

Approved Memory Update


---

## Gemini Role

Gemini acts as an observation and analysis layer.

Responsibilities:

- identify changes;
- summarize differences;
- detect possible inconsistencies.

Gemini does not own project truth.

---

## GPT Role

GPT acts as an architectural validation layer.

Responsibilities:

- determine importance;
- evaluate consequences;
- approve memory changes.

---

## Claude Role

Claude acts as implementation support.

Responsibilities:

- apply approved changes;
- perform technical modifications.

---

# 9. MEMORY UPDATE RULES

Not every change updates all documents.

Examples:

Small UI change:

No architecture update.

New subsystem:

Update:

- current state;
- architecture documentation.

New fundamental decision:

Update:

- decision memory;
- changelog;
- related documentation.

---

# 10. DOCUMENTATION DRIFT DETECTION

Memory Core must detect differences between:

Documented state:


Expected:
src/core/intelligence exists


Reality:


Folder missing


Result:


Documentation Drift Detected


The system should report:

- what differs;
- possible reason;
- recommended correction.

---

# 11. AUTOMATION PRINCIPLE

The goal of synchronization automation:

Not:

"Create more documentation."

The goal:

"Maintain project understanding with minimal human effort."

---

# 12. APPROVAL MODEL

Automatic actions are limited by importance.

Allowed automatically:

- collecting information;
- generating reports;
- detecting changes.

Requires approval:

- changing architecture;
- changing decisions;
- modifying project identity;
- deleting historical information.

---

# 13. FUTURE DEVELOPMENT

Future capabilities:

- continuous project monitoring;
- automatic context package generation;
- AI-assisted documentation updates;
- integration with development environments;
- visual synchronization dashboard.

---

# 14. FINAL PRINCIPLE

A project should not depend on human memory alone.

REQUIEM Memory Core exists so that:

> Changes are discovered, understood and preserved before they become forgotten.

---

END OF SYNC PROTOCOL