---
generated_by: "build_obsidian_vault.py"
type: "mindmap-node"
aliases: ["OpenVLA"]
node_id: "openvla"
kind: "paper"
domain: "policy"
layer: 3
source: "intelligence/mindmap.json"
updated: "2026-09-18"
tags: ["mindmap", "policy", "paper"]
---

# OpenVLA

Kim et al., 7B discrete action tokens on public robot data. The heavy open baseline SmolVLA is sized against. 16 Sep 2026: ActionPiece (arXiv 2609.18487) retrains the AR tokenizer with joint representation+quantization so physical action relationships survive decode — 94.8% LIBERO / 68.8% unseen LIBERO-Plus under a Qwen3-VL-4B policy (not OpenVLA weights; same discrete-token problem).

> **Why it belongs**
> Read the tokenizer to see what flow matching is refusing.

## Parent

- [[Mind Map/Nodes/vla-family|Vision-language-action]]

## Semantic connections

- [[Mind Map/Nodes/oxe|Open X-Embodiment]] — trained-on
- [[Mind Map/Nodes/policy|Policies / VLA]] — includes
- [[Mind Map/Nodes/smolvla|SmolVLA]] — compared-to
- [[Mind Map/Nodes/transformers|Transformers]] — uses
- [[Mind Map/Nodes/vla-family|Vision-language-action]] — contains

## Verified public provenance

- [[Organizations/stanford|Stanford University]] — Research affiliation of several OpenVLA authors in the 2024 project author list; not exclusive ownership. _(verified 2026-09-16)_
- [[Organizations/berkeley|UC Berkeley]] — Research affiliation of OpenVLA authors in the 2024 project author list; not exclusive ownership. _(verified 2026-09-16)_
- [[Organizations/tri|Toyota Research Institute]] — Research affiliation of OpenVLA co-authors in the 2024 project author list; not exclusive ownership. _(verified 2026-09-16)_
- [[Contacts/moojin-kim|Moo Jin Kim]] — Equal-contribution co-first author of OpenVLA. _(verified 2026-09-16)_
- [[Contacts/karl-pertsch|Karl Pertsch]] — Equal-contribution co-first author of OpenVLA. _(verified 2026-09-16)_
- [[Contacts/ethan-foster|Ethan Foster]] — Named co-author of OpenVLA; no individual implementation responsibility inferred. _(verified 2026-09-16)_

## Primary resources

- **Paper:** [ActionPiece — AR VLA action tokenization (arXiv 2609.18487)](https://arxiv.org/abs/2609.18487)
- **Video:** [Moo Jin Kim — OpenVLA (author talk)](https://www.youtube.com/watch?v=-0s0v3q7mBk)
- **Paper:** [arXiv 2406.09246](https://arxiv.org/abs/2406.09246)

## Source

- Canonical record: `intelligence/mindmap.json#openvla`
- Live graph: https://chippy1520.github.io/ai-research-lab/mindmap.html#node=openvla
