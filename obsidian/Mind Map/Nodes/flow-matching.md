---
generated_by: "build_obsidian_vault.py"
type: "mindmap-node"
aliases: ["Flow matching"]
node_id: "flow-matching"
kind: "method"
domain: "learning"
layer: 3
source: "intelligence/mindmap.json"
updated: "2026-09-18"
tags: ["mindmap", "learning", "method"]
cssclasses: ["research-note", "concept-note"]
related_papers: ["Papers/SmolVLA and LeRobot.md"]
related_curriculum: ["Curriculum/Lessons/Day 31 - Flow Matching & Optimal-Transport Paths.md"]
---

[[Home|Research Lab]]  /  [[Mind Map/Embodied AI|Knowledge Graph]]

# Flow matching

> [!concept] Method · Learning · Layer 3
> Regress a velocity field that transports noise to data along nearly straight ODE paths. Fewer function evaluations than diffusion. Robot uses in 2026: π₀/SmolVLA action experts; VGFM (IROS 2026, arXiv 2609.14261) value-guides intermediate flow times without BPTT; FMP (arXiv 2609.15631) replaces AMP discriminators with an online OT+flow reward on Unitree G1. 17 Sep 2026: Agile-WAM (arXiv 2609.20761) is direct vision-tactile-to-action flow matching that jointly emits action chunks and future vis/tactile latents — first-party 11.9 ms and +29.4% relative real success. TraceFlow (arXiv 2609.20646) steers a frozen flow expert from success/failure traces (one terminal bit; no weight update) — first-party 21→39/50 ordered packing.
>
> **Why it belongs —** SmolVLA's action expert is 0.75d because the path is short. Lipman et al. 2210.02747 is the paper.

## Knowledge neighborhood

> [!hierarchy] Hierarchy
> - [[Mind Map/Nodes/gen-world|↑ World models & generation]]

> [!outgoing] Outgoing relationships
> - **expert →** [[Mind Map/Nodes/smolvla|SmolVLA]]

> [!incoming] Incoming relationships
> - **← expert —** [[Mind Map/Nodes/pi0|π₀]]
> - **← includes —** [[Mind Map/Nodes/generative|Generative models]]

> [!study] Read and study
> - [[Papers/SmolVLA and LeRobot|SmolVLA and LeRobot]]
> - [[Curriculum/Lessons/Day 31 - Flow Matching & Optimal-Transport Paths|Day 31 - Flow Matching & Optimal-Transport Paths]]

## Research directions

- Joint vis-tactile flow WAMs vs frozen-expert TraceFlow guidance on the same contact task
- Value guidance at random flow times vs extra Euler steps at inference
- Flow-matched motion priors vs AMP for humanoid walking from a default pose
- TraceFlow stacking from the robot's own failures vs extra critic/world-model guidance

## Primary resources

- **Paper:** [Agile-WAM — vis-tactile-to-action flow matching (arXiv 2609.20761)](https://arxiv.org/abs/2609.20761)
- **Paper:** [TraceFlow — frozen flow-matching guidance from success/failure traces (arXiv 2609.20646)](https://arxiv.org/abs/2609.20646)
- **Paper:** [Flow-Matched Motion Priors (arXiv 2609.15631)](https://arxiv.org/abs/2609.15631)
- **Paper:** [VGFM — Value-Guided Flow Matching (arXiv 2609.14261)](https://arxiv.org/abs/2609.14261)
- **Video:** [Outlier — Flow matching explained](https://www.youtube.com/watch?v=7cMzfkWFWhI)
- **Paper:** [Flow Matching for Generative Modeling](https://arxiv.org/abs/2210.02747)

> [!source] Source record
> - Canonical: `intelligence/mindmap.json#flow-matching`
> - [Open the public graph](https://chippy1520.github.io/ai-research-lab/mindmap.html#node=flow-matching)
