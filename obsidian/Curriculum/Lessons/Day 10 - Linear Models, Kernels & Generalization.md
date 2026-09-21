---
generated_by: "build_obsidian_vault.py"
type: "curriculum-lesson"
aliases: ["Linear Models, Kernels & Generalization"]
day: 10
cycle: 4
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

# Day 10 — Linear Models, Kernels & Generalization

> [!curriculum] Machine Learning · Foundations
> **Cycle 4** · **status: planned**
> Use the videos for first-pass learning; use this note for fast recall without rewatching.

> [!sequence] Learning sequence
> - [[Curriculum/Lessons/Day 09 - Dynamic Programming- Policy-Value Iteration|← Day 09]]
> - [[Curriculum/Curriculum|Curriculum map]]
> - [[Curriculum/Lessons/Day 11 - Projective Geometry & Camera Calibration|Day 11 →]]

> [!concepts] Knowledge-graph concepts
> - [[Mind Map/Nodes/systems|Systems]]
> - [[Mind Map/Nodes/learning|Learning]]

## Brief description

Linear predictors provide interpretable baselines, kernels make linear learning nonlinear through similarity functions, and generalization theory explains why fitting training data is not the same as predicting new data.

## Recall in 30 seconds

- Linear models are linear in parameters; feature maps can make their decision boundary nonlinear in the input.
- The kernel trick computes inner products in an implicit feature space.
- Margin, regularization, model capacity, and sample size jointly affect generalization.
- A flexible kernel can still overfit, scale poorly with dataset size, and fail under distribution shift.

## Watch in order

> [!method] Why this sequence
> Watch in order: foundation first, then mechanism, then application or diagnostics where the topic needs it.

### 1. Lecture 03 -The Linear Model I

> [!video] caltech · English · university course
> **Purpose:** Builds linear prediction and classification from the hypothesis-set and learning-algorithm viewpoint.
> [Watch on YouTube](https://www.youtube.com/watch?v=FIbVs5GbBlQ)

### 2. Lecture 15 - Kernel Methods

> [!video] caltech · English · university course
> **Purpose:** Introduces feature mappings, the kernel trick, nonlinear decision functions, and kernelized learning.
> [Watch on YouTube](https://www.youtube.com/watch?v=XUj5JbQihlU)

### 3. Lecture 05 - Training Versus Testing

> [!video] caltech · English · university course
> **Purpose:** Completes the sequence with out-of-sample error, generalization, and the distinction between fitting and learning.
> [Watch on YouTube](https://www.youtube.com/watch?v=SEYAnnLazMU)

> [!summary] After watching
> Close the videos and explain the recall bullets in your own words. Add only corrections or a worked example below—do not recreate the lecture.

## My correction or example

-
