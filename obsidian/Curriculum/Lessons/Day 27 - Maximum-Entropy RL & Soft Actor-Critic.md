---
generated_by: "build_obsidian_vault.py"
type: "curriculum-lesson"
aliases: ["Maximum-Entropy RL & Soft Actor-Critic"]
day: 27
cycle: 9
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

# Day 27 — Maximum-Entropy RL & Soft Actor-Critic

> [!curriculum] Embodied AI & RL Robotics · Modern
> **Cycle 9** · **status: planned**
> Use the videos for first-pass learning; use this note for fast recall without rewatching.

> [!sequence] Learning sequence
> - [[Curriculum/Lessons/Day 26 - Self-Supervised Visual Representation Learning|← Day 26]]
> - [[Curriculum/Curriculum|Curriculum map]]
> - [[Curriculum/Lessons/Day 28 - Diffusion, Score Matching & SDEs|Day 28 →]]

> [!concepts] Knowledge-graph concepts
> - [[Mind Map/Nodes/systems|Systems]]
> - [[Mind Map/Nodes/policy|Policies / VLA]]

## Brief description

Maximum-entropy reinforcement learning optimizes reward while preserving policy entropy; Soft Actor-Critic implements this with off-policy critics and a stochastic actor for robust continuous control.

## Recall in 30 seconds

- The objective rewards both task return and entropy, so optimal behavior remains stochastic when several actions are useful.
- Soft values replace the hard maximum with an entropy-regularized backup.
- SAC learns twin critics from replay and updates a reparameterized stochastic actor.
- Temperature controls the reward-entropy trade and can be adapted toward a target entropy.

## Watch in order

> [!method] Why this sequence
> Watch in order: foundation first, then mechanism, then application or diagnostics where the topic needs it.

### 1. L1 MDPs, Exact Solution Methods, Max-ent RL (Foundations of Deep RL Series)

> [!video] Pieter Abbeel · English · respected educator
> **Purpose:** Derives the maximum-entropy objective and soft value-learning foundations.
> [Watch on YouTube](https://www.youtube.com/watch?v=2GwBez0D20A)

### 2. L5 DDPG and SAC (Foundations of Deep RL Series)

> [!video] Pieter Abbeel · English · respected educator
> **Purpose:** Builds on maximum-entropy RL to present Soft Actor-Critic, its actor-critic updates, and its relation to deterministic off-policy control.
> [Watch on YouTube](https://www.youtube.com/watch?v=pg-lKy7JIRk)

> [!summary] After watching
> Close the videos and explain the recall bullets in your own words. Add only corrections or a worked example below—do not recreate the lecture.

## My correction or example

-
