---
generated_by: "build_obsidian_vault.py"
type: "paper-guide"
aliases: ["I-JEPA", "I-JEPA: predict embeddings of masked blocks, not their pixels"]
paper_slug: "ijepa"
source: "site/papers-ijepa.html"
live_url: "https://chippy1520.github.io/ai-research-lab/papers-ijepa.html"
tags: ["paper", "reading-guide"]
related_nodes: ["representation", "world-models"]
related_curriculum: ["Curriculum/Lessons/Day 07 - Information Theory & Representation.md", "Curriculum/Lessons/Day 26 - Self-Supervised Visual Representation Learning.md", "Curriculum/Lessons/Day 42 - World Models & Latent Imagination.md", "Curriculum/Lessons/Day 46 - Causal Representation Learning & Invariance.md"]
cssclasses: ["research-note", "paper-note"]
---

[[Home|Research Lab]]  /  [[Papers/Paper Guides|Paper Guides]]

# I-JEPA: predict embeddings of masked blocks, not their pixels

> [!paper] Research reading guide
> Complete reading guide for I-JEPA (Assran et al., CVPR 2023, arXiv 2301.08243): predict target-block embeddings from a context block, no SimCLR augmentations.
>
> **Concepts:** 2 · **Related curriculum notes:** 4

> [!concepts] Connected concepts
> - [[Mind Map/Nodes/representation|Self-supervised representation]]
> - [[Mind Map/Nodes/world-models|World models]]

> [!study] Continue in the curriculum
> - [[Curriculum/Lessons/Day 07 - Information Theory & Representation|Day 07 - Information Theory & Representation]]
> - [[Curriculum/Lessons/Day 26 - Self-Supervised Visual Representation Learning|Day 26 - Self-Supervised Visual Representation Learning]]
> - [[Curriculum/Lessons/Day 42 - World Models & Latent Imagination|Day 42 - World Models & Latent Imagination]]
> - [[Curriculum/Lessons/Day 46 - Causal Representation Learning & Invariance|Day 46 - Causal Representation Learning & Invariance]]

> [!source] Canonical and public versions
> - Repository guide: `site/papers-ijepa.html`
> - [Open the published HTML guide](https://chippy1520.github.io/ai-research-lab/papers-ijepa.html)
> - Companion source: `papers/ijepa.md`

---

## How a person fills in a dog whose head is covered

A notebook covers a dog’s head in a photo. MAE would train a decoder to fill in those pixels. You do not need the fur. You need the fact “dog head, this pose.” I-JEPA trains a predictor to match the target encoder’s embeddings $E(y)$ on the covered blocks, not a reconstruction of $y$.

> [!example] Step 01 — You
> **You:** You look at everything that is not covered: body, leash, grass, the way the neck is aimed.
>
> **The paper:** Context encoder (ViT) sees only the visible patches. No mask tokens inside the encoder — they would leak “something is missing here.”

> [!example] Step 02 — You
> **You:** You are told where to guess: “the rectangle over the neck.” Without a location you would not know whether to predict a head or a tail.
>
> **The paper:** Predictor is a narrow ViT. It gets context tokens plus positional tokens $z$ for the target block’s location.

> [!example] Step 03 — You
> **You:** Your answer is the identity and pose of the hidden part, not an RGB crop of it.
>
> **The paper:** Loss is in representation space . Targets come from a target encoder (EMA of the context encoder) run on the full image; you read off the tokens in the target block.

> [!example] Step 04 — You
> **You:** You guess several covered regions, not one pixel-wide slit. A slit is texture. A block is an object part.
>
> **The paper:** Multi-block masking: four target blocks with scale $(0.15, 0.2)$, then a big context block scale $(0.85, 1.0)$ with those targets punched out. Small random MAE masks fail this test.

The mapping *is* the architecture: context ViT → predictor-with-positions → EMA target tokens. No colour jitter was required for you to know it was a dog head. That is the point of dropping SimCLR augmentations.

## The paper, in order — every section

Open [arXiv 2301.08243](https://arxiv.org/pdf/2301.08243) (v3, 13 Apr 2023) next to this. Headings below match the PDF.

### Abstract

Learn semantic image representations without hand-crafted view augmentations. I-JEPA: from a single context block, predict representations of various target blocks in the same image. Masking must (a) sample large-scale (semantic) targets and (b) keep a spatially distributed informative context. ViT-H/14 on ImageNet, 16 A100s, under 72 hours; transfers to linear classification, object counting, depth.

### Figure 1 — ImageNet linear vs GPU hours

The poster plot: I-JEPA sits above MAE/data2vec at fewer GPU hours because the loss is already in embedding space, so you do not train a pixel decoder. Read the axes before you memorise a single top-1.

### Figure 2 — three energy cartoons

(a) Joint-Embedding Architecture: pull $E(x)$ and $E(y)$ together for two augmented views. Collapse is the failure mode. (b) Generative: decode $y$ from $E(x)$ and mask tokens $z$. Collapse is unlikely if $z$ is small. (c) JEPA: predict $E(y)$ from $E(x)$ given $z$. Looks like (b), loses like (a). This figure is LeCun 2022 drawn for CVPR. If you cannot redraw it, do not start §3.

### §1 Introduction

Two SSL families in vision. Invariance methods (SimCLR, BYOL, DINO, VICReg, iBOT): strong semantics, but the augmentation list is a prior that does not travel to audio and is wrong for some tasks (classification vs instance segmentation want different invariances). Generative / mask-denoising (MAE, BEiT): less prior, travels across modalities, but representations are lower-level — you need full fine-tuning to catch up on linear probe. I-JEPA wants MAE’s lack of augmentation prior and DINO’s off-the-shelf semantics.

Three empirical claims to score later: (1) beats MAE-like methods on ImageNet linear / 1% / semantic transfer; (2) competitive with view-invariant methods on semantics and *better* on counting and depth; (3) cheaper: ViT-H/14 < 1200 GPU hours, $2.5\times$ faster than iBOT ViT-S/16, $10\times$ more efficient than MAE ViT-H/14.

### §2 Background

EBMs: low energy on compatible pairs. JEA collapse fixes: contrastive negatives, VICReg redundancy, clustering entropy, or asymmetric EMA. Generative collapse is rare because you still have to paint $y$. JEPA collapse is real; they steal BYOL’s EMA teacher plus a predictor. Conditioning on $z$ is what makes JEPA not “make two views identical.”

### §3 Method — Figure 3

![I-JEPA: context encoder, predictor with positional tokens, EMA target encoder](https://arxiv.org/html/2301.08243v3/ijepa.png)

**Paper Figure 3.** Context ViT on visible patches. Narrow predictor, coloured positional tokens = $z$. Target encoder is EMA of the context encoder. Loss is between predictor output and target-encoder tokens in the block. There is no pixel decoder in this figure. If a slide added one, it is MAE, not this paper.

**Targets.** Run the target encoder on the full image (or all patches), then *keep only* the tokens whose patches fall in a sampled target block. Targets are representations, not pixels, not discrete visual tokens.

**Context.** Sample a large block, remove any overlap with the targets, feed the rest to the context encoder. The encoder never sees mask tokens.

**Predictor.** Narrow ViT. Inputs: context tokens + one learned positional token per target patch location. Output: one vector per target patch, same width as the encoder.

**Loss.** Average L2 (paper: average of squared error in representation space) over predicted vs target tokens. Stop-gradient through the target encoder. EMA update of target weights.

### Figure 4 — masking

![I-JEPA context and target block masking examples](https://arxiv.org/html/2301.08243v3/mask-samples-4.png)

**Paper Figure 4.** Four target blocks, scale $(0.15,0.2)$, aspect $(0.75,1.5)$. Context scale $(0.85,1.0)$ minus those blocks. Targets look like object parts. Context is still most of the image, just with holes.

### §4 Related work

Places I-JEPA against MAE, data2vec, CAE, MSN, DINO, iBOT. data2vec is the closest cousin (predict EMA representations) but uses a different mask and is not sold as “no view augmentations.” Cite the PDF, not a blog, for the exact differences.

### §5 Image classification — Table 1

Protocol: freeze encoder, linear probe on full ImageNet-1K train, average-pooled tokens (no [CLS]). LARS, batch 16384, 50 epochs (appendix). Numbers from Table 1:

| Method (no view augs) | Arch | Epochs | IN-1K linear top-1 |
| --- | --- | --- | --- |
| MAE | ViT-B/16 | 1600 | 68.0 |
| MAE | ViT-L/16 | 1600 | 76.0 |
| MAE | ViT-H/14 | 1600 | 77.2 |
| data2vec | ViT-L/16 | 1600 | 77.3 |
| I-JEPA | ViT-B/16 | 600 | 72.9 |
| I-JEPA | ViT-L/16 | 600 | 77.5 |
| I-JEPA | ViT-H/14 | 300 | 79.3 |
| I-JEPA | ViT-H/16 at 448 | 300 | 81.1 |

View-aug methods still sit higher at similar size (DINO ViT-B/8 80.1, iBOT ViT-L/16 81.0). The paper’s claim is not “beats DINO.” It is “matches that ballpark without the augmentation prior, and does it with fewer epochs than MAE.”

1% ImageNet semi-supervised (≈12 labels/class): ViT-L/16 69.4, ViT-H/14 73.3, ViT-H/16448 77.3 (Meta blog quotes the 12-shot story). Full fine-tune, appendix Table 15: I-JEPA ViT-H/16448 87.1 vs MAE ViT-H/14448 87.8 after 1600 MAE epochs — I-JEPA used 300. Within 1%, 5.3× fewer epochs. Do not say “beats MAE at fine-tune.”

### §6 Local prediction tasks

This is the section that justifies dropping SimCLR. Counting (CLEVR) and depth: view-invariance methods throw away localisation that those tasks need. I-JEPA keeps it because the predictor is still spatially addressed. Quote the PDF’s tables here rather than a tweet. The qualitative claim in the Meta blog: a decoder fitted on predictor outputs sketches a dog head / bird leg in the right pose — semantics without discarding position.

![I-JEPA predictor visualizations decoded back to pixels](https://arxiv.org/html/2301.08243v3/visualization_predictor_2.png)

**Paper predictor visualisation.** Context outside the box → predictor representation inside the box → a separate generative probe paints a sketch. The sketch is not the training loss. It is a probe that the latent meant “the rest of the animal, correct pose.”

### §7 Scalability

ViT-H/14 < 1200 GPU hours; 16×A100 < 72 h. Faster than iBOT ViT-S/16 by $2.5\times$, cheaper than MAE ViT-H/14 by $10\times$. Predicting in representation space removes the decoder FLOPs and converges in ~5× fewer iterations than MAE (paper’s comparison).

### §8 Predictor visualisations

Already above. The predictor is a restricted world model of *spatial* uncertainty in a still image. It is not a physics engine.

### §9 Ablations

Load-bearing knobs, from the PDF: large target blocks beat small/random MAE masks; context must remain informative (do not mask 90% like MAE); predicting encoder outputs beats predicting pixels (Table 11 flavour: masking the target-encoder output vs input). Predictor width is a bottleneck on purpose — too wide and it copies texture.

### §10 Conclusion

Semantic features, no hand-crafted views, cheaper than pixel reconstruction. Path for joint-embedding methods that are not SimCLR. Next sentence in history is V-JEPA (replace image blocks with video tubes).

### What the paper does *not* claim

Not a world model of time. Not an agent. Not “beats DINO.” Not hierarchical JEPA. No language. No robot.

## The engineering tension

| Alternative | Representation and consequence |
|---|---|
| **MAE** | MAE Mask 75% of patches, decode RGB. Travels to video. Linear probe is mediocre because the encoder kept texture the decoder needed. |
| **I-JEPA** | I-JEPA Mask large semantic blocks, predict EMA embeddings. Same “no augmentation list” as MAE. Linear probe jumps (ViT-H/14: 79.3 vs MAE 77.2) at a fraction of the GPU hours. |

| Alternative | Representation and consequence |
|---|---|
| **DINO / SimCLR** | DINO / SimCLR Two views, make embeddings equal. Needs colour jitter, crops, maybe multi-crop. Semantics are great; counting/depth suffer; the recipe is image-specific. |
| **I-JEPA** | I-JEPA One view, predict other places in the same image. Invariances are learned only if they help prediction. Depth and counting stay in the representation. |

## Prerequisites

1. **01**

   #### Vision Transformers

   Patch tokens, positional embeddings, no [CLS] required (I-JEPA pools). If ViT is fuzzy, Figure 3 is unreadable.
2. **02**

   #### MAE-style masking

   I-JEPA reuses the “hide patches, predict them” game. The change is the output space.
3. **03**

   #### BYOL / EMA teacher

   Stop-gradient + slow copy of the encoder is the collapse brake. Same idea as Grill et al. 2020.
4. **04**

   #### The JEPA cartoon

   Read [[Papers/JEPA|LeCun 2022]] until Figure 2 of this paper is obvious.

> [!video] 3Blue1Brown — Transformers
> [Watch video](https://www.youtube.com/watch?v=wjZofJX0v4M)
>
> Why this video: the ViT is a transformer on patches. Not a recap of I-JEPA.

> [!video] DINOv2 — self-supervised ViT features
> [Watch video](https://www.youtube.com/watch?v=csEgtSh7jV4)
>
> The invariance-family cousin. Useful so you can feel what I-JEPA is refusing (view augmentations) and what it still wants (semantic frozen features).

## Knowledge graph

```text
LeCun JEPA 2022
   │
   ├─ MAE (mask, pixel loss)
   ├─ BYOL (EMA teacher)
   └─ ViT
          │
          ▼
       I-JEPA
          ├─ multi-block mask
          ├─ context ViT
          └─ predictor + z
                │
                ▼
             V-JEPA
```

> [!graph] Concept flow
> **JEPA 2022 · MAE · BYOL EMA**
> ↓
> **context encoder · predictor + z · EMA target**
> ↓
> **I-JEPA (this paper)**

## Architecture

> [!flow] Architecture / data flow
> **Image patches** — 224², patch 16 or 14
> ↓ sample 4 target blocks + 1 context
> **Context encoder ViT** — visible patches only + **Target encoder ViT** — EMA, full image, stop-grad
> ↓ + positional tokens z
> **Predictor (narrow ViT)** — emits one vector per target patch
> ↓ L2
> **‖P − Ē(target tokens)‖²**

## Multi-block masking

Default recipe from Figure 4 / §3: $M=4$ targets, scale $U(0.15,0.2)$, aspect $U(0.75,1.5)$; context scale $U(0.85,1.0)$ then subtract overlaps. This is not MAE’s random 75%. A random sprinkle of patches can be inpainted from local texture; a 20% block cannot, unless you know what object was there.

## Results, honestly

| Fact from the paper | What it means |
| --- | --- |
| ViT-H/14 linear 79.3 after 300 epochs | Above MAE ViT-H/14 77.2 after 1600 epochs, no view augs. |
| ViT-H/16448 linear 81.1 | In iBOT’s neighbourhood, still without SimCLR augs. |
| Fine-tune 87.1 vs MAE 87.8 | Not a win. A near-tie at 5.3× fewer pretrain epochs. |
| <1200 GPU hours for ViT-H/14 | The efficiency claim. Predict in $E(\cdot)$, skip the pixel decoder. |
| Better counting / depth than DINO-like | The reason to prefer I-JEPA when the downstream task is spatial, not just IN-1K top-1. |

Protocol reminder: linear numbers are frozen-encoder, average pool, LARS probe. Do not compare them to a paper that fine-tunes the backbone unless you say so.

## Worked intuition

ViT-B/16, $224\times 224$ → $14\times 14 = 196$ patches, $d=768$. Sample a target block of ~20% area ≈ 40 patches. Context keeps ~$196-40=156$ patches (more, because four smaller blocks). Context encoder: 156 tokens → 156 vectors in $\mathbb{R}^{768}$. Predictor (narrower, say 384-d inside, project back) + 40 position tokens → 40 vectors in $\mathbb{R}^{768}$. Target encoder: 196 tokens, index the 40. Loss: mean of $\| \hat{v}\_i - \mathrm{sg}(\bar{v}\_i) \|\_2^2$. EMA $\bar{\theta} \leftarrow m\bar{\theta} + (1-m)\theta$. Nobody decoded $16\times 16\times 3$ RGB cells.

## Caveats

- Still ImageNet-centric pretraining. “No augmentations” still uses random resized crop to 224 in the usual ViT pipeline — they mean no colour jitter / blur / multi-crop *views*.
- Linear-probe wins versus MAE are the headline; fine-tune is a near-tie.
- Predictor visualisations use a separate generative probe. Pretty pictures are not the loss.
- Not a temporal world model. That is V-JEPA.

## Study plan

80 minutes: case (10) → Figure 2 cartoons + Figure 3 (20) → Table 1 protocol and numbers (15) → Figure 4 masking + §9 (15) → §6 counting/depth vs DINO (10) → open [[Papers/V-JEPA|V-JEPA]] (10). Hold the PDF on Figure 3 the whole time.

## Primary sources

- Paper: [arXiv:2301.08243](https://arxiv.org/abs/2301.08243) · [arXiv HTML v3](https://arxiv.org/html/2301.08243v3)
- CVPR page: Assran et al., CVPR 2023, pp. 15619–15629
- Code / weights: [github.com/facebookresearch/ijepa](https://github.com/facebookresearch/ijepa)
- Official blog: [Meta AI — I-JEPA](https://ai.meta.com/blog/yann-lecun-ai-model-i-jepa/)
- Blueprint: [[Papers/JEPA|LeCun 2022 JEPA]] · next: [[Papers/V-JEPA|V-JEPA]]

**BibTeX**

```
@InProceedings{Assran_2023_CVPR,
  author    = {Assran, Mahmoud and Duval, Quentin and Misra, Ishan and Bojanowski, Piotr and Vincent, Pascal and Rabbat, Michael and LeCun, Yann and Ballas, Nicolas},
  title     = {Self-Supervised Learning From Images With a Joint-Embedding Predictive Architecture},
  booktitle = {Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)},
  month     = {June},
  year      = {2023},
  pages     = {15619--15629}
}
```
