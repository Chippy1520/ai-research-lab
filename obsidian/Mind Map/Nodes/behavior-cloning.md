---
generated_by: "build_obsidian_vault.py"
type: "mindmap-node"
aliases: ["Behavior cloning"]
node_id: "behavior-cloning"
kind: "concept"
domain: "learning"
layer: 3
source: "intelligence/mindmap.json"
updated: "2026-09-18"
tags: ["mindmap", "learning", "concept"]
---

# Behavior cloning

Supervised map from observation to expert action. Fast to train, fails when the policy leaves the demo manifold — compounding error. 17 Sep 2026: HIL-UMI (arXiv 2609.20659) runs DAgger-style VLA post-training on a handheld UMI without executing the policy on the robot — Energy Score collects OOD frames; first-party, beats HG-DAgger on Clean Up Table with lower per-frame collection time.

> **Why it belongs**
> Every LeRobot ACT/SmolVLA fine-tune is still BC at heart.

## Parent

- [[Mind Map/Nodes/imit|Imitation]]

## Research directions

- Robot-free UMI Energy Score vs on-robot HG-DAgger for the same VLA checkpoint
- Does advantage-conditioned BC on mixed UMI+base demos beat plain SFT on SO-100 contact?

## Semantic connections

- [[Mind Map/Nodes/compounding-error|Compounding error]] — fails-by
- [[Mind Map/Nodes/imit|Imitation]] — contains
- [[Mind Map/Nodes/il|Imitation learning]] — includes
- [[Mind Map/Nodes/learning|Learning]] — includes
- [[Mind Map/Nodes/teleop|Teleoperation]] — data-for

## Primary resources

- **Paper:** [HIL-UMI — robot-free HIL post-training of VLAs (arXiv 2609.20659)](https://arxiv.org/abs/2609.20659)
- **Video:** [LeRobot — ALOHA and ACT (imitation / behavior cloning on a real arm)](https://www.youtube.com/watch?v=ft73x0LfGpM)
- **Paper:** [DAgger](https://arxiv.org/abs/1011.0686)

## Source

- Canonical record: `intelligence/mindmap.json#behavior-cloning`
- Live graph: https://chippy1520.github.io/ai-research-lab/mindmap.html#node=behavior-cloning
