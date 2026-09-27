# CLAUDE TASK TEMPLATE

Version: 1.0 Draft

Document Type:
Implementation Task Template

Purpose:
Define the standard format for technical tasks given to Claude.

---

# TASK INFORMATION

## Task Name

[Short descriptive name]

---

# OBJECTIVE

## Goal

Describe exactly what must be achieved.

The objective should describe the desired result, not only the implementation method.

---

# CONTEXT

## Background

Explain:

- why this task exists;
- what problem it solves;
- how it fits REQUIEM development.

---

# ARCHITECTURE CONTEXT

## Responsible Layer

Define the REQUIEM layer affected.

Examples:

- Visual Core
- Intelligence Layer
- Operations Runtime
- Execution Engine
- Environment Adapter
- Documentation System

---

## Architectural Reasoning

Explain why this responsibility belongs to this layer.

---

# ALLOWED CHANGES

Files and systems Claude may modify:


[List]


---

# FORBIDDEN CHANGES

Files and systems Claude must not modify:


[List]


---

# IMPLEMENTATION REQUIREMENTS

Describe:

- required behavior;
- technical expectations;
- constraints;
- important details.

---

# PRESERVATION REQUIREMENTS

Specify what must remain unchanged:

Examples:

- existing visual language;
- architecture boundaries;
- current behavior;
- naming conventions.

---

# VALIDATION CRITERIA

The task is complete when:

- build succeeds;
- expected behavior works;
- architecture remains intact;
- modified files are documented.

---

# OPTIONAL IMPROVEMENTS

Claude may suggest improvements here.

If Claude identifies:

- cleaner implementation;
- safer approach;
- better structure;
- future risks;

it should describe them separately.

Do not apply major architectural changes without approval.

---

# FINAL REPORT FORMAT

After completion Claude should provide:

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

# END OF TASK TEMPLATE