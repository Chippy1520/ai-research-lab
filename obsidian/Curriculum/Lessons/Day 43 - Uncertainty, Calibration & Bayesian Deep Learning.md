---
generated_by: "build_obsidian_vault.py"
type: "curriculum-lesson"
aliases: ["Uncertainty, Calibration & Bayesian Deep Learning"]
day: 43
cycle: 15
domain: "Machine Learning"
stage: "Integration"
status: "planned"
source: ["curriculum_plan.json", "curriculum_resources.json"]
tags: ["curriculum", "machine-learning", "integration"]
cssclasses: ["research-note", "curriculum-note"]
related_concepts: ["Mind Map/Nodes/learning.md", "Mind Map/Nodes/systems.md"]
related_papers: []
---

[[Home|Research Lab]]  /  [[Curriculum/Curriculum|Curriculum]]

# Day 43 — Uncertainty, Calibration & Bayesian Deep Learning

> [!curriculum] Machine Learning · Integration
> **Cycle 15** · **status: planned**
> Use the videos for first-pass learning; use this note for fast recall without rewatching.

> [!sequence] Learning sequence
> - [[Curriculum/Lessons/Day 42 - World Models & Latent Imagination|← Day 42]]
> - [[Curriculum/Curriculum|Curriculum map]]
> - [[Curriculum/Lessons/Day 44 - 3D Scene Understanding and Point-Implicit Representations|Day 44 →]]

> [!concepts] Knowledge-graph concepts
> - [[Mind Map/Nodes/learning|Learning]]
> - [[Mind Map/Nodes/systems|Systems]]

## Brief description

Predictive uncertainty separates noise in outcomes from uncertainty about the model; calibration asks whether stated probabilities match observed frequencies, and Bayesian approximations represent distributions over plausible predictors.

## Recall in 30 seconds

- Aleatoric uncertainty comes from irreducible variability; epistemic uncertainty can shrink with relevant data.
- A calibrated 80% prediction should be correct about 80% of the time within the evaluated population.
- Ensembles, variational methods, and posterior approximations capture different slices of model uncertainty.
- Calibration can fail under shift, and a low expected calibration error can hide class- or region-specific risk.

## Watch in order

> [!method] Why this sequence
> Watch in order: foundation first, then mechanism, then application or diagnostics where the topic needs it.

### 1. Yarin Gal - Uncertainty in Deep Learning | MLSS Kraków 2023

> [!video] ML in PL · English · official conference
> **Purpose:** Covers epistemic and aleatoric uncertainty, approximate Bayesian deep learning, and practical predictive-uncertainty methods.
> [Watch on YouTube](https://www.youtube.com/watch?v=fxiI_akW6MA)

### 2. Meelis Kull: "Calibration and confidence in Machine Learning"

> [!video] University of Tartu Institute of Computer Science · English · university course
> **Purpose:** Adds the distinct calibration perspective: confidence reliability, calibration assessment, and post-hoc correction.
> [Watch on YouTube](https://www.youtube.com/watch?v=zSNQTfKGvhE)

> [!summary] After watching
> Close the videos and explain the recall bullets in your own words. Add only corrections or a worked example below—do not recreate the lecture.

## My correction or example

-
