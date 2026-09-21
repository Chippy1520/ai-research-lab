---
generated_by: "build_obsidian_vault.py"
type: "curriculum-lesson"
aliases: ["Flow Matching & Optimal-Transport Paths"]
day: 31
cycle: 11
domain: "Machine Learning"
stage: "Modern"
status: "planned"
source: ["curriculum_plan.json", "curriculum_resources.json"]
tags: ["curriculum", "machine-learning", "modern"]
cssclasses: ["research-note", "curriculum-note"]
related_concepts: ["Mind Map/Nodes/flow-matching.md", "Mind Map/Nodes/systems.md", "Mind Map/Nodes/learning.md"]
related_papers: ["Papers/SmolVLA and LeRobot.md"]
---

[[Home|Research Lab]]  /  [[Curriculum/Curriculum|Curriculum]]

# Day 31 — Flow Matching & Optimal-Transport Paths

> [!curriculum] Machine Learning · Modern
> **Cycle 11** · **status: planned**
> Use the videos for first-pass learning; use this note for fast recall without rewatching.

> [!sequence] Learning sequence
> - [[Curriculum/Lessons/Day 30 - Model-Based RL and Uncertainty-Aware Planning|← Day 30]]
> - [[Curriculum/Curriculum|Curriculum map]]
> - [[Curriculum/Lessons/Day 32 - 3D Gaussian Splatting & Differentiable Rasterization|Day 32 →]]

> [!concepts] Knowledge-graph concepts
> - [[Mind Map/Nodes/flow-matching|Flow matching]]
> - [[Mind Map/Nodes/systems|Systems]]
> - [[Mind Map/Nodes/learning|Learning]]

> [!study] Paper companions
> - [[Papers/SmolVLA and LeRobot|SmolVLA and LeRobot]]

## Brief description

Flow matching learns a time-dependent vector field that transports a simple distribution to the data distribution; choosing the probability path determines the target velocities and links the method to optimal transport.

## Recall in 30 seconds

- Training regresses a vector field on samples drawn along a chosen conditional path.
- Generation solves an ODE from noise to data rather than iteratively denoising a stochastic chain.
- Different couplings and paths produce different curvature, variance, and integration cost.
- Optimal-transport-inspired paths can be straighter, but practical minibatch couplings only approximate global transport.

## Watch in order

> [!method] Why this sequence
> Watch in order: foundation first, then mechanism, then application or diagnostics where the topic needs it.

### 1. "Optimal Transport for Statistics and Machine Learning" Prof. Philippe Rigollet, MIT

> [!video] Center for Intelligent Systems CIS EPFL · English · university course
> **Purpose:** Supplies the optimal-transport foundation: couplings, transport costs, and Wasserstein geometry.
> [Watch on YouTube](https://www.youtube.com/watch?v=G8KsRBWb1PE)

### 2. MIT 6.S184: Flow Matching and Diffusion Models - Lecture 02: Flow Matching (2026)

> [!video] Peter Holderrieth · English · respected educator
> **Purpose:** Derives conditional probability paths and velocity-field regression, including transport-inspired paths used by flow-matching models.
> [Watch on YouTube](https://www.youtube.com/watch?v=PNkMKWW8Khw)

> [!summary] After watching
> Close the videos and explain the recall bullets in your own words. Add only corrections or a worked example below—do not recreate the lecture.

## My correction or example

-
