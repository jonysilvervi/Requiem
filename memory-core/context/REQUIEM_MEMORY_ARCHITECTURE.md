# REQUIEM MEMORY ARCHITECTURE

Version: 0.2

Status: DRAFT


---

# 1. Purpose


REQUIEM Memory Architecture defines the general architecture of Memory Core.

The purpose of Memory Core is to preserve, understand and evolve knowledge about projects inside the REQUIEM ecosystem.


Memory Core does not store project files.

Memory Core stores verified understanding about projects.


The system exists to support:

- project continuity;
- architectural understanding;
- historical tracking;
- change analysis;
- future multi-project development.


Memory Core is a development infrastructure system.

It is independent from any specific game or engine.



---

# 2. Core principle


Memory Core separates facts, interpretation and knowledge.


Files are observations.


Snapshots are recorded project states.


Changes are historical facts.


Analysis provides interpretation.


Architecture Knowledge provides meaning.


Human approval creates trusted knowledge.


Memory Core does not silently change project understanding.



---

# 3. System overview


REQUIEM


├── Projects

├── Engine

├── Tools

└── Memory Core



REQUIEM ecosystem contains multiple independent areas.

Memory Core observes and understands these areas.

Memory Core does not control project execution.

Memory Core does not modify engine data automatically.

Memory Core does not depend on one specific project.



---

# 4. Separation between REQUIEM and Memory Core


REQUIEM ecosystem:



REQUIEM

|

├── Game Projects

|

├── Engine

|

├── Development Tools

|

└── Memory Core



Memory Core works as an internal knowledge system.


Projects provide information.


Memory Core preserves and analyzes information.


The relationship:


Project

↓

Observation

↓

Memory Core

↓

Knowledge



Memory Core supports projects but remains architecturally independent.



---

# 5. Memory Core layers


Memory Core consists of separated layers.


## Observation


Responsible for collecting project information.


Answers:


"What exists?"


Example:

- files;
- metadata;
- hashes;
- project state.



## Storage


Responsible for preserving historical states.


Answers:


"What was the project state at a specific moment?"


Example:

- snapshots;
- history;
- checkpoints.



## Comparison


Responsible for detecting differences between states.


Answers:


"What changed?"


Does not explain meaning.



## Change Report


Responsible for creating structured records of detected changes.


Answers:


"What change record exists?"



## Analysis


Responsible for interpreting detected changes using rules and architecture knowledge.


Answers:


"What could this change affect?"



## Architecture Knowledge


Responsible for storing approved understanding of project structure.


Answers:


"What does this part of the project mean?"



## Human Review


Responsible for approval of important knowledge changes.


Answers:


"Should this information become trusted memory?"



## Context Update


Responsible for applying approved knowledge changes.


Answers:


"What information can be stored permanently?"



## Memory


Final preserved project knowledge.



---

# 6. Data flow


Complete Memory Core flow:



Project

↓

Scanner

↓

Snapshot

↓

Comparison

↓

Change Record

↓

Analysis

↓

Human Review

↓

Context Update

↓

Memory



The order is intentional.


Each layer has limited responsibility.


No layer replaces another.



---

# 7. Responsibility boundaries


Each component answers a different question.


Scanner:


"What exists?"



Snapshot:


"What was recorded?"



Comparison:


"What changed?"



Change Report:


"What change record describes this?"



Analysis:


"What could this affect?"



Architecture Map:


"What does this part mean?"



Context Update:


"What knowledge can be stored?"



Memory:


"What is known about the project?"



---

# 8. Storage separation


Memory Core separates information by purpose.


## database/


Contains protected project memory.


Examples:

- identity;
- decisions;
- events;
- checkpoints;
- state.



## history/


Contains historical project states.


Examples:

- snapshots.



## reports/


Contains generated analysis results.


Examples:

- scan reports;
- comparison reports;
- analysis reports.



## review/


Contains temporary human review materials.


Examples:

- change records;
- update proposals;
- backups.



## context/


Contains architectural and system knowledge documentation.



---

# 9. Protected areas


Some information cannot be modified automatically.


Protected:


identity


decisions


checkpoints


architecture approval


These represent trusted project knowledge.


Changes require explicit human control.



---

# 10. Architecture Knowledge


Architecture Knowledge represents understanding of a project.


It is not a copy of project files.


It describes:


- systems;
- components;
- relationships;
- responsibilities;
- dependencies.



Example:


File:



scripts/quest/main.lua



Architecture meaning:



System:
Quest System

Component:
Quest Logic

Role:
Controls quest progression



One architecture concept may include multiple files.



---

# 11. Multi-project model


REQUIEM is designed as a multi-project ecosystem.


Example:



REQUIEM

|

├── STALKER 2 Project

| |

| └── Architecture Map

|

├── Future Game Project

| |

| └── Architecture Map

|

└── Shared Knowledge



Each project has independent architecture knowledge.


Shared knowledge may contain:


- patterns;
- solutions;
- experience;
- reusable approaches.



---

# 12. Future integrations


Memory Core may later connect with external systems.


Possible adapters:


## Engine Adapter


Provides:


- engine events;
- generated information;
- runtime information.



## Project Adapter


Provides:


- project-specific information;
- project metadata;
- structure information.



## Tool Adapter


Provides:


- editor actions;
- build information;
- external tool events.



Integrations must extend Memory Core without making it dependent on a specific environment.



---

# 13. Current implementation


Currently implemented:


- Scanner Layer;
- Snapshot System;
- Comparison Layer;
- Change Report Layer;
- Analysis Layer;
- Context Update Layer.



Current limitations:


- Architecture Map is a DRAFT;
- engine integration does not exist;
- automatic architecture extraction does not exist;
- cross-project knowledge does not exist.



Memory Core currently works using manually approved knowledge.



---

# 14. Future architecture


Future Memory Core development direction:


From:



Project description



towards:



Project understanding model



The goal is not only knowing where files exist.


The goal is understanding:


- what systems exist;
- how components interact;
- why they exist;
- how changes affect the project.



---

# 15. Architectural principles


Memory Core follows these principles:


## Project independence


Memory Core must not become a system for one game only.



## Human authority


Important knowledge requires human approval.



## Separation of layers


Each layer has one responsibility.



## Reproducibility


Knowledge must be based on verified information.



## Controlled evolution


Memory grows through approved changes, not automatic rewriting.



---

# 16. Final vision


REQUIEM Memory Core is not a file tracker.


It is a knowledge system for long-term project development.


Its purpose is to preserve understanding of complex ecosystems over time.


The system should allow REQUIEM to grow from a single project into a multi-project development environment where previous experience, architecture decisions and project knowledge remain available.