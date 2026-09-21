---
generated_by: "build_obsidian_vault.py"
type: "curriculum-lesson"
aliases: ["Dataset Design, Long-Tail Metrics & Failure Analysis"]
day: 59
cycle: 20
domain: "Computer Vision"
stage: "Systems"
status: "planned"
source: ["curriculum_plan.json", "curriculum_resources.json"]
tags: ["curriculum", "computer-vision", "systems"]
cssclasses: ["research-note", "curriculum-note"]
related_concepts: ["Mind Map/Nodes/perception.md"]
related_papers: []
---

[[Home|Research Lab]]  /  [[Curriculum/Curriculum|Curriculum]]

# Day 59 — Dataset Design, Long-Tail Metrics & Failure Analysis

> [!curriculum] Computer Vision · Systems
> **Cycle 20** · **status: planned**
> Use the videos for first-pass learning; use this note for fast recall without rewatching.

> [!sequence] Learning sequence
> - [[Curriculum/Lessons/Day 58 - Data-Centric ML, Evaluation & Reproducibility|← Day 58]]
> - [[Curriculum/Curriculum|Curriculum map]]
> - [[Curriculum/Lessons/Day 60 - Robot Evaluation, Safety Cases & Reproducible Benchmarks|Day 60 →]]

> [!concepts] Knowledge-graph concepts
> - [[Mind Map/Nodes/perception|Perception]]

## Brief description

Vision datasets define the visual world a model can learn; long-tailed distributions, annotation policy, and scenario coverage require metrics and failure analysis that expose rare but consequential errors.

## Recall in 30 seconds

- Class counts alone do not capture variation in pose, context, geography, sensors, and difficulty.
- Macro, per-class, and worst-group metrics reveal failures hidden by aggregate accuracy.
- Detection and segmentation require matching and IoU conventions that can change conclusions.
- Turn error clusters into named failure modes with representative examples, likely causes, and a data-collection response.

## Watch in order

> [!method] Why this sequence
> Watch in order: foundation first, then mechanism, then application or diagnostics where the topic needs it.

### 1. CPSC 330 Lecture 3: data splitting

> [!video] Mike Gelbart · English · respected educator
> **Purpose:** Covers defensible dataset splitting and leakage prevention as core dataset-design requirements.
> [Watch on YouTube](https://www.youtube.com/watch?v=arrhrBjOPhY)

### 2. Shir Bar - Lecture 6 - Evaluation Metrics in Computer Vision for Ecology

> [!video] CV4Ecology · English · official conference
> **Purpose:** Provides computer-vision-specific metrics and demonstrates why evaluation must reflect task and data characteristics.
> [Watch on YouTube](https://www.youtube.com/watch?v=alO00a0cINg)

### 3. Deva Ramanan - Understanding Visual Appearances in the Long-tail

> [!video] UBC Computer Science · English · university course
> **Purpose:** Addresses rare categories, long-tailed appearance distributions, diagnostic slicing, and failures hidden by aggregate metrics.
> [Watch on YouTube](https://www.youtube.com/watch?v=YTHqXEI_vgs)

> [!summary] After watching
> Close the videos and explain the recall bullets in your own words. Add only corrections or a worked example below—do not recreate the lecture.

## My correction or example

-
