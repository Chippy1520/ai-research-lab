"""Structural, numerical, roadmap, and persistence tests."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from curriculum import (
    DOMAINS,
    CurriculumState,
    advance_state,
    lesson_for_day,
    load_learning_log,
    load_plan,
    load_research_log,
    load_state,
    save_learning_reflection,
)
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


def test_roadmap_is_broad_contiguous_and_strictly_rotating() -> None:
    metadata, lessons = load_plan(ROOT / "curriculum_plan.json")
    horizon = metadata["horizon_policy"]
    assert horizon["mode"] == "rolling_open_ended"
    assert horizon["terminal_day"] is None
    assert horizon["minimum_mapped_ahead_days"] > 0
    assert horizon["extension_batch_cycles"] > 0
    assert len(lessons) >= 72
    assert [lesson.day for lesson in lessons] == list(range(1, len(lessons) + 1))
    assert [lesson.domain_index for lesson in lessons[:9]] == [0, 1, 2] * 3
    assert lesson_for_day(1, ROOT / "curriculum_plan.json").topic == (
        "Optimization Dynamics & AdamW"
    )
    assert lessons[-1].stage == "Live review"


def test_logs_have_day_one_provenance_and_archive_entry() -> None:
    learning = load_learning_log(ROOT / "learning_log.json")
    research = load_research_log(ROOT / "research_log.json")
    assert learning[0]["module_slug"] == "module_01"
    assert learning[0]["status"] == "ready"
    assert research[0]["module_slug"] == "module_01"
    assert len(research[0]["sources"]) >= 3
    assert all(source["url"].startswith("https://") for source in research[0]["sources"])


def test_learning_reflection_updates_a_copy_atomically(tmp_path: Path) -> None:
    temporary_log = tmp_path / "learning_log.json"
    temporary_log.write_text(
        (ROOT / "learning_log.json").read_text(encoding="utf-8"), encoding="utf-8"
    )
    saved = save_learning_reflection(
        1, 64, 4, "Re-derive bias correction.", True, True, temporary_log
    )
    assert saved["status"] == "completed"
    assert saved["minutes_spent"] == 64
    persisted = json.loads(temporary_log.read_text(encoding="utf-8"))["entries"][0]
    assert persisted["confidence"] == 4
    assert persisted["revisit"] is True
    assert not list(tmp_path.glob("*.tmp"))


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
