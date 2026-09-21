---
generated_by: "build_obsidian_vault.py"
type: "curriculum-lesson"
aliases: ["Graph Neural Networks & Geometric Deep Learning"]
day: 37
cycle: 13
domain: "Machine Learning"
stage: "Modern"
status: "planned"
source: ["curriculum_plan.json", "curriculum_resources.json"]
tags: ["curriculum", "machine-learning", "modern"]
cssclasses: ["research-note", "curriculum-note"]
related_concepts: ["Mind Map/Nodes/learning.md", "Mind Map/Nodes/systems.md"]
related_papers: []
---

[[Home|Research Lab]]  /  [[Curriculum/Curriculum|Curriculum]]

# Day 37 — Graph Neural Networks & Geometric Deep Learning

> [!curriculum] Machine Learning · Modern
> **Cycle 13** · **status: planned**
> Use the videos for first-pass learning; use this note for fast recall without rewatching.

> [!sequence] Learning sequence
> - [[Curriculum/Lessons/Day 36 - Offline RL, Behavior Regularization & Dataset Shift|← Day 36]]
> - [[Curriculum/Curriculum|Curriculum map]]
> - [[Curriculum/Lessons/Day 38 - Open-Vocabulary Detection & Foundation Segmentation|Day 38 →]]

> [!concepts] Knowledge-graph concepts
> - [[Mind Map/Nodes/learning|Learning]]
> - [[Mind Map/Nodes/systems|Systems]]

## Brief description

Graph neural networks learn on entities and relations by exchanging messages along edges; geometric deep learning generalizes this idea by respecting permutation, rotation, translation, or manifold symmetries.

## Recall in 30 seconds

- Message passing aggregates neighbor information with shared functions and permutation-invariant pooling.
- Depth expands the receptive field but can cause over-smoothing, over-squashing, and expensive neighborhoods.
- Equivariance makes outputs transform predictably with the input and reduces sample complexity when the symmetry is real.
- Graph construction encodes assumptions and can dominate downstream performance.

## Watch in order

> [!method] Why this sequence
> Watch in order: foundation first, then mechanism, then application or diagnostics where the topic needs it.

### 1. AMMI 2022 Course "Geometric Deep Learning" - Lecture 1 (Introduction) - Michael Bronstein

> [!video] Michael Bronstein · English · university course
> **Purpose:** Introduces geometric priors, symmetry, invariance/equivariance, and the geometric-deep-learning blueprint.
> [Watch on YouTube](https://www.youtube.com/watch?v=5c_-KX1sRDQ)

### 2. AMMI Course "Geometric Deep Learning" - Lecture 6 (Graphs & Sets II) - Petar Veličković

> [!video] Michael Bronstein · English · university course
> **Purpose:** Specializes the blueprint to graphs and sets, covering message passing, graph architectures, expressivity, and limitations.
> [Watch on YouTube](https://www.youtube.com/watch?v=i79ewWQiUX4)

> [!summary] After watching
> Close the videos and explain the recall bullets in your own words. Add only corrections or a worked example below—do not recreate the lecture.

## My correction or example

-
