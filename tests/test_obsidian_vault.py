"""Regression tests for the generated Obsidian research vault."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from urllib.parse import urlparse

import yaml
from bs4 import BeautifulSoup

from scripts.build_obsidian_vault import PAPER_SPECS, VAULT, build, safe_filename, validate_vault

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


def test_wikilinks_resolve_and_graph_canvas_roles_are_explicit():
    counts = validate_vault()
    assert counts["markdown_notes"] > 200
    assert not (VAULT / "Mind Map/Embodied AI.canvas").exists()
    canvas = json.loads((VAULT / "Research Dashboard.canvas").read_text(encoding="utf-8"))
    assert canvas["generated_by"] == "build_obsidian_vault.py"
    assert len([node for node in canvas["nodes"] if node["type"] == "group"]) == 9
    assert {node["label"] for node in canvas["nodes"] if node["type"] == "group"} >= {
        "Concepts", "Papers", "Curriculum", "Contacts", "Organizations", "Reports", "Lectures"
    }
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
    assert graph["repelStrength"] == 11.0
    assert graph["linkStrength"] == 1.0
    assert graph["linkDistance"] == 175


def test_reading_theme_and_plugins_are_configured():
    appearance = json.loads((VAULT / ".obsidian/appearance.json").read_text(encoding="utf-8"))
    enabled = json.loads((VAULT / ".obsidian/community-plugins.json").read_text(encoding="utf-8"))
    quickadd = json.loads((VAULT / ".obsidian/plugins/quickadd/data.json").read_text(encoding="utf-8"))
    css = (VAULT / ".obsidian/snippets/research-lab.css").read_text(encoding="utf-8")
    assert appearance["cssTheme"] == "Minimal"
    assert enabled == ["quickadd"]
    assert quickadd["disableOnlineFeatures"] is True
    assert quickadd["templateFolderPaths"] == ["_Templates"]
    assert {choice["name"] for choice in quickadd["choices"]} == {
        "New concept", "New paper", "New lecture"
    }
    assert "--research-reading-width" in css
    assert '.callout[data-callout="capture"]' in css
    assert ".canvas-node-content" in css
    assert ".smart-lookup" not in css and ".connections-list" not in css
    gitignore = (VAULT / ".gitignore").read_text(encoding="utf-8")
    assert ".smart-env" not in gitignore
    library = (VAULT / "Library/Research Library.base").read_text(encoding="utf-8")
    assert "name: Concepts" in library and "name: Research queue" in library


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
    assert "Research Dashboard" in home
    assert "Research Library" in home
    assert "built-in **Search**" in home
    assert "Smart Lookup" not in home and "Omnisearch" not in home


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


def test_curriculum_is_recall_first_and_video_led():
    plan = _json("curriculum_plan.json")
    resources = _json("curriculum_resources.json")
    by_day = {int(item["day"]): item for item in resources["lessons"]}
    assert set(by_day) == {int(item["day"]) for item in plan["lessons"]}

    allowed_sources = {
        "university_course",
        "research_lab",
        "official_conference",
        "professional_foundation",
        "respected_educator",
    }
    for planned in plan["lessons"]:
        day = int(planned["day"])
        resource = by_day[day]
        assert resource["topic"] == planned["topic"]
        if planned["stage"] == "Live review":
            assert resource["selection_status"] == "deferred_until_topic_selected"
            assert resource["videos"] == []
        else:
            assert resource["selection_status"] == "verified"
            assert 1 <= len(resource["videos"]) <= 3
        assert 3 <= len(resource["recall"]) <= 5
        assert len(resource["description"]) <= 600
        assert [int(video["order"]) for video in resource["videos"]] == list(
            range(1, len(resource["videos"]) + 1)
        )
        for video in resource["videos"]:
            assert video["language"] == "English"
            assert video["source_type"] in allowed_sources
            assert video["source_rationale"]
            assert video["oembed_verified_on"]
            assert video["url"].startswith("https://www.youtube.com/watch?v=")

        path = VAULT / f"Curriculum/Lessons/Day {day:02d} - {safe_filename(planned['topic'])}.md"
        lesson = path.read_text(encoding="utf-8")
        assert "## Brief description" in lesson
        assert "## Recall in 30 seconds" in lesson
        if planned["stage"] == "Live review":
            assert "## Video path selected on generation day" in lesson
        else:
            assert "## Watch in order" in lesson
        assert "curriculum_resources.json" in lesson
        assert "Authored technical lesson" not in lesson
        assert "Video masterclasses and source ledger" not in lesson
        assert "$$" not in lesson
        assert len(lesson.splitlines()) <= 120

    lecture_hub = (VAULT / "Lectures/Lecture Notes.md").read_text(encoding="utf-8")
    lecture_template = (VAULT / "_Templates/Lecture Note.md").read_text(encoding="utf-8")
    concept_template = (VAULT / "_Templates/Lecture Concept.md").read_text(encoding="utf-8")
    assert "QuickAdd: New lecture" in lecture_hub
    assert "Research Library.base#Lectures" in lecture_hub
    assert "## Source material" in lecture_template
    assert "## Failure modes and boundaries" in concept_template
    assert "<%" not in lecture_template and "<%" not in concept_template
    paper_template = (VAULT / "_Templates/Paper Note.md").read_text(encoding="utf-8")
    research_template = (VAULT / "_Templates/Concept Note.md").read_text(encoding="utf-8")
    assert "## Model or system step" in paper_template
    assert "## Mechanism" in research_template


def test_jobs_are_grouped_into_readable_company_sections():
    jobs = (VAULT / "Robotics Intelligence/Current Openings.md").read_text(encoding="utf-8")
    assert "[!current] Early-career roles" in jobs
    assert "## [[Organizations/agility-robotics|Agility Robotics]]" in jobs
    assert jobs.count("| Role | Location | Seniority | Last seen |") >= 3
