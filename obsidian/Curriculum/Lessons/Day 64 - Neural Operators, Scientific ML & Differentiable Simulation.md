---
generated_by: "build_obsidian_vault.py"
type: "curriculum-lesson"
aliases: ["Neural Operators, Scientific ML & Differentiable Simulation"]
day: 64
cycle: 22
domain: "Machine Learning"
stage: "Frontier"
status: "planned"
source: ["curriculum_plan.json", "curriculum_resources.json"]
tags: ["curriculum", "machine-learning", "frontier"]
cssclasses: ["research-note", "curriculum-note"]
related_concepts: ["Mind Map/Nodes/sim-stack.md", "Mind Map/Nodes/systems.md", "Mind Map/Nodes/learning.md"]
related_papers: []
---

[[Home|Research Lab]]  /  [[Curriculum/Curriculum|Curriculum]]

# Day 64 — Neural Operators, Scientific ML & Differentiable Simulation

> [!curriculum] Machine Learning · Frontier
> **Cycle 22** · **status: planned**
> Use the videos for first-pass learning; use this note for fast recall without rewatching.

> [!sequence] Learning sequence
> - [[Curriculum/Lessons/Day 63 - Safe RL, Constraints, Shielding & Human Oversight|← Day 63]]
> - [[Curriculum/Curriculum|Curriculum map]]
> - [[Curriculum/Lessons/Day 65 - Event Cameras, Active Vision & Computational Imaging|Day 65 →]]

> [!concepts] Knowledge-graph concepts
> - [[Mind Map/Nodes/sim-stack|Simulation]]
> - [[Mind Map/Nodes/systems|Systems]]
> - [[Mind Map/Nodes/learning|Learning]]

## Brief description

Scientific ML combines physical structure with learned approximations; neural operators learn mappings between functions, and differentiable simulators expose gradients through numerical models for inverse problems and control.

## Recall in 30 seconds

- An operator maps an input field or boundary condition to an output field, not merely one finite vector to another.
- Discretization invariance is a goal: behavior should transfer across meshes or resolutions within the modeled regime.
- Physics-informed losses encode equations and constraints but can be poorly conditioned or under-identify solutions.
- Differentiable simulation gradients inherit approximation, contact, and solver errors and must be checked against perturbations.

## Watch in order

> [!method] Why this sequence
> Watch in order: foundation first, then mechanism, then application or diagnostics where the topic needs it.

### 1. Fourier Neural Operator (FNO) [Physics Informed Machine Learning]

> [!video] Steve Brunton · English · respected educator
> **Purpose:** Introduces operator learning and Fourier Neural Operators for learning mappings between function spaces and PDE solutions.
> [Watch on YouTube](https://www.youtube.com/watch?v=W8PybqAk6Ik)

### 2. ETH Zürich DLSC: Physics-Informed Neural Networks - Introduction

> [!video] CAMLab, ETH Zürich · English · university course
> **Purpose:** Places neural operators alongside physics-informed learning and the broader scientific-ML problem setting.
> [Watch on YouTube](https://www.youtube.com/watch?v=Oh1nhCNlqjg)

### 3. ETH Zürich DLSC: Introduction to Differentiable Physics Part 1

> [!video] CAMLab, ETH Zürich · English · university course
> **Purpose:** Explains differentiable simulation and gradient propagation through physical models.
> [Watch on YouTube](https://www.youtube.com/watch?v=1Edfts3UzaY)

> [!summary] After watching
> Close the videos and explain the recall bullets in your own words. Add only corrections or a worked example below—do not recreate the lecture.

## My correction or example

-
