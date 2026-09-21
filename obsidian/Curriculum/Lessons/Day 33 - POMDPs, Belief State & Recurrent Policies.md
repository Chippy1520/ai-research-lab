---
generated_by: "build_obsidian_vault.py"
type: "curriculum-lesson"
aliases: ["POMDPs, Belief State & Recurrent Policies"]
day: 33
cycle: 11
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

# Day 33 — POMDPs, Belief State & Recurrent Policies

> [!curriculum] Embodied AI & RL Robotics · Modern
> **Cycle 11** · **status: planned**
> Use the videos for first-pass learning; use this note for fast recall without rewatching.

> [!sequence] Learning sequence
> - [[Curriculum/Lessons/Day 32 - 3D Gaussian Splatting & Differentiable Rasterization|← Day 32]]
> - [[Curriculum/Curriculum|Curriculum map]]
> - [[Curriculum/Lessons/Day 34 - Sequence Models- RNNs, S4 & Mamba|Day 34 →]]

> [!concepts] Knowledge-graph concepts
> - [[Mind Map/Nodes/systems|Systems]]
> - [[Mind Map/Nodes/policy|Policies / VLA]]

## Brief description

A POMDP models decision-making when observations do not reveal the true state; a belief state summarizes uncertainty, while recurrent policies learn an implicit memory when exact Bayesian filtering is impractical.

## Recall in 30 seconds

- Observation and state are different: the agent acts from evidence about a hidden process.
- A belief is a probability distribution over states and is sufficient for optimal control when updated exactly.
- History-based recurrent policies approximate filtering but may forget, miscalibrate, or exploit spurious temporal cues.
- Active sensing matters because actions can improve information as well as reward.

## Watch in order

> [!method] Why this sequence
> Watch in order: foundation first, then mechanism, then application or diagnostics where the topic needs it. Coverage boundary: Recurrent-policy implementation details are secondary to the POMDP and partially observable RL formulation.

### 1. CS885 Module 4: Partially Observable Reinforcement Learning

> [!video] Pascal Poupart · English · university course
> **Purpose:** Graduate lecture connecting POMDPs and belief-state reasoning to reinforcement learning under partial observability, including learned history representations.
> [Watch on YouTube](https://www.youtube.com/watch?v=96V9tWNFaS4)

> [!summary] After watching
> Close the videos and explain the recall bullets in your own words. Add only corrections or a worked example below—do not recreate the lecture.

## My correction or example

-
