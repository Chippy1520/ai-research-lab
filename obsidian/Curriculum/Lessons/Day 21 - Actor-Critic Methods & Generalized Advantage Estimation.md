---
generated_by: "build_obsidian_vault.py"
type: "curriculum-lesson"
aliases: ["Actor-Critic Methods & Generalized Advantage Estimation"]
day: 21
cycle: 7
domain: "Embodied AI & RL Robotics"
stage: "Core"
status: "planned"
source: ["curriculum_plan.json", "curriculum_resources.json"]
tags: ["curriculum", "embodied-ai-rl-robotics", "core"]
cssclasses: ["research-note", "curriculum-note"]
related_concepts: ["Mind Map/Nodes/systems.md", "Mind Map/Nodes/policy.md"]
related_papers: []
---

[[Home|Research Lab]]  /  [[Curriculum/Curriculum|Curriculum]]

# Day 21 — Actor-Critic Methods & Generalized Advantage Estimation

> [!curriculum] Embodied AI & RL Robotics · Core
> **Cycle 7** · **status: planned**
> Use the videos for first-pass learning; use this note for fast recall without rewatching.

> [!sequence] Learning sequence
> - [[Curriculum/Lessons/Day 20 - Semantic, Instance & Panoptic Segmentation|← Day 20]]
> - [[Curriculum/Curriculum|Curriculum map]]
> - [[Curriculum/Lessons/Day 22 - Normalizing Flows & Change of Variables|Day 22 →]]

> [!concepts] Knowledge-graph concepts
> - [[Mind Map/Nodes/systems|Systems]]
> - [[Mind Map/Nodes/policy|Policies / VLA]]

## Brief description

Actor-critic methods use a learned value function to train a policy, combining the flexibility of policy gradients with bootstrapped credit assignment; GAE controls the bias-variance trade in advantages.

## Recall in 30 seconds

- The actor chooses actions; the critic estimates value and supplies an advantage-like learning signal.
- A one-step TD error is a noisy local advantage estimate.
- GAE exponentially mixes multi-step TD residuals using a parameter that trades variance for bias.
- Critic error can bias the actor, so value loss, advantage scale, and shared representations require monitoring.

## Watch in order

> [!method] Why this sequence
> Watch in order: foundation first, then mechanism, then application or diagnostics where the topic needs it.

### 1. DeepMind x UCL RL Lecture Series - Policy-Gradient and Actor-Critic methods [9/13]

> [!video] Google DeepMind · English · research lab
> **Purpose:** Builds actor-critic algorithms from policy gradients, value-function critics, bootstrapping, and compatible learning signals.
> [Watch on YouTube](https://www.youtube.com/watch?v=y3oqOjHilio)

### 2. L3 Policy Gradients and Advantage Estimation (Foundations of Deep RL Series)

> [!video] Pieter Abbeel · English · respected educator
> **Purpose:** Focuses on advantage estimators and the bias-variance tradeoff culminating in generalized advantage estimation.
> [Watch on YouTube](https://www.youtube.com/watch?v=AKbX1Zvo7r8)

> [!summary] After watching
> Close the videos and explain the recall bullets in your own words. Add only corrections or a worked example below—do not recreate the lecture.

## My correction or example

-
