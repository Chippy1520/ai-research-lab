"""Day 1 — optimization dynamics, Adam bias correction, and AdamW."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import plotly.graph_objects as go
import streamlit as st
from numpy.typing import NDArray

METADATA = {
    "day": 1,
    "title": "Optimization Dynamics & AdamW",
    "domain": "Machine Learning",
    "duration_minutes": 60,
}

ROOT = Path(__file__).resolve().parents[1]


def _render_article() -> None:
    """Render the self-contained technical chapter."""
    st.header("Optimization as a discrete-time dynamical system")
    st.markdown(
        """
        <div class="research-note"><b>Research objective.</b> Derive how curvature,
        momentum, adaptive preconditioning, finite-time moment bias, and decoupled
        regularization determine an optimizer's trajectory—not merely its final loss.</div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("1 · Executive summary and engineering motivation")
    st.markdown(
        r"""
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
        """
    )

    st.subheader("2 · Local quadratic model and why naive descent fails")
    st.markdown(
        r"""
        Around a strict local minimizer $\theta^\star$, a twice-differentiable objective
        admits the second-order approximation
        """
    )
    st.latex(
        r"\mathcal L(\theta) \approx \mathcal L(\theta^\star) + "
        r"\frac{1}{2}(\theta-\theta^\star)^\top H(\theta-\theta^\star), "
        r"\qquad H=H^\top\succ 0."
    )
    st.markdown(r"Define the error $e_t=\theta_t-\theta^\star$. Then")
    st.latex(r"\nabla_\theta \mathcal L(\theta_t)=He_t,")
    st.latex(
        r"\theta_{t+1}=\theta_t-\alpha H e_t "
        r"\quad\Longrightarrow\quad e_{t+1}=(I-\alpha H)e_t."
    )
    st.markdown(
        r"""
        Since $H$ is real symmetric, write $H=Q\Lambda Q^\top$, where
        $Q^\top Q=I$ and $\Lambda=\operatorname{diag}(\lambda_1,\ldots,\lambda_d)$.
        Rotating into the eigenbasis with $z_t=Q^\top e_t$ gives
        """
    )
    st.latex(
        r"z_{t+1}=Q^\top(I-\alpha Q\Lambda Q^\top)Qz_t"
        r"=(I-\alpha\Lambda)z_t."
    )
    st.latex(r"z_{t+1,i}=(1-\alpha\lambda_i)z_{t,i}"
             r"=(1-\alpha\lambda_i)^{t+1}z_{0,i}.")
    st.markdown(
        r"""
        Convergence for every eigendirection requires
        $|1-\alpha\lambda_i|<1$. Unrolling both inequalities,
        """
    )
    st.latex(
        r"-1<1-\alpha\lambda_i<1"
        r"\Longrightarrow -2<-\alpha\lambda_i<0"
        r"\Longrightarrow 0<\alpha\lambda_i<2."
    )
    st.latex(r"\boxed{0<\alpha<\frac{2}{\lambda_{\max}(H)}}")
    st.markdown(
        r"""
        A high condition number $\kappa(H)=\lambda_{\max}/\lambda_{\min}$ creates a
        narrow valley. Stability is dictated by $\lambda_{\max}$, while progress along
        the shallow direction scales with $\lambda_{\min}$. Thus stable SGD zig-zags
        across the steep axis and crawls along the shallow axis.
        """
    )

    st.subheader("3 · Momentum as a second-order recurrence")
    st.latex(
        r"v_t=\mu v_{t-1}+g_t,\qquad "
        r"\theta_{t+1}=\theta_t-\alpha v_t."
    )
    st.markdown(
        r"For one Hessian eigendirection with curvature $\lambda$, "
        r"$g_t=\lambda e_t$ and $\alpha v_{t-1}=e_{t-1}-e_t$. Substitution gives"
    )
    st.latex(
        r"e_{t+1}=e_t-\alpha(\mu v_{t-1}+\lambda e_t)"
        r"=(1-\alpha\lambda)e_t-\mu(e_{t-1}-e_t)"
        r"=(1+\mu-\alpha\lambda)e_t-\mu e_{t-1}."
    )
    st.latex(
        r"r^2-(1+\mu-\alpha\lambda)r+\mu=0."
    )
    st.markdown(
        r"""
        The characteristic roots determine damping. Real roots inside the unit circle
        give monotone or over-damped convergence; complex roots produce oscillation with
        envelope approximately controlled by $\sqrt{\mu}$. Momentum accumulates
        persistent low-curvature gradients while rapidly alternating steep-direction
        gradients partially cancel.
        """
    )

    st.subheader("4 · Adam: moment estimation and diagonal preconditioning")
    st.markdown(r"For stochastic gradient $g_t=\nabla_\theta\ell(\theta_{t-1};\xi_t)$,")
    st.latex(r"m_t=\beta_1m_{t-1}+(1-\beta_1)g_t,")
    st.latex(r"v_t=\beta_2v_{t-1}+(1-\beta_2)(g_t\odot g_t).")
    st.markdown(
        r"""
        Here $m_t$ estimates the first moment and $v_t$ estimates the uncentered second
        moment coordinate-wise. Expanding the first recurrence from $m_0=0$ yields
        """
    )
    st.latex(
        r"m_t=(1-\beta_1)\sum_{i=1}^{t}\beta_1^{t-i}g_i."
    )
    st.markdown(
        r"If $\mathbb E[g_i]=\mu_g$ is locally stationary, then the expected value is"
    )
    st.latex(
        r"\mathbb E[m_t]=(1-\beta_1)\sum_{i=1}^{t}\beta_1^{t-i}\mu_g"
        r"=(1-\beta_1)\mu_g\sum_{k=0}^{t-1}\beta_1^k."
    )
    st.latex(
        r"\sum_{k=0}^{t-1}\beta_1^k=\frac{1-\beta_1^t}{1-\beta_1}"
        r"\quad\Longrightarrow\quad\mathbb E[m_t]=(1-\beta_1^t)\mu_g."
    )
    st.markdown(
        r"The zero initialization therefore attenuates early moments. Dividing by the "
        r"known attenuation gives the bias-corrected estimators"
    )
    st.latex(
        r"\widehat m_t=\frac{m_t}{1-\beta_1^t},\qquad"
        r"\widehat v_t=\frac{v_t}{1-\beta_2^t}."
    )
    st.latex(
        r"\theta_t=\theta_{t-1}-\alpha\frac{\widehat m_t}"
        r"{\sqrt{\widehat v_t}+\varepsilon}."
    )
    st.markdown(
        r"""
        The denominator is an online diagonal preconditioner. A coordinate with
        repeatedly large squared gradients receives a smaller effective step, while a
        coordinate with small or sparse gradients receives a relatively larger one.
        The $\varepsilon$ term is not only a divide-by-zero guard: when
        $\sqrt{\widehat v_{t,i}}\ll\varepsilon$, it sets the coordinate's effective
        learning-rate ceiling.
        """
    )

    st.subheader("5 · Why $L_2$ inside Adam is not weight decay")
    st.markdown(
        r"""
        For plain SGD, adding $\frac{\lambda}{2}\|\theta\|_2^2$ to the loss produces
        $g_t+\lambda\theta_t$ and therefore
        """
    )
    st.latex(
        r"\theta_{t+1}=\theta_t-\alpha(g_t+\lambda\theta_t)"
        r"=(1-\alpha\lambda)\theta_t-\alpha g_t."
    )
    st.markdown(
        r"""
        This is exactly multiplicative weight decay. For an adaptive optimizer with
        diagonal preconditioner $D_t=\operatorname{diag}
        (1/(\sqrt{\widehat v_t}+\varepsilon))$, placing the penalty in the gradient gives
        """
    )
    st.latex(
        r"\theta_{t+1}=\theta_t-\alpha D_t(g_t+\lambda\theta_t)"
        r"=(I-\alpha\lambda D_t)\theta_t-\alpha D_tg_t."
    )
    st.markdown(
        r"""
        The shrinkage matrix $I-\alpha\lambda D_t$ now varies by coordinate and time.
        Parameters with large historical gradients are regularized less. Hence the
        claimed weight decay has become entangled with the optimizer state.
        AdamW restores a uniform contraction by separating the operations:
        """
    )
    st.latex(
        r"\boxed{\theta_t=(1-\alpha\lambda)\theta_{t-1}"
        r"-\alpha\frac{\widehat m_t}{\sqrt{\widehat v_t}+\varepsilon}}"
    )
    st.markdown(
        r"""
        Decoupling also makes learning-rate and regularization tuning more nearly
        orthogonal. In production, parameter groups commonly exclude biases and
        normalization scale/shift parameters from decay because their norms do not play
        the same capacity-control role as weight matrices.
        """
    )

    st.subheader("6 · Failure modes and research practice")
    st.markdown(
        """
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
        """
    )

    _render_optimizer_landscape()

    st.subheader("15 · Video masterclasses and source ledger")
    video_left, video_right = st.columns(2)
    with video_left:
        st.video("https://www.youtube.com/watch?v=JXQT_vxqwIs")
        st.caption("DeepLearning.AI · Adam Optimization Algorithm")
    with video_right:
        st.video("https://www.youtube.com/watch?v=NE88eqLngkg")
        st.caption("DeepBean · Momentum, RMSProp, AdaGrad, and Adam")
    st.markdown(
        """
        <div class="citation">
        <b>Primary and implementation sources</b><br>
        [1] J. Duchi, E. Hazan, and Y. Singer, “Adaptive Subgradient Methods for
        Online Learning and Stochastic Optimization,”
        <a href="https://jmlr.org/papers/v12/duchi11a.html">JMLR 12</a>, 2011.<br>
        [2] I. Sutskever, J. Martens, G. Dahl, and G. Hinton, “On the Importance of
        Initialization and Momentum in Deep Learning,”
        <a href="https://proceedings.mlr.press/v28/sutskever13.html">ICML/PMLR 28</a>, 2013.<br>
        [3] D. P. Kingma and J. Ba, “Adam: A Method for Stochastic Optimization,”
        <a href="https://arxiv.org/abs/1412.6980">arXiv:1412.6980</a>, 2014.<br>
        [4] I. Loshchilov and F. Hutter, “Decoupled Weight Decay Regularization,”
        <a href="https://arxiv.org/abs/1711.05101">arXiv:1711.05101</a>, 2017.<br>
        [5] S. J. Reddi, S. Kale, and S. Kumar, “On the Convergence of Adam and Beyond,”
        <a href="https://arxiv.org/abs/1904.09237">arXiv:1904.09237</a>, 2019.<br>
        [6] PyTorch contributors, <a href="https://docs.pytorch.org/docs/stable/generated/torch.optim.AdamW.html">
        torch.optim.AdamW reference</a>, accessed 2026-08-29.
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_optimizer_landscape() -> None:
    """Connect AdamW to the wider optimization family and production practice."""
    st.subheader("7 · What problem are we actually optimizing?")
    st.markdown(
        r"""
        Supervised learning usually minimizes empirical risk plus an explicit
        regularizer. For parameters $\theta\in\mathbb R^d$, data
        $\mathcal D=\{(x_i,y_i)\}_{i=1}^{N}$, per-example loss $\ell_i$, and
        regularizer $R$, the finite-sum problem is
        """
    )
    st.latex(
        r"F(\theta)=\frac{1}{N}\sum_{i=1}^{N}\ell_i(\theta)+\lambda R(\theta)."
    )
    st.markdown(
        r"""
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
        """
    )

    st.subheader("8 · Conditioning, optimal scalar steps, and preconditioning")
    st.markdown(
        r"For a positive-definite quadratic with eigenvalues in $[\mu,L]$, the worst "
        r"one-step contraction under scalar-step gradient descent is"
    )
    st.latex(
        r"\rho(\alpha)=\max_{\lambda\in[\mu,L]}|1-\alpha\lambda|."
    )
    st.markdown(
        r"The minimax choice balances the endpoint magnitudes: "
        r"$1-\alpha\mu=-(1-\alpha L)$. Solving explicitly,"
    )
    st.latex(
        r"1-\alpha\mu=-1+\alpha L"
        r"\Longrightarrow 2=\alpha(L+\mu)"
        r"\Longrightarrow \alpha^\star=\frac{2}{L+\mu}."
    )
    st.latex(
        r"\rho^\star=1-\alpha^\star\mu"
        r"=1-\frac{2\mu}{L+\mu}"
        r"=\frac{L-\mu}{L+\mu}"
        r"=\frac{\kappa-1}{\kappa+1}."
    )
    st.markdown(
        r"""
        As $\kappa=L/\mu$ grows, $\rho^\star\to1$ and progress slows. A positive-definite
        preconditioner $P_t$ changes the update to
        $\theta_{t+1}=\theta_t-\alpha P_tg_t$. Newton's method uses
        $P_t=H_t^{-1}$ and natural gradient uses an inverse information geometry, but
        storing or solving with dense $d\times d$ matrices is usually prohibitive.
        AdaGrad, RMSProp, and Adam are inexpensive diagonal approximations: they cannot
        remove rotated cross-coordinate curvature, but they can normalize unequal
        coordinate scales.
        """
    )

    st.subheader("9 · The optimizer family: what each method adds")
    st.markdown(
        r"""
        **SGD** uses the current gradient and has no optimizer memory.
        **Heavy-ball momentum** low-pass filters directions that persist across steps.
        **Nesterov momentum** evaluates the gradient after a look-ahead displacement,
        coupling prediction and correction. **AdaGrad** accumulates every squared
        gradient, making its effective learning rate monotonically decrease. **RMSProp**
        replaces that unbounded accumulator with an exponential window. **Adam** combines
        an exponential first moment with RMSProp-like second-moment scaling and finite-time
        bias correction. **AdamW** changes regularization, not the moment estimator.
        """
    )
    st.latex(
        r"\text{AdaGrad:}\quad G_t=G_{t-1}+g_t\odot g_t,\qquad"
        r"\theta_t=\theta_{t-1}-\alpha\frac{g_t}{\sqrt{G_t}+\varepsilon}."
    )
    st.latex(
        r"\text{RMSProp:}\quad v_t=\beta_2v_{t-1}+(1-\beta_2)g_t\odot g_t,\qquad"
        r"\theta_t=\theta_{t-1}-\alpha\frac{g_t}{\sqrt{v_t}+\varepsilon}."
    )
    st.latex(
        r"\text{Nesterov:}\quad \widetilde\theta_t=\theta_t-\alpha\mu v_t,\quad"
        r"v_{t+1}=\mu v_t+\nabla F(\widetilde\theta_t),\quad"
        r"\theta_{t+1}=\theta_t-\alpha v_{t+1}."
    )
    st.dataframe(
        [
            {"Method": "SGD", "State/parameter": "0", "Adaptation": "none", "Strength": "simple; low memory", "Typical weakness": "conditioning; noisy zig-zag"},
            {"Method": "Momentum", "State/parameter": "1", "Adaptation": "temporal direction", "Strength": "accelerates persistent gradients", "Typical weakness": "oscillation; coupled tuning"},
            {"Method": "AdaGrad", "State/parameter": "1", "Adaptation": "cumulative coordinate scale", "Strength": "sparse features; convex regret", "Typical weakness": "learning rate can vanish"},
            {"Method": "RMSProp", "State/parameter": "1", "Adaptation": "recent coordinate scale", "Strength": "nonstationary scaling", "Typical weakness": "no first-moment smoothing"},
            {"Method": "Adam", "State/parameter": "2", "Adaptation": "direction + coordinate scale", "Strength": "fast robust defaults", "Typical weakness": "coupled L2; convergence edge cases"},
            {"Method": "AdamW", "State/parameter": "2", "Adaptation": "Adam + uniform decay", "Strength": "predictable norm control", "Typical weakness": "extra memory; decay/schedule interaction"},
        ],
        hide_index=True,
        width="stretch",
    )
    st.caption(
        "State/parameter counts optimizer tensors, excluding the parameter and gradient. "
        "Mixed-precision training may also keep full-precision master weights."
    )

    st.subheader("10 · A worked Adam step: why bias correction matters")
    st.markdown(
        r"""
        Let $g_1=[4,\,0.5]^\top$, $\beta_1=0.9$, $\beta_2=0.999$, and initialize
        $m_0=v_0=0$. Before correction,
        """
    )
    st.latex(r"m_1=0.1g_1=[0.4,\,0.05]^\top,")
    st.latex(r"v_1=0.001(g_1\odot g_1)=[0.016,\,0.00025]^\top.")
    st.markdown("Applying the exact first-step corrections,")
    st.latex(
        r"\widehat m_1=\frac{m_1}{1-0.9}=g_1,\qquad"
        r"\widehat v_1=\frac{v_1}{1-0.999}=g_1\odot g_1."
    )
    st.latex(
        r"\Delta\theta_1=-\alpha\frac{g_1}{|g_1|+\varepsilon}"
        r"\approx-\alpha[1,\,1]^\top."
    )
    st.markdown(
        r"""
        Thus the first Adam step is nearly sign descent: magnitude information is
        normalized away coordinate-wise. Later, $m_t/\sqrt{v_t}$ encodes the ratio of
        persistent signed direction to recent root-mean-square magnitude. This explains
        both Adam's resilience to scale disparities and its inability to represent a
        rotated dense inverse Hessian.
        """
    )

    st.subheader("11 · Convergence caveats and important variants")
    st.markdown(
        r"""
        Adam's intuitive moving averages do not guarantee convergence for every online
        convex sequence. A problematic coordinate can receive an increasing effective
        step because $v_t$ forgets old large gradients. AMSGrad prevents this particular
        failure by maintaining a coordinate-wise nondecreasing denominator:
        """
    )
    st.latex(
        r"v_t=\beta_2v_{t-1}+(1-\beta_2)g_t^2,\qquad"
        r"\widetilde v_t=\max(\widetilde v_{t-1},v_t),\qquad"
        r"\theta_t=\theta_{t-1}-\alpha_t\frac{m_t}{\sqrt{\widetilde v_t}+\varepsilon}."
    )
    st.markdown(
        r"""
        The result is not “Adam always fails”; it is that implementation details,
        assumptions, and schedules matter. Other variants target different mechanisms:
        RAdam adjusts early adaptive variance, AdaBelief tracks squared prediction error
        $(g_t-m_t)^2$, LAMB/LARS use layer-wise trust ratios for very large batches, and
        Adafactor factorizes second moments to reduce memory. These are not universally
        superior replacements. Ask which failure mechanism is present before changing the
        optimizer.
        """
    )

    st.subheader("12 · Hyperparameters as time scales, not magic constants")
    st.markdown(
        r"An exponential average gives observation $g_{t-k}$ weight "
        r"$(1-\beta)\beta^k$. Its characteristic memory is approximately"
    )
    st.latex(r"\tau\approx\frac{1}{1-\beta}.")
    st.markdown(
        r"""
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
        """
    )
    st.latex(
        r"g_t^{\mathrm{clip}}=g_t\min\left(1,\frac{c}{\|g_t\|_2+\delta}\right)."
    )

    st.subheader("13 · AdamW in a real training system")
    st.markdown(
        """
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
        """
    )
    st.code(
        """decay, no_decay = [], []
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
""",
        language="python",
    )
    st.caption(
        "This grouping is a baseline, not a theorem. Match exclusions to architecture "
        "and regularization intent."
    )

    st.subheader("14 · Diagnostics, selection guide, and mastery checks")
    st.markdown(
        """
        Log more than loss. At minimum inspect **gradient norm**, **update norm**,
        **parameter norm**, **update-to-weight ratio**, learning rate, clipping fraction,
        overflow/skip count, training–validation gap, and per-group statistics. A falling
        loss with exploding parameter norm suggests weak regularization; tiny update ratios
        with nonzero gradients suggest stale second moments or an exhausted schedule;
        repeated clipping suggests the nominal learning rate or data scale is wrong.
        """
    )
    st.dataframe(
        [
            {"Observed regime": "Well-scaled dense supervised problem", "Start with": "SGD + momentum", "Reason": "low memory; often strong final generalization"},
            {"Observed regime": "Sparse or highly unequal feature frequencies", "Start with": "AdaGrad or AdamW", "Reason": "coordinate adaptation"},
            {"Observed regime": "Transformer/diffusion baseline", "Start with": "AdamW + warm-up + decay schedule", "Reason": "established robust recipe"},
            {"Observed regime": "Very large batch", "Start with": "AdamW, LAMB/LARS only if needed", "Reason": "trust ratios target layer-scale mismatch"},
            {"Observed regime": "Memory-limited large model", "Start with": "Adafactor or optimizer-state sharding", "Reason": "reduce two-state-tensor cost"},
            {"Observed regime": "Nonstationary online objective", "Start with": "RMSProp/AdamW with shorter second-moment memory", "Reason": "faster scale adaptation"},
        ],
        hide_index=True,
        width="stretch",
    )
    st.markdown(
        r"""
        **Mastery checks**

        1. Re-derive the SGD stability interval and minimax scalar step for a quadratic.
        2. Explain why Adam is invariant to a positive coordinate-wise rescaling of a
           stationary gradient at the first step, and where $\varepsilon$ breaks it.
        3. Derive why $L_2$ and weight decay coincide for scalar-step SGD but not for Adam.
        4. Predict which trajectory changes when $\beta_2$ moves from $0.999$ to $0.9$.
        5. Design an ablation separating optimizer, schedule, clipping, and decay effects.
        6. Given a training run, use logged update-to-weight ratios to identify frozen,
           unstable, or over-regularized parameter groups.
        """
    )



def _quadratic_geometry(
    condition_number: float, rotation_degrees: float
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Return Hessian and minimizer for the simulator's quadratic objective."""
    angle = np.deg2rad(rotation_degrees)
    rotation = np.array(
        [[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]],
        dtype=np.float64,
    )
    eigenvalues = np.diag([1.0, condition_number])
    hessian = rotation @ eigenvalues @ rotation.T
    optimum = np.array([1.0, -1.0], dtype=np.float64)
    return hessian, optimum


def _objective(
    points: NDArray[np.float64],
    hessian: NDArray[np.float64],
    optimum: NDArray[np.float64],
) -> NDArray[np.float64]:
    """Evaluate 0.5*(x-x*)^T H (x-x*) for one point or a point batch."""
    displacement = points - optimum
    return 0.5 * np.einsum("...i,ij,...j->...", displacement, hessian, displacement)


def _simulate(
    method: str,
    hessian: NDArray[np.float64],
    optimum: NDArray[np.float64],
    learning_rate: float,
    beta1: float,
    beta2: float,
    weight_decay: float,
    iterations: int,
    noise_std: float = 0.0,
    seed: int = 7,
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Simulate first-order optimizers with shared seeded gradient noise."""
    if noise_std < 0.0:
        raise ValueError("noise_std cannot be negative")
    if iterations < 1:
        raise ValueError("iterations must be positive")
    supported = {"SGD", "Momentum", "AdaGrad", "RMSProp", "AdamW"}
    if method not in supported:
        raise ValueError(f"Unknown optimization method: {method}")
    generator = np.random.default_rng(seed)
    parameter = np.array([-3.6, 3.2], dtype=np.float64)
    first = np.zeros(2, dtype=np.float64)
    second = np.zeros(2, dtype=np.float64)
    trajectory = [parameter.copy()]
    losses = [float(_objective(parameter, hessian, optimum))]

    for step in range(1, iterations + 1):
        gradient = hessian @ (parameter - optimum)
        gradient += generator.normal(0.0, noise_std, size=gradient.shape)
        if method == "SGD":
            parameter -= learning_rate * gradient
        elif method == "Momentum":
            first = beta1 * first + gradient
            parameter -= learning_rate * first
        elif method == "AdaGrad":
            second += np.square(gradient)
            parameter -= learning_rate * gradient / (np.sqrt(second) + 1e-8)
        elif method == "RMSProp":
            second = beta2 * second + (1.0 - beta2) * np.square(gradient)
            parameter -= learning_rate * gradient / (np.sqrt(second) + 1e-8)
        elif method == "AdamW":
            first = beta1 * first + (1.0 - beta1) * gradient
            second = beta2 * second + (1.0 - beta2) * np.square(gradient)
            first_hat = first / (1.0 - beta1**step)
            second_hat = second / (1.0 - beta2**step)
            parameter *= 1.0 - learning_rate * weight_decay
            parameter -= learning_rate * first_hat / (np.sqrt(second_hat) + 1e-8)
        trajectory.append(parameter.copy())
        losses.append(float(_objective(parameter, hessian, optimum)))

    return np.asarray(trajectory), np.asarray(losses)


def _render_simulator() -> None:
    """Render interactive loss geometry and optimizer trajectories."""
    st.header("Interactive anisotropic-quadratic laboratory")
    st.markdown(
        r"The controlled objective is $f(x)=\frac12(x-x^\star)^\top H(x-x^\star)$ "
        r"with eigenvalues $1$ and $\kappa$. Rotate $H$ to separate coordinate axes "
        r"from curvature axes, then compare the resulting discrete trajectories."
    )

    first_row = st.columns(4)
    condition_number = first_row[0].slider("Condition number κ", 1.0, 80.0, 25.0, 1.0)
    rotation = first_row[1].slider("Valley rotation (degrees)", 0.0, 90.0, 32.0, 1.0)
    learning_rate = first_row[2].slider(
        "Base learning rate α", 0.001, 0.200, 0.045, 0.001, format="%.3f"
    )
    iterations = first_row[3].slider("Iterations", 20, 300, 140, 10)

    second_row = st.columns(4)
    beta1 = second_row[0].slider("β₁ / momentum", 0.0, 0.99, 0.90, 0.01)
    beta2 = second_row[1].slider("β₂", 0.80, 0.9999, 0.990, 0.001, format="%.4f")
    weight_decay = second_row[2].slider("AdamW decay λ", 0.0, 0.20, 0.02, 0.005)
    noise_std = second_row[3].slider("Gradient-noise σ", 0.0, 5.0, 0.0, 0.1)

    all_methods = ["SGD", "Momentum", "AdaGrad", "RMSProp", "AdamW"]
    selected_methods = st.multiselect(
        "Optimizer traces", all_methods, default=all_methods
    )
    if not selected_methods:
        st.info("Select at least one optimizer trace.")
        return

    hessian, optimum = _quadratic_geometry(condition_number, rotation)
    axis = np.linspace(-4.2, 4.2, 95)
    x_grid, y_grid = np.meshgrid(axis, axis)
    points = np.stack([x_grid, y_grid], axis=-1)
    z_grid = _objective(points, hessian, optimum)
    display_ceiling = float(np.quantile(z_grid, 0.82))
    z_display = np.minimum(z_grid, display_ceiling)

    colors = {
        "SGD": "#fb7185",
        "Momentum": "#fbbf24",
        "AdaGrad": "#a78bfa",
        "RMSProp": "#4ade80",
        "AdamW": "#38bdf8",
    }
    simulations = {
        method: _simulate(
            method,
            hessian,
            optimum,
            learning_rate,
            beta1,
            beta2,
            weight_decay,
            iterations,
            noise_std,
        )
        for method in selected_methods
    }

    surface = go.Figure(
        data=[
            go.Surface(
                x=x_grid,
                y=y_grid,
                z=z_display,
                colorscale="Viridis",
                opacity=0.72,
                showscale=False,
                name="loss surface",
            )
        ]
    )
    for method, (trajectory, losses) in simulations.items():
        clipped = np.minimum(losses, display_ceiling) + 0.02 * display_ceiling
        surface.add_trace(
            go.Scatter3d(
                x=trajectory[:, 0],
                y=trajectory[:, 1],
                z=clipped,
                mode="lines+markers",
                marker={"size": 2.5, "color": colors[method]},
                line={"width": 5, "color": colors[method]},
                name=method,
            )
        )
    surface.update_layout(
        template="plotly_dark",
        height=610,
        margin={"l": 0, "r": 0, "t": 35, "b": 0},
        title="Optimizer trajectories on rotated loss geometry (upper surface clipped)",
        scene={
            "xaxis_title": "θ₁",
            "yaxis_title": "θ₂",
            "zaxis_title": "f(θ)",
            "camera": {"eye": {"x": 1.55, "y": 1.55, "z": 1.05}},
        },
    )

    convergence = go.Figure()
    for method, (_, losses) in simulations.items():
        convergence.add_trace(
            go.Scatter(
                x=np.arange(losses.size),
                y=np.maximum(losses, 1e-14),
                mode="lines",
                line={"width": 2.5, "color": colors[method]},
                name=method,
            )
        )
    convergence.update_layout(
        template="plotly_dark",
        height=440,
        margin={"l": 30, "r": 15, "t": 45, "b": 35},
        title="Objective convergence",
        xaxis_title="Iteration",
        yaxis_title="Quadratic objective",
        yaxis_type="log",
        hovermode="x unified",
    )

    left, right = st.columns([1.35, 1.0])
    left.plotly_chart(surface, width="stretch")
    right.plotly_chart(convergence, width="stretch")

    final_columns = st.columns(len(simulations))
    for column, method in zip(final_columns, simulations, strict=True):
        trajectory, losses = simulations[method]
        distance = np.linalg.norm(trajectory[-1] - optimum)
        column.metric(method, f"loss {losses[-1]:.3e}", f"‖θ−θ*‖ {distance:.3e}")

    stability_limit = 2.0 / condition_number
    if learning_rate >= stability_limit:
        st.warning(
            f"For plain SGD, α={learning_rate:.3f} violates the quadratic stability "
            f"bound 2/λ_max={stability_limit:.3f}. Divergence is expected."
        )
    st.caption(
        "Every optimizer receives the same seeded noise sequence for a fair comparison. "
        "The surface remains deterministic; σ perturbs observed gradients, approximating "
        "minibatch noise without claiming a complete stochastic-training model."
    )


def _render_code() -> None:
    """Display the executable reference implementation without duplicating source."""
    st.header("Complete from-scratch PyTorch AdamW")
    st.markdown(
        "The code below is the exact executable file at "
        "`experiments/adamw_reference.py`. It includes validation, bias correction, "
        "decoupled decay, checkpoint state, and a deterministic quadratic smoke test."
    )
    source_path = ROOT / "experiments" / "adamw_reference.py"
    st.code(source_path.read_text(encoding="utf-8"), language="python", line_numbers=True)
    st.markdown("Run it directly:")
    st.code("python experiments/adamw_reference.py", language="bash")


def render() -> None:
    """Render the article, simulator, and code tabs required by the module contract."""
    tab_article, tab_sim, tab_code = st.tabs(
        ["Technical article", "Interactive simulator", "Complete code"]
    )
    with tab_article:
        _render_article()
    with tab_sim:
        _render_simulator()
    with tab_code:
        _render_code()
