---
generated_by: "build_obsidian_vault.py"
type: "curriculum-lesson"
aliases: ["Q-Learning, Function Approximation & DQN"]
day: 15
cycle: 5
domain: "Embodied AI & RL Robotics"
stage: "Foundations"
status: "planned"
source: ["curriculum_plan.json", "curriculum_resources.json"]
tags: ["curriculum", "embodied-ai-rl-robotics", "foundations"]
cssclasses: ["research-note", "curriculum-note"]
related_concepts: ["Mind Map/Nodes/q-learning.md", "Mind Map/Nodes/learning.md", "Mind Map/Nodes/systems.md", "Mind Map/Nodes/policy.md"]
related_papers: []
---

[[Home|Research Lab]]  /  [[Curriculum/Curriculum|Curriculum]]

# Day 15 — Q-Learning, Function Approximation & DQN

> [!curriculum] Embodied AI & RL Robotics · Foundations
> **Cycle 5** · **status: planned**
> Use the videos for first-pass learning; use this note for fast recall without rewatching.

> [!sequence] Learning sequence
> - [[Curriculum/Lessons/Day 14 - Multi-View Geometry, Epipolar Constraints & SfM|← Day 14]]
> - [[Curriculum/Curriculum|Curriculum map]]
> - [[Curriculum/Lessons/Day 16 - CNN Inductive Biases & Modern ConvNets|Day 16 →]]

> [!concepts] Knowledge-graph concepts
> - [[Mind Map/Nodes/q-learning|Q-learning]]
> - [[Mind Map/Nodes/learning|Learning]]
> - [[Mind Map/Nodes/systems|Systems]]
> - [[Mind Map/Nodes/policy|Policies / VLA]]

## Brief description

Q-learning estimates action values from off-policy bootstrapped targets; DQN extends it to high-dimensional observations with a neural network, replay buffer, and target network.

## Recall in 30 seconds

- Q-learning targets reward plus the best estimated next action, independent of the behavior policy.
- Function approximation couples updates across states, so replay reduces correlation and a target network slows target drift.
- Overestimation, extrapolation, reward scale, and insufficient exploration can dominate performance.
- DQN is principally a discrete-action method; continuous control needs another policy representation.

## Watch in order

> [!method] Why this sequence
> Watch in order: foundation first, then mechanism, then application or diagnostics where the topic needs it.

### 1. RL Course by David Silver - Lecture 5: Model Free Control

> [!video] Google DeepMind · English · research lab
> **Purpose:** Develops model-free control, on-policy versus off-policy learning, SARSA, and tabular Q-learning.
> [Watch on YouTube](https://www.youtube.com/watch?v=0g4j2k_Ggc4)

### 2. Reinforcement Learning 5: Function Approximation and Deep Reinforcement Learning

> [!video] Google DeepMind · English · research lab
> **Purpose:** Moves from tabular values to function approximation and deep Q-learning, including instability and DQN stabilization mechanisms.
> [Watch on YouTube](https://www.youtube.com/watch?v=wAk1lxmiW4c)

> [!summary] After watching
> Close the videos and explain the recall bullets in your own words. Add only corrections or a worked example below—do not recreate the lecture.

## My correction or example

-
