---
generated_by: "build_obsidian_vault.py"
type: "curriculum-lesson"
aliases: ["4D Dynamic Reconstruction & Neural Scene Flow"]
day: 47
cycle: 16
domain: "Computer Vision"
stage: "Integration"
status: "planned"
source: ["curriculum_plan.json", "curriculum_resources.json"]
tags: ["curriculum", "computer-vision", "integration"]
cssclasses: ["research-note", "curriculum-note"]
related_concepts: ["Mind Map/Nodes/perception.md"]
related_papers: []
---

[[Home|Research Lab]]  /  [[Curriculum/Curriculum|Curriculum]]

# Day 47 — 4D Dynamic Reconstruction & Neural Scene Flow

> [!curriculum] Computer Vision · Integration
> **Cycle 16** · **status: planned**
> Use the videos for first-pass learning; use this note for fast recall without rewatching.

> [!sequence] Learning sequence
> - [[Curriculum/Lessons/Day 46 - Causal Representation Learning & Invariance|← Day 46]]
> - [[Curriculum/Curriculum|Curriculum map]]
> - [[Curriculum/Lessons/Day 48 - Motion Planning, Trajectory Optimization & MPC|Day 48 →]]

> [!concepts] Knowledge-graph concepts
> - [[Mind Map/Nodes/perception|Perception]]

## Brief description

4D reconstruction models geometry as it changes through time, combining camera motion, scene deformation, correspondence, and rendering; neural scene flow estimates continuous 3D motion rather than only image-plane displacement.

## Recall in 30 seconds

- Dynamic reconstruction must separate observer motion from non-rigid scene motion.
- Scene flow is 3D displacement over time; optical flow is its projected 2D evidence.
- Temporal consistency and canonical-space deformation reduce ambiguity but impose motion assumptions.
- Occlusion, topology change, sparse views, timing errors, and long sequences expose drift and hallucinated geometry.

## Watch in order

> [!method] Why this sequence
> Watch in order: foundation first, then mechanism, then application or diagnostics where the topic needs it.

### 1. Temporally Coherent 4D Reconstruction of Complex Dynamic Scenes

> [!video] ComputerVisionFoundation Videos · English · official conference
> **Purpose:** Introduces temporally coherent dynamic-scene reconstruction and the geometric constraints needed to recover changing 3D structure.
> [Watch on YouTube](https://www.youtube.com/watch?v=9v6i8VZZE5k)

### 2. Flow4R: Unifying 4D Reconstruction and Tracking with Scene Flow

> [!video] Shenhan Qian · English · respected educator
> **Purpose:** Shows a modern neural formulation that unifies reconstruction, tracking, and scene-flow estimation over time.
> [Watch on YouTube](https://www.youtube.com/watch?v=DmaG6F3qlmk)

> [!summary] After watching
> Close the videos and explain the recall bullets in your own words. Add only corrections or a worked example below—do not recreate the lecture.

## My correction or example

-
