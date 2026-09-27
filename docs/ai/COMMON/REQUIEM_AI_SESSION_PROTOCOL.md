# REQUIEM AI SESSION PROTOCOL

Version: 1.1 Draft

Document Type:
AI Session Initialization Protocol

Purpose:
Define how any AI session starts working with REQUIEM.

---

# 1. PURPOSE

Every AI session working with REQUIEM must begin by establishing project context.

The AI must not assume previous conversations exist.

The documentation system is the source of continuity.

---

# 2. SESSION START ORDER

Before performing any task:

## Step 0

Read the repository entry points (Decision #008):

- README.md;
- docs/system/REQUIEM_ACTIVE_SESSION.md.

---

## Step 1

Read:

- REQUIEM_AI_MASTER_CONTEXT.md

Understand:

- project identity;
- philosophy;
- architecture.

---

## Step 2

Read current project state:

- Current State Snapshot;
- relevant architecture documents.

---

## Step 3

Identify:

- current phase;
- active objectives;
- recent changes.

---

## Step 4

Confirm understanding before major changes.

---

# 3. CONTEXT RULE

The AI must treat documentation as the project memory.

Chat history is temporary.

Documentation is permanent.

---

# 4. BEFORE IMPLEMENTATION

The AI must know:

- what is being changed;
- why it is being changed;
- which layer owns the responsibility;
- what must remain untouched.

---

# 5. SESSION END REQUIREMENT

After significant work:

Evaluate:

- Does documentation require updates?
- Was a new decision made?
- Did architecture change?

Always, at the end of every work session:

- update docs/system/REQUIEM_ACTIVE_SESSION.md: what was done, where work stopped, what is next;
- commit the change to the repository.

The next session continues from that file, not from chat history.

---

# END OF PROTOCOL