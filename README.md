# REQUIEM

This repository is the single source of truth for the REQUIEM project. It replaces
passing zip archives between chats: every document here is versioned, and every
change goes through a pull request instead of a silent overwrite.

## What REQUIEM is

REQUIEM is an ecosystem, not a single application and not a S.T.A.L.K.E.R. 2 tool.

```
REQUIEM Ecosystem
├── Projects        (REQUIEM Application, REQUIEM Mod Pack, Memory Core Development Project, ...)
├── REQUIEM Engine
├── Tools
└── Memory Core
```

Games and external systems (S.T.A.L.K.E.R. 2 is the first one) are *environments* —
REQUIEM connects to them through adapters but does not own them.
Full definitions: `memory-core/context/REQUIEM_GLOSSARY.md`.

## Current state

| Area | State |
|---|---|
| REQUIEM Visual Core | **ACTIVE** — current work stream (Decision #011) |
| Execution Engine (PowerShell) | **FROZEN** (Decision #010) |
| Memory Core | **PAUSED** at Knowledge Model v0.5; resume point at the top of `memory-core/context/REQUIEM_KNOWLEDGE_MODEL.md` (Decision #009) |
| Architecture documentation | **FROZEN** for new documents; maintenance continues (Decision #010) |

Where work stopped and what is next: `docs/system/REQUIEM_ACTIVE_SESSION.md`.
Decisions: `docs/system/REQUIEM_DECISION_LOG.md`.

## Repository layout

| Folder | What it is | Status |
|---|---|---|
| `memory-core/` | The Memory Core system itself: its architecture, data model, protocols and the actual document set (Foundation Decisions, Glossary, Knowledge Model, Document Registry, etc.), plus its scanner/analyzer code and database. | **Current source of truth.** Document status is defined by `memory-core/context/REQUIEM_DOCUMENT_REGISTRY.md`, not by the "Status:" line inside each file. |
| `docs/ai/` | AI role definitions: GPT (Architect), Claude (Executor), Gemini (Support), and the shared workflow/session/documentation rules. | Current. |
| `docs/system/` | Ecosystem-level history: decision log, changelog, documentation index, start-here guide. | Current as a historical record. |
| `docs/app/` | REQUIEM Application (the Tauri desktop app) — current state snapshot and Phase 1 planning docs. The code itself is in the separate repository `jonysilvervi/requiem-tauri`. | Verified against the code on 2026-09-27 (including `src-tauri`). Open findings: `docs/app/NOTES.md`. Visual Core migration plan: `docs/app/R0_MIGRATION_PLAN.md`. |
| `docs/memory-core-legacy/` | The original v0.1 concept documents for Memory Core (Constitution, MVP, early Architecture/Protocols/Schemas/Roadmap). | **Superseded by `memory-core/context/`. Kept for history only — do not use as current reference.** |

## Reading order for a new session (human or AI)

1. `docs/system/REQUIEM_ACTIVE_SESSION.md` — where work stopped and what is next.
2. `docs/ai/COMMON/REQUIEM_AI_MASTER_CONTEXT.md` — identity, principles, current state.
3. `docs/ai/` — who does what (GPT / Claude / Gemini / human).
4. For the task at hand: `docs/app/` for the application, `memory-core/context/` for Memory Core (start with `REQUIEM_GLOSSARY.md` and `REQUIEM_DOCUMENT_REGISTRY.md`).

At the end of every work session, `docs/system/REQUIEM_ACTIVE_SESSION.md` is updated and committed.

## Working rules

- Every document's real status lives in the Document Registry, not in its own header.
- No claim about a document counts unless it is a literal quote with a `FILE.md, section N` reference.
- Nothing is APPROVED or TRUSTED until the project owner confirms it, in a pull request.
- Known contradictions between documents are not resolved silently — see each file's own notes and the Document Registry.
