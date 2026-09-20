---
generated_by: "build_obsidian_vault.py"
type: "paper-guide"
aliases: ["VGGT", "VGGT: 3D from images without the SfM ritual"]
paper_slug: "vggt"
source: "site/papers-vggt.html"
live_url: "https://chippy1520.github.io/ai-research-lab/papers-vggt.html"
tags: ["paper", "reading-guide"]
related_nodes: ["vggt"]
---

# VGGT: 3D from images without the SfM ritual

> Complete reading guide for VGGT (CVPR 2025 Best Paper, arXiv 2503.11651): SfM vs feed-forward, alternating attention, over-complete 3D heads.

- **Canonical guide:** `site/papers-vggt.html`
- **Live guide:** https://chippy1520.github.io/ai-research-lab/papers-vggt.html
- **Companion source:** `papers/vggt.md`

## Connected concepts

- [[Mind Map/Nodes/vggt|vggt]]

---

## How a person builds a room in their head

You walk into a messy office with a phone and want cameras, depth, and correspondences for the desk. Classical SfM does that as a pipeline: match, triangulate, bundle-adjust, then maybe dense stereo. VGGT is one transformer: one forward pass emits cameras, depth, point maps, and tracks. No essential-matrix layer in the middle.

01

#### You

Look at each photo on its own: “this is a desk; that is a keyboard close-up.”

#### The paper

DINO patchifies each image. *Frame-wise* self-attention mixes tokens inside one view.

02

#### You

Relate photos: that desk corner in shot 1 is the same corner in shot 4, even if the zoom changed.

#### The paper

*Global* self-attention across all views. Alternating with frame-wise attention, 24 layers. No essential-matrix layer.

03

#### You

Guess where you were standing, and treat the first photo as “here” — the origin of your mental map.

#### The paper

Camera token per frame predicts $\mathbf{g}=[\mathbf{q},\mathbf{t},\mathbf{f}]$. Frame 1 is the world origin (identity extrinsics, special tokens).

04

#### You

Guess how far the wall is, and where every pixel sits in the room. Point at the mug in photo 1 and find it in photo 3.

#### The paper

DPT heads emit depth, a viewpoint-invariant point map, and tracking features (CoTracker2). Train all of them; at inference, fused depth+cameras often beat the dedicated point-map head.

05

#### You

You do not run bundle adjustment in your head. You form a 3D sketch in one look. Later you might refine it with geometry.

#### The paper

Feed-forward VGGT is already competitive with methods that still run geometry optimization. VGGT+BA is the optional refinement.

COLMAP is match → triangulate → bundle-adjust. VGGT is the same outputs from one transformer pass; VGGT+BA is the optional refinement. The rest of the guide is how those heads are trained.

## The paper, in order — every section

Open [arXiv 2503.11651](https://arxiv.org/pdf/2503.11651). CVPR 2025 Best Paper. Walk it in the authors’ order.

### Abstract

VGGT is a feed-forward net that infers cameras, point maps, depth, and 3D tracks from one, a few, or hundreds of views. 3D vision has been specialized per task; this is one model for all of them. Reconstruction in under a second, still beating methods that post-process with geometry optimization. SOTA on camera pose, multi-view depth, dense clouds, point tracking. Pretrained VGGT as a backbone also helps non-rigid tracking and feed-forward novel-view synthesis. Code: facebookresearch/vggt.

![VGGT teaser: cameras, depth, points, tracks from many views](https://arxiv.org/html/2503.11651v1/teaser.png)

**Paper Figure 1 (teaser).** One forward pass, variable $N$. The frustums are predicted cameras, not COLMAP cameras. If this picture is not obvious, the method section will not be either.

![VGGT architecture: DINO tokens, alternating attention, heads](https://arxiv.org/html/2503.11651v1/architecture_v4.png)

**Paper architecture figure.** Patchify with DINO, append camera + register tokens, alternate frame-wise and global self-attention, then camera head vs DPT heads. No cross-attention. Frame 1’s camera token is a different learned vector so the world frame is marked.

![VGGT vs DUSt3R qualitative 3D](https://arxiv.org/html/2503.11651v1/comparison_vggt_dust3r.png)

**Paper qualitative vs DUSt3R.** Oil painting, non-overlapping pair, repeated texture. DUSt3R is a two-view method plus fusion; this figure is why “just run DUSt3R” is not the same paper.

### §1 Introduction

Problem: 3D attributes of a scene from images, with a feed-forward net. Tradition is visual geometry + iterative BA (Hartley & Zisserman). Learning used to be complementary (matching, monocular depth). VGGSfM then folded learning and differentiable BA into one loop — geometry still sits in the inner loop, which is slow and complex.

The question: can a net now skip almost all geometry post-processing? DUSt3R / MASt3R are the nearest yes — but they take *two* images and fuse pairs with extra optimization for $N>2$.

VGGT’s bet: a large transformer, almost no 3D inductive bias, trained on a pile of 3D-annotated data, $N$ variable.

### §3.1 Problem (Eq. 1)

Input $(I\_i)\_{i=1}^N$, $I\_i\in\mathbb{R}^{3\times H\times W}$. Output, per frame: cameras $\mathbf{g}\_i$, depth $D\_i$, point map $P\_i$, tracking features $T\_i$. Equivariant to permuting frames $2\ldots N$; frame 1 is the world origin ($\mathbf{q}\_1=[0,0,0,1]$, $\mathbf{t}\_1=\mathbf{0}$).

**I1**world origin**I2****I3****… IN**↓ one transformer, permutation-equivariant on 2…N**g**camera**D**depth**P**points**T**tracks

Eq. 1 drawn. Dark token is the coordinate frame. Do not permute it with the others.

**Over-complete predictions.** $\mathbf{g}$ is recoverable from $P$ by PnP; depth from $P$ and $\mathbf{g}$. They still train all heads: extra supervision helps. At test, composing depth + cameras beats the dedicated point-map head. That sentence is the deployment default.

### §3.2 Backbone

Minimal 3D bias. DINO-style patchify each image to $K$ tokens. Alternating-Attention (AA): frame-wise SA (within a view) then global SA (across views), $L=24$ pairs. No cross-attention — only self-attention. AA is the inductive bias they did keep: integrate across images, normalize within an image.

#### Frame-wise SA

Tokens inside $I\_i$ talk. Normalizes one view. Cheap in $N$.

#### Global SA

Tokens across all views talk. This is the multi-view triangulation, learned.

$L=24$ of (frame, global). No cross-attention anywhere.

### §3.3 Heads

Per image: camera token $\mathrm{t}^{\mathbf{g}}\_i$ plus four register tokens (Darcet et al.). Frame 1 gets a *different* learned camera/register set so the net knows which view is the origin. After AA, discard registers; camera token → $\mathbf{g}=[q,t,f]$ (9-D); image tokens → DPT heads for depth, points, track features.

K image patches1 camera4 registers↓ AA · drop registersg = [q, t, f]DPT → D, P, T

Tracker $\mathcal{T}$ is CoTracker2 on $T\_i$. Query point in image $q$ (train: $q=1$), bilinear sample, correlate with other $T\_i$, self-attend, emit 2D correspondences. No temporal order assumed — unordered photo sets, not just video.

### §3.4 Training

$\mathcal{L}=\mathcal{L}\_{\mathrm{camera}}+\mathcal{L}\_{\mathrm{depth}}+\mathcal{L}\_{\mathrm{pmap}}+\lambda\mathcal{L}\_{\mathrm{track}}$, $\lambda=0.05$. Camera/depth/point losses sit on similar scales (unweighted). Data mix: Co3D, MegaDepth, ScanNet, Hypersim, BlendMVS, MVS-Synth, PointOdyssey, Virtual KITTI, Aria, Objaverse-like assets — real + synthetic, indoor + outdoor, SfM labels + renderer labels. Size comparable to MASt3R’s mix.

### §4 Experiments, table by table

**§4.1 cameras (Table 1).** CO3Dv2 + RealEstate10K, 10 images/scene, AUC@30 (min of relative rotation/translation accuracy). VGGT feed-forward beats COLMAP+SPSG, PixSfM, PoseDiff, DUSt3R, MASt3R, VGGSfM v2 — those last ones still run global alignment or BA (~7–20 s). VGGT: ~0.2 s. Optional BA on VGGT init still helps and is ~2 s because you skip triangulation.

COLMAP-class**~15s**DUSt3R + align**~7s**VGGT + optional BA**~2s**VGGT feed-forward**0.2s**

Wall-clock on the paper’s hardware, schematic widths. Accuracy still higher at 0.2 s.

**§4.2 depth (DTU).** Accuracy / completeness / overall (Chamfer). Only DUSt3R and VGGT lack GT cameras. Overall 1.741 → 0.382 vs DUSt3R; comparable to methods that *are given* GT cameras (GeoMVSNet cost volumes, MASt3R with GT triangulation).

**§4.3 point maps (ETH3D).** 10 frames, Umeyama align, official masks. Same three Chamfer numbers vs DUSt3R/MASt3R.

![VGGT predicted point maps with camera frustums](https://arxiv.org/html/2503.11651v1/pointmap_v6.png)

**Paper point-map figure.** Predicted cloud + frustums. This is $P$ (or fused $D$+$g$), not a COLMAP sparse model colored in.

**§4.4 tracking / matching.** Tracking head is not a two-view specialist, yet beats Roma on ScanNet-1500 AUC. Finetuned backbone also lifts dynamic CoTracker.

**Qualitative (Figs. 3–4).** Oil painting geometry, two views with *no overlap*, repeated texture — DUSt3R fails or OOMs past 32 frames; VGGT does not.

**§4.5 over-complete ablation** is the reason they predict redundant heads. Read it before you delete a loss “because PnP exists.”

### What not to claim

Feed-forward already beats prior pipelines; BA on top can still add points. Pairwise DUSt3R is not the same model class — do not quote VGGT’s $N=100$ numbers against a 2-view method without saying so. Single-view 3D is an emergent trick, not the training task.

## Why this paper exists

Structure-from-Motion (SfM) estimates cameras and a sparse point cloud from overlapping images. The industrial implementation is COLMAP: keypoints, matching, geometric verification, triangulation, bundle adjustment (BA). Learning has been invading that pipeline for a decade — learned detectors, learned matchers, even differentiable BA (VGGSfM). Geometry, however, still sits in the loop, which is why reconstruction is slow and brittle on texture-poor or few-view scenes.

DUSt3R and MASt3R made a different bet: a network that emits pairwise point maps, then a *global alignment* optimization to fuse pairs. VGGT asks whether that last optimization can go away. The network sees *all* images at once (one, a few, or hundreds), and directly predicts every 3D quantity you actually wanted from SfM+MVS+tracking.

Two claims to keep separate while you read:

1. **Feed-forward VGGT** is already competitive with, and often better than, methods that post-optimize.
2. **VGGT + optional BA** is the “we still win even if you give the other side their ritual” result.

Best Paper at CVPR 2025 is about claim 1 changing what a 3D backbone looks like, not about shaving 0.3° off a pose table.

CVPR 2025 Best Paper
feed-forward
1–hundreds of views
< 1 secondImages I1…INone, a few, or hundreds↓ DINO patchifyImage tokensCamera token + 4 registers / frame↓ alternating attention × 24Frame-wise SAwithin one viewGlobal SAacross views↓ headsg = [q, t, f]DPT → depthpoint map Ptracks T

Figure. VGGT is one transformer, four 3D outputs. First camera is the world origin.

A 3-minute flyover of VGGT: DINO tokens, camera tokens, alternating attention, no test-time BA required.

### Prerequisites

1. **01**

   #### Pinhole camera, extrinsics, intrinsics

   A camera is a rotation $R$ (here a quaternion $\mathbf{q}\in\mathbb{R}^4$), translation $\mathbf{t}\in\mathbb{R}^3$, and a field of view $\mathbf{f}\in\mathbb{R}^2$. VGGT packs $\mathbf{g}=[\mathbf{q},\mathbf{t},\mathbf{f}]\in\mathbb{R}^9$ and assumes the principal point is the image center — the same simplification COLMAP-style pipelines often make. If you cannot project a 3D point into a pixel, you cannot audit a point map.
2. **02**

   #### What bundle adjustment actually optimizes

   BA jointly refines cameras and 3D points to minimize reprojection error. It is iterative, requires correspondences, and fails without overlap. VGGT’s bet is that a large transformer trained on 3D-annotated data can *amortize* that optimization.

   UCF CRCV, Lecture 15 — Structure from Motion. The ritual VGGT is trying to skip.

   Polyfjord — a practical COLMAP track. Watch 5 minutes so “export to COLMAP / gsplat” in the VGGT repo is not abstract.
3. **03**

   #### Point maps (DUSt3R’s key object)

   A point map $P\_i\in\mathbb{R}^{3\times H\times W}$ stores, at each pixel, the 3D scene point observed there. Crucially in VGGT (and DUSt3R), point maps are *viewpoint-invariant*: every $P\_i$ is expressed in the coordinate frame of the **first camera**. Depth $D\_i$ is in that camera’s own view. Mixing those frames is the #1 implementation bug.
4. **04**

   #### DINOv2 tokens and DPT heads

   Images are patchified by a frozen/pretrained DINO encoder into tokens $t^I$. Dense outputs (depth, points, tracking features) are decoded with a DPT (dense prediction transformer) head — the multi-scale ViT readout from Ranftl et al. 2021 — then a $3\times 3$ conv.

   Yannic Kilcher — DINO (self-supervised ViT). VGGT’s tokenizer is this family of features, not a 3D-specialized CNN.
5. **05**

   #### Tracking-any-point

   Given a query pixel in one frame, predict its 2D location in all others (TAP-Vid, CoTracker). VGGT does not invent a new tracker; it emits dense tracking features $T\_i$ and plugs them into a CoTracker2 head. The result is that geometry features help correspondence, and correspondence is a first-class output rather than a SfM byproduct.

### Knowledge graph

Center is the claim: one transformer, all 3D attributes, almost no BA. Everything else is a spoke.

[COLMAP / SfM](https://colmap.github.io/)
[DUSt3R pairs](https://arxiv.org/abs/2312.14132)
[DINOv2 tokens](https://arxiv.org/abs/2304.07193)
[CoTracker](https://arxiv.org/abs/2307.07635)VGGTfeed-forward 3D · CVPR 2025alternating attn
over-complete heads
frame-1 origin
D + g at test

pipelines it replaces  foundations  backbones  tracking

classical SfM (COLMAP)
match → triangulate → bundle adjust
│
▼
learned SfM (VGGSfM) — differentiable BA still in the loop
pairwise feed-forward
DUSt3R / MASt3R: 2 images → point maps
│
└── still need global alignment for N>2
monocular specialists
DepthAnything, MoGe, LRM (one task each)
▼
VGGT (this paper)
DINO patchify
+ camera token + 4 register tokens / frame
+ alternating frame-wise / global attention (L=24)
+ camera head (g ∈ R^9)
+ DPT → depth, point map, track features
+ CoTracker2 head
train: over-complete (all heads), aleatoric uncertainties
infer: often fuse depth + cameras > raw point-map head
optional: BA on top → extra SOTA
downstream: non-rigid tracking, feed-forward NVS
export: COLMAP files → gsplat / NeRFCOLMAP SfM
DUSt3R pairs
DepthAnything / MoGe↓ still a pipeline or a pair-fuseDINO tokens
alternating attention↓ one forward passcameras g
depth D
points P
tracks T

The graph the ASCII block is drawing. Specialists on top; VGGT is the merge.

#### COLMAP / SfM

1. Detect & match
2. Triangulate
3. Bundle adjust
4. Then dense stereo

Slow. Breaks with little overlap.

#### VGGT glance

1. All images in
2. One transformer
3. Cameras, depth, points, tracks out
4. Optional BA afterwards

Under a second. N from 1 to hundreds.

### Problem statement, with the paper’s symbols

Input: $N$ RGB images $(I\_i)\_{i=1}^N$, $I\_i\in\mathbb{R}^{3\times H\times W}$. Output:

$$f\big((I\_i)\_{i=1}^{N}\big)=\big(\mathbf{g}\_i,\, D\_i,\, P\_i,\, T\_i\big)\_{i=1}^{N}.$$

$\mathbf{g}\_i$ cameras, $D\_i$ depth, $P\_i$ point map, $T\_i$ tracking feature grid. The first camera is the world frame: $\mathbf{q}\_1=[0,0,0,1]$, $\mathbf{t}\_1=\mathbf{0}$. Special learned camera/register tokens on frame 1 tell the transformer which image is the origin.

### Architecture — follow Figure 2

**Tokenize.** DINO turns each image into $K$ patch tokens. Concatenate a camera token $t\_i^{\mathbf{g}}$ and four register tokens $t\_i^{R}$ (Darcet et al. 2023 style). Frame 1 uses a *different* learned camera/register initialization than frames $2\ldots N$, which is how “I am the world origin” is encoded without writing $SE(3)$ into the architecture.

**Alternating-Attention (AA).** A standard transformer would global-attend all tokens from all frames, which mixes poorly when $N$ is large (activations of one image drowned by others) or small (no cross-view). AA alternates:

- *Frame-wise* self-attention: tokens of image $i$ only. Normalizes within a view.
- *Global* self-attention: all tokens from all images. Moves information across views.

Default depth: $L=24$ pairs. The paper is explicit that this is almost the *only* 3D inductive bias. No essential matrix, no cost volume, no explicit epipolar mask. The 3D prior lives in the training sets, not in the layers.

**Camera head.** Reads the output camera token and predicts $\mathbf{g}\_i$.

**Dense head.** DPT lifts image tokens to a feature map $F\_i$, then $3\times 3$ convolutions produce $D\_i$, $P\_i$, and tracking features $T\_i$, plus aleatoric uncertainty maps $\Sigma\_i^D$, $\Sigma\_i^P$. After training, those maps are usable as confidence.

**Tracking head.** CoTracker2 consumes $\{T\_i\}$ and query points (training queries always from image 1). Output: 2D correspondences in every frame.

### The over-complete prediction trick

Cameras, depth, and point maps are algebraically redundant. Given $P$ you can PnP for $\mathbf{g}$; given $\mathbf{g}$ and $D$ you can back-project to $P$. So why predict all three?

**During training**, forcing the shared backbone to explain several related 3D views of the same scene improves every head. Redundancy is a feature: it is extra supervision on the same geometry.

**During inference**, the paper reports that *composing* the independently predicted depth and cameras yields more accurate 3D points than using the dedicated point-map head. That is the opposite of what a tidy architecture diagram suggests, and it is one of the most useful sentences in the paper. If you wrap VGGT in a library, default to depth+camera fusion, not $P\_i$ verbatim.

Train all threeg, D, P — extra heads are extra supervision↓ at test, don’t trust the named headUse D + gback-project → 3DNot raw Pdedicated point-map is weaker

Over-complete training, selective decoding. The head named after the quantity is not always the head you read.

When a network is over-complete, train on the union of losses; decode with the empirically best combination. Do not assume the head named after the quantity you want is the head you should read.

### Training picture

VGGT is trained on a large union of public 3D-annotated datasets (the paper’s §3.4). Losses hit cameras, depth, point maps, tracks, and uncertainties. Uncertainties reweight the dense losses (aleatoric: predict $\sigma$, penalize $(\hat y-y)^2/\sigma^2 + \log\sigma$). You should expect the usual multi-task tension: if one loss dominates, turn its weight down rather than deleting a head — the over-complete result says the extra heads are doing work even when you will not use them at test time.

Inference cost: “under one second” for typical sets; “hundreds of images in seconds.” DUSt3R pairwise fusion runs out of memory beyond ~32 frames in their comparison figure; VGGT is built for the $N\gg 2$ regime.

### How to read the experiments

- **Camera pose** on Co3D and similar: compare feed-forward VGGT vs DUSt3R/MASt3R vs COLMAP vs VGGSfM. Then look at VGGT+BA as a separate row.
- **Multi-view depth and dense clouds:** this is MVS without known cameras. The headline is beating pairwise methods that still globally align.
- **Tracking:** VGGT features + CoTracker vs specialist TAP methods. The claim is “geometry backbone helps correspondence,” not “we obsolete CoTracker.”
- **Downstream:** freeze VGGT, improve non-rigid tracking and feed-forward novel view synthesis. This is the GPT/DINO analogy: a general 3D backbone, not a one-task network.
- **Qualitative landmines** they highlight: oil-painting geometry (DUSt3R flattens), two images with *no overlap* (DUSt3R fails; VGGT can still hallucinate a plausible scene — treat that with respect and suspicion), repeated textures.

Code release extras you should know: training/finetune scripts (July 2025), COLMAP export for gsplat/NeRF, Co3D pose eval branch, interactive viser/Gradio demos.

### Worked reconstruction (mental)

1. Take 8 photos of a desk, any order, including a close-up of the keyboard.
2. Pick photo 1 as world origin (or let the implementation do it). Identity extrinsics for that camera.
3. Forward pass: 8× (patches + 1 camera token + 4 registers) through 24 AA layers.
4. Read $\mathbf{g}\_{2:8}$ as poses relative to photo 1. Read depths. Fuse $D\_i$ with $\mathbf{g}\_i$ to a point cloud in frame 1.
5. Confidence-threshold $\Sigma^D$ before meshing. Export COLMAP, splat.
6. If a view is an outlier (motion blur), its uncertainty map should light up; drop it rather than BA-ing it in blindly.

Single-image mode is the zero-shot surprise: the same weights produce a plausible depth/point map from one photo because training included monocular 3D datasets. It is not metric SfM. Do not use a one-image point map as a survey.

### Failure modes

- Principal point is assumed centered. Heavy crop/letterbox breaks $\mathbf{f}$.
- Dynamic scenes: trained mostly static. Tracking head helps, but this is not a 4D Gaussian method.
- No-overlap views: the network will still emit a scene. That can be a hallucination. Check overlap before trusting metric structure.
- Memory still scales with $N \times K$. “Hundreds of images” is not “tens of thousands.”
- Downstream fine-tunes can destroy the over-complete balance; if you only supervise depth, pose may drift.

### Study plan

1. Write $\mathbf{g}=[\mathbf{q},\mathbf{t},\mathbf{f}]$ and the world-frame convention from memory.
2. Explain AA in one sentence that a COLMAP user would accept.
3. Prove to yourself that $P$ and $(D,\mathbf{g})$ are redundant. Then explain why training predicts both.
4. Run the official demo on 5 images. Compare fused depth+camera vs the point-map head on a textured object vs a blank wall.
5. Read DUSt3R’s global alignment section (not the whole paper) so you know what VGGT deleted.

### Constellation — read these next

- **pairs**

  #### [DUSt3R · Wang et al.](https://arxiv.org/abs/2312.14132)

  Two images → point maps, then global alignment for $N>2$. VGGT’s nearest ancestor. Read it to see what “no post-process” is refusing.
- **tokens**

  #### [DINOv2 · Oquab et al.](https://arxiv.org/abs/2304.07193)

  The patch encoder. VGGT adds almost no 3D bias on top of this.
- **tracks**

  #### [CoTracker · Karaev et al.](https://arxiv.org/abs/2307.07635)

  The tracking head VGGT plugs its $T\_i$ into. Geometry features, not a new tracker.
- **SfM+**

  #### [VGGSfM · Wang et al.](https://arxiv.org/abs/2311.17033)

  Video: DINO explained — https://www.youtube.com/embed/h3ij3F3cPIk

### Primary sources

- Paper: [arXiv:2503.11651](https://arxiv.org/abs/2503.11651).
- CVPR Open Access: [Wang et al., CVPR 2025, pp. 5294–5306](https://openaccess.thecvf.com/content/CVPR2025/html/Wang_VGGT_Visual_Geometry_Grounded_Transformer_CVPR_2025_paper.html).
- Project: [vgg-t.github.io](https://vgg-t.github.io/).
- Code: [github.com/facebookresearch/vggt](https://github.com/facebookresearch/vggt).
- Backspan: Hartley & Zisserman (chapters on cameras + BA); DUSt3R; DINOv2; DPT; CoTracker2; COLMAP tutorial until you can run it once.

**BibTeX**

```
@inproceedings{wang2025vggt,
  title={VGGT: Visual Geometry Grounded Transformer},
  author={Wang, Jianyuan and Chen, Minghao and Karaev, Nikita
          and Vedaldi, Andrea and Rupprecht, Christian and Novotny, David},
  booktitle={Proceedings of the IEEE/CVF Conference on Computer Vision
             and Pattern Recognition (CVPR)},
  pages={5294--5306},
  year={2025}
}
```
