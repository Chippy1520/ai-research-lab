---
generated_by: "build_obsidian_vault.py"
type: "curriculum-lesson"
aliases: ["Semantic, Instance & Panoptic Segmentation"]
day: 20
cycle: 7
domain: "Computer Vision"
stage: "Core"
status: "planned"
source: ["curriculum_plan.json", "curriculum_resources.json"]
tags: ["curriculum", "computer-vision", "core"]
cssclasses: ["research-note", "curriculum-note"]
related_concepts: ["Mind Map/Nodes/segmentation.md", "Mind Map/Nodes/perception.md"]
related_papers: []
---

[[Home|Research Lab]]  /  [[Curriculum/Curriculum|Curriculum]]

# Day 20 — Semantic, Instance & Panoptic Segmentation

> [!curriculum] Computer Vision · Core
> **Cycle 7** · **status: planned**
> Use the videos for first-pass learning; use this note for fast recall without rewatching.

> [!sequence] Learning sequence
> - [[Curriculum/Lessons/Day 19 - Variational Inference, ELBO & VAEs|← Day 19]]
> - [[Curriculum/Curriculum|Curriculum map]]
> - [[Curriculum/Lessons/Day 21 - Actor-Critic Methods & Generalized Advantage Estimation|Day 21 →]]

> [!concepts] Knowledge-graph concepts
> - [[Mind Map/Nodes/segmentation|Segmentation]]
> - [[Mind Map/Nodes/perception|Perception]]

## Brief description

Semantic segmentation labels categories per pixel, instance segmentation separates individual objects, and panoptic segmentation unifies countable things with amorphous stuff in one scene representation.

## Recall in 30 seconds

- Semantic masks do not distinguish two objects of the same class; instance masks do.
- Panoptic output assigns every pixel a semantic label and, for things, an instance identity.
- Decoder resolution, multi-scale context, boundary quality, and label taxonomy determine useful output.
- IoU variants measure different failure modes; class imbalance and small objects need explicit attention.

## Watch in order

> [!method] Why this sequence
> Watch in order: foundation first, then mechanism, then application or diagnostics where the topic needs it.

### 1. Lecture 11 | Detection and Segmentation

> [!video] Stanford University School of Engineering · English · university course
> **Purpose:** Introduces dense semantic labeling and the relationship between detection and instance-aware segmentation.
> [Watch on YouTube](https://www.youtube.com/watch?v=nDPWywWRIRo)

### 2. CV3DST - Instance and panoptic segmentation

> [!video] Dynamic Vision and Learning Group · English · university course
> **Purpose:** Develops instance segmentation and then unifies semantic and instance outputs through panoptic segmentation and its evaluation.
> [Watch on YouTube](https://www.youtube.com/watch?v=LMZI8DDyltQ)

> [!summary] After watching
> Close the videos and explain the recall bullets in your own words. Add only corrections or a worked example below—do not recreate the lecture.

## My correction or example

-
