---
generated_by: "build_obsidian_vault.py"
type: "curriculum-lesson"
aliases: ["Adversarial Robustness, OOD Detection & Model Editing"]
day: 62
cycle: 21
domain: "Computer Vision"
stage: "Frontier"
status: "planned"
source: ["curriculum_plan.json", "curriculum_resources.json"]
tags: ["curriculum", "computer-vision", "frontier"]
cssclasses: ["research-note", "curriculum-note"]
related_concepts: ["Mind Map/Nodes/detection.md", "Mind Map/Nodes/perception.md"]
related_papers: []
---

[[Home|Research Lab]]  /  [[Curriculum/Curriculum|Curriculum]]

# Day 62 — Adversarial Robustness, OOD Detection & Model Editing

> [!curriculum] Computer Vision · Frontier
> **Cycle 21** · **status: planned**
> Use the videos for first-pass learning; use this note for fast recall without rewatching.

> [!sequence] Learning sequence
> - [[Curriculum/Lessons/Day 61 - Interpretability, Mechanistic Analysis & Alignment|← Day 61]]
> - [[Curriculum/Curriculum|Curriculum map]]
> - [[Curriculum/Lessons/Day 63 - Safe RL, Constraints, Shielding & Human Oversight|Day 63 →]]

> [!concepts] Knowledge-graph concepts
> - [[Mind Map/Nodes/detection|Detection]]
> - [[Mind Map/Nodes/perception|Perception]]

## Brief description

Adversarial robustness studies worst-case input sensitivity, OOD detection flags unfamiliar data, and model editing changes selected knowledge or behavior; all three require testing side effects beyond the targeted examples.

## Recall in 30 seconds

- Adversarial examples exploit local decision geometry under a defined threat model.
- OOD scores are meaningful only relative to specified in- and out-distributions.
- Robust accuracy must be measured with strong adaptive attacks, not a single weak perturbation.
- An edit should be specific, generalize to paraphrases, persist appropriately, and avoid damaging unrelated behavior.

## Watch in order

> [!method] Why this sequence
> Watch in order: foundation first, then mechanism, then application or diagnostics where the topic needs it.

### 1. On the Adversarial Robustness of Deep Learning

> [!video] Microsoft Research · English · research lab
> **Purpose:** Covers adversarial examples, threat models, attacks, defenses, and the limits of empirical robustness.
> [Watch on YouTube](https://www.youtube.com/watch?v=YgYiECAr9Gs)

### 2. [ICCV 2023 Tutorial] Sharon Yixuan Li: Out-of-Distribution detection

> [!video] Andrei Bursuc · English · official conference
> **Purpose:** Introduces OOD detection, uncertainty scores, evaluation protocols, and open-world deployment concerns.
> [Watch on YouTube](https://www.youtube.com/watch?v=hgLC9_9ZCJI)

### 3. David Bau: Interpretability and model editing

> [!video] UC Berkeley EECS · English · university course
> **Purpose:** Explains causal localization and direct editing of model knowledge or behavior, including evaluation of edit specificity.
> [Watch on YouTube](https://www.youtube.com/watch?v=8QPVKpzyZdY)

> [!summary] After watching
> Close the videos and explain the recall bullets in your own words. Add only corrections or a worked example below—do not recreate the lecture.

## My correction or example

-
