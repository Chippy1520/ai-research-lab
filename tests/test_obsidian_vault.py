"""Regression tests for the generated Obsidian research vault."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from urllib.parse import urlparse

import yaml
from bs4 import BeautifulSoup

from scripts.build_obsidian_vault import PAPER_SPECS, VAULT, build, validate_vault

ROOT = Path(__file__).resolve().parents[1]


def _json(relative: str):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def _generated_digest() -> str:
    digest = hashlib.sha256()
    for path in sorted(VAULT.rglob("*.md")):
        data = path.read_bytes()
        if b'generated_by: "build_obsidian_vault.py"' not in data[:600]:
            continue
        relative = path.relative_to(VAULT).as_posix()
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(data)
        digest.update(b"\0")
    return digest.hexdigest()


def test_build_is_complete_and_idempotent():
    first = build()
    first_digest = _generated_digest()
    second = build()
    second_digest = _generated_digest()

    mindmap = _json("intelligence/mindmap.json")
    entities = _json("intelligence/entities.json")
    ecosystem = _json("intelligence/ecosystem.json")
    curriculum = _json("curriculum_plan.json")

    assert first == second
    assert first_digest == second_digest
    assert first["mindmap_notes"] == len(mindmap["nodes"])
    assert first["semantic_edges"] == len(mindmap["edges"])
    assert first["graph_links"] >= 2 * len(mindmap["edges"])
    assert first["paper_guides"] == len(PAPER_SPECS)
    assert first["contact_notes"] == len(entities["people"])
    assert first["organization_notes"] == len(
        set(item["id"] for item in entities["organizations"])
        | set(item["company_id"] for item in ecosystem["companies"])
    )
    assert first["curriculum_lessons"] == len(curriculum["lessons"])


def test_wikilinks_resolve_and_native_graph_replaces_canvas():
    counts = validate_vault()
    assert counts["markdown_notes"] > 200
    assert not (VAULT / "Mind Map/Embodied AI.canvas").exists()
    graph = json.loads((VAULT / ".obsidian/graph.json").read_text(encoding="utf-8"))
    assert graph["hideUnresolved"] is True
    assert graph["showOrphans"] is False
    assert graph["showTags"] is False
    assert len(graph["colorGroups"]) == 8
    assert {group["query"]: group["color"]["rgb"] for group in graph["colorGroups"]} == {
        'path:"Mind Map"': 42747,
        "path:Papers": 16743168,
        "path:Curriculum": 3715072,
        "path:Contacts": 16196997,
        "path:Organizations": 16766474,
        "path:Reports": 15672124,
        "path:Lectures": 8599788,
        'path:"Robotics Intelligence"': 54472,
    }
    assert graph["showArrow"] is True
    assert graph["repelStrength"] == 14.0
    assert graph["linkStrength"] == 0.72
    assert graph["linkDistance"] == 260


def test_reading_theme_and_plugins_are_configured():
    appearance = json.loads((VAULT / ".obsidian/appearance.json").read_text(encoding="utf-8"))
    enabled = json.loads((VAULT / ".obsidian/community-plugins.json").read_text(encoding="utf-8"))
    homepage = json.loads((VAULT / ".obsidian/plugins/homepage/data.json").read_text(encoding="utf-8"))
    css = (VAULT / ".obsidian/snippets/research-lab.css").read_text(encoding="utf-8")
    assert appearance["cssTheme"] == "Minimal"
    assert {
        "obsidian-style-settings", "obsidian-minimal-settings", "homepage",
        "dataview", "omnisearch", "table-editor-obsidian", "templater-obsidian", "voice-scribe",
        "smart-connections", "smart-lookup", "callout-manager",
    } <= set(enabled)
    dataview = json.loads((VAULT / ".obsidian/plugins/dataview/data.json").read_text(encoding="utf-8"))
    templater = json.loads((VAULT / ".obsidian/plugins/templater-obsidian/data.json").read_text(encoding="utf-8"))
    assert dataview["enableDataviewJs"] is False
    assert dataview["enableInlineDataviewJs"] is False
    assert templater["templates_folder"] == "_Templates"
    assert homepage["homepages"]["Main Homepage"]["value"] == "Home"
    assert homepage["homepages"]["Main Homepage"]["view"] == "Reading view"
    assert "@settings" in css and "--research-reading-width" in css
    assert '.callout[data-callout="semantic"]' in css
    assert ".lookup-item-view .lookup-query-form" in css
    gitignore = (VAULT / ".gitignore").read_text(encoding="utf-8")
    assert ".smart-env/" in gitignore


def test_full_paper_guides_are_present_and_connected():
    for slug, spec in PAPER_SPECS.items():
        note = (VAULT / "Papers" / f"{spec['title']}.md").read_text(encoding="utf-8")
        source = BeautifulSoup((ROOT / "site" / f"papers-{slug}.html").read_text(encoding="utf-8"), "html.parser")
        assert "type: \"paper-guide\"" in note
        assert f"site/papers-{slug}.html" in note
        assert 'content_mode: "local"' in note
        assert "live_url:" not in note
        assert "chippy1520.github.io/ai-research-lab" not in note
        assert "Connected concepts" in note
        assert "## The paper" in note or "paper, in order" in note.lower()
        assert len(note) > 3_000
        assert "OBSMD" not in note
        assert "**1**step" not in note
        assert note.count("[!video]") == len(source.find_all("iframe"))
        for image in source.find_all("img"):
            src = image.get("src", "")
            if not src.startswith(("http://", "https://")):
                continue
            filename = Path(urlparse(src).path).name
            asset = VAULT / "_attachments" / "Papers" / slug / filename
            assert asset.is_file(), asset
            assert f"../_attachments/Papers/{slug}/{filename}" in note
        assert not re.search(r"!\[[^\]]*\]\(https?://", note)


def test_generated_vault_has_no_first_party_pages_dependency():
    forbidden = "https://chippy1520.github.io/ai-research-lab"
    for path in VAULT.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        if 'generated_by: "build_obsidian_vault.py"' not in text[:700]:
            continue
        assert forbidden not in text, path
    paper_index = (VAULT / "Papers/Paper Guides.md").read_text(encoding="utf-8")
    concept = (VAULT / "Mind Map/Nodes/act.md").read_text(encoding="utf-8")
    assert "[!local] Local-first library" in paper_index
    assert "[[Papers/ACT and ALOHA|Our ACT guide]]" in concept
    assert "[[Mind Map/Embodied AI|Embodied AI Knowledge Graph]]" in concept


def test_contacts_preserve_public_privacy_boundary():
    forbidden_frontmatter = {
        "priority:", "outreach_draft:", "contacted:", "readiness:", "next_follow_up:"
    }
    for path in (VAULT / "Contacts").glob("*.md"):
        text = path.read_text(encoding="utf-8")
        frontmatter = text.split("---", 2)[1] if text.startswith("---") else ""
        assert not any(field in frontmatter for field in forbidden_frontmatter)
    assert "Private career preparation" in (VAULT / "Home.md").read_text(encoding="utf-8")


def test_home_exposes_each_research_surface():
    home = (VAULT / "Home.md").read_text(encoding="utf-8")
    for target in (
        "Mind Map/Embodied AI", "Papers/Paper Guides", "Curriculum/Curriculum",
        "Robotics Intelligence/Robotics Intelligence", "Contacts/Contacts",
        "Organizations/Organizations", "Reports/Daily Reports", "Lectures/Lecture Notes",
    ):
        assert f"[[{target}" in home
    assert "Smart Lookup: Open: Lookup view" in home
    assert "Smart Connections: Open: Connections view" in home


def test_directional_graph_relations_and_normalized_tags():
    act = (VAULT / "Mind Map/Nodes/act.md").read_text(encoding="utf-8")
    chunking = (VAULT / "Mind Map/Nodes/action-chunking.md").read_text(encoding="utf-8")
    assert "[!outgoing] Outgoing relationships" in chunking
    assert "**implemented in →** [[Mind Map/Nodes/act|ACT]]" in chunking
    assert "[!incoming] Incoming relationships" in act
    assert "**← implemented in —** [[Mind Map/Nodes/action-chunking|Action chunking]]" in act

    tag_pattern = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
    for path in VAULT.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---\n"):
            continue
        metadata = yaml.safe_load(text.split("---\n", 2)[1]) or {}
        tags = metadata.get("tags", [])
        assert len(tags) == len(set(tags)), path
        assert all(tag_pattern.fullmatch(tag) for tag in tags), (path, tags)


def test_authored_curriculum_and_lecture_capture_are_preserved():
    lesson = (VAULT / "Curriculum/Lessons/Day 01 - Optimization Dynamics & AdamW.md").read_text(encoding="utf-8")
    assert "modules/module_01.py" in lesson
    assert "[!lesson] Authored technical lesson" in lesson
    assert "### 15 · Video masterclasses and source ledger" in lesson
    assert lesson.count("### ") >= 15

    lecture_hub = (VAULT / "Lectures/Lecture Notes.md").read_text(encoding="utf-8")
    lecture_template = (VAULT / "_Templates/Lecture Note.md").read_text(encoding="utf-8")
    concept_template = (VAULT / "_Templates/Lecture Concept.md").read_text(encoding="utf-8")
    assert "Voice Scribe" in lecture_hub
    assert "FROM \"Lectures/Notes\"" in lecture_hub
    assert "## Transcript and recording" in lecture_template
    assert "## Failure modes and boundaries" in concept_template


def test_jobs_are_grouped_into_readable_company_sections():
    jobs = (VAULT / "Robotics Intelligence/Current Openings.md").read_text(encoding="utf-8")
    assert "[!current] Early-career roles" in jobs
    assert "## [[Organizations/agility-robotics|Agility Robotics]]" in jobs
    assert jobs.count("| Role | Location | Seniority | Last seen |") >= 3
