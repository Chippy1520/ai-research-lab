"""From-scratch AdamW reference implementation and deterministic demonstration."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

import torch
from torch import Tensor


class AdamW:
    """Optimize tensors using bias-corrected Adam and decoupled weight decay.

    Parameters
    ----------
    parameters:
        Iterable of leaf tensors whose ``.grad`` fields are populated.
    learning_rate:
        Positive step size :math:`\\alpha`.
    betas:
        Exponential decay rates :math:`(\\beta_1, \\beta_2)` in ``[0, 1)``.
    epsilon:
        Positive numerical-stability constant.
    weight_decay:
        Non-negative decoupled shrinkage coefficient :math:`\\lambda`.
    """

    def __init__(
        self,
        parameters: Iterable[Tensor],
        learning_rate: float = 1e-3,
        betas: tuple[float, float] = (0.9, 0.999),
        epsilon: float = 1e-8,
        weight_decay: float = 1e-2,
    ) -> None:
        self.parameters = list(parameters)
        self._validate(learning_rate, betas, epsilon, weight_decay)
        if not self.parameters:
            raise ValueError("parameters must contain at least one tensor")
        if any(not parameter.is_leaf for parameter in self.parameters):
            raise ValueError("AdamW can optimize only leaf tensors")

        self.learning_rate = float(learning_rate)
        self.beta1, self.beta2 = map(float, betas)
        self.epsilon = float(epsilon)
        self.weight_decay = float(weight_decay)
        self.step_index = 0
        self.first_moments = [torch.zeros_like(p) for p in self.parameters]
        self.second_moments = [torch.zeros_like(p) for p in self.parameters]

    @staticmethod
    def _validate(
        learning_rate: float,
        betas: tuple[float, float],
        epsilon: float,
        weight_decay: float,
    ) -> None:
        if learning_rate <= 0.0:
            raise ValueError("learning_rate must be positive")
        if len(betas) != 2 or any(not 0.0 <= beta < 1.0 for beta in betas):
            raise ValueError("both beta values must lie in [0, 1)")
        if epsilon <= 0.0:
            raise ValueError("epsilon must be positive")
        if weight_decay < 0.0:
            raise ValueError("weight_decay cannot be negative")

    @torch.no_grad()
    def step(self) -> None:
        """Apply one AdamW update to every parameter with a gradient."""
        self.step_index += 1
        correction1 = 1.0 - self.beta1**self.step_index
        correction2 = 1.0 - self.beta2**self.step_index

        for parameter, first, second in zip(
            self.parameters, self.first_moments, self.second_moments, strict=True
        ):
            gradient = parameter.grad
            if gradient is None:
                continue
            if gradient.is_sparse:
                raise RuntimeError("This reference AdamW does not support sparse gradients")

            # Decay is a direct parameter-space contraction, not part of g_t.
            parameter.mul_(1.0 - self.learning_rate * self.weight_decay)
            first.mul_(self.beta1).add_(gradient, alpha=1.0 - self.beta1)
            second.mul_(self.beta2).addcmul_(
                gradient, gradient, value=1.0 - self.beta2
            )
            first_hat = first / correction1
            second_hat = second / correction2
            parameter.addcdiv_(
                first_hat,
                second_hat.sqrt().add_(self.epsilon),
                value=-self.learning_rate,
            )

    def zero_grad(self) -> None:
        """Set existing gradients to ``None`` without allocating zero tensors."""
        for parameter in self.parameters:
            parameter.grad = None

    def state_dict(self) -> dict[str, Any]:
        """Return serializable optimizer state for checkpointing."""
        return {
            "step_index": self.step_index,
            "learning_rate": self.learning_rate,
            "betas": (self.beta1, self.beta2),
            "epsilon": self.epsilon,
            "weight_decay": self.weight_decay,
            "first_moments": [moment.clone() for moment in self.first_moments],
            "second_moments": [moment.clone() for moment in self.second_moments],
        }


def run_quadratic_demo(steps: int = 500) -> tuple[Tensor, float]:
    """Minimize an anisotropic quadratic and return parameters and final loss."""
    if steps < 1:
        raise ValueError("steps must be at least one")
    torch.manual_seed(7)
    parameter = torch.tensor([4.0, -3.0], dtype=torch.float64, requires_grad=True)
    hessian = torch.tensor([[40.0, 0.0], [0.0, 1.0]], dtype=torch.float64)
    target = torch.tensor([1.0, 1.0], dtype=torch.float64)
    optimizer = AdamW([parameter], learning_rate=0.05, weight_decay=0.01)

    loss = torch.tensor(float("inf"), dtype=torch.float64)
    for _ in range(steps):
        displacement = parameter - target
        loss = 0.5 * displacement @ hessian @ displacement
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()

    displacement = parameter.detach() - target
    final_loss = float(0.5 * displacement @ hessian @ displacement)
    return parameter.detach(), final_loss


if __name__ == "__main__":
    solution, objective = run_quadratic_demo()
    print(f"solution={solution.tolist()}, loss={objective:.6e}")
