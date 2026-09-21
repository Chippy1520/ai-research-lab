---
generated_by: "build_obsidian_vault.py"
type: "curriculum-lesson"
aliases: ["Efficient Vision: Quantization, Distillation & Edge Deployment"]
day: 56
cycle: 19
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

# Day 56 — Efficient Vision: Quantization, Distillation & Edge Deployment

> [!curriculum] Computer Vision · Systems
> **Cycle 19** · **status: planned**
> Use the videos for first-pass learning; use this note for fast recall without rewatching.

> [!sequence] Learning sequence
> - [[Curriculum/Lessons/Day 55 - ML Systems- Accelerators, Mixed Precision & Distributed Training|← Day 55]]
> - [[Curriculum/Curriculum|Curriculum map]]
> - [[Curriculum/Lessons/Day 57 - ROS 2, Real-Time Robot Software & Hardware Interfaces|Day 57 →]]

> [!concepts] Knowledge-graph concepts
> - [[Mind Map/Nodes/perception|Perception]]

## Brief description

Efficient vision compresses computation and memory through quantization, distillation, pruning, and architecture design, then measures the resulting model on the actual edge runtime rather than proxy FLOPs alone.

## Recall in 30 seconds

- Quantization maps values to fewer levels; calibration or quantization-aware training controls the induced error.
- Distillation trains a smaller student to match a teacher's outputs or intermediate behavior.
- Latency depends on operator support, memory movement, batch size, and hardware—not just parameter count.
- Evaluate accuracy, tail latency, energy, memory, thermal behavior, and robustness after conversion.

## Watch in order

> [!method] Why this sequence
> Watch in order: foundation first, then mechanism, then application or diagnostics where the topic needs it.

### 1. Lec 30 | Quantization, Pruning & Distillation

> [!video] NPTEL IIT Delhi · English · professional foundation
> **Purpose:** Provides the algorithmic foundation for quantization and knowledge distillation, with pruning as useful adjacent context.
> [Watch on YouTube](https://www.youtube.com/watch?v=Kx5x3HYBDls)

### 2. Machine Learning on the Edge - From Microcontrollers to Embedded Linux Devices

> [!video] Toronto Machine Learning Series (TMLS) · English · official conference
> **Purpose:** Covers deployment constraints and implementation choices across microcontrollers and embedded Linux edge devices.
> [Watch on YouTube](https://www.youtube.com/watch?v=KpwXcVk4hZY)

> [!summary] After watching
> Close the videos and explain the recall bullets in your own words. Add only corrections or a worked example below—do not recreate the lecture.

## My correction or example

-
