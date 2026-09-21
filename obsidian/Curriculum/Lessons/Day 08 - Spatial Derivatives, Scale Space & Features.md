---
generated_by: "build_obsidian_vault.py"
type: "curriculum-lesson"
aliases: ["Spatial Derivatives, Scale Space & Features"]
day: 8
cycle: 3
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

# Day 08 — Spatial Derivatives, Scale Space & Features

> [!curriculum] Computer Vision · Foundations
> **Cycle 3** · **status: planned**
> Use the videos for first-pass learning; use this note for fast recall without rewatching.

> [!sequence] Learning sequence
> - [[Curriculum/Lessons/Day 07 - Information Theory & Representation|← Day 07]]
> - [[Curriculum/Curriculum|Curriculum map]]
> - [[Curriculum/Lessons/Day 09 - Dynamic Programming- Policy-Value Iteration|Day 09 →]]

> [!concepts] Knowledge-graph concepts
> - [[Mind Map/Nodes/perception|Perception]]

## Brief description

Spatial derivatives reveal local change, scale space controls which structures are meaningful at each resolution, and feature detectors convert stable local patterns into points or descriptors for matching.

## Recall in 30 seconds

- Image gradients provide edge direction and strength but amplify noise.
- Gaussian smoothing before differentiation creates a well-behaved scale space.
- Corners are repeatable where intensity changes in multiple directions; blobs represent characteristic scale.
- A detector chooses locations; a descriptor makes those locations comparable across images.

## Watch in order

> [!method] Why this sequence
> Watch in order: foundation first, then mechanism, then application or diagnostics where the topic needs it.

### 1. Canny Edge Detector | Edge Detection

> [!video] First Principles of Computer Vision · English · university course
> **Purpose:** Introduces image derivatives, gradient-based edge evidence, smoothing, non-maximum suppression, and thresholding.
> [Watch on YouTube](https://www.youtube.com/watch?v=hUC1uoigH6s)

### 2. Lecture 05 - Scale-invariant Feature Transform (SIFT)

> [!video] UCF CRCV · English · university course
> **Purpose:** Develops scale space, extrema detection, orientation assignment, local descriptors, and scale-invariant features.
> [Watch on YouTube](https://www.youtube.com/watch?v=NPcMS49V5hg)

> [!summary] After watching
> Close the videos and explain the recall bullets in your own words. Add only corrections or a worked example below—do not recreate the lecture.

## My correction or example

-
