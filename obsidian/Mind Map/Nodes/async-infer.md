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
cssclasses: ["research-note", "concept-note"]
related_papers: ["Papers/SmolVLA and LeRobot.md"]
related_curriculum: []
---

[[Home|Research Lab]]  /  [[Mind Map/Embodied AI|Knowledge Graph]]

# Async inference

> [!concept] Method · Systems · Layer 3
> Decouple RobotClient (pops actions at Δt) from PolicyServer (fills chunks when queue < g). SmolVLA: similar success, ~30% shorter task time (13.75s → 9.7s pick-place). 17 Sep 2026: SkipVLA (arXiv 2609.20648) runs a classical planner in free space and queries the VLA only for contact-rich skills — first-party up to 2.5× faster on LIBERO and a YAM arm at the same success rate. 16 Sep 2026: rMuscle (arXiv 2609.19104) caches visual tokens and neuron activations across repeated executions — 1.29–1.42× on RTX 4090 and Jetson Thor without dropping real-robot success; Real-Time EXPO-FT (arXiv 2609.18207) RL-finetunes the same latency split.
>
> **Why it belongs —** The systems paper hiding inside a VLA paper. Edge robots live or die here.

## Knowledge neighborhood

> [!hierarchy] Hierarchy
> - [[Mind Map/Nodes/stacks|↑ Software stacks]]

> [!incoming] Incoming relationships
> - **← cousin —** [[Mind Map/Nodes/temporal-ensembling|Temporal ensembling]]
> - **← includes —** [[Mind Map/Nodes/systems|Systems]]
> - **← introduces —** [[Mind Map/Nodes/smolvla|SmolVLA]]
> - **← needs —** [[Mind Map/Nodes/rl|Reinforcement learning]]

> [!study] Read and study
> - [[Papers/SmolVLA and LeRobot|SmolVLA and LeRobot]]

## Research directions

- Planner-for-free-space (SkipVLA) vs muscle-memory cache (rMuscle) vs async chunk queues on the same VLA
- Does SkipVLA's frozen-VLM pose predictor transfer from LIBERO pick-place to SO-100 contact?

## Primary resources

- **Paper:** [SkipVLA — skip VLA steps with classical planning (arXiv 2609.20648)](https://arxiv.org/abs/2609.20648)
- **Paper:** [rMuscle — muscle-memory VLA inference cache (arXiv 2609.19104)](https://arxiv.org/abs/2609.19104)
- **Paper:** [Real-Time EXPO-FT (arXiv 2609.18207)](https://arxiv.org/abs/2609.18207)
- **Video:** [Hugging Face — LeRobot tutorials (record/evaluate loop)](https://www.youtube.com/playlist?list=PLo2EIpI_JMQu5zrDHe4NchRyumF2ynaUN)
- **Guide:** [[Papers/SmolVLA and LeRobot|SmolVLA §3.3]]

> [!source] Local source record
> - Canonical data: `intelligence/mindmap.json#async-infer`
> - Vault map: [[Mind Map/Embodied AI|Embodied AI Knowledge Graph]]
> - This note is the complete local concept record; no published mirror is required.
