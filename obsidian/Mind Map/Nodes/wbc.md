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
cssclasses: ["research-note", "concept-note"]
related_papers: []
related_curriculum: []
---

[[Home|Research Lab]]  /  [[Mind Map/Embodied AI|Knowledge Graph]]

# Whole-body control

> [!concept] Concept · Policy · Layer 3
> Lower-body RL + upper IK, or a learned high-rate controller under a VLA. NVIDIA SONIC / GR00T-WBC; Figure Helix System 0 (~1 kHz). 17 Sep 2026: LYRIC (arXiv 2609.19688) is a generative flow-matching controller for language-driven contact-rich whole-body object interaction (planner + closed-loop action generator) — first-party 90.3% vs 74.2% held-out OMOMO vs the strongest kinematic-planner baseline. 16 Sep: KINO (arXiv 2609.18869) uses VLM-selected whole-body keyframes as the interface to an RL loco-manipulation policy (44%→92% with saliency sampling; Unitree G1).
>
> **Why it belongs —** Tabletop VLAs stall on humanoids. This is the actuator-side neighbor.

## Knowledge neighborhood

> [!hierarchy] Hierarchy
> - [[Mind Map/Nodes/embodiment|↑ Embodiment & WBC]]

> [!outgoing] Outgoing relationships
> - **uses →** [[Mind Map/Nodes/ppo-sac|PPO / SAC]]

> [!incoming] Incoming relationships
> - **← classic —** [[Mind Map/Nodes/boston-dynamics|Boston Dynamics]]
> - **← feeds —** [[Mind Map/Nodes/state-est|State estimation]]
> - **← needs —** [[Mind Map/Nodes/agility|Agility Robotics]]
> - **← needs —** [[Mind Map/Nodes/apptronik|Apptronik]]
> - **← needs —** [[Mind Map/Nodes/persona-ai|Persona AI]]
> - **← plus —** [[Mind Map/Nodes/gemini-robotics|Gemini Robotics 2]]
> - **← plus —** [[Mind Map/Nodes/gr00t|GR00T N1.5]]
> - **← plus —** [[Mind Map/Nodes/helix|Helix / Helix 2.5]]
> - **← priors —** [[Mind Map/Nodes/world-models|World models]]
> - **← uses —** [[Mind Map/Nodes/kinematics|Kinematics]]

## Research directions

- Language-conditioned flow WBC (LYRIC) vs keyframe VLM+RL (KINO) on the same humanoid

## Primary resources

- **Paper:** [LYRIC — language-driven flow matching for whole-body object interaction (arXiv 2609.19688)](https://arxiv.org/abs/2609.19688)
- **Paper:** [KINO — keyframe VLM + WBC (arXiv 2609.18869)](https://arxiv.org/abs/2609.18869)
- **Paper:** [WholeBodyWAM (arXiv 2609.18197)](https://arxiv.org/abs/2609.18197)
- **Video:** [Boston Dynamics Atlas — Partners in Parkour](https://www.youtube.com/watch?v=tF4DML7FIWk)
- **Code:** [GR00T-WholeBodyControl](https://github.com/NVlabs/GR00T-WholeBodyControl)

> [!source] Source record
> - Canonical: `intelligence/mindmap.json#wbc`
> - [Open the public graph](https://chippy1520.github.io/ai-research-lab/mindmap.html#node=wbc)
