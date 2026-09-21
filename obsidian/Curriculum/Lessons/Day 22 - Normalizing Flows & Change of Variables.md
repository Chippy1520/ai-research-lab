---
generated_by: "build_obsidian_vault.py"
type: "curriculum-lesson"
aliases: ["Normalizing Flows & Change of Variables"]
day: 22
cycle: 8
domain: "Machine Learning"
stage: "Core"
status: "planned"
source: ["curriculum_plan.json", "curriculum_resources.json"]
tags: ["curriculum", "machine-learning", "core"]
cssclasses: ["research-note", "curriculum-note"]
related_concepts: ["Mind Map/Nodes/systems.md", "Mind Map/Nodes/learning.md"]
related_papers: []
---

[[Home|Research Lab]]  /  [[Curriculum/Curriculum|Curriculum]]

# Day 22 — Normalizing Flows & Change of Variables

> [!curriculum] Machine Learning · Core
> **Cycle 8** · **status: planned**
> Use the videos for first-pass learning; use this note for fast recall without rewatching.

> [!sequence] Learning sequence
> - [[Curriculum/Lessons/Day 21 - Actor-Critic Methods & Generalized Advantage Estimation|← Day 21]]
> - [[Curriculum/Curriculum|Curriculum map]]
> - [[Curriculum/Lessons/Day 23 - Vision Transformers & Patch Geometry|Day 23 →]]

> [!concepts] Knowledge-graph concepts
> - [[Mind Map/Nodes/systems|Systems]]
> - [[Mind Map/Nodes/learning|Learning]]

## Brief description

A normalizing flow builds a flexible density by composing invertible transformations whose Jacobian determinants are tractable, enabling exact likelihood and reversible sampling.

## Recall in 30 seconds

- Change of variables adjusts density by the absolute determinant of the transformation's Jacobian.
- Composition gives expressive mappings while log-determinants add across layers.
- Invertibility and cheap determinants constrain architecture design.
- High likelihood does not guarantee perceptual quality or reliable out-of-distribution detection.

## Watch in order

> [!method] Why this sequence
> Watch in order: foundation first, then mechanism, then application or diagnostics where the topic needs it.

### 1. Cornell CS 6785: Deep Generative Models. Lecture 7: Normalizing Flows

> [!video] Volodymyr Kuleshov · English · university course
> **Purpose:** Derives change-of-variables density evaluation and develops invertible transformations, Jacobian determinants, coupling layers, and flow architectures.
> [Watch on YouTube](https://www.youtube.com/watch?v=3IqRV40LKPs)

> [!summary] After watching
> Close the videos and explain the recall bullets in your own words. Add only corrections or a worked example below—do not recreate the lecture.

## My correction or example

-
