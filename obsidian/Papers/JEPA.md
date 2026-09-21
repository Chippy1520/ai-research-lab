---
generated_by: "build_obsidian_vault.py"
type: "paper-guide"
aliases: ["JEPA", "JEPA: train the world model to predict $E(y)$, not $y$"]
paper_slug: "jepa"
source: ["site/papers-jepa.html", "papers/jepa.md"]
content_mode: "local"
tags: ["paper", "reading-guide"]
related_nodes: ["representation", "world-models"]
related_curriculum: ["Curriculum/Lessons/Day 07 - Information Theory & Representation.md", "Curriculum/Lessons/Day 26 - Self-Supervised Visual Representation Learning.md", "Curriculum/Lessons/Day 42 - World Models & Latent Imagination.md", "Curriculum/Lessons/Day 46 - Causal Representation Learning & Invariance.md"]
cssclasses: ["research-note", "paper-note"]
---

[[Home|Research Lab]]  /  [[Papers/Paper Guides|Paper Guides]]

# JEPA: train the world model to predict $E(y)$, not $y$

> [!paper] Research reading guide
> Complete reading guide for Yann LeCun’s 2022 position paper A Path Towards Autonomous Machine Intelligence — the Joint Embedding Predictive Architecture (JEPA).
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

> [!source] Local reconstruction and provenance
> - This note contains the complete recreated reading guide; no published mirror is required.
> - Canonical editorial source: `site/papers-jepa.html`
> - Companion source: `papers/jepa.md`
> - Local figures: `_attachments/Papers/jepa/`
> - Primary papers, repositories, and videos remain linked as evidence.

---

## Reach for a mug: what you predict, and what a generative model predicts

You decide to pick up a mug. The facts that matter are pose and contact: the mug stays put, the handle is on the left, the counter is solid. A video generator / MAE is trained to output the next RGB frame (or its pixels). You are not. A JEPA is trained to output a vector $E(y)$ from which those facts can still be read, and from which unpredictable texture can be dropped. That is the claim of this position paper.

> [!example] Step 01 — You
> **You:** You encode the scene as a handful of facts (counter, mug, kettle pose). You do not store a pixel buffer.
>
> **The paper:** Perception module. Embed the sensory stream into a representation $s_t$ that already threw away unpredictable clutter.

> [!example] Step 02 — You
> **You:** You remember: I just walked through a doorway; the mug was on the left. You do not replay the last minute of video.
>
> **The paper:** Short-term memory. A running latent of recent $s_t$, not a pixel buffer.

> [!example] Step 03 — You
> **You:** You predict the next state of the mug, not a new photograph of the kitchen.
>
> **The paper:** World model = JEPA. Encode the scene as $E(x)$, encode a later or hidden part as $E(y)$, train a predictor so $P(E(x), z) \approx E(y)$. The loss never looks at pixels of $y$. $z$ says which hidden part / which future you are asking about.

> [!example] Step 04 — You
> **You:** You feel a cost: do not burn your hand; do not knock the cat. Nobody labelled those as rewards in this kitchen.
>
> **The paper:** Cost / energy module with intrinsic drives (energy, uncertainty, discomfort) plus a few hardwired terms. Behaviour is not “maximise a scalar reward the experimenter wrote.”

> [!example] Step 05 — You
> **You:** You pick an action by mentally trying a few reaches until the predicted cost is low, then you move.
>
> **The paper:** Actor proposes actions; planning is search in latent space through the world model. Configurator sets which level of the hierarchy is running (grasp vs walk-to-counter).

The mapping *is* the architecture: perception → memory → JEPA world model ($P(E(x),z)\approx E(y)$) → cost → actor. I-JEPA trains that predictor on still images. V-JEPA trains it on video. V-JEPA 2 adds the actor’s planning loop on a Franka.

## The paper, in order — every section

Open [OpenReview PDF BZ5a1r-kVsf](https://openreview.net/pdf?id=BZ5a1r-kVsf) (62 pages, version 0.9.2). This is a *position* paper. There are no ImageNet tables. Do not look for them.

### Abstract

Three questions: how could machines learn as efficiently as humans and animals? How could they reason and plan? How could they learn representations of percepts and action plans at multiple levels of abstraction, so they can predict and plan at multiple time horizons?

The proposed answer is an architecture plus training paradigms: a configurable predictive world model, behaviour driven by intrinsic motivation, and hierarchical joint-embedding architectures trained with self-supervised learning.

Keywords he lists so you know the vocabulary pile: energy-based models, world models, joint embedding architecture, intrinsic motivation, SSL.

### §1 Prologue

He says this is not a technical nor scholarly paper in the traditional sense. It is a vision for machines that learn more like animals, that can reason and plan, whose behaviour is driven by intrinsic objectives rather than hard-wired programs, external supervision, or external rewards. Read that sentence twice: the later I-JEPA paper is allowed to have no labels and no SimCLR colour jitter because this prologue already forbade those as the path.

### Stated contributions (early in the PDF)

1. A cognitive architecture for autonomous intelligence (the six modules).
2. **JEPA and Hierarchical JEPA** — a non-generative architecture for predictive world models that learn a hierarchy of representations (his Figures 12 and 15).
3. A non-contrastive SSL paradigm that produces representations that are simultaneously informative and predictable (his Figure 13; the VICReg family is the working example).

### Why not generative models / LLMs as the world model

A *generative* world model (MAE on images, a video generator, an LLM that emits tokens) is trained to reconstruct the observation $y$ itself. If $y$ is an image, that means pixels. Most of those pixels are unpredictable — leaves in wind, steam, sensor noise — so the model spends capacity on texture it cannot use for planning. LeCun’s claim is that animals (and a useful robot) do not do that. A JEPA predicts $E(y)$, a vector that is allowed to drop anything the encoder decides is noise. Planning then searches in that vector space, not in image space. That is the technical content of the position paper; I-JEPA §2 draws it as three energy-based diagrams.

LLMs, in this document, are useful but are not a world model of the physical world: they predict tokens, not latent states of a kitchen. Do not over-read a 2022 position paper as a 2026 LLM takedown. The engineering content is “predict $E(y)$ from $E(x)$, conditioned on $z$.”

### Energy-based models (the maths he actually uses)

Compatible pair $(x,y)$ should have low energy $F(x,y)$; incompatible pairs high energy. JEA (joint embedding architecture, SimCLR/BYOL/VICReg): $F = D(E\_x(x), E\_y(y))$. Generative: $F = D(y, \mathrm{Dec}(E(x), z))$. JEPA: $F = D(E\_y(y), P(E\_x(x), z))$. Same energy idea, loss in latent space, extra variable $z$ that tells the predictor *which* $y$ to aim at (mask location, future time, action).

### The six-module agent

Configurator, perception, world model, cost, actor, short-term memory. Perception and world model are JEPAs (possibly stacked). The configurator modulates them so the same hardware can plan a grasp at 200 ms and a walk across the room at 20 s. Cost is not a sparse external reward; it is a differentiable energy the actor minimises by thinking ahead through the world model.

### Hierarchical JEPA

Low level: fast, concrete, maybe closer to pixels. High level: slow, abstract, good for long-horizon planning. Each level predicts at its own timescale. This is the piece *none* of I-JEPA / V-JEPA / V-JEPA 2 fully trains. They are single-level JEPAs. When someone says “LeCun’s JEPA,” check whether they mean this hierarchy or the single predictor in I-JEPA Figure 3.

### Training / collapse

Joint embedding methods collapse if you only pull positives together. Contrastive negatives, VICReg variance-covariance, clustering, or an EMA teacher (BYOL) are the collapse brakes. I-JEPA and V-JEPA pick the EMA teacher. The position paper prefers non-contrastive (no need to define “incompatible” images).

### What the paper does *not* claim

No new ImageNet number. No trained weights. No proof that JEPA beats MAE. No robot demo. Those arrive in 2023–2025. If you only need the trained image model, skip to [[Papers/I-JEPA|I-JEPA]].

## The engineering tension

SSL in vision in 2022 is a fork: (A) invariance methods that need a hand-written list of “this crop is the same image,” which do not travel to video or audio cleanly; (B) MAE-style pixel reconstruction, which travels but learns a lot of texture. JEPA is the bet that you can keep MAE’s masking (so no SimCLR recipe) and still get semantic features by moving the loss into embedding space. In the kitchen: you want a vector that still says “mug on the left,” not a reconstruction of the steam.

| Alternative | Representation and consequence |
|---|---|
| **Naive world model** | Naive world model Decode the next RGB frame. Capacity goes into leaves and specularities. Planning a grasp means generating a video. Expensive, and most of the video is irrelevant. |
| **JEPA world model** | JEPA world model Encode $x$ and $y$. Predict $E(y)$ from $E(x)$ given $z$. The encoder may delete steam. Planning is search in $E(\cdot)$, which is what V-JEPA 2-AC later does on a Franka. |

## Prerequisites

1. **01**

   #### What a representation is for

   If “embedding” is still a vibe, the rest of JEPA is word salad. You need: a vector that is useful for later tasks, not a compressed JPEG.
2. **02**

   #### Self-supervised learning, two families

   Invariance (SimCLR / DINO / VICReg) versus reconstruction (MAE / BERT). JEPA is a third cartoon that looks like MAE but loses like DINO.
3. **03**

   #### World models as “imagine then act”

   Ha & Schmidhuber 2018 is the named ancestor for “train a model of the world, then plan inside it.” JEPA is that idea with the decoder ripped out.

> [!video] 3Blue1Brown — But what is a neural network?
> [Watch video](https://www.youtube.com/watch?v=aircAruvnKk)
>
> Why this video: the prerequisite, not this paper. What an embedding layer even is.

> [!video] World Models explained
> [Watch video](https://www.youtube.com/watch?v=b1roEd6liWI)
>
> Ha & Schmidhuber lineage: VAE + RNN world model. JEPA’s move is to drop the pixel decoder and predict $E(y)$ instead.

## Knowledge graph

```text
energy-based models
   │
   ├─ JEA (SimCLR / VICReg / DINO)  — invariant views
   ├─ generative (MAE / BERT)       — reconstruct y
   └─ JEPA                          — predict E(y) | E(x), z
          │
          ├─ I-JEPA   images, 2023
          ├─ V-JEPA   video, 2024
          └─ V-JEPA 2 video + robot planning, 2025
```

> [!graph] Concept flow
> **EBM / VICReg / MAE**
> ↓
> **perception · JEPA world model · cost**
> ↓
> **six-module agent (this paper)**

## Architecture

> [!flow] Architecture / data flow
> **Configurator** — which timescale / which expert
> ↓ modulates
> **Perception** — s_t = E(obs) + **Short-term memory** — recent s
> ↓
> **World model (JEPA)** — ŝ' = P(E(x), z) + **Cost / energy** — intrinsic + a few hardwired
> ↓
> **Actor** — search actions that lower predicted cost

LeCun’s agent. Only the world-model box is what I-JEPA trains. V-JEPA 2-AC is the first paper in this family that actually closes the actor loop on hardware.

> [!flow] Architecture / data flow
> **x** — context (visible) + **y** — target (hidden / future) + **z** — mask / time / action
> ↓
> **E_x(x)** + **E_y(y)** — often EMA teacher
> ↓
> **P(E_x(x), z) ≈ E_y(y)** — loss in embedding space

The JEPA cartoon every later paper redraws. $z$ is what makes this *predictive* rather than “make two views identical.”

## Results, honestly

| Fact from the paper | What it means |
| --- | --- |
| Zero trained models, zero tables | Do not cite this PDF for an ImageNet number. |
| JEPA defined as $P(E(x),z)\approx E(y)$ | This is the sentence I-JEPA implements with multi-block masking. |
| Hierarchical JEPA is proposed, not trained | Still mostly open. V-JEPA 2 has two *stages* (video then actions), not a trained hierarchy of timescales. |
| Behaviour from intrinsic cost, not RL reward | V-JEPA 2-AC still plans toward an *image goal*, not a learned intrinsic cost. The actor in this PDF is ahead of the engineering. |

If a blog says “JEPA achieves 81% on ImageNet,” they mean I-JEPA or V-JEPA. This document cannot achieve anything. It is a drawing.

## Worked intuition

Take a $224\times 224$ kitchen photo. Split it into $16\times 16$ ViT patches ($14\times 14 = 196$ tokens). Hide a $6\times 6$ block covering the mug (36 tokens). Context encoder sees the remaining tokens → a set of $d$-dimensional vectors. Predictor, told the $(x,y)$ positions of the missing block via $z$, emits 36 vectors. Target encoder (EMA) sees the *full* image and you read off those 36 locations. L2 or L1 between predicted and target vectors. Nobody asked you to paint mug pixels. If the 36 vectors mean “ceramic cylinder, handle on the left,” the loss is already happy — which is what you wanted in the kitchen.

## Caveats

- Position paper. Citing it as empirical evidence is a mistake.
- The six-module agent is a research programme, not a released stack.
- Collapse prevention is hand-waved toward VICReg / EMA; the later papers pick EMA and an asymmetric predictor.
- OpenReview, not arXiv. Link the PDF id `BZ5a1r-kVsf`, not a random mirror.

## Study plan

60–75 minutes: kitchen case (10) → abstract + JEPA cartoon vs MAE vs SimCLR (20) → six modules (15) → hierarchical JEPA and “what is not claimed” (10) → start [[Papers/I-JEPA|I-JEPA]] Figure 3 (15). Do not read all 62 pages of speculation on consciousness; the load-bearing pages are the energy cartoons and the module diagram.

## Primary sources

- Paper: [A Path Towards Autonomous Machine Intelligence](https://openreview.net/pdf?id=BZ5a1r-kVsf) (OpenReview, 2022-06-27, v0.9.2)
- Next engineering paper: [[Papers/I-JEPA|I-JEPA]] · [[Papers/V-JEPA|V-JEPA]] · [[Papers/V-JEPA 2|V-JEPA 2]]
- Official I-JEPA blog (Meta AI, 2023): [ai.meta.com/blog/yann-lecun-ai-model-i-jepa](https://ai.meta.com/blog/yann-lecun-ai-model-i-jepa/)

**BibTeX**

```
@article{lecun2022path,
  title={A Path Towards Autonomous Machine Intelligence},
  author={LeCun, Yann},
  journal={OpenReview},
  year={2022},
  note={Version 0.9.2, 2022-06-27, id BZ5a1r-kVsf}
}
```
