---
generated_by: "build_obsidian_vault.py"
type: "curriculum-lesson"
aliases: ["Optimization Dynamics & AdamW"]
day: 1
cycle: 1
domain: "Machine Learning"
stage: "Foundations"
status: "ready"
source: ["curriculum_plan.json", "curriculum_resources.json"]
tags: ["curriculum", "machine-learning", "foundations"]
cssclasses: ["research-note", "curriculum-note"]
related_concepts: ["Mind Map/Nodes/systems.md", "Mind Map/Nodes/learning.md"]
related_papers: []
---

[[Home|Research Lab]]  /  [[Curriculum/Curriculum|Curriculum]]

# Day 01 — Optimization Dynamics & AdamW

> [!curriculum] Machine Learning · Foundations
> **Cycle 1** · **status: ready**
> Use the videos for first-pass learning; use this note for fast recall without rewatching.

> [!sequence] Learning sequence
> - [[Curriculum/Curriculum|Curriculum map]]
> - [[Curriculum/Lessons/Day 02 - Image Formation, Sampling & Color|Day 02 →]]

> [!concepts] Knowledge-graph concepts
> - [[Mind Map/Nodes/systems|Systems]]
> - [[Mind Map/Nodes/learning|Learning]]

## Learning record

| Status | Confidence | Minutes | Revisit |
|---|---|---|---|
| ready | Not recorded | Not recorded | No |

> [!current] Current due lesson
> Watch the sequence once, then test whether the recall summary is enough to reconstruct the concept.

## Brief description

Optimization is the dynamics of how parameters move under noisy gradients; AdamW combines momentum and coordinate-wise scaling while keeping weight decay separate from the gradient update.

## Recall in 30 seconds

- Momentum smooths persistent gradient directions; the second-moment estimate reduces steps along coordinates with repeatedly large gradients.
- Bias correction matters early because both moving averages start at zero.
- AdamW decouples parameter shrinkage from adaptive preconditioning, unlike adding an L2 term inside Adam.
- Warm-up, clipping, schedules, and parameter-group choices still determine stability.

## Watch in order

> [!method] Why this sequence
> Watch in order: foundation first, then mechanism, then application or diagnostics where the topic needs it.

### 1. CS231n Winter 2016: Lecture 3: Linear Classification 2, Optimization

> [!video] Andrej Karpathy · English · respected educator
> **Purpose:** Builds the optimization foundation: loss landscapes, gradient-based learning, SGD dynamics, conditioning, and optimizer behavior.
> [Watch on YouTube](https://www.youtube.com/watch?v=qlLChbHhbg4)

### 2. The Algorithm that Helps Machines Learn [AdamW]

> [!video] Jia-Bin Huang · English · respected educator
> **Purpose:** Adds AdamW specifically, emphasizing decoupled weight decay and why it differs from putting an L2 penalty inside Adam.
> [Watch on YouTube](https://www.youtube.com/watch?v=1_nujVNUsto)

> [!summary] After watching
> Close the videos and explain the recall bullets in your own words. Add only corrections or a worked example below—do not recreate the lecture.

## My correction or example

-
