---
generated_by: "build_obsidian_vault.py"
type: "curriculum-lesson"
aliases: ["Open-Vocabulary Detection & Foundation Segmentation"]
day: 38
cycle: 13
domain: "Computer Vision"
stage: "Modern"
status: "planned"
source: ["curriculum_plan.json", "curriculum_resources.json"]
tags: ["curriculum", "computer-vision", "modern"]
cssclasses: ["research-note", "curriculum-note"]
related_concepts: ["Mind Map/Nodes/segmentation.md", "Mind Map/Nodes/foundation-lab.md", "Mind Map/Nodes/detection.md", "Mind Map/Nodes/perception.md"]
related_papers: []
---

[[Home|Research Lab]]  /  [[Curriculum/Curriculum|Curriculum]]

# Day 38 — Open-Vocabulary Detection & Foundation Segmentation

> [!curriculum] Computer Vision · Modern
> **Cycle 13** · **status: planned**
> Use the videos for first-pass learning; use this note for fast recall without rewatching.

> [!sequence] Learning sequence
> - [[Curriculum/Lessons/Day 37 - Graph Neural Networks & Geometric Deep Learning|← Day 37]]
> - [[Curriculum/Curriculum|Curriculum map]]
> - [[Curriculum/Lessons/Day 39 - Imitation Learning, DAgger & Inverse RL|Day 39 →]]

> [!concepts] Knowledge-graph concepts
> - [[Mind Map/Nodes/segmentation|Segmentation]]
> - [[Mind Map/Nodes/foundation-lab|Foundation]]
> - [[Mind Map/Nodes/detection|Detection]]
> - [[Mind Map/Nodes/perception|Perception]]

## Brief description

Open-vocabulary perception replaces a fixed class list with language-conditioned recognition, while foundation segmentation models use prompts to produce masks that transfer across categories and domains.

## Recall in 30 seconds

- Vision-language pretraining aligns image regions or features with text so class names can be supplied at inference.
- Open-vocabulary detection must localize and name objects beyond the detector's supervised category set.
- Promptable segmentation predicts masks from points, boxes, text, or prior masks but does not guarantee semantic correctness.
- Vocabulary bias, background confusion, calibration, and domain shift require explicit evaluation.

## Watch in order

> [!method] Why this sequence
> Watch in order: foundation first, then mechanism, then application or diagnostics where the topic needs it.

### 1. Lecture 11 | Detection and Segmentation

> [!video] Stanford University School of Engineering · English · university course
> **Purpose:** Establishes closed-set object detection and semantic/instance segmentation architectures and metrics.
> [Watch on YouTube](https://www.youtube.com/watch?v=nDPWywWRIRo)

### 2. Open-Vocabulary Visual Perception upon Frozen Vision and Language Models (Yin Cui, Google)

> [!video] Computer Vision in the Wild (CVinW) · English · university course
> **Purpose:** Extends detection and segmentation to open vocabularies using frozen vision-language foundation models.
> [Watch on YouTube](https://www.youtube.com/watch?v=LAesxhjebDA)

> [!summary] After watching
> Close the videos and explain the recall bullets in your own words. Add only corrections or a worked example below—do not recreate the lecture.

## My correction or example

-
