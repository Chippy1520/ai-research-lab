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
---

# Diffusion Policy

Chi et al.: denoise an action chunk. Same chunking instinct as ACT, different generative head. LeRobot ships it next to ACT. 17 Sep 2026: Movement Trend Guidance (arXiv 2609.20669) conditions DP3 on a compact latent of interaction evolution (sparse future gripper states at train; latent-only at test, +3.52% params) — first-party 71.93% vs 37.08% LIBERO-40 and 72% vs 49% on five real tasks.

> **Why it belongs**
> The other baseline you will actually train before a VLA.

## Parent

- [[Mind Map/Nodes/chunked-pi|Chunked policies]]

## Research directions

- Latent interaction-evolution (Movement Trend) vs extra point-cloud tokens on SO-100 contact

## Semantic connections

- [[Mind Map/Nodes/action-chunking|Action chunking]] — uses
- [[Mind Map/Nodes/chunked-pi|Chunked policies]] — contains
- [[Mind Map/Nodes/generative|Generative models]] — includes
- [[Mind Map/Nodes/generative|Generative models]] — is-a
- [[Mind Map/Nodes/rdt|RDT-1B]] — scales
- [[Mind Map/Nodes/vqbet|VQ-BeT]] — cousin

## Primary resources

- **Paper:** [Learning Foresight without Explicit Trajectories for 3D Diffusion Policies (arXiv 2609.20669)](https://arxiv.org/abs/2609.20669)
- **Video:** [Cheng Chi — Diffusion Policy (LeRobot)](https://www.youtube.com/watch?v=M03sZFfW-qU)
- **Paper:** [arXiv 2303.04137](https://arxiv.org/abs/2303.04137)

## Source

- Canonical record: `intelligence/mindmap.json#diffusion-policy`
- Live graph: https://chippy1520.github.io/ai-research-lab/mindmap.html#node=diffusion-policy
