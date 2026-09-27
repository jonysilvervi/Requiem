# REQUIEM MEMORY CORE MODEL

Version: 0.1

Status: DRAFT


---

## 1. Purpose


Memory Core is the internal knowledge continuity system of REQUIEM.


Its purpose:

- preserve project history;
- maintain architectural knowledge;
- track evolution of systems;
- support human decision making;
- prevent loss of project context.


Memory Core is not a game system.

Memory Core is not an engine feature.

Memory Core is not an automatic decision maker.


---

## 2. Position inside REQUIEM ecosystem


REQUIEM consists of multiple independent systems.


Example:


REQUIEM

|

├── Projects

├── Engine

├── Tools

├── Documentation

└── Memory Core



Memory Core observes and preserves knowledge about these systems.


It does not own them.


---

## 3. Core principles


### 3.1 Independence


Memory Core must not depend on one specific project.


Example:

- STALKER 2 is a project;
- future games are projects;
- Memory Core remains unchanged.



---

### 3.2 Human authority


Memory Core may analyze and suggest.


Human decisions remain the source of truth.



---

### 3.3 Historical preservation


Previous states must never be silently overwritten.


Changes create history.



---

### 3.4 Layer separation


Each responsibility has its own layer.


Current:


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

Memory



---

## 4. What Memory Core stores


Memory Core stores knowledge about:


### Projects


Examples:

- games;
- applications;
- tools.



### Systems


Examples:

- rendering;
- AI;
- quests;
- UI;
- configuration.



### Components


Examples:

- files;
- modules;
- resources.



### Decisions


Why something was created or changed.



### History


How systems evolved.



---

## 5. What Memory Core does not do


Memory Core does not:


- modify project code automatically;
- replace source control;
- replace documentation;
- control the engine;
- decide architecture without approval;
- belong to one game.



---

## 6. Relationship with projects


Each project can provide information to Memory Core.


Example:


STALKER 2 project:


Project

|

├── Code

├── Configurations

├── Assets

├── Engine data

└── Documentation



Memory Core receives knowledge about changes.


It does not become part of the project.



---

## 7. Relationship with REQUIEM Engine


Engine integration is future functionality.


Possible future model:


Engine

|

| Adapter

|

v


Memory Core



The engine provides structured information.


Memory Core stores and analyzes it.


The engine does not control Memory Core.



---

## 8. Future multi-project architecture


Memory Core must support:


REQUIEM


Projects


├── Project A


├── Project B


└── Project C



Shared Knowledge


├── Systems

├── Patterns

├── Decisions

└── History



Knowledge may exist:

- inside one project;
- across multiple projects.



---

## 9. Current implementation state


Implemented:


- Snapshot System v0.1

- Comparison Layer v0.1

- Change Report Layer v0.1

- Context Update Layer v0.1

- Analysis Layer v0.1



Not implemented:


- Engine integration;

- Architecture knowledge graph;

- Cross-project knowledge;

- Automatic semantic understanding.



---

## 10. Knowledge levels


Memory Core operates with different levels of knowledge.


Each level represents a transition from raw information to deeper project understanding.



---

### Level 1 — Observation


Raw facts collected from project states.


Examples:


- file changed;
- configuration updated;
- component appeared;
- component removed;
- project state changed.


Observation answers:


"What happened?"


It does not explain why it happened.



---

### Level 2 — Understanding


Structured interpretation of project information.


Examples:


- this file belongs to a specific system;
- this configuration controls a specific feature;
- this component depends on another component;
- this change affects a known project area.


Understanding answers:


"What does this change relate to?"



---

### Level 3 — Decisions


Human-approved architectural knowledge.


Examples:


- why a system was created;
- why a technology was chosen;
- why a design approach was rejected;
- why a change was accepted.


Decisions answer:


"Why does the project work this way?"



---

### Level 4 — Experience


Knowledge accumulated across multiple projects.


Examples:


- reusable solutions;
- architectural patterns;
- known problems;
- successful approaches;
- lessons learned.


Experience allows REQUIEM to preserve knowledge beyond a single project.



---

## 11. Memory Core evolution


Memory Core evolves through several stages.


Current stage:


"File history system"


The system can detect and preserve changes.



Future stage:


"Project understanding system"


The system understands relationships between files, systems and decisions.



Final direction:


"REQUIEM knowledge continuity system"


The system preserves not only what changed, but why it changed and what was learned.



---

## 12. Relationship between data and knowledge


Memory Core separates facts from understanding.


Facts:


- snapshots;
- hashes;
- file changes;
- timestamps.



Knowledge:


- system relationships;
- architecture;
- decisions;
- experience.



Facts are collected automatically.


Knowledge requires validation and human approval.



---

## 13. Future direction


Memory Core should evolve from:


"file history system"


into:


"REQUIEM knowledge continuity system"



The goal is not to remember files.


The goal is to preserve understanding.