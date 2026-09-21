---
generated_by: "build_obsidian_vault.py"
type: "curriculum-lesson"
aliases: ["Generative Vision: Latent Diffusion & Controllable Synthesis"]
day: 41
cycle: 14
domain: "Computer Vision"
stage: "Modern"
status: "planned"
source: ["curriculum_plan.json", "curriculum_resources.json"]
tags: ["curriculum", "computer-vision", "modern"]
cssclasses: ["research-note", "curriculum-note"]
related_concepts: ["Mind Map/Nodes/generative.md", "Mind Map/Nodes/perception.md"]
related_papers: []
---

[[Home|Research Lab]]  /  [[Curriculum/Curriculum|Curriculum]]

# Day 41 — Generative Vision: Latent Diffusion & Controllable Synthesis

> [!curriculum] Computer Vision · Modern
> **Cycle 14** · **status: planned**
> Use the videos for first-pass learning; use this note for fast recall without rewatching.

> [!sequence] Learning sequence
> - [[Curriculum/Lessons/Day 40 - Self-Supervised, Contrastive & Multimodal Learning|← Day 40]]
> - [[Curriculum/Curriculum|Curriculum map]]
> - [[Curriculum/Lessons/Day 42 - World Models & Latent Imagination|Day 42 →]]

> [!concepts] Knowledge-graph concepts
> - [[Mind Map/Nodes/generative|Generative models]]
> - [[Mind Map/Nodes/perception|Perception]]

## Brief description

Latent diffusion performs denoising in a compressed representation to reduce cost, while conditioning and guidance steer synthesis through text, images, geometry, or control signals.

## Recall in 30 seconds

- An autoencoder maps pixels to a latent space where diffusion is cheaper.
- A conditional denoiser combines noisy latents, timestep information, and control context.
- Classifier-free guidance trades diversity for stronger conditioning by extrapolating between conditional and unconditional predictions.
- Controllability depends on data alignment and conditioning architecture; guidance cannot recover missing knowledge or exact geometry.

## Watch in order

> [!method] Why this sequence
> Watch in order: foundation first, then mechanism, then application or diagnostics where the topic needs it.

### 1. Latent Diffusion Models

> [!video] William Smith · English · respected educator
> **Purpose:** Explains moving diffusion into an autoencoder latent space and the architecture underlying latent image diffusion.
> [Watch on YouTube](https://www.youtube.com/watch?v=wuwByIh5kDU)

### 2. CMU 10799 S26: Lecture 7 - Guidance & Controllable Generation - Diffusion & Flow Matching

> [!video] Kelly He · English · respected educator
> **Purpose:** Covers classifier/classifier-free guidance and structural conditioning methods for controllable synthesis.
> [Watch on YouTube](https://www.youtube.com/watch?v=lPipzIG6rkc)

> [!summary] After watching
> Close the videos and explain the recall bullets in your own words. Add only corrections or a worked example below—do not recreate the lecture.

## My correction or example

-
