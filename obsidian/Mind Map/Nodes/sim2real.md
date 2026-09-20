---
generated_by: "build_obsidian_vault.py"
type: "mindmap-node"
aliases: ["Sim-to-real"]
node_id: "sim2real"
kind: "concept"
domain: "learning"
layer: 3
source: "intelligence/mindmap.json"
updated: "2026-09-18"
tags: ["mindmap", "learning", "concept"]
---

# Sim-to-real

Train in sim (Isaac, MuJoCo), run on metal. Domain randomization, residual RL, or GEN-1.5’s claim: sim demos as prompts with no sim in pretrain. 17 Sep 2026: ReShoot (arXiv 2609.19661) re-renders recorded demos under edited appearance (VLM caption + edge-conditioned video) and copies actions/proprio verbatim — first-party recolored object success 0%→42.9% / 47.5% on two real platforms with 43 and 100 source demos. 16 Sep: function-preserving Real-to-Sim-to-Real (arXiv 2609.18293) deforms reconstructed meshes under contact-interface constraints so synthetic demos stay physically valid.

> **Why it belongs**
> Data multiplier when you do not own a factory.

## Parent

- [[Mind Map/Nodes/xfer|Transfer]]

## Research directions

- ReShoot appearance re-render vs extra teleop in each new visual context
- GEN-1.5 sim-prompt replication on SO-100
- Isaac locomotion + LeRobot manipulation
- Constraint-guided mesh deformation vs naive shape aug for contact-rich insertion

## Semantic connections

- [[Mind Map/Nodes/gen15|GEN-1.5]] — claims
- [[Mind Map/Nodes/isaac|Isaac Lab / Sim]] — from
- [[Mind Map/Nodes/learning|Learning]] — includes
- [[Mind Map/Nodes/mujoco|MuJoCo / MJX]] — from
- [[Mind Map/Nodes/one-shot|One-shot physical prompting]] — touches
- [[Mind Map/Nodes/xfer|Transfer]] — contains

## Primary resources

- **Paper:** [ReShoot — generative visual domain randomization of recorded demos (arXiv 2609.19661)](https://arxiv.org/abs/2609.19661)
- **Paper:** [Function-preserving Real-to-Sim-to-Real (arXiv 2609.18293)](https://arxiv.org/abs/2609.18293)
- **Video:** [NVIDIA — Isaac Lab Office Hours (sim-to-real stack)](https://www.youtube.com/playlist?list=PL3jK4xNnlCVcnMqm4Lnqa5Bok4_iP5NsK)

## Source

- Canonical record: `intelligence/mindmap.json#sim2real`
- Live graph: https://chippy1520.github.io/ai-research-lab/mindmap.html#node=sim2real
