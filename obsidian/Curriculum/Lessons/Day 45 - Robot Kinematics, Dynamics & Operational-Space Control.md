---
generated_by: "build_obsidian_vault.py"
type: "curriculum-lesson"
aliases: ["Robot Kinematics, Dynamics & Operational-Space Control"]
day: 45
cycle: 15
domain: "Embodied AI & RL Robotics"
stage: "Integration"
status: "planned"
source: ["curriculum_plan.json", "curriculum_resources.json"]
tags: ["curriculum", "embodied-ai-rl-robotics", "integration"]
cssclasses: ["research-note", "curriculum-note"]
related_concepts: ["Mind Map/Nodes/kinematics.md", "Mind Map/Nodes/systems.md", "Mind Map/Nodes/policy.md"]
related_papers: []
---

[[Home|Research Lab]]  /  [[Curriculum/Curriculum|Curriculum]]

# Day 45 — Robot Kinematics, Dynamics & Operational-Space Control

> [!curriculum] Embodied AI & RL Robotics · Integration
> **Cycle 15** · **status: planned**
> Use the videos for first-pass learning; use this note for fast recall without rewatching.

> [!sequence] Learning sequence
> - [[Curriculum/Lessons/Day 44 - 3D Scene Understanding and Point-Implicit Representations|← Day 44]]
> - [[Curriculum/Curriculum|Curriculum map]]
> - [[Curriculum/Lessons/Day 46 - Causal Representation Learning & Invariance|Day 46 →]]

> [!concepts] Knowledge-graph concepts
> - [[Mind Map/Nodes/kinematics|Kinematics]]
> - [[Mind Map/Nodes/systems|Systems]]
> - [[Mind Map/Nodes/policy|Policies / VLA]]

## Brief description

Robot kinematics maps joint motion to task-space motion, dynamics relates forces to acceleration, and operational-space control commands end-effector behavior while respecting the robot's full-body mechanics.

## Recall in 30 seconds

- Forward kinematics maps joints to poses; the Jacobian maps joint velocities to task-space velocity.
- Dynamics combines inertia, Coriolis/centrifugal effects, gravity, and external forces.
- Operational-space control shapes task acceleration or wrench through dynamically consistent mappings.
- Singularities, torque limits, contacts, model error, and competing tasks require regularization and prioritization.

## Watch in order

> [!method] Why this sequence
> Watch in order: foundation first, then mechanism, then application or diagnostics where the topic needs it.

### 1. Lecture 5 | Introduction to Robotics

> [!video] Stanford · English · university course
> **Purpose:** Stanford robotics-course treatment of manipulator differential kinematics, Jacobians, forces, and the transition toward dynamics.
> [Watch on YouTube](https://www.youtube.com/watch?v=u79KfNgP1Cc)

### 2. Lecture 6 | Introduction to Robotics

> [!video] Stanford · English · university course
> **Purpose:** Continues the Stanford sequence through manipulator dynamics and feedback-control foundations.
> [Watch on YouTube](https://www.youtube.com/watch?v=fwHc0a8DMQ0)

### 3. Lecture 14: MIT 6.800/6.843 Robotics Manipulation (Fall 2021) | "Manipulator Control"

> [!video] underactuated · English · university course
> **Purpose:** Connects dynamics to task-space/manipulator control, including operational objectives, feedback, and contact-aware control.
> [Watch on YouTube](https://www.youtube.com/watch?v=CfDPMYfk_0o)

> [!summary] After watching
> Close the videos and explain the recall bullets in your own words. Add only corrections or a worked example below—do not recreate the lecture.

## My correction or example

-
