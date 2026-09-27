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
- Owner performed manual validation of [TASK-001] on 2026-09-27 (`npm run tauri dev`, checklist in TASK-001 section "B"). Passed: drag, buttons excluded from drag, minimize, maximize/restore, close, `REQUIEM VISUAL CORE` placeholder, no Command Palette/theme-toggle controls, button hover visuals (close hover confirmed red). Did NOT pass: dark theme is not visible immediately — the window shows a white flash for about a second before the calibrated dark colors paint. Logged as [ISS-008] (docs/app/NOTES.md, finding 8); root cause is the native window (`src-tauri/tauri.conf.json`, `"transparent": true`, no background color) being shown before WebView2's first paint, not the static `data-theme` itself. Owner decision: do not fix inside TASK-001; two candidate fixes are recorded in ISS-008, both requiring changes to the frozen `src-tauri` (Decision #010).
- Additional observation from validation: after clicking Maximize/Restore, a blue keyboard-focus outline (existing R0 `:focus-visible` rule in `src/index.css`) remains visible around the button. Not fixed, not filed as a separate ISS — recorded as an observation in TASK-001's passport.
- [TASK-001] Object Status updated to AWAITING CHECK in REQUIEM_DOCUMENTATION_INDEX.md. Owner "OK" and GPT report review are still pending before merge into `main`.
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

1. Owner forwards Claude's final report on [TASK-001] to GPT for review, including [ISS-008] (white flash before dark theme paints) and the unfiled Maximize/Restore focus-outline observation.
2. Owner and GPT decide how to handle [ISS-008]: fix now via a separate task against the frozen `src-tauri` (requires explicitly unfreezing that file for the fix), or accept and defer.
3. After owner says "OK" and GPT review, merge `visual-core/r0-step1-l0-shell` into `main`; then plan [STEP-R0-02] (L1 NAVIGATION).
4. Owner: answer [Q-001] — where the PowerShell Execution Engine code lives.

---

# OPEN QUESTIONS

- [Q-001] Location of the PowerShell Execution Engine code (related: [ISS-006]).

---

# LAST UPDATE

2026-09-27

---

# END OF SESSION