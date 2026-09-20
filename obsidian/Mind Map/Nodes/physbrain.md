---
generated_by: "build_obsidian_vault.py"
type: "mindmap-node"
aliases: ["PhysBrain 1.5"]
node_id: "physbrain"
kind: "paper"
domain: "policy"
layer: 3
source: "intelligence/mindmap.json"
updated: "2026-09-18"
tags: ["mindmap", "policy", "paper"]
---

# PhysBrain 1.5

DeepCybo, 14 Sep 2026. 8B physical foundation model: autoregressive next-token over language, end-effector motion, and dense visual targets. Embodied pretrain is entirely human interaction video; SFT mixes human demos, robot trajectories, and sim. First-party: 72.5 avg on 28 embodied-understanding benches (open-source SOTA; best on 14). Qualitative EE trajectories plus future RGB/depth/robot-mask. Treat numbers as first-party until replicated on a public robot.

> **Why it belongs**
> Open 8B understand→act→predict loop trained from human video, not a closed GEN/π/GR00T checkpoint. Neighbor of world-models and GEN-1.5 — do not merge them.

## Parent

- [[Mind Map/Nodes/robot-fm|Robot foundation models]]

## Research directions

- Independent real-robot success vs understanding-bench scores
- Discrete EE tokens vs flow action experts on the same demos
- Human-video-only pretrain vs OXE robot logs

## Semantic connections

- [[Mind Map/Nodes/policy|Policies / VLA]] — includes
- [[Mind Map/Nodes/robot-fm|Robot foundation models]] — contains
- [[Mind Map/Nodes/world-models|World models]] — predicts

## Primary resources

- **Paper:** [PhysBrain 1.5 (arXiv 2609.14973)](https://arxiv.org/abs/2609.14973)
- **Docs:** [Project page](https://deepcybo-physai.github.io/PhysBrain-1.5/)

## Source

- Canonical record: `intelligence/mindmap.json#physbrain`
- Live graph: https://chippy1520.github.io/ai-research-lab/mindmap.html#node=physbrain
