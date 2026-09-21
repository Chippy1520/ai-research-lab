---
generated_by: "build_obsidian_vault.py"
type: "curriculum-lesson"
aliases: ["Projective Geometry & Camera Calibration"]
day: 11
cycle: 4
domain: "Computer Vision"
stage: "Foundations"
status: "planned"
source: ["curriculum_plan.json", "curriculum_resources.json"]
tags: ["curriculum", "computer-vision", "foundations"]
cssclasses: ["research-note", "curriculum-note"]
related_concepts: ["Mind Map/Nodes/perception.md"]
related_papers: []
---

[[Home|Research Lab]]  /  [[Curriculum/Curriculum|Curriculum]]

# Day 11 — Projective Geometry & Camera Calibration

> [!curriculum] Computer Vision · Foundations
> **Cycle 4** · **status: planned**
> Use the videos for first-pass learning; use this note for fast recall without rewatching.

> [!sequence] Learning sequence
> - [[Curriculum/Lessons/Day 10 - Linear Models, Kernels & Generalization|← Day 10]]
> - [[Curriculum/Curriculum|Curriculum map]]
> - [[Curriculum/Lessons/Day 12 - Monte Carlo and Temporal-Difference Learning|Day 12 →]]

> [!concepts] Knowledge-graph concepts
> - [[Mind Map/Nodes/perception|Perception]]

## Brief description

Projective geometry explains how 3D points map to an image, while calibration estimates the intrinsic and extrinsic camera parameters needed to recover rays, poses, and metric measurements.

## Recall in 30 seconds

- Homogeneous coordinates represent perspective projection and points at infinity uniformly.
- Intrinsics describe the camera's internal projection; extrinsics place the camera in the world.
- Calibration uses known geometry and many correspondences because noise and distortion make one view insufficient.
- A pixel back-projects to a ray; depth requires extra geometry, motion, or prior knowledge.

## Watch in order

> [!method] Why this sequence
> Watch in order: foundation first, then mechanism, then application or diagnostics where the topic needs it.

### 1. 3D Computer Vision | Lecture 1 (Part 1): 2D and 1D projective geometry

> [!video] CVRP Lab at NUS · English · university course
> **Purpose:** Develops homogeneous coordinates, projective transformations, points at infinity, and the geometry underlying cameras.
> [Watch on YouTube](https://www.youtube.com/watch?v=LAHQ_qIzNGU)

### 2. Linear Camera Model | Camera Calibration

> [!video] First Principles of Computer Vision · English · university course
> **Purpose:** Introduces the camera projection matrix and the relationship between world, camera, and image coordinates.
> [Watch on YouTube](https://www.youtube.com/watch?v=qByYk6JggQU)

### 3. Camera Calibration | Camera Calibration

> [!video] First Principles of Computer Vision · English · university course
> **Purpose:** Explains how camera parameters are estimated from geometric correspondences and calibration constraints.
> [Watch on YouTube](https://www.youtube.com/watch?v=GUbWsXU1mac)

> [!summary] After watching
> Close the videos and explain the recall bullets in your own words. Add only corrections or a worked example below—do not recreate the lecture.

## My correction or example

-
