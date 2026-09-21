---
generated_by: "build_obsidian_vault.py"
type: "curriculum-lesson"
aliases: ["Variational Inference, ELBO & VAEs"]
day: 19
cycle: 7
domain: "Machine Learning"
stage: "Core"
status: "planned"
source: ["curriculum_plan.json", "curriculum_resources.json"]
tags: ["curriculum", "machine-learning", "core"]
cssclasses: ["research-note", "curriculum-note"]
related_concepts: ["Mind Map/Nodes/systems.md", "Mind Map/Nodes/learning.md"]
related_papers: []
---

[[Home|Research Lab]]  /  [[Curriculum/Curriculum|Curriculum]]

# Day 19 — Variational Inference, ELBO & VAEs

> [!curriculum] Machine Learning · Core
> **Cycle 7** · **status: planned**
> Use the videos for first-pass learning; use this note for fast recall without rewatching.

> [!sequence] Learning sequence
> - [[Curriculum/Lessons/Day 18 - Policy Gradients and Variance Reduction|← Day 18]]
> - [[Curriculum/Curriculum|Curriculum map]]
> - [[Curriculum/Lessons/Day 20 - Semantic, Instance & Panoptic Segmentation|Day 20 →]]

> [!concepts] Knowledge-graph concepts
> - [[Mind Map/Nodes/systems|Systems]]
> - [[Mind Map/Nodes/learning|Learning]]

## Brief description

Variational inference replaces an intractable posterior with a tractable approximation; the ELBO balances data reconstruction against posterior-to-prior regularization, and a VAE amortizes this inference with an encoder.

## Recall in 30 seconds

- The ELBO is a lower bound because the gap to log evidence is a KL divergence to the true posterior.
- The encoder predicts an approximate latent posterior; the decoder maps latent samples back to data distributions.
- Reparameterization separates sampling noise from differentiable distribution parameters.
- Posterior collapse occurs when the decoder can ignore the latent code; likelihood quality and sample appearance are not identical goals.

## Watch in order

> [!method] Why this sequence
> Watch in order: foundation first, then mechanism, then application or diagnostics where the topic needs it.

### 1. MIT 6.S191 (2023): Deep Generative Modeling

> [!video] Alexander Amini · English · respected educator
> **Purpose:** Introduces latent-variable generative models, variational inference, the ELBO, reparameterization, VAE training, and sampling.
> [Watch on YouTube](https://www.youtube.com/watch?v=3G5hWM6jqPk)

> [!summary] After watching
> Close the videos and explain the recall bullets in your own words. Add only corrections or a worked example below—do not recreate the lecture.

## My correction or example

-
