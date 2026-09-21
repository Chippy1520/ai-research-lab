---
generated_by: "build_obsidian_vault.py"
type: "curriculum-lesson"
aliases: ["Video Motion: Optical Flow, Tracking & Temporal Models"]
day: 35
cycle: 12
domain: "Computer Vision"
stage: "Modern"
status: "planned"
source: ["curriculum_plan.json", "curriculum_resources.json"]
tags: ["curriculum", "computer-vision", "modern"]
cssclasses: ["research-note", "curriculum-note"]
related_concepts: ["Mind Map/Nodes/optical-flow.md", "Mind Map/Nodes/perception.md"]
related_papers: []
---

[[Home|Research Lab]]  /  [[Curriculum/Curriculum|Curriculum]]

# Day 35 — Video Motion: Optical Flow, Tracking & Temporal Models

> [!curriculum] Computer Vision · Modern
> **Cycle 12** · **status: planned**
> Use the videos for first-pass learning; use this note for fast recall without rewatching.

> [!sequence] Learning sequence
> - [[Curriculum/Lessons/Day 34 - Sequence Models- RNNs, S4 & Mamba|← Day 34]]
> - [[Curriculum/Curriculum|Curriculum map]]
> - [[Curriculum/Lessons/Day 36 - Offline RL, Behavior Regularization & Dataset Shift|Day 36 →]]

> [!concepts] Knowledge-graph concepts
> - [[Mind Map/Nodes/optical-flow|Optical flow]]
> - [[Mind Map/Nodes/perception|Perception]]

## Brief description

Video motion methods estimate how image content moves, associate entities across frames, and model temporal context; optical flow, tracking, and learned temporal features solve related but distinct correspondence problems.

## Recall in 30 seconds

- Optical flow is a dense apparent-motion field, not necessarily physical 3D motion.
- Brightness constancy and local smoothness make flow estimable but fail under occlusion, lighting changes, and large displacement.
- Tracking maintains identity through time and must handle disappearance, re-entry, and ambiguity.
- Temporal models need evaluation on motion, identity, causality, and long-range consistency rather than frame accuracy alone.

## Watch in order

> [!method] Why this sequence
> Watch in order: foundation first, then mechanism, then application or diagnostics where the topic needs it.

### 1. Lecture 06 - Optical Flow

> [!video] UCF CRCV · English · university course
> **Purpose:** Covers motion fields, brightness constancy, classical optical-flow constraints, and estimation.
> [Watch on YouTube](https://www.youtube.com/watch?v=5VyLAH8BhF8)

### 2. CV3DST - Object tracking

> [!video] Dynamic Vision and Learning Group · English · university course
> **Purpose:** Moves from frame-to-frame motion to object tracking and temporal state estimation.
> [Watch on YouTube](https://www.youtube.com/watch?v=QtAYgtBnhws)

### 3. Rui Hou - Action Recognition, Temporal Localization and Detection in Trimmed and Untrimmed Videos

> [!video] UCF CRCV · English · university course
> **Purpose:** Completes the progression with learned temporal representations for video understanding, action recognition, and temporal localization.
> [Watch on YouTube](https://www.youtube.com/watch?v=HpyQV1Ux5NI)

> [!summary] After watching
> Close the videos and explain the recall bullets in your own words. Add only corrections or a worked example below—do not recreate the lecture.

## My correction or example

-
