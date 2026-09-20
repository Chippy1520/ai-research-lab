---
generated_by: "build_obsidian_vault.py"
type: "mindmap-node"
aliases: ["Reinforcement learning"]
node_id: "rl"
kind: "concept"
domain: "learning"
layer: 3
source: "intelligence/mindmap.json"
updated: "2026-09-18"
tags: ["mindmap", "learning", "concept"]
---

# Reinforcement learning

Learn from reward, not (only) demos. On real robots: expensive, unsafe, sample-hungry. Still the path for locomotion, recovery, and improving a cloned policy. 16 Sep 2026: Real-Time EXPO-FT (Dong, Hung, Sadigh, Finn; arXiv 2609.18207) RL-finetunes a delayed VLA by splitting slow chunk proposals from a fast edit policy; 10 min of online data lifts four dynamic real tasks 42%→97% (first-party), no human intervention.

> **Why it belongs**
> Humanoid labs mix IL for manipulation with RL for balance. Don't pretend BC replaced RL.

## Parent

- [[Mind Map/Nodes/rl-family|Reinforcement learning]]

## Research directions

- Offline RL on teleop logs
- RL fine-tune of a VLA action expert
- Does Real-Time EXPO-FT's edit policy transfer from Kinetix/dynamic tabletop to SO-100 contact?

## Semantic connections

- [[Mind Map/Nodes/agility|Agility Robotics]] — locomotion
- [[Mind Map/Nodes/async-infer|Async inference]] — needs
- [[Mind Map/Nodes/boston-dynamics|Boston Dynamics]] — uses
- [[Mind Map/Nodes/learning|Learning]] — includes
- [[Mind Map/Nodes/mdp|MDP]] — formalism
- [[Mind Map/Nodes/offline-rl|Offline RL]] — includes
- [[Mind Map/Nodes/policy-gradient|Policy gradient]] — includes
- [[Mind Map/Nodes/ppo-sac|PPO / SAC]] — includes
- [[Mind Map/Nodes/q-learning|Q-learning]] — includes
- [[Mind Map/Nodes/rl-family|Reinforcement learning]] — contains

## Primary resources

- **Paper:** [Real-Time EXPO-FT (arXiv 2609.18207)](https://arxiv.org/abs/2609.18207)
- **Video:** [David Silver — Reinforcement Learning course](https://www.youtube.com/playlist?list=PLEAYkSg4uSQ2S3rHUCqz6W1ZKybVICeSP)
- **Docs:** [Isaac Lab](https://developer.nvidia.com/isaac/lab)

## Source

- Canonical record: `intelligence/mindmap.json#rl`
- Live graph: https://chippy1520.github.io/ai-research-lab/mindmap.html#node=rl
