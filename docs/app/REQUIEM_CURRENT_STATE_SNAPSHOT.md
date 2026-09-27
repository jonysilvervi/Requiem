# REQUIEM CURRENT STATE SNAPSHOT

Version: 0.3  
Status: Living Project Memory Document  
Purpose: Recovery checkpoint, architectural continuity and handoff document.

---

# 1. PROJECT IDENTITY

## REQUIEM

REQUIEM is a premium desktop tactical environment and AI-assisted modding platform.

REQUIEM is **not** a S.T.A.L.K.E.R. 2-only application.

S.T.A.L.K.E.R. 2 is the first supported environment.

The core architecture must allow future game environments, modding targets and integrations without rewriting the foundation.

Core principle:

> Games are environments. REQUIEM is the intelligence and orchestration layer above them.

---

# 2. CURRENT TECHNOLOGY FOUNDATION

Current stack:

- Tauri desktop application
- React
- Vite
- Tailwind CSS
- PostCSS
- Framer Motion
- Windows WebView2 environment

Code repository: jonysilvervi/requiem-tauri (GitHub, private).

Current repository root:


requiem-tauri/


Expected launch location:


E:\Games\STALKER 2 - REQUIEM\NECESSARY FILES\requiem-tauri


---

# 3. ARCHITECTURAL MODEL

Future REQUIEM structure:


REQUIEM CORE

├── Application Shell
│
├── Environment Layer
│
├── Intelligence Boundary
│
├── Operations Runtime
│
├── Configuration Layer
│
└── Game Adapter Layer
│
├── S.T.A.L.K.E.R. 2 Adapter
│
└── Future Game Adapters


---

# 4. IMPORTANT ARCHITECTURAL RULES

## Intelligence

Intelligence is not a chat widget.

The AI layer must become a system-level reasoning and assistance layer.

It must not be reduced to:

- fake conversations;
- message lists;
- assistant personas;
- UI demonstrations.

---

## Operations

Operations are real system actions.

The interface must not contain fake buttons pretending to control systems.

Future operations must communicate through proper runtime boundaries.

---

## Game Separation

The core must remain game-independent.

Do not hardcode:

- S.T.A.L.K.E.R. paths;
- S.T.A.L.K.E.R. mechanics;
- S.T.A.L.K.E.R.-only assumptions.

Game-specific logic belongs inside adapters.

---

# 5. PHASE 0 STATUS

## Phase 0 — Demolition

STATUS:


COMPLETE


Goal:

Remove prototype architecture and create a clean foundation.

---

# 6. PHASE 0 COMPLETED ACTIONS

Removed:

## Legacy UI Model

Removed:

- old dashboard approach;
- old navigation system;
- fake assistant interface;
- fake operational controls;
- developer calibration panel.

---

## Legacy AI/Chat Model

Removed:

- messages state;
- assistant modes;
- Companion/Operator/Ambient concepts;
- fake chat logic;
- message handling architecture.

---

## Legacy Dependencies

Removed:


@tauri-apps/plugin-opener
tauri-plugin-opener
clsx
tailwind-merge

Note (verified 2026-09-27): package.json still lists @tauri-apps/plugin-opener, clsx and tailwind-merge. They were either not removed or were added back.

---

## Template Content

Removed:


src/assets/react.svg
vite.svg reference


---

# 7. PRESERVED FOUNDATION

The following files remain the foundation:


src/main.jsx

src/index.css

vite.config.js

tailwind.config.js

postcss.config.js

tauri.conf.json


---

## CSS Foundation

Important:

`src/index.css` was preserved.

It contains the base visual foundation:

- reset;
- variables;
- theme structure;
- layout foundations;
- portal rules.

Do not delete without architectural review.

---

# 8. CURRENT APPLICATION STATE

Verified against the code on 2026-09-27 (repository jonysilvervi/requiem-tauri, including src-tauri).

Entry point:

src/main.jsx renders AppRoot → RequiemShell → WindowFrame → MainLayout → Workspace.

The Workspace shows the text "REQUIEM VISUAL CORE". This is the whole visible interface at the moment.

Build:

vite build succeeds (21 modules). The output is identical to dist/ built on 2026-09-22.

Not connected:

src/App.jsx (984 lines, last changed 2026-09-24) contains the earlier visual prototype "FOUNDATION RESET (R0)" with five levels L0 SHELL, L1 NAVIGATION, L2 WORKSPACE, L3 INTELLIGENCE, L4 SYSTEM. It is not imported anywhere and does not appear in the running application.

---

# 9. CURRENT REPOSITORY STATE

Verified 2026-09-27:


requiem-tauri/

├── src/
│ ├── main.jsx
│ ├── index.css
│ ├── App.jsx            (not connected, see section 8)
│ ├── App.css            (empty)
│ ├── app/
│ │ ├── AppRoot.jsx
│ │ ├── shell/           (RequiemShell, WindowFrame)
│ │ ├── layout/          (MainLayout)
│ │ ├── workspace/       (Workspace)
│ │ └── modules/         (environment, intelligence, navigation, system — empty)
│ ├── core/
│ │ ├── contracts/       (UserIntent, OperationRequest, OperationResult, EnvironmentState, EngineCommand, EngineResponse)
│ │ ├── intelligence/    (boundary only)
│ │ ├── operations/      (boundary only)
│ │ ├── environment/     (boundary only)
│ │ └── configuration/   (boundary only)
│ ├── adapters/contracts/ (empty)
│ ├── components/shared/  (empty)
│ ├── styles/             (empty)
│ └── assets/react.svg
│
├── src-tauri/
├── public/
├── package.json
├── package-lock.json
├── index.html
├── vite.config.js
├── tailwind.config.js
└── postcss.config.js


Phase 1 success criteria (REQUIEM_PHASE_1_CORE_SKELETON_SPEC_v0.3.md, section 16), checked against the code:

- folder structure created — yes;
- ownership boundaries defined — yes (core boundary modules);
- contracts defined — yes, all six contracts of REQUIEM_PHASE_1_CORE_SKELETON_SPEC_v0.3.md, section 14;
- build remains functional — yes;
- no layer violations introduced — none found: core modules contain no UI, shell components contain no system logic.

Phase 1 stays open by decision of the owner (Decision #012).

(Actual tree must always be verified against repository.)

---

# 10. RUNNING THE PROJECT

Current known launch method:

Batch file:


cd /d "E:\Games\STALKER 2 - REQUIEM\NECESSARY FILES\requiem-tauri"

call npm run tauri dev


Expected manual equivalent:


cd requiem-tauri

npm install

npm run tauri dev


---

# 11. CURRENT LIMITATIONS

Current state intentionally does not contain:

- final UI;
- Intelligence implementation;
- Operations runtime;
- PowerShell engine bridge;
- game adapters;
- S.T.A.L.K.E.R. integration.

This is expected.

---

# 12. NEXT DEVELOPMENT PHASE

# Phase 1 — Core Skeleton

Goal:

Create immutable application architecture.

Before coding define:

- component ownership;
- folder structure;
- system boundaries;
- responsibility separation.

Required layers:


Application Shell

Environment

Intelligence Boundary

Operations

Configuration

Game Adapter Interface


---

# 13. PHASE 1 RESTRICTIONS

Do not:

- restore old interface;
- create chat UI;
- create dashboard cards;
- create fake monitoring systems;
- hardcode S.T.A.L.K.E.R.;
- mix UI and runtime logic.

---

# 14. DEVELOPMENT ORDER

Correct order:


Phase 0
Foundation cleanup
↓
Phase 1
Core Skeleton
↓
Phase 2
Runtime Systems
↓
Phase 3
Intelligence Integration
↓
Phase 4
Game Adapters
↓
Phase 5
S.T.A.L.K.E.R. 2 Integration


---

# 15. CURRENT CHECKPOINT

Current state (2026-09-27):


PHASE 0 COMPLETE

PHASE 1 CORE SKELETON: present in code, success criteria met (section 9); phase stays OPEN by decision of the owner (Decision #012)

ACTIVE WORK STREAM: Visual Core (Decision #011)

FROZEN: Execution Engine (PowerShell), Memory Core development, new architecture documentation


---

# 16. HANDOFF INSTRUCTION FOR FUTURE CHAT

If this document is provided to another AI/session:

Do not restart audit.

Do not repeat demolition.

Do not redesign old systems.

Continue from docs/system/REQUIEM_ACTIVE_SESSION.md in the repository jonysilvervi/Requiem.

---

END OF SNAPSHOT