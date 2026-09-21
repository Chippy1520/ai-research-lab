---
generated_by: "build_obsidian_vault.py"
type: "curriculum-lesson"
aliases: ["NeRF Volume Rendering & Positional Encoding"]
day: 29
cycle: 10
domain: "Computer Vision"
stage: "Modern"
status: "planned"
source: ["curriculum_plan.json", "curriculum_resources.json"]
tags: ["curriculum", "computer-vision", "modern"]
cssclasses: ["research-note", "curriculum-note"]
related_concepts: ["Mind Map/Nodes/perception.md"]
related_papers: []
---

[[Home|Research Lab]]  /  [[Curriculum/Curriculum|Curriculum]]

# Day 29 — NeRF Volume Rendering & Positional Encoding

> [!curriculum] Computer Vision · Modern
> **Cycle 10** · **status: planned**
> Use the videos for first-pass learning; use this note for fast recall without rewatching.

> [!sequence] Learning sequence
> - [[Curriculum/Lessons/Day 28 - Diffusion, Score Matching & SDEs|← Day 28]]
> - [[Curriculum/Curriculum|Curriculum map]]
> - [[Curriculum/Lessons/Day 30 - Model-Based RL and Uncertainty-Aware Planning|Day 30 →]]

> [!concepts] Knowledge-graph concepts
> - [[Mind Map/Nodes/perception|Perception]]

## Brief description

NeRF represents a scene as a continuous field of density and view-dependent radiance, then synthesizes images by integrating samples along camera rays; positional encoding lets an MLP represent fine spatial variation.

## Recall in 30 seconds

- Each 3D sample predicts density and color conditioned on position and viewing direction.
- Volume rendering accumulates transmittance-weighted color from front to back along a ray.
- Positional encoding exposes high frequencies that a plain MLP learns poorly.
- Accurate camera poses and many views are central; rendering speed, dynamic scenes, and extrapolation remain challenges.

## Watch in order

> [!method] Why this sequence
> Watch in order: foundation first, then mechanism, then application or diagnostics where the topic needs it.

### 1. 3D Computer Vision | Neural Field Representations

> [!video] CVRP Lab at NUS · English · university course
> **Purpose:** University lecture covering neural fields and NeRF's coordinate MLP, positional encoding, ray sampling, and differentiable volume rendering.
> [Watch on YouTube](https://www.youtube.com/watch?v=a5hbNFRxZT4)

> [!summary] After watching
> Close the videos and explain the recall bullets in your own words. Add only corrections or a worked example below—do not recreate the lecture.

## My correction or example

-
