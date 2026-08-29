"""Persistent curriculum, roadmap, learning-log, and research-log utilities."""

from __future__ import annotations

import json
import os
import tempfile
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
STATE_PATH = ROOT / "curriculum_state.json"
PLAN_PATH = ROOT / "curriculum_plan.json"
LEARNING_LOG_PATH = ROOT / "learning_log.json"
RESEARCH_LOG_PATH = ROOT / "research_log.json"
DOMAINS: tuple[str, ...] = (
    "Machine Learning",
    "Computer Vision",
    "Embodied AI & RL Robotics",
)


@dataclass(frozen=True)
class CurriculumState:
    """Validated cursor identifying the one module currently due."""

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


@dataclass(frozen=True)
class PlannedLesson:
    """A lightweight roadmap entry; content is deliberately generated later."""

    day: int
    cycle: int
    domain: str
    domain_index: int
    topic: str
    stage: str
    status: str
    foundation_threads: tuple[str, ...]

    @classmethod
    def from_mapping(cls, payload: dict[str, Any]) -> "PlannedLesson":
        """Validate one lesson without treating the roadmap as authored content."""
        lesson = cls(
            day=int(payload["day"]),
            cycle=int(payload["cycle"]),
            domain=str(payload["domain"]),
            domain_index=int(payload["domain_index"]),
            topic=str(payload["topic"]),
            stage=str(payload["stage"]),
            status=str(payload["status"]),
            foundation_threads=tuple(map(str, payload["foundation_threads"])),
        )
        if lesson.day < 1 or lesson.cycle < 1:
            raise ValueError("lesson day and cycle must be positive")
        if lesson.domain_index not in range(len(DOMAINS)):
            raise ValueError("invalid lesson domain index")
        if lesson.domain != DOMAINS[lesson.domain_index]:
            raise ValueError("lesson domain and domain index disagree")
        if not lesson.topic.strip():
            raise ValueError("lesson topic cannot be empty")
        return lesson


def _read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as stream:
        payload = json.load(stream)
    if not isinstance(payload, dict):
        raise TypeError(f"{path.name} must contain a JSON object")
    return payload


def _atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    """Persist JSON with fsync + atomic replacement to resist interrupted writes."""
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        dir=path.parent, prefix=f".{path.name}.", suffix=".tmp", text=True
    )
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            json.dump(payload, stream, indent=2, ensure_ascii=False)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary_name, path)
    except BaseException:
        Path(temporary_name).unlink(missing_ok=True)
        raise


def load_state(path: Path = STATE_PATH) -> CurriculumState:
    """Read and validate the current just-in-time curriculum cursor."""
    return CurriculumState.from_mapping(_read_json(path))


def save_state(state: CurriculumState, path: Path = STATE_PATH) -> None:
    """Atomically persist curriculum state."""
    _atomic_write_json(path, asdict(state))


def load_plan(path: Path = PLAN_PATH) -> tuple[dict[str, Any], list[PlannedLesson]]:
    """Load roadmap metadata and verify strict day/domain ordering."""
    payload = _read_json(path)
    horizon = payload.get("horizon_policy", {})
    if horizon.get("mode") != "rolling_open_ended":
        raise ValueError("curriculum must use a rolling open-ended horizon")
    if horizon.get("terminal_day") is not None:
        raise ValueError("open-ended curriculum cannot define a terminal day")
    if int(horizon.get("minimum_mapped_ahead_days", 0)) < 1:
        raise ValueError("minimum_mapped_ahead_days must be positive")
    if int(horizon.get("extension_batch_cycles", 0)) < 1:
        raise ValueError("extension_batch_cycles must be positive")
    lessons = [PlannedLesson.from_mapping(item) for item in payload["lessons"]]
    for expected_day, lesson in enumerate(lessons, start=1):
        if lesson.day != expected_day:
            raise ValueError("roadmap days must be contiguous and one-indexed")
        expected_domain = (expected_day - 1) % len(DOMAINS)
        if lesson.domain_index != expected_domain:
            raise ValueError(f"day {expected_day} violates strict domain rotation")
    return payload, lessons


def lesson_for_day(day: int, path: Path = PLAN_PATH) -> PlannedLesson:
    """Return the planned lesson for *day*."""
    _, lessons = load_plan(path)
    if day < 1 or day > len(lessons):
        raise IndexError(f"day {day} lies outside the current planning horizon")
    return lessons[day - 1]


def load_learning_log(path: Path = LEARNING_LOG_PATH) -> list[dict[str, Any]]:
    """Return validated learning-log entries sorted by day."""
    entries = list(_read_json(path).get("entries", []))
    required = {"day", "module_slug", "title", "domain", "status", "generated_on"}
    for entry in entries:
        missing = required.difference(entry)
        if missing:
            raise ValueError(f"learning-log entry is missing {sorted(missing)}")
        date.fromisoformat(str(entry["generated_on"]))
    return sorted(entries, key=lambda item: int(item["day"]))


def load_research_log(path: Path = RESEARCH_LOG_PATH) -> list[dict[str, Any]]:
    """Return research provenance, source lists, and appended corrections."""
    entries = list(_read_json(path).get("entries", []))
    for entry in entries:
        if not {"day", "module_slug", "researched_on", "sources"} <= set(entry):
            raise ValueError("research-log entry violates its schema")
        date.fromisoformat(str(entry["researched_on"]))
    return sorted(entries, key=lambda item: int(item["day"]))


def save_learning_reflection(
    day: int,
    minutes_spent: int,
    confidence: int,
    notes: str,
    revisit: bool,
    mark_complete: bool,
    path: Path = LEARNING_LOG_PATH,
) -> dict[str, Any]:
    """Update one archived module's reflection without rewriting lesson content."""
    if minutes_spent < 0:
        raise ValueError("minutes_spent cannot be negative")
    if confidence not in range(1, 6):
        raise ValueError("confidence must lie from 1 to 5")
    payload = _read_json(path)
    matches = [entry for entry in payload["entries"] if int(entry["day"]) == day]
    if len(matches) != 1:
        raise ValueError(f"expected exactly one learning-log entry for day {day}")
    entry = matches[0]
    entry.update(
        minutes_spent=int(minutes_spent),
        confidence=int(confidence),
        notes=notes.strip(),
        revisit=bool(revisit),
    )
    if mark_complete:
        entry["status"] = "completed"
        entry["studied_on"] = date.today().isoformat()
    _atomic_write_json(path, payload)
    return dict(entry)


def advance_state(state: CurriculumState, completed_slug: str) -> CurriculumState:
    """Return the next cursor under strict ML→CV→EAI rotation."""
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
