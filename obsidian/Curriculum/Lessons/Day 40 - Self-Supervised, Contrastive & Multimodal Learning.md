---
generated_by: "build_obsidian_vault.py"
type: "curriculum-lesson"
aliases: ["Self-Supervised, Contrastive & Multimodal Learning"]
day: 40
cycle: 14
domain: "Machine Learning"
stage: "Modern"
status: "planned"
source: ["curriculum_plan.json", "curriculum_resources.json"]
tags: ["curriculum", "machine-learning", "modern"]
cssclasses: ["research-note", "curriculum-note"]
related_concepts: ["Mind Map/Nodes/supervised.md", "Mind Map/Nodes/learning.md", "Mind Map/Nodes/systems.md"]
related_papers: []
---

[[Home|Research Lab]]  /  [[Curriculum/Curriculum|Curriculum]]

# Day 40 — Self-Supervised, Contrastive & Multimodal Learning

> [!curriculum] Machine Learning · Modern
> **Cycle 14** · **status: planned**
> Use the videos for first-pass learning; use this note for fast recall without rewatching.

> [!sequence] Learning sequence
> - [[Curriculum/Lessons/Day 39 - Imitation Learning, DAgger & Inverse RL|← Day 39]]
> - [[Curriculum/Curriculum|Curriculum map]]
> - [[Curriculum/Lessons/Day 41 - Generative Vision- Latent Diffusion & Controllable Synthesis|Day 41 →]]

> [!concepts] Knowledge-graph concepts
> - [[Mind Map/Nodes/supervised|Supervised learning]]
> - [[Mind Map/Nodes/learning|Learning]]
> - [[Mind Map/Nodes/systems|Systems]]

## Brief description

Self-supervised and contrastive learning build representations from paired views or modalities; multimodal objectives align related signals while preserving enough modality-specific information for downstream reasoning.

## Recall in 30 seconds

- Positive-pair design defines what the representation should treat as equivalent.
- Negatives, stop-gradient, momentum teachers, or redundancy constraints are alternative ways to avoid collapsed features.
- Multimodal alignment can enable zero-shot transfer but may discard details not shared across modalities.
- Dataset composition, shortcut correlations, and retrieval metrics shape what apparent alignment means.

## Watch in order

> [!method] Why this sequence
> Watch in order: foundation first, then mechanism, then application or diagnostics where the topic needs it. Coverage boundary: Audio and video multimodality are not treated in depth; image-text learning supplies the principal multimodal case study.

### 1. MedAI Session 8: Self-supervision & Contrastive Frameworks: a vision-based review | Nandita Bhaskhar

> [!video] Stanford MedAI · English · university course
> **Purpose:** Reviews self-supervised pretext learning, contrastive objectives, positive/negative construction, and visual representations.
> [Watch on YouTube](https://www.youtube.com/watch?v=OF_7dBbb_N0)

### 2. OpenAI CLIP: ConnectingText and Images (Paper Explained)

> [!video] Yannic Kilcher · English · respected educator
> **Purpose:** Shows how contrastive learning extends across image and language modalities in CLIP, including zero-shot transfer.
> [Watch on YouTube](https://www.youtube.com/watch?v=T9XSU0pKX2E)

> [!summary] After watching
> Close the videos and explain the recall bullets in your own words. Add only corrections or a worked example below—do not recreate the lecture.

## My correction or example

-
