---
generated_by: "build_obsidian_vault.py"
type: "paper-guide"
aliases: ["ACT and ALOHA", "ACT: compounding error is a horizon problem"]
paper_slug: "act"
source: "site/papers-act.html"
live_url: "https://chippy1520.github.io/ai-research-lab/papers-act.html"
tags: ["paper", "reading-guide"]
related_nodes: ["act", "action-chunking"]
related_curriculum: []
cssclasses: ["research-note", "paper-note"]
---

[[Home|Research Lab]]  /  [[Papers/Paper Guides|Paper Guides]]

# ACT: compounding error is a horizon problem

> [!paper] Research reading guide
> Complete reading guide for ACT / ALOHA (Zhao et al., RSS 2023, arXiv 2304.13705): compounding error, action chunking, CVAE, temporal ensembling.
>
> **Concepts:** 2 · **Related curriculum notes:** 0

> [!concepts] Connected concepts
> - [[Mind Map/Nodes/act|ACT]]
> - [[Mind Map/Nodes/action-chunking|Action chunking]]

> [!source] Canonical and public versions
> - Repository guide: `site/papers-act.html`
> - [Open the published HTML guide](https://chippy1520.github.io/ai-research-lab/papers-act.html)
> - Companion source: `papers/act.md`

---

## How a person opens a condiment cup

The cup is on the table. A policy that emits one joint command per 20 ms, independently, compounds a 1% error into a state no demonstration ever showed. ACT instead predicts a chunk of $k$ future joint targets from one observation, samples one mode of that chunk with a CVAE, and averages overlapping forecasts of the same $a\_t$ (temporal ensembling).

> [!example] Step 01 — You
> **You:** Look at the cup from a few angles, feel where your wrists are.
>
> **The paper:** Four RGB cameras through ResNet-18, plus joint positions. Pixel-to-action, no object CAD.

> [!example] Step 02 — You
> **You:** Commit to a short sequence: tip it, nest it, pry the lid. You do not re-choose every millimetre. A 1% twitch, repeated, knocks the cup over — compounding error.
>
> **The paper:** Predict $k$ future joint targets at once, $\pi(a_{t:t+k}\mid s_t)$. Effective horizon $\div k$. Ablation: 1% success at $k=1$, 44% at $k=100$.

> [!example] Step 03 — You
> **You:** There are two decent ways to pry. You pick one style and stick with it. Averaging both motions puts a finger through the lid.
>
> **The paper:** CVAE over chunks. Train with a style latent $z$. At test, $z=0$ — one coherent trajectory, not the mushy mean of two.

> [!example] Step 04 — You
> **You:** As you move, you keep a running blend of “what I already committed to” and “what I see now,” instead of jerking to a brand-new plan every two seconds.
>
> **The paper:** Temporal ensembling: query every tick, average overlapping forecasts of the same $a_t$ with $w_i=\exp(-m i)$.

> [!example] Step 05 — You
> **You:** You learned this from watching someone do it about fifty times, not from a warehouse of expert corrections (DAgger) that would ruin the teleop.
>
> **The paper:** ~50 demonstrations / ~10 minutes. Offline only. ALOHA is the cheap stage those demos were collected on.

Every later VLA that “predicts action chunks” is citing this case study, whether or not it names ACT. SmolVLA keeps 02 and replaces 03–04 with flow matching and an async queue.

## The paper, in order — every section

Open [arXiv 2304.13705](https://arxiv.org/pdf/2304.13705) (RSS 2023). Hardware paper + algorithm paper glued together. Read both; LeRobot only ships the algorithm.

### Abstract

Fine tasks (cable ties, battery slotting) need precision, contact, closed-loop vision. Usually that means expensive robots and calibration. Question: can learning make cheap, imprecise hardware do them? They collect demos on a custom teleop rig and train end-to-end. Imitation has two diseases here: compounding error, and non-stationary humans. ACT is a generative model over action sequences. Six real tasks (open a translucent condiment cup, slot a battery) at 80–90% with ~10 minutes of demos. Site: tonyzhaozh.github.io/aloha.

![ALOHA bimanual teleoperation hardware](https://arxiv.org/html/2304.13705v1/figures/setup.jpg)

**Paper hardware figure.** Leader arms in the operator’s hands, followers on the table, four cameras. Joint-space mapping — no IK. This is the data engine; ACT is the learner.

![ACT real-world fine manipulation tasks](https://arxiv.org/html/2304.13705v1/real_tasks.png)

**Paper real tasks.** Cup, battery, velcro, tape, shoe. Each frame is a contact story from §V-A. Quote subtask columns, not a single %.

![Four camera observations used by ACT](https://arxiv.org/html/2304.13705v1/figures/obs.jpg)

**Paper observations.** Four RGB streams at 480×640. Wrist + workspace. This is why ResNet-18 × 4, not a single front camera.

### §I Introduction — the cup paragraph

Do not skim this. Opening a condiment cup sitting upright: right gripper tips it, nudges it into the open left gripper; left closes gently and lifts; a right finger comes from below and pries the lid. Millimetres fail. That sequence is the definition of “fine” in this paper: pinch, pry, tear — not pick-and-place.

Prior fine systems used expensive robots and sensors. Cheap hardware is less precise, so sensing/planning get worse. Learning is the proposed compensation. Then: compounding error at 50 Hz, and humans who pause or take different styles.

### §III ALOHA (the five design rules)

Low-cost (lab-budget, comparable to one industrial arm), versatile, user-friendly, repairable, high-performance teleop. Off-the-shelf ViperX-style arms + 3D-printed handles, joint-space leader–follower, no special encoders. Assemble in <2 hours. Capabilities they brag about (zip-tie thread, RAM insert, ping-pong juggle) are teleop existence proofs, not ACT success rates — do not mix those.

Actions recorded are *leader* joint positions, not follower. The PID tracks the gap; force is implicit in that gap. Observations: follower joints + 4 cameras.

### §IV ACT pipeline

Collect demos → train to predict future action sequence from current obs → at test, load lowest val-loss checkpoint. Main failure they name: compounding error, previous actions leave you off the demonstration manifold.

### §IV-A Chunking + temporal ensemble

Neuroscience “action chunking”: grasp-the-wrapper is one unit, not 50 independent joint commands. Fix chunk size $k$: every $k$ steps, observe, emit $k$ actions, execute. Effective horizon of a $T$-step task becomes $T/k$. Policy is $\pi\_\theta(a\_{t:t+k}\mid s\_t)$ not $\pi\_\theta(a\_t\mid s\_t)$.

| Alternative | Representation and consequence |
|---|---|
| **π(a t \| s t )** | 1 step → 1 → 1 → × T · π(a t \| s t ) Horizon = T. 1% ablation. |
| **π(a t:t+k \| s t )** | k chunk → k · π(a t:t+k \| s t ) Horizon = T/k. 44% at k=100. |

Chunking also models non-Markov human pauses: a single-step policy cannot condition on “we are in the middle of a hesitation.”

Naive chunk = open-loop for $k$ steps (jerky at boundaries). Fix: query every timestep, dump overlapping predictions into buffers $\mathcal{B}[t:t+k]$, apply $a\_t=\sum\_i w\_i A\_t[i]/\sum\_i w\_i$ with $w\_i=\exp(-m\cdot i)$ (Algorithm 2). Newer predictions weigh more.

> [!diagram] Overlapping chunks with exponential weights
> chunk at t · chunk at t+1 (heavier) · chunk at t+2 (heaviest) · now

The dashed line is the action you actually send: weighted average of every chunk that covers “now.”

Ablation they want you to remember: $k=1$ ≈ 1% success on the simulated cube/insertion average with ensembling off; $k=100$ ≈ 44%. Chunk size is the paper.

### §IV-B CVAE

Same observation, different human trajectories; humans are more stochastic where precision does not matter. So the policy is a CVAE over chunks. Encoder: $q(z\mid a\_{t:t+k}, o\_t)$ as a diagonal Gaussian — in practice they drop images and condition only on proprio + the action chunk (faster). Decoder/policy: $p(a\_{t:t+k}\mid o\_t,z)$. Train: reconstruction + $\beta$ KL to a Gaussian prior. Test: discard encoder, $z=\mathbf{0}$.

Higher $\beta$ ⇒ less information in $z$. They call the CVAE *essential* for precise tasks from human data (§VI-B).

### §IV-C Implementation

Encoder: BERT-style transformer, inputs = current joints + $k$ actions + learned [CLS] ($k+2$ tokens); [CLS] predicts $(\mu,\sigma)$ of $z$. Decoder: ResNet-18 on four $480\times 640$ RGB → $15\times 20\times 512$ maps → 300 tokens + 2D sinusoidal PE; transformer encoder mixes cameras + 14-DoF joints + $z$; transformer decoder emits $k\times 14$ absolute joint targets. Dynamixel PID tracks those targets at high rate.

**4**×480×640→**300**×4 tokens+**14**joints+**z**→**k×14**

Decoder tensor path. Train $z$ from [CLS]; test $z=0$.

### §V Tasks (read every one)

![ACT simulated cube transfer and insertion](https://arxiv.org/html/2304.13705v1/sim_tasks.png)

**Paper sim tasks.** Transfer Cube and Bimanual Insertion — the $k=1$ vs $k=100$ ablation lives here, not on the cup.

![ALOHA teleop skill examples](https://arxiv.org/html/2304.13705v1/figures/teleop_tasks.jpg)

**Paper teleop skills.** Existence proof for the hardware (zip-tie, RAM, …). Do not quote these as ACT policy success rates.

Sim: Transfer Cube, Bimanual Insertion. Real: Slide Ziploc, Slot Battery, Open Cup, Thread Velcro (3 mm × 25 mm loop), Prep Tape, Put On Shoe. Each paragraph in V-A is a contact story — mid-air second grasp, springy battery slot, tight shoe. Thread Velcro: millimetres at grasp 1 become >10 mm at insertion.

### Tables I–II

Sim: scripted vs human data, 3 seeds × 50 evals. Real: 1 seed × 25 evals. ACT crushes BeT and earlier BC. Open Cup: tip-over 100, grasp 96, open lid 84. Thread Velcro insert only 20 — the paper is honest about the hard step. Put On Shoe substeps stay ≥92 after the lift. Quote subtask columns, not a single headline %.

### What not to mix

ALOHA teleop skill list ≠ ACT policy success. Leader joints ≠ follower joints. $z=0$ at eval is a choice, not “the model is deterministic by architecture.” SmolVLA keeps chunks and throws away this CVAE.

## The task that breaks ordinary behavior cloning

Opening a translucent condiment cup: tip it with the right gripper, nest it into the left, lift, pry the lid from below. Millimetres matter. Contact is rich. The object deforms. Modeling this well enough to plan is a research project by itself. Humans do not model it; they look and compensate. The paper’s hardware bet is that a *pixel-to-joint* policy on commodity webcams can do the same, if you can collect demonstrations on a robot that costs about as much as one industrial arm.

Imitation learning then fails in two textbook ways:

1. **Compounding error.** $\pi(a\_t\mid o\_t)$ is slightly wrong; $o\_{t+1}$ is off-distribution; errors accelerate. DAgger would ask for expert corrections on-policy. That is miserable with a teleop interface, and noise injection during demos can make the fine task fail while you are trying to demonstrate it.
2. **Non-stationary human demos.** People pause. They take different trajectories for the same state. A deterministic Markov policy cannot represent “sometimes wait, sometimes commit,” and L2/L1 on a single next action averages those modes into a mushy middle that collides with the cup.

ACT’s answers are, respectively: predict $k$ actions at once (horizon $\div k$), and train a CVAE over those chunks (multimodality). Smoothness is a third, separate trick: temporal ensembling.

~80M
chunk size k
CVAE · z=0 at test
50 demos

> [!flow] Architecture / data flow
> **4 RGB cameras** — ResNet-18 each + **Joints** — 14-DoF bimanual + **z** — style latent · 0 at eval
> ↓ transformer encoder
> **Transformer decoder** — emits k joint-target vectors
> ↓
> **Naive chunk** — open-loop for k steps + **+ temporal ensemble** — query every tick · exp weights

Figure. ACT datapath. Ensembling is inference-only; training still sees whole chunks.

### Prerequisites

1. **01**

   #### Behavior cloning as supervised learning

   Dataset of $(o,a)$ from an expert. Minimize a regression loss. No environment interaction at train time. That is the feature (safe, off-policy) and the bug (covariate shift).
2. **02**

   #### Why DAgger exists, and why they refuse it

   Ross, Gordon, Bagnell 2011: mix expert actions on states visited by the current policy. For ALOHA, the expert is a human on leader arms. Stopping every few seconds for a correction destroys dexterity. ACT is the “offline-only” alternative.
3. **03**

   #### Transformers as sequence models

   Encoder over a set of visual tokens + joints; decoder over a target action sequence of length $k$. If you have written a tiny GPT, you have the decoder. Causal masking on actions is the same idea as next-token training, except the “tokens” are continuous joint vectors.
4. **04**

   #### Conditional VAE, one picture

   Encoder $q(z\mid a\_{t:t+k}, o\_t)$ → Gaussian. Decoder $p(a\_{t:t+k}\mid o\_t, z)$. Loss = reconstruction + $\beta\,\mathrm{KL}(q\|p(z))$. At test time drop the encoder, set $z=0$ (prior mean). You get a deterministic policy that was trained as if it were generative — a useful hack when you want multimodality during learning and a single good trajectory at eval.

> [!video] Variational Autoencoders animated
> [Watch video](https://www.youtube.com/watch?v=qJeaCHQ1k2w)
>
> Deepia, “Variational Autoencoders | Generative AI Animated.” Map this onto ACT: encoder sees the chunk, decoder is the policy, z is clamped to 0 on the robot.

### Knowledge graph

Center is cheap-arm fine manipulation. Spokes are the three diseases and the three modules.

[compounding error](https://arxiv.org/abs/1011.0686)
[VAE / CVAE](https://arxiv.org/abs/1312.6114)
[Diffusion Policy](https://arxiv.org/abs/2303.04137)
ALOHA teleopACTchunk · CVAE · ensemblek-step chunk
z=0 at test
exp weights
[[Papers/SmolVLA and LeRobot|SmolVLA keeps k]]

problems  foundations  cousins  descendants

The field-scale version of this tree is the [living mind map](https://chippy1520.github.io/ai-research-lab/mindmap.html) (click ACT, chunking, CVAE, SmolVLA).

> [!graph] Concept flow
> **ALOHA teleop**
> ↓ 50 demos
> **compounding error · human modes / pauses · jerky chunk edges**
> ↓ three fixes
> **chunk k · CVAE · z=0 · temporal ensemble**
> ↓
> **ACT in LeRobot**

Three problems, three modules. Later VLAs keep the chunk and swap the other two.

| Alternative | Representation and consequence |
|---|---|
| **Single-step BC (k=1)** | Single-step BC (k=1) Error grows. 1% ablation success. |
| **Chunked (k=100)** | Chunked (k=100) Horizon ÷ k. 44% on the same ablation. |

Bars are error magnitude over time, schematic. The numbers are the paper’s k-ablation, ensembling off.

### ALOHA, only as much as the algorithm needs

The paper is a *system* paper: hardware + algorithm. For the algorithm you need this much hardware context:

- Two ViperX 6-DoF follower arms + two smaller leader arms, joint-space mapping, ~$20k all-in, assemble in <2 hours from off-the-shelf parts plus 3D print.
- Four RGB cameras: front, top, two wrists. Actions are leader joint positions (14-DoF bimanual: 2×6 + grippers), recorded at high frequency (~50 Hz in the usual telling).
- Design principles they list: low-cost, versatile, user-friendly, repairable, easy-to-build. No special encoders, no machined parts.

You can ignore ping-pong juggling teleop videos until after you understand chunking. They are capability ads for the teleop, not for ACT.

### Action chunking

Psychology: humans group motor primitives and fire them as a unit. Implementation: every $k$ steps, observe once, emit $k$ target joint positions, execute open-loop inside the chunk.

$$\pi\_\theta(a\_{t:t+k}\mid s\_t)\quad\text{instead of}\quad\pi\_\theta(a\_t\mid s\_t).$$

Effective horizon of a $T$-step task becomes $T/k$. Ablation (simulated cube transfer / bimanual insertion, averaged, ensembling off): **1% success at $k=1$**, **44% at $k=100$**, then a decline at $k=200$ and $400$ as the policy becomes too open-loop. Chunk size is a bias–variance dial, not a magic constant. Typical real-robot operating point in follow-on work: $k=50$–$100$ (about 1–2 seconds at 50 Hz).

- k = 1 — 1%

- k = 100 — 44%

- k = 200+ — drops

Paper ablation, ensembling off. Too small k → compounding error. Too large k → open-loop drift.

Chunking also swallows short non-Markovian confounders (a pause of length $

### Temporal ensembling

Naïve chunking incorporates a new observation only every $k$ steps → abrupt switches, jerky motion. Fix: query the policy *every* timestep. Then timestep $t$ has overlapping predictions from chunks that started at $t, t-1, \ldots$. Average them with exponential weights

$$w\_i=\exp(-m\cdot i),\qquad i=0\text{ is the oldest prediction for this same $t$}.$$

Smaller $m$ incorporates new observations faster (more reactive, potentially noisier). This is *not* smoothing across adjacent times, which would bias the target. It averages different forecasts of the *same* $a\_t$. Training cost unchanged; inference cost × roughly $k$ if you are naïve, or you keep a rolling buffer of recent decoder outputs.

SmolVLA’s async stack is a later, cheaper cousin: instead of inferring every tick, infer when the queue is half empty. Read that paper after this one.

### Why a CVAE, not plain L1 on chunks

Humans are stochastic where precision does not matter and precise where it does. Averaging modes of $a\_{t:t+k}$ produces an action that was never demonstrated (the gripper passing through the lid). A CVAE puts a latent $z$ on the chunk:

- **Encoder** (train only): sees action chunk + proprioception (they drop images here for speed), predicts $(\mu,\sigma)$ of diagonal Gaussian $z$.
- **Decoder / policy**: sees images, joints, and $z$; transformer-decodes the chunk. Reconstruction is L1 on actions, plus KL toward the prior, weight $\beta$.
- **Test:** $z=\mathbf{0}$. Deterministic, but trained not to collapse modes in the same way a raw L1 decoder would.

If your task is unimodal and low-precision, the CVAE is overhead. If your task is “pry a lid,” it is load-bearing. LeRobot still ships this as the default ACT.

| Alternative | Representation and consequence |
|---|---|
| **Train** | Train Encoder sees the chunk + proprio, predicts $(\mu,\sigma)$ of $z$. Decoder reconstructs the chunk from images, joints, and $z$. L1 + $\beta$ KL. |
| **Test** | Test Throw the encoder away. Set $z=\mathbf{0}$. One coherent style, not the average of two prying motions. |

### Architecture (Figure 2 of the paper)

- **Vision:** ResNet-18 per camera. Four views in the ALOHA setup.
- **Transformer encoder:** synthesizes visual tokens, joint positions, and $z$.
- **Transformer decoder:** outputs $k$ action vectors (continuous joints).
- ~80 million parameters. Trains in a few hours on one GPU. Data-efficient: 50 demos is the headline.

Actions at train time are *leader* joint positions, not follower. That is the teleop copy signal. At test time the policy’s outputs are sent to the followers.

### Results you should actually remember

- Six real fine-manipulation tasks (condiment cup, battery slotting, etc.): **80–90% success from ~50 demonstrations / ~10 minutes of teleop**.
- Beats prior imitation baselines on the same hardware by a wide margin; $k=1$ ablation collapses.
- Simulation: chunk size curve cited above. Use it when someone asks “why not $k=1$ with a better vision encoder?”

The paper’s contribution is the *product* of ALOHA and ACT. Algorithm papers that drop the hardware still keep chunking + ensembling; that is the intellectual core.

### Where this sits in 2025–2026 stacks

LeRobot’s docs call ACT the first policy to train: fast, light, 50-demo territory. SmolVLA keeps chunks, replaces the CVAE decoder with a flow-matching expert, and replaces every-tick ensembling with async queues. Diffusion Policy is the other chunked baseline (iterative denoising instead of one transformer decode). When a new VLA paper says “we predict action chunks,” they are citing this paper whether or not they name it.

Practical LeRobot notes (from the official ACT page, not folklore): ResNet-18 backbone, transformer over cameras + joints + latent, L1 + KL, $z=0$ at eval, temporal ensembling on. Watch the LeRobot team’s ACT tutorial before your first train run.

> [!video] Train an ACT Policy for the SO-101 with LeRobot
> [Watch video](https://www.youtube.com/watch?v=-tkEMLOLEwo)
>
> Trelis Research — train ACT on SO-101 with LeRobot (includes KL / style discussion). Pair with HF Tutorial #4 for recording.

> [!video] Attention in transformers, step by step
> [Watch video](https://www.youtube.com/watch?v=eMlx5fFNoYc)
>
> 3Blue1Brown, attention step-by-step. This is the decoder that emits the chunk.

### Worked chunk at 50 Hz, $k=100$

A 100-step chunk is 2 seconds. Observation at $t=0$: four RGB frames + 14 joint angles. Decoder emits $100\times 14$ targets. Without ensembling, the arm is open-loop until $t=100$. With ensembling, at $t=10$ you already have 11 overlapping forecasts of $a\_{10}$; the exponential mix is what is written to the controller. If the cup tips unexpectedly at $t=30$, reactivity is governed by $m$ and by the fact that new images enter every 20 ms — not by waiting for the chunk to end.

Failure mode of too-large $k$: the 2-second plan was built for a cup that is no longer there. Failure mode of too-small $k$: you are back to compounding error (the 1% ablation).

### Caveats

- $z=0$ at test time throws away multimodality at eval. If you need diversity, sample $z$ — and accept variance in success.
- Ensembling assumes you can afford one forward pass per control tick. On a CPU robot, you cannot; go read SmolVLA async.
- 50 demos is for their tasks and their teleop quality. Your noisy SO-100 dataset is not their ALOHA dataset.
- ResNet-18 is 2023. Replacing it with a VLM does not make ACT a VLA; you also changed the objective and the language interface. That is SmolVLA / $\pi\_0$.

### Study plan

1. Derive $T/k$ effective horizon. Plot imagined success vs $k$ with a peak and a drop.
2. Write the CVAE loss (L1 + $\beta$ KL) and the test-time $z$.
3. Implement temporal ensembling in five lines of numpy on fake overlapping arrays. Check that you average the same $t$, not neighbors.
4. Train LeRobot ACT on a public dataset. Change $k$. Do not tune anything else until you have seen that curve move.
5. Then read SmolVLA §3.3 and note what they kept (chunks) and what they replaced (CVAE, ensembling).

### Constellation — read these next

- **error**

  #### [DAgger · Ross, Gordon, Bagnell](https://arxiv.org/abs/1011.0686)

  The compounding-error diagnosis ACT answers with horizon reduction instead of interactive relabeling.
- **CVAE**

  #### [Auto-Encoding Variational Bayes · Kingma & Welling](https://arxiv.org/abs/1312.6114)

  Plus Sohn et al. CVAE. Why $z=0$ at test is a prior sample, not “the encoder died.”
- **cousin**

  #### [Diffusion Policy · Chi et al.](https://arxiv.org/abs/2303.04137)

  Same chunking instinct, different generative head. LeRobot ships both.
- **next**

  #### [[Papers/SmolVLA and LeRobot|SmolVLA]]

  Keeps the chunk, replaces CVAE+ensemble with flow matching and an async queue.

### Primary sources

- Paper: [arXiv:2304.13705](https://arxiv.org/abs/2304.13705) — Zhao, Kumar, Levine, Finn.
- Project: [tonyzhaozh.github.io/aloha](https://tonyzhaozh.github.io/aloha/).
- Original code: [github.com/tonyzhaozh/aloha](https://github.com/tonyzhaozh/aloha).
- LeRobot ACT: [huggingface.co/docs/lerobot/act](https://huggingface.co/docs/lerobot/act).
- Backspan: Ross et al., DAgger (AISTATS 2011); Kingma & Welling VAE; Vaswani et al. transformers; LeRobot ACT tutorial on YouTube (official team).

**BibTeX**

```
@inproceedings{zhao2023learning,
  title={Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware},
  author={Zhao, Tony Z. and Kumar, Vikash and Levine, Sergey and Finn, Chelsea},
  booktitle={Robotics: Science and Systems (RSS)},
  year={2023}
}
```
