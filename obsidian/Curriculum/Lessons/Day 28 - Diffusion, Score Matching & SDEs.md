---
generated_by: "build_obsidian_vault.py"
type: "curriculum-lesson"
aliases: ["Diffusion, Score Matching & SDEs"]
day: 28
cycle: 10
domain: "Machine Learning"
stage: "Modern"
status: "planned"
source: ["curriculum_plan.json", "curriculum_resources.json"]
tags: ["curriculum", "machine-learning", "modern"]
cssclasses: ["research-note", "curriculum-note"]
related_concepts: ["Mind Map/Nodes/systems.md", "Mind Map/Nodes/learning.md"]
related_papers: []
---

[[Home|Research Lab]]  /  [[Curriculum/Curriculum|Curriculum]]

# Day 28 — Diffusion, Score Matching & SDEs

> [!curriculum] Machine Learning · Modern
> **Cycle 10** · **status: planned**
> Use the videos for first-pass learning; use this note for fast recall without rewatching.

> [!sequence] Learning sequence
> - [[Curriculum/Lessons/Day 27 - Maximum-Entropy RL & Soft Actor-Critic|← Day 27]]
> - [[Curriculum/Curriculum|Curriculum map]]
> - [[Curriculum/Lessons/Day 29 - NeRF Volume Rendering & Positional Encoding|Day 29 →]]

> [!concepts] Knowledge-graph concepts
> - [[Mind Map/Nodes/systems|Systems]]
> - [[Mind Map/Nodes/learning|Learning]]

## Brief description

Diffusion models learn to reverse a gradual corruption process; score matching estimates gradients of log density, and the same evolution can be expressed through stochastic differential equations or related deterministic flows.

## Recall in 30 seconds

- The forward process destroys structure with known noise; the learned reverse process reconstructs samples step by step.
- A denoiser, noise predictor, and score are related parameterizations of the same conditional information.
- The reverse-time SDE requires the score; a probability-flow ODE shares its marginals without stochastic sampling.
- Noise schedule, objective weighting, solver, guidance, and latent representation jointly determine quality and speed.

## Watch in order

> [!method] Why this sequence
> Watch in order: foundation first, then mechanism, then application or diagnostics where the topic needs it.

### 1. MIT 6.S184: Flow Matching and Diffusion Models - Lecture 01 - Generative AI with SDEs (2025)

> [!video] Peter Holderrieth · English · respected educator
> **Purpose:** Introduces forward and reverse stochastic processes and the SDE formulation of diffusion generative models.
> [Watch on YouTube](https://www.youtube.com/watch?v=GCoP2w-Cqtg)

### 2. MIT 6.S184: Flow Matching and Diffusion Models - Lecture 03A - Score Functions (2026)

> [!video] Peter Holderrieth · English · respected educator
> **Purpose:** Develops score functions and score estimation, connecting denoising objectives to reverse-time generation.
> [Watch on YouTube](https://www.youtube.com/watch?v=ngC3QnYSVNM)

> [!summary] After watching
> Close the videos and explain the recall bullets in your own words. Add only corrections or a worked example below—do not recreate the lecture.

## My correction or example

-
