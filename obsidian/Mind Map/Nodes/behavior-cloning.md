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
cssclasses: ["research-note", "concept-note"]
related_papers: []
related_curriculum: []
---

[[Home|Research Lab]]  /  [[Mind Map/Embodied AI|Knowledge Graph]]

# Behavior cloning

> [!concept] Concept · Learning · Layer 3
> Supervised map from observation to expert action. Fast to train, fails when the policy leaves the demo manifold — compounding error. 17 Sep 2026: HIL-UMI (arXiv 2609.20659) runs DAgger-style VLA post-training on a handheld UMI without executing the policy on the robot — Energy Score collects OOD frames; first-party, beats HG-DAgger on Clean Up Table with lower per-frame collection time.
>
> **Why it belongs —** Every LeRobot ACT/SmolVLA fine-tune is still BC at heart.

## Knowledge neighborhood

> [!hierarchy] Hierarchy
> - [[Mind Map/Nodes/imit|↑ Imitation]]

> [!outgoing] Outgoing relationships
> - **fails by →** [[Mind Map/Nodes/compounding-error|Compounding error]]

> [!incoming] Incoming relationships
> - **← data for —** [[Mind Map/Nodes/teleop|Teleoperation]]
> - **← includes —** [[Mind Map/Nodes/il|Imitation learning]]
> - **← includes —** [[Mind Map/Nodes/learning|Learning]]

## Research directions

- Robot-free UMI Energy Score vs on-robot HG-DAgger for the same VLA checkpoint
- Does advantage-conditioned BC on mixed UMI+base demos beat plain SFT on SO-100 contact?

## Primary resources

- **Paper:** [HIL-UMI — robot-free HIL post-training of VLAs (arXiv 2609.20659)](https://arxiv.org/abs/2609.20659)
- **Video:** [LeRobot — ALOHA and ACT (imitation / behavior cloning on a real arm)](https://www.youtube.com/watch?v=ft73x0LfGpM)
- **Paper:** [DAgger](https://arxiv.org/abs/1011.0686)

> [!source] Local source record
> - Canonical data: `intelligence/mindmap.json#behavior-cloning`
> - Vault map: [[Mind Map/Embodied AI|Embodied AI Knowledge Graph]]
> - This note is the complete local concept record; no published mirror is required.
