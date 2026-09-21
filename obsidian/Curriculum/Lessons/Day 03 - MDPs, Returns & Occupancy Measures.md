---
generated_by: "build_obsidian_vault.py"
type: "curriculum-lesson"
aliases: ["MDPs, Returns & Occupancy Measures"]
day: 3
cycle: 1
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

# Day 03 — MDPs, Returns & Occupancy Measures

> [!curriculum] Embodied AI & RL Robotics · Foundations
> **Cycle 1** · **status: planned**
> Use the videos for first-pass learning; use this note for fast recall without rewatching.

> [!sequence] Learning sequence
> - [[Curriculum/Lessons/Day 02 - Image Formation, Sampling & Color|← Day 02]]
> - [[Curriculum/Curriculum|Curriculum map]]
> - [[Curriculum/Lessons/Day 04 - Probability, Estimation & Statistical Learning|Day 04 →]]

> [!concepts] Knowledge-graph concepts
> - [[Mind Map/Nodes/systems|Systems]]
> - [[Mind Map/Nodes/policy|Policies / VLA]]

## Brief description

A Markov decision process formalizes sequential choice with states, actions, transitions, rewards, and discounting; returns value trajectories, while occupancy measures describe how a policy distributes visits over state-action pairs.

## Recall in 30 seconds

- The Markov assumption makes the current state sufficient for predicting the next transition.
- A return aggregates future rewards, usually with discounting or a finite horizon.
- Value functions are expectations under a policy and transition model, not properties of a state alone.
- Occupancy measures connect trajectory optimization to expectations over visited state-action pairs.

## Watch in order

> [!method] Why this sequence
> Watch in order: foundation first, then mechanism, then application or diagnostics where the topic needs it. Coverage boundary: Occupancy measures are developed through state-visitation distributions rather than a standalone measure-theoretic treatment.

### 1. RL Course by David Silver - Lecture 2: Markov Decision Process

> [!video] Google DeepMind · English · research lab
> **Purpose:** Establishes MDPs, policies, trajectories, discounted returns, value functions, and Bellman relationships.
> [Watch on YouTube](https://www.youtube.com/watch?v=lfHX2hHRMVQ)

### 2. L1 MDPs, Exact Solution Methods, Max-ent RL (Foundations of Deep RL Series)

> [!video] Pieter Abbeel · English · respected educator
> **Purpose:** Extends the MDP treatment to policy-induced state visitation distributions, exact solution methods, and the occupancy perspective used in maximum-entropy RL.
> [Watch on YouTube](https://www.youtube.com/watch?v=2GwBez0D20A)

> [!summary] After watching
> Close the videos and explain the recall bullets in your own words. Add only corrections or a worked example below—do not recreate the lecture.

## My correction or example

-
