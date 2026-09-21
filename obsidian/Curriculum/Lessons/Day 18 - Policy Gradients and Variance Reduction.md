---
generated_by: "build_obsidian_vault.py"
type: "curriculum-lesson"
aliases: ["Policy Gradients and Variance Reduction"]
day: 18
cycle: 6
domain: "Embodied AI & RL Robotics"
stage: "Core"
status: "planned"
source: ["curriculum_plan.json", "curriculum_resources.json"]
tags: ["curriculum", "embodied-ai-rl-robotics", "core"]
cssclasses: ["research-note", "curriculum-note"]
related_concepts: ["Mind Map/Nodes/systems.md", "Mind Map/Nodes/policy.md"]
related_papers: []
---

[[Home|Research Lab]]  /  [[Curriculum/Curriculum|Curriculum]]

# Day 18 — Policy Gradients and Variance Reduction

> [!curriculum] Embodied AI & RL Robotics · Core
> **Cycle 6** · **status: planned**
> Use the videos for first-pass learning; use this note for fast recall without rewatching.

> [!sequence] Learning sequence
> - [[Curriculum/Lessons/Day 17 - CNN Backbones, FPN & Detection|← Day 17]]
> - [[Curriculum/Curriculum|Curriculum map]]
> - [[Curriculum/Lessons/Day 19 - Variational Inference, ELBO & VAEs|Day 19 →]]

> [!concepts] Knowledge-graph concepts
> - [[Mind Map/Nodes/systems|Systems]]
> - [[Mind Map/Nodes/policy|Policies / VLA]]

## Brief description

Policy-gradient methods optimize expected return directly by increasing the probability of sampled actions in proportion to an estimate of their advantage; variance reduction makes that stochastic gradient usable.

## Recall in 30 seconds

- The log-derivative trick moves the policy gradient inside an expectation over trajectories.
- Subtracting a state-dependent baseline does not change the expected gradient but can greatly reduce variance.
- Rewards-to-go avoid crediting an action for rewards that occurred before it.
- On-policy estimates are sensitive to batch size, reward scale, exploration, and advantage normalization.

## Watch in order

> [!method] Why this sequence
> Watch in order: foundation first, then mechanism, then application or diagnostics where the topic needs it.

### 1. RL Course by David Silver - Lecture 7: Policy Gradient Methods

> [!video] Google DeepMind · English · research lab
> **Purpose:** Derives the policy-gradient theorem and covers score-function gradients, baselines, actor-critic estimators, and variance reduction.
> [Watch on YouTube](https://www.youtube.com/watch?v=KHZVXao4qXs)

> [!summary] After watching
> Close the videos and explain the recall bullets in your own words. Add only corrections or a worked example below—do not recreate the lecture.

## My correction or example

-
