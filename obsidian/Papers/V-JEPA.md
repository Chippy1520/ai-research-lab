---
generated_by: "build_obsidian_vault.py"
type: "paper-guide"
aliases: ["V-JEPA", "V-JEPA: predict the next motion in feature space, from video only"]
paper_slug: "vjepa"
source: "site/papers-vjepa.html"
live_url: "https://chippy1520.github.io/ai-research-lab/papers-vjepa.html"
tags: ["paper", "reading-guide"]
related_nodes: ["representation", "world-models"]
related_curriculum: ["Curriculum/Lessons/Day 07 - Information Theory & Representation.md", "Curriculum/Lessons/Day 26 - Self-Supervised Visual Representation Learning.md", "Curriculum/Lessons/Day 42 - World Models & Latent Imagination.md", "Curriculum/Lessons/Day 46 - Causal Representation Learning & Invariance.md"]
cssclasses: ["research-note", "paper-note"]
---

[[Home|Research Lab]]  /  [[Papers/Paper Guides|Paper Guides]]

# V-JEPA: predict the next motion in feature space, from video only

> [!paper] Research reading guide
> Complete reading guide for V-JEPA (Bardes et al., arXiv 2404.08471): feature prediction as a stand-alone objective for video representations.
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
> - Repository guide: `site/papers-vjepa.html`
> - [Open the published HTML guide](https://chippy1520.github.io/ai-research-lab/papers-vjepa.html)
> - Companion source: `papers/vjepa.md`

---

## How a person watches someone pour coffee with a hand in the way

A clip: kettle, mug, arm. For a few frames a sleeve occludes the mug. A video MAE would reconstruct those pixels. The question that matters on Something-Something-v2 is whether the pour continues (push vs pull), which lives in the motion of $E(y)$. V-JEPA masks a space–time tube and predicts those embeddings; it never decodes RGB.

> [!example] Step 01 — You
> **You:** You watch the visible parts of the clip as one moving picture, not 16 unrelated JPEGs.
>
> **The paper:** Video is tube-tokenised (space–time patches). The encoder is a ViT over those tokens. No frozen DINO image encoder is allowed — the abstract forbids it.

> [!example] Step 02 — You
> **You:** Someone covers the mug for a moment. You still know the pour is happening there .
>
> **The paper:** Mask a spatio-temporal region $y$. Context $x$ is the rest. Predictor $P_\phi(E_\theta(x), \Delta_y)$ is told the missing coordinates via $z \leftarrow \Delta_y$.

> [!example] Step 03 — You
> **You:** Your prediction is that liquid is still going into the mug, not an inpainted RGB of the hidden frames.
>
> **The paper:** L1 in feature space against an EMA teacher $\bar{E}_\theta(y)$ with stop-gradient. Eq. (1) in the PDF. L1, not I-JEPA’s L2 — they say L1 was more stable on video.

> [!example] Step 04 — You
> **You:** Later, without retraining your eyes, you can both name the action (Kinetics) and tell pushing from pulling (SSv2), and even recognise a still (ImageNet).
>
> **The paper:** Frozen backbone + attentive probe. Figure 1’s whole point: one encoder, motion and appearance, no end-to-end fine-tune required to make the claim.

The mapping *is* the method: mask a tube, predict $E(y)$, evaluate the frozen encoder. A video MAE can look sharp and still lose SSv2, because the loss rewarded pixel texture instead of motion in $E(\cdot)$.

## The paper, in order — every section

Open [arXiv 2404.08471](https://arxiv.org/pdf/2404.08471). Code line in the PDF: github.com/facebookresearch/jepa.

### Abstract

Feature prediction as a stand-alone unsupervised objective on video. No pretrained image encoder, text, negatives, reconstruction, or other supervision. 2M videos from public datasets. Frozen evaluation on image and video tasks. Largest: ViT-H/16 → 81.9% K400, 72.2% SSv2, 77.9% ImageNet-1K.

### Figure 1

Two axes: motion (SSv2) vs appearance (K400), frozen. V-JEPA sits up-right. DINOv2-like image models sit high on appearance and drop on SSv2. That scatter is the paper’s argument in one glance.

### §1 Introduction

Humans map retina spikes into objects and global motion (Spelke). Predictive-feature principle (Rao & Ballard): temporally adjacent representations should predict each other. Question they isolate: *how effective is feature prediction as a stand-alone objective for unsupervised learning from video with modern tools* (ViT, masked modelling, JEPA, bigger data)?

Three findings to score: (1) frozen versatility, +6% on SSv2 vs methods they consider, competitive on K400 where image models already excel; (2) beats pixel prediction under frozen/attentive probe, competitive under full fine-tune, shorter schedule; (3) more label-efficient as you remove labels (their Table 7).

### §2 Related works

Slow features / SFA: make nearby frames identical. Predictive features: a predictor from $t$ to $t{+}1$, often on a frozen encoder or with contrastive negatives. JEPA (LeCun 2022) + I-JEPA (images) + data2vec (audio/vision). Video MAEs (Tong et al. VideoMAE, Feichtenhofer MAE): pixel/tube reconstruction. V-JEPA’s bet: same mask game, latent loss, video from scratch.

### §3 Methodology: Video-JEPA

![V-JEPA joint-embedding predictive architecture](https://arxiv.org/html/2404.08471v1/decoder-color.png)

**Paper Figure 2 flavour.** Predict $E(y)$ from $E(x)$ given $z$. $z$ carries the spatio-temporal location of the missing tube. If this drawing has a pixel decoder, you are in the VideoMAE column of their comparison, not here.

#### §3.1 Training objective — Eq. (1)

Naive $\\|P\_\phi(E\_\theta(x),\Delta\_y) - E\_\theta(y)\\|\_1$ collapses to a constant. They use
$$
\min\_{\theta,\phi}\ \big\| P\_\phi(E\_\theta(x),\Delta\_y) - \mathrm{sg}(\bar{E}\_\theta(y)) \big\|\_1
$$
EMA teacher $\bar{E}$, stop-gradient, L1 (I-JEPA used L2; they found L1 more stable). Theoretical aside: BYOL-style argument adapted to L1, one-dimensional sketch in the PDF — read it if you need why EMA does not collapse, skip if you already believe Grill et al.

#### §3.2 Prediction task

$y$ is a masked spatio-temporal block (or several). $x$ is the complement. $z=\Delta\_y$ is positions. Multi-block, as in I-JEPA, extended in time. Figure samples in the HTML: `assets/samples-v1.png`.

![V-JEPA masking samples on video](https://arxiv.org/html/2404.08471v1/assets/samples-v1.png)

**Masking samples.** Targets are tubes, not salt-and-pepper. Local texture should not be enough; you need the motion.

#### §3.3 Network parameterization

ViT over space–time patches. Predictor is a lighter transformer. Table 2 in the PDF lists widths / depths — copy from there if you re-implement, do not invent.

#### §3.4 Data and eval

2M videos, public mixtures (VideoMix2M in their notation). Downstream: K400, SSv2, IN1K, plus detection in the appendix. Two protocols: frozen + attentive probe, and end-to-end fine-tune. Attentive probe matters: average-pool linear probes understate video models that have no [CLS].

### §4 What matters

§4.1 Representations vs pixels: latent prediction wins frozen eval, similar fine-tune, shorter training. §4.2 Pretraining data mix — video diversity vs ImageNet-only. §4.3 Attentive probing is the fair frozen protocol. §4.4 How you sample $(x,y)$ (block size, duration) is load-bearing, same moral as I-JEPA Figure 4.

### §5 Comparison with prior work

Headline frozen ViT-H/16: **K400 81.9, SSv2 72.2, IN1K 77.9**. Pixel-prediction video MAEs lag on frozen SSv2. Image SSL (DINOv2) is strong on K400/IN1K and weaker on SSv2 — appearance without motion. Label-efficiency Table 7: drop labels, the gap vs pixel models grows. Fine-tune tables in the appendix: competitive, not a massacre. Quote the protocol (frozen vs 100% fine-tune) every time you repeat a number.

### §6 Evaluating the predictor

They probe whether $P$ actually forecasts, not just whether $E$ is a good frozen backbone. Visualisations (Figure 6 in the PDF) decode predicted latents. Treat them as qualitative, like I-JEPA’s dog-head sketches.

### §7 Conclusion

Feature prediction is a sufficient stand-alone objective for video with 2024 tools. Frozen versatility is the product. Next paper in the family (V-JEPA 2) scales data to 1M hours and adds an action-conditioned planner.

### What the paper does *not* claim

No robot. No LLM alignment. No 1M-hour dataset yet. Not “beats every video foundation model ever.” SSv2 +6% is versus the methods in their tables, under their probe.

## The engineering tension

| Alternative | Representation and consequence |
|---|---|
| **Video MAE** | Video MAE Reconstruct masked RGB tubes. Need long schedules. Frozen probe sees a texture specialist. SSv2 (push vs pull) suffers. |
| **V-JEPA** | V-JEPA Reconstruct masked features . Shorter schedule. Frozen backbone keeps motion. SSv2 72.2 with ViT-H/16, still 81.9 on K400. |

| Alternative | Representation and consequence |
|---|---|
| **Frozen DINOv2 on video** | Frozen DINOv2 on video Excellent “what.” Weak “how it moved.” Kinetics can be solved as a bag of objects. SSv2 cannot. |
| **Train on video, predict features** | Train on video, predict features One encoder for both axes in Figure 1. That is why they forbid a pretrained image encoder in the abstract. |

## Prerequisites

1. **01**

   #### I-JEPA

   Same three networks (context, EMA target, predictor). Read [[Papers/I-JEPA|I-JEPA]] Figure 3 before this Figure 2.
2. **02**

   #### Space–time patches

   A token is a cube of pixels across a few frames, not a 16×16 still. VideoMAE already taught this; V-JEPA keeps the tokenisation and changes the loss.
3. **03**

   #### Frozen vs fine-tune

   If you only compare fine-tunes, pixel models look closer. The paper’s claim is the frozen column.

> [!video] 3Blue1Brown — Attention in transformers
> [Watch video](https://www.youtube.com/watch?v=eMlx5fFNoYc)
>
> Prerequisite: attention, not a V-JEPA recap. The video ViT is this mechanism on tube tokens.

> [!video] World Models explained
> [Watch video](https://www.youtube.com/watch?v=b1roEd6liWI)
>
> World-model intuition. V-JEPA is still only the encoder+predictor, not the actor. The actor arrives in V-JEPA 2-AC.

## Knowledge graph

```text
I-JEPA (images)
   │
   ├─ VideoMAE tokenisation (tubes)
   ├─ BYOL EMA + L1
   └─ 2M unlabeled clips
          │
          ▼
       V-JEPA
          ├─ frozen K400 / SSv2 / IN1K
          └─ predictor as primitive dynamics
                │
                ▼
             V-JEPA 2
```

> [!graph] Concept flow
> **I-JEPA · VideoMAE tubes**
> ↓
> **L1 + EMA · multi-block tubes · frozen probe**
> ↓
> **V-JEPA (this paper)**

## Architecture

> [!flow] Architecture / data flow
> **Clip → space–time tokens** — 2M public videos
> ↓ mask tubes y, keep context x
> **E_θ(x)** + **Ē_θ(y) EMA, sg**
> ↓ z = Δy
> **P_φ(E(x), z)**
> ↓ L1
> **frozen E_θ → K400 / SSv2 / IN1K**

## Results, honestly

| Fact from the paper | What it means |
| --- | --- |
| ViT-H/16 frozen: K400 81.9, SSv2 72.2, IN1K 77.9 | The abstract triple. Appearance *and* motion, one backbone, trained only on video. |
| +6% SSv2 vs methods they consider | The motion-understanding headline. Check Table 6 for the exact baselines. |
| Frozen > pixel models; fine-tune ≈ | Do not advertise a fine-tune blowout. The paper does not. |
| Label-efficiency gap grows as labels drop | Table 7. Feature prediction helps when you cannot fine-tune on a lot of SSv2 labels. |
| No image-encoder init | A constraint, not a trick. If you cheat with DINOv2 init you are not reproducing this paper. |

## Worked intuition

Take 16 frames at 224². Tube tokens $2\times 16\times 16$ pixels → about $8\times 14\times 14 \approx 1568$ tokens (order-of-magnitude; use the paper’s exact tube size when coding). Mask ~50% as a few large tubes. Encoder sees the rest. Predictor emits one vector per masked token. Teacher (EMA) sees the full clip, stop-grad. L1. After pretrain, freeze $E\_\theta$, train a tiny attentive pool + linear head on K400. If SSv2 is also high, you did not just learn “there is a kettle.”

## Caveats

- 2M videos is already a cluster job. The method is simple; the data is not.
- Attentive probe ≠ linear probe on a [CLS]. Mixing those numbers is how people “beat” this paper on Twitter.
- Predictor visualisations are decoded with an extra network. Not evidence of a physics simulator.
- No actions in $z$. $z$ is only *where/when* the hole is. Actions arrive in V-JEPA 2-AC.

## Study plan

80 minutes: coffee case (10) → Eq. (1) and why L1+EMA (15) → Figure 1 scatter (10) → abstract triple + frozen vs fine-tune (20) → masking samples (10) → [[Papers/V-JEPA 2|V-JEPA 2]] planning teaser (15).

## Primary sources

- Paper: [arXiv:2404.08471](https://arxiv.org/abs/2404.08471) · [HTML v1](https://arxiv.org/html/2404.08471v1)
- Code: [github.com/facebookresearch/jepa](https://github.com/facebookresearch/jepa)
- Official blog: [Meta AI — V-JEPA](https://ai.meta.com/blog/v-jepa-yann-lecun-ai-model-video-joint-embedding-predictive-architecture/)
- Previous: [[Papers/I-JEPA|I-JEPA]] · next: [[Papers/V-JEPA 2|V-JEPA 2]]

**BibTeX**

```
@article{bardes2024vjepa,
  title={Revisiting Feature Prediction for Learning Visual Representations from Video},
  author={Bardes, Adrien and Garrido, Quentin and Ponce, Jean and Chen, Xinlei and Rabbat, Michael and LeCun, Yann and Assran, Mahmoud and Ballas, Nicolas},
  journal={arXiv preprint arXiv:2404.08471},
  year={2024}
}
```
