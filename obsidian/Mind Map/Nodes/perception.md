---
generated_by: "build_obsidian_vault.py"
type: "mindmap-node"
aliases: ["Perception"]
node_id: "perception"
kind: "domain"
domain: "perception"
layer: 1
source: "intelligence/mindmap.json"
updated: "2026-09-18"
tags: ["mindmap", "perception", "domain"]
---

# Perception

Turn pixels (and maybe depth) into geometry, semantics, and tracks the policy can condition on. 16 Sep 2026: ActiveScale (arXiv 2609.18514) adds historical video + per-frame pose tokens so a VLA can change viewpoint instead of guessing from a fixed camera.

> **Why it belongs**
> A VLA that cannot see 3D structure or correspondences is guessing in image space.

## Parent

- [[Mind Map/Nodes/embodied-ai|Embodied AI]]

## Children

- [[Mind Map/Nodes/geom-3d|Geometry & 3D]]
- [[Mind Map/Nodes/recog|Recognition]]
- [[Mind Map/Nodes/track-motion|Tracking & motion]]

## Research directions

- Feed-forward multi-view 3D
- Self-supervised ViT features as robot backbones
- Pose-supervised active perception vs extra cameras at train time

## Semantic connections

- [[Mind Map/Nodes/cotracker|CoTracker]] — includes
- [[Mind Map/Nodes/depth-anything|Depth Anything]] — includes
- [[Mind Map/Nodes/detection|Detection]] — includes
- [[Mind Map/Nodes/dinov2|DINOv2]] — uses
- [[Mind Map/Nodes/dust3r|DUSt3R]] — includes
- [[Mind Map/Nodes/eagle|Eagle 2.5]] — includes
- [[Mind Map/Nodes/embodied-ai|Embodied AI]] — includes
- [[Mind Map/Nodes/geom-3d|Geometry & 3D]] — contains
- [[Mind Map/Nodes/mast3r|MASt3R]] — includes
- [[Mind Map/Nodes/recog|Recognition]] — contains
- [[Mind Map/Nodes/segmentation|Segmentation]] — includes
- [[Mind Map/Nodes/stlight|STLight]] — includes
- [[Mind Map/Nodes/track-motion|Tracking & motion]] — contains
- [[Mind Map/Nodes/vggt|VGGT]] — includes

## Primary resources

- **Paper:** [ActiveScale — Scaling Active Perception (arXiv 2609.18514)](https://arxiv.org/abs/2609.18514)
- **Video:** [Stanford CS231n 2025 — Deep Learning for Computer Vision](https://www.youtube.com/playlist?list=PLoROMvodv4rOmsNzYBMe0gJY2XS8AQg16)

## Source

- Canonical record: `intelligence/mindmap.json#perception`
- Live graph: https://chippy1520.github.io/ai-research-lab/mindmap.html#node=perception
