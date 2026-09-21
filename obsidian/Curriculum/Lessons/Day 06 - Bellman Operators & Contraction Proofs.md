---
generated_by: "build_obsidian_vault.py"
type: "curriculum-lesson"
aliases: ["Bellman Operators & Contraction Proofs"]
day: 6
cycle: 2
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

# Day 06 — Bellman Operators & Contraction Proofs

> [!curriculum] Embodied AI & RL Robotics · Foundations
> **Cycle 2** · **status: planned**
> Use the videos for first-pass learning; use this note for fast recall without rewatching.

> [!sequence] Learning sequence
> - [[Curriculum/Lessons/Day 05 - 2D Fourier Analysis & Phase|← Day 05]]
> - [[Curriculum/Curriculum|Curriculum map]]
> - [[Curriculum/Lessons/Day 07 - Information Theory & Representation|Day 07 →]]

> [!concepts] Knowledge-graph concepts
> - [[Mind Map/Nodes/systems|Systems]]
> - [[Mind Map/Nodes/policy|Policies / VLA]]

## Brief description

Bellman operators turn long-horizon prediction or control into a one-step backup; under discounting they are contractions, which explains why repeated backups converge to a unique fixed point.

## Recall in 30 seconds

- Policy evaluation uses an expectation backup; optimal control replaces the policy average with a maximum.
- The fixed point of the Bellman operator is the corresponding value function.
- A discount factor below one makes the operator a contraction in the sup norm.
- Approximation, sampling, or off-policy updates can break the clean tabular convergence story.

## Watch in order

> [!method] Why this sequence
> Watch in order: foundation first, then mechanism, then application or diagnostics where the topic needs it.

### 1. DeepMind x UCL RL Lecture Series - Theoretical Fund. of Dynamic Programming Algorithms [4/13]

> [!video] Google DeepMind · English · research lab
> **Purpose:** Provides the theoretical treatment of Bellman operators, fixed points, contraction arguments, and convergence of dynamic-programming algorithms.
> [Watch on YouTube](https://www.youtube.com/watch?v=XpbLq7rIJAA)

> [!summary] After watching
> Close the videos and explain the recall bullets in your own words. Add only corrections or a worked example below—do not recreate the lecture.

## My correction or example

-
