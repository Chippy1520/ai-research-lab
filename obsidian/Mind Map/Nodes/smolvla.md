---
generated_by: "build_obsidian_vault.py"
type: "mindmap-node"
aliases: ["SmolVLA"]
node_id: "smolvla"
kind: "paper"
domain: "policy"
layer: 3
source: "intelligence/mindmap.json"
updated: "2026-09-18"
tags: ["mindmap", "policy", "paper"]
cssclasses: ["research-note", "concept-note"]
related_papers: ["Papers/SmolVLA and LeRobot.md"]
related_curriculum: []
---

[[Home|Research Lab]]  /  [[Mind Map/Embodied AI|Knowledge Graph]]

# SmolVLA

> [!concept] Paper · Policy · Layer 3
> Hugging Face, 450M. SmolVLM-2 + flow expert, community data, async inference. LIBERO-competitive with 10× smaller VLAs. SO-100 average 78.3% after community pretrain (51.7 without).
>
> **Why it belongs —** The open, one-GPU VLA you can actually fine-tune.

## Knowledge neighborhood

> [!hierarchy] Hierarchy
> - [[Mind Map/Nodes/vla-family|↑ Vision-language-action]]

> [!outgoing] Outgoing relationships
> - **compared to →** [[Mind Map/Nodes/octo|Octo]]
> - **compared to →** [[Mind Map/Nodes/openvla|OpenVLA]]
> - **evals on →** [[Mind Map/Nodes/aloha|ALOHA / SO-100]]
> - **evals on →** [[Mind Map/Nodes/libero|LIBERO]]
> - **flow →** [[Mind Map/Nodes/generative|Generative models]]
> - **introduces →** [[Mind Map/Nodes/async-infer|Async inference]]
> - **ships in →** [[Mind Map/Nodes/lerobot|LeRobot]]

> [!incoming] Incoming relationships
> - **← CA SA —** [[Mind Map/Nodes/attention|Attention]]
> - **← backbone —** [[Mind Map/Nodes/transformers|Transformers]]
> - **← chunks kept —** [[Mind Map/Nodes/act|ACT]]
> - **← expert —** [[Mind Map/Nodes/flow-matching|Flow matching]]
> - **← includes —** [[Mind Map/Nodes/policy|Policies / VLA]]
> - **← input —** [[Mind Map/Nodes/proprio|Proprioception]]
> - **← objective —** [[Mind Map/Nodes/supervised|Supervised learning]]
> - **← releases —** [[Mind Map/Nodes/huggingface|Hugging Face / LeRobot]]
> - **← trains —** [[Mind Map/Nodes/backprop|Backprop / SGD]]
> - **← trains —** [[Mind Map/Nodes/il|Imitation learning]]
> - **← vision —** [[Mind Map/Nodes/representation|Self-supervised representation]]

> [!study] Read and study
> - [[Papers/SmolVLA and LeRobot|SmolVLA and LeRobot]]

> [!evidence] Verified public provenance
> - [[Organizations/hugging-face|Hugging Face]] — Published the SmolVLA release and training/inference recipes in the LeRobot ecosystem. _(verified 2026-09-16)_
> - [[Contacts/andres-marafioti|Andres Marafioti]] — Co-author of the official SmolVLA release article; this evidence alone does not establish ownership of a particular subsystem. _(verified 2026-09-16)_
> - [[Contacts/mustafa-shukor|Mustafa Shukor]] — SmolVLA researcher and release article co-author; personal research page identifies the work. _(verified 2026-09-16)_

## Primary resources

- **Video:** [Hugging Face — SmolVLA (official)](https://www.youtube.com/watch?v=VbhL8_vVtVM)
- **Guide:** [[Papers/SmolVLA and LeRobot|Our SmolVLA guide]]
- **Paper:** [arXiv 2506.01844](https://arxiv.org/abs/2506.01844)
- **Code:** [LeRobot](https://github.com/huggingface/lerobot)

> [!source] Local source record
> - Canonical data: `intelligence/mindmap.json#smolvla`
> - Vault map: [[Mind Map/Embodied AI|Embodied AI Knowledge Graph]]
> - This note is the complete local concept record; no published mirror is required.
