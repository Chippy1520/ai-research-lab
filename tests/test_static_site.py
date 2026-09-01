"""Tests for the static GitHub Pages export."""

from __future__ import annotations

import json
import xml.etree.ElementTree as ET
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
    assert manifest["curriculum"] == {
        "current_day": 1,
        "mapped_lessons": 72,
        "generated_modules": 1,
        "research_sources": 8,
    }


def test_curriculum_export_preserves_article_code_and_rotation() -> None:
    payload = json.loads(
        (SITE / "data" / "curriculum.json").read_text(encoding="utf-8")
    )
    module = payload["modules"][0]
    block_types = {block["type"] for block in module["article"]}
    assert {"markdown", "latex", "table", "code", "video"} <= block_types
    assert module["experiment_source"] == (
        ROOT / "experiments" / "adamw_reference.py"
    ).read_text(encoding="utf-8")
    domains = [lesson["domain"] for lesson in payload["plan"]["lessons"]]
    assert all(
        domain == payload["plan"]["policy"]["rotation"][index % 3]
        for index, domain in enumerate(domains)
    )


def test_static_entrypoint_references_existing_local_assets() -> None:
    for entrypoint in ("index.html", "curriculum.html"):
        parser = _AssetParser()
        parser.feed((SITE / entrypoint).read_text(encoding="utf-8"))
        assert "assets/styles.css" in parser.local_assets
        for asset in parser.local_assets:
            assert (SITE / asset).is_file(), (entrypoint, asset)


def test_static_pages_keep_editorial_shells_and_us_map() -> None:
    robotics = (SITE / "index.html").read_text(encoding="utf-8")
    curriculum = (SITE / "curriculum.html").read_text(encoding="utf-8")
    assert 'class="news-page"' in robotics
    assert 'src="assets/us-outline.svg"' in robotics
    assert 'class="editorial"' in curriculum
    assert 'role="tablist"' not in curriculum

    svg = ET.parse(SITE / "assets" / "us-outline.svg")
    namespace = {"svg": "http://www.w3.org/2000/svg"}
    assert len(svg.findall(".//svg:path", namespace)) == 49


def test_pages_workflow_has_daily_sri_lanka_schedule() -> None:
    workflow = (ROOT / ".github" / "workflows" / "pages.yml").read_text(
        encoding="utf-8"
    )
    assert 'cron: "30 2 * * *"' in workflow
    assert "actions/deploy-pages@v4" in workflow
    assert "scripts/update_robotics_jobs.py" in workflow
