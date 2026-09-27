# REQUIEM AI MASTER CONTEXT

Version: 1.1 Draft

Document Type:
AI Integration Context

Purpose:
Provide a complete operational context for AI systems working with the REQUIEM project.

---

# 1. PROJECT IDENTITY

## What is REQUIEM?

REQUIEM is an intelligent environment layer designed to create a unified interaction space between the user and complex digital environments.

REQUIEM is not a launcher.
REQUIEM is not a simple mod manager.
REQUIEM is not a chatbot interface.

Games, applications, and tools are considered environments connected through adapters.

The first supported environment is S.T.A.L.K.E.R. 2.

However, S.T.A.L.K.E.R. 2 is not the center of the system.

The center is REQUIEM itself.

REQUIEM is an ecosystem (memory-core/context/REQUIEM_GLOSSARY.md, section 3):

- Projects — for example REQUIEM Application (the desktop application, requiem-tauri), REQUIEM Mod Pack, Memory Core Development Project;
- REQUIEM Engine;
- Tools;
- Memory Core — the project continuity system.

All documentation lives in the repository jonysilvervi/Requiem (Decision #008).

---

## Core Idea

The user should not manually operate dozens of separate tools.

The user expresses intent.

REQUIEM:

1. Understands the intent.
2. Analyzes context.
3. Creates an operation plan.
4. Executes actions through internal systems.
5. Presents the result through the Visual Core.

The complexity stays behind the system layers.

The user experiences a coherent premium environment.

---

# 2. REQUIEM PHILOSOPHY

REQUIEM is built around three principles:

## 2.1 Intelligence over buttons

Traditional software exposes functions.

REQUIEM exposes intent.

The user should not think:

"Which tool should I open?"

The user should think:

"What do I want to achieve?"

---

## 2.2 Architecture over features

New functionality must extend the existing architecture.

Features must not force the destruction of the foundation.

The system grows through layers.

---

## 2.3 Premium experience through precision

REQUIEM aims for a premium experience.

Premium does not mean excessive decoration.

Premium means:

- every element has purpose;
- every interaction has meaning;
- every visual decision supports the system state.

Animations, effects, materials, lighting, and transitions are allowed.

There are no artificial restrictions.

The only requirement:

Use them with precision.

---

# 3. SYSTEM ARCHITECTURE

REQUIEM is divided into independent responsibility layers.


VISUAL CORE

↓

INTELLIGENCE LAYER

↓

OPERATIONS RUNTIME

↓

EXECUTION ENGINE

↓

ENVIRONMENT ADAPTERS

↓

TARGET ENVIRONMENT


---

# 4. LAYER RESPONSIBILITIES

## Visual Core

Responsible for:

- user experience;
- visualization;
- interaction;
- system presentation.

Visual Core does NOT:

- execute system commands;
- directly control environments;
- contain environment-specific logic.

---

## Intelligence Layer

Responsible for:

- understanding user intent;
- context analysis;
- planning.

Intelligence does NOT directly execute actions.

It produces structured requests for the operation system.

---

## Operations Runtime

Responsible for:

- operation planning;
- validation;
- execution flow;
- reporting.

Operations decides HOW a goal should be achieved.

---

## Execution Engine

Responsible for actual actions.

Examples:

- filesystem operations;
- automation;
- PowerShell execution;
- system communication.

Execution Engine performs actions.

It does not decide why actions are needed.

---

## Environment Adapters

Adapters connect REQUIEM to external environments.

Examples:

- S.T.A.L.K.E.R. 2 adapter;
- future environments.

Core systems must never depend directly on a specific environment.

---

# 5. CURRENT PROJECT STATE

Active work stream:

REQUIEM Visual Core (Decision #011).

Frozen:

- Execution Engine (PowerShell) (Decision #010);
- Memory Core development, paused at REQUIEM_KNOWLEDGE_MODEL.md v0.5 (Decision #009);
- new architecture documentation (Decision #010).

REQUIEM Application state:

Recorded in docs/app/REQUIEM_CURRENT_STATE_SNAPSHOT.md (verified against the code on 2026-09-27). The Phase 1 skeleton exists in code; open findings are listed in docs/app/NOTES.md. The real code is always the reference.

The current position between sessions is recorded in docs/system/REQUIEM_ACTIVE_SESSION.md.

---

# 6. IMPORTANT CURRENT DECISIONS

## PowerShell

PowerShell is not the architecture.

PowerShell is a future execution mechanism.

Current status:

FROZEN.

Do not expand PowerShell integration during foundation work.

---

## Memory Core

Memory Core development is paused (Decision #009).

The implemented layers (checkpoint CP-006) remain usable. No new Memory Core work starts without an explicit request of the human owner.

---

## Visual Core

The Visual Core is the active work stream (Decision #011).

The Phase 1 restrictions on visual work are lifted for it. The architecture boundaries remain in force: the Visual Core owns presentation only, never executes system actions and never contains environment-specific logic.

---

## AI

REQUIEM is not an AI chatbot.

AI is an intelligence layer inside a larger system.

---

## S.T.A.L.K.E.R. 2

S.T.A.L.K.E.R. 2 is the first environment.

It is not the core.

Do not place S.T.A.L.K.E.R. 2 specific logic inside the core architecture.

---

# 7. AI WORKING RULES

When working with REQUIEM:

1. Study existing documentation first.
2. Understand current architecture before proposing changes.
3. Do not rebuild the project from zero.
4. Do not simplify architecture without approval.
5. Do not introduce features without defining their layer ownership.
6. Preserve existing decisions unless explicitly changed.

---

# 8. AI ROLES

REQUIEM uses different AI systems with different responsibilities.

## GPT

Role:

ARCHITECT

Responsible for:

- architecture;
- planning;
- documentation;
- analysis;
- review;
- decision making.

---

## Claude

Role:

EXECUTOR

Responsible for:

- implementation;
- refactoring;
- code generation;
- precise execution of technical tasks.

Claude receives:

- architecture;
- documentation;
- specific task instructions.

Claude does not redefine architecture.

---

## Gemini

Role:

SUPPORT INTELLIGENCE (Optional)

Used only when specific capabilities are beneficial.

---

## Human owner

Final approval of decisions and changes.

Approves changes by merging them in the repository (Decision #008).

---

# 9. DEVELOPMENT PRINCIPLE

REQUIEM is not developed as a collection of isolated features.

It is developed as a permanent ecosystem.

Every decision must answer:

"Does this strengthen the foundation?"

---

# END OF CONTEXT