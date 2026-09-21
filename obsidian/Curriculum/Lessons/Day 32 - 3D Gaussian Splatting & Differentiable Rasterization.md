---
generated_by: "build_obsidian_vault.py"
type: "curriculum-lesson"
aliases: ["3D Gaussian Splatting & Differentiable Rasterization"]
day: 32
cycle: 11
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

# Day 32 — 3D Gaussian Splatting & Differentiable Rasterization

> [!curriculum] Computer Vision · Modern
> **Cycle 11** · **status: planned**
> Use the videos for first-pass learning; use this note for fast recall without rewatching.

> [!sequence] Learning sequence
> - [[Curriculum/Lessons/Day 31 - Flow Matching & Optimal-Transport Paths|← Day 31]]
> - [[Curriculum/Curriculum|Curriculum map]]
> - [[Curriculum/Lessons/Day 33 - POMDPs, Belief State & Recurrent Policies|Day 33 →]]

> [!concepts] Knowledge-graph concepts
> - [[Mind Map/Nodes/perception|Perception]]

## Brief description

3D Gaussian Splatting represents a scene with anisotropic colored Gaussians and renders them by differentiable projection and alpha composition, trading NeRF-style implicit fields for fast explicit primitives.

## Recall in 30 seconds

- Each Gaussian stores position, covariance, opacity, and view-dependent appearance.
- Projection turns a 3D covariance into a screen-space ellipse that can be sorted and composited.
- Optimization alternates parameter updates with densification and pruning to allocate detail.
- Fast rendering comes with memory cost, visibility-order approximations, and difficulty handling dynamics or sparse views.

## Watch in order

> [!method] Why this sequence
> Watch in order: foundation first, then mechanism, then application or diagnostics where the topic needs it. Coverage boundary: Low-level CUDA implementation and production renderer engineering are not the lecture's primary focus.

### 1. 3D Gaussian Splatting | Guest Lecture for "Computer Graphics in the AI Era"

> [!video] Barney (Barnabás) Börcsök · English · respected educator
> **Purpose:** Full academic guest lecture on the Gaussian scene representation, projection and splatting, differentiable alpha compositing, optimization, and rendering.
> [Watch on YouTube](https://www.youtube.com/watch?v=MBVmQSA24Yk)

> [!summary] After watching
> Close the videos and explain the recall bullets in your own words. Add only corrections or a worked example below—do not recreate the lecture.

## My correction or example

-
