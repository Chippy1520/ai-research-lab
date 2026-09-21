---
generated_by: "build_obsidian_vault.py"
type: "curriculum-lesson"
aliases: ["Backpropagation, Initialization & Normalization"]
day: 13
cycle: 5
domain: "Machine Learning"
stage: "Foundations"
status: "planned"
source: ["curriculum_plan.json", "curriculum_resources.json"]
tags: ["curriculum", "machine-learning", "foundations"]
cssclasses: ["research-note", "curriculum-note"]
related_concepts: ["Mind Map/Nodes/systems.md", "Mind Map/Nodes/learning.md"]
related_papers: []
---

[[Home|Research Lab]]  /  [[Curriculum/Curriculum|Curriculum]]

# Day 13 — Backpropagation, Initialization & Normalization

> [!curriculum] Machine Learning · Foundations
> **Cycle 5** · **status: planned**
> Use the videos for first-pass learning; use this note for fast recall without rewatching.

> [!sequence] Learning sequence
> - [[Curriculum/Lessons/Day 12 - Monte Carlo and Temporal-Difference Learning|← Day 12]]
> - [[Curriculum/Curriculum|Curriculum map]]
> - [[Curriculum/Lessons/Day 14 - Multi-View Geometry, Epipolar Constraints & SfM|Day 14 →]]

> [!concepts] Knowledge-graph concepts
> - [[Mind Map/Nodes/systems|Systems]]
> - [[Mind Map/Nodes/learning|Learning]]

## Brief description

Backpropagation applies the chain rule efficiently through a computation graph; initialization and normalization keep signals and gradients in workable ranges so optimization can use that information.

## Recall in 30 seconds

- The forward pass stores intermediates; the reverse pass propagates vector-Jacobian products.
- Initialization should preserve activation and gradient scale across depth.
- Normalization changes optimization geometry and stabilizes feature statistics, but its behavior depends on train/eval mode and batch structure.
- Vanishing, exploding, dead, or noisy gradients are diagnostic symptoms, not problems solved by backprop alone.

## Watch in order

> [!method] Why this sequence
> Watch in order: foundation first, then mechanism, then application or diagnostics where the topic needs it.

### 1. CS231n Winter 2016: Lecture 4: Backpropagation, Neural Networks 1

> [!video] Andrej Karpathy · English · respected educator
> **Purpose:** Derives computational graphs, chain-rule differentiation, gradient flow, and neural-network backpropagation.
> [Watch on YouTube](https://www.youtube.com/watch?v=i94OvYb6noo)

### 2. Lecture 6 | Training Neural Networks I

> [!video] Stanford University School of Engineering · English · university course
> **Purpose:** Covers activation behavior, data preprocessing, weight initialization, normalization, and practical training stability.
> [Watch on YouTube](https://www.youtube.com/watch?v=wEoyxE0GP2M)

> [!summary] After watching
> Close the videos and explain the recall bullets in your own words. Add only corrections or a worked example below—do not recreate the lecture.

## My correction or example

-
