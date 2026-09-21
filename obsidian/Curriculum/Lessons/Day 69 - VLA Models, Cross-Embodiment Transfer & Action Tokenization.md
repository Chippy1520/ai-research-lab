---
generated_by: "build_obsidian_vault.py"
type: "curriculum-lesson"
aliases: ["VLA Models, Cross-Embodiment Transfer & Action Tokenization"]
day: 69
cycle: 23
domain: "Embodied AI & RL Robotics"
stage: "Frontier"
status: "planned"
source: ["curriculum_plan.json", "curriculum_resources.json"]
tags: ["curriculum", "embodied-ai-rl-robotics", "frontier"]
cssclasses: ["research-note", "curriculum-note"]
related_concepts: ["Mind Map/Nodes/cross-embod.md", "Mind Map/Nodes/embodiment.md", "Mind Map/Nodes/xfer.md", "Mind Map/Nodes/systems.md", "Mind Map/Nodes/policy.md"]
related_papers: []
---

[[Home|Research Lab]]  /  [[Curriculum/Curriculum|Curriculum]]

# Day 69 — VLA Models, Cross-Embodiment Transfer & Action Tokenization

> [!curriculum] Embodied AI & RL Robotics · Frontier
> **Cycle 23** · **status: planned**
> Use the videos for first-pass learning; use this note for fast recall without rewatching.

> [!sequence] Learning sequence
> - [[Curriculum/Lessons/Day 68 - Video Foundation Models & World-Centric Perception|← Day 68]]
> - [[Curriculum/Curriculum|Curriculum map]]
> - [[Curriculum/Lessons/Day 70 - Frontier ML Review — Selected on Generation Day|Day 70 →]]

> [!concepts] Knowledge-graph concepts
> - [[Mind Map/Nodes/cross-embod|Cross-embodiment]]
> - [[Mind Map/Nodes/embodiment|Embodiment & WBC]]
> - [[Mind Map/Nodes/xfer|Transfer]]
> - [[Mind Map/Nodes/systems|Systems]]
> - [[Mind Map/Nodes/policy|Policies / VLA]]

## Brief description

Vision-language-action models map perception and instructions to robot actions, pool experience across embodiments, and encode continuous control as tokens, chunks, or generated trajectories.

## Recall in 30 seconds

- A VLA connects a visual-language backbone to an action representation and robot-specific interfaces.
- Cross-embodiment transfer needs shared semantics plus explicit handling of different kinematics, sensors, and action spaces.
- Action tokenization simplifies sequence modeling but introduces quantization, timing, and control-frequency choices.
- Evaluate closed-loop robustness, intervention rate, novel tasks, and embodiment transfer—not only offline action prediction.

## Watch in order

> [!method] Why this sequence
> Watch in order: foundation first, then mechanism, then application or diagnostics where the topic needs it.

### 1. Gemini Robotics: Bringing AI to the physical world

> [!video] Google DeepMind · English · research lab
> **Purpose:** Introduces modern vision-language-action models and the grounding of multimodal foundation models in physical robot actions.
> [Watch on YouTube](https://www.youtube.com/watch?v=4MvGnmmP3c0)

### 2. Spring 2024 GRASP SFI - Karl Pertsch, University of California, Berkeley and Stanford University

> [!video] GRASP Lab · English · university course
> **Purpose:** Covers generalist robot policies and cross-robot or cross-embodiment transfer, including the Octo line of research.
> [Watch on YouTube](https://www.youtube.com/watch?v=81PgFEH62Uw)

### 3. π0: A Foundation Model for Robotics with Sergey Levine - 719

> [!video] The TWIML AI Podcast with Sam Charrington · English · professional foundation
> **Purpose:** Explains a prominent VLA policy, including continuous-action generation and alternatives to simple discrete action tokenization.
> [Watch on YouTube](https://www.youtube.com/watch?v=5mY71rGXAkM)

> [!summary] After watching
> Close the videos and explain the recall bullets in your own words. Add only corrections or a worked example below—do not recreate the lecture.

## My correction or example

-
