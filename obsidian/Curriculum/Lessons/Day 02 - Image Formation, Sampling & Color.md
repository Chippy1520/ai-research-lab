---
generated_by: "build_obsidian_vault.py"
type: "curriculum-lesson"
aliases: ["Image Formation, Sampling & Color"]
day: 2
cycle: 1
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

# Day 02 — Image Formation, Sampling & Color

> [!curriculum] Computer Vision · Foundations
> **Cycle 1** · **status: planned**
> Use the videos for first-pass learning; use this note for fast recall without rewatching.

> [!sequence] Learning sequence
> - [[Curriculum/Lessons/Day 01 - Optimization Dynamics & AdamW|← Day 01]]
> - [[Curriculum/Curriculum|Curriculum map]]
> - [[Curriculum/Lessons/Day 03 - MDPs, Returns & Occupancy Measures|Day 03 →]]

> [!concepts] Knowledge-graph concepts
> - [[Mind Map/Nodes/perception|Perception]]

## Brief description

Image formation maps light from a three-dimensional scene through optics and a sensor into sampled, quantized color measurements; every later vision method inherits the ambiguities introduced here.

## Recall in 30 seconds

- Projection, illumination, surface reflectance, lens effects, and sensor response jointly create a pixel value.
- Sampling below the scene's spatial bandwidth causes aliasing; prefilter before downsampling.
- Color channels are device-dependent measurements, not intrinsic object properties.
- Exposure and dynamic range trade signal-to-noise against clipping and motion blur.

## Watch in order

> [!method] Why this sequence
> Watch in order: foundation first, then mechanism, then application or diagnostics where the topic needs it.

### 1. Pinhole and Perspective Projection | Image Formation

> [!video] First Principles of Computer Vision · English · university course
> **Purpose:** Introduces geometric image formation through the pinhole camera and perspective projection.
> [Watch on YouTube](https://www.youtube.com/watch?v=_EhY31MSbNM)

### 2. Sampling Theory and Aliasing | Image Processing II

> [!video] First Principles of Computer Vision · English · university course
> **Purpose:** Covers discrete image sampling, sampling limits, reconstruction, and spatial aliasing.
> [Watch on YouTube](https://www.youtube.com/watch?v=YFZsxY_2_l4)

### 3. Sensing Color | Image Sensing

> [!video] First Principles of Computer Vision · English · university course
> **Purpose:** Completes the lesson with wavelength-sensitive sensing, color channels, and practical color-image acquisition.
> [Watch on YouTube](https://www.youtube.com/watch?v=V4y3K6zoUQs)

> [!summary] After watching
> Close the videos and explain the recall bullets in your own words. Add only corrections or a worked example below—do not recreate the lecture.

## My correction or example

-
