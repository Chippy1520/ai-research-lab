---
generated_by: "build_obsidian_vault.py"
type: "mindmap-node"
aliases: ["One-shot physical prompting"]
node_id: "one-shot"
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

# One-shot physical prompting

> [!concept] Concept · Learning · Layer 3
> Put a short sensorimotor demo in the model's context window; the robot attempts the task with no SGD. GEN-1.5's name for it; Skild S1's video prompt is the same cluster. Sep 2026: VLBiMan++ (arXiv 2609.14310) starts from one human demo and claims transfer across task, object, scene, dual-arm embodiment, and long closed-loop perturbations — geometric adaptation, not a foundation-model prompt. 16 Sep 2026: GPT-Policy (arXiv 2609.19138) compiles visual transitions into a commercial VLM agent (GPT-6 Astra) that proposes verified robot-tool actions with no gradient updates; human videos help even without robot action labels.
>
> **Why it belongs —** If this becomes real outside one lab, dataset size is no longer the only scaling law.

## Knowledge neighborhood

> [!hierarchy] Hierarchy
> - [[Mind Map/Nodes/xfer|↑ Transfer]]

> [!outgoing] Outgoing relationships
> - **claimed by →** [[Mind Map/Nodes/gen15|GEN-1.5]]
> - **claimed by →** [[Mind Map/Nodes/skild-s1|Skild S1]]
> - **touches →** [[Mind Map/Nodes/sim2real|Sim-to-real]]

> [!incoming] Incoming relationships
> - **← claims adjacent —** [[Mind Map/Nodes/tesla-optimus|Tesla Optimus]]
> - **← includes —** [[Mind Map/Nodes/learning|Learning]]

## Research directions

- Public one-shot benchmark on SO-100
- Prompt composition for long horizon
- Geometric one-shot (VLBiMan++) vs in-context physical prompting (GEN-1.5 / S1)
- Public one-shot bimanual protocol that is not lab-owned hardware
- VLM-agent ICL (GPT-Policy) vs native VLA context windows (GEN-1.5 / S1)

## Primary resources

- **Paper:** [GPT-Policy — In-Context Robot Learning with VLM Agents (arXiv 2609.19138)](https://arxiv.org/abs/2609.19138)
- **Paper:** [VLBiMan++ (arXiv 2609.14310)](https://arxiv.org/abs/2609.14310)
- **Video:** [Generalist — Introducing GEN-1.5 (in-context physical prompting)](https://www.youtube.com/watch?v=1cllCVK-9lo)

> [!source] Local source record
> - Canonical data: `intelligence/mindmap.json#one-shot`
> - Vault map: [[Mind Map/Embodied AI|Embodied AI Knowledge Graph]]
> - This note is the complete local concept record; no published mirror is required.
