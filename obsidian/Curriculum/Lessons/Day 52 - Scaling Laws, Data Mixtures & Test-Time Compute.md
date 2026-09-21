---
generated_by: "build_obsidian_vault.py"
type: "curriculum-lesson"
aliases: ["Scaling Laws, Data Mixtures & Test-Time Compute"]
day: 52
cycle: 18
domain: "Machine Learning"
stage: "Frontier"
status: "planned"
source: ["curriculum_plan.json", "curriculum_resources.json"]
tags: ["curriculum", "machine-learning", "frontier"]
cssclasses: ["research-note", "curriculum-note"]
related_concepts: ["Mind Map/Nodes/systems.md", "Mind Map/Nodes/learning.md"]
related_papers: []
---

[[Home|Research Lab]]  /  [[Curriculum/Curriculum|Curriculum]]

# Day 52 — Scaling Laws, Data Mixtures & Test-Time Compute

> [!curriculum] Machine Learning · Frontier
> **Cycle 18** · **status: planned**
> Use the videos for first-pass learning; use this note for fast recall without rewatching.

> [!sequence] Learning sequence
> - [[Curriculum/Lessons/Day 51 - Diffusion Policy for Visuomotor Control|← Day 51]]
> - [[Curriculum/Curriculum|Curriculum map]]
> - [[Curriculum/Lessons/Day 53 - Vision-Language Models and Visual Reasoning|Day 53 →]]

> [!concepts] Knowledge-graph concepts
> - [[Mind Map/Nodes/systems|Systems]]
> - [[Mind Map/Nodes/learning|Learning]]

## Brief description

Scaling laws describe predictable trends with model, data, and compute; data mixtures choose which capabilities receive that compute, and test-time compute spends additional inference effort on search, sampling, or verification.

## Recall in 30 seconds

- Power-law trends summarize a regime; they do not guarantee extrapolation after architecture, data, or objective changes.
- Compute-optimal training balances model size and useful token or example count.
- Mixture weights change the learned task distribution and can dominate aggregate scaling gains.
- Test-time compute helps only when extra samples or reasoning can be selected by a reliable verifier or policy.

## Watch in order

> [!method] Why this sequence
> Watch in order: foundation first, then mechanism, then application or diagnostics where the topic needs it.

### 1. Jared Kaplan | Scaling Laws and Their Implications for Coding AI

> [!video] Harvard CMSA · English · official conference
> **Purpose:** Introduces empirical neural scaling laws and the relationships among model size, data, compute, and loss.
> [Watch on YouTube](https://www.youtube.com/watch?v=Suhp3OLASSo)

### 2. Danqi Chen: Data Selection for Pre-training and Instruction-tuning of LLMs

> [!video] KUIS AI · English · university course
> **Purpose:** Covers data selection and mixture quality for pretraining and instruction tuning, complementing compute-centric scaling laws.
> [Watch on YouTube](https://www.youtube.com/watch?v=SFuNEkGUziA)

### 3. Inference-time scaling and reasoning: Lecture 12 of NLPwDL 25/26

> [!video] Ivan Habernal · English · respected educator
> **Purpose:** Completes the lesson with inference-time scaling, reasoning-time compute, and the shift from train-time to test-time resource allocation.
> [Watch on YouTube](https://www.youtube.com/watch?v=ZbaFQjWB6Vo)

> [!summary] After watching
> Close the videos and explain the recall bullets in your own words. Add only corrections or a worked example below—do not recreate the lecture.

## My correction or example

-
