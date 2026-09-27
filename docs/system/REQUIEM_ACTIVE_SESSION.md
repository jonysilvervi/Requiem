# REQUIEM ACTIVE SESSION

Version: 1.1 Draft

Document Type:
Current Work Session State

Purpose:
Preserve the current development position between work sessions.

Rule:
This file is updated at the end of every work session (Decision #010). A new session reads it right after README.md.

---

# CURRENT SESSION

Date:

2026-09-27

---

# CURRENT FOCUS

REQUIEM Visual Core (Decision #011).

---

# FROZEN

- Execution Engine (PowerShell) — frozen (Decision #010).
- Memory Core development — paused at REQUIEM_KNOWLEDGE_MODEL.md v0.5; resume point at the top of that document (Decision #009).
- New architecture documentation — frozen (Decision #010).

---

# COMPLETED THIS SESSION

- [TASK-001] / [STEP-R0-01] implemented by Claude Code in `requiem-tauri`: branch `visual-core/r0-step1-l0-shell`, commit `6b02445`. L0 window chrome (drag region, minimize, maximize/restore, close) moved into `src/app/shell/ShellChrome.jsx`; default theme set statically to dark in `index.html`; the four calibrated color tokens fixed in `src/index.css` for dark and light. `npm run build` succeeded. Branch is NOT merged into `main`.
- Owner performed manual validation of [TASK-001] on 2026-09-27 (`npm run tauri dev`, checklist in TASK-001 section "B"). Passed: drag, buttons excluded from drag, minimize, maximize/restore, close, `REQUIEM VISUAL CORE` placeholder, no Command Palette/theme-toggle controls, button hover visuals (close hover confirmed red). Check 6 (dark default with no flash) initially did NOT pass — logged as [ISS-008] (docs/app/NOTES.md, finding 8).
- [ISS-008] resolved on 2026-09-27. Root cause not conclusively isolated between two hypotheses (transparent window shown before WebView2 first paint, or dark background only present in `src/index.css` loaded via the JS module graph); fixed by elimination, in order, all on branch `visual-core/r0-step1-l0-shell`: (1) inline dark background in `index.html` (GPT-reviewed Variant A, commit `2fb8947`) — did not fix it; (2) owner exception to Decision #010 — window `backgroundColor` in `tauri.conf.json` (commit `0824b1b`) — did not fix it alone; (3) `transparent: false` (commit `23eb7ea`) — partial improvement only; (4) window created hidden (`visible: false`) and shown via `getCurrentWindow().show()` in `src/app/shell/WindowFrame.jsx` after first render, plus the new `core:window:allow-show` capability in `src-tauri/capabilities/default.json` (commit `aa12566`) — fixed it, confirmed by the owner via frame-by-frame video review (no white frame, no transparent phase). `src-tauri/src/lib.rs` was not touched. Check 6 is now DONE.
- Residual risk from the ISS-008 fix: if the frontend throws before the `WindowFrame.jsx` `useEffect` runs, `show()` is never called and the window never becomes visible, with no native fallback to indicate the app is running.
- `src-tauri/tauri.conf.json` and `src-tauri/capabilities/default.json` were edited to resolve [ISS-008] despite TASK-001 explicitly forbidding it, under a one-time owner exception to the `src-tauri` freeze (Decision #010) granted 2026-09-27, scoped to exactly this fix — flagged for GPT review.
- Additional observation from validation: after clicking Maximize/Restore, a blue keyboard-focus outline (existing R0 `:focus-visible` rule in `src/index.css`) remains visible around the button. Not fixed, not filed as a separate ISS — recorded as an observation in TASK-001's passport.
- [TASK-001] Object Status remains AWAITING CHECK in REQUIEM_DOCUMENTATION_INDEX.md. Owner "OK" and GPT report review are still pending before merge into `main`.
- Documentation moved into the repository jonysilvervi/Requiem (Decision #008).
- Memory Core put into a clean pause: Knowledge Model v0.5 with the recorded boundary decision and a resume point; development protocol, state and registry updated.
- Ecosystem documentation brought up to date: Decision Log, Changelog, this file, reading order.
- REQUIEM_DOCUMENT_REGISTRY.md v0.7 approved by the human owner.
- REQUIEM Application documents checked against the code: Phase 1 skeleton exists, build works; REQUIEM_CURRENT_STATE_SNAPSHOT.md v0.3, docs/app/NOTES.md.
- Application code put under git: repository jonysilvervi/requiem-tauri.
- Phase 1 stays open until the foundation is polished (Decision #012).
- R0 migration plan accepted, option A (Decision #013, docs/app/R0_MIGRATION_PLAN.md).
- GPT project instructions saved (docs/ai/GPT/GPT_PROJECT_INSTRUCTIONS.md); Claude working rules recorded (docs/ai/CLAUDE/CLAUDE_WORKING_RULES.md); citation checker added (tools/refcheck_km.py).
- New GPT chat restored the full context from the repository alone (context recovery test passed).
- Information standard recorded (Decision #014 [ED-014]); identifier registry initialized in docs/system/REQUIEM_DOCUMENTATION_INDEX.md.
- Ecosystem roadmap saved: docs/system/REQUIEM_ROADMAP.md (drafted by GPT, owner-confirmed area statuses) and its visual view docs/system/REQUIEM_ROADMAP.html.
- Practical working cycle recorded: docs/ai/COMMON/REQUIEM_AI_WORKFLOW.md, section 8; shown in the roadmap (Markdown and visual view).
- Claude Code session rules written: CLAUDE.md in jonysilvervi/requiem-tauri (merged).
- Owner: the PowerShell engine works only with S.T.A.L.K.E.R. 2. GPT recommends treating its S.T.A.L.K.E.R.-specific part as a S.T.A.L.K.E.R. 2 adapter over a generic Execution Engine; not decided, to be decided when the engine is unfrozen (related: O6, [Q-001]).
- Reference for the four calibrated colors decided by the owner: R0 values with all four Dev Panel sliders at their default 1.00 (used by [TASK-001]).

---

# NEXT ACTIONS

1. All 9 owner manual-validation checks for [TASK-001] now pass, including check 6 after the [ISS-008] fix. Owner forwards the final report (including the `src-tauri` exception) to GPT for review.
2. After GPT review and the owner's explicit "OK", merge `visual-core/r0-step1-l0-shell` into `main`; then plan [STEP-R0-02] (L1 NAVIGATION).
3. Owner: answer [Q-001] — where the PowerShell Execution Engine code lives.

---

# OPEN QUESTIONS

- [Q-001] Location of the PowerShell Execution Engine code (related: [ISS-006]).

---

# LAST UPDATE

2026-09-27

---

# END OF SESSION