# REQUIEM INSTANCE MODEL

Version: 0.3

Status: DRAFT


---

# 1. Purpose


REQUIEM Instance Model defines the relationship between the REQUIEM ecosystem, the Memory Core System, a Memory Core Instance, projects and environments.


The purpose of this model is to separate:

- the Memory Core System;
- the Memory Core Development Project;
- projects observed by Memory Core;
- environments referenced by projects;
- knowledge by ownership level.


This separation is required for long-term multi-project development.


Terms are defined in REQUIEM_GLOSSARY.md. Decisions FD-B1 … FD-B8 are defined in REQUIEM_FOUNDATION_DECISIONS.md.


---

# 2. Core principle


The Memory Core System is not a project.

It is a system that stores and manages knowledge about projects.


The development of the Memory Core System is a project: the Memory Core Development Project (FD-B8).


A Memory Core Instance may observe multiple independent projects.


The existence of Memory Core must not depend on one specific project.


Memory Core observes and supports projects. It does not control projects or environments.


---

# 3. REQUIEM Ecosystem


REQUIEM Ecosystem is the highest organizational level.


It contains:


REQUIEM

├── Projects

├── Engine

├── Tools

└── Memory Core



"Engine" is the REQUIEM Engine. External engines such as Unreal Engine are environments (FD-B3).


REQUIEM Ecosystem represents the complete development environment.


---

# 4. Memory Core Instance


A Memory Core Instance is an installation of the Memory Core System.


An instance contains:

- Memory Core System components;
- configuration;
- System Knowledge;
- Ecosystem Knowledge;
- Shared Knowledge;
- registered projects.


System, Ecosystem and Shared Knowledge belong to the instance, not to any project.


An instance is independent from the projects it serves.


The number of instances per ecosystem is not decided (FD open item O4).


---

# 5. Project


A Project is an independent development subject owned by REQUIEM and observed and supported by Memory Core.


A project has:

- identity;
- files;
- observations;
- snapshots;
- change history;
- project knowledge.


Projects:

- REQUIEM Application;
- REQUIEM Mod Pack;
- Memory Core Development Project.


---

# 6. Environment


An environment is an external or supporting system in which a project operates (FD-B3).


Examples:

- S.T.A.L.K.E.R. 2;
- Unreal Engine;
- operating system;
- runtime environment.


Rules:

- an environment is not registered as a project;
- a project references the environments it operates in;
- an environment does not own knowledge;
- project-specific usage and modifications of an environment are Project Knowledge of the referencing project (FD-B7);
- the identity of an environment (name, version) is Ecosystem Knowledge (FD-B7, rule 5).


---

# 7. Relationship model


REQUIEM Ecosystem

↓

Memory Core Instance

(System, Ecosystem and Shared Knowledge)

↓

Projects

↓

Project Knowledge


Projects

→ reference →

Environments



Memory Core observes projects.

Projects do not control Memory Core.

Memory Core does not control projects or environments.


---

# 8. Memory Core System and Memory Core Development Project


| | Memory Core System | Memory Core Development Project |
|---|---|---|
| What | implemented layers, formats, rules | development state, milestones, versions, roadmap |
| Is a project | no | yes |
| Knowledge level | System Knowledge | Project Knowledge |
| Current examples | layer code, layer models, development protocol section 5, DEC-005 … DEC-018 | state.json, milestone events, CP-001 … CP-006 |


Memory Core System code and project knowledge must remain separated.


The full mapping of current records is in REQUIEM_FOUNDATION_DECISIONS.md, FD-B8.


---

# 9. Project identity


Each project requires a stable identity.


Project identity contains:

- project_id;
- name;
- kind (Project Kind);
- owner — the human responsible for approving the project's knowledge;
- environment references;
- creation information.


Project identity must not depend on:

- folder name;
- computer location;
- temporary paths.


The location of the observed files is configuration of the project, not its identity.


The format of project_id is not decided (FD open item O5).


Illustrative identifiers used in this document (not registered):

- requiem-application;
- requiem-mod-pack;
- memory-core-development.


---

# 10. Project isolation


Each project maintains separate:

- snapshots;
- change records;
- context update proposals;
- analysis results;
- project knowledge, including architecture knowledge and project-specific usage and modifications of referenced environments;
- project decisions;
- project events;
- project state.


One project's knowledge cannot automatically become another project's knowledge.


References from one project to another project are not decided (FD open item O2).


---

# 11. Knowledge levels in an instance


| Level | Owner | Contains project paths |
|---|---|---|
| System Knowledge | Memory Core System | no |
| Ecosystem Knowledge | REQUIEM Ecosystem | no |
| Shared Knowledge | REQUIEM Ecosystem (reusable between projects) | no |
| Project Knowledge | one project | yes |


Shared Knowledge must not contain:

- project-specific files or paths;
- private project decisions;
- temporary information.


Project Knowledge becomes Shared Knowledge only through human review, without project-specific content.


---

# 12. Future structure


Possible future structure:


REQUIEM

└── Memory Core Instance

    ├── System Knowledge

    ├── Ecosystem Knowledge

    ├── Shared Knowledge

    └── Projects

        ├── REQUIEM Application

        ├── REQUIEM Mod Pack

        └── Memory Core Development Project



Environments (S.T.A.L.K.E.R. 2, Unreal Engine) are outside the instance. Projects reference them.


The physical storage layout is not defined by this model. Current storage remains unchanged until migration planning is approved (REQUIEM_FOUNDATION_DECISIONS.md, sections 11–12).


---

# 13. Relationship with Architecture Knowledge


Architecture Knowledge belongs to one project (FD-B5).


Illustrative examples (not trusted knowledge):


REQUIEM Mod Pack:

- project components of the mod pack;
- project knowledge about S.T.A.L.K.E.R. 2 systems that the mod pack changes (for example the weapon system of the environment).


REQUIEM Application:

- application systems and components.


The mod pack does not own the systems of S.T.A.L.K.E.R. 2. It owns its knowledge about how it uses and modifies them (FD-B7).


Projects may have different architectures.


---

# 14. Current CP-006 state


CP-006 is a single-store implementation. It does not yet follow this model.


Correspondence (for migration planning, not a migration):

| CP-006 | Model |
|---|---|
| snapshot project "REQUIEM" / "requiem-tauri" | REQUIEM Application |
| snapshots, CHG-001, CU-001, EVENT-006 | REQUIEM Application data |
| state.json, milestone events, checkpoints | Memory Core Development Project data |
| identity.json, DEC-001 … DEC-003, development protocol except section 5 | Ecosystem Knowledge |
| DEC-005 … DEC-018, layer models, development protocol section 5 | System Knowledge |
| analysis/architecture_map.json revision 2 | prototype; not project knowledge (FD-B5) |


Known deviations are listed in REQUIEM_FOUNDATION_DECISIONS.md, section 12.


---

# 15. Human authority


Registration of new projects requires human approval.


Memory Core may suggest project information.


Memory Core cannot silently create trusted project identity.


---

# 16. Future development


Future versions may introduce:

- project registry;
- project adapters;
- automatic project discovery;
- sharing of knowledge between projects through Shared Knowledge.


---

# 17. Final vision


REQUIEM Memory Core should become a universal knowledge system capable of supporting multiple independent projects while preserving separation, history and human control.


END OF DOCUMENT
