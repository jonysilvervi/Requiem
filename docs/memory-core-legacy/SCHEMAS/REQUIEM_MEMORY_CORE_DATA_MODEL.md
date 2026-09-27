# REQUIEM MEMORY CORE DATA MODEL

Version: 0.1

Document Type:
Memory Data Structure Definition

Purpose:
Define the internal data structures and relationships used by the REQUIEM Memory Core system.

---

# 1. DATA MODEL PURPOSE

The REQUIEM Memory Core Data Model defines how project knowledge is represented internally.

The purpose is not only storing information.

The purpose is preserving meaningful relationships between:

- facts;
- events;
- decisions;
- states;
- changes;
- recovery points.

---

# 2. CORE DATA PRINCIPLE

Memory Core stores information as connected knowledge objects.

A memory item should answer:


What is it?

Why does it exist?

Where did it come from?

What does it affect?

What is its current status?


---

# 3. MEMORY OBJECT STRUCTURE

Every Memory Core object contains common metadata.

Base structure:


Memory Object

├── Identity
├── Content
├── Relations
├── Status
├── History
└── Metadata


---

# 4. COMMON MEMORY OBJECT FIELDS

Every memory object may contain:

## ID

Unique identifier.

Example:


DEC-001
STATE-001
EVENT-001


---

## Type

Defines object category.

Possible types:


IDENTITY

STATE

DECISION

EVENT

CONTEXT

CHECKPOINT


---

## Created

Creation date.

---

## Updated

Last modification date.

---

## Source

Origin of information.

Possible sources:


Human

AI Analysis

Project Scan

System Event


---

## Status

Current lifecycle state.

Possible values:


ACTIVE

SUPERSEDED

ARCHIVED

REJECTED


---

# 5. IDENTITY OBJECT

Purpose:

Store permanent project characteristics.

Example:


Type:

IDENTITY

Content:

REQUIEM is an ecosystem above game environments.

Protection:

Critical


Properties:

- rarely changes;
- highest protection;
- requires approval.

---

# 6. STATE OBJECT

Purpose:

Represent current project condition.

Example:


Type:

STATE

Current Phase:

Phase 1

Status:

Architecture preparation

Next Action:

Core Skeleton design


State objects are frequently updated.

---

# 7. DECISION OBJECT

Purpose:

Store important choices and reasoning.

Structure:


Decision

├── Problem

├── Chosen Solution

├── Reason

├── Alternatives

├── Consequences

└── Status


Example:


Decision:

S.T.A.L.K.E.R. 2 is an adapter.

Reason:

REQUIEM must remain game-independent.

Status:

Active.


---

# 8. EVENT OBJECT

Purpose:

Record meaningful project events.

Structure:


Event

├── Date

├── Description

├── Impact

└── Related Objects


Example:


Event:

Documentation foundation completed.

Impact:

Project continuity system created.


---

# 9. CONTEXT OBJECT

Purpose:

Store information required for correct understanding.

Context explains:

- relationships;
- background;
- restrictions;
- dependencies.

Example:


Context:

Memory Core is separated from the main application because current purpose is development continuity.


---

# 10. CHECKPOINT OBJECT

Purpose:

Represent recoverable project states.

Structure:


Checkpoint

├── Name

├── Date

├── Project State

├── Documentation State

├── Source State

├── Reason

└── Restore Information


Example:


Checkpoint:

CP-001

Name:

Documentation Foundation Complete

Purpose:

Safe state before implementation.


---

# 11. RELATION SYSTEM

Memory objects must be connected.

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


Relations explain project evolution.

---

# 12. IMPORTANCE LEVELS

Every object may have importance.

Levels:


CRITICAL

IMPORTANT

NORMAL

TEMPORARY


---

## CRITICAL

Examples:

- project identity;
- architecture rules;
- fundamental decisions.

Protection:

Maximum.

---

## IMPORTANT

Examples:

- milestones;
- phase changes;
- major systems.

Protection:

Controlled.

---

## NORMAL

Examples:

- technical changes.

Protection:

Standard.

---

## TEMPORARY

Examples:

- experiments;
- drafts.

Protection:

Low.

---

# 13. CONFIDENCE SYSTEM

Memory Core must distinguish certainty.

Possible values:


CONFIRMED

ANALYSIS

ASSUMPTION

UNKNOWN


Purpose:

Prevent assumptions from becoming false project history.

---

# 14. MEMORY EVOLUTION

Memory objects can change over time.

Example:


Decision:

Active

↓

Superseded

↓

Archived


History remains preserved.

---

# 15. FUTURE IMPLEMENTATION

The data model may later be represented as:

- JSON structures;
- database records;
- internal REQUIEM storage;
- API objects.

The current document defines logic, not implementation technology.

---

# 16. FINAL PRINCIPLE

Memory Core does not store isolated information.

It stores connected understanding.

The value of memory comes from relationships between information.

---

END OF DATA MODEL