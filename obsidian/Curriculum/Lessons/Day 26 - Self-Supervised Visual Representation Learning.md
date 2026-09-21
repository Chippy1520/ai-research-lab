---
generated_by: "build_obsidian_vault.py"
type: "curriculum-lesson"
aliases: ["Self-Supervised Visual Representation Learning"]
day: 26
cycle: 9
domain: "Computer Vision"
stage: "Modern"
status: "planned"
source: ["curriculum_plan.json", "curriculum_resources.json"]
tags: ["curriculum", "computer-vision", "modern"]
cssclasses: ["research-note", "curriculum-note"]
related_concepts: ["Mind Map/Nodes/representation.md", "Mind Map/Nodes/supervised.md", "Mind Map/Nodes/learning.md", "Mind Map/Nodes/perception.md"]
related_papers: ["Papers/I-JEPA.md", "Papers/JEPA.md", "Papers/V-JEPA.md", "Papers/V-JEPA 2.md"]
---

[[Home|Research Lab]]  /  [[Curriculum/Curriculum|Curriculum]]

# Day 26 — Self-Supervised Visual Representation Learning

> [!curriculum] Computer Vision · Modern
> **Cycle 9** · **status: planned**
> Use the videos for first-pass learning; use this note for fast recall without rewatching.

> [!sequence] Learning sequence
> - [[Curriculum/Lessons/Day 25 - Attention, RoPE & KV-Caching|← Day 25]]
> - [[Curriculum/Curriculum|Curriculum map]]
> - [[Curriculum/Lessons/Day 27 - Maximum-Entropy RL & Soft Actor-Critic|Day 27 →]]

> [!concepts] Knowledge-graph concepts
> - [[Mind Map/Nodes/representation|Self-supervised representation]]
> - [[Mind Map/Nodes/supervised|Supervised learning]]
> - [[Mind Map/Nodes/learning|Learning]]
> - [[Mind Map/Nodes/perception|Perception]]

> [!study] Paper companions
> - [[Papers/I-JEPA|I-JEPA]]
> - [[Papers/JEPA|JEPA]]
> - [[Papers/V-JEPA|V-JEPA]]
> - [[Papers/V-JEPA 2|V-JEPA 2]]

## Brief description

Self-supervised visual learning creates supervision from the images themselves, training representations through invariance, reconstruction, clustering, or teacher-student prediction before downstream labels are introduced.

## Recall in 30 seconds

- The pretext objective determines which variations become invariant and which information is preserved.
- Contrastive methods distinguish related views from alternatives; non-contrastive methods prevent collapse through architectural or optimization asymmetry.
- Masked and predictive methods learn by reconstructing pixels, tokens, or latent targets.
- Representation quality must be tested across frozen, fine-tuned, dense, and shifted downstream tasks.

## Watch in order

> [!method] Why this sequence
> Watch in order: foundation first, then mechanism, then application or diagnostics where the topic needs it. Coverage boundary: Predates some newer masked-image and teacher-student systems, but covers the central objectives and evaluation framework.

### 1. 10L – Self-supervised learning in computer vision

> [!video] Alfredo Canziani (冷在) · English · respected educator
> **Purpose:** Full university lecture surveying visual pretext tasks, representation learning, contrastive objectives, and downstream transfer.
> [Watch on YouTube](https://www.youtube.com/watch?v=8L10w1KoOU8)

> [!summary] After watching
> Close the videos and explain the recall bullets in your own words. Add only corrections or a worked example below—do not recreate the lecture.

## My correction or example

-
