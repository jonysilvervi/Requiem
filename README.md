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

## Repository layout

| Folder | What it is | Status |
|---|---|---|
| `memory-core/` | The Memory Core system itself: its architecture, data model, protocols and the actual document set (Foundation Decisions, Glossary, Knowledge Model, Document Registry, etc.), plus its scanner/analyzer code and database. | **Current source of truth.** Document status is defined by `memory-core/context/REQUIEM_DOCUMENT_REGISTRY.md`, not by the "Status:" line inside each file. |
| `docs/ai/` | AI role definitions: GPT (Architect), Claude (Executor), Gemini (Support), and the shared workflow/session/documentation rules. | Current. |
| `docs/system/` | Ecosystem-level history: decision log, changelog, documentation index, start-here guide. | Current as a historical record. |
| `docs/app/` | REQUIEM Application (the Tauri desktop app) — current state snapshot and Phase 1 planning docs. | **Last confirmed 2026-09-23. Verify against the actual app repository before relying on it.** |
| `docs/memory-core-legacy/` | The original v0.1 concept documents for Memory Core (Constitution, MVP, early Architecture/Protocols/Schemas/Roadmap). | **Superseded by `memory-core/context/`. Kept for history only — do not use as current reference.** |

## Reading order for a new session (human or AI)

1. `memory-core/context/REQUIEM_GLOSSARY.md` — terminology, so nothing gets misread.
2. `memory-core/context/REQUIEM_FOUNDATION_DECISIONS.md` — the approved architectural decisions (FD-B1…FD-B8).
3. `memory-core/context/REQUIEM_DOCUMENT_REGISTRY.md` — the real status of every document.
4. `docs/ai/` — who does what (GPT / Claude / Gemini / human).
5. Whatever the current task actually concerns.

## Working rules

- Every document's real status lives in the Document Registry, not in its own header.
- No claim about a document counts unless it is a literal quote with a `FILE.md, section N` reference.
- Nothing is APPROVED or TRUSTED until the project owner confirms it, in a pull request.
- Known contradictions between documents are not resolved silently — see each file's own notes and the Document Registry.
