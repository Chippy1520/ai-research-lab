---
generated_by: "build_obsidian_vault.py"
type: "curriculum-lesson"
aliases: ["Vision Transformers & Patch Geometry"]
day: 23
cycle: 8
domain: "Computer Vision"
stage: "Core"
status: "planned"
source: ["curriculum_plan.json", "curriculum_resources.json"]
tags: ["curriculum", "computer-vision", "core"]
cssclasses: ["research-note", "curriculum-note"]
related_concepts: ["Mind Map/Nodes/transformers.md", "Mind Map/Nodes/perception.md"]
related_papers: ["Papers/STLight.md"]
---

[[Home|Research Lab]]  /  [[Curriculum/Curriculum|Curriculum]]

# Day 23 — Vision Transformers & Patch Geometry

> [!curriculum] Computer Vision · Core
> **Cycle 8** · **status: planned**
> Use the videos for first-pass learning; use this note for fast recall without rewatching.

> [!sequence] Learning sequence
> - [[Curriculum/Lessons/Day 22 - Normalizing Flows & Change of Variables|← Day 22]]
> - [[Curriculum/Curriculum|Curriculum map]]
> - [[Curriculum/Lessons/Day 24 - PPO- Clipping, Trust Regions & Diagnostics|Day 24 →]]

> [!concepts] Knowledge-graph concepts
> - [[Mind Map/Nodes/transformers|Transformers]]
> - [[Mind Map/Nodes/perception|Perception]]

> [!study] Paper companions
> - [[Papers/STLight|STLight]]

## Brief description

Vision Transformers split images into patch tokens and model their interactions with self-attention; patch size, positional information, and hierarchical design determine the balance between global context, detail, and compute.

## Recall in 30 seconds

- Patch projection converts fixed image regions into a token sequence; smaller patches preserve detail but increase attention cost.
- Self-attention mixes information globally, while position encodings prevent the sequence from becoming orderless.
- ViTs have weaker built-in locality than CNNs and therefore depend strongly on data and training regularization.
- Resolution changes alter token geometry, so positional interpolation and memory scaling matter at deployment.

## Watch in order

> [!method] Why this sequence
> Watch in order: foundation first, then mechanism, then application or diagnostics where the topic needs it. Coverage boundary: A single focused research lecture covers the core ViT and patch geometry; hierarchical and shifted-window variants are not treated in depth.

### 1. Vision Transformer Basics

> [!video] Samuel Albanie · English · respected educator
> **Purpose:** Explains image-to-patch tokenization, patch embeddings, positional information, self-attention, class tokens, and the geometric consequences of treating images as token grids.
> [Watch on YouTube](https://www.youtube.com/watch?v=vsqKGZT8Qn8)

> [!summary] After watching
> Close the videos and explain the recall bullets in your own words. Add only corrections or a worked example below—do not recreate the lecture.

## My correction or example

-
