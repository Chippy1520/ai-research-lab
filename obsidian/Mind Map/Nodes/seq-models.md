---
generated_by: "build_obsidian_vault.py"
type: "mindmap-node"
aliases: ["Sequence models"]
node_id: "seq-models"
kind: "concept"
domain: "learning"
layer: 3
source: "intelligence/mindmap.json"
updated: "2026-09-18"
tags: ["mindmap", "learning", "concept"]
cssclasses: ["research-note", "concept-note"]
related_papers: []
related_curriculum: ["Curriculum/Lessons/Day 34 - Sequence Models- RNNs, S4 & Mamba.md"]
---

[[Home|Research Lab]]  /  [[Mind Map/Embodied AI|Knowledge Graph]]

# Sequence models

> [!concept] Concept · Learning · Layer 3
> RNN/LSTM then transformers. PredRNN is the STL tax STLight refused. Action chunks are sequences. 17 Sep 2026: Workspace Models (arXiv 2609.20820, CoRL 2026) distill train-time VLM saliency into a lightweight workspace token so policies keep task memory without in-the-loop VLM queries — drop-in for observations; authors report better policy performance, not just cheaper memory.
>
> **Why it belongs —** Time is a sequence problem before it is a VLA problem.

## Knowledge neighborhood

> [!hierarchy] Hierarchy
> - [[Mind Map/Nodes/opt-basics|↑ Training machinery]]

> [!outgoing] Outgoing relationships
> - **chunks are →** [[Mind Map/Nodes/action-chunking|Action chunking]]
> - **cnn instead →** [[Mind Map/Nodes/stlight|STLight]]
> - **succeeded by →** [[Mind Map/Nodes/transformers|Transformers]]

> [!incoming] Incoming relationships
> - **← includes —** [[Mind Map/Nodes/foundations|Foundations]]

> [!study] Read and study
> - [[Curriculum/Lessons/Day 34 - Sequence Models- RNNs, S4 & Mamba|Day 34 - Sequence Models- RNNs, S4 & Mamba]]

## Research directions

- Workspace token vs full-history conditioning vs in-the-loop VLM memory on long-horizon SO-100

## Primary resources

- **Paper:** [Workspace Models — lightweight robotic memory via saliency distillation (arXiv 2609.20820)](https://arxiv.org/abs/2609.20820)
- **Video:** [Karpathy — RNNs, seq2seq, attention (CS231n)](https://www.youtube.com/watch?v=yCC09vCHzF8)

> [!source] Source record
> - Canonical: `intelligence/mindmap.json#seq-models`
> - [Open the public graph](https://chippy1520.github.io/ai-research-lab/mindmap.html#node=seq-models)
