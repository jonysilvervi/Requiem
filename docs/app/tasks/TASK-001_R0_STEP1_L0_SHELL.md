# TASK-001 — R0 migration step 1: L0 SHELL + static theme + calibrated color tokens

ID: TASK-001
Type: Task Specification
Document Status: DRAFT
Object Status: SPECIFIED
Area: AREA-VC
Updated: 2026-09-27

Related: [STEP-R0-01] (docs/app/R0_MIGRATION_PLAN.md, section Steps, step 1), [ED-013], [ED-011], [ED-012].

Prepared by GPT (Architect) on 2026-09-27. Checked against the code by Claude (Executor) on 2026-09-27: all file and line references, CSS class names, Tauri configuration and permissions, and the eight calibrated color values match `jonysilvervi/requiem-tauri` at commit `ec43d4a`.
Accepted by the owner as the next implementation task. The reference for the four calibrated colors (R0 values with all four Dev Panel sliders at their default 1.00) was decided by the owner.

Executor: Claude in Claude Code, on the owner's PC, in the local `requiem-tauri` folder.

The specification below is kept verbatim.

````text
Task Name
R0 Migration — Step 1: L0 SHELL + Static Theme + Calibrated Color Tokens

Objective
Implement step 1 of the accepted R0 migration plan in the local `requiem-tauri` repository:

1. Move the R0 L0 window chrome into the existing Phase 1 shell structure.
2. Set the default theme statically to dark on `<html>`.
3. Fix the four R0 calibrated color values directly in CSS for both dark and light themes.
4. Preserve the current Phase 1 skeleton and the `REQUIEM VISUAL CORE` workspace placeholder.
5. Keep the application buildable and runnable after this step.

Do only step 1. Do not start L1, L2, L3, L4, cleanup, or any unrelated work.

Context
Documentation is in the adjacent local `Requiem` repository. Application code is in the local `requiem-tauri` repository.

The accepted migration plan states:

"Carry the visual prototype R0 (`src/App.jsx`, `src/index.css` in `jonysilvervi/requiem-tauri`)
into the Phase 1 structure layer by layer. The application must build and start after every step."

Source: `docs/app/R0_MIGRATION_PLAN.md`, section `Goal`.

For step 1 it states:

"1. **L0 SHELL + theme + tokens.** Window chrome moves into `src/app/shell/`
   (`getCurrentWindow()`, drag region, minimize, maximize/restore, close)."

Source: `docs/app/R0_MIGRATION_PLAN.md`, section `Steps`.

Decision #013 states:

"R0 (src/App.jsx and src/index.css in jonysilvervi/requiem-tauri) is carried into the Phase 1 structure layer by layer, following docs/app/R0_MIGRATION_PLAN.md. It is not reconnected as a whole."

Source: `docs/system/REQUIEM_DECISION_LOG.md`, section `DECISION #013 / Decision`.

Decision #011 preserves the architecture boundary:

"the Visual Core owns presentation only; it does not execute system actions, does not modify game files, MO2 or other external environments, and does not contain environment-specific logic"

Source: `docs/system/REQUIEM_DECISION_LOG.md`, section `DECISION #011 / Decision`.

Current application entry path:
- `src/main.jsx:4` imports `AppRoot`.
- `src/main.jsx:6` imports `src/index.css`.
- `src/main.jsx:10` renders `AppRoot`.
- `src/app/AppRoot.jsx:5` renders `RequiemShell`.
- `src/app/shell/RequiemShell.jsx:6-7` renders `WindowFrame` and `MainLayout`.
- `src/app/shell/WindowFrame.jsx:3` currently uses `requiem-window-frame`.
- The disconnected R0 implementation remains in `src/App.jsx`.

Relevant R0 source:
- `FOUNDATION`: `src/App.jsx:71`.
- `DEV_VARS`: `src/App.jsx:92`.
- `applyCalibratedVars`: `src/App.jsx:99`.
- `ShellChrome`: `src/App.jsx:308`.
- drag region: `src/App.jsx:311`.
- minimize: `src/App.jsx:321`.
- maximize/restore: `src/App.jsx:324`.
- close: `src/App.jsx:327`.
- old React theme setter: `src/App.jsx:771`.

Existing R0 CSS to reuse:
- `.env`: `src/index.css:169`.
- `.env-chrome`: `src/index.css:183`.
- `.act`: `src/index.css:928`.
- `.act-critical:hover`: `src/index.css:949`.

Do not create a parallel L0 styling system.

The native window is already configured without OS decorations:
- `"decorations": false` — `src-tauri/tauri.conf.json:20`.

The required Tauri permissions already exist:
- close — `src-tauri/capabilities/default.json:8`
- minimize — `src-tauri/capabilities/default.json:9`
- toggle maximize — `src-tauri/capabilities/default.json:10`
- start dragging — `src-tauri/capabilities/default.json:11`

Architecture Context
Owner layer:
`REQUIEM Application -> Visual Core -> L0 SHELL / presentation`.

Why:
L0 owns the application window frame, drag surface, and native window controls. This is presentation/window-shell behavior and belongs under `src/app/shell/`.

This task must not move runtime, environment-specific, Execution Engine, game, MO2, intelligence, navigation, workspace-domain, or system-command logic into the shell.

The existing Phase 1 structure remains the active application. `src/App.jsx` is only a migration source and must remain disconnected.

Allowed Changes
Application repository `requiem-tauri`:

- `index.html`
- `src/index.css`
- `src/app/shell/`
- only the minimal import/export/composition changes required to connect the L0 shell inside the existing Phase 1 structure

Expected shell files may include:
- existing `WindowFrame.jsx`
- existing `RequiemShell.jsx`
- existing `src/app/shell/index.js`
- a new `ShellChrome.jsx` if required

Documentation repository `Requiem`:

- At the end of the work session, update `docs/system/REQUIEM_ACTIVE_SESSION.md` as required by Decision #010.
- Record factual implementation/session state only.
- Do not mark this implementation APPROVED, TRUSTED, accepted, or merged unless the human owner has actually confirmed it.

Forbidden Changes
- Do not reconnect `src/App.jsx`.
- Do not import `src/App.jsx` into the active application.
- Do not delete or clean up `src/App.jsx`.
- Do not perform the migration cleanup step.
- Do not migrate L1 Navigation.
- Do not migrate L2 Workspace geometry.
- Do not migrate L3 Intelligence.
- Do not migrate L4 System / Command Palette.
- Do not add the R0 Command Palette button to the chrome in this step.
- Do not add the R0 theme-toggle button to the chrome in this step.
- Do not add React theme state or a React theme setter in this step.
- Do not migrate the Dev Panel or calibration sliders.
- Do not add assistant modes, personas, chat state, fake replies, fake monitoring, or fake system actions.
- Do not change Execution Engine or PowerShell code.
- Do not change game files, MO2 integration, adapters, contracts, or external-environment logic.
- Do not add a second set of L0 CSS classes that duplicates `.env`, `.env-chrome`, `.act`, or `.act-critical`.
- Do not replace the existing R0 CSS visual system with a new visual system.
- Do not split `src/index.css`.
- Do not add or remove npm dependencies.
- Do not modify `src-tauri/capabilities/default.json` or `src-tauri/tauri.conf.json`; the required window permissions and undecorated-window configuration already exist. If an unexpected runtime problem appears there, report it instead of broadening this task.
- Do not merge into `main`.
- Do not mark the work approved. Approval belongs to the human owner.

Implementation Requirements

1. Git branch

Create and work on a separate branch from the current application `main`.

Preferred branch name:
`visual-core/r0-step1-l0-shell`

Do not merge this branch into `main`.

The branch remains separate until the human owner explicitly says "OK" after manual validation.

Before editing, check `git status`.
Do not destroy or overwrite unrelated pre-existing local changes. If unrelated changes already exist, preserve them and report them.

2. Static default theme

Change `index.html` so the `<html>` element has the dark theme statically:

`<html lang="en" data-theme="dark">`

Current location:
`index.html:2`.

This is deliberately static.

Do not set the initial theme through React.
Do not add a `useEffect`, state variable, initialization script, localStorage read, or other runtime mechanism for the default theme in this step.

The light theme CSS must remain present for future theme switching, but step 1 does not provide a UI or state mechanism for switching themes.

3. Fix the four calibrated CSS tokens

The human owner has selected the R0 values produced by `applyCalibratedVars` with all four Dev Panel sliders at their default value `1.00` as the reference.

Source data:
`src/App.jsx:71-115`.

The four sliders all have default `1` in `DEV_VARS`:
- `workspaceLift = 1`
- `seam = 1`
- `textContrast = 1`
- `accentPresence = 1`

Apply the exact resulting values directly in the existing theme blocks in `src/index.css`.

DARK

R0 calculation:

`m1 = [14, 16, 19]`
`m2Delta = 13`
`workspaceLift = 1.00`

Therefore:

`[14 + 13, 16 + 13, 19 + 13]`
`= [27, 29, 32]`

Set:

`--m2-workspace: rgb(27, 29, 32);`
`--seam-light: rgba(255, 255, 255, 0.0900);`
`--text-secondary: rgba(231, 234, 238, 0.6000);`
`--accent-quiet: rgba(79, 131, 230, 0.1600);`

LIGHT

R0 calculation:

`m1 = [168, 173, 179]`
`m2Delta = 43`
`workspaceLift = 1.00`

Therefore:

`[168 + 43, 173 + 43, 179 + 43]`
`= [211, 216, 222]`

Set:

`--m2-workspace: rgb(211, 216, 222);`
`--seam-light: rgba(255, 255, 255, 0.3000);`
`--text-secondary: rgba(22, 25, 29, 0.6400);`
`--accent-quiet: rgba(47, 98, 196, 0.1400);`

Important:
Only these four calibrated values are fixed from `applyCalibratedVars`.

Do not derive or replace `--m1-background` from the JavaScript `FOUNDATION` object. `applyCalibratedVars` did not write `--m1-background`.

Therefore preserve the existing CSS `--m1-background` values:
- dark: `#0c0e11` (`src/index.css:103`)
- light: `#9ba0a7` (`src/index.css:139`)

Preserve all other palette tokens unless a directly necessary step-1 correction is discovered. Any such discovery must be reported before broadening the implementation.

4. L0 shell structure

Move only the L0 portion of R0 `ShellChrome` into `src/app/shell/`.

The active Phase 1 component tree after this step must conceptually remain:

`AppRoot`
  -> `RequiemShell`
      -> `WindowFrame`
          -> `ShellChrome`
          -> existing `MainLayout`

Do not route through the old R0 `App`.

5. WindowFrame

Use the existing R0 `.env` class for the outer application shell.

The active outer window-frame element must use:

`className="env"`

Do not create a replacement such as `.new-shell`, `.window-shell-v2`, or another parallel L0 root style.

Preserve `WindowFrame` as the structural owner of its children unless there is a concrete implementation reason not to; report any structural deviation.

6. ShellChrome

Implement the active L0 chrome under `src/app/shell/`.

Use the existing:

`className="env-chrome"`

Carry only:
- drag region
- minimize
- maximize/restore
- close

Do not carry the R0 Command Palette control.
Do not carry the R0 theme-toggle control.

The drag region should follow the existing R0 mechanism:

`<div data-tauri-drag-region className="flex-1 h-full" />`

The `data-tauri-drag-region` attribute must be on the intended empty draggable region, not on the entire header and not on the window-control buttons.

7. Native window API

Use:

`getCurrentWindow`

from:

`@tauri-apps/api/window`

Keep Tauri window-control ownership inside `src/app/shell/`.

Do not lift the native window object or handlers into `AppRoot`.

Required behavior:
- minimize -> `appWindow.minimize()`
- maximize/restore -> `appWindow.toggleMaximize()`
- close -> `appWindow.close()`

8. Window-control visuals

Reuse the R0 controls and current dependencies.

Use the existing Lucide icons:
- `Minus`
- `Square`
- `X`

Use the existing `.act` and `.act-critical` styles.

Minimize:
`className="act h-7 w-7 flex items-center justify-center ml-1"`

Maximize/restore:
`className="act h-7 w-7 flex items-center justify-center"`

Close:
`className="act act-critical h-7 w-7 flex items-center justify-center"`

The close control must therefore retain the existing critical hover treatment from `.act-critical:hover`.

Do not create new CSS specifically to recreate these same visual states.

9. Existing application composition

Preserve the current active entry point:
- `src/main.jsx` continues to render `AppRoot`.
- `src/main.jsx` continues to load `src/index.css`.
- `AppRoot` continues to use the Phase 1 shell.
- `MainLayout` remains inside the shell.

Do not bypass the Phase 1 structure.

10. Workspace placeholder

The workspace must continue to show exactly:

`REQUIEM VISUAL CORE`

Do not redesign the workspace in this step.

Do not introduce L2 R0 geometry yet.

11. CSS ownership

Continue using `src/index.css` as the R0 visual-language source.

Do not split L0 styles into a new stylesheet in this migration step.

Use the already existing:
- `.env`
- `.env-chrome`
- `.act`
- `.act-critical`

No parallel shell style system is allowed.

12. No runtime theme logic yet

The old disconnected R0 contains:

`document.documentElement.setAttribute("data-theme", theme);`

at `src/App.jsx:771`.

Do not migrate this behavior in step 1.

The default is defined statically in `index.html`.

A real theme-switching mechanism belongs to a later step when the relevant presentation command/state is deliberately introduced.

Preservation Requirements
- Preserve the Phase 1 application entry architecture.
- Preserve `src/App.jsx` as a disconnected migration source.
- Preserve the existing R0 CSS outside the explicitly required four token changes.
- Preserve both dark and light theme blocks.
- Preserve all current Tauri window permissions.
- Preserve the undecorated native window configuration.
- Preserve the `REQUIEM VISUAL CORE` placeholder.
- Preserve all work from previous Phase 1 skeleton steps.
- Preserve architecture separation: shell presentation must not acquire runtime/business/environment logic.
- Preserve git history.
- Do not merge the implementation branch into `main` before human approval.
- At session end, follow Decision #010 and update `docs/system/REQUIEM_ACTIVE_SESSION.md` in the adjacent `Requiem` repository. Record factual current state only and make clear that owner validation/merge is still pending if that is the case.

Validation Criteria

A. Claude checks itself

Before implementation:
1. Confirm current branch and `git status`.
2. Create/use the separate step-1 feature branch.
3. Confirm unrelated local changes, if any, are preserved.

Static file validation:
4. Confirm `index.html` contains:
   `<html lang="en" data-theme="dark">`.
5. Confirm there is no new React/default-theme initialization logic.
6. Confirm the eight calibrated CSS declarations exactly match the required values:

Dark:
- `--m2-workspace: rgb(27, 29, 32);`
- `--seam-light: rgba(255, 255, 255, 0.0900);`
- `--text-secondary: rgba(231, 234, 238, 0.6000);`
- `--accent-quiet: rgba(79, 131, 230, 0.1600);`

Light:
- `--m2-workspace: rgb(211, 216, 222);`
- `--seam-light: rgba(255, 255, 255, 0.3000);`
- `--text-secondary: rgba(22, 25, 29, 0.6400);`
- `--accent-quiet: rgba(47, 98, 196, 0.1400);`

7. Confirm dark `--m1-background` remains `#0c0e11`.
8. Confirm light `--m1-background` remains `#9ba0a7`.
9. Confirm the active shell uses `.env`.
10. Confirm the chrome uses `.env-chrome`.
11. Confirm the three native window buttons use `.act`, with close also using `.act-critical`.
12. Confirm only the intended drag area has `data-tauri-drag-region`.
13. Confirm `src/App.jsx` is still disconnected.
14. Confirm no L1/L2/L3/L4 R0 implementation was migrated.
15. Confirm `src-tauri/capabilities/default.json` is unchanged.
16. Confirm `src-tauri/tauri.conf.json` is unchanged.
17. Review `git diff` for scope violations.

Build/runtime validation:
18. Run:
   `npm run build`
   It must succeed.

19. Run:
   `npm run tauri dev`

20. Confirm the application window starts successfully.
21. Check terminal/build output for errors.
22. Check the frontend/Tauri console for errors that can be inspected from Claude Code.
23. Report warnings separately; do not silently classify warnings as errors or ignore new warnings.
24. Confirm the application still renders the `REQUIEM VISUAL CORE` placeholder.
25. Do not claim manual mouse/window-button validation that Claude did not actually perform.

Git validation:
26. Show the final application-repository `git status`.
27. Show the feature branch name.
28. Confirm the branch has not been merged into `main`.

Documentation/session validation:
29. At the end of the session, update `docs/system/REQUIEM_ACTIVE_SESSION.md` according to Decision #010.
30. Do not record owner approval unless the owner has given it.

B. Human owner checks manually in the running app

The owner will perform these checks after Claude reports completion:

1. Start/open the application with `npm run tauri dev`.
2. Confirm the application opens in the dark theme immediately, without a visible unthemed/default-color start.
3. Confirm `REQUIEM VISUAL CORE` is still visible.
4. Drag the application window by the empty chrome drag area.
5. Confirm dragging does not start when pressing/using a window-control button.
6. Click Minimize and confirm the window minimizes.
7. Restore the window.
8. Click Maximize and confirm the window maximizes.
9. Click the same control again and confirm the window restores.
10. Hover the regular window controls and confirm they use the existing R0 `.act` visual behavior.
11. Hover Close and confirm the existing critical/red `.act-critical` behavior appears.
12. Click Close and confirm the application window closes.
13. Reopen the application and confirm the dark default and placeholder remain correct.
14. Confirm there is no Command Palette button in the chrome yet.
15. Confirm there is no theme-toggle button in the chrome yet.
16. If all checks pass, the owner may explicitly say "OK". Only after that may the implementation be merged into `main`.

Optional Improvements
Approved Path:
Implement exactly the requirements above.

Optional Improvement:
If it can be done without changing appearance, architecture, or scope, add clear `aria-label` attributes to the three native window-control buttons:
- Minimize
- Maximize / Restore
- Close

Why It May Be Better:
It improves accessibility and semantic clarity without creating a new visual or architectural mechanism.

This is optional and must not delay or broaden step 1.

Final Report Format
Return a concise report with these sections:

1. Branch
- branch name
- latest commit hash, if committed
- explicitly state whether it is merged or not

2. Files Changed
- every changed file in `requiem-tauri`
- `docs/system/REQUIEM_ACTIVE_SESSION.md` separately if updated in the adjacent `Requiem` repository

3. Requirement-by-Requirement Result
For each implementation requirement:
- DONE
- NOT DONE
- DONE DIFFERENTLY

If DONE DIFFERENTLY, explain exactly how and why.

4. Calibrated Tokens
Print the final eight CSS values actually present in the file.

5. Claude Validation
Report:
- `npm run build` result
- `npm run tauri dev` result
- startup result
- terminal/console errors
- warnings
- static file checks
- confirmation that `src/App.jsx` remains disconnected
- confirmation that Tauri configuration/capabilities were not modified
- confirmation that L1/L2/L3/L4 were not migrated

6. Human Validation Required
Repeat only the short manual checks the owner still needs to perform in the running window:
- drag
- buttons excluded from drag
- minimize
- maximize/restore
- close
- dark default
- placeholder
- button hover visuals
- no palette/theme controls

7. Git State
Report final:
- current branch
- `git status`
- whether there are uncommitted changes
- explicitly: NOT MERGED INTO MAIN

8. Documentation State
State whether `docs/system/REQUIEM_ACTIVE_SESSION.md` was updated at session end.
Do not describe the implementation as approved until the human owner has approved it.
````
