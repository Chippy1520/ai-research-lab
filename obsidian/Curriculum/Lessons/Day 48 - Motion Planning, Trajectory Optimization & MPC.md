---
generated_by: "build_obsidian_vault.py"
type: "curriculum-lesson"
aliases: ["Motion Planning, Trajectory Optimization & MPC"]
day: 48
cycle: 16
domain: "Embodied AI & RL Robotics"
stage: "Integration"
status: "planned"
source: ["curriculum_plan.json", "curriculum_resources.json"]
tags: ["curriculum", "embodied-ai-rl-robotics", "integration"]
cssclasses: ["research-note", "curriculum-note"]
related_concepts: ["Mind Map/Nodes/systems.md", "Mind Map/Nodes/policy.md"]
related_papers: []
---

[[Home|Research Lab]]  /  [[Curriculum/Curriculum|Curriculum]]

# Day 48 — Motion Planning, Trajectory Optimization & MPC

> [!curriculum] Embodied AI & RL Robotics · Integration
> **Cycle 16** · **status: planned**
> Use the videos for first-pass learning; use this note for fast recall without rewatching.

> [!sequence] Learning sequence
> - [[Curriculum/Lessons/Day 47 - 4D Dynamic Reconstruction & Neural Scene Flow|← Day 47]]
> - [[Curriculum/Curriculum|Curriculum map]]
> - [[Curriculum/Lessons/Day 49 - Meta-Learning, Continual Learning & Adaptation|Day 49 →]]

> [!concepts] Knowledge-graph concepts
> - [[Mind Map/Nodes/systems|Systems]]
> - [[Mind Map/Nodes/policy|Policies / VLA]]

## Brief description

Motion planning searches for collision-free behavior, trajectory optimization refines a parameterized path under costs and constraints, and model predictive control repeatedly replans from updated state estimates.

## Recall in 30 seconds

- Sampling-based planners explore feasible connectivity; optimization-based planners exploit smooth local structure.
- Trajectory optimization balances dynamics, collision, task, smoothness, and actuator constraints.
- MPC executes the first part of a finite-horizon plan, observes again, and shifts the horizon.
- Model error, latency, non-convexity, and uncertain obstacles require margins, feedback, and fallback behavior.

## Watch in order

> [!method] Why this sequence
> Watch in order: foundation first, then mechanism, then application or diagnostics where the topic needs it. Coverage boundary: The final lecture emphasizes trajectory stabilization; detailed MPC solver engineering and real-time iteration are not treated exhaustively.

### 1. Lecture 15 | MIT 6.881 (Robotic Manipulation), Fall 2020 | Motion Planning (Part 1)

> [!video] underactuated · English · university course
> **Purpose:** Introduces configuration-space motion planning, collision constraints, and search/sampling-based planning.
> [Watch on YouTube](https://www.youtube.com/watch?v=RjKkA_6-0C4)

### 2. Lecture 10 | MIT 6.832 (Underactuated Robotics), Spring 2020 | Trajectory Optimization

> [!video] underactuated · English · university course
> **Purpose:** Reformulates planning as constrained trajectory optimization with dynamics and costs.
> [Watch on YouTube](https://www.youtube.com/watch?v=ZTizHbj339w)

### 3. Lecture 12: MIT 6.832 Underactuated Robotics (Spring 2022) | "Trajectory Stabilization"

> [!video] underactuated · English · university course
> **Purpose:** Closes the loop through receding-horizon/trajectory-stabilization ideas that connect optimized plans to model-predictive feedback control.
> [Watch on YouTube](https://www.youtube.com/watch?v=sd7Lj7StBkA)

> [!summary] After watching
> Close the videos and explain the recall bullets in your own words. Add only corrections or a worked example below—do not recreate the lecture.

## My correction or example

-
