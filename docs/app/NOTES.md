# REQUIEM Application docs — notes

## Resolved on 2026-09-27: where Phase 1 stands

Four documents disagreed about Phase 1 progress. The code was checked on 2026-09-27
(repository `jonysilvervi/requiem-tauri`, including `src-tauri`). Result:

| Document | Its claim | Code says |
|---|---|---|
| `REQUIEM_AI_MASTER_CONTEXT.md` v1.0, section 5 | Shell, Visual Core foundation and contracts exist | **Correct** |
| `REQUIEM_CURRENT_STATE_SNAPSHOT.md` v0.2, section 15 | only Phase 0 complete | Outdated — fixed in v0.3 |
| `REQUIEM_PHASE_1_CORE_SKELETON_SPEC_v0.3.md`, section 17 | next: create contracts | Done — all six contracts exist |
| `REQUIEM_ACTIVE_SESSION.md` (2026-09-23) | next: create folders | Done — fixed in v1.1 |

The Phase 1 success criteria are met in code (`REQUIEM_CURRENT_STATE_SNAPSHOT.md`, section 9).
Phase 1 stays open by decision of the owner until the foundation is polished (Decision #012).

The phase documents (`REQUIEM_PHASE_1_*`) are kept as the plans they were; they are not
rewritten to match the result.

## Open findings for the owner

1. **The visual prototype is not connected.** `src/App.jsx` (984 lines, changed 2026-09-24)
   holds the prototype "FOUNDATION RESET (R0)" with levels L0 SHELL … L4 SYSTEM. Nothing imports
   it. The running application shows only the shell placeholder "REQUIEM VISUAL CORE".
   The empty folders `src/app/modules/{navigation,intelligence,environment,system}` match the
   R0 levels. According to the owner, the visual work before the documentation phase was done in
   `src/App.jsx` and `src/index.css`. `src/main.jsx` renders the new skeleton (`AppRoot`) since
   2026-09-22, so changes made to `src/App.jsx` after that date do not appear on screen.
   `src/index.css` is still loaded. Decided: R0 is carried layer by layer, see
   `R0_MIGRATION_PLAN.md` (Decision #013).
2. **Legacy dependencies are back.** `package.json` lists `@tauri-apps/plugin-opener`, `clsx`,
   `tailwind-merge`, which the Phase 0 snapshot records as removed.
3. **Leftovers:** `src/assets/react.svg` (template), empty `src/App.css`, and a stray empty
   folder `src/stylesnpm` (looks like a typing accident next to `src/styles`).
4. **Empty folders are not stored by git.** `adapters/contracts`, `components/shared`, `styles`
   and `app/modules/*` will not appear in the repository until they contain a file.
5. **Implementation Plan reference.** `REQUIEM_PHASE_1_IMPLEMENTATION_PLAN_v0.2.md` names
   "REQUIEM_PHASE_1_CORE_SKELETON_SPEC_v0.1.md" as its previous document; the file present is v0.3.
6. **PowerShell bridge in `src-tauri/src/lib.rs` is a stub.** The only Tauri command,
   `run_core_bridge`, runs PowerShell to print a fixed JSON line
   (`"engine":"REQUIEM_CORE_LIVE"`). Nothing in `src` calls it. The Execution Engine the owner
   describes as nearly complete is not in this repository; where it lives is open.
7. **Before the bridge is used for real:** `run_core_bridge` inserts `action` into the PowerShell
   command text without escaping. A value containing a quote would change the command. This
   must be fixed before any real input reaches it (the engine is frozen, Decision #010).
8. **RESOLVED 2026-09-27.** The native window used to flash white, with a brief transparent
   phase, for about a second before the static dark theme painted. Symptom confirmed by the owner
   during TASK-001 / STEP-R0-01 manual validation on 2026-09-27 (`npm run tauri dev`); confirmed
   fixed by the owner the same day via a frame-by-frame video review (no white frame, no
   transparent phase, window appears already fully rendered).
   Two root-cause hypotheses were recorded: (a) `src-tauri/tauri.conf.json` had `"transparent":
   true` on the window with no explicit background color, so the native window could be shown
   before WebView2 finished loading and painting `index.html`; (b) the dark background only
   existed in `src/index.css`, loaded through the `<script type="module" src="/src/main.jsx">`
   import graph, so the browser could paint the raw HTML (default white background) before that
   module executed and injected the stylesheet.
   Attempts, in order, all on branch `visual-core/r0-step1-l0-shell`:
   1. GPT review selected Variant A for hypothesis (b): minimal inline dark background
      (`background-color: #0c0e11`) added to `index.html` (allowed by TASK-001). Built and run by
      the owner — **did not fix it**.
   2. Owner granted a one-line exception to the `src-tauri` freeze (Decision #010), 2026-09-27:
      `"backgroundColor": "#0c0e11"` added to the window in `tauri.conf.json`. Built and run —
      **did not fix it alone**.
   3. Owner extended the exception: `"transparent": false` (kept `backgroundColor`). Built and
      run — **partial improvement**, white flash remained.
   4. Owner extended the exception further: window created hidden (`"visible": false` in
      `tauri.conf.json`), made visible only via `getCurrentWindow().show()` called once in a
      `useEffect` in `src/app/shell/WindowFrame.jsx` after the shell's first render — window-show
      ownership stays in L0 shell. Required adding the `core:window:allow-show` capability in
      `src-tauri/capabilities/default.json` (verified against the local schema
      `src-tauri/gen/schemas/desktop-schema.json`: the permission is not part of
      `core:window:default`). `src-tauri/src/lib.rs` was not touched — the fix uses only the
      existing `@tauri-apps/api/window` JS binding. Built and run — **fixed it**, confirmed by the
      owner's frame-by-frame review.
   Final state: `transparent: false`, `backgroundColor: "#0c0e11"`, `visible: false` +
   `WindowFrame.jsx` showing the window after first render.
   Residual risk: if the frontend throws before that `useEffect` runs, `show()` is never called
   and the window never becomes visible, with no native fallback to indicate the app is running.
   For GPT review: `src-tauri/tauri.conf.json` and `src-tauri/capabilities/default.json` were
   edited under a one-time owner exception to the `src-tauri` freeze (Decision #010), granted
   2026-09-27, scoped to exactly this fix; TASK-001 explicitly forbade editing these files, and
   this work is authorized separately from TASK-001's original scope.
