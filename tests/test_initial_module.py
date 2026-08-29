"""Fast structural and numerical tests for the initial research module."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from curriculum import DOMAINS, CurriculumState, advance_state, load_state
from modules.module_01 import _objective, _quadratic_geometry, _simulate

ROOT = Path(__file__).resolve().parents[1]


def test_initial_state_matches_contract() -> None:
    state = load_state(ROOT / "curriculum_state.json")
    assert state.current_day == 1
    assert state.current_domain_index == 0
    assert state.completed_modules == []
    assert DOMAINS[state.current_domain_index] == "Machine Learning"


def test_state_rotation_is_strict() -> None:
    state = CurriculumState(1, [], 0, "2026-08-29")
    indices = []
    for day in range(1, 7):
        indices.append(state.current_domain_index)
        state = advance_state(state, f"module_{day:02d}")
    assert indices == [0, 1, 2, 0, 1, 2]


def test_quadratic_hessian_has_requested_condition_number() -> None:
    hessian, _ = _quadratic_geometry(40.0, 37.0)
    eigenvalues = np.linalg.eigvalsh(hessian)
    assert np.isclose(eigenvalues[-1] / eigenvalues[0], 40.0)
    assert np.all(eigenvalues > 0.0)


def test_adamw_simulation_is_finite_and_decreases_loss() -> None:
    hessian, optimum = _quadratic_geometry(25.0, 32.0)
    trajectory, losses = _simulate(
        "AdamW", hessian, optimum, 0.045, 0.9, 0.99, 0.02, 140
    )
    assert trajectory.shape == (141, 2)
    assert np.all(np.isfinite(trajectory))
    assert losses[-1] < losses[0] * 5e-3
    assert _objective(optimum, hessian, optimum) == 0.0


def test_state_json_remains_machine_readable() -> None:
    payload = json.loads((ROOT / "curriculum_state.json").read_text(encoding="utf-8"))
    assert set(payload) == {
        "current_day",
        "completed_modules",
        "current_domain_index",
        "last_updated",
    }
