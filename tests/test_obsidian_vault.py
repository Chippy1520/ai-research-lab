"""Regression tests for the generated Obsidian research vault."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from scripts.build_obsidian_vault import PAPER_SPECS, VAULT, build, validate_vault

ROOT = Path(__file__).resolve().parents[1]


def _json(relative: str):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def _generated_digest() -> str:
    digest = hashlib.sha256()
    for path in sorted(p for p in VAULT.rglob("*") if p.is_file()):
        relative = path.relative_to(VAULT).as_posix()
        if relative in {".obsidian/workspace.json", ".obsidian/workspace-mobile.json"}:
            continue
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
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
    assert first["canvas_nodes"] == len(mindmap["nodes"])
    assert first["canvas_edges"] == len(mindmap["nodes"]) - 1
    assert first["paper_guides"] == len(PAPER_SPECS)
    assert first["contact_notes"] == len(entities["people"])
    assert first["organization_notes"] == len(
        set(item["id"] for item in entities["organizations"])
        | set(item["company_id"] for item in ecosystem["companies"])
    )
    assert first["curriculum_lessons"] == len(curriculum["lessons"])


def test_wikilinks_and_canvas_references_resolve():
    counts = validate_vault()
    assert counts["markdown_notes"] > 200
    canvas = json.loads((VAULT / "Mind Map/Embodied AI.canvas").read_text(encoding="utf-8"))
    assert all((VAULT / node["file"]).exists() for node in canvas["nodes"])


def test_full_paper_guides_are_present_and_connected():
    for slug, spec in PAPER_SPECS.items():
        note = (VAULT / "Papers" / f"{spec['title']}.md").read_text(encoding="utf-8")
        assert "type: \"paper-guide\"" in note
        assert f"site/papers-{slug}.html" in note
        assert "## Connected concepts" in note
        assert "## The paper" in note or "paper, in order" in note.lower()
        assert len(note) > 3_000


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
        "Organizations/Organizations", "Reports/Daily Reports",
    ):
        assert f"[[{target}" in home
