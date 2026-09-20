---
generated_by: "build_obsidian_vault.py"
type: "mindmap-node"
aliases: ["VGGT"]
node_id: "vggt"
kind: "paper"
domain: "perception"
layer: 3
source: "intelligence/mindmap.json"
updated: "2026-09-18"
tags: ["mindmap", "perception", "paper"]
---

# VGGT

CVPR 2025 Best Paper. One transformer: cameras, depth, points, tracks from 1–hundreds of views in <1 s, often beating BA-based pipelines. At test, fuse depth+cameras rather than the point-map head.

> **Why it belongs**
> A perception backbone for robots that need 3D without a COLMAP ritual.

## Parent

- [[Mind Map/Nodes/geom-3d|Geometry & 3D]]

## Semantic connections

- [[Mind Map/Nodes/attention|Attention]] — AA
- [[Mind Map/Nodes/camera-model|Camera model]] — outputs
- [[Mind Map/Nodes/cotracker|CoTracker]] — uses
- [[Mind Map/Nodes/depth-anything|Depth Anything]] — specialist-vs
- [[Mind Map/Nodes/dinov2|DINOv2]] — uses
- [[Mind Map/Nodes/dust3r|DUSt3R]] — replaces-postprocess
- [[Mind Map/Nodes/geom-3d|Geometry & 3D]] — contains
- [[Mind Map/Nodes/mast3r|MASt3R]] — compared-to
- [[Mind Map/Nodes/perception|Perception]] — includes
- [[Mind Map/Nodes/segmentation|Segmentation]] — masks
- [[Mind Map/Nodes/stereo|Stereo / multi-view]] — learned
- [[Mind Map/Nodes/transformers|Transformers]] — backbone
- [[Mind Map/Nodes/transformers|Transformers]] — is

## Primary resources

- **Guide:** [Our VGGT guide](https://chippy1520.github.io/ai-research-lab/papers-vggt.html)
- **Paper:** [arXiv 2503.11651](https://arxiv.org/abs/2503.11651)
- **Code:** [facebookresearch/vggt](https://github.com/facebookresearch/vggt)

## Source

- Canonical record: `intelligence/mindmap.json#vggt`
- Live graph: https://chippy1520.github.io/ai-research-lab/mindmap.html#node=vggt
