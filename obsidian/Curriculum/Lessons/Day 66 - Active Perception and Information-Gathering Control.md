---
generated_by: "build_obsidian_vault.py"
type: "curriculum-lesson"
aliases: ["Active Perception and Information-Gathering Control"]
day: 66
cycle: 22
domain: "Embodied AI & RL Robotics"
stage: "Frontier"
status: "planned"
source: ["curriculum_plan.json", "curriculum_resources.json"]
tags: ["curriculum", "embodied-ai-rl-robotics", "frontier"]
cssclasses: ["research-note", "curriculum-note"]
related_concepts: ["Mind Map/Nodes/perception.md", "Mind Map/Nodes/systems.md", "Mind Map/Nodes/policy.md"]
related_papers: []
---

[[Home|Research Lab]]  /  [[Curriculum/Curriculum|Curriculum]]

# Day 66 — Active Perception and Information-Gathering Control

> [!curriculum] Embodied AI & RL Robotics · Frontier
> **Cycle 22** · **status: planned**
> Use the videos for first-pass learning; use this note for fast recall without rewatching.

> [!sequence] Learning sequence
> - [[Curriculum/Lessons/Day 65 - Event Cameras, Active Vision & Computational Imaging|← Day 65]]
> - [[Curriculum/Curriculum|Curriculum map]]
> - [[Curriculum/Lessons/Day 67 - Foundation-Model Agents, Tool Use & Memory|Day 67 →]]

> [!concepts] Knowledge-graph concepts
> - [[Mind Map/Nodes/perception|Perception]]
> - [[Mind Map/Nodes/systems|Systems]]
> - [[Mind Map/Nodes/policy|Policies / VLA]]

## Brief description

Active perception selects actions partly for the information they reveal, coupling belief estimation with control so the agent can reduce uncertainty before committing to a task action.

## Recall in 30 seconds

- A sensing action can have low immediate task reward but high value of information.
- Belief-space planning predicts how actions change both physical state and uncertainty.
- Information gain, entropy reduction, and task value are related but not interchangeable objectives.
- Approximate beliefs and expensive lookahead require receding horizons, learned surrogates, and safety-aware exploration.

## Watch in order

> [!method] Why this sequence
> Watch in order: foundation first, then mechanism, then application or diagnostics where the topic needs it.

### 1. Christopher Denniston on Active Robot Perception for Understanding the World | Toronto AIR Seminar

> [!video] AI Robotics Seminar - University of Toronto · English · university course
> **Purpose:** Introduces active robot perception and the coupling between sensing actions, scene understanding, and downstream decisions.
> [Watch on YouTube](https://www.youtube.com/watch?v=ffyGHsoZKwo)

### 2. Geoffrey A. Hollinger - Information Gathering with Multi-Robot Teams

> [!video] ARL Workshop on Heterogeneity, Diversity and Resilience in Multi-Robot Systems · English · official conference
> **Purpose:** Develops information objectives, informative planning, uncertainty reduction, and control for single- and multi-robot sensing.
> [Watch on YouTube](https://www.youtube.com/watch?v=DRKj-SHLS58)

> [!summary] After watching
> Close the videos and explain the recall bullets in your own words. Add only corrections or a worked example below—do not recreate the lecture.

## My correction or example

-
