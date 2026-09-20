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
cssclasses: ["research-note", "concept-note"]
related_papers: ["Papers/VGGT.md"]
related_curriculum: []
---

[[Home|Research Lab]]  /  [[Mind Map/Embodied AI|Knowledge Graph]]

# VGGT

> [!concept] Paper · Perception · Layer 3
> CVPR 2025 Best Paper. One transformer: cameras, depth, points, tracks from 1–hundreds of views in <1 s, often beating BA-based pipelines. At test, fuse depth+cameras rather than the point-map head.
>
> **Why it belongs —** A perception backbone for robots that need 3D without a COLMAP ritual.

## Knowledge neighborhood

> [!hierarchy] Hierarchy
> - [[Mind Map/Nodes/geom-3d|↑ Geometry & 3D]]

> [!outgoing] Outgoing relationships
> - **compared to →** [[Mind Map/Nodes/mast3r|MASt3R]]
> - **is →** [[Mind Map/Nodes/transformers|Transformers]]
> - **replaces postprocess →** [[Mind Map/Nodes/dust3r|DUSt3R]]
> - **uses →** [[Mind Map/Nodes/cotracker|CoTracker]]
> - **uses →** [[Mind Map/Nodes/dinov2|DINOv2]]

> [!incoming] Incoming relationships
> - **← AA —** [[Mind Map/Nodes/attention|Attention]]
> - **← backbone —** [[Mind Map/Nodes/transformers|Transformers]]
> - **← includes —** [[Mind Map/Nodes/perception|Perception]]
> - **← learned —** [[Mind Map/Nodes/stereo|Stereo / multi-view]]
> - **← masks —** [[Mind Map/Nodes/segmentation|Segmentation]]
> - **← outputs —** [[Mind Map/Nodes/camera-model|Camera model]]
> - **← specialist vs —** [[Mind Map/Nodes/depth-anything|Depth Anything]]

> [!study] Read and study
> - [[Papers/VGGT|VGGT]]

## Primary resources

- **Guide:** [Our VGGT guide](https://chippy1520.github.io/ai-research-lab/papers-vggt.html)
- **Paper:** [arXiv 2503.11651](https://arxiv.org/abs/2503.11651)
- **Code:** [facebookresearch/vggt](https://github.com/facebookresearch/vggt)

> [!source] Source record
> - Canonical: `intelligence/mindmap.json#vggt`
> - [Open the public graph](https://chippy1520.github.io/ai-research-lab/mindmap.html#node=vggt)
