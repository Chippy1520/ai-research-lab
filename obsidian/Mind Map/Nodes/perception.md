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
cssclasses: ["research-note", "concept-note"]
related_papers: []
related_curriculum: ["Curriculum/Lessons/Day 02 - Image Formation, Sampling & Color.md", "Curriculum/Lessons/Day 05 - 2D Fourier Analysis & Phase.md", "Curriculum/Lessons/Day 08 - Spatial Derivatives, Scale Space & Features.md", "Curriculum/Lessons/Day 11 - Projective Geometry & Camera Calibration.md", "Curriculum/Lessons/Day 14 - Multi-View Geometry, Epipolar Constraints & SfM.md", "Curriculum/Lessons/Day 17 - CNN Backbones, FPN & Detection.md"]
---

[[Home|Research Lab]]  /  [[Mind Map/Embodied AI|Knowledge Graph]]

# Perception

> [!concept] Domain · Perception · Layer 1
> Turn pixels (and maybe depth) into geometry, semantics, and tracks the policy can condition on. 16 Sep 2026: ActiveScale (arXiv 2609.18514) adds historical video + per-frame pose tokens so a VLA can change viewpoint instead of guessing from a fixed camera.
>
> **Why it belongs —** A VLA that cannot see 3D structure or correspondences is guessing in image space.

## Knowledge neighborhood

> [!hierarchy] Hierarchy
> - [[Mind Map/Nodes/embodied-ai|↑ Embodied AI]]
> - [[Mind Map/Nodes/geom-3d|↓ Geometry & 3D]]
> - [[Mind Map/Nodes/recog|↓ Recognition]]
> - [[Mind Map/Nodes/track-motion|↓ Tracking & motion]]

> [!outgoing] Outgoing relationships
> - **includes →** [[Mind Map/Nodes/cotracker|CoTracker]]
> - **includes →** [[Mind Map/Nodes/depth-anything|Depth Anything]]
> - **includes →** [[Mind Map/Nodes/detection|Detection]]
> - **includes →** [[Mind Map/Nodes/dust3r|DUSt3R]]
> - **includes →** [[Mind Map/Nodes/eagle|Eagle 2.5]]
> - **includes →** [[Mind Map/Nodes/mast3r|MASt3R]]
> - **includes →** [[Mind Map/Nodes/segmentation|Segmentation]]
> - **includes →** [[Mind Map/Nodes/stlight|STLight]]
> - **includes →** [[Mind Map/Nodes/vggt|VGGT]]
> - **uses →** [[Mind Map/Nodes/dinov2|DINOv2]]

> [!study] Read and study
> - [[Curriculum/Lessons/Day 02 - Image Formation, Sampling & Color|Day 02 - Image Formation, Sampling & Color]]
> - [[Curriculum/Lessons/Day 05 - 2D Fourier Analysis & Phase|Day 05 - 2D Fourier Analysis & Phase]]
> - [[Curriculum/Lessons/Day 08 - Spatial Derivatives, Scale Space & Features|Day 08 - Spatial Derivatives, Scale Space & Features]]
> - [[Curriculum/Lessons/Day 11 - Projective Geometry & Camera Calibration|Day 11 - Projective Geometry & Camera Calibration]]
> - [[Curriculum/Lessons/Day 14 - Multi-View Geometry, Epipolar Constraints & SfM|Day 14 - Multi-View Geometry, Epipolar Constraints & SfM]]
> - [[Curriculum/Lessons/Day 17 - CNN Backbones, FPN & Detection|Day 17 - CNN Backbones, FPN & Detection]]

## Research directions

- Feed-forward multi-view 3D
- Self-supervised ViT features as robot backbones
- Pose-supervised active perception vs extra cameras at train time

## Primary resources

- **Paper:** [ActiveScale — Scaling Active Perception (arXiv 2609.18514)](https://arxiv.org/abs/2609.18514)
- **Video:** [Stanford CS231n 2025 — Deep Learning for Computer Vision](https://www.youtube.com/playlist?list=PLoROMvodv4rOmsNzYBMe0gJY2XS8AQg16)

> [!source] Local source record
> - Canonical data: `intelligence/mindmap.json#perception`
> - Vault map: [[Mind Map/Embodied AI|Embodied AI Knowledge Graph]]
> - This note is the complete local concept record; no published mirror is required.
