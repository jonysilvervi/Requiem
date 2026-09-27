# GPT REVIEW CHECKLIST

Version: 1.0 Draft

Document Type:
Implementation Review Checklist

Purpose:
Define how GPT reviews completed implementation work in REQUIEM.

---

# 1. ARCHITECTURE CHECK

## Responsibility

Does every changed file belong to the correct layer?

Check:

- Is UI logic inside Visual Core?
- Is system logic outside UI?
- Is environment-specific logic outside Core?

---

## Layer Separation

Verify that the change does not mix:

- Visual Core
- Intelligence Layer
- Operations Runtime
- Execution Engine
- Environment Adapter

---

# 2. FOUNDATION CHECK

Verify:

- Existing architecture was preserved.
- No unnecessary restructuring was introduced.
- No temporary solutions became permanent without approval.

---

# 3. CODE QUALITY CHECK

Review:

- clarity;
- maintainability;
- naming;
- structure;
- unnecessary complexity.

The goal is not minimum code.

The goal is strong code.

---

# 4. REQUIEM PHILOSOPHY CHECK

Ask:

Does this change strengthen REQUIEM as an ecosystem?

Does it preserve:

- premium experience;
- intentional design;
- scalability;
- architectural clarity?

---

# 5. VISUAL CHECK

For visual changes:

Verify:

- visual decisions have purpose;
- effects support the experience;
- animations support system state;
- complexity is controlled.

Premium does not mean excessive.

Premium means intentional.

---

# 6. EXECUTION CHECK

Before accepting implementation:

Confirm:

- expected functionality exists;
- validation was performed;
- affected files are documented.

---

# 7. DOCUMENTATION CHECK

After significant changes:

Update:

- current state;
- architecture notes;
- decisions history.

---

# 8. FINAL REVIEW QUESTION

Before approval:

"Would this decision make REQUIEM stronger if the project continued for years?"

If uncertain:

Further analysis is required.

---

# END OF CHECKLIST