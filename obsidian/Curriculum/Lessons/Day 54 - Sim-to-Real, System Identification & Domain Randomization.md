---
generated_by: "build_obsidian_vault.py"
type: "curriculum-lesson"
aliases: ["Sim-to-Real, System Identification & Domain Randomization"]
day: 54
cycle: 18
domain: "Embodied AI & RL Robotics"
stage: "Frontier"
status: "planned"
source: ["curriculum_plan.json", "curriculum_resources.json"]
tags: ["curriculum", "embodied-ai-rl-robotics", "frontier"]
cssclasses: ["research-note", "curriculum-note"]
related_concepts: ["Mind Map/Nodes/sim2real.md", "Mind Map/Nodes/systems.md", "Mind Map/Nodes/policy.md"]
related_papers: []
---

[[Home|Research Lab]]  /  [[Curriculum/Curriculum|Curriculum]]

# Day 54 — Sim-to-Real, System Identification & Domain Randomization

> [!curriculum] Embodied AI & RL Robotics · Frontier
> **Cycle 18** · **status: planned**
> Use the videos for first-pass learning; use this note for fast recall without rewatching.

> [!sequence] Learning sequence
> - [[Curriculum/Lessons/Day 53 - Vision-Language Models and Visual Reasoning|← Day 53]]
> - [[Curriculum/Curriculum|Curriculum map]]
> - [[Curriculum/Lessons/Day 55 - ML Systems- Accelerators, Mixed Precision & Distributed Training|Day 55 →]]

> [!concepts] Knowledge-graph concepts
> - [[Mind Map/Nodes/sim2real|Sim-to-real]]
> - [[Mind Map/Nodes/systems|Systems]]
> - [[Mind Map/Nodes/policy|Policies / VLA]]

## Brief description

Sim-to-real transfers policies or models from simulation to hardware by identifying important dynamics, randomizing uncertain factors, and adapting representations or controllers to residual mismatch.

## Recall in 30 seconds

- System identification estimates simulator or controller parameters from real trajectories.
- Domain randomization trains across a distribution so the real system is likely to lie inside learned robustness.
- Randomizing irrelevant variables wastes capacity; omitting a causal factor creates brittle transfer.
- Validate progressively with uncertainty bounds, safety limits, residual adaptation, and hardware-specific latency/noise tests.

## Watch in order

> [!method] Why this sequence
> Watch in order: foundation first, then mechanism, then application or diagnostics where the topic needs it.

### 1. Lecture 1: Introduction to Identification, Estimation, and Learning

> [!video] dLabRoboticsMIT · English · university course
> **Purpose:** Introduces system identification and estimation as mechanisms for reducing model mismatch.
> [Watch on YouTube](https://www.youtube.com/watch?v=MfUBy2Fxlmg)

### 2. Research at NVIDIA: Structured Domain Randomization

> [!video] NVIDIA · English · research lab
> **Purpose:** Explains domain randomization and how structured variation can make synthetic training data useful in reality.
> [Watch on YouTube](https://www.youtube.com/watch?v=1WdjWJYx9AY)

### 3. Learning and Deploying Robust Locomotion Policies with Minimal Dynamics Randomization

> [!video] Oxford Dynamic Robot Systems Group · English · research lab
> **Purpose:** Shows the complete sim-to-real loop for learned robot control, including dynamics variation and real-hardware deployment.
> [Watch on YouTube](https://www.youtube.com/watch?v=kGkOoJ_DAwQ)

> [!summary] After watching
> Close the videos and explain the recall bullets in your own words. Add only corrections or a worked example below—do not recreate the lecture.

## My correction or example

-
