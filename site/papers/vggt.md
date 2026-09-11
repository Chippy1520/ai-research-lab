# VGGT — Comprehensive Paper Reading Guide

**VGGT: Visual Geometry Grounded Transformer** (CVPR 2025 Best Paper)

## Prerequisites & Knowledge Graph
Multi-view Geometry → Vision Transformers + DINO → Dense Prediction Heads → Feed-forward 3D

## Core Contribution
Feed-forward network that directly outputs camera poses, depth, point maps, and 3D tracks from 1 to hundreds of views in seconds.

## Architecture
Patch + camera tokens. Alternating frame-wise and global self-attention. Camera head + DPT heads.

## Key Results
Strong zero-shot single-view. Outputs usable with COLMAP and splatting.

## Resources
- arXiv: https://arxiv.org/abs/2503.11651
- Code: https://github.com/facebookresearch/vggt
- Demos and COLMAP export in repo

## BibTeX
```bibtex
@inproceedings{wang2025vggt,
  title={VGGT: Visual Geometry Grounded Transformer},
  author={Wang et al.},
  booktitle={CVPR},
  year={2025}
}
```

Full guide inside this repo.
