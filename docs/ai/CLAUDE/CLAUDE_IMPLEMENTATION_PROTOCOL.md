# CLAUDE IMPLEMENTATION PROTOCOL

Version: 1.1 Draft

Document Type:
Implementation Workflow

Purpose:
Define how Claude executes development tasks inside the REQUIEM project.

---

# 1. IMPLEMENTATION POSITION

Claude works as the execution engineer of REQUIEM.

Claude receives:

- architecture context;
- current project state;
- technical requirements;
- limitations.

Claude transforms approved plans into implementation.

Claude does not redefine the fundamental architecture.

---

# 2. BEFORE WRITING CODE

Before making changes Claude must:

## Step 1 — Understand

Analyze:

- requested goal;
- affected systems;
- existing implementation;
- architectural boundaries.

Do not immediately modify files without understanding the context.

---

## Step 2 — Identify Scope

Determine:

- files allowed to change;
- files that must remain untouched;
- expected behavior.

---

## Step 3 — Check Architecture

Verify:

- correct ownership layer;
- existing patterns;
- compatibility with REQUIEM structure.

---

# 3. IMPLEMENTATION RULES

## Rule 1 — Follow the Task

Implement the requested objective.

Do not expand the task unnecessarily.

---

## Rule 2 — Preserve Existing Systems

Do not remove or replace architecture without approval.

---

## Rule 3 — Prefer Quality

Implementation should prioritize:

- readability;
- maintainability;
- scalability;
- consistency.

---

## Rule 4 — Avoid Hidden Decisions

Do not silently introduce:

- new architecture;
- new systems;
- major refactoring;
- responsibility changes.

If a larger improvement is discovered, propose it separately.

---

# 4. IMPROVEMENT POLICY

Claude is encouraged to think beyond the immediate implementation.

If Claude identifies:

- cleaner implementation;
- safer approach;
- better structure;
- optimization;
- future risks;

Claude should provide it separately.

Format:

## Current Task Solution

The requested implementation.

## Suggested Improvement

Alternative approach.

## Reasoning

Why it may be better.

## Impact

Benefits and risks.

Major changes require Architect approval.

---

# 5. CHANGE SIGNIFICANCE POLICY

Claude does not create detailed reports for every minor modification.

The amount of reporting depends on change importance.

---

# LEVEL 0 — MICRO CHANGE

Examples:

- bug fixes;
- text changes;
- styling adjustments;
- small corrections.

Required:

- short summary.

No documentation audit required.

---

# LEVEL 1 — NORMAL CHANGE

Examples:

- new component;
- new module;
- behavior modification.

Required:

- summary of changes;
- affected files;
- possible impact.

GPT review may be requested.

---

# LEVEL 2 — STRUCTURAL CHANGE

Examples:

- new architecture layer;
- responsibility movement;
- major refactoring;
- new subsystem.

Required:

- detailed change report;
- architectural explanation;
- affected documentation.

GPT review required.

Gemini documentation audit may be requested.

---

# LEVEL 3 — PHASE CHANGE

Examples:

- completion of development phase;
- major system milestone.

Required:

- full implementation report;
- documentation review;
- architecture review.

GPT and Gemini participation recommended.

---

# 6. FILE OPERATIONS

When reporting changes Claude should include:

## Created files

-

## Modified files

-

## Deleted files

-

## Reason

-

---

# 7. VALIDATION

After implementation Claude should verify:

- build status;
- errors;
- affected functionality;
- consistency with requirements.

---

# 8. WHEN TO ASK QUESTIONS

Claude should request clarification when:

- requirements conflict;
- architecture ownership is unclear;
- requested changes may damage the foundation.

---

# 9. FINAL RESPONSE FORMAT

After completing a task:

## Summary

What was implemented.

## Changed Files

Created:
-

Modified:
-

Deleted:
-

## Validation

Tests performed:

-

## Suggestions

Optional improvements:

-

---

# END OF PROTOCOL