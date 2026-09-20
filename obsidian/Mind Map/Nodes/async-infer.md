---
generated_by: "build_obsidian_vault.py"
type: "mindmap-node"
aliases: ["Async inference"]
node_id: "async-infer"
kind: "method"
domain: "systems"
layer: 3
source: "intelligence/mindmap.json"
updated: "2026-09-18"
tags: ["mindmap", "systems", "method"]
---

# Async inference

Decouple RobotClient (pops actions at Δt) from PolicyServer (fills chunks when queue < g). SmolVLA: similar success, ~30% shorter task time (13.75s → 9.7s pick-place). 17 Sep 2026: SkipVLA (arXiv 2609.20648) runs a classical planner in free space and queries the VLA only for contact-rich skills — first-party up to 2.5× faster on LIBERO and a YAM arm at the same success rate. 16 Sep 2026: rMuscle (arXiv 2609.19104) caches visual tokens and neuron activations across repeated executions — 1.29–1.42× on RTX 4090 and Jetson Thor without dropping real-robot success; Real-Time EXPO-FT (arXiv 2609.18207) RL-finetunes the same latency split.

> **Why it belongs**
> The systems paper hiding inside a VLA paper. Edge robots live or die here.

## Parent

- [[Mind Map/Nodes/stacks|Software stacks]]

## Research directions

- Planner-for-free-space (SkipVLA) vs muscle-memory cache (rMuscle) vs async chunk queues on the same VLA
- Does SkipVLA's frozen-VLM pose predictor transfer from LIBERO pick-place to SO-100 contact?

## Semantic connections

- [[Mind Map/Nodes/rl|Reinforcement learning]] — needs
- [[Mind Map/Nodes/smolvla|SmolVLA]] — introduces
- [[Mind Map/Nodes/stacks|Software stacks]] — contains
- [[Mind Map/Nodes/systems|Systems]] — includes
- [[Mind Map/Nodes/temporal-ensembling|Temporal ensembling]] — cousin

## Primary resources

- **Paper:** [SkipVLA — skip VLA steps with classical planning (arXiv 2609.20648)](https://arxiv.org/abs/2609.20648)
- **Paper:** [rMuscle — muscle-memory VLA inference cache (arXiv 2609.19104)](https://arxiv.org/abs/2609.19104)
- **Paper:** [Real-Time EXPO-FT (arXiv 2609.18207)](https://arxiv.org/abs/2609.18207)
- **Video:** [Hugging Face — LeRobot tutorials (record/evaluate loop)](https://www.youtube.com/playlist?list=PLo2EIpI_JMQu5zrDHe4NchRyumF2ynaUN)
- **Guide:** [SmolVLA §3.3](https://chippy1520.github.io/ai-research-lab/papers-smolvla.html#walk)

## Source

- Canonical record: `intelligence/mindmap.json#async-infer`
- Live graph: https://chippy1520.github.io/ai-research-lab/mindmap.html#node=async-infer
