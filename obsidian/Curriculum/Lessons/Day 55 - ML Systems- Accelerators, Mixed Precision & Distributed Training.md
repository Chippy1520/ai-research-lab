---
generated_by: "build_obsidian_vault.py"
type: "curriculum-lesson"
aliases: ["ML Systems: Accelerators, Mixed Precision & Distributed Training"]
day: 55
cycle: 19
domain: "Machine Learning"
stage: "Systems"
status: "planned"
source: ["curriculum_plan.json", "curriculum_resources.json"]
tags: ["curriculum", "machine-learning", "systems"]
cssclasses: ["research-note", "curriculum-note"]
related_concepts: ["Mind Map/Nodes/systems.md", "Mind Map/Nodes/learning.md"]
related_papers: []
---

[[Home|Research Lab]]  /  [[Curriculum/Curriculum|Curriculum]]

# Day 55 — ML Systems: Accelerators, Mixed Precision & Distributed Training

> [!curriculum] Machine Learning · Systems
> **Cycle 19** · **status: planned**
> Use the videos for first-pass learning; use this note for fast recall without rewatching.

> [!sequence] Learning sequence
> - [[Curriculum/Lessons/Day 54 - Sim-to-Real, System Identification & Domain Randomization|← Day 54]]
> - [[Curriculum/Curriculum|Curriculum map]]
> - [[Curriculum/Lessons/Day 56 - Efficient Vision- Quantization, Distillation & Edge Deployment|Day 56 →]]

> [!concepts] Knowledge-graph concepts
> - [[Mind Map/Nodes/systems|Systems]]
> - [[Mind Map/Nodes/learning|Learning]]

## Brief description

ML systems turn tensor programs into efficient distributed execution; accelerators exploit parallel arithmetic, mixed precision reduces memory and bandwidth, and distributed strategies partition data, model state, or pipeline work.

## Recall in 30 seconds

- Throughput is constrained by compute, memory capacity, memory bandwidth, communication, and input pipelines.
- Mixed precision keeps selected operations or master states at higher precision to prevent overflow and underflow.
- Data parallelism replicates model state; tensor, pipeline, and sharded methods divide it in different ways.
- Scaling efficiency must include synchronization, stragglers, failures, reproducibility, and total cost—not only device utilization.

## Watch in order

> [!method] Why this sequence
> Watch in order: foundation first, then mechanism, then application or diagnostics where the topic needs it.

### 1. Lecture 15 | Efficient Methods and Hardware for Deep Learning

> [!video] Stanford University School of Engineering · English · university course
> **Purpose:** Covers efficient computation, memory movement, model compression, and accelerator architecture.
> [Watch on YouTube](https://www.youtube.com/watch?v=eZdOkDtYMoo)

### 2. NVAITC Webinar: Automatic Mixed Precision Training in PyTorch

> [!video] NVIDIA Developer · English · research lab
> **Purpose:** Explains reduced-precision arithmetic, loss scaling, numerical stability, and practical mixed-precision training.
> [Watch on YouTube](https://www.youtube.com/watch?v=b5dAmcBKxHg)

### 3. Distributed Deep Learning

> [!video] Argonne Leadership Computing Facility · English · professional foundation
> **Purpose:** Completes the systems view with distributed training, parallel execution, communication, and large-compute infrastructure.
> [Watch on YouTube](https://www.youtube.com/watch?v=GGR7CzIHt14)

> [!summary] After watching
> Close the videos and explain the recall bullets in your own words. Add only corrections or a worked example below—do not recreate the lecture.

## My correction or example

-
