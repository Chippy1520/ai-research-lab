---
generated_by: "build_obsidian_vault.py"
type: "curriculum-lesson"
aliases: ["Domain Adaptation, Test-Time Adaptation & Robustness"]
day: 50
cycle: 17
domain: "Computer Vision"
stage: "Frontier"
status: "planned"
source: ["curriculum_plan.json", "curriculum_resources.json"]
tags: ["curriculum", "computer-vision", "frontier"]
cssclasses: ["research-note", "curriculum-note"]
related_concepts: ["Mind Map/Nodes/perception.md"]
related_papers: []
---

[[Home|Research Lab]]  /  [[Curriculum/Curriculum|Curriculum]]

# Day 50 — Domain Adaptation, Test-Time Adaptation & Robustness

> [!curriculum] Computer Vision · Frontier
> **Cycle 17** · **status: planned**
> Use the videos for first-pass learning; use this note for fast recall without rewatching.

> [!sequence] Learning sequence
> - [[Curriculum/Lessons/Day 49 - Meta-Learning, Continual Learning & Adaptation|← Day 49]]
> - [[Curriculum/Curriculum|Curriculum map]]
> - [[Curriculum/Lessons/Day 51 - Diffusion Policy for Visuomotor Control|Day 51 →]]

> [!concepts] Knowledge-graph concepts
> - [[Mind Map/Nodes/perception|Perception]]

## Brief description

Domain adaptation transfers a model across different train and test distributions, test-time adaptation updates it using unlabeled deployment data, and robustness asks which changes the system should withstand without unsafe degradation.

## Recall in 30 seconds

- Covariate, label, and concept shift require different assumptions and corrections.
- Feature alignment can erase class information or align the wrong modes if labels and supports differ.
- Test-time adaptation must avoid leakage, collapse, and irreversible updates under nonstationary streams.
- Report source performance, target performance, calibration, and failure detection—not only average target accuracy.

## Watch in order

> [!method] Why this sequence
> Watch in order: foundation first, then mechanism, then application or diagnostics where the topic needs it.

### 1. [ML 2021 (English version)] Lecture 27: Domain Adaptation

> [!video] Hung-yi Lee · English · respected educator
> **Purpose:** Builds the domain-shift problem and principal supervised and unsupervised domain-adaptation approaches.
> [Watch on YouTube](https://www.youtube.com/watch?v=8AKqH6V9kjE)

### 2. Test-Time Adaptation: Next Steps for Robust Visual Recognition

> [!video] Ai2 · English · research lab
> **Purpose:** Extends adaptation to deployment-time distribution shifts and discusses robustness objectives, assumptions, and failure modes.
> [Watch on YouTube](https://www.youtube.com/watch?v=EyyMSjxbvII)

> [!summary] After watching
> Close the videos and explain the recall bullets in your own words. Add only corrections or a worked example below—do not recreate the lecture.

## My correction or example

-
