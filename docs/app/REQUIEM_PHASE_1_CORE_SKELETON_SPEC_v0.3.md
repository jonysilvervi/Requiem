# REQUIEM PHASE 1 — CORE SKELETON SPECIFICATION v0.3

Status:

ARCHITECTURE APPROVED

Phase:

1 — Core Skeleton

Previous phase:

Phase 0 — Foundation Demolition

Current goal:

Create the immutable architectural skeleton of the REQUIEM Ecosystem.

No implementation begins before this architecture is approved.

---

# 1. REQUIEM IDENTITY

REQUIEM is an ecosystem.

REQUIEM is not a simple launcher.

The visual application is only one part of the complete system.

The ecosystem consists of:

- REQUIEM Visual Core;
- Intelligence Layer;
- Operations Runtime;
- Execution Engine;
- Environment Adapters;
- Configuration System;
- Future Extensions.

The purpose of REQUIEM:

Create a unified intelligent control environment for modding, management and interaction with supported environments.

---

# 2. CORE ARCHITECTURE PRINCIPLE

REQUIEM is built from independent but connected systems.

They must operate as reinforced architectural layers.

No single layer replaces another.

Concept:

```
                    REQUIEM ECOSYSTEM


        ┌───────────────────────────────────┐
        │                                   │
        │        REQUIEM VISUAL CORE        │
        │        (Command Center)           │
        │                                   │
        └───────────────────────────────────┘

                    ↓

        ┌───────────────────────────────────┐
        │        INTELLIGENCE LAYER         │
        │        Understanding / Planning   │
        └───────────────────────────────────┘

                    ↓

        ┌───────────────────────────────────┐
        │       OPERATIONS RUNTIME          │
        │       Control / Validation        │
        └───────────────────────────────────┘

                    ↓

        ┌───────────────────────────────────┐
        │       EXECUTION ENGINE            │
        │       PowerShell Automation        │
        └───────────────────────────────────┘

                    ↓

        ┌───────────────────────────────────┐
        │       ENVIRONMENT ADAPTERS        │
        └───────────────────────────────────┘

                    ↓

        Target Environment
```

---

# 3. REQUIEM VISUAL CORE

Purpose:

The primary user-facing command center of REQUIEM.

The Visual Core is not a traditional launcher.

It is the visual control environment of the ecosystem.

Responsibilities:

- user interaction;
- system visualization;
- command input;
- displaying intelligence responses;
- displaying operation states;
- presenting environment information.

The Visual Core owns:

- interface composition;
- presentation state;
- user experience.

The Visual Core does NOT own:

- file manipulation;
- game modification;
- MO2 manipulation;
- PowerShell execution;
- external environment control.

The Visual Core represents the ecosystem.

It does not directly operate the ecosystem.

---

# 4. INTELLIGENCE LAYER

Purpose:

Understand user intent and create structured decisions.

Intelligence is NOT:

- a chat widget;
- a fake assistant;
- a message container;
- a simple command parser.

Responsibilities:

- interpret user requests;
- analyze context;
- create operation plans;
- request execution;
- explain system states.

Flow:

```
User Intent

↓

Intelligence Layer

↓

Operation Request
```

The Intelligence Layer never directly executes system actions.

The Intelligence Layer never directly accesses external files.

The Intelligence Layer never directly calls PowerShell.

---

# 5. OPERATIONS RUNTIME

Purpose:

The control layer between intelligence and execution.

Operations Runtime transforms intentions into controlled operations.

Responsibilities:

- operation planning;
- validation;
- execution management;
- logging;
- error handling;
- rollback preparation;
- result tracking.

Example:

```
Operation:

Install Mod Package


Process:

1. Validate package

2. Prepare workspace

3. Create backup

4. Execute

5. Verify

6. Report
```

Operations Runtime does not directly manipulate external environments.

---

# 6. REQUIEM EXECUTION ENGINE

Purpose:

The physical execution layer.

This is where real system actions happen.

The Execution Engine is separate from the Visual Core.

Responsibilities:

- filesystem operations;
- automation;
- PowerShell execution;
- environment communication;
- deployment;
- backup;
- restoration;
- validation tasks.

The Execution Engine is the hand of REQUIEM.

It is not the brain.

It does not decide:

- what should happen;
- why it should happen;
- when it should happen.

Those decisions belong to higher layers.

---

# 7. ABSOLUTE ENVIRONMENT ISOLATION RULE

REQUIEM Visual Core must never directly manipulate external environments.

The following are forbidden:

```
Visual Core

↓

Game Files
```

```
Visual Core

↓

MO2

↓

Mod Files
```

```
Intelligence Layer

↓

Direct PowerShell Command

↓

External System
```

All external actions must follow:

```
User

↓

REQUIEM Visual Core

↓

Intelligence Layer

↓

Operation Request

↓

Operations Runtime

↓

Execution Engine

↓

Environment Adapter

↓

Target Environment
```

The user experience may appear seamless.

The execution remains controlled through system boundaries.

---

# 8. REQUIEM RUNTIME WORKSPACE

REQUIEM does not use external environments as a workspace.

Operations must pass through controlled runtime areas.

Workspace responsibilities:

- temporary processing;
- staging;
- backups;
- validation;
- operation data;
- rollback preparation.

Example:

```
Mod Package

↓

REQUIEM Workspace

↓

Validation

↓

Backup

↓

Execution Engine

↓

Environment Adapter

↓

Game Environment
```

---

# 9. ENVIRONMENT ADAPTER LAYER

Purpose:

Connect REQUIEM with external environments.

Games and tools are adapters.

They are not the core.

Example:

```
REQUIEM Core

↓

STALKER 2 Adapter

↓

STALKER 2 Environment
```

Future:

```
REQUIEM Core

↓

Future Adapter

↓

Future Environment
```

The core must not require rewriting for new environments.

---

# 10. CONFIGURATION SYSTEM

Purpose:

Centralized persistent system information.

Contains:

- user preferences;
- environment profiles;
- adapter configuration;
- runtime settings;
- system state.

Configuration remains independent from Visual Core.

---

# 11. DATA FLOW

Approved flow:

```
User

↓

REQUIEM Visual Core

↓

Intelligence Layer

↓

Operations Runtime

↓

Execution Engine

↓

Environment Adapter

↓

Target Environment
```

Forbidden:

```
Interface

↓

Direct External Modification
```

No layer bypasses ownership boundaries.

---

# 12. PROJECT STRUCTURE

Approved concept:

```
src/

├── app/
│   ├── shell/
│   └── layout/

├── core/
│   ├── intelligence/
│   ├── operations/
│   ├── environment/
│   ├── configuration/
│   └── contracts/

├── adapters/
│   └── contracts/

├── components/
│   └── shared/

├── styles/

└── main.jsx
```

Folders represent responsibility ownership.

They are not feature containers.

---

# 13. SYSTEM OWNERSHIP RULES

Every system has one owner.

Rules:

Visual Core:

- owns presentation.

Intelligence Layer:

- owns interpretation.

Operations Runtime:

- owns operation control.

Execution Engine:

- owns physical execution.

Adapters:

- own environment-specific knowledge.

Configuration:

- owns persistent state.

No system silently absorbs another system responsibility.

---

# 14. DATA CONTRACT PRINCIPLE

Communication between layers must happen through defined contracts.

Initial contracts:

```
User Intent Contract

Operation Request Contract

Environment State Contract

Operation Result Contract

Engine Command Contract

Engine Response Contract
```

Direct uncontrolled communication is forbidden.

---

# 15. PHASE 1 RESTRICTIONS

Phase 1 may create:

- folders;
- contracts;
- interfaces;
- boundaries;
- architectural foundations.

Phase 1 may not create:

- full Visual Core UI;
- AI provider integration;
- PowerShell implementation;
- game integration;
- mod management logic;
- external automation.

---

# 16. PHASE 1 SUCCESS CRITERIA

Phase 1 is complete when:

✓ ecosystem architecture approved

✓ ownership boundaries defined

✓ contracts defined

✓ folder structure created

✓ build remains functional

✓ no layer violations introduced

---

# 17. CURRENT CHECKPOINT

Current state:

```
PHASE 0 COMPLETE

PHASE 1:

CORE SKELETON ARCHITECTURE APPROVED

NEXT ACTION:

Create system contracts and foundations.
```

---

END OF DOCUMENT