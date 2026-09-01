"""Build the static GitHub Pages payload for Robotics Intelligence."""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
INTELLIGENCE_DIR = ROOT / "intelligence"
SITE_DIR = ROOT / "site"
DATA_DIR = SITE_DIR / "data"
REPORT_OUTPUT_DIR = DATA_DIR / "reports"


def _read_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError(f"Expected a JSON object in {path}")
    return payload


def build() -> dict[str, Any]:
    """Copy validated intelligence data and create a compact site manifest."""
    ecosystem_path = INTELLIGENCE_DIR / "ecosystem.json"
    jobs_path = INTELLIGENCE_DIR / "jobs.json"
    reports_dir = INTELLIGENCE_DIR / "reports"

    ecosystem = _read_json(ecosystem_path)
    jobs = _read_json(jobs_path)
    report_paths = sorted(reports_dir.glob("????-??-??.md"), reverse=True)
    if not report_paths:
        raise ValueError("At least one dated intelligence report is required")

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ecosystem_path, DATA_DIR / "ecosystem.json")
    shutil.copy2(jobs_path, DATA_DIR / "jobs.json")

    reports = []
    current_names = set()
    for report_path in report_paths:
        output_name = report_path.name
        current_names.add(output_name)
        shutil.copy2(report_path, REPORT_OUTPUT_DIR / output_name)
        reports.append(
            {
                "date": report_path.stem,
                "path": f"data/reports/{output_name}",
            }
        )
    for stale_path in REPORT_OUTPUT_DIR.glob("*.md"):
        if stale_path.name not in current_names:
            stale_path.unlink()

    openings = jobs.get("openings", [])
    early_career = [
        opening
        for opening in openings
        if opening.get("seniority") in {"internship", "new graduate"}
    ]
    companies = ecosystem.get("companies", [])
    manifest = {
        "site_title": "US Robotics Intelligence",
        "ecosystem_as_of": ecosystem.get("as_of"),
        "jobs_last_checked": jobs.get("last_checked"),
        "company_count": len(companies),
        "humanoid_count": sum(
            str(company.get("category", "")).startswith("Humanoid")
            for company in companies
        ),
        "opening_count": len(openings),
        "early_career_count": len(early_career),
        "reports": reports,
    }
    with (DATA_DIR / "manifest.json").open("w", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
    return manifest


if __name__ == "__main__":
    result = build()
    print(
        "static site data built: "
        f"companies={result['company_count']}, "
        f"openings={result['opening_count']}, "
        f"reports={len(result['reports'])}"
    )
