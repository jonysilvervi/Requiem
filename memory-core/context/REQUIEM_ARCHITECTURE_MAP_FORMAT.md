# REQUIEM ARCHITECTURE MAP FORMAT

Version: 0.1

Status: DRAFT


---

# 1. Purpose


Architecture Map Format defines the structure of architecture_map.json.


The purpose of the format is to represent approved project architecture knowledge in a structured way.


Architecture Map does not store all project files.

It stores important architectural relationships and meanings.



---

# 2. Core principle


Architecture Map describes:


"What exists in the project?"


and:


"How project elements are organized?"


It does not replace:


- project files;
- source code;
- documentation;
- snapshots.



---

# 3. Architecture Map structure


The basic structure:



Project

↓

Systems

↓

Subsystems

↓

Components

↓

Resources



Each element may contain:


- identity;
- description;
- relationships;
- dependencies;
- ownership.



---

# 4. Map entities


Architecture Map contains the following entities:


## Project


Represents a complete project.


Example:



STALKER 2



Properties:


- name;
- description;
- version.



---

## System


Represents a major project area.


Examples:


- Gameplay;
- Rendering;
- AI;
- Tools.



Properties:


- name;
- purpose;
- components.



---

## Subsystem


Represents a logical part of a system.


Properties:


- name;
- description;
- parent system.



---

## Component


Represents a functional project element.


Properties:


- name;
- role;
- dependencies;
- resources.



---

## Resource


Represents a concrete project element.


Examples:


- script;
- configuration;
- model;
- database;
- asset.



Properties:


- path;
- type;
- role.



---

# 5. Relationships


Architecture Map may contain relationships:



contains

depends_on

affects

generated_by

controlled_by



Relationships describe connections between entities.



---

# 6. Approval status


Architecture Map has an approval state.


Possible states:



DRAFT

↓

REVIEW

↓

APPROVED



Only APPROVED architecture knowledge becomes trusted memory.



---

# 7. Human ownership


Architecture Map is created and approved by humans.


AI and tools may prepare suggestions.


AI cannot automatically create architectural truth.



---

# 8. Example structure


Example:



Project:

REQUIEM Game Project

System:

Gameplay System

Subsystem:

Quest System

Component:

Quest Manager

Resource:

quest_manager.cpp



The example represents meaning, not a required project structure.



---

# 9. Multi-project support


Each project has its own Architecture Map.


Example:



REQUIEM

|

├── STALKER 2

| └── architecture_map.json

|

├── Future Game

| └── architecture_map.json



Shared knowledge is stored separately.



---

# 10. Current limitations


Current limitations:


- no automatic architecture extraction;
- no engine integration;
- no automatic approval;
- architecture maps require human creation.



---

# 11. Future development


Future versions may support:


- engine-generated suggestions;
- dependency discovery;
- architecture validation;
- impact prediction.



---

# 12. Final vision


Architecture Map becomes the bridge between project files and project understanding.


Files show what exists.

Architecture Map explains what it means.