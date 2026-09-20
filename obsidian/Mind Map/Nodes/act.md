---
generated_by: "build_obsidian_vault.py"
type: "mindmap-node"
aliases: ["ACT"]
node_id: "act"
kind: "paper"
domain: "policy"
layer: 3
source: "intelligence/mindmap.json"
updated: "2026-09-18"
tags: ["mindmap", "policy", "paper"]
---

# ACT

Zhao et al., RSS 2023. Chunk + CVAE + temporal ensemble on ALOHA. ~80M, 50 demos, fine bimanual contact. LeRobot's recommended first policy. Sep 2026: UGR (arXiv 2609.15840) adds a decoupled uncertainty head and residual-corrects only the most uncertain timesteps in the chunk — up to +13 pp vs ACT on four of five RoboTwin dual-arm tasks.

> **Why it belongs**
> The design space later VLAs still live in.

## Parent

- [[Mind Map/Nodes/chunked-pi|Chunked policies]]

## Research directions

- Does sparse uncertainty refinement transfer from ACT to flow/VLA chunks?
- Calibrate ACT hidden-state uncertainty on real SO-100 contact failures

## Semantic connections

- [[Mind Map/Nodes/action-chunking|Action chunking]] — implemented-in
- [[Mind Map/Nodes/aloha|ALOHA / SO-100]] — uses
- [[Mind Map/Nodes/backprop|Backprop / SGD]] — trains
- [[Mind Map/Nodes/chunked-pi|Chunked policies]] — contains
- [[Mind Map/Nodes/cnn|CNNs]] — vision-tower
- [[Mind Map/Nodes/cnn|CNNs]] — resnet
- [[Mind Map/Nodes/cvae|CVAE over chunks]] — implemented-in
- [[Mind Map/Nodes/il|Imitation learning]] — trains
- [[Mind Map/Nodes/lerobot|LeRobot]] — ships-in
- [[Mind Map/Nodes/mujoco|MuJoCo / MJX]] — sim-in
- [[Mind Map/Nodes/pid|PID control]] — tracks
- [[Mind Map/Nodes/policy|Policies / VLA]] — includes
- [[Mind Map/Nodes/proprio|Proprioception]] — input
- [[Mind Map/Nodes/smolvla|SmolVLA]] — chunks-kept
- [[Mind Map/Nodes/temporal-ensembling|Temporal ensembling]] — in
- [[Mind Map/Nodes/transformers|Transformers]] — policy
- [[Mind Map/Nodes/transformers|Transformers]] — decoder

## Primary resources

- **Paper:** [UGR — Uncertainty-Guided Sparse Refinement for ACT (arXiv 2609.15840)](https://arxiv.org/abs/2609.15840)
- **Video:** [ALOHA — Learning Fine-Grained Bimanual Manipulation (ACT paper video)](https://www.youtube.com/watch?v=pN4Ig_aTSUo)
- **Guide:** [Our ACT guide](https://chippy1520.github.io/ai-research-lab/papers-act.html)
- **Paper:** [arXiv 2304.13705](https://arxiv.org/abs/2304.13705)
- **Docs:** [LeRobot ACT](https://huggingface.co/docs/lerobot/act)

## Source

- Canonical record: `intelligence/mindmap.json#act`
- Live graph: https://chippy1520.github.io/ai-research-lab/mindmap.html#node=act
