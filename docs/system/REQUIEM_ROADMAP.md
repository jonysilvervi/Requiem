# REQUIEM ECOSYSTEM ROADMAP

ID: N/A  
Type: Ecosystem Roadmap  
Document Status: DRAFT  
Area: N/A  
Updated: 2026-09-27

## Ecosystem

| Area | Status | Now | Next | Later | Blockers | Links |
|---|---|---|---|---|---|---|
| AREA-VC — REQUIEM Visual Core | ACTIVE | TASK-001 is specified; STEP-R0-01 is not executed. | Implement and validate STEP-R0-01. | Continue STEP-R0-02 → STEP-R0-06 in order. | No blocker recorded for STEP-R0-01. | [ED-011] [ED-012] [ED-013] [TASK-001] |
| AREA-EE — Execution Engine (PowerShell) | FROZEN | Existing application bridge is a stub; real engine location is still open. | No work until the owner resolves Q-001 and explicitly resumes the area. | Revisit integration only after architecture ownership is settled. | Q-001; ISS-006; ISS-007; ED-010 freeze. | [ED-010] [Q-001] [ISS-006] [ISS-007] |
| AREA-MC — Memory Core | PAUSED | Knowledge Model v0.5 is paused; CP-006 remains usable. | On resume, decide the lifecycle rule after DEPRECATED. | Complete remaining Knowledge Model responsibilities and move toward REVIEW. | Owner authorization to resume; O2/O5/O7 remain open. | [ED-009] O2 O5 O7 |
| AREA-MP — REQUIEM Mod Pack | FROZEN | No active work. | Resume only by owner decision. | Not defined. | No repository blocker recorded; O2 affects future project-to-project references. | O2 |
| AREA-RE — REQUIEM Engine | — (owner decision pending)* | Scope is not assigned; O6 remains open. | Resolve O6 before assigning a formal AREA lifecycle status. | Define the REQUIEM Engine scope and its relation to engine contracts. | O6. | O6 |
| AREA-TL — Tools | PAUSED | Existing tools are used as-is; no separate workstream is active. | No planned work. | Add or change tools only when another area requires it. | None recorded. | — |

\* `Owner decision pending` is not an AREA lifecycle status under ED-014. AREA-RE intentionally has no formal lifecycle status until O6 is resolved.

## AREA-VC Active Path

| Step | Status | Scope | Related task |
|---|---|---|---|
| STEP-R0-01 | SPECIFIED — not executed | L0 SHELL + theme + tokens | [TASK-001] |
| STEP-R0-02 | Not started | L1 NAVIGATION | — |
| STEP-R0-03 | Not started | L2 WORKSPACE | — |
| STEP-R0-04 | Not started | L4 SYSTEM — safe part | — |
| STEP-R0-05 | Not started | L3 INTELLIGENCE | — |
| STEP-R0-06 | Not started | Cleanup | — |

## Open Questions and Issues

- **Q-001** — Location of the PowerShell execution code: owner decision pending.
- **ISS-001** — R0 visual prototype is disconnected; migration is handled layer by layer.
- **ISS-002** — Legacy dependencies are present again.
- **ISS-003** — Template/leftover files and stray folder remain.
- **ISS-004** — Empty folders are not stored by git.
- **ISS-005** — Phase 1 Implementation Plan references the old Core Skeleton spec version.
- **ISS-006** — Application PowerShell bridge is a stub; real execution code location is open.
- **ISS-007** — Bridge action input is not escaped and must be fixed before real input is used.

## Update Rule

Claude updates this roadmap after each completed STEP; GPT reviews the update before owner approval.

## Sources

### Repository evidence

- **README.md, section Current state** — “REQUIEM Visual Core | **ACTIVE** — current work stream (Decision #011)”; “Execution Engine (PowerShell) | **FROZEN** (Decision #010)”; “Memory Core | **PAUSED** at Knowledge Model v0.5”.
- **REQUIEM_ACTIVE_SESSION.md, section NEXT ACTIONS** — “[TASK-001] ([STEP-R0-01]): status SPECIFIED, not executed. The specification is stored in docs/app/tasks/TASK-001_R0_STEP1_L0_SHELL.md”.
- **REQUIEM_ACTIVE_SESSION.md, section OPEN QUESTIONS** — “[Q-001] Location of the PowerShell Execution Engine code (related: [ISS-006]).”
- **REQUIEM_DECISION_LOG.md, DECISION #010 / Decision** — “The Execution Engine (PowerShell) remains FROZEN.” and “Work on frozen areas requires an explicit decision of the human owner.”
- **REQUIEM_DECISION_LOG.md, DECISION #011 / Decision** — “The active work stream is the REQUIEM Visual Core — the visual environment of the ecosystem.”
- **REQUIEM_DECISION_LOG.md, DECISION #012 / Decision** — “Phase 1 (Core Skeleton) is not closed” and “Phase 1 is closed by a separate decision of the human owner.”
- **REQUIEM_DECISION_LOG.md, DECISION #013 / Decision** — “R0 ... is carried into the Phase 1 structure layer by layer, following docs/app/R0_MIGRATION_PLAN.md.”
- **REQUIEM_DOCUMENTATION_INDEX.md, section ALLOCATED IDENTIFIERS / TASK** — “TASK-001 ... AREA-VC | SPECIFIED | STEP-R0-01 ... docs/app/tasks/TASK-001_R0_STEP1_L0_SHELL.md”.
- **R0_MIGRATION_PLAN.md, section Steps** — “L0 SHELL + theme + tokens”; “L1 NAVIGATION”; “L2 WORKSPACE”; “L4 SYSTEM (safe part)”; “L3 INTELLIGENCE”; “Cleanup.”
- **NOTES.md, section Open findings for the owner** — “The visual prototype is not connected.”; “Legacy dependencies are back.”; “Leftovers:”; “Empty folders are not stored by git.”; “Implementation Plan reference.”; “PowerShell bridge in `src-tauri/src/lib.rs` is a stub.”; “Before the bridge is used for real:”.
- **REQUIEM_KNOWLEDGE_MODEL.md, Resume point** — “Decide whether DEPRECATED is terminal for a Knowledge Element”.
- **REQUIEM_FOUNDATION_DECISIONS.md, section 13** — “O6 | Scope of REQUIEM Engine and its relation to the engine contracts in requiem-tauri (src/core/contracts/).”
- **REQUIEM_AI_MASTER_CONTEXT.md, section 6 / S.T.A.L.K.E.R. 2** — “Do not place S.T.A.L.K.E.R. 2 specific logic inside the core architecture.”
- **REQUIEM_PHASE_1_CORE_SKELETON_SPEC_v0.3.md, section 9** — “Games and tools are adapters. They are not the core.”
- **REQUIEM_PHASE_1_CORE_SKELETON_SPEC_v0.3.md, section 13** — “Execution Engine: - owns physical execution.” and “Adapters: - own environment-specific knowledge.”
- **REQUIEM_GLOSSARY.md, section 4 / Environment Reference** — “Project-specific usage and modifications of the environment are Project Knowledge of the referencing project (FD-B7).”
- **REQUIEM_GLOSSARY.md, section 5 / REQUIEM Engine** — “The internal execution system of REQUIEM.” and “Its scope and its relation to the engine contracts in requiem-tauri (src/core/contracts/) are not decided (FD open item O6).”

### Owner-confirmed state for this roadmap

- AREA-MP — FROZEN.
- AREA-TL — PAUSED; existing tools are used as-is and have no separate active workstream.
- AREA-RE — formal lifecycle status intentionally pending the architectural decision around O6.
- Q-001 — owner answer remains pending.
