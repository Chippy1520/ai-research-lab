---
generated_by: "build_obsidian_vault.py"
type: "mindmap-node"
aliases: ["Whole-body control"]
node_id: "wbc"
kind: "concept"
domain: "policy"
layer: 3
source: "intelligence/mindmap.json"
updated: "2026-09-18"
tags: ["mindmap", "policy", "concept"]
---

# Whole-body control

Lower-body RL + upper IK, or a learned high-rate controller under a VLA. NVIDIA SONIC / GR00T-WBC; Figure Helix System 0 (~1 kHz). 17 Sep 2026: LYRIC (arXiv 2609.19688) is a generative flow-matching controller for language-driven contact-rich whole-body object interaction (planner + closed-loop action generator) — first-party 90.3% vs 74.2% held-out OMOMO vs the strongest kinematic-planner baseline. 16 Sep: KINO (arXiv 2609.18869) uses VLM-selected whole-body keyframes as the interface to an RL loco-manipulation policy (44%→92% with saliency sampling; Unitree G1).

> **Why it belongs**
> Tabletop VLAs stall on humanoids. This is the actuator-side neighbor.

## Parent

- [[Mind Map/Nodes/embodiment|Embodiment & WBC]]

## Research directions

- Language-conditioned flow WBC (LYRIC) vs keyframe VLM+RL (KINO) on the same humanoid

## Semantic connections

- [[Mind Map/Nodes/agility|Agility Robotics]] — needs
- [[Mind Map/Nodes/apptronik|Apptronik]] — needs
- [[Mind Map/Nodes/boston-dynamics|Boston Dynamics]] — classic
- [[Mind Map/Nodes/embodiment|Embodiment & WBC]] — contains
- [[Mind Map/Nodes/gemini-robotics|Gemini Robotics 2]] — plus
- [[Mind Map/Nodes/gr00t|GR00T N1.5]] — plus
- [[Mind Map/Nodes/helix|Helix / Helix 2.5]] — plus
- [[Mind Map/Nodes/kinematics|Kinematics]] — uses
- [[Mind Map/Nodes/persona-ai|Persona AI]] — needs
- [[Mind Map/Nodes/ppo-sac|PPO / SAC]] — uses
- [[Mind Map/Nodes/state-est|State estimation]] — feeds
- [[Mind Map/Nodes/world-models|World models]] — priors

## Primary resources

- **Paper:** [LYRIC — language-driven flow matching for whole-body object interaction (arXiv 2609.19688)](https://arxiv.org/abs/2609.19688)
- **Paper:** [KINO — keyframe VLM + WBC (arXiv 2609.18869)](https://arxiv.org/abs/2609.18869)
- **Paper:** [WholeBodyWAM (arXiv 2609.18197)](https://arxiv.org/abs/2609.18197)
- **Video:** [Boston Dynamics Atlas — Partners in Parkour](https://www.youtube.com/watch?v=tF4DML7FIWk)
- **Code:** [GR00T-WholeBodyControl](https://github.com/NVlabs/GR00T-WholeBodyControl)

## Source

- Canonical record: `intelligence/mindmap.json#wbc`
- Live graph: https://chippy1520.github.io/ai-research-lab/mindmap.html#node=wbc
