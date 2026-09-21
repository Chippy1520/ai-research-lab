---
generated_by: "build_obsidian_vault.py"
type: "curriculum-lesson"
aliases: ["CNN Backbones, FPN & Detection"]
day: 17
cycle: 6
domain: "Computer Vision"
stage: "Core"
status: "planned"
source: ["curriculum_plan.json", "curriculum_resources.json"]
tags: ["curriculum", "computer-vision", "core"]
cssclasses: ["research-note", "curriculum-note"]
related_concepts: ["Mind Map/Nodes/detection.md", "Mind Map/Nodes/cnn.md", "Mind Map/Nodes/perception.md"]
related_papers: []
---

[[Home|Research Lab]]  /  [[Curriculum/Curriculum|Curriculum]]

# Day 17 — CNN Backbones, FPN & Detection

> [!curriculum] Computer Vision · Core
> **Cycle 6** · **status: planned**
> Use the videos for first-pass learning; use this note for fast recall without rewatching.

> [!sequence] Learning sequence
> - [[Curriculum/Lessons/Day 16 - CNN Inductive Biases & Modern ConvNets|← Day 16]]
> - [[Curriculum/Curriculum|Curriculum map]]
> - [[Curriculum/Lessons/Day 18 - Policy Gradients and Variance Reduction|Day 18 →]]

> [!concepts] Knowledge-graph concepts
> - [[Mind Map/Nodes/detection|Detection]]
> - [[Mind Map/Nodes/cnn|CNNs]]
> - [[Mind Map/Nodes/perception|Perception]]

## Brief description

A detection system turns backbone features into localized object predictions; feature pyramids expose multiple resolutions so heads can handle objects at different scales.

## Recall in 30 seconds

- The backbone extracts visual features; the neck fuses scales; the head predicts classes and geometry.
- Feature pyramids combine semantically strong coarse features with spatially precise fine features.
- Anchor-based and anchor-free heads encode different candidate and assignment assumptions.
- NMS, class imbalance, localization loss, resolution, and evaluation IoU thresholds shape observed performance.

## Watch in order

> [!method] Why this sequence
> Watch in order: foundation first, then mechanism, then application or diagnostics where the topic needs it.

### 1. Lecture 9 | CNN Architectures

> [!video] Stanford University School of Engineering · English · university course
> **Purpose:** Establishes CNN feature hierarchies and the backbone architectures reused by detection systems.
> [Watch on YouTube](https://www.youtube.com/watch?v=DAOcjicFr1Y)

### 2. Lecture 11 | Detection and Segmentation

> [!video] Stanford University School of Engineering · English · university course
> **Purpose:** Covers localization and object-detection pipelines, region proposals, classification/regression heads, and detector design.
> [Watch on YouTube](https://www.youtube.com/watch?v=nDPWywWRIRo)

### 3. Feature Pyramid Networks | Lecture 37 (Part 1) | Applied Deep Learning

> [!video] Maziar Raissi · English · respected educator
> **Purpose:** Adds the explicit FPN construction: top-down pathways, lateral connections, and multi-scale detection features.
> [Watch on YouTube](https://www.youtube.com/watch?v=6fXBXNjd1JQ)

> [!summary] After watching
> Close the videos and explain the recall bullets in your own words. Add only corrections or a worked example below—do not recreate the lecture.

## My correction or example

-
