"""Curriculum state and domain-rotation utilities.

The state file is deliberately human-readable and updated atomically so a failed
module-generation process cannot corrupt curriculum progress.
"""

from __future__ import annotations

import json
import os
import tempfile
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path
from typing import Any

STATE_PATH = Path(__file__).with_name("curriculum_state.json")
DOMAINS: tuple[str, ...] = (
    "Machine Learning",
    "Computer Vision",
    "Embodied AI & RL Robotics",
)


@dataclass(frozen=True)
class CurriculumState:
    """Validated persistent curriculum cursor."""

    current_day: int
    completed_modules: list[str]
    current_domain_index: int
    last_updated: str

    @classmethod
    def from_mapping(cls, payload: dict[str, Any]) -> "CurriculumState":
        """Construct and validate a state from decoded JSON."""
        state = cls(
            current_day=int(payload["current_day"]),
            completed_modules=list(payload["completed_modules"]),
            current_domain_index=int(payload["current_domain_index"]),
            last_updated=str(payload["last_updated"]),
        )
        if state.current_day < 1:
            raise ValueError("current_day must be at least 1")
        if not 0 <= state.current_domain_index < len(DOMAINS):
            raise ValueError("current_domain_index is outside the domain rotation")
        if not all(isinstance(item, str) for item in state.completed_modules):
            raise TypeError("completed_modules must contain only strings")
        date.fromisoformat(state.last_updated)
        return state


def load_state(path: Path = STATE_PATH) -> CurriculumState:
    """Read and validate curriculum state from *path*."""
    with path.open("r", encoding="utf-8") as stream:
        return CurriculumState.from_mapping(json.load(stream))


def save_state(state: CurriculumState, path: Path = STATE_PATH) -> None:
    """Atomically persist *state* as indented JSON."""
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        dir=path.parent, prefix=f".{path.name}.", suffix=".tmp", text=True
    )
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            json.dump(asdict(state), stream, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary_name, path)
    except BaseException:
        Path(temporary_name).unlink(missing_ok=True)
        raise


def advance_state(state: CurriculumState, completed_slug: str) -> CurriculumState:
    """Return the next daily cursor under strict ML→CV→EAI rotation."""
    if not completed_slug.strip():
        raise ValueError("completed_slug cannot be empty")
    completed = list(state.completed_modules)
    if completed_slug not in completed:
        completed.append(completed_slug)
    return CurriculumState(
        current_day=state.current_day + 1,
        completed_modules=completed,
        current_domain_index=(state.current_domain_index + 1) % len(DOMAINS),
        last_updated=date.today().isoformat(),
    )
