---
generated_by: "build_obsidian_vault.py"
type: "mindmap-node"
aliases: ["World models"]
node_id: "world-models"
kind: "concept"
domain: "learning"
layer: 3
source: "intelligence/mindmap.json"
updated: "2026-09-18"
tags: ["mindmap", "learning", "concept"]
cssclasses: ["research-note", "concept-note"]
related_papers: ["Papers/I-JEPA.md", "Papers/JEPA.md", "Papers/V-JEPA.md", "Papers/V-JEPA 2.md"]
related_curriculum: ["Curriculum/Lessons/Day 42 - World Models & Latent Imagination.md"]
---

[[Home|Research Lab]]  /  [[Mind Map/Embodied AI|Knowledge Graph]]

# World models

> [!concept] Concept · Learning · Layer 3
> Predict future observations (or latents) to plan. STL, video DMs, and some VLA imagination heads sit here. STLight is the efficient CNN end; GEN-1.5's 30 s memory is the foundation-model end. 17 Sep 2026: Agile-WAM (arXiv 2609.20761) flow-matches action chunks plus future vis/tactile latents at different horizons (vision far, touch next-frame) — first-party +29.4% relative real success at 11.9 ms, not a giant video backbone. DexTouch-WM (arXiv 2609.20649) scales the same contact prediction from human touch (0→100 h human, 5 h robot fixed). Earlier 17 Sep: MoWAM drops future-video generation at inference for explicit robot-motion prediction. 16 Sep: WholeBodyWAM pretrains a Motion Expert on UniMotion-4K (>4K h).
>
> **Why it belongs —** A policy that can predict contact is halfway to recovering from it.

## Knowledge neighborhood

> [!hierarchy] Hierarchy
> - [[Mind Map/Nodes/gen-world|↑ World models & generation]]

> [!outgoing] Outgoing relationships
> - **often →** [[Mind Map/Nodes/generative|Generative models]]
> - **priors →** [[Mind Map/Nodes/wbc|Whole-body control]]

> [!incoming] Incoming relationships
> - **← can use —** [[Mind Map/Nodes/q-learning|Q-learning]]
> - **← includes —** [[Mind Map/Nodes/learning|Learning]]
> - **← is a —** [[Mind Map/Nodes/cosmos|NVIDIA Cosmos]]
> - **← is a —** [[Mind Map/Nodes/stlight|STLight]]
> - **← predicts —** [[Mind Map/Nodes/physbrain|PhysBrain 1.5]]

> [!study] Read and study
> - [[Papers/I-JEPA|I-JEPA]]
> - [[Papers/JEPA|JEPA]]
> - [[Papers/V-JEPA|V-JEPA]]
> - [[Papers/V-JEPA 2|V-JEPA 2]]
> - [[Curriculum/Lessons/Day 42 - World Models & Latent Imagination|Day 42 - World Models & Latent Imagination]]

## Research directions

- Human-touch world models (DexTouch-WM) vs robot-only tactile logs at fixed robot hours
- Tactile WAMs (Agile-WAM 11.9 ms) vs video WAMs (MoWAM/DIDO) under contact-rich latency
- Wrist-cam STL as collision prior
- Latent world models for humanoids
- One-step distilled WAMs vs multi-step video imagination under closed-loop latency
- Human-video world-latent actions as VLA mid-training vs OXE-only
- Map-token JEPA world models for mobile manipulation, not just ObjectNav

## Primary resources

- **Paper:** [Agile-WAM — agile tactile world-action model (arXiv 2609.20761)](https://arxiv.org/abs/2609.20761)
- **Paper:** [DexTouch-WM — tactile world models from human touch (arXiv 2609.20649)](https://arxiv.org/abs/2609.20649)
- **Paper:** [MoWAM — explicit future motion for efficient WAMs (arXiv 2609.20709)](https://arxiv.org/abs/2609.20709)
- **Paper:** [WholeBodyWAM (arXiv 2609.18197)](https://arxiv.org/abs/2609.18197)
- **Paper:** [WLA³ — World Latent Action Modeling (arXiv 2609.15870)](https://arxiv.org/abs/2609.15870)
- **Paper:** [DIDO — one-step world-action distillation (arXiv 2609.15570)](https://arxiv.org/abs/2609.15570)
- **Paper:** [GLAM — latent world model over global map memory (arXiv 2609.14561)](https://arxiv.org/abs/2609.14561)
- **Video:** [David Ha / World Models lineage explained](https://www.youtube.com/watch?v=b1roEd6liWI)

> [!source] Source record
> - Canonical: `intelligence/mindmap.json#world-models`
> - [Open the public graph](https://chippy1520.github.io/ai-research-lab/mindmap.html#node=world-models)
