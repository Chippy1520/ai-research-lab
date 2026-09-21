---
generated_by: "build_obsidian_vault.py"
type: "curriculum-lesson"
aliases: ["Attention, RoPE & KV-Caching"]
day: 25
cycle: 9
domain: "Machine Learning"
stage: "Modern"
status: "planned"
source: ["curriculum_plan.json", "curriculum_resources.json"]
tags: ["curriculum", "machine-learning", "modern"]
cssclasses: ["research-note", "curriculum-note"]
related_concepts: ["Mind Map/Nodes/attention.md", "Mind Map/Nodes/systems.md", "Mind Map/Nodes/learning.md"]
related_papers: []
---

[[Home|Research Lab]]  /  [[Curriculum/Curriculum|Curriculum]]

# Day 25 — Attention, RoPE & KV-Caching

> [!curriculum] Machine Learning · Modern
> **Cycle 9** · **status: planned**
> Use the videos for first-pass learning; use this note for fast recall without rewatching.

> [!sequence] Learning sequence
> - [[Curriculum/Lessons/Day 24 - PPO- Clipping, Trust Regions & Diagnostics|← Day 24]]
> - [[Curriculum/Curriculum|Curriculum map]]
> - [[Curriculum/Lessons/Day 26 - Self-Supervised Visual Representation Learning|Day 26 →]]

> [!concepts] Knowledge-graph concepts
> - [[Mind Map/Nodes/attention|Attention]]
> - [[Mind Map/Nodes/systems|Systems]]
> - [[Mind Map/Nodes/learning|Learning]]

## Brief description

Transformer inference combines content-based attention with positional rotation and a cache of previous keys and values; these choices determine context handling, memory use, and generation speed.

## Recall in 30 seconds

- Queries select information from keys and aggregate the corresponding values.
- RoPE encodes relative position by rotating query and key features before their dot product.
- Autoregressive decoding reuses past keys and values so earlier tokens are not recomputed.
- KV-cache memory grows with layers, sequence length, batch size, heads, and precision, making bandwidth a deployment bottleneck.

## Watch in order

> [!method] Why this sequence
> Watch in order: foundation first, then mechanism, then application or diagnostics where the topic needs it.

### 1. Stanford CS25: V1 I Transformers United: DL Models that have revolutionized NLP, CV, RL

> [!video] Stanford Online · English · university course
> **Purpose:** Establishes transformer architecture and self-attention before the positional and inference-specific material.
> [Watch on YouTube](https://www.youtube.com/watch?v=P127jhj-8-Y)

### 2. RoPE: Understanding Rotary Positional Embeddings in transformers

> [!video] Hugging Face · English · professional foundation
> **Purpose:** Explains rotary positional embeddings and how rotation injects relative-position information into attention.
> [Watch on YouTube](https://www.youtube.com/watch?v=jlGf2qieSk0)

### 3. How KV Cache Speeds Up LLMs for Faster AI Models on GPUs

> [!video] IBM Technology · English · professional foundation
> **Purpose:** Completes the lesson with autoregressive KV reuse, latency benefits, and memory costs.
> [Watch on YouTube](https://www.youtube.com/watch?v=o0gkdZBtwEg)

> [!summary] After watching
> Close the videos and explain the recall bullets in your own words. Add only corrections or a worked example below—do not recreate the lecture.

## My correction or example

-
