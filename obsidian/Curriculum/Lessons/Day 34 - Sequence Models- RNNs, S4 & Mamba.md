---
generated_by: "build_obsidian_vault.py"
type: "curriculum-lesson"
aliases: ["Sequence Models: RNNs, S4 & Mamba"]
day: 34
cycle: 12
domain: "Machine Learning"
stage: "Modern"
status: "planned"
source: ["curriculum_plan.json", "curriculum_resources.json"]
tags: ["curriculum", "machine-learning", "modern"]
cssclasses: ["research-note", "curriculum-note"]
related_concepts: ["Mind Map/Nodes/seq-models.md", "Mind Map/Nodes/systems.md", "Mind Map/Nodes/learning.md"]
related_papers: []
---

[[Home|Research Lab]]  /  [[Curriculum/Curriculum|Curriculum]]

# Day 34 — Sequence Models: RNNs, S4 & Mamba

> [!curriculum] Machine Learning · Modern
> **Cycle 12** · **status: planned**
> Use the videos for first-pass learning; use this note for fast recall without rewatching.

> [!sequence] Learning sequence
> - [[Curriculum/Lessons/Day 33 - POMDPs, Belief State & Recurrent Policies|← Day 33]]
> - [[Curriculum/Curriculum|Curriculum map]]
> - [[Curriculum/Lessons/Day 35 - Video Motion- Optical Flow, Tracking & Temporal Models|Day 35 →]]

> [!concepts] Knowledge-graph concepts
> - [[Mind Map/Nodes/seq-models|Sequence models]]
> - [[Mind Map/Nodes/systems|Systems]]
> - [[Mind Map/Nodes/learning|Learning]]

## Brief description

Sequence models compress and propagate context through recurrent state, structured state spaces, or selective state updates; RNNs, S4, and Mamba differ mainly in how they preserve long-range information and parallelize computation.

## Recall in 30 seconds

- RNNs update a hidden state sequentially and struggle with long gradients and limited parallelism.
- Structured state-space models turn linear dynamical systems into long convolutions that can be trained in parallel.
- Mamba makes state updates input-dependent, selectively remembering or discarding tokens.
- Long-context benchmarks must distinguish true memory and retrieval from local pattern matching.

## Watch in order

> [!method] Why this sequence
> Watch in order: foundation first, then mechanism, then application or diagnostics where the topic needs it. Coverage boundary: The talk emphasizes structured state-space models; Mamba-specific hardware-aware scan implementation receives less detail than the mathematical lineage.

### 1. MedAI #41: Efficiently Modeling Long Sequences with Structured State Spaces | Albert Gu

> [!video] Stanford MedAI · English · university course
> **Purpose:** Albert Gu presents the recurrence/state-space foundation, structured state-space models such as S4, and the line of work leading to selective sequence models.
> [Watch on YouTube](https://www.youtube.com/watch?v=luCBXCErkCs)

> [!summary] After watching
> Close the videos and explain the recall bullets in your own words. Add only corrections or a worked example below—do not recreate the lecture.

## My correction or example

-
