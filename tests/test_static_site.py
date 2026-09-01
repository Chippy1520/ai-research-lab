"""Tests for the static GitHub Pages export."""

from __future__ import annotations

import json
from html.parser import HTMLParser
from pathlib import Path

from scripts.build_robotics_site import build

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"


class _AssetParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.local_assets: list[str] = []

    def handle_starttag(
        self,
        tag: str,
        attrs: list[tuple[str, str | None]],
    ) -> None:
        values = dict(attrs)
        attribute = "href" if tag in {"link", "a"} else "src"
        value = values.get(attribute)
        if value and not value.startswith(("http", "#", "mailto:")):
            self.local_assets.append(value)


def test_static_site_builds_from_current_intelligence() -> None:
    manifest = build()
    saved = json.loads((SITE / "data" / "manifest.json").read_text(encoding="utf-8"))
    assert saved == manifest
    assert manifest["company_count"] >= 12
    assert manifest["opening_count"] >= 100
    assert manifest["early_career_count"] >= 6
    assert manifest["reports"][0]["date"] == "2026-09-01"


def test_static_entrypoint_references_existing_local_assets() -> None:
    parser = _AssetParser()
    parser.feed((SITE / "index.html").read_text(encoding="utf-8"))
    assert "assets/styles.css" in parser.local_assets
    assert "assets/app.js" in parser.local_assets
    for asset in parser.local_assets:
        assert (SITE / asset).is_file(), asset


def test_pages_workflow_has_daily_sri_lanka_schedule() -> None:
    workflow = (ROOT / ".github" / "workflows" / "pages.yml").read_text(
        encoding="utf-8"
    )
    assert 'cron: "30 2 * * *"' in workflow
    assert "actions/deploy-pages@v4" in workflow
    assert "scripts/update_robotics_jobs.py" in workflow
