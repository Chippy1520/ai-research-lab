---
generated_by: "build_obsidian_vault.py"
type: "curriculum-lesson"
aliases: ["Optimization Dynamics & AdamW"]
day: 1
cycle: 1
domain: "Machine Learning"
stage: "Foundations"
status: "ready"
source: ["curriculum_plan.json", "modules/module_01.py"]
tags: ["curriculum", "machine-learning", "foundations"]
cssclasses: ["research-note", "curriculum-note"]
related_concepts: ["Mind Map/Nodes/systems.md", "Mind Map/Nodes/learning.md"]
related_papers: []
---

[[Home|Research Lab]]  /  [[Curriculum/Curriculum|Curriculum]]

# Day 01 — Optimization Dynamics & AdamW

> [!curriculum] Machine Learning · Foundations
> **Cycle 1** · **status: ready**
> Research and write only when this day becomes current.

> [!sequence] Learning sequence
> - [[Curriculum/Curriculum|Curriculum map]]
> - [[Curriculum/Lessons/Day 02 - Image Formation, Sampling & Color|Day 02 →]]

> [!concepts] Knowledge-graph concepts
> - [[Mind Map/Nodes/systems|Systems]]
> - [[Mind Map/Nodes/learning|Learning]]

## Foundation threads

- probability & statistics
- linear algebra
- optimization
- algorithms
- information theory
- systems

## Learning record

| Status | Confidence | Minutes | Revisit |
|---|---|---|---|
| ready | Not recorded | Not recorded | No |

> [!current] Current due lesson
> Generate or deepen this lesson just in time rather than pre-authoring future modules.

---

> [!lesson] Authored technical lesson
> The complete static chapter is exported from the canonical Streamlit module.
> Interactive plots and controls remain available in the research-lab application.

## Optimization as a discrete-time dynamical system

**Research objective.** Derive how curvature,
momentum, adaptive preconditioning, finite-time moment bias, and decoupled
regularization determine an optimizer's trajectory—not merely its final loss.

### 1 · Executive summary and engineering motivation

Training a foundation model is a controlled dynamical process in a parameter
space with millions or billions of dimensions. The optimizer receives a noisy
local measurement $g_t$ and must select a stable, computationally affordable
update. In transformers, coordinates associated with embeddings, normalization
gains, attention projections, and sparse tokens can exhibit radically different
gradient scales. A single scalar learning rate therefore moves some coordinates
too slowly while destabilizing others.

Adam combines a low-pass estimate of the gradient with a diagonal estimate of
its second raw moment. AdamW then separates this data-dependent preconditioning
from parameter-norm control. This distinction is operationally important in
large language models, vision transformers, diffusion models, and robot policies:
coupling an $L_2$ penalty into Adam makes the effective regularization strength
depend on each coordinate's gradient history. Decoupled decay instead applies a
predictable contraction in parameter space.

### 2 · Local quadratic model and why naive descent fails

Around a strict local minimizer $\theta^\star$, a twice-differentiable objective
admits the second-order approximation

$$
\mathcal L(\theta) \approx \mathcal L(\theta^\star) + \frac{1}{2}(\theta-\theta^\star)^\top H(\theta-\theta^\star), \qquad H=H^\top\succ 0.
$$

Define the error $e_t=\theta_t-\theta^\star$. Then

$$
\nabla_\theta \mathcal L(\theta_t)=He_t,
$$

$$
\theta_{t+1}=\theta_t-\alpha H e_t \quad\Longrightarrow\quad e_{t+1}=(I-\alpha H)e_t.
$$

Since $H$ is real symmetric, write $H=Q\Lambda Q^\top$, where
$Q^\top Q=I$ and $\Lambda=\operatorname{diag}(\lambda_1,\ldots,\lambda_d)$.
Rotating into the eigenbasis with $z_t=Q^\top e_t$ gives

$$
z_{t+1}=Q^\top(I-\alpha Q\Lambda Q^\top)Qz_t=(I-\alpha\Lambda)z_t.
$$

$$
z_{t+1,i}=(1-\alpha\lambda_i)z_{t,i}=(1-\alpha\lambda_i)^{t+1}z_{0,i}.
$$

Convergence for every eigendirection requires
$|1-\alpha\lambda_i|<1$. Unrolling both inequalities,

$$
-1<1-\alpha\lambda_i<1\Longrightarrow -2<-\alpha\lambda_i<0\Longrightarrow 0<\alpha\lambda_i<2.
$$

$$
\boxed{0<\alpha<\frac{2}{\lambda_{\max}(H)}}
$$

A high condition number $\kappa(H)=\lambda_{\max}/\lambda_{\min}$ creates a
narrow valley. Stability is dictated by $\lambda_{\max}$, while progress along
the shallow direction scales with $\lambda_{\min}$. Thus stable SGD zig-zags
across the steep axis and crawls along the shallow axis.

### 3 · Momentum as a second-order recurrence

$$
v_t=\mu v_{t-1}+g_t,\qquad \theta_{t+1}=\theta_t-\alpha v_t.
$$

For one Hessian eigendirection with curvature $\lambda$, $g_t=\lambda e_t$ and $\alpha v_{t-1}=e_{t-1}-e_t$. Substitution gives

$$
e_{t+1}=e_t-\alpha(\mu v_{t-1}+\lambda e_t)=(1-\alpha\lambda)e_t-\mu(e_{t-1}-e_t)=(1+\mu-\alpha\lambda)e_t-\mu e_{t-1}.
$$

$$
r^2-(1+\mu-\alpha\lambda)r+\mu=0.
$$

The characteristic roots determine damping. Real roots inside the unit circle
give monotone or over-damped convergence; complex roots produce oscillation with
envelope approximately controlled by $\sqrt{\mu}$. Momentum accumulates
persistent low-curvature gradients while rapidly alternating steep-direction
gradients partially cancel.

### 4 · Adam: moment estimation and diagonal preconditioning

For stochastic gradient $g_t=\nabla_\theta\ell(\theta_{t-1};\xi_t)$,

$$
m_t=\beta_1m_{t-1}+(1-\beta_1)g_t,
$$

$$
v_t=\beta_2v_{t-1}+(1-\beta_2)(g_t\odot g_t).
$$

Here $m_t$ estimates the first moment and $v_t$ estimates the uncentered second
moment coordinate-wise. Expanding the first recurrence from $m_0=0$ yields

$$
m_t=(1-\beta_1)\sum_{i=1}^{t}\beta_1^{t-i}g_i.
$$

If $\mathbb E[g_i]=\mu_g$ is locally stationary, then the expected value is

$$
\mathbb E[m_t]=(1-\beta_1)\sum_{i=1}^{t}\beta_1^{t-i}\mu_g=(1-\beta_1)\mu_g\sum_{k=0}^{t-1}\beta_1^k.
$$

$$
\sum_{k=0}^{t-1}\beta_1^k=\frac{1-\beta_1^t}{1-\beta_1}\quad\Longrightarrow\quad\mathbb E[m_t]=(1-\beta_1^t)\mu_g.
$$

The zero initialization therefore attenuates early moments. Dividing by the known attenuation gives the bias-corrected estimators

$$
\widehat m_t=\frac{m_t}{1-\beta_1^t},\qquad\widehat v_t=\frac{v_t}{1-\beta_2^t}.
$$

$$
\theta_t=\theta_{t-1}-\alpha\frac{\widehat m_t}{\sqrt{\widehat v_t}+\varepsilon}.
$$

The denominator is an online diagonal preconditioner. A coordinate with
repeatedly large squared gradients receives a smaller effective step, while a
coordinate with small or sparse gradients receives a relatively larger one.
The $\varepsilon$ term is not only a divide-by-zero guard: when
$\sqrt{\widehat v_{t,i}}\ll\varepsilon$, it sets the coordinate's effective
learning-rate ceiling.

### 5 · Why $L_2$ inside Adam is not weight decay

For plain SGD, adding $\frac{\lambda}{2}\|\theta\|_2^2$ to the loss produces
$g_t+\lambda\theta_t$ and therefore

$$
\theta_{t+1}=\theta_t-\alpha(g_t+\lambda\theta_t)=(1-\alpha\lambda)\theta_t-\alpha g_t.
$$

This is exactly multiplicative weight decay. For an adaptive optimizer with
diagonal preconditioner $D_t=\operatorname{diag}
(1/(\sqrt{\widehat v_t}+\varepsilon))$, placing the penalty in the gradient gives

$$
\theta_{t+1}=\theta_t-\alpha D_t(g_t+\lambda\theta_t)=(I-\alpha\lambda D_t)\theta_t-\alpha D_tg_t.
$$

The shrinkage matrix $I-\alpha\lambda D_t$ now varies by coordinate and time.
Parameters with large historical gradients are regularized less. Hence the
claimed weight decay has become entangled with the optimizer state.
AdamW restores a uniform contraction by separating the operations:

$$
\boxed{\theta_t=(1-\alpha\lambda)\theta_{t-1}-\alpha\frac{\widehat m_t}{\sqrt{\widehat v_t}+\varepsilon}}
$$

Decoupling also makes learning-rate and regularization tuning more nearly
orthogonal. In production, parameter groups commonly exclude biases and
normalization scale/shift parameters from decay because their norms do not play
the same capacity-control role as weight matrices.

### 6 · Failure modes and research practice

- **Unstable base rate:** adaptive scaling does not remove the need for warm-up,
  clipping, or curvature-aware tuning.
- **Stale moments:** abrupt distribution changes can make long-memory second
  moments suppress useful adaptation.
- **Small-batch noise:** the optimizer trajectory may exploit noise but can also
  become dominated by outliers; inspect gradient and update norms separately.
- **Silent regularization errors:** verify whether a framework's optimizer truly
  decouples decay and which parameter groups receive it.
- **Metric myopia:** training loss alone cannot reveal whether decay improves
  held-out performance or merely slows fitting.

### 7 · What problem are we actually optimizing?

Supervised learning usually minimizes empirical risk plus an explicit
regularizer. For parameters $\theta\in\mathbb R^d$, data
$\mathcal D=\{(x_i,y_i)\}_{i=1}^{N}$, per-example loss $\ell_i$, and
regularizer $R$, the finite-sum problem is

$$
F(\theta)=\frac{1}{N}\sum_{i=1}^{N}\ell_i(\theta)+\lambda R(\theta).
$$

A minibatch $B_t$ of size $b$ replaces the full gradient with
$g_t=\frac1b\sum_{i\in B_t}\nabla\ell_i(\theta_t)$. Under uniform sampling,
$\mathbb E[g_t\mid\theta_t]=\nabla F_{\mathrm{data}}(\theta_t)$: the estimator is
conditionally unbiased, but not noiseless. Writing
$g_t=\nabla F_{\mathrm{data}}(\theta_t)+\xi_t$ isolates gradient noise with
conditional covariance $\Sigma_t=\mathbb E[\xi_t\xi_t^\top\mid\theta_t]$.
Approximately, independent examples make the variance shrink as $1/b$, although
correlated or heavy-tailed examples violate the clean textbook picture.

Optimization and generalization are therefore not identical objectives. A method
may minimize training loss rapidly yet reach a solution with worse validation
behavior. Batch size, data order, augmentation, schedules, clipping, and decay all
change the stochastic trajectory. The optimizer is one part of a coupled training
system—not a detachable ranking of algorithms.

### 8 · Conditioning, optimal scalar steps, and preconditioning

For a positive-definite quadratic with eigenvalues in $[\mu,L]$, the worst one-step contraction under scalar-step gradient descent is

$$
\rho(\alpha)=\max_{\lambda\in[\mu,L]}|1-\alpha\lambda|.
$$

The minimax choice balances the endpoint magnitudes: $1-\alpha\mu=-(1-\alpha L)$. Solving explicitly,

$$
1-\alpha\mu=-1+\alpha L\Longrightarrow 2=\alpha(L+\mu)\Longrightarrow \alpha^\star=\frac{2}{L+\mu}.
$$

$$
\rho^\star=1-\alpha^\star\mu=1-\frac{2\mu}{L+\mu}=\frac{L-\mu}{L+\mu}=\frac{\kappa-1}{\kappa+1}.
$$

As $\kappa=L/\mu$ grows, $\rho^\star\to1$ and progress slows. A positive-definite
preconditioner $P_t$ changes the update to
$\theta_{t+1}=\theta_t-\alpha P_tg_t$. Newton's method uses
$P_t=H_t^{-1}$ and natural gradient uses an inverse information geometry, but
storing or solving with dense $d\times d$ matrices is usually prohibitive.
AdaGrad, RMSProp, and Adam are inexpensive diagonal approximations: they cannot
remove rotated cross-coordinate curvature, but they can normalize unequal
coordinate scales.

### 9 · The optimizer family: what each method adds

**SGD** uses the current gradient and has no optimizer memory.
**Heavy-ball momentum** low-pass filters directions that persist across steps.
**Nesterov momentum** evaluates the gradient after a look-ahead displacement,
coupling prediction and correction. **AdaGrad** accumulates every squared
gradient, making its effective learning rate monotonically decrease. **RMSProp**
replaces that unbounded accumulator with an exponential window. **Adam** combines
an exponential first moment with RMSProp-like second-moment scaling and finite-time
bias correction. **AdamW** changes regularization, not the moment estimator.

$$
\text{AdaGrad:}\quad G_t=G_{t-1}+g_t\odot g_t,\qquad\theta_t=\theta_{t-1}-\alpha\frac{g_t}{\sqrt{G_t}+\varepsilon}.
$$

$$
\text{RMSProp:}\quad v_t=\beta_2v_{t-1}+(1-\beta_2)g_t\odot g_t,\qquad\theta_t=\theta_{t-1}-\alpha\frac{g_t}{\sqrt{v_t}+\varepsilon}.
$$

$$
\text{Nesterov:}\quad \widetilde\theta_t=\theta_t-\alpha\mu v_t,\quadv_{t+1}=\mu v_t+\nabla F(\widetilde\theta_t),\quad\theta_{t+1}=\theta_t-\alpha v_{t+1}.
$$

*State/parameter counts optimizer tensors, excluding the parameter and gradient. Mixed-precision training may also keep full-precision master weights.*

### 10 · A worked Adam step: why bias correction matters

Let $g_1=[4,\,0.5]^\top$, $\beta_1=0.9$, $\beta_2=0.999$, and initialize
$m_0=v_0=0$. Before correction,

$$
m_1=0.1g_1=[0.4,\,0.05]^\top,
$$

$$
v_1=0.001(g_1\odot g_1)=[0.016,\,0.00025]^\top.
$$

Applying the exact first-step corrections,

$$
\widehat m_1=\frac{m_1}{1-0.9}=g_1,\qquad\widehat v_1=\frac{v_1}{1-0.999}=g_1\odot g_1.
$$

$$
\Delta\theta_1=-\alpha\frac{g_1}{|g_1|+\varepsilon}\approx-\alpha[1,\,1]^\top.
$$

Thus the first Adam step is nearly sign descent: magnitude information is
normalized away coordinate-wise. Later, $m_t/\sqrt{v_t}$ encodes the ratio of
persistent signed direction to recent root-mean-square magnitude. This explains
both Adam's resilience to scale disparities and its inability to represent a
rotated dense inverse Hessian.

### 11 · Convergence caveats and important variants

Adam's intuitive moving averages do not guarantee convergence for every online
convex sequence. A problematic coordinate can receive an increasing effective
step because $v_t$ forgets old large gradients. AMSGrad prevents this particular
failure by maintaining a coordinate-wise nondecreasing denominator:

$$
v_t=\beta_2v_{t-1}+(1-\beta_2)g_t^2,\qquad\widetilde v_t=\max(\widetilde v_{t-1},v_t),\qquad\theta_t=\theta_{t-1}-\alpha_t\frac{m_t}{\sqrt{\widetilde v_t}+\varepsilon}.
$$

The result is not “Adam always fails”; it is that implementation details,
assumptions, and schedules matter. Other variants target different mechanisms:
RAdam adjusts early adaptive variance, AdaBelief tracks squared prediction error
$(g_t-m_t)^2$, LAMB/LARS use layer-wise trust ratios for very large batches, and
Adafactor factorizes second moments to reduce memory. These are not universally
superior replacements. Ask which failure mechanism is present before changing the
optimizer.

### 12 · Hyperparameters as time scales, not magic constants

An exponential average gives observation $g_{t-k}$ weight $(1-\beta)\beta^k$. Its characteristic memory is approximately

$$
\tau\approx\frac{1}{1-\beta}.
$$

Therefore $\beta_1=0.9$ remembers roughly 10 steps and $\beta_2=0.999$ roughly
1000 steps. Raising $\beta_2$ smooths noisy curvature estimates but reacts slowly
after distribution shifts. Lowering it adapts faster but makes the denominator
noisier. $\varepsilon$ controls the transition between normalized and effectively
unnormalized coordinates; changing it can matter in low precision.

A schedule makes the actual update scale $\alpha_t$, not a constant $\alpha$.
Warm-up limits early movement while activations, moments, and normalization
statistics settle. Cosine decay, inverse-square-root decay, or step decay then
lower the noise floor. Gradient clipping changes $g_t$ before moment estimation;
clipping by global norm preserves direction while capping magnitude:

$$
g_t^{\mathrm{clip}}=g_t\min\left(1,\frac{c}{\|g_t\|_2+\delta}\right).
$$

### 13 · AdamW in a real training system

A defensible baseline separates parameter groups:

- **Decay:** dense weight matrices in attention, MLPs, convolutions, and embeddings
  when norm control is intended.
- **Usually no decay:** biases and normalization scale/shift parameters.
- **Explicit decision required:** token/position embeddings, output heads, scalar
  temperatures, and physically meaningful robot parameters.
- **Order matters:** confirm whether the framework applies decay before or after
  the adaptive step and whether schedulers report the pre- or post-update rate.
- **Mixed precision:** unscale gradients before clipping; check overflow skips so
  moment and schedule counters do not advance inconsistently.
- **Distributed training:** global clipping and gradient averaging semantics must
  match the intended effective batch size.

```python
decay, no_decay = [], []
for name, parameter in model.named_parameters():
    if not parameter.requires_grad:
        continue
    if parameter.ndim < 2 or name.endswith("bias"):
        no_decay.append(parameter)
    else:
        decay.append(parameter)

optimizer = torch.optim.AdamW(
    [
        {"params": decay, "weight_decay": 0.01},
        {"params": no_decay, "weight_decay": 0.0},
    ],
    lr=3e-4,
    betas=(0.9, 0.999),
    eps=1e-8,
)
```

*This grouping is a baseline, not a theorem. Match exclusions to architecture and regularization intent.*

### 14 · Diagnostics, selection guide, and mastery checks

Log more than loss. At minimum inspect **gradient norm**, **update norm**,
**parameter norm**, **update-to-weight ratio**, learning rate, clipping fraction,
overflow/skip count, training–validation gap, and per-group statistics. A falling
loss with exploding parameter norm suggests weak regularization; tiny update ratios
with nonzero gradients suggest stale second moments or an exhausted schedule;
repeated clipping suggests the nominal learning rate or data scale is wrong.

**Mastery checks**

1. Re-derive the SGD stability interval and minimax scalar step for a quadratic.
2. Explain why Adam is invariant to a positive coordinate-wise rescaling of a
   stationary gradient at the first step, and where $\varepsilon$ breaks it.
3. Derive why $L_2$ and weight decay coincide for scalar-step SGD but not for Adam.
4. Predict which trajectory changes when $\beta_2$ moves from $0.999$ to $0.9$.
5. Design an ablation separating optimizer, schedule, clipping, and decay effects.
6. Given a training run, use logged update-to-weight ratios to identify frozen,
   unstable, or over-regularized parameter groups.

### 15 · Video masterclasses and source ledger

> [!video] Lecture companion
> [Open video](https://www.youtube.com/watch?v=JXQT_vxqwIs)

*DeepLearning.AI · Adam Optimization Algorithm*

> [!video] Lecture companion
> [Open video](https://www.youtube.com/watch?v=NE88eqLngkg)

*DeepBean · Momentum, RMSProp, AdaGrad, and Adam*

**Primary and implementation sources**\
[1] J. Duchi, E. Hazan, and Y. Singer, “Adaptive Subgradient Methods for
Online Learning and Stochastic Optimization,”
[JMLR 12](https://jmlr.org/papers/v12/duchi11a.html), 2011.\
[2] I. Sutskever, J. Martens, G. Dahl, and G. Hinton, “On the Importance of
Initialization and Momentum in Deep Learning,”
[ICML/PMLR 28](https://proceedings.mlr.press/v28/sutskever13.html), 2013.\
[3] D. P. Kingma and J. Ba, “Adam: A Method for Stochastic Optimization,”
[arXiv:1412.6980](https://arxiv.org/abs/1412.6980), 2014.\
[4] I. Loshchilov and F. Hutter, “Decoupled Weight Decay Regularization,”
[arXiv:1711.05101](https://arxiv.org/abs/1711.05101), 2017.\
[5] S. J. Reddi, S. Kale, and S. Kumar, “On the Convergence of Adam and Beyond,”
[arXiv:1904.09237](https://arxiv.org/abs/1904.09237), 2019.\
[6] PyTorch contributors, [torch.optim.AdamW reference](https://docs.pytorch.org/docs/stable/generated/torch.optim.AdamW.html), accessed 2026-08-29.
