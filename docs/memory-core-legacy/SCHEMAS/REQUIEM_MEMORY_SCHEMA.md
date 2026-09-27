# REQUIEM MEMORY SCHEMA

Version: 0.1

Document Type:
Memory Structure Definition

Purpose:
Define the fundamental types of information stored, managed and processed by the REQUIEM Memory Core system.

---

# 1. MEMORY MODEL

REQUIEM Memory Core does not store information as a simple archive.

It organizes project knowledge into different memory categories.

Each category has:

- purpose;
- importance;
- lifecycle;
- protection level.

---

# 2. CORE MEMORY TYPES

The Memory Core consists of the following primary memory types:


IDENTITY
STATE
DECISION
EVENT
CONTEXT
CHECKPOINT


---

# 3. IDENTITY MEMORY

Purpose:

Store the fundamental identity of REQUIEM.

Identity memory answers:

"What is this project?"

Contains:

- project purpose;
- core principles;
- long-term vision;
- fundamental restrictions.

Examples:


REQUIEM is not a S.T.A.L.K.E.R. 2-only application.

Games are environments.
REQUIEM is the intelligence layer above them.


Characteristics:

- Rarely changes.
- Highest protection level.
- Requires explicit approval for modification.

---

# 4. STATE MEMORY

Purpose:

Store the current condition of the project.

State memory answers:

"Where are we now?"

Contains:

- current phase;
- active objectives;
- completed milestones;
- current blockers;
- next actions.

Example:


Phase:
1

Status:
Architecture approved

Next:
Core Skeleton implementation


Characteristics:

- Frequently updated.
- Must remain synchronized with reality.

---

# 5. DECISION MEMORY

Purpose:

Store important project decisions and their reasoning.

Decision memory answers:

"Why was this chosen?"

Contains:

- decision;
- reason;
- alternatives considered;
- consequences;
- current status.

Example:


Decision:

S.T.A.L.K.E.R. 2 remains an adapter.

Reason:

REQUIEM must remain game-independent.


Characteristics:

- Long-term memory.
- Cannot be silently deleted.
- Previous decisions remain part of history.

---

# 6. EVENT MEMORY

Purpose:

Store important project events.

Event memory answers:

"What happened?"

Examples:

- phase completion;
- architecture approval;
- major system creation;
- important changes.

Event memory does not store every small modification.

Only meaningful events are recorded.

---

# 7. CONTEXT MEMORY

Purpose:

Preserve information required for correct understanding.

Context memory answers:

"What does this information depend on?"

Contains:

- relationships;
- explanations;
- dependencies;
- historical background.

Example:


Memory Core exists separately from the main application because current purpose is development continuity.


---

# 8. CHECKPOINT MEMORY

Purpose:

Create recoverable project states.

Checkpoint memory answers:

"Where can we safely return?"

Contains:

- date;
- project state;
- documentation state;
- source state;
- reason for checkpoint creation.

Example:


Checkpoint:

Documentation Foundation Complete

Status:

Stable


---

# 9. MEMORY PRIORITY LEVELS

Not all information has equal importance.

Memory Core uses priority levels:

## CRITICAL

Examples:

- project identity;
- architecture laws;
- fundamental decisions.

Protection:
Maximum.

---

## IMPORTANT

Examples:

- phase states;
- major milestones;
- system changes.

Protection:
Controlled.

---

## NORMAL

Examples:

- technical changes;
- temporary progress information.

Protection:
Standard.

---

## TEMPORARY

Examples:

- experiments;
- drafts;
- unfinished ideas.

Protection:
Low.

---

# 10. MEMORY RELATIONSHIPS

Memory Core must understand relationships between information.

Example:


Decision

↓

Architecture Rule

↓

Implementation

↓

Event

↓

Checkpoint


Information should not exist isolated.

---

# 11. MEMORY VALIDITY

Each memory item should have:

- creation date;
- source;
- status;
- confidence.

Possible statuses:


ACTIVE

SUPERSEDED

ARCHIVED

REJECTED


---

# 12. MEMORY CORE OBJECTIVE

The goal of the schema:

Create a system where AI and humans can quickly understand:

- what REQUIEM is;
- where it is;
- why it is built this way;
- what happened;
- what can be done next.

---

END OF MEMORY SCHEMA