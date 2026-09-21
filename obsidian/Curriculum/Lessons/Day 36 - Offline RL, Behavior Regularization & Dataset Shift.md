---
generated_by: "build_obsidian_vault.py"
type: "curriculum-lesson"
aliases: ["Offline RL, Behavior Regularization & Dataset Shift"]
day: 36
cycle: 12
domain: "Embodied AI & RL Robotics"
stage: "Modern"
status: "planned"
source: ["curriculum_plan.json", "curriculum_resources.json"]
tags: ["curriculum", "embodied-ai-rl-robotics", "modern"]
cssclasses: ["research-note", "curriculum-note"]
related_concepts: ["Mind Map/Nodes/offline-rl.md", "Mind Map/Nodes/systems.md", "Mind Map/Nodes/policy.md"]
related_papers: []
---

[[Home|Research Lab]]  /  [[Curriculum/Curriculum|Curriculum]]

# Day 36 — Offline RL, Behavior Regularization & Dataset Shift

> [!curriculum] Embodied AI & RL Robotics · Modern
> **Cycle 12** · **status: planned**
> Use the videos for first-pass learning; use this note for fast recall without rewatching.

> [!sequence] Learning sequence
> - [[Curriculum/Lessons/Day 35 - Video Motion- Optical Flow, Tracking & Temporal Models|← Day 35]]
> - [[Curriculum/Curriculum|Curriculum map]]
> - [[Curriculum/Lessons/Day 37 - Graph Neural Networks & Geometric Deep Learning|Day 37 →]]

> [!concepts] Knowledge-graph concepts
> - [[Mind Map/Nodes/offline-rl|Offline RL]]
> - [[Mind Map/Nodes/systems|Systems]]
> - [[Mind Map/Nodes/policy|Policies / VLA]]

## Brief description

Offline RL learns policies only from a fixed dataset, so it must improve without querying the environment while avoiding actions whose values are unsupported by the logged behavior distribution.

## Recall in 30 seconds

- Distribution shift makes the learned policy visit actions that the dataset cannot evaluate reliably.
- Bootstrapping can amplify optimistic errors on out-of-distribution actions.
- Behavior regularization, conservative values, and uncertainty penalties trade improvement against staying near support.
- Dataset coverage and reward quality often matter more than the nominal algorithm.

## Watch in order

> [!method] Why this sequence
> Watch in order: foundation first, then mechanism, then application or diagnostics where the topic needs it.

### 1. CS 285: Lecture 15, Part 1: Offline Reinforcement Learning

> [!video] RAIL · English · research lab
> **Purpose:** Introduces the fixed-dataset setting and why distribution shift breaks ordinary off-policy RL.
> [Watch on YouTube](https://www.youtube.com/watch?v=NV4oSWe1H9o)

### 2. CS 285: Lecture 15, Part 2: Offline Reinforcement Learning

> [!video] RAIL · English · research lab
> **Purpose:** Develops conservative and behavior-constrained approaches for avoiding out-of-distribution actions.
> [Watch on YouTube](https://www.youtube.com/watch?v=9HrN6nHoxD8)

### 3. CS 285: Lecture 15, Part 3: Offline Reinforcement Learning

> [!video] RAIL · English · research lab
> **Purpose:** Completes the lecture with practical offline-RL objectives, algorithm comparisons, and evaluation concerns.
> [Watch on YouTube](https://www.youtube.com/watch?v=YNritd36FB0)

> [!summary] After watching
> Close the videos and explain the recall bullets in your own words. Add only corrections or a worked example below—do not recreate the lecture.

## My correction or example

-
