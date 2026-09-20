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
---

# Temporal ensembling

Query a new chunk every tick, average overlaps with w_i=exp(−m i). Smooth, expensive — a forward pass per control step.

> **Why it belongs**
> SmolVLA async is the cheap cousin: infer only when the queue fraction drops below g.

## Parent

- [[Mind Map/Nodes/chunked-pi|Chunked policies]]

## Semantic connections

- [[Mind Map/Nodes/act|ACT]] — in
- [[Mind Map/Nodes/action-chunking|Action chunking]] — plus
- [[Mind Map/Nodes/async-infer|Async inference]] — cousin
- [[Mind Map/Nodes/chunked-pi|Chunked policies]] — contains

## Primary resources

- **Video:** [LeRobot — ALOHA and ACT (temporal ensemble of overlapping chunks)](https://www.youtube.com/watch?v=ft73x0LfGpM)
- **Guide:** [ACT](https://chippy1520.github.io/ai-research-lab/papers-act.html)

## Source

- Canonical record: `intelligence/mindmap.json#temporal-ensembling`
- Live graph: https://chippy1520.github.io/ai-research-lab/mindmap.html#node=temporal-ensembling
