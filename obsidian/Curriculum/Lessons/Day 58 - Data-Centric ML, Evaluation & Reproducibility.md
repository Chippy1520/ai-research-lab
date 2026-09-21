---
generated_by: "build_obsidian_vault.py"
type: "curriculum-lesson"
aliases: ["Data-Centric ML, Evaluation & Reproducibility"]
day: 58
cycle: 20
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

# Day 58 — Data-Centric ML, Evaluation & Reproducibility

> [!curriculum] Machine Learning · Systems
> **Cycle 20** · **status: planned**
> Use the videos for first-pass learning; use this note for fast recall without rewatching.

> [!sequence] Learning sequence
> - [[Curriculum/Lessons/Day 57 - ROS 2, Real-Time Robot Software & Hardware Interfaces|← Day 57]]
> - [[Curriculum/Curriculum|Curriculum map]]
> - [[Curriculum/Lessons/Day 59 - Dataset Design, Long-Tail Metrics & Failure Analysis|Day 59 →]]

> [!concepts] Knowledge-graph concepts
> - [[Mind Map/Nodes/systems|Systems]]
> - [[Mind Map/Nodes/learning|Learning]]

## Brief description

Data-centric ML improves the dataset, labels, splits, and evaluation process as deliberately as the model; reproducibility records enough code, data lineage, configuration, and randomness to explain a result.

## Recall in 30 seconds

- Label quality, coverage, duplicates, leakage, and split design can dominate algorithm changes.
- Metrics must correspond to the operational cost and be reported with uncertainty and subgroup breakdowns.
- An ablation changes one causal factor at a time; a benchmark score without controls is weak evidence.
- Reproducibility needs immutable data versions, executable environments, seeds, hardware details, and failure logs.

## Watch in order

> [!method] Why this sequence
> Watch in order: foundation first, then mechanism, then application or diagnostics where the topic needs it.

### 1. Data centric AI development  From Big Data to Good Data   Andrew Ng

> [!video] Databricks · English · professional foundation
> **Purpose:** Motivates systematic dataset iteration, labeling quality, error analysis, and the data-centric development loop.
> [Watch on YouTube](https://www.youtube.com/watch?v=avoijDORAlc)

### 2. Lecture 15 - Evaluation Metrics | Data Science & Machine Learning | University of Bremen

> [!video] Hendrik Heuer · English · respected educator
> **Purpose:** Supplies the evaluation layer: metric selection, confusion-matrix-derived measures, and interpretation of model performance.
> [Watch on YouTube](https://www.youtube.com/watch?v=1TJ6154M1hQ)

### 3. TechAide AI4Good 2020 - Joelle Pineau: Building Reproducible, Reusable and Robust Deep RL Systems

> [!video] Hugo Larochelle · English · respected educator
> **Purpose:** Explains experimental reproducibility, reusable research infrastructure, reporting discipline, and robustness of empirical conclusions.
> [Watch on YouTube](https://www.youtube.com/watch?v=Phy9Yex5bm4)

> [!summary] After watching
> Close the videos and explain the recall bullets in your own words. Add only corrections or a worked example below—do not recreate the lecture.

## My correction or example

-
