---
generated_by: "build_obsidian_vault.py"
type: "mindmap-node"
aliases: ["Diffusion Policy"]
node_id: "diffusion-policy"
kind: "paper"
domain: "policy"
layer: 3
source: "intelligence/mindmap.json"
updated: "2026-09-18"
tags: ["mindmap", "policy", "paper"]
cssclasses: ["research-note", "concept-note"]
related_papers: []
related_curriculum: ["Curriculum/Lessons/Day 51 - Diffusion Policy for Visuomotor Control.md"]
---

[[Home|Research Lab]]  /  [[Mind Map/Embodied AI|Knowledge Graph]]

# Diffusion Policy

> [!concept] Paper · Policy · Layer 3
> Chi et al.: denoise an action chunk. Same chunking instinct as ACT, different generative head. LeRobot ships it next to ACT. 17 Sep 2026: Movement Trend Guidance (arXiv 2609.20669) conditions DP3 on a compact latent of interaction evolution (sparse future gripper states at train; latent-only at test, +3.52% params) — first-party 71.93% vs 37.08% LIBERO-40 and 72% vs 49% on five real tasks.
>
> **Why it belongs —** The other baseline you will actually train before a VLA.

## Knowledge neighborhood

> [!hierarchy] Hierarchy
> - [[Mind Map/Nodes/chunked-pi|↑ Chunked policies]]

> [!outgoing] Outgoing relationships
> - **cousin →** [[Mind Map/Nodes/vqbet|VQ-BeT]]
> - **is a →** [[Mind Map/Nodes/generative|Generative models]]
> - **uses →** [[Mind Map/Nodes/action-chunking|Action chunking]]

> [!incoming] Incoming relationships
> - **← includes —** [[Mind Map/Nodes/generative|Generative models]]
> - **← scales —** [[Mind Map/Nodes/rdt|RDT-1B]]

> [!study] Read and study
> - [[Curriculum/Lessons/Day 51 - Diffusion Policy for Visuomotor Control|Day 51 - Diffusion Policy for Visuomotor Control]]

## Research directions

- Latent interaction-evolution (Movement Trend) vs extra point-cloud tokens on SO-100 contact

## Primary resources

- **Paper:** [Learning Foresight without Explicit Trajectories for 3D Diffusion Policies (arXiv 2609.20669)](https://arxiv.org/abs/2609.20669)
- **Video:** [Cheng Chi — Diffusion Policy (LeRobot)](https://www.youtube.com/watch?v=M03sZFfW-qU)
- **Paper:** [arXiv 2303.04137](https://arxiv.org/abs/2303.04137)

> [!source] Source record
> - Canonical: `intelligence/mindmap.json#diffusion-policy`
> - [Open the public graph](https://chippy1520.github.io/ai-research-lab/mindmap.html#node=diffusion-policy)
