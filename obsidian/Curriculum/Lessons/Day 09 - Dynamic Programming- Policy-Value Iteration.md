---
generated_by: "build_obsidian_vault.py"
type: "curriculum-lesson"
aliases: ["Dynamic Programming: Policy/Value Iteration"]
day: 9
cycle: 3
domain: "Embodied AI & RL Robotics"
stage: "Foundations"
status: "planned"
source: ["curriculum_plan.json", "curriculum_resources.json"]
tags: ["curriculum", "embodied-ai-rl-robotics", "foundations"]
cssclasses: ["research-note", "curriculum-note"]
related_concepts: ["Mind Map/Nodes/systems.md", "Mind Map/Nodes/policy.md"]
related_papers: []
---

[[Home|Research Lab]]  /  [[Curriculum/Curriculum|Curriculum]]

# Day 09 — Dynamic Programming: Policy/Value Iteration

> [!curriculum] Embodied AI & RL Robotics · Foundations
> **Cycle 3** · **status: planned**
> Use the videos for first-pass learning; use this note for fast recall without rewatching.

> [!sequence] Learning sequence
> - [[Curriculum/Lessons/Day 08 - Spatial Derivatives, Scale Space & Features|← Day 08]]
> - [[Curriculum/Curriculum|Curriculum map]]
> - [[Curriculum/Lessons/Day 10 - Linear Models, Kernels & Generalization|Day 10 →]]

> [!concepts] Knowledge-graph concepts
> - [[Mind Map/Nodes/systems|Systems]]
> - [[Mind Map/Nodes/policy|Policies / VLA]]

## Brief description

Dynamic programming solves known finite MDPs by repeatedly applying Bellman backups: policy iteration alternates evaluation and improvement, while value iteration folds both into an optimality update.

## Recall in 30 seconds

- Policy evaluation predicts returns for a fixed policy; policy improvement acts greedily with respect to those values.
- Policy iteration usually makes larger, costlier updates; value iteration makes cheaper partial backups.
- Both rely on a known transition and reward model in the classical tabular setting.
- The state-space explosion motivates sampling, approximation, and planning methods.

## Watch in order

> [!method] Why this sequence
> Watch in order: foundation first, then mechanism, then application or diagnostics where the topic needs it.

### 1. RL Course by David Silver - Lecture 3: Planning by Dynamic Programming

> [!video] Google DeepMind · English · research lab
> **Purpose:** Covers policy evaluation, policy iteration, value iteration, generalized policy iteration, and their convergence relationships.
> [Watch on YouTube](https://www.youtube.com/watch?v=Nd1-UUMVfz4)

> [!summary] After watching
> Close the videos and explain the recall bullets in your own words. Add only corrections or a worked example below—do not recreate the lecture.

## My correction or example

-
