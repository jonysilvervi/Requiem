# REQUIEM Application docs — notes

## Resolved on 2026-09-27: where Phase 1 stands

Four documents disagreed about Phase 1 progress. The code was checked on 2026-09-27
(archive of requiem-tauri without src-tauri; `src-tauri` not checked). Result:

| Document | Its claim | Code says |
|---|---|---|
| `REQUIEM_AI_MASTER_CONTEXT.md` v1.0, section 5 | Shell, Visual Core foundation and contracts exist | **Correct** |
| `REQUIEM_CURRENT_STATE_SNAPSHOT.md` v0.2, section 15 | only Phase 0 complete | Outdated — fixed in v0.3 |
| `REQUIEM_PHASE_1_CORE_SKELETON_SPEC_v0.3.md`, section 17 | next: create contracts | Done — all six contracts exist |
| `REQUIEM_ACTIVE_SESSION.md` (2026-09-23) | next: create folders | Done — fixed in v1.1 |

The Phase 1 success criteria are met in code (`REQUIEM_CURRENT_STATE_SNAPSHOT.md`, section 9).
Formal completion of Phase 1 is a decision of the owner.

The phase documents (`REQUIEM_PHASE_1_*`) are kept as the plans they were; they are not
rewritten to match the result.

## Open findings for the owner

1. **The visual prototype is not connected.** `src/App.jsx` (984 lines, changed 2026-09-24)
   holds the prototype "FOUNDATION RESET (R0)" with levels L0 SHELL … L4 SYSTEM. Nothing imports
   it. The running application shows only the shell placeholder "REQUIEM VISUAL CORE".
   The empty folders `src/app/modules/{navigation,intelligence,environment,system}` match the
   R0 levels. Decide whether R0 is moved into the new structure, used as reference, or retired.
2. **Legacy dependencies are back.** `package.json` lists `@tauri-apps/plugin-opener`, `clsx`,
   `tailwind-merge`, which the Phase 0 snapshot records as removed.
3. **Leftovers:** `src/assets/react.svg` (template), empty `src/App.css`, and a stray empty
   folder `src/stylesnpm` (looks like a typing accident next to `src/styles`).
4. **Empty folders are not stored by git.** `adapters/contracts`, `components/shared`, `styles`
   and `app/modules/*` will not appear in the repository until they contain a file.
5. **Implementation Plan reference.** `REQUIEM_PHASE_1_IMPLEMENTATION_PLAN_v0.2.md` names
   "REQUIEM_PHASE_1_CORE_SKELETON_SPEC_v0.1.md" as its previous document; the file present is v0.3.
6. **src-tauri not checked yet** — including where the PowerShell Execution Engine code lives.
