# R0 migration plan — Visual Core

Status: accepted by the owner on 2026-09-27 (Decision #013).
Prepared by: GPT (Architect), checked against the code by Claude (Executor).

## Goal

Carry the visual prototype R0 (`src/App.jsx`, `src/index.css` in `jonysilvervi/requiem-tauri`)
into the Phase 1 structure layer by layer. The application must build and start after every step.

`src/App.jsx` is not connected to the entry point since 2026-09-22 (`NOTES.md`, finding 1).
It is not reconnected as a whole.

## What moves where

| R0 part | New owner | What is carried |
|---|---|---|
| L0 `ShellChrome` | `src/app/shell/` | drag region, minimize / maximize / close, window frame |
| L1 `Navigation` + `NAV_ITEMS` | `src/app/modules/navigation/` | visual navigation and its presentation state; no `ai` destination |
| L2 `WorkArea` | `src/app/workspace/` | geometry: Context / Structure / Object / Control / Feedback |
| L3 `Intelligence` | `src/app/modules/intelligence/` | presentation surface only (collapsed / engaged / full) |
| L4 `CommandPalette` | `src/app/modules/system/` | temporary system surfaces and commands the Visual Core really performs |
| R0 `App()` composition | `src/app/AppRoot.jsx` | cross-module presentation state only, no runtime or business logic |
| R0 CSS | `src/index.css` (stays) | not split during the component migration |

## What is not carried (Decision #013, option A)

- chat state and fake replies: `messages`, `handleSend`;
- assistant modes and personas: `assistantMode`, `profile`, Companion / Operator / Ambient;
- Dev Panel (calibration sliders); its values are fixed in CSS;
- data and commands that pretend to control systems: `CONTEXTS` actions such as "Reinstall",
  "Cancel operation", "Apply"; palette commands `deploy-prz`, `scan-conflicts`, `clear-cache`.
  Where data does not exist yet, the interface shows nothing or states "not connected".

## Steps

1. **L0 SHELL + theme + tokens.** Window chrome moves into `src/app/shell/`
   (`getCurrentWindow()`, drag region, minimize, maximize/restore, close). In the same step:
   - the theme attribute is set on `<html>` (default `dark`): all palette colors in
     `src/index.css` exist only inside `[data-theme="dark"]` / `[data-theme="light"]`, and
     nothing sets the attribute since R0 was disconnected;
   - the four calibrated colors (`--m2-workspace`, `--seam-light`, `--text-secondary`,
     `--accent-quiet`) are fixed in CSS. R0 computed them in `applyCalibratedVars`
     (`src/App.jsx`, lines 99–115); the values on screen differed slightly from the CSS
     defaults. Which values are the reference is set by the task specification.

   Workspace keeps the placeholder "REQUIEM VISUAL CORE".
2. **L1 NAVIGATION.** Navigation zones switch; Workspace works in every state.
3. **L2 WORKSPACE.** Geometry of R0; only honest state, no fake actions.
4. **L4 SYSTEM (safe part).** Command Palette with real presentation commands only
   (navigation, settings, theme, close).
5. **L3 INTELLIGENCE.** Presentation surface without conversation semantics.
6. **Cleanup.** Delete `src/App.jsx` once L0–L4 work in the new structure (git keeps its history).
   Then, as a separate small change, remove CSS used only by removed mechanisms
   (including the Companion / Operator / Ambient state rules).

## Validation after every step

`npm run build` succeeds; `npm run tauri dev` starts the window; the behaviour of the step works;
nothing from the previous steps broke. Step 1 also: the window moves by its drag region, the
buttons are not part of the drag region, minimize / maximize / close work, colors are applied.

## Where work stands

Next: GPT writes the task specification for step 1. Claude executes it in a new session.
