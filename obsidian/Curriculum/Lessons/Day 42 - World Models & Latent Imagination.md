---
generated_by: "build_obsidian_vault.py"
type: "curriculum-lesson"
aliases: ["World Models & Latent Imagination"]
day: 42
cycle: 14
domain: "Embodied AI & RL Robotics"
stage: "Modern"
status: "planned"
source: ["curriculum_plan.json", "curriculum_resources.json"]
tags: ["curriculum", "embodied-ai-rl-robotics", "modern"]
cssclasses: ["research-note", "curriculum-note"]
related_concepts: ["Mind Map/Nodes/world-models.md", "Mind Map/Nodes/systems.md", "Mind Map/Nodes/policy.md"]
related_papers: ["Papers/I-JEPA.md", "Papers/JEPA.md", "Papers/V-JEPA.md", "Papers/V-JEPA 2.md"]
---

[[Home|Research Lab]]  /  [[Curriculum/Curriculum|Curriculum]]

# Day 42 — World Models & Latent Imagination

> [!curriculum] Embodied AI & RL Robotics · Modern
> **Cycle 14** · **status: planned**
> Use the videos for first-pass learning; use this note for fast recall without rewatching.

> [!sequence] Learning sequence
> - [[Curriculum/Lessons/Day 41 - Generative Vision- Latent Diffusion & Controllable Synthesis|← Day 41]]
> - [[Curriculum/Curriculum|Curriculum map]]
> - [[Curriculum/Lessons/Day 43 - Uncertainty, Calibration & Bayesian Deep Learning|Day 43 →]]

> [!concepts] Knowledge-graph concepts
> - [[Mind Map/Nodes/world-models|World models]]
> - [[Mind Map/Nodes/systems|Systems]]
> - [[Mind Map/Nodes/policy|Policies / VLA]]

> [!study] Paper companions
> - [[Papers/I-JEPA|I-JEPA]]
> - [[Papers/JEPA|JEPA]]
> - [[Papers/V-JEPA|V-JEPA]]
> - [[Papers/V-JEPA 2|V-JEPA 2]]

## Brief description

World models learn compact predictive dynamics and use imagined trajectories to evaluate behavior; latent imagination is useful only when the representation preserves control-relevant consequences and uncertainty.

## Recall in 30 seconds

- The model predicts future latent states, observations, rewards, or termination from state-action history.
- Learning and planning in latent space can ignore pixel detail and make long rollouts cheaper.
- A policy can exploit model errors, so uncertainty, short horizons, and real-data correction are essential.
- Visual prediction quality is not the same as decision quality; test whether imagined differences change action choices correctly.

## Watch in order

> [!method] Why this sequence
> Watch in order: foundation first, then mechanism, then application or diagnostics where the topic needs it. Coverage boundary: Concentrates on the Dreamer family rather than surveying every world-model architecture.

### 1. Dream to Control: Learning Behaviors by Latent Imagination

> [!video] Danijar Hafner · English · research lab
> **Purpose:** First-author presentation of Dreamer: latent dynamics learning, imagined rollouts, value learning, and policy optimization inside a learned world model.
> [Watch on YouTube](https://www.youtube.com/watch?v=BDxRNnhPTlU)

> [!summary] After watching
> Close the videos and explain the recall bullets in your own words. Add only corrections or a worked example below—do not recreate the lecture.

## My correction or example

-
