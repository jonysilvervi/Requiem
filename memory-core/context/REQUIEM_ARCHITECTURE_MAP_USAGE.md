# REQUIEM ARCHITECTURE MAP USAGE

Version: 0.1

Status: DRAFT


---

# 1. Purpose


Architecture Map Usage defines how Memory Core uses Architecture Map during project understanding.


The document describes:


- which layers can read Architecture Map;
- which layers can use its information;
- who can modify it;
- how architectural knowledge evolves.



---

# 2. Core principle


Architecture Map is a source of architectural understanding.


It is not:


- a file database;
- a replacement for project documentation;
- a replacement for source code;
- an automatic generated structure.



Architecture Map provides context for understanding project changes.



---

# 3. Architecture Map position in Memory Core


Architecture Map is used after project observation and before final knowledge update.


Flow:



Project

↓

Scanner

↓

Snapshot

↓

Comparison

↓

Change Report

↓

Analysis

↓

Architecture Map

↓

Human Review

↓

Context Update

↓

Memory



Architecture Map provides meaning to detected changes.



---

# 4. Layer access rules


## Scanner


Scanner does not use Architecture Map.


Reason:


Scanner only observes project state.


It collects:


- files;
- metadata;
- hashes;
- structure information.



---

## Storage


Storage does not use Architecture Map.


Snapshots preserve project states only.



---

## Comparison


Comparison does not use Architecture Map.


Comparison answers:


"What changed?"


It does not answer:


"What does the change mean?"



---

## Change Report


Change Report does not require Architecture Map.


It records detected changes.



---

## Analysis


Analysis uses Architecture Map.


Purpose:


Understand possible impact of changes.


Example:


Without Architecture Map:



config/player.ini changed



With Architecture Map:



Player System configuration changed




---

## Human Review


Human Review uses Architecture Map when evaluating analysis results.


Human decides whether interpretation is correct.



---

## Context Update


Context Update does not automatically modify Architecture Map.


Architecture changes require separate approval.



---

# 5. Architecture Map ownership


Architecture Map belongs to the project knowledge layer.


Ownership:



Human

↓

Architecture Knowledge

↓

Architecture Map



Tools may suggest changes.


Human approves architectural changes.



---

# 6. Modification rules


Architecture Map cannot be modified automatically.


Allowed:


- human creation;
- human editing;
- approved architectural updates.



Not allowed:


- automatic rewriting;
- engine-generated replacement;
- scanner updates;
- analysis automatic changes.



---

# 7. Relationship with Analysis Layer


Analysis uses Architecture Map as context.


Example:


Change:



quest_manager.cpp modified



Without knowledge:



File changed



With Architecture Map:



Quest System logic changed
Possible impact:
quest progression behavior




Analysis provides suggestions.


Architecture Map provides meaning.



---

# 8. Relationship with Engine Integration


Future engine adapters may provide information.


However:


Engine data is a source of information, not architectural truth.


The process:



Engine Information

↓

Suggestion

↓

Human Review

↓

Architecture Map Update




---

# 9. Multi-project usage


Each project has its own Architecture Map.


Example:



REQUIEM

|

├── STALKER 2

| └── Architecture Map

|

├── Future Game

| └── Architecture Map



Shared knowledge does not replace project-specific architecture.



---

# 10. Current state


Current state:


- Architecture Map format defined;
- Architecture Map usage defined;
- no approved project map exists;
- no automatic generation exists.



The first architecture map requires human creation.



---

# 11. Future development


Future improvements may include:


- architecture suggestions;
- dependency discovery;
- engine integration;
- automatic validation;
- impact prediction.



All future features must preserve human authority.



---

# 12. Final vision


Architecture Map connects project reality with project understanding.


Files show existence.


Architecture Map shows meaning.


Analysis uses meaning to understand change.


Memory preserves approved understanding.