---
generated_by: "build_obsidian_vault.py"
type: "mindmap-node"
aliases: ["Action chunking"]
node_id: "action-chunking"
kind: "method"
domain: "learning"
layer: 3
source: "intelligence/mindmap.json"
updated: "2026-09-18"
tags: ["mindmap", "learning", "method"]
---

# Action chunking

Predict k future joint commands at once, π(a_{t:t+k}|o_t). Effective horizon becomes T/k. Ablation in ACT: k=1 ~1% vs k=100 ~44% on the sim average. 17 Sep 2026: GeoAAC (arXiv 2609.20776) reads Flow Matching denoising geometry to pick k per step with no extra training — GR00T N1.5 / π₀.₅; first-party up to +8.7 pp sim and 53.3%→74.4% real-world average.

> **Why it belongs**
> SmolVLA, Diffusion Policy, and π₀ all still emit chunks. The fight moved to how the chunk is generated.

## Parent

- [[Mind Map/Nodes/imit|Imitation]]

## Research directions

- Does prefix-wise flow geometry beat a fixed k on SO-100 contact, not just LIBERO/RoboCasa?
- GeoAAC adaptive horizon vs SmolVLA async queue threshold g

## Semantic connections

- [[Mind Map/Nodes/act|ACT]] — implemented-in
- [[Mind Map/Nodes/compounding-error|Compounding error]] — mitigated-by
- [[Mind Map/Nodes/cvae|CVAE over chunks]] — plus
- [[Mind Map/Nodes/diffusion-policy|Diffusion Policy]] — uses
- [[Mind Map/Nodes/imit|Imitation]] — contains
- [[Mind Map/Nodes/seq-models|Sequence models]] — chunks-are
- [[Mind Map/Nodes/temporal-ensembling|Temporal ensembling]] — plus
- [[Mind Map/Nodes/vqbet|VQ-BeT]] — uses

## Primary resources

- **Paper:** [GeoAAC — geometry-based adaptive action chunking (arXiv 2609.20776)](https://arxiv.org/abs/2609.20776)
- **Video:** [LeRobot — ALOHA and ACT](https://www.youtube.com/watch?v=ft73x0LfGpM)
- **Guide:** [ACT](https://chippy1520.github.io/ai-research-lab/papers-act.html)

## Source

- Canonical record: `intelligence/mindmap.json#action-chunking`
- Live graph: https://chippy1520.github.io/ai-research-lab/mindmap.html#node=action-chunking
