---
generated_by: "build_obsidian_vault.py"
type: "curriculum-lesson"
aliases: ["Model-Based RL and Uncertainty-Aware Planning"]
day: 30
cycle: 10
domain: "Embodied AI & RL Robotics"
stage: "Modern"
status: "planned"
source: ["curriculum_plan.json", "curriculum_resources.json"]
tags: ["curriculum", "embodied-ai-rl-robotics", "modern"]
cssclasses: ["research-note", "curriculum-note"]
related_concepts: ["Mind Map/Nodes/systems.md", "Mind Map/Nodes/policy.md"]
related_papers: []
---

[[Home|Research Lab]]  /  [[Curriculum/Curriculum|Curriculum]]

# Day 30 — Model-Based RL and Uncertainty-Aware Planning

> [!curriculum] Embodied AI & RL Robotics · Modern
> **Cycle 10** · **status: planned**
> Use the videos for first-pass learning; use this note for fast recall without rewatching.

> [!sequence] Learning sequence
> - [[Curriculum/Lessons/Day 29 - NeRF Volume Rendering & Positional Encoding|← Day 29]]
> - [[Curriculum/Curriculum|Curriculum map]]
> - [[Curriculum/Lessons/Day 31 - Flow Matching & Optimal-Transport Paths|Day 31 →]]

> [!concepts] Knowledge-graph concepts
> - [[Mind Map/Nodes/systems|Systems]]
> - [[Mind Map/Nodes/policy|Policies / VLA]]

## Brief description

Model-based RL learns or uses a transition model to predict consequences and plan; uncertainty awareness separates reliable imagined rollouts from regions where model error would compound.

## Recall in 30 seconds

- A model may predict next observations, latent states, rewards, or full trajectory distributions.
- Planning evaluates candidate action sequences through the model and executes only part before replanning.
- Epistemic uncertainty indicates unfamiliar data and should shorten, penalize, or diversify imagined rollouts.
- Better one-step prediction does not guarantee better control; errors matter in proportion to how planning exploits them.

## Watch in order

> [!method] Why this sequence
> Watch in order: foundation first, then mechanism, then application or diagnostics where the topic needs it. Coverage boundary: Uncertainty is treated in the model-based-RL context; detailed Bayesian filtering or formal risk-sensitive planning is outside these lectures.

### 1. CS 285: Lecture 12, Part 1: Model-Based RL with Policies

> [!video] RAIL · English · research lab
> **Purpose:** Introduces learned dynamics models, policy learning through models, and sources of model bias.
> [Watch on YouTube](https://www.youtube.com/watch?v=UQGS4ycGv8g)

### 2. CS 285: Lecture 12, Part 2: Model-Based RL with Policies

> [!video] RAIL · English · research lab
> **Purpose:** Continues with practical model-based policy optimization and strategies for handling prediction error and uncertainty.
> [Watch on YouTube](https://www.youtube.com/watch?v=2POKgmzPAto)

> [!summary] After watching
> Close the videos and explain the recall bullets in your own words. Add only corrections or a worked example below—do not recreate the lecture.

## My correction or example

-
