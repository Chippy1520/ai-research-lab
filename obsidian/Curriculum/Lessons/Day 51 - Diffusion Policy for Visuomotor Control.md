---
generated_by: "build_obsidian_vault.py"
type: "curriculum-lesson"
aliases: ["Diffusion Policy for Visuomotor Control"]
day: 51
cycle: 17
domain: "Embodied AI & RL Robotics"
stage: "Frontier"
status: "planned"
source: ["curriculum_plan.json", "curriculum_resources.json"]
tags: ["curriculum", "embodied-ai-rl-robotics", "frontier"]
cssclasses: ["research-note", "curriculum-note"]
related_concepts: ["Mind Map/Nodes/diffusion-policy.md", "Mind Map/Nodes/systems.md", "Mind Map/Nodes/policy.md"]
related_papers: []
---

[[Home|Research Lab]]  /  [[Curriculum/Curriculum|Curriculum]]

# Day 51 — Diffusion Policy for Visuomotor Control

> [!curriculum] Embodied AI & RL Robotics · Frontier
> **Cycle 17** · **status: planned**
> Use the videos for first-pass learning; use this note for fast recall without rewatching.

> [!sequence] Learning sequence
> - [[Curriculum/Lessons/Day 50 - Domain Adaptation, Test-Time Adaptation & Robustness|← Day 50]]
> - [[Curriculum/Curriculum|Curriculum map]]
> - [[Curriculum/Lessons/Day 52 - Scaling Laws, Data Mixtures & Test-Time Compute|Day 52 →]]

> [!concepts] Knowledge-graph concepts
> - [[Mind Map/Nodes/diffusion-policy|Diffusion Policy]]
> - [[Mind Map/Nodes/systems|Systems]]
> - [[Mind Map/Nodes/policy|Policies / VLA]]

## Brief description

Diffusion Policy models a distribution over action sequences and generates a receding-horizon chunk conditioned on observations, using iterative denoising to represent multimodal visuomotor behavior.

## Recall in 30 seconds

- The policy denoises an action trajectory rather than predicting one action independently.
- Action chunks capture temporal coherence and reduce compounding from stepwise behavior cloning.
- At deployment, the robot repeatedly conditions, samples a chunk, executes part, and replans.
- Sampling latency, observation alignment, chunk horizon, multimodal data quality, and closed-loop correction determine control performance.

## Watch in order

> [!method] Why this sequence
> Watch in order: foundation first, then mechanism, then application or diagnostics where the topic needs it.

### 1. Diffusion in RL and robotics: how expressive policies changed how we use continuous actions

> [!video] Simons Institute for the Theory of Computing · English · official conference
> **Purpose:** Explains why diffusion models are useful as expressive, multimodal continuous-action policies in RL and robotics.
> [Watch on YouTube](https://www.youtube.com/watch?v=agi3xLTGyaU)

### 2. Princeton Robotics - Russ Tedrake - Dexterous Manipulation with Diffusion Policies

> [!video] Intelligent Robot Motion Lab · English · university course
> **Purpose:** Connects action diffusion to visuomotor manipulation, receding-horizon execution, dexterity, and real-robot deployment.
> [Watch on YouTube](https://www.youtube.com/watch?v=whpK0HDtOJ0)

> [!summary] After watching
> Close the videos and explain the recall bullets in your own words. Add only corrections or a worked example below—do not recreate the lecture.

## My correction or example

-
