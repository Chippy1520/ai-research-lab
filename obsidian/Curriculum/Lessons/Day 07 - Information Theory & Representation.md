---
generated_by: "build_obsidian_vault.py"
type: "curriculum-lesson"
aliases: ["Information Theory & Representation"]
day: 7
cycle: 3
domain: "Machine Learning"
stage: "Foundations"
status: "planned"
source: ["curriculum_plan.json", "curriculum_resources.json"]
tags: ["curriculum", "machine-learning", "foundations"]
cssclasses: ["research-note", "curriculum-note"]
related_concepts: ["Mind Map/Nodes/representation.md", "Mind Map/Nodes/systems.md", "Mind Map/Nodes/learning.md"]
related_papers: ["Papers/I-JEPA.md", "Papers/JEPA.md", "Papers/V-JEPA.md", "Papers/V-JEPA 2.md"]
---

[[Home|Research Lab]]  /  [[Curriculum/Curriculum|Curriculum]]

# Day 07 — Information Theory & Representation

> [!curriculum] Machine Learning · Foundations
> **Cycle 3** · **status: planned**
> Use the videos for first-pass learning; use this note for fast recall without rewatching.

> [!sequence] Learning sequence
> - [[Curriculum/Lessons/Day 06 - Bellman Operators & Contraction Proofs|← Day 06]]
> - [[Curriculum/Curriculum|Curriculum map]]
> - [[Curriculum/Lessons/Day 08 - Spatial Derivatives, Scale Space & Features|Day 08 →]]

> [!concepts] Knowledge-graph concepts
> - [[Mind Map/Nodes/representation|Self-supervised representation]]
> - [[Mind Map/Nodes/systems|Systems]]
> - [[Mind Map/Nodes/learning|Learning]]

> [!study] Paper companions
> - [[Papers/I-JEPA|I-JEPA]]
> - [[Papers/JEPA|JEPA]]
> - [[Papers/V-JEPA|V-JEPA]]
> - [[Papers/V-JEPA 2|V-JEPA 2]]

## Brief description

Information theory quantifies uncertainty and distinguishability, giving representation learning a language for deciding what information to preserve, discard, compress, or make predictive.

## Recall in 30 seconds

- Entropy measures uncertainty; cross-entropy scores a predictive distribution against observed outcomes.
- KL divergence is asymmetric and measures excess coding or distribution mismatch, not geometric distance.
- Mutual information is the reduction in uncertainty about one variable after observing another.
- A useful representation preserves task-relevant structure while suppressing nuisance variation; maximizing information blindly is not enough.

## Watch in order

> [!method] Why this sequence
> Watch in order: foundation first, then mechanism, then application or diagnostics where the topic needs it.

### 1. Introduction to Information Theory (Lecture 1) by Jaikumar Radhakrishnan

> [!video] International Centre for Theoretical Sciences · English · official conference
> **Purpose:** Introduces entropy, information, coding, and the probabilistic foundations of information theory.
> [Watch on YouTube](https://www.youtube.com/watch?v=z6J-PTcJNa4)

### 2. Deep Representation Learning - Yoshua Bengio (MILA, Canada)

> [!video] Center for Language & Speech Processing(CLSP), JHU · English · university course
> **Purpose:** Connects information-processing ideas to learned representations, distributed features, abstraction, and deep architectures.
> [Watch on YouTube](https://www.youtube.com/watch?v=-BjJMs8DS-8)

> [!summary] After watching
> Close the videos and explain the recall bullets in your own words. Add only corrections or a worked example below—do not recreate the lecture.

## My correction or example

-
