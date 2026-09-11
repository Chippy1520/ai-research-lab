# VGGT — Comprehensive Paper Reading Guide

**VGGT: Visual Geometry Grounded Transformer** (CVPR 2025 Best Paper)

## Prerequisites & Knowledge Graph
Multi-view Geometry → Vision Transformers + DINO → Dense Prediction Heads → Feed-forward 3D

## Core Contribution
Feed-forward network that directly outputs camera poses, depth, point maps, and tracks from 1 to hundreds of images in seconds.

## Detailed Architecture
- Patch + camera tokens
- Alternating frame-wise and global attention
- Camera head + DPT heads

## Key Insights
Strong zero-shot single-view performance. Outputs usable with COLMAP/Gaussian Splatting.

## Resources
- arXiv / CVPR paper
- https://github.com/facebookresearch/vggt
- DINO and DPT explainers on YouTube

*Self-contained in AI Research Lab.*
