# CLAUDE WORKING RULES

Practical rules for Claude as Executor, learned while working on REQUIEM (2026-09-24 … 2026-09-27).
They add to CLAUDE_ROLE.md and CLAUDE_IMPLEMENTATION_PROTOCOL.md and do not replace them.

## 1. Verify before acting

- Every task specification from GPT is checked against the files before it is executed: quotes, section numbers, line numbers, values, file names. GPT has produced invented quotes and misattributed ones before.
- Every claim relayed to the owner is checked against the files first. If it cannot be checked, say so.
- If a specification is wrong or conflicts with a decision or a standing rule, report it before executing. Do not silently "fix" the task.
- For code: check what the changed code needs at runtime (imports, DOM attributes, CSS variables, configuration, Tauri permissions), not only the files the task names.

## 2. Citations in documents

- Always the full form: "DOCUMENT.md, section N". Never a bare "(section N)" and never "section X and section Y" inheriting a file name — these become ambiguous when a document's own sections have the same numbers.
- For REQUIEM_KNOWLEDGE_MODEL.md run `python tools/refcheck_km.py memory-core/context` after any edit. Expected: "problems: 0".

## 3. Files

- Many documentation files use Windows line endings (CRLF). Edits must keep the line endings of the file; a whole-file line-ending change makes the diff unreadable.
- Before and after an edit, check the diff: only the intended lines may change.
- Approved documents are not edited. Their "Status:" lines stay as they were at approval; the current status is in memory-core/context/REQUIEM_DOCUMENT_REGISTRY.md.

## 4. Changes and approval

- Every change goes through a separate branch; the owner approves by merging (Decision #008).
- Recording an approval the owner gave explicitly in the conversation (approval records, SHA-256) is administrative metadata and may go straight to main.
- Decisions are recorded in docs/system/REQUIEM_DECISION_LOG.md only after the owner confirms them.

## 5. Session end

- Update docs/system/REQUIEM_ACTIVE_SESSION.md: what was done, where work stopped, what is next, open questions. Commit it (Decision #010).
- The next session continues from that file, not from chat history.

## 6. Talking to the owner

- The owner is not a programmer. Plain language, verdict first, no filler.
- Say plainly when something was not verified or when Claude made a mistake.
