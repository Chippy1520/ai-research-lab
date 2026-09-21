---
generated_by: "build_obsidian_vault.py"
type: "mindmap-node"
aliases: ["Temporal ensembling"]
node_id: "temporal-ensembling"
kind: "method"
domain: "policy"
layer: 3
source: "intelligence/mindmap.json"
updated: "2026-09-18"
tags: ["mindmap", "policy", "method"]
cssclasses: ["research-note", "concept-note"]
related_papers: []
related_curriculum: []
---

[[Home|Research Lab]]  /  [[Mind Map/Embodied AI|Knowledge Graph]]

# Temporal ensembling

> [!concept] Method · Policy · Layer 3
> Query a new chunk every tick, average overlaps with w_i=exp(−m i). Smooth, expensive — a forward pass per control step.
>
> **Why it belongs —** SmolVLA async is the cheap cousin: infer only when the queue fraction drops below g.

## Knowledge neighborhood

> [!hierarchy] Hierarchy
> - [[Mind Map/Nodes/chunked-pi|↑ Chunked policies]]

> [!outgoing] Outgoing relationships
> - **cousin →** [[Mind Map/Nodes/async-infer|Async inference]]
> - **in →** [[Mind Map/Nodes/act|ACT]]

> [!incoming] Incoming relationships
> - **← plus —** [[Mind Map/Nodes/action-chunking|Action chunking]]

## Primary resources

- **Video:** [LeRobot — ALOHA and ACT (temporal ensemble of overlapping chunks)](https://www.youtube.com/watch?v=ft73x0LfGpM)
- **Guide:** [[Papers/ACT and ALOHA|ACT]]

> [!source] Local source record
> - Canonical data: `intelligence/mindmap.json#temporal-ensembling`
> - Vault map: [[Mind Map/Embodied AI|Embodied AI Knowledge Graph]]
> - This note is the complete local concept record; no published mirror is required.
