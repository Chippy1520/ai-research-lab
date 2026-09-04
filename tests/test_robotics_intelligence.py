"""Schema and evidence tests for US robotics market intelligence."""

from __future__ import annotations

from pathlib import Path

from robotics_intelligence import latest_report, load_ecosystem, load_jobs
from scripts.update_robotics_jobs import (
    _classify_seniority,
    _derive_signals,
    _preserve_failed_company_openings,
)

ROOT = Path(__file__).resolve().parents[1]


def test_ecosystem_has_sourced_humanoid_and_adjacent_companies() -> None:
    metadata, companies = load_ecosystem(ROOT / "intelligence" / "ecosystem.json")
    report_date, _ = latest_report(ROOT / "intelligence" / "reports")
    assert metadata["as_of"] == report_date
    assert len(companies) >= 12
    assert sum(company.category == "Humanoid platform" for company in companies) >= 7
    assert len(metadata["hubs"]) >= 7
    assert all(company.sources for company in companies)
    assert all(company.careers_url.startswith("https://") for company in companies)


def test_valuations_are_dated_typed_observations() -> None:
    _, companies = load_ecosystem(ROOT / "intelligence" / "ecosystem.json")
    for company in companies:
        assert company.valuation_type
        assert company.valuation_note
        if company.valuation_usd_billions is not None:
            assert company.valuation_usd_billions > 0
            assert company.valuation_as_of is not None
    tesla = next(company for company in companies if company.company_id == "tesla-optimus")
    assert tesla.valuation_type == "Public parent market capitalization"
    assert "not an Optimus valuation" in tesla.valuation_note


def test_jobs_snapshot_contains_verified_early_career_roles() -> None:
    jobs = load_jobs(ROOT / "intelligence" / "jobs.json")
    assert len(jobs["openings"]) >= 100
    early_career = [
        opening
        for opening in jobs["openings"]
        if opening["seniority"] in {"internship", "new graduate"}
    ]
    assert len(early_career) >= 6
    assert all(opening["url"].startswith("https://") for opening in early_career)
    assert not jobs.get("scan_failures")
    assert len(jobs["requirement_signals"]) >= 6


def test_signal_derivation_counts_companies_not_repeated_roles() -> None:
    openings = [
        {"company": "A", "title": "C++ Robotics Intern", "description": "Python ROS 2"},
        {"company": "A", "title": "Robotics Engineer", "description": "Python"},
        {"company": "B", "title": "Controls Engineer", "description": "C++ Python"},
    ]
    signals = {item["skill"]: item for item in _derive_signals(openings)}
    assert signals["Python"]["company_mentions"] == 2
    assert signals["Python"]["role_mentions"] == 3
    assert signals["C++ / modern C++"]["company_mentions"] == 2
    assert _classify_seniority("Firmware Intern [Fall 2026]") == "internship"


def test_failed_board_preserves_previous_roles_without_advancing_last_seen() -> None:
    previous = {
        "https://example.com/job": {
            "company": "Figure AI",
            "title": "Robotics Intern",
            "url": "https://example.com/job",
            "first_seen": "2026-09-01",
            "last_seen": "2026-09-03",
            "status": "tracked",
        }
    }
    retained = _preserve_failed_company_openings(previous, "Figure AI", "2026-09-04")
    assert retained[0]["status"] == "unverified"
    assert retained[0]["last_seen"] == "2026-09-03"
    assert previous["https://example.com/job"]["status"] == "tracked"


def test_daily_report_archive_has_a_dated_baseline() -> None:
    report_date, report = latest_report(ROOT / "intelligence" / "reports")
    metadata, _ = load_ecosystem(ROOT / "intelligence" / "ecosystem.json")
    assert report_date == metadata["as_of"]
    assert "Verified early-career openings" in report
    assert "valuation" in report.lower()
