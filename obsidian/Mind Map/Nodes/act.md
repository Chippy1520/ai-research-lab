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
cssclasses: ["research-note", "concept-note"]
related_papers: ["Papers/ACT and ALOHA.md"]
related_curriculum: []
---

[[Home|Research Lab]]  /  [[Mind Map/Embodied AI|Knowledge Graph]]

# ACT

> [!concept] Paper · Policy · Layer 3
> Zhao et al., RSS 2023. Chunk + CVAE + temporal ensemble on ALOHA. ~80M, 50 demos, fine bimanual contact. LeRobot's recommended first policy. Sep 2026: UGR (arXiv 2609.15840) adds a decoupled uncertainty head and residual-corrects only the most uncertain timesteps in the chunk — up to +13 pp vs ACT on four of five RoboTwin dual-arm tasks.
>
> **Why it belongs —** The design space later VLAs still live in.

## Knowledge neighborhood

> [!hierarchy] Hierarchy
> - [[Mind Map/Nodes/chunked-pi|↑ Chunked policies]]

> [!outgoing] Outgoing relationships
> - **chunks kept →** [[Mind Map/Nodes/smolvla|SmolVLA]]
> - **decoder →** [[Mind Map/Nodes/transformers|Transformers]]
> - **resnet →** [[Mind Map/Nodes/cnn|CNNs]]
> - **ships in →** [[Mind Map/Nodes/lerobot|LeRobot]]
> - **sim in →** [[Mind Map/Nodes/mujoco|MuJoCo / MJX]]
> - **uses →** [[Mind Map/Nodes/aloha|ALOHA / SO-100]]

> [!incoming] Incoming relationships
> - **← implemented in —** [[Mind Map/Nodes/action-chunking|Action chunking]]
> - **← implemented in —** [[Mind Map/Nodes/cvae|CVAE over chunks]]
> - **← in —** [[Mind Map/Nodes/temporal-ensembling|Temporal ensembling]]
> - **← includes —** [[Mind Map/Nodes/policy|Policies / VLA]]
> - **← input —** [[Mind Map/Nodes/proprio|Proprioception]]
> - **← policy —** [[Mind Map/Nodes/transformers|Transformers]]
> - **← tracks —** [[Mind Map/Nodes/pid|PID control]]
> - **← trains —** [[Mind Map/Nodes/backprop|Backprop / SGD]]
> - **← trains —** [[Mind Map/Nodes/il|Imitation learning]]
> - **← vision tower —** [[Mind Map/Nodes/cnn|CNNs]]

> [!study] Read and study
> - [[Papers/ACT and ALOHA|ACT and ALOHA]]

## Research directions

- Does sparse uncertainty refinement transfer from ACT to flow/VLA chunks?
- Calibrate ACT hidden-state uncertainty on real SO-100 contact failures

## Primary resources

- **Paper:** [UGR — Uncertainty-Guided Sparse Refinement for ACT (arXiv 2609.15840)](https://arxiv.org/abs/2609.15840)
- **Video:** [ALOHA — Learning Fine-Grained Bimanual Manipulation (ACT paper video)](https://www.youtube.com/watch?v=pN4Ig_aTSUo)
- **Guide:** [[Papers/ACT and ALOHA|Our ACT guide]]
- **Paper:** [arXiv 2304.13705](https://arxiv.org/abs/2304.13705)
- **Docs:** [LeRobot ACT](https://huggingface.co/docs/lerobot/act)

> [!source] Local source record
> - Canonical data: `intelligence/mindmap.json#act`
> - Vault map: [[Mind Map/Embodied AI|Embodied AI Knowledge Graph]]
> - This note is the complete local concept record; no published mirror is required.
