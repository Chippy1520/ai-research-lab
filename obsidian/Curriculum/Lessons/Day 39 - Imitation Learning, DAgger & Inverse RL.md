---
generated_by: "build_obsidian_vault.py"
type: "curriculum-lesson"
aliases: ["Imitation Learning, DAgger & Inverse RL"]
day: 39
cycle: 13
domain: "Embodied AI & RL Robotics"
stage: "Modern"
status: "planned"
source: ["curriculum_plan.json", "curriculum_resources.json"]
tags: ["curriculum", "embodied-ai-rl-robotics", "modern"]
cssclasses: ["research-note", "curriculum-note"]
related_concepts: ["Mind Map/Nodes/il.md", "Mind Map/Nodes/imit.md", "Mind Map/Nodes/learning.md", "Mind Map/Nodes/systems.md", "Mind Map/Nodes/policy.md"]
related_papers: []
---

[[Home|Research Lab]]  /  [[Curriculum/Curriculum|Curriculum]]

# Day 39 — Imitation Learning, DAgger & Inverse RL

> [!curriculum] Embodied AI & RL Robotics · Modern
> **Cycle 13** · **status: planned**
> Use the videos for first-pass learning; use this note for fast recall without rewatching.

> [!sequence] Learning sequence
> - [[Curriculum/Lessons/Day 38 - Open-Vocabulary Detection & Foundation Segmentation|← Day 38]]
> - [[Curriculum/Curriculum|Curriculum map]]
> - [[Curriculum/Lessons/Day 40 - Self-Supervised, Contrastive & Multimodal Learning|Day 40 →]]

> [!concepts] Knowledge-graph concepts
> - [[Mind Map/Nodes/il|Imitation learning]]
> - [[Mind Map/Nodes/imit|Imitation]]
> - [[Mind Map/Nodes/learning|Learning]]
> - [[Mind Map/Nodes/systems|Systems]]
> - [[Mind Map/Nodes/policy|Policies / VLA]]

## Brief description

Imitation learning trains behavior from demonstrations; DAgger reduces compounding error by querying an expert on learner-visited states, while inverse RL infers a reward that could explain expert behavior.

## Recall in 30 seconds

- Behavior cloning is supervised learning under the demonstrator's state distribution.
- Small action errors change future states, so deployment can drift outside the training distribution.
- DAgger aggregates corrections from states induced by the current learner, at the cost of expert interaction.
- Inverse RL is underdetermined: many rewards explain the same behavior, so assumptions and evaluation matter.

## Watch in order

> [!method] Why this sequence
> Watch in order: foundation first, then mechanism, then application or diagnostics where the topic needs it. Coverage boundary: Only the first IRL lecture part is included; it establishes the formulation but omits some later adversarial-IRL variants.

### 1. CS 285: Lecture 2, Imitation Learning. Part 1

> [!video] RAIL · English · research lab
> **Purpose:** Introduces behavioral cloning and supervised imitation learning.
> [Watch on YouTube](https://www.youtube.com/watch?v=tbLaFtYpWWU)

### 2. CS 285: Lecture 2, Imitation Learning. Part 2

> [!video] RAIL · English · research lab
> **Purpose:** Explains compounding covariate shift and interactive data aggregation approaches such as DAgger.
> [Watch on YouTube](https://www.youtube.com/watch?v=YivJ9KDjn-o)

### 3. CS 285: Lecture 20, Inverse Reinforcement Learning, Part 1

> [!video] RAIL · English · research lab
> **Purpose:** Introduces inverse reinforcement learning as inference of objectives or rewards from expert behavior.
> [Watch on YouTube](https://www.youtube.com/watch?v=EcxpbhDeuZw)

> [!summary] After watching
> Close the videos and explain the recall bullets in your own words. Add only corrections or a worked example below—do not recreate the lecture.

## My correction or example

-
