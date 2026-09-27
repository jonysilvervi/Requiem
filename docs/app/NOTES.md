# REQUIEM Application docs — known inconsistencies

These four documents disagree with each other about where Phase 1 currently stands.
None of this has been reconciled against the actual `requiem-tauri` repository yet —
do that before relying on any of them.

- `REQUIEM_AI_MASTER_CONTEXT.md`, section 5 — claims Application Shell, Visual Core
  foundation and contracts already exist.
- `REQUIEM_CURRENT_STATE_SNAPSHOT.md`, section 15 — says only Phase 0 (Demolition)
  is complete; Phase 1 has not started.
- `REQUIEM_PHASE_1_CORE_SKELETON_SPEC_v0.3.md`, section 17 — says architecture is
  approved, next action is creating system contracts.
- `REQUIEM_ACTIVE_SESSION.md` — says the next action is physical folder creation.

Also: `REQUIEM_PHASE_1_IMPLEMENTATION_PLAN_v0.2.md` references
"REQUIEM_PHASE_1_CORE_SKELETON_SPEC_v0.1.md" as its previous document, but the file
actually present here is v0.3.

All of these are dated 2026-09-23. Resolve by checking the actual `requiem-tauri`
repository state, not by picking whichever document sounds most authoritative.
