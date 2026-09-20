---
generated_by: "build_obsidian_vault.py"
type: "paper-guide"
aliases: ["V-JEPA 2", "V-JEPA 2: watch a million hours, then plan a grasp in latent space"]
paper_slug: "vjepa2"
source: "site/papers-vjepa2.html"
live_url: "https://chippy1520.github.io/ai-research-lab/papers-vjepa2.html"
tags: ["paper", "reading-guide"]
related_nodes: ["representation", "world-models"]
related_curriculum: ["Curriculum/Lessons/Day 07 - Information Theory & Representation.md", "Curriculum/Lessons/Day 26 - Self-Supervised Visual Representation Learning.md", "Curriculum/Lessons/Day 42 - World Models & Latent Imagination.md", "Curriculum/Lessons/Day 46 - Causal Representation Learning & Invariance.md"]
cssclasses: ["research-note", "paper-note"]
---

[[Home|Research Lab]]  /  [[Papers/Paper Guides|Paper Guides]]

# V-JEPA 2: watch a million hours, then plan a grasp in latent space

> [!paper] Research reading guide
> Complete reading guide for V-JEPA 2 (Assran et al., arXiv 2506.09985): 1M-hour video JEPA, action-conditioned world model, zero-shot Franka planning.
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
> - Repository guide: `site/papers-vjepa2.html`
> - [Open the published HTML guide](https://chippy1520.github.io/ai-research-lab/papers-vjepa2.html)
> - Companion source: `papers/vjepa2.md`

---

## How a person picks up a mug they have never seen, in a kitchen they have never been in

Stage 1: action-free JEPA on >1 million hours of internet video — the encoder $E$ learns $P(E(x),z)\approx E(y)$ with no robot. Stage 2: freeze $E$, train a 300M action-conditioned predictor on <62 hours of unlabeled Droid. At test: image goal $g$, sample action chunks, roll the latents, pick the chunk whose predicted embedding is closest to $E(g)$, execute $a\_0$ (MPC). No task reward, no data from the test Franka.

> [!example] Step 01 — You
> **You:** Years of watching: objects persist, hands grasp, liquids pour. You were not labelled.
>
> **The paper:** Stage 1 — V-JEPA 2. Action-free mask-denoising JEPA on >1M hours of internet video plus images. Encoder up to ~1B parameters. Same game as V-JEPA, scaled.

> [!example] Step 02 — You
> **You:** A weekend of actually moving: if I send this joint command, the scene changes like that .
>
> **The paper:** Stage 2 — V-JEPA 2-AC. Freeze $E$. Train a 300M block-causal transformer that predicts the next frame’s embedding given past embeddings and the action. <62 hours of unlabeled Droid robot video. No reward.

> [!example] Step 03 — You
> **You:** Someone shows a goal photo. You mentally try reaches until the imagined view looks like the photo.
>
> **The paper:** Planning. Sample action sequences, roll out $\hat{s}_{t+1}=P(\hat{s}_t, a_t)$ in latent space, score distance to $E(\text{goal image})$, pick the best first action (MPC). Figure of the loop: vjepa2-mpc.png .

> [!example] Step 04 — You
> **You:** You do this in a new building, with a mug the weekend never contained, without a new round of practice.
>
> **The paper:** Zero-shot Franka, two labs, novel objects. No data from those robots, no task-specific training. Prehensile grasp / pick-and-place from a monocular RGB camera.

The mapping *is* the two-stage training: watch the world at internet scale, then fit a cheap action-conditioned predictor on a little interaction, then plan. That is LeCun 2022’s actor, finally on hardware — with an image goal instead of his intrinsic cost module.

## The paper, in order — every section

Open [arXiv 2506.09985](https://arxiv.org/pdf/2506.09985) (48 pages, 19 figures). HTML figures below are the paper’s own.

### Abstract

Learn to understand and act largely by observation. Combine internet-scale video with a small amount of interaction. Stage 1: action-free V-JEPA 2 on >1M hours. Motion: 77.3 top-1 on SSv2. Anticipation: 39.7 recall-at-5 on Epic-Kitchens-100 (SOTA, 44% relative over previous best). Align with an 8B LLM: 84.0 PerceptionTest, 76.9 TempCompass, plus MVP 44.5, TemporalBench 36.7, TOMATO 40.3. Stage 2: V-JEPA 2-AC on <62 h Droid, zero-shot Franka pick-and-place with image goals, no in-lab data, no task reward.

### Figure 1 — overview

![V-JEPA 2 overview: pretrain, probes, LLM align, action-conditioned planning](https://arxiv.org/html/2506.09985v1/flowchart.png)

**Paper Figure 1 / flowchart.** Left: mask-denoise video → encoder. Branches: classification probes, LLM alignment for VideoQA, freeze encoder and train AC predictor for robot MPC. If your mental model has one loss that does all of this, redraw. It is staged.

### §1 Introduction

Humans integrate sensation into a world model and use it to plan (Sutton & Barto; Ha & Schmidhuber; Wolpert). Interaction-only world models do not scale — not enough real robot hours. Video-generation world models can look pretty and still be too slow to plan in (you would generate RGB at every candidate action). JEPA predicts in $E(\cdot)$, so planning is cheap and the encoder may ignore grass blades.

Four claims: (understanding / probe) SSv2 77.3; (understanding / VQA) SOTA in the 8B class on several temporal benchmarks without language supervision in the video encoder; (prediction) EK100 39.7 R@5, +44% relative; (planning) AC model from 62 h Droid, zero-shot Franka.

Roadmap they announce: §2 pretrain, §3 AC model, §4 robot, §5 probes, §6 anticipation, §7 VQA, §8 related, §9 close. That is the PDF order. Follow it; do not read the robot section as if the VQA numbers proved the grasp.

### §2 V-JEPA 2 — scaling SSL video

#### §2.1 Methodology

Mask-denoising in feature space, as V-JEPA. Patchify clip → drop tokens → encoder on the rest → concat learnable mask tokens with positions → predictor → L1 to teacher targets. Teacher is EMA. Scaling ingredients beyond Bardes et al. 2024 live in §2.2–2.4 (data, resolution, duration, model size). Copy those tables from the PDF when reproducing; do not invent a recipe from this sentence.

![V-JEPA 2 pretraining: mask denoising in representation space](https://arxiv.org/html/2506.09985v1/vjepa2-abstract-new.png)

**Pretrain cartoon.** Same JEPA as V-JEPA, internet scale. $z$ is still mask position, not yet an action.

#### §2.3 Dataset

>1 million hours of internet video + ~1M images. This is the number that changed from V-JEPA’s 2M clips. Diversity and duration, not a new loss.

#### §2.4 Recipe

Progressive scaling: model size up to 1B, longer clips, higher resolution. The paper’s ablation claim: scaling SSL video pretraining improves motion understanding and anticipation, not just IN1K.

### §3 V-JEPA 2-AC

![V-JEPA 2-AC action-conditioned world model](https://arxiv.org/html/2506.09985v1/vjepa2-ac-abstract-new.png)

**AC cartoon.** Frozen $E$ from stage 1. New predictor $P(s\_t, a\_t)\to s\_{t+1}$ in latent space. Actions are robot controls from Droid, not internet-video verbs.

#### §3.1 Training

300M-parameter transformer, **block-causal** attention, autoregressive in time: each frame embedding may look at past frames and the action that was applied. Unlabeled Droid trajectories: images + actions, no language, no reward. <62 hours. Because $E$ is frozen, this stage cannot invent a new visual system; it can only learn dynamics *in the coordinates $E$ already provides*.

#### §3.2 Inferring actions by planning

Not imitation of Droid’s actions at test time. At test time you have a goal image. Sample or optimise $a\_{0:H}$, roll out latents, minimise $\| \hat{s}\_H - E(g) \|$ (plus regularisers the PDF specifies). Receding horizon: execute $a\_0$, replan. That is classical MPC sitting on a latent world model.

### §4 Planning — zero-shot robot control

![V-JEPA 2-AC model-predictive control loop](https://arxiv.org/html/2506.09985v1/vjepa2-mpc.png)

**MPC loop.** RGB → $E$ → plan actions in $E$ → send to Franka → new RGB. Goal is an image, not a reward classifier.

#### §4.1 Setup

Franka arms, two different labs, monocular RGB, image subgoals for grasp / pick-and-place. Novel objects. No demonstrations from these robots.

#### §4.2 Results

They report success on prehensile tasks under that protocol. Read the exact success-rate table in the PDF before quoting a percentage — the abstract claims feasibility (“successfully handles”), not 99% warehouse picking. Trajectory figures (`traj-pnp-*.jpg`) are qualitative.

#### §4.3 Limitations

Read this subsection. Typical failures for latent MPC: goal image underspecifies (which mug?), long-horizon compounding in $P$, contact-rich physics $E$ never represented, camera/robot shift beyond Droid. Do not skip it to make the Franka GIF the paper.

### §5 Understanding — probe-based classification

SSv2 **77.3** top-1 with an attentive probe (abstract). Compare to V-JEPA’s 72.2 ViT-H/16: scaling data/model moved motion understanding. Appearance tasks remain strong; the point of §5 is “frozen encoder, many tasks,” not a new loss.

### §6 Prediction — action anticipation

Epic-Kitchens-100: **39.7 recall-at-5**, SOTA, 44% relative over previous best, attentive probe. Anticipation is the closest frozen proxy to “world model” they have without a robot: given the past, which action is coming.

### §7 Video question answering

Align frozen (or lightly adapted) V-JEPA 2 encoder with an 8B LLM via visual instruction tuning (§7.1). Encoder was *not* trained with language. They treat that as a feature: conventional wisdom said you need a vision encoder trained on captions. Numbers at 8B class: PerceptionTest **84.0**, TempCompass **76.9**, MVP 44.5 paired acc, TemporalBench 36.7, TOMATO 40.3. §7.2 vs image encoders, §7.3 scale encoder size and resolution, §7.4 scale data. These numbers do not imply the Franka can answer questions.

![V-JEPA 2 qualitative visualisations](https://arxiv.org/html/2506.09985v1/visualizations_2.png)

**Qualitative visualisations.** Use them as “what the latent attends to,” not as proof of planning.

### §8 Related work

World models from interaction (Dreamer, TD-MPC), video generation for control, V-JEPA 1, VLAs. The contrast they want: generate pixels vs predict $E$; train only on robot hours vs pretrain on internet video then a little Droid.

### §9 Conclusion

SSL from web video + a little interaction can yield a world model that understands, predicts, and plans. Hierarchical JEPA (LeCun’s stacked timescales) is still not trained here — two stages, one encoder timescale.

### What the paper does *not* claim

Not a VLA (no language in the control loop). Not reward-free in LeCun’s intrinsic-cost sense — the goal is an image you provide. Not trained on the deployment robots, but also not “works in any kitchen.” Not 1M hours of *robot* data. Not hierarchical JEPA.

## The engineering tension

| Alternative | Representation and consequence |
|---|---|
| **Train a world model only on robot hours** | Train a world model only on robot hours Droid is tens of hours, not a childhood. The visual system never sees a mug that was not in the lab. Planning is then overfitting to that room. |
| **Internet video, then a little Droid** | Internet video, then a little Droid $E$ already knows objects and motion. AC only has to learn how Franka-like actions move that latent. 62 hours become plausible. |

| Alternative | Representation and consequence |
|---|---|
| **Plan by generating video** | Plan by generating video Each candidate action sequence is a video. Too slow for MPC at control rate. Also wastes capacity on unneeded pixels. |
| **Plan in $E(\cdot)$** | Plan in $E(\cdot)$ Rollouts are transformer steps on embeddings. Goal score is a latent distance. That is why a 300M $P$ can sit in a control loop. |

## Prerequisites

1. **01**

   #### V-JEPA

   Stage 1 is V-JEPA scaled. If Eq. (1) from [[Papers/V-JEPA|V-JEPA]] is fuzzy, §2 here is unreadable.
2. **02**

   #### Model-predictive control

   Optimise a short action sequence, execute the first, repeat. No new ML — classical. The novelty is the model $P$ being a latent JEPA.
3. **03**

   #### World models

   Ha & Schmidhuber: learn $s\_{t+1}=f(s\_t,a\_t)$, plan inside it. JEPA removes the pixel decoder.

> [!video] World Models explained
> [Watch video](https://www.youtube.com/watch?v=b1roEd6liWI)
>
> Prerequisite: imagine-then-act. V-JEPA 2-AC is that loop with $f$ in embedding space.

> [!video] 3Blue1Brown — Transformers
> [Watch video](https://www.youtube.com/watch?v=wjZofJX0v4M)
>
> The AC predictor is a block-causal transformer. This is the mechanism, not a recap of the paper.

## Knowledge graph

```text
LeCun JEPA 2022
   │
   ├─ I-JEPA → V-JEPA
   │         │
   │         ▼
   │      V-JEPA 2 encoder  (1M hours)
   │         │
   │         ├─ probes (SSv2, EK100)
   │         ├─ + LLM  (VideoQA)
   │         └─ freeze
   │              │
   │              ▼
   │         V-JEPA 2-AC  (62 h Droid)
   │              │
   │              ▼
   │         MPC on Franka
   └─ Ha world models / MPC
```

> [!graph] Concept flow
> **V-JEPA · 1M h video**
> ↓
> **V-JEPA 2 encoder**
> ↓
> **probes / VQA · AC predictor**
> ↓
> **zero-shot Franka MPC**

## Two-stage architecture

> [!flow] Architecture / data flow
> **Internet video >1M h** — action-free
> ↓ mask-denoise JEPA
> **Encoder E up to 1B** — frozen after stage 1
> ↓
> **Attentive probes** + **+ 8B LLM** + **AC predictor 300M** — block-causal, Droid 62 h
> ↓ image goal
> **MPC → Franka**

## Planning / MPC

State $s\_t = E(\text{frame}\_t)$. Dynamics $\hat{s}\_{t+1} = P(\hat{s}\_t, a\_t)$. Goal $s\_g = E(\text{goal image})$. Horizon $H$ short enough that $P$ does not drift off a table. Objective roughly $\sum\_t \| \hat{s}\_t - s\_g \|$ plus action smoothness (see PDF for the exact regularisers). Receding horizon. Subgoals matter: a single goal image of “mug in the rack” is a long-horizon problem $P$ may not hold; the paper uses subgoals for grasp then place.

## Results, honestly

| Fact from the paper | What it means |
| --- | --- |
| SSv2 77.3 top-1 (probe) | Motion understanding after scaling. V-JEPA was 72.2 at ViT-H/16. |
| EK100 39.7 R@5, +44% relative | Frozen anticipation SOTA. Closest non-robot “prediction” number. |
| PerceptionTest 84.0, TempCompass 76.9 (8B) | VideoQA after LLM alignment. Encoder itself had no language loss. |
| <62 h Droid → AC model | Interaction data is small *because* $E$ already exists. Not “62 h from scratch.” |
| Zero-shot Franka, two labs, image goals | The LeCun-loop result. Quote success tables from §4, not the GIF. |
| No in-lab robot data, no task reward | True under their protocol. Goal images are still supervision of a kind. |

Three papers’ numbers are not interchangeable. 81.1 linear IN-1K is I-JEPA. 72.2 SSv2 is V-JEPA ViT-H/16. 77.3 SSv2 is V-JEPA 2. Mixing them is how a blog invents a model that does not exist.

## Worked intuition

Stage 1: 16-frame clip, tube tokens, mask, L1 in $E$, as V-JEPA, but the data loader now spans a million hours. Stage 2: a Droid episode is $(o\_0,a\_0,o\_1,a\_1,\ldots)$. Encode every $o\_t$ once with frozen $E$ → $s\_t$. Train $P$ so $P(s\_t, a\_t)\approx s\_{t+1}$ (block-causal over the window). At test: current camera frame $o$, goal photo $g$. Sample $K$ action chunks of length $H$, roll $P$, score $\|P^{\circ H}(E(o), a\_{0:H}) - E(g)\|$, execute $a\_0^\star$, repeat. The Franka never sees a pixel decoder.

## Caveats

- Image goals are a crutch relative to LeCun’s intrinsic cost. Someone still has to specify the photo.
- Zero-shot is “zero data from these two labs,” not “any morphology, any camera.”
- VQA SOTA is at the 8B language-model class, after alignment. It is not the robot stack.
- Hierarchical JEPA (multiple timescales) remains a drawing in the 2022 PDF.
- Contact, occlusion, and long-horizon rearrangement are exactly where latent MPC usually dies — §4.3.

## Study plan

90 minutes: Franka mug case (10) → Figure 1 flowchart until the three branches are distinct (10) → §2 scaling vs V-JEPA (15) → §3 AC + MPC diagram (20) → §4 limitations with the success table (15) → abstract numbers for SSv2 / EK100 / VQA, each with protocol (15) → skim [[Papers/JEPA|LeCun 2022]] six-module list and mark which boxes are still empty (5).

## Primary sources

- Paper: [arXiv:2506.09985](https://arxiv.org/abs/2506.09985) · [HTML v1](https://arxiv.org/html/2506.09985v1)
- Code: [github.com/facebookresearch/vjepa2](https://github.com/facebookresearch/vjepa2)
- Official blog: [Meta AI — V-JEPA 2](https://ai.meta.com/blog/v-jepa-2-world-model-benchmarks)
- Family: [[Papers/JEPA|JEPA 2022]] · [[Papers/I-JEPA|I-JEPA]] · [[Papers/V-JEPA|V-JEPA]]

**BibTeX**

```
@article{assran2025vjepa2,
  title={V-JEPA 2: Self-Supervised Video Models Enable Understanding, Prediction and Planning},
  author={Assran, Mahmoud and Bardes, Adrien and Fan, David and Garrido, Quentin and Howes, Russell and Komeili, Mojtaba and Muckley, Matthew and Rizvi, Ammar and Roberts, Claire and Sinha, Koustuv and others},
  journal={arXiv preprint arXiv:2506.09985},
  year={2025}
}
```
