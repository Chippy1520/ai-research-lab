---
generated_by: "build_obsidian_vault.py"
type: "curriculum-lesson"
aliases: ["Multi-View Geometry, Epipolar Constraints & SfM"]
day: 14
cycle: 5
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

# Day 14 — Multi-View Geometry, Epipolar Constraints & SfM

> [!curriculum] Computer Vision · Foundations
> **Cycle 5** · **status: planned**
> Use the videos for first-pass learning; use this note for fast recall without rewatching.

> [!sequence] Learning sequence
> - [[Curriculum/Lessons/Day 13 - Backpropagation, Initialization & Normalization|← Day 13]]
> - [[Curriculum/Curriculum|Curriculum map]]
> - [[Curriculum/Lessons/Day 15 - Q-Learning, Function Approximation & DQN|Day 15 →]]

> [!concepts] Knowledge-graph concepts
> - [[Mind Map/Nodes/perception|Perception]]

## Brief description

Multi-view geometry uses correspondences between calibrated or uncalibrated images to constrain relative pose and triangulate structure; structure-from-motion repeatedly combines these constraints into a consistent camera-and-scene estimate.

## Recall in 30 seconds

- The epipolar constraint reduces a point search in the second image to a line.
- The essential matrix assumes calibrated cameras; the fundamental matrix absorbs intrinsics.
- Triangulation needs parallax and accurate correspondences; small baselines make depth unstable.
- SfM alternates correspondence, pose, triangulation, and bundle adjustment while rejecting outliers.

## Watch in order

> [!method] Why this sequence
> Watch in order: foundation first, then mechanism, then application or diagnostics where the topic needs it.

### 1. Epipolar Geometry | Uncalibrated Stereo

> [!video] First Principles of Computer Vision · English · university course
> **Purpose:** Explains epipoles, epipolar lines, correspondence constraints, and uncalibrated two-view geometry.
> [Watch on YouTube](https://www.youtube.com/watch?v=6kpBqfgSPRc)

### 2. 3D Computer Vision | Lecture 10 (Part 1): Structure-from-Motion (SfM) and bundle adjustment

> [!video] CVRP Lab at NUS · English · university course
> **Purpose:** Extends two-view constraints to camera-pose and 3D-structure recovery, including bundle adjustment.
> [Watch on YouTube](https://www.youtube.com/watch?v=MUadR35FFqk)

> [!summary] After watching
> Close the videos and explain the recall bullets in your own words. Add only corrections or a worked example below—do not recreate the lecture.

## My correction or example

-
