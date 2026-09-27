# REQUIEM ARCHITECTURE KNOWLEDGE MODEL

Version: 0.1

Status: DRAFT


## 1. Purpose


Architecture Knowledge Model defines how Memory Core represents understanding about project structure.


Architecture knowledge describes not only where project elements exist, but what role they have, how they are connected and what they affect.



---


## 2. Difference between structure and knowledge


Structure:


A file exists in a specific location.


Example:



config/weapons/ak74.ini



Knowledge:


The file belongs to a system,
has a role,
has dependencies,
and affects other components.


Example:



AK74 configuration belongs to Weapon System.

It controls weapon parameters.




---


## 3. Architecture Map role


Architecture Map is not a copy of the project.


It describes the understanding of the project structure.


Architecture Map defines relationships between:


- systems;
- subsystems;
- components;
- resources.



It provides the foundation for Architecture Knowledge.



---


## 4. Knowledge hierarchy


Architecture Knowledge follows a hierarchical structure:



REQUIEM

↓

Project

↓

System

↓

Subsystem

↓

Component

↓

Resource




Each level provides additional meaning and context.



---


## 5. Architecture entities


Architecture Knowledge contains different types of entities:


## Project


A complete project inside the REQUIEM ecosystem.



## System


A major functional area of a project.


Examples:


- Gameplay System;
- Rendering System;
- Quest System.



## Subsystem


A logical part of a system.



## Component


A specific functional element inside a subsystem.



## Resource


A project element connected to a component.


Examples:


- configuration;
- script;
- model;
- database entry.



## Decision


A documented architectural choice.


Example:


"Inventory system uses modular components."



## Dependency


A relationship where one element requires another.



---


## 6. Relationships


Architecture Knowledge describes relationships between entities.


Supported relationship types:



contains

depends_on

affects

generated_by

controlled_by




Relationships explain how project elements interact.



---


## 7. Knowledge sources


Architecture knowledge may come from different sources:


## Human knowledge


Direct understanding provided by developers.


Human knowledge has the highest authority.



## Project documentation


Technical descriptions, design documents and explanations.



## Architecture Map


Structured representation of project organization.



## Analysis results


Possible relationships and impact information discovered by Analysis Layer.



## Future adapters


External systems may provide additional information.


Automatically discovered information is not automatically trusted.



---


## 8. Human approval


Architecture knowledge cannot appear automatically.


AI and tools may suggest possible knowledge.


Human approves trusted architectural information.


The process:



Information

↓

Proposal

↓

Human Review

↓

Approved Knowledge

↓

Memory




---


## 9. Multiple project support


REQUIEM supports multiple projects.


Example:



STALKER 2:

Project A

Future game:

Project B

Shared knowledge:

Patterns

Solutions

Experience




Each project has independent architecture knowledge.


Shared knowledge contains reusable concepts, not project-specific facts.



---


## 10. Current state


Current Architecture Knowledge state:


Architecture Map:



DRAFT




Current limitations:


- no automatic generation;
- no engine integration;
- no cross-project knowledge system;
- knowledge requires human approval.



---


## 11. Future integration


Future integrations may provide additional information.


Possible sources:


- Engine adapters;
- Project adapters;
- External tools.



Memory Core remains independent from specific engines and projects.



---


## 12. Final vision


Architecture Knowledge transforms Memory Core from a file tracking system into a project understanding system.


The goal is not only knowing:


"What file changed?"


The goal is understanding:


"What part of the project changed?"

"Why does it matter?"

"What can be affected?"



Architecture Knowledge is the foundation for long-term REQUIEM ecosystem development.