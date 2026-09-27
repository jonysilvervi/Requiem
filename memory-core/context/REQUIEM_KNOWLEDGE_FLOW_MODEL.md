# REQUIEM KNOWLEDGE FLOW MODEL

Version: 0.1

Status: DRAFT


---

## 1. Purpose


Knowledge Flow Model defines how information moves through REQUIEM systems and becomes preserved knowledge.


The purpose of this model:

- define the lifecycle of information;
- separate facts from interpretation;
- define validation points;
- prevent uncontrolled memory changes.



---

## 2. Core principle


REQUIEM separates:


Information

↓

Understanding

↓

Knowledge



Raw information can be collected automatically.

Knowledge requires validation.


Memory Core preserves approved knowledge, not uncontrolled assumptions.



---

## 3. Knowledge lifecycle


The general flow:


Project

↓

Observation

↓

Storage

↓

Comparison

↓

Change Report

↓

Analysis

↓

Human Review

↓

Context Update

↓

Memory Core



Each stage has a separate responsibility.



---

## 4. Stage 1 — Observation


Observation collects facts from external systems.


Examples:


- file state;
- configuration state;
- project structure;
- metadata;
- timestamps;
- hashes.



Observation answers:


"What exists?"


Observation does not interpret meaning.



---

## 5. Stage 2 — Storage


Storage preserves observed states.


Examples:


- snapshots;
- historical states;
- project versions.



Storage answers:


"What did the project look like at a specific moment?"


Stored states must remain immutable.



---

## 6. Stage 3 — Comparison


Comparison identifies differences between stored states.


Examples:


- added files;
- removed files;
- modified files;
- unchanged files;
- unverified changes.



Comparison answers:


"What changed?"



Comparison does not explain why the change happened.



---

## 7. Stage 4 — Change Report


Change Report converts technical differences into structured change records.


Examples:


- CHG records;
- affected files;
- change scope;
- review status.



Change Report answers:


"What specific change should be reviewed?"



---

## 8. Stage 5 — Analysis


Analysis evaluates changes using predefined rules.


Examples:


- affected system;
- possible impact;
- change category;
- architectural area.



Analysis answers:


"What could this change mean?"


Analysis produces suggestions, not decisions.



---

## 9. Stage 6 — Human Review


Human review is the validation boundary.


A person decides:


- whether the interpretation is correct;
- whether the change is important;
- whether knowledge should be stored.



Human approval is required before memory updates.



---

## 10. Stage 7 — Context Update


Context Update transfers approved knowledge into Memory Core.


Possible updates:


- project context;
- events;
- documented state;
- approved knowledge.



Context Update does not create knowledge.

It preserves already approved knowledge.



---

## 11. Stage 8 — Memory Core


Memory Core stores accumulated understanding.


Examples:


- project history;
- architecture knowledge;
- decisions;
- patterns;
- experience.



Memory Core represents what REQUIEM knows about its ecosystem.



---

## 12. Facts and knowledge separation


REQUIEM separates objective facts and interpreted knowledge.


### Facts


Examples:


- file hash changed;
- configuration exists;
- component was added;
- snapshot was created.



Facts can be collected automatically.



### Knowledge


Examples:


- this component belongs to a specific system;
- this design decision affects future development;
- this pattern can be reused.



Knowledge requires validation.



---

## 13. Multiple project knowledge flow


REQUIEM supports multiple independent projects.


Example:


Project A

↓

Project knowledge


Project B

↓

Project knowledge


Project C

↓

Project knowledge



Shared knowledge:


- architectural patterns;
- reusable solutions;
- development experience.



---

## 14. Relationship with external systems


External systems may provide information to REQUIEM.


Examples:


- game engines;
- development tools;
- project applications.


The integration model:


External System

↓

Adapter

↓

Memory Core



External systems provide data.

Memory Core preserves and understands knowledge.



---

## 15. Current implementation state


Implemented:


- Observation through Scanner;
- Storage through Snapshot System;
- Comparison Layer;
- Change Report Layer;
- Analysis Layer;
- Context Update Layer.



Future:


- Architecture Knowledge;
- cross-project experience;
- external system adapters;
- deeper semantic understanding.



---

## 16. Core limitation


Memory Core must not confuse:


"detecting information"


with:


"understanding meaning"



Understanding requires:

- architecture knowledge;
- project context;
- human validation.



---

## 17. Final direction


The purpose of Knowledge Flow is not to create an automatic programmer.


The purpose is to create continuity of understanding.


REQUIEM should remember:

- what happened;
- how systems evolved;
- why decisions were made;
- what knowledge can be reused.



The final goal:


REQUIEM knowledge continuity system.