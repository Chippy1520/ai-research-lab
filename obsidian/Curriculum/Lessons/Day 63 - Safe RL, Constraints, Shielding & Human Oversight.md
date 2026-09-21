---
generated_by: "build_obsidian_vault.py"
type: "curriculum-lesson"
aliases: ["Safe RL, Constraints, Shielding & Human Oversight"]
day: 63
cycle: 21
domain: "Embodied AI & RL Robotics"
stage: "Frontier"
status: "planned"
source: ["curriculum_plan.json", "curriculum_resources.json"]
tags: ["curriculum", "embodied-ai-rl-robotics", "frontier"]
cssclasses: ["research-note", "curriculum-note"]
related_concepts: ["Mind Map/Nodes/systems.md", "Mind Map/Nodes/policy.md"]
related_papers: []
---

[[Home|Research Lab]]  /  [[Curriculum/Curriculum|Curriculum]]

# Day 63 — Safe RL, Constraints, Shielding & Human Oversight

> [!curriculum] Embodied AI & RL Robotics · Frontier
> **Cycle 21** · **status: planned**
> Use the videos for first-pass learning; use this note for fast recall without rewatching.

> [!sequence] Learning sequence
> - [[Curriculum/Lessons/Day 62 - Adversarial Robustness, OOD Detection & Model Editing|← Day 62]]
> - [[Curriculum/Curriculum|Curriculum map]]
> - [[Curriculum/Lessons/Day 64 - Neural Operators, Scientific ML & Differentiable Simulation|Day 64 →]]

> [!concepts] Knowledge-graph concepts
> - [[Mind Map/Nodes/systems|Systems]]
> - [[Mind Map/Nodes/policy|Policies / VLA]]

## Brief description

Safe RL constrains learning and execution through cost objectives, shields, recovery policies, and human oversight, recognizing that reward optimization alone does not encode operational acceptability.

## Recall in 30 seconds

- A constrained MDP distinguishes reward from safety costs or hard limits.
- A shield overrides or filters an action when a verified safety condition would be violated.
- Training safety and deployment safety differ because exploration, estimation error, and distribution shift change risk.
- Oversight needs calibrated uncertainty, meaningful intervention points, audit logs, and a safe fallback state.

## Watch in order

> [!method] Why this sequence
> Watch in order: foundation first, then mechanism, then application or diagnostics where the topic needs it.

### 1. RLSS 2023 - Safe Reinforcement Learning - Felix Berkenkamp

> [!video] Universitat Pompeu Fabra - Barcelona · English · university course
> **Purpose:** Establishes safe-RL objectives, constrained decision making, safe exploration, and safety guarantees.
> [Watch on YouTube](https://www.youtube.com/watch?v=HhTBUHiZWPE)

### 2. Shield Synthesis for Safe Reinforcement Learning

> [!video] Simons Institute for the Theory of Computing · English · official conference
> **Purpose:** Focuses on runtime shields and formal intervention mechanisms that prevent unsafe actions.
> [Watch on YouTube](https://www.youtube.com/watch?v=DUkqNJ-rwck)

### 3. Research talk: Safe reinforcement learning using advantage-based intervention

> [!video] Microsoft Research · English · research lab
> **Purpose:** Covers intervention and oversight mechanisms in which an external controller or human supervisor constrains learned behavior.
> [Watch on YouTube](https://www.youtube.com/watch?v=3PEOFPtVrPw)

> [!summary] After watching
> Close the videos and explain the recall bullets in your own words. Add only corrections or a worked example below—do not recreate the lecture.

## My correction or example

-
