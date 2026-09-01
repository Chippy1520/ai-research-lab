"""Refresh official ATS robotics openings and recurring qualification signals."""

from __future__ import annotations

import html
import json
import os
import re
import tempfile
import urllib.request
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
JOBS_PATH = ROOT / "intelligence" / "jobs.json"
USER_AGENT = "AI-Research-Lab/1.0 (public careers monitor)"
TECHNICAL_KEYWORDS = (
    "ai",
    "autonomy",
    "controls",
    "electrical",
    "embedded",
    "firmware",
    "hardware",
    "learning",
    "machine",
    "mechanical",
    "mechatronics",
    "perception",
    "robot",
    "simulation",
    "software",
    "systems",
)

GREENHOUSE_BOARDS = {
    "Figure AI": "figureai",
    "Apptronik": "apptronik",
    "Agility Robotics": "agilityrobotics",
}
LEVER_BOARDS = {"Dexterity": "dexterity"}

SIGNAL_DEFINITIONS = {
    "C++ / modern C++": {
        "category": "Software",
        "patterns": (r"\bc\+\+(?!\w)", r"modern c\+\+"),
        "portfolio_response": (
            "Build a deterministic C++ robot-control component with profiling, tests, "
            "and a documented real-time boundary."
        ),
    },
    "Python": {
        "category": "Software",
        "patterns": (r"\bpython\b",),
        "portfolio_response": (
            "Ship a typed Python experiment and data pipeline whose results are "
            "reproducible from one command."
        ),
    },
    "ROS / ROS 2": {
        "category": "Robotics systems",
        "patterns": (r"\bros\s?2?\b", r"robot operating system"),
        "portfolio_response": (
            "Create a ROS 2 package with lifecycle nodes, recorded bags, latency "
            "measurements, and integration tests."
        ),
    },
    "Controls / estimation": {
        "category": "Robotics foundations",
        "patterns": (
            r"\bcontrol(?:s| theory)?\b",
            r"state estimation",
            r"kalman",
            r"mpc\b",
        ),
        "portfolio_response": (
            "Implement and compare a model-based controller and estimator under delay, "
            "noise, saturation, and model mismatch."
        ),
    },
    "Robot learning / RL": {
        "category": "Embodied AI",
        "patterns": (
            r"reinforcement learning",
            r"robot learning",
            r"imitation learning",
            r"learning from demonstration",
        ),
        "portfolio_response": (
            "Train and evaluate a policy with explicit baselines, ablations, sim-to-real "
            "assumptions, and failure taxonomy."
        ),
    },
    "Perception / computer vision": {
        "category": "Perception",
        "patterns": (
            r"computer vision",
            r"\bperception\b",
            r"visual[- ]inertial",
            r"\bslam\b",
        ),
        "portfolio_response": (
            "Build a calibrated perception pipeline and report uncertainty, latency, "
            "domain shift, and task-level failure costs."
        ),
    },
    "Embedded / real-time systems": {
        "category": "Hardware systems",
        "patterns": (r"embedded", r"real[- ]time", r"rtos", r"firmware"),
        "portfolio_response": (
            "Demonstrate a bounded-latency sensor-actuator loop with timing traces, "
            "watchdogs, and hardware-fault handling."
        ),
    },
    "Simulation": {
        "category": "Robotics systems",
        "patterns": (
            r"simulation",
            r"mujoco",
            r"isaac",
            r"gazebo",
            r"digital twin",
        ),
        "portfolio_response": (
            "Publish a simulation benchmark with parameter randomization, validation "
            "against measured behavior, and reproducible seeds."
        ),
    },
    "Mechanical design / CAD": {
        "category": "Hardware systems",
        "patterns": (
            r"mechanical design",
            r"\bcad\b",
            r"solidworks",
            r"tolerance analysis",
        ),
        "portfolio_response": (
            "Document one mechanism from requirements through CAD, tolerance/FEA "
            "reasoning, fabrication, and measured validation."
        ),
    },
}


class _HTMLText:
    """Tiny dependency-free HTML text normalizer."""

    @staticmethod
    def strip(value: str) -> str:
        value = html.unescape(html.unescape(value))
        value = re.sub(
            r"<script.*?</script>|<style.*?</style>",
            " ",
            value,
            flags=re.I | re.S,
        )
        value = re.sub(r"<[^>]+>", " ", value)
        return re.sub(r"\s+", " ", value).strip()


def _fetch_json(url: str) -> Any:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=45) as response:
        return json.load(response)


def _classify_seniority(title: str) -> str:
    lowered = title.lower()
    if "intern" in lowered:
        return "internship"
    if any(token in lowered for token in ("apprentice", "new grad", "graduate")):
        return "new graduate"
    experienced = ("senior", "staff", "principal", "director", "lead", "manager")
    if any(token in lowered for token in experienced):
        return "experienced"
    return "unspecified"


def _is_relevant(title: str) -> bool:
    lowered = title.lower()
    return any(keyword in lowered for keyword in TECHNICAL_KEYWORDS)


def _greenhouse_openings(company: str, board: str) -> list[dict[str, Any]]:
    payload = _fetch_json(
        f"https://boards-api.greenhouse.io/v1/boards/{board}/jobs?content=true"
    )
    results = []
    for job in payload["jobs"]:
        title = str(job["title"]).strip()
        if not _is_relevant(title):
            continue
        results.append(
            {
                "company": company,
                "title": title,
                "location": str(job.get("location", {}).get("name", "Unspecified")),
                "seniority": _classify_seniority(title),
                "url": str(job["absolute_url"]),
                "description": _HTMLText.strip(str(job.get("content", ""))),
                "source": "official Greenhouse board",
            }
        )
    return results


def _lever_openings(company: str, board: str) -> list[dict[str, Any]]:
    payload = _fetch_json(f"https://api.lever.co/v0/postings/{board}?mode=json")
    results = []
    for job in payload:
        title = str(job.get("text", "")).strip()
        if not _is_relevant(title):
            continue
        categories = job.get("categories", {})
        description = " ".join(
            str(job.get(field, ""))
            for field in ("descriptionPlain", "additionalPlain")
        )
        results.append(
            {
                "company": company,
                "title": title,
                "location": str(categories.get("location", "Unspecified")),
                "seniority": _classify_seniority(title),
                "url": str(job["hostedUrl"]),
                "description": _HTMLText.strip(description),
                "source": "official Lever board",
            }
        )
    return results


def _qualification_excerpt(description: str, limit: int = 700) -> str:
    """Keep a compact verbatim window around an official requirements heading."""
    lowered = description.lower()
    starts = [
        lowered.find(label)
        for label in ("requirements", "qualifications", "education and/or experience")
        if lowered.find(label) >= 0
    ]
    start = min(starts) if starts else 0
    excerpt = description[start : start + limit].strip()
    if start + limit < len(description):
        excerpt = f"{excerpt}…"
    return excerpt


def _derive_signals(openings: list[dict[str, Any]]) -> list[dict[str, Any]]:
    evidence: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for opening in openings:
        searchable = f"{opening['title']} {opening['description']}".lower()
        for skill, definition in SIGNAL_DEFINITIONS.items():
            if any(re.search(pattern, searchable, re.I) for pattern in definition["patterns"]):
                evidence[skill].append(opening)
    signals = []
    for skill, matches in evidence.items():
        companies = sorted({str(match["company"]) for match in matches})
        definition = SIGNAL_DEFINITIONS[skill]
        signals.append(
            {
                "skill": skill,
                "category": definition["category"],
                "company_mentions": len(companies),
                "role_mentions": len(matches),
                "evidence": f"{len(matches)} roles across {', '.join(companies)}",
                "portfolio_response": definition["portfolio_response"],
            }
        )
    return sorted(
        signals,
        key=lambda item: (int(item["company_mentions"]), int(item["role_mentions"])),
        reverse=True,
    )


def _atomic_write(payload: dict[str, Any]) -> None:
    descriptor, temporary_name = tempfile.mkstemp(
        dir=JOBS_PATH.parent, prefix=".jobs.", suffix=".tmp", text=True
    )
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            json.dump(payload, stream, indent=2, ensure_ascii=False)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary_name, JOBS_PATH)
    except BaseException:
        Path(temporary_name).unlink(missing_ok=True)
        raise


def refresh() -> dict[str, Any]:
    """Refresh accessible official boards, preserving local first-seen dates."""
    with JOBS_PATH.open("r", encoding="utf-8") as stream:
        existing = json.load(stream)
    previous = {
        str(opening["url"]): opening for opening in existing.get("openings", [])
    }
    now = datetime.now(ZoneInfo("Asia/Colombo"))
    today = now.date().isoformat()
    openings: list[dict[str, Any]] = []
    failures: list[dict[str, str]] = []

    for company, board in GREENHOUSE_BOARDS.items():
        try:
            openings.extend(_greenhouse_openings(company, board))
        except Exception as error:  # network failures must not erase other boards
            failures.append({"company": company, "error": str(error)})
    for company, board in LEVER_BOARDS.items():
        try:
            openings.extend(_lever_openings(company, board))
        except Exception as error:  # network failures must not erase other boards
            failures.append({"company": company, "error": str(error)})

    for opening in openings:
        old = previous.get(str(opening["url"]))
        opening["first_seen"] = str(old.get("first_seen", today)) if old else today
        opening["last_seen"] = today
        opening["status"] = "tracked" if old else "new"

    openings.sort(
        key=lambda item: (
            item["seniority"] not in {"internship", "new graduate"},
            item["company"],
            item["title"],
        )
    )
    signals = _derive_signals(openings)
    for opening in openings:
        description = str(opening.pop("description", ""))
        if opening["seniority"] in {"internship", "new graduate"}:
            opening["qualification_excerpt"] = _qualification_excerpt(description)
    output = {
        "version": 1,
        "last_checked": now.isoformat(timespec="seconds"),
        "methodology": existing["methodology"],
        "openings": openings,
        "requirement_signals": signals,
        "targets": existing["targets"],
        "scan_failures": failures,
    }
    _atomic_write(output)
    return output


if __name__ == "__main__":
    refreshed = refresh()
    early = sum(
        opening["seniority"] in {"internship", "new graduate"}
        for opening in refreshed["openings"]
    )
    print(
        f"official openings={len(refreshed['openings'])}, "
        f"intern/new-grad={early}, failures={len(refreshed['scan_failures'])}"
    )
