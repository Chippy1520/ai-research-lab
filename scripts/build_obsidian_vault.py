#!/usr/bin/env python3
"""Build an Obsidian knowledge vault from the research lab's canonical data.

The JSON, HTML, and Markdown files elsewhere in this repository remain the source
of truth. Generated notes carry ``generated_by: build_obsidian_vault.py`` and may
be rebuilt safely; hand-written notes without that marker are left untouched.
"""
from __future__ import annotations

import ast
import json
import re
import textwrap
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import parse_qs, urlparse

from bs4 import BeautifulSoup, Tag
from markdownify import markdownify as html_to_markdown

ROOT = Path(__file__).resolve().parents[1]
VAULT = ROOT / "obsidian"
GENERATOR = "build_obsidian_vault.py"

PAPER_SPECS = {
    "act": {"title": "ACT and ALOHA", "source": "act.md", "nodes": ["act", "action-chunking"]},
    "ijepa": {"title": "I-JEPA", "source": "ijepa.md", "nodes": ["representation", "world-models"]},
    "jepa": {"title": "JEPA", "source": "jepa.md", "nodes": ["representation", "world-models"]},
    "smolvla": {
        "title": "SmolVLA and LeRobot",
        "source": "smolvla-lerobot.md",
        "nodes": ["smolvla", "lerobot", "flow-matching", "async-infer"],
    },
    "stlight": {"title": "STLight", "source": "stlight.md", "nodes": ["stlight", "transformers"]},
    "vggt": {"title": "VGGT", "source": "vggt.md", "nodes": ["vggt", "geometry-3d"]},
    "vjepa": {"title": "V-JEPA", "source": "vjepa.md", "nodes": ["representation", "world-models"]},
    "vjepa2": {"title": "V-JEPA 2", "source": "vjepa2.md", "nodes": ["representation", "world-models"]},
}

INVALID_FILENAME = re.compile(r'[<>:"/\\|?*]')
WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")


def load_json(relative: str) -> dict[str, Any]:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def yaml_scalar(value: Any) -> str:
    """JSON scalars and arrays are valid YAML and avoid quoting edge cases."""
    return json.dumps(value, ensure_ascii=False)


def normalize_tag(value: Any) -> str:
    tag = re.sub(r"[^a-z0-9]+", "-", str(value).strip().lower()).strip("-")
    return tag or "untagged"


def frontmatter(**fields: Any) -> str:
    if "tags" in fields:
        fields["tags"] = list(dict.fromkeys(normalize_tag(tag) for tag in fields["tags"]))
    if "aliases" in fields:
        fields["aliases"] = list(dict.fromkeys(fields["aliases"]))
    ordered = {"generated_by": GENERATOR, **fields}
    lines = ["---"]
    for key, value in ordered.items():
        if value is None:
            continue
        lines.append(f"{key}: {yaml_scalar(value)}")
    lines.extend(["---", ""])
    return "\n".join(lines)


def safe_filename(name: str) -> str:
    cleaned = INVALID_FILENAME.sub("-", name).strip().rstrip(".")
    return re.sub(r"\s+", " ", cleaned) or "Untitled"


def write(relative: str, content: str) -> Path:
    path = VAULT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    normalized = "\n".join(content.splitlines()).rstrip() + "\n"
    path.write_text(normalized, encoding="utf-8")
    return path


def write_template(relative: str, content: str) -> Path:
    """Write a managed Templater source without marking created user notes as generated."""
    marker = f'<%* /* generated_by: "{GENERATOR}" */ -%>\n'
    path = VAULT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    normalized = "\n".join(content.splitlines()).rstrip() + "\n"
    path.write_text(marker + normalized, encoding="utf-8")
    return path


def wiki(path: str, label: str | None = None) -> str:
    target = path[:-3] if path.endswith(".md") else path
    return f"[[{target}|{label}]]" if label else f"[[{target}]]"


def bullet_links(items: Iterable[tuple[str, str]]) -> str:
    rows = [f"- {wiki(path, label)}" for path, label in items]
    return "\n".join(rows) if rows else "- None recorded."


def markdown_link(title: str, url: str) -> str:
    return f"[{title}]({url})"


def local_site_wikilink(href: str, label: str, paper_file_map: dict[str, str] | None = None) -> str | None:
    """Resolve links to this project's published HTML into vault-native notes."""
    parsed = urlparse(href)
    if parsed.scheme in {"http", "https"}:
        if parsed.netloc.lower() != "chippy1520.github.io" or not parsed.path.startswith("/ai-research-lab/"):
            return None
        site_path = parsed.path.removeprefix("/ai-research-lab/")
    elif parsed.scheme or parsed.netloc or href.startswith("#"):
        return None
    else:
        site_path = parsed.path.lstrip("./")

    file_name = Path(site_path).name
    paper_file_map = paper_file_map or {f"papers-{slug}.html": slug for slug in PAPER_SPECS}
    if file_name in paper_file_map:
        spec = PAPER_SPECS[paper_file_map[file_name]]
        return wiki(f"Papers/{spec['title']}.md", label)
    if file_name == "papers.html":
        return wiki("Papers/Paper Guides.md", label)
    if file_name == "mindmap.html":
        fragment_values = parse_qs(parsed.fragment)
        query_values = parse_qs(parsed.query)
        node_id = (fragment_values.get("node") or query_values.get("node") or [None])[0]
        target = f"Mind Map/Nodes/{node_id}.md" if node_id else "Mind Map/Embodied AI.md"
        return wiki(target, label)
    if file_name in {"", "index.html"}:
        return wiki("Home.md", label)
    return None


def table_cell(value: Any) -> str:
    return str(value if value is not None else "—").replace("|", "\\|").replace("\n", " ")


def nav(section_path: str, section_label: str) -> str:
    """Compact breadcrumb shared by every generated note family."""
    return f"{wiki('Home.md', 'Research Lab')}  /  {wiki(section_path, section_label)}"


def callout(kind: str, title: str, body: Iterable[str]) -> list[str]:
    """Render a native Obsidian callout without coupling notes to a plugin."""
    lines = [f"> [!{kind}] {title}"]
    rows = list(body)
    if not rows:
        return lines
    for row in rows:
        lines.append(">" if not row else f"> {row}")
    return lines


def link_callout(title: str, items: Iterable[tuple[str, str]], kind: str = "links") -> list[str]:
    rows = [f"- {wiki(path, label)}" for path, label in items]
    return callout(kind, title, rows or ["No linked records yet."])


def normalized_text(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def related_node_ids(text: str, nodes: list[dict[str, Any]], *, roots: Iterable[str] = (), limit: int = 8) -> list[str]:
    """Match explicit concept names, then add stable domain roots."""
    haystack = f" {normalized_text(text)} "
    scored: list[tuple[int, str]] = []
    for node in nodes:
        candidates = {normalized_text(node["label"]), normalized_text(node["id"])}
        hits = [candidate for candidate in candidates if len(candidate) >= 3 and f" {candidate} " in haystack]
        if hits:
            scored.append((max(len(hit) for hit in hits), node["id"]))
    ordered = [node_id for _, node_id in sorted(scored, key=lambda item: (-item[0], item[1]))]
    for node_id in roots:
        if node_id not in ordered:
            ordered.append(node_id)
    return ordered[:limit]


def clean_generated_files() -> None:
    if not VAULT.exists():
        return
    for path in VAULT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".md", ".canvas"}:
            continue
        try:
            sample = path.read_text(encoding="utf-8")[:600]
        except UnicodeDecodeError:
            continue
        generated_canvas = False
        if path.suffix.lower() == ".canvas":
            try:
                generated_canvas = json.loads(path.read_text(encoding="utf-8")).get("generated_by") == GENERATOR
            except (json.JSONDecodeError, AttributeError):
                generated_canvas = False
        if f'generated_by: "{GENERATOR}"' in sample or generated_canvas:
            path.unlink()


def build_settings() -> None:
    settings = {
        ".obsidian/app.json": {"alwaysUpdateLinks": True, "newFileLocation": "current", "showLineNumber": True},
        ".obsidian/appearance.json": {"baseFontSize": 17, "cssTheme": "Minimal", "enabledCssSnippets": ["research-lab"]},
        ".obsidian/core-plugins.json": {
            "file-explorer": True, "global-search": True, "switcher": True, "graph": True,
            "backlink": True, "outgoing-link": True, "tag-pane": True, "page-preview": True,
            "daily-notes": False, "templates": False, "note-composer": True,
            "command-palette": True, "slash-command": True, "editor-status": True,
            "markdown-importer": False, "zk-prefixer": False, "random-note": False,
            "outline": True, "word-count": True, "slides": False, "audio-recorder": False,
            "workspaces": True, "file-recovery": True, "publish": False, "sync": False,
            "canvas": True, "footnotes": True, "properties": True, "bookmarks": True,
            "bases": True, "webviewer": False,
        },
        ".obsidian/community-plugins.json": [
            "obsidian-style-settings", "obsidian-minimal-settings", "homepage",
            "dataview", "omnisearch", "table-editor-obsidian",
            "templater-obsidian", "voice-scribe",
        ],
        ".obsidian/plugins/dataview/data.json": {
            "enableDataviewJs": False, "enableInlineDataview": True,
            "enableInlineDataviewJs": False, "refreshEnabled": True,
        },
        ".obsidian/plugins/templater-obsidian/data.json": {
            "data_version": 2, "command_timeout": 5, "templates_folder": "_Templates",
            "templates_pairs": [], "trigger_on_file_creation_mode": "none",
            "auto_jump_to_cursor": False, "jump_to_cursor_after_file_name": False,
            "shell_path": "", "user_scripts_folder": "", "folder_templates": [],
            "file_templates": [], "syntax_highlighting": True,
            "syntax_highlighting_mobile": False, "enabled_templates_hotkeys": [],
            "startup_templates": [], "intellisense_render": "1",
            "ignore_folders_on_creation": [],
        },
        ".obsidian/plugins/homepage/data.json": {
            "version": 4,
            "homepages": {
                "Main Homepage": {
                    "value": "Home", "kind": "File", "openOnStartup": True,
                    "openMode": "Replace all open notes", "manualOpenMode": "Keep open notes",
                    "view": "Reading view", "revertView": True, "openWhenEmpty": False,
                    "refreshDataview": False, "autoCreate": False, "autoScroll": False,
                    "pin": True, "commands": [], "alwaysApply": False, "hideReleaseNotes": False,
                }
            },
            "separateMobile": False,
        },
        ".obsidian/graph.json": {
            "collapse-filter": False, "search": "", "showTags": False,
            "showAttachments": False, "hideUnresolved": True, "showOrphans": False,
            "collapse-color-groups": False,
            "colorGroups": [
                {"query": "path:\"Mind Map\"", "color": {"a": 1, "rgb": 42747}},
                {"query": "path:Papers", "color": {"a": 1, "rgb": 16743168}},
                {"query": "path:Curriculum", "color": {"a": 1, "rgb": 3715072}},
                {"query": "path:Contacts", "color": {"a": 1, "rgb": 16196997}},
                {"query": "path:Organizations", "color": {"a": 1, "rgb": 16766474}},
                {"query": "path:Reports", "color": {"a": 1, "rgb": 15672124}},
                {"query": "path:Lectures", "color": {"a": 1, "rgb": 8599788}},
                {"query": "path:\"Robotics Intelligence\"", "color": {"a": 1, "rgb": 54472}},
            ],
            "collapse-display": False, "showArrow": True, "textFadeMultiplier": 0.65,
            "nodeSizeMultiplier": 1.35, "lineSizeMultiplier": 0.7,
            "collapse-forces": False, "centerStrength": 0.28,
            "repelStrength": 14.0, "linkStrength": 0.72, "linkDistance": 260,
            "scale": 0.55, "close": True,
        },
    }
    for relative, payload in settings.items():
        path = VAULT / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (VAULT / ".gitignore").write_text(
        ".obsidian/workspace.json\n.obsidian/workspace-mobile.json\n.obsidian/backlink.json\n"
        ".obsidian/themes/\n.obsidian/plugins/*/main.js\n.obsidian/plugins/*/manifest.json\n"
        ".obsidian/plugins/*/styles.css\n.obsidian/plugins/obsidian-style-settings/data.json\n"
        ".obsidian/plugins/obsidian-minimal-settings/data.json\n.trash/\n",
        encoding="utf-8",
    )
    css = """/* @settings
name: AI Research Lab
id: research-lab
settings:
  - id: research-accent
    title: Accent color
    type: variable-color
    format: hex
    default: '#4e6d5a'
  - id: research-reading-width
    title: Reading width
    type: variable-number-slider
    default: 860
    min: 680
    max: 1100
    step: 20
    format: px
*/
/* Warm editorial additions layered on the Minimal theme. */
:root {
  --research-cream: #f3f0e8;
  --research-ink: #24231f;
  --research-accent: #4e6d5a;
  --research-blue: #41687d;
  --research-reading-width: 860px;
  --file-line-width: var(--research-reading-width);
  --line-height-normal: 1.7;
  --heading-spacing: 2.2rem;
}
.theme-light {
  --background-primary: var(--research-cream);
  --background-secondary: #ebe6da;
  --text-normal: var(--research-ink);
  --interactive-accent: var(--research-accent);
  --link-color: var(--research-blue);
  --link-color-hover: var(--research-accent);
  --h1-color: #243c32;
  --h2-color: #315541;
}
.markdown-rendered,
.markdown-source-view.mod-cm6 .cm-scroller {
  font-variant-numeric: oldstyle-nums proportional-nums;
}
.markdown-rendered h1,
.markdown-rendered h2,
.markdown-rendered h3,
.markdown-rendered h4 {
  font-family: Georgia, "Times New Roman", serif;
  letter-spacing: -0.02em;
  text-wrap: balance;
}
.markdown-rendered h1 {
  border-bottom: 1px solid var(--background-modifier-border);
  padding-bottom: .35em;
}
.markdown-rendered p { text-wrap: pretty; }
.markdown-rendered blockquote {
  border-left-color: var(--research-accent);
  background: color-mix(in srgb, var(--research-accent) 7%, transparent);
  border-radius: 0 8px 8px 0;
  padding: .7rem 1rem;
}
.callout { border-radius: 10px; }
.markdown-rendered table {
  display: block;
  overflow-x: auto;
  width: 100%;
  border-collapse: collapse;
}
.markdown-rendered th {
  background: color-mix(in srgb, var(--research-accent) 10%, var(--background-primary));
}
.markdown-rendered tbody tr:nth-child(even) {
  background: color-mix(in srgb, var(--research-accent) 3%, transparent);
}
.markdown-rendered code:not(pre code) {
  border: 1px solid var(--background-modifier-border);
  border-radius: 4px;
}
.markdown-rendered img { border-radius: 8px; }
.markdown-rendered hr { margin: 3rem auto; width: 35%; }
.metadata-container {
  border-bottom: 1px solid var(--background-modifier-border);
  padding-bottom: .75rem;
}
.nav-file-title.is-active { border-left: 3px solid var(--research-accent); }
.markdown-rendered .internal-link {
  text-decoration-thickness: .08em;
  text-underline-offset: .14em;
}
.markdown-rendered .tag { border-radius: 999px; font-size: .8em; }
.markdown-rendered ul > li::marker { color: var(--research-accent); }
.markdown-rendered ol > li::marker { color: var(--research-accent); font-weight: 650; }
.markdown-rendered .callout[data-callout="abstract"] { --callout-color: 65, 104, 125; }
.markdown-rendered .callout[data-callout="important"] { --callout-color: 78, 109, 90; }
.markdown-rendered .callout[data-callout="tip"] { --callout-color: 174, 121, 64; }
.markdown-rendered .callout-title { font-family: Georgia, "Times New Roman", serif; }

/* A semantic visual language shared by every generated note family. */
.callout[data-callout="home"] { --callout-color: 45, 74, 62; --callout-icon: lucide-library-big; }
.callout[data-callout="graph"] { --callout-color: 65, 104, 125; --callout-icon: lucide-orbit; }
.callout[data-callout="concept"] { --callout-color: 78, 109, 90; --callout-icon: lucide-network; }
.callout[data-callout="paper"] { --callout-color: 45, 112, 100; --callout-icon: lucide-book-open-text; }
.callout[data-callout="curriculum"] { --callout-color: 204, 153, 78; --callout-icon: lucide-graduation-cap; }
.callout[data-callout="person"] { --callout-color: 168, 130, 174; --callout-icon: lucide-user-round; }
.callout[data-callout="organization"] { --callout-color: 173, 119, 78; --callout-icon: lucide-building-2; }
.callout[data-callout="intelligence"],
.callout[data-callout="report"] { --callout-color: 132, 104, 144; --callout-icon: lucide-radar; }
.callout[data-callout="jobs"] { --callout-color: 145, 112, 48; --callout-icon: lucide-briefcase-business; }
.callout[data-callout="signal"],
.callout[data-callout="skill"] { --callout-color: 174, 121, 64; --callout-icon: lucide-activity; }
.callout[data-callout="evidence"] { --callout-color: 55, 112, 108; --callout-icon: lucide-badge-check; }
.callout[data-callout="source"],
.callout[data-callout="method"] { --callout-color: 102, 104, 99; --callout-icon: lucide-file-check-2; }
.callout[data-callout="privacy"] { --callout-color: 137, 103, 83; --callout-icon: lucide-shield; }
.callout[data-callout="current"] { --callout-color: 174, 121, 64; --callout-icon: lucide-map-pin-check; }
.callout[data-callout="profile"] { --callout-color: 88, 108, 145; --callout-icon: lucide-contact-round; }
.callout[data-callout="lecture"] { --callout-color: 105, 88, 146; --callout-icon: lucide-presentation; }
.callout[data-callout="recording"] { --callout-color: 164, 78, 92; --callout-icon: lucide-audio-lines; }
.callout[data-callout="question"] { --callout-color: 174, 121, 64; --callout-icon: lucide-circle-help; }
.callout[data-callout="summary"] { --callout-color: 55, 112, 108; --callout-icon: lucide-notebook-tabs; }
.callout[data-callout="hierarchy"] { --callout-color: 88, 113, 91; --callout-icon: lucide-git-branch; }
.callout[data-callout="outgoing"] { --callout-color: 62, 111, 142; --callout-icon: lucide-arrow-up-right; }
.callout[data-callout="incoming"] { --callout-color: 132, 104, 144; --callout-icon: lucide-arrow-down-left; }
.callout[data-callout="palette"] { --callout-color: 0, 166, 251; --callout-icon: lucide-palette; }
.callout[data-callout="local"] { --callout-color: 56, 176, 0; --callout-icon: lucide-folder-check; }
.callout[data-callout="sequence"],
.callout[data-callout="prerequisite"] { --callout-color: 105, 117, 132; --callout-icon: lucide-route; }

.callout[data-callout="map"],
.callout[data-callout="links"],
.callout[data-callout="study"],
.callout[data-callout="concepts"],
.callout[data-callout="library"],
.callout[data-callout="people"],
.callout[data-callout="organizations"],
.callout[data-callout="desks"],
.callout[data-callout="reports"],
.callout[data-callout="sequence"],
.callout[data-callout="prerequisite"],
.callout[data-callout="hierarchy"] {
  --callout-color: 78, 109, 90;
  --callout-icon: lucide-layout-grid-2;
  background: color-mix(in srgb, rgb(var(--callout-color)) 5%, var(--background-primary));
}
.callout[data-callout="map"] .callout-content > ul,
.callout[data-callout="links"] .callout-content > ul,
.callout[data-callout="study"] .callout-content > ul,
.callout[data-callout="concepts"] .callout-content > ul,
.callout[data-callout="library"] .callout-content > ul,
.callout[data-callout="people"] .callout-content > ul,
.callout[data-callout="organizations"] .callout-content > ul,
.callout[data-callout="desks"] .callout-content > ul,
.callout[data-callout="reports"] .callout-content > ul,
.callout[data-callout="sequence"] .callout-content > ul,
.callout[data-callout="prerequisite"] .callout-content > ul,
.callout[data-callout="hierarchy"] .callout-content > ul {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(13rem, 1fr));
  gap: .55rem;
  list-style: none;
  padding-left: 0;
}
.callout[data-callout="map"] .callout-content > ul > li,
.callout[data-callout="links"] .callout-content > ul > li,
.callout[data-callout="study"] .callout-content > ul > li,
.callout[data-callout="concepts"] .callout-content > ul > li,
.callout[data-callout="library"] .callout-content > ul > li,
.callout[data-callout="people"] .callout-content > ul > li,
.callout[data-callout="organizations"] .callout-content > ul > li,
.callout[data-callout="desks"] .callout-content > ul > li,
.callout[data-callout="reports"] .callout-content > ul > li,
.callout[data-callout="sequence"] .callout-content > ul > li,
.callout[data-callout="prerequisite"] .callout-content > ul > li,
.callout[data-callout="hierarchy"] .callout-content > ul > li {
  margin: 0;
  padding: .65rem .75rem;
  border: 1px solid color-mix(in srgb, rgb(var(--callout-color)) 22%, var(--background-modifier-border));
  border-radius: 8px;
  background: color-mix(in srgb, rgb(var(--callout-color)) 4%, var(--background-primary));
}
.research-note .callout { border: 1px solid color-mix(in srgb, rgb(var(--callout-color)) 20%, transparent); }
.research-note .callout-title { font-size: 1.02em; letter-spacing: .01em; }
.research-note .callout-content > :last-child { margin-bottom: 0; }
.paper-note .markdown-rendered img {
  display: block;
  max-height: 34rem;
  margin: 1.4rem auto .6rem;
  box-shadow: 0 8px 26px rgb(40 35 26 / 9%);
}
.paper-note .markdown-rendered h2 { margin-top: 3.2rem; }
.curriculum-hub .markdown-rendered table,
.jobs-note .markdown-rendered table { font-size: .92em; }
.home-note .markdown-rendered table td:first-child { font-weight: 650; color: var(--research-accent); }
.report-note .markdown-rendered h2 { border-bottom: 1px solid var(--background-modifier-border); padding-bottom: .25em; }
@media (max-width: 700px) {
  :root { --research-reading-width: 100%; }
  .callout .callout-content > ul { grid-template-columns: 1fr !important; }
  .markdown-rendered table { font-size: .88em; }
}
"""
    path = VAULT / ".obsidian/snippets/research-lab.css"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(css, encoding="utf-8")


def node_path(node_id: str) -> str:
    return f"Mind Map/Nodes/{node_id}.md"


def build_mindmap() -> dict[str, str]:
    data = load_json("intelligence/mindmap.json")
    nodes = data["nodes"]
    by_id = {node["id"]: node for node in nodes}
    children: dict[str, list[dict[str, Any]]] = defaultdict(list)
    outgoing: dict[str, list[tuple[str, str]]] = defaultdict(list)
    incoming: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for node in nodes:
        if node.get("parent"):
            children[node["parent"]].append(node)
    for edge in data["edges"]:
        source_id, target_id, relation = edge["from"], edge["to"], edge["rel"]
        # Parent/child membership already has an explicit hierarchy section. Do
        # not duplicate the same structural edge as a semantic relationship.
        if (
            by_id.get(target_id, {}).get("parent") == source_id
            or by_id.get(source_id, {}).get("parent") == target_id
        ) and relation in {"contains", "includes"}:
            continue
        outgoing[source_id].append((target_id, relation))
        incoming[target_id].append((source_id, relation))

    entities = load_json("intelligence/entities.json")
    orgs = {item["id"]: item for item in entities["organizations"]}
    people = {item["id"]: item for item in entities["people"]}
    associations: dict[str, list[dict[str, Any]]] = defaultdict(list)
    contributions: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in entities["associations"]:
        associations[item["node_id"]].append(item)
    for item in entities["contributions"]:
        contributions[item["node_id"]].append(item)

    paper_links: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for spec in PAPER_SPECS.values():
        for node_id in spec["nodes"]:
            paper_links[node_id].append((f"Papers/{spec['title']}.md", spec["title"]))

    curriculum_links: dict[str, list[tuple[str, str]]] = defaultdict(list)
    plan = load_json("curriculum_plan.json")
    domain_roots = {
        "Machine Learning": ("learning",),
        "Computer Vision": ("perception",),
        "Embodied AI & RL Robotics": ("policy", "systems"),
    }
    for lesson in plan["lessons"]:
        day = int(lesson["day"])
        title = f"Day {day:02d} - {safe_filename(lesson['topic'])}"
        text = " ".join([lesson["topic"], *lesson.get("foundation_threads", [])])
        related_ids = related_node_ids(text, nodes, roots=domain_roots.get(lesson["domain"], ()), limit=6)
        for node_id in related_ids:
            curriculum_links[node_id].append((f"Curriculum/Lessons/{title}.md", title))

    paths = {node["id"]: node_path(node["id"]) for node in nodes}
    for node in nodes:
        parent = node.get("parent")
        hierarchy: list[tuple[str, str]] = []
        if parent and parent in by_id:
            hierarchy.append((node_path(parent), f"↑ {by_id[parent]['label']}"))
        hierarchy.extend(
            (node_path(child["id"]), f"↓ {child['label']}")
            for child in sorted(children.get(node["id"], []), key=lambda item: item["label"].lower())
        )
        outbound = sorted(outgoing.get(node["id"], []), key=lambda item: (item[1], by_id[item[0]]["label"].lower()))
        inbound = sorted(incoming.get(node["id"], []), key=lambda item: (item[1], by_id[item[0]]["label"].lower()))
        evidence_links = [*paper_links.get(node["id"], []), *curriculum_links.get(node["id"], [])[:6]]
        lines = [
            frontmatter(
                type="mindmap-node", aliases=[node["label"]], node_id=node["id"],
                kind=node["kind"], domain=node["domain"], layer=node["layer"],
                source="intelligence/mindmap.json", updated=data["updated"],
                tags=["mindmap", node["domain"], node["kind"]],
                cssclasses=["research-note", "concept-note"],
                related_papers=[path for path, _ in paper_links.get(node["id"], [])],
                related_curriculum=[path for path, _ in curriculum_links.get(node["id"], [])[:6]],
            ),
            nav("Mind Map/Embodied AI.md", "Knowledge Graph"), "",
            f"# {node['label']}", "",
            *callout(
                "concept",
                f"{node['kind'].replace('-', ' ').title()} · {node['domain'].replace('-', ' ').title()} · Layer {node['layer']}",
                [node.get("brief", "No brief recorded."), "", f"**Why it belongs —** {node.get('why', 'No rationale recorded yet.')}"],
            ), "",
            "## Knowledge neighborhood", "",
            *link_callout("Hierarchy", hierarchy, "hierarchy"), "",
        ]
        if outbound:
            lines.extend(callout(
                "outgoing", "Outgoing relationships",
                [f"- **{relation.replace('-', ' ')} →** {wiki(node_path(other_id), by_id[other_id]['label'])}" for other_id, relation in outbound],
            ))
            lines.append("")
        if inbound:
            lines.extend(callout(
                "incoming", "Incoming relationships",
                [f"- **← {relation.replace('-', ' ')} —** {wiki(node_path(other_id), by_id[other_id]['label'])}" for other_id, relation in inbound],
            ))
            lines.append("")
        if evidence_links:
            lines.extend([*link_callout("Read and study", evidence_links, "study"), ""])
        if node.get("research_directions"):
            lines.extend(["## Research directions", "", *[f"- {item}" for item in node["research_directions"]], ""])
        provenance: list[str] = []
        for item in associations.get(node["id"], []):
            org = orgs[item["organization_id"]]
            org_link = wiki(f"Organizations/{org['id']}.md", org["name"])
            provenance.append(f"- {org_link} — {item['relationship']} _(verified {item['verified_on']})_")
        for item in contributions.get(node["id"], []):
            person = people[item["person_id"]]
            person_link = wiki(f"Contacts/{person['id']}.md", person["name"])
            provenance.append(f"- {person_link} — {item['relationship']} _(verified {item['verified_on']})_")
        if provenance:
            lines.extend([*callout("evidence", "Verified public provenance", provenance), ""])
        if node.get("resources"):
            lines.extend(["## Primary resources", ""])
            for resource in node["resources"]:
                url = resource["url"]
                local_link = local_site_wikilink(url, resource["title"])
                rendered_link = local_link or markdown_link(resource["title"], url)
                lines.append(f"- **{resource['type'].title()}:** {rendered_link}")
            lines.append("")
        lines.extend(callout(
            "source", "Local source record",
            [
                f"- Canonical data: `intelligence/mindmap.json#{node['id']}`",
                f"- Vault map: {wiki('Mind Map/Embodied AI.md', 'Embodied AI Knowledge Graph')}",
                "- This note is the complete local concept record; no published mirror is required.",
            ],
        ))
        write(paths[node["id"]], "\n".join(lines))

    domains = sorted((node for node in nodes if node["layer"] == 1), key=lambda item: item["label"])
    overview = [
        frontmatter(
            type="map-of-content", aliases=["Embodied AI Mind Map", "Embodied AI Knowledge Graph"],
            tags=["moc", "mindmap"], source="intelligence/mindmap.json",
            cssclasses=["research-note", "hub-note", "graph-hub"],
        ),
        nav("Mind Map/Embodied AI.md", "Knowledge Graph"), "",
        "# Embodied AI Knowledge Graph", "",
        *callout(
            "graph", "The research system",
            [data["scope"], "", f"**{len(nodes)} concepts** · **{len(data['edges'])} semantic relationships** · updated **{data['updated']}**"],
        ), "",
        *link_callout("Enter through a branch", ((node_path(node["id"]), node["label"]) for node in domains), "map"), "",
        "## How to navigate", "",
        "1. Open **Graph View** for the whole research system.",
        "2. Open a concept's **Local Graph** for one- or two-hop context.",
        "3. Follow **Read and study** to move from a concept into papers and curriculum.",
        "4. Follow provenance links to the people and organizations behind the work.", "",
        "## Recent evolution", "",
    ]
    for item in reversed(data.get("changelog", [])[-10:]):
        overview.append(f"- **{item['date']}** — {item['note']}")
    write("Mind Map/Embodied AI.md", "\n".join(overview))
    return paths


def prepare_article(article: Tag, paper_file_map: dict[str, str], slug: str) -> str:
    clone = BeautifulSoup(str(article), "html.parser")
    blocks: dict[str, str] = {}

    def text(element: Tag | None) -> str:
        return re.sub(r"\s+", " ", element.get_text(" ", strip=True)).strip() if element else ""

    def stash(element: Tag, markdown: str) -> None:
        marker = f"OBSMDZ{len(blocks):03d}Z"
        blocks[marker] = markdown.strip()
        element.replace_with(marker)

    # Preserve rich visual structures as readable, portable Markdown instead of
    # flattening nested HTML into concatenated text.
    for figure in list(clone.select("figure.video-embed")):
        iframe = figure.find("iframe")
        if not iframe:
            continue
        src = iframe.get("src", "")
        watch_url = src.replace("youtube.com/embed/", "youtube.com/watch?v=")
        title = iframe.get("title", "Video")
        caption = text(figure.find("figcaption"))
        body = [f"> [!video] {title}", f"> [Watch video]({watch_url})"]
        if caption:
            body.extend([">", f"> {caption}"])
        stash(figure, "\n".join(body))

    for step in list(clone.select(".case-step")):
        number = text(step.select_one(".n"))
        human = step.select_one(".human")
        model = step.select_one(".model")
        human_title = text(human.find(["h3", "h4"])) if human else "You"
        model_title = text(model.find(["h3", "h4"])) if model else "The paper"
        human_body = text(human.find("p")) if human else ""
        model_body = text(model.find("p")) if model else ""
        stash(step, "\n".join([
            f"> [!example] Step {number} — {human_title}",
            f"> **{human_title}:** {human_body}",
            ">",
            f"> **{model_title}:** {model_body}",
        ]))

    for comparison in list(clone.select(".compare")):
        panes = comparison.select(":scope > .pane")
        rows = []
        for pane in panes:
            heading = text(pane.find(["h3", "h4"])) or "Alternative"
            token_rows = []
            for token_row in pane.select(".token-row"):
                tokens = [text(token) for token in token_row.select(".token")]
                token_rows.append(" → ".join(filter(None, tokens)))
                token_row.decompose()
            detail = text(pane)
            if token_rows:
                detail = " · ".join([*token_rows, detail]).strip(" ·")
            rows.append((heading, detail))
        if rows:
            table = ["| Alternative | Representation and consequence |", "|---|---|"]
            table.extend(f"| **{table_cell(name)}** | {table_cell(detail)} |" for name, detail in rows)
            stash(comparison, "\n".join(table))

    for architecture in list(clone.select(".arch")):
        flow = ["> [!flow] Architecture / data flow"]
        for child in architecture.find_all(recursive=False):
            child_classes = set(child.get("class", []))
            if "arch-row" in child_classes:
                boxes = []
                for box in child.select(":scope > .arch-box"):
                    small = box.find("small")
                    detail = text(small)
                    if small:
                        small.decompose()
                    label = text(box)
                    boxes.append(f"**{label}**" + (f" — {detail}" if detail else ""))
                if boxes:
                    flow.append("> " + " + ".join(boxes))
            elif "arch-down" in child_classes:
                flow.append(f"> {text(child)}")
        stash(architecture, "\n".join(flow))

    for graph in list(clone.select(".graph-stack")):
        lines = ["> [!graph] Concept flow"]
        for child in graph.find_all(recursive=False):
            child_classes = set(child.get("class", []))
            if "graph-level" in child_classes:
                nodes = [text(node) for node in child.select(".kg-node")]
                if nodes:
                    lines.append("> **" + " · ".join(nodes) + "**")
            elif "graph-v" in child_classes:
                lines.append(f"> {text(child)}")
        stash(graph, "\n".join(lines))

    for graph in list(clone.select(".knowledge-graph")):
        raw = graph.get_text("\n", strip=False).strip("\n")
        raw = re.sub(r"\n[ \t]*\n", "\n", raw)
        stash(graph, f"```text\n{raw}\n```")

    for row in list(clone.select(".bar-row")):
        direct = [text(child) for child in row.find_all(recursive=False) if "bar-track" not in child.get("class", [])]
        direct = [value for value in direct if value]
        stash(row, "- " + " — ".join(direct))

    for token_row in list(clone.select(".token-row")):
        tokens = [text(token) for token in token_row.select(".token")]
        stash(token_row, "`" + " → ".join(filter(None, tokens)) + "`")

    for svg in list(clone.find_all("svg")):
        label = svg.get("aria-label") or svg.get("title") or "Paper diagram"
        labels = " · ".join(dict.fromkeys(filter(None, (text(node) for node in svg.find_all("text")))))
        body = [f"> [!diagram] {label}"]
        if labels:
            body.append(f"> {labels}")
        stash(svg, "\n".join(body))

    # Catch any iframe not enclosed by the paper's video figure component.
    for iframe in list(clone.find_all("iframe")):
        src = iframe.get("src", "")
        title = iframe.get("title", "Video")
        watch_url = src.replace("youtube.com/embed/", "youtube.com/watch?v=")
        stash(iframe, f"> [!video] {title}\n> [Watch video]({watch_url})")

    for image in clone.find_all("img"):
        src = image.get("src", "")
        if src.startswith(("http://", "https://")):
            filename = Path(urlparse(src).path).name
            asset_relative = Path("_attachments") / "Papers" / slug / filename
            asset_path = VAULT / asset_relative
            if not filename or not asset_path.is_file():
                raise FileNotFoundError(f"Missing localized paper image for {src}: {asset_path}")
            image["src"] = f"../{asset_relative.as_posix()}"

    for anchor in clone.find_all("a"):
        href = anchor.get("href", "")
        label = anchor.get_text(" ", strip=True) or href
        local_link = local_site_wikilink(href, label, paper_file_map)
        if local_link:
            anchor.replace_with(local_link)
        elif href and not href.startswith(("http://", "https://", "#")):
            # Unknown first-party navigation is not allowed to become a web
            # dependency. Its surrounding article content is already local.
            anchor.replace_with(label)
    markdown = html_to_markdown(str(clone), heading_style="ATX", bullets="-", strip=["article", "div", "span"])
    for marker, block in blocks.items():
        markdown = markdown.replace(marker, f"\n\n{block}\n\n")
    markdown = re.sub(r"[ \t]+\n", "\n", markdown)
    markdown = re.sub(r"\n{3,}", "\n\n", markdown)
    markdown = markdown.replace("\\[", "$$\n").replace("\\]", "\n$$")
    return markdown.strip()


def build_papers(node_paths: dict[str, str]) -> dict[str, str]:
    paper_file_map = {f"papers-{slug}.html": slug for slug in PAPER_SPECS}
    mindmap = load_json("intelligence/mindmap.json")
    nodes = mindmap["nodes"]
    node_labels = {node["id"]: node["label"] for node in nodes}
    plan = load_json("curriculum_plan.json")
    domain_roots = {
        "Machine Learning": ("learning",),
        "Computer Vision": ("perception",),
        "Embodied AI & RL Robotics": ("policy", "systems"),
    }
    lesson_nodes: list[tuple[str, str, set[str]]] = []
    for lesson in plan["lessons"]:
        day = int(lesson["day"])
        title = f"Day {day:02d} - {safe_filename(lesson['topic'])}"
        text = " ".join([lesson["topic"], *lesson.get("foundation_threads", [])])
        ids = set(related_node_ids(text, nodes, roots=domain_roots.get(lesson["domain"], ()), limit=6))
        lesson_nodes.append((f"Curriculum/Lessons/{title}.md", title, ids))

    output_paths: dict[str, str] = {}
    for slug, spec in PAPER_SPECS.items():
        html_path = ROOT / "site" / f"papers-{slug}.html"
        soup = BeautifulSoup(html_path.read_text(encoding="utf-8"), "html.parser")
        article = soup.select_one("article.technical-article")
        if article is None:
            raise ValueError(f"Missing article.technical-article in {html_path}")
        header_title = soup.select_one("header.publication-header h1")
        title = spec["title"]
        display_title = header_title.get_text(" ", strip=True) if header_title else title
        description = soup.find("meta", attrs={"name": "description"})
        summary = description["content"] if description and description.get("content") else "Complete technical reading guide."
        aliases = [title]
        if display_title != title:
            aliases.append(display_title)
        related_nodes = [node_id for node_id in spec["nodes"] if node_id in node_paths]
        curriculum = [(path, label) for path, label, ids in lesson_nodes if ids.intersection(related_nodes)][:8]
        lines = [
            frontmatter(
                type="paper-guide", aliases=aliases, paper_slug=slug,
                source=[f"site/papers-{slug}.html", f"papers/{spec['source']}"],
                content_mode="local", tags=["paper", "reading-guide"],
                related_nodes=related_nodes, related_curriculum=[path for path, _ in curriculum],
                cssclasses=["research-note", "paper-note"],
            ),
            nav("Papers/Paper Guides.md", "Paper Guides"), "",
            f"# {display_title}", "",
            *callout(
                "paper", "Research reading guide",
                [summary, "", f"**Concepts:** {len(related_nodes)} · **Related curriculum notes:** {len(curriculum)}"],
            ), "",
            *link_callout(
                "Connected concepts",
                ((node_paths[node_id], node_labels.get(node_id, node_id)) for node_id in related_nodes),
                "concepts",
            ), "",
        ]
        if curriculum:
            lines.extend([*link_callout("Continue in the curriculum", curriculum, "study"), ""])
        lines.extend([
            *callout(
                "source", "Local reconstruction and provenance",
                [
                    "- This note contains the complete recreated reading guide; no published mirror is required.",
                    f"- Canonical editorial source: `site/papers-{slug}.html`",
                    f"- Companion source: `papers/{spec['source']}`",
                    f"- Local figures: `_attachments/Papers/{slug}/`",
                    "- Primary papers, repositories, and videos remain linked as evidence.",
                ],
            ), "", "---", "", prepare_article(article, paper_file_map, slug),
        ])
        relative = f"Papers/{title}.md"
        output_paths[slug] = relative
        write(relative, "\n".join(lines))
    index = [
        frontmatter(
            type="map-of-content", aliases=["Paper Reading Guides"], tags=["moc", "papers"],
            cssclasses=["research-note", "hub-note", "papers-hub"],
        ),
        nav("Papers/Paper Guides.md", "Paper Guides"), "",
        "# Paper Reading Guides", "",
        *callout(
            "paper", "From human intuition to model mechanism",
            [
                "Self-contained companions generated from the canonical editorial HTML guides.",
                "", f"**{len(output_paths)} complete guides** · CLIP-Meets-DINO and FaultAdapt remain intentionally excluded.",
            ],
        ), "",
        *link_callout("Reading library", ((path, PAPER_SPECS[slug]["title"]) for slug, path in output_paths.items()), "library"), "",
        "## Editorial protocol", "",
        "1. Begin with the human case study and prerequisites.",
        "2. Walk through the paper in its original order.",
        "3. Name the model mechanism precisely.",
        "4. Tie results to their evaluation protocol and separate evidence from hypotheses.", "",
        *callout(
            "local", "Local-first library",
            [
                "Every guide is fully recreated inside this vault, including its figures and cross-links.",
                "External links are retained only for primary evidence, repositories, and videos.",
            ],
        ),
    ]
    write("Papers/Paper Guides.md", "\n".join(index))
    return output_paths


def build_contacts(node_paths: dict[str, str]) -> tuple[dict[str, str], dict[str, str]]:
    entities = load_json("intelligence/entities.json")
    ecosystem = load_json("intelligence/ecosystem.json")
    jobs = load_json("intelligence/jobs.json")
    people = {item["id"]: item for item in entities["people"]}
    provenance_orgs = {item["id"]: dict(item) for item in entities["organizations"]}
    ecosystem_orgs = {item["company_id"]: item for item in ecosystem["companies"]}
    organizations = {**provenance_orgs}
    for org_id, company in ecosystem_orgs.items():
        organizations.setdefault(org_id, {"id": org_id, "name": company["name"], "kind": "company", "url": company["careers_url"]})

    contrib_by_person: dict[str, list[dict[str, Any]]] = defaultdict(list)
    assoc_by_org: dict[str, list[dict[str, Any]]] = defaultdict(list)
    people_by_org: dict[str, list[dict[str, Any]]] = defaultdict(list)
    jobs_by_company: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in entities["contributions"]:
        contrib_by_person[item["person_id"]].append(item)
    for item in entities["associations"]:
        assoc_by_org[item["organization_id"]].append(item)
    for person in people.values():
        if person.get("organization_id"):
            people_by_org[person["organization_id"]].append(person)
    for opening in jobs["openings"]:
        jobs_by_company[opening["company"]].append(opening)

    org_paths = {org_id: f"Organizations/{org_id}.md" for org_id in organizations}
    person_paths = {person_id: f"Contacts/{person_id}.md" for person_id in people}

    mindmap_nodes = load_json("intelligence/mindmap.json")["nodes"]
    node_labels = {node["id"]: node["label"] for node in mindmap_nodes}

    for person_id, person in people.items():
        org_id = person.get("organization_id")
        affiliation = organizations.get(org_id) if org_id else None
        lines = [
            frontmatter(
                type="public-contact", aliases=[person["name"]], contact_id=person_id,
                organization_id=org_id, verified_on=person["verified_on"],
                source="intelligence/entities.json", tags=["contact", "public-record"],
                cssclasses=["research-note", "person-note"],
            ),
            nav("Contacts/Contacts.md", "Research Contacts"), "",
            f"# {person['name']}", "",
            *callout(
                "person", person["role"],
                [
                    f"**Affiliation:** {wiki(org_paths[org_id], affiliation['name']) if affiliation else 'Independent / not recorded'}",
                    f"**Public record verified:** {person['verified_on']}",
                ],
            ), "",
        ]
        contributions = []
        for item in contrib_by_person.get(person_id, []):
            if item["node_id"] in node_paths:
                label = node_labels.get(item["node_id"], item["node_id"])
                contributions.append(
                    f"- {wiki(node_paths[item['node_id']], label)} — {item['relationship']} _(verified {item['verified_on']})_"
                )
        if contributions:
            lines.extend([*callout("evidence", "Verified contributions", contributions), ""])
        profiles = [f"- {markdown_link('Research profile', person['profile_url'])}"]
        if person.get("linkedin_url"):
            profiles.append(f"- {markdown_link('Verified LinkedIn', person['linkedin_url'])}")
        lines.extend([*callout("profile", "Public profiles", profiles), "", "## Source ledger", ""])
        for source in person["sources"]:
            lines.append(f"- {markdown_link(source['title'], source['url'])}")
        lines.extend(["", *callout(
            "privacy", "Public provenance boundary",
            ["No outreach ranking, contact history, private notes, or message drafts belong in this repository."],
        )])
        write(person_paths[person_id], "\n".join(lines))

    for org_id, org in organizations.items():
        company = ecosystem_orgs.get(org_id)
        concept_rows = []
        if org.get("map_node_id") in node_paths:
            concept_rows.append((node_paths[org["map_node_id"]], node_labels.get(org["map_node_id"], org["name"])))
        for item in assoc_by_org.get(org_id, []):
            if item["node_id"] in node_paths:
                concept_rows.append((node_paths[item["node_id"]], node_labels.get(item["node_id"], item["node_id"])))
        organization_text = " ".join([
            org["name"],
            company.get("focus", "") if company else "",
            company.get("category", "") if company else "",
        ])
        for node_id in related_node_ids(organization_text, mindmap_nodes, limit=4):
            if node_id in node_paths:
                concept_rows.append((node_paths[node_id], node_labels[node_id]))
        concept_rows = list(dict.fromkeys(concept_rows))
        lines = [
            frontmatter(
                type="organization", aliases=[org["name"]], organization_id=org_id,
                organization_kind=org.get("kind", "company"),
                source="intelligence/entities.json" if org_id in provenance_orgs else "intelligence/ecosystem.json",
                tags=["organization", org.get("kind", "company")],
                cssclasses=["research-note", "organization-note"],
                related_concepts=[path for path, _ in concept_rows],
            ),
            nav("Organizations/Organizations.md", "Organizations"), "",
            f"# {org['name']}", "",
        ]
        if company:
            lines.extend([
                *callout("organization", company["category"], [company["focus"]]), "",
                "| Founded | Location | Stage |", "|---|---|---|",
                f"| {company['founded']} | {company['hq_city']}, {company['hq_state']} · {company['cluster']} | {company['stage']} |", "",
                *callout(
                    "signal", "Verified market observation",
                    [
                        f"**Valuation:** {company['valuation_label']} — {company['valuation_type']}, {company['valuation_as_of']}",
                        company["valuation_note"],
                        f"**Careers:** {markdown_link('Official careers page', company['careers_url'])}",
                    ],
                ), "",
            ])
        elif org.get("url"):
            lines.extend([*callout("organization", org.get("kind", "Organization").replace("-", " ").title(), [markdown_link("Official site", org["url"])]), ""])
        if concept_rows:
            lines.extend([*link_callout("Connected research", concept_rows, "concepts"), ""])
        if people_by_org.get(org_id):
            lines.extend([*link_callout(
                "Verified public people",
                ((person_paths[person["id"]], person["name"]) for person in people_by_org[org_id]),
                "people",
            ), ""])
        company_jobs = jobs_by_company.get(org["name"], [])
        if company_jobs:
            job_rows = [
                f"- {markdown_link(opening['title'], opening['url'])} — {opening['location']}"
                for opening in sorted(company_jobs, key=lambda item: item["title"])[:12]
            ]
            if len(company_jobs) > 12:
                job_rows.append(f"- …and {len(company_jobs) - 12} more in {wiki('Robotics Intelligence/Current Openings.md', 'Current Openings')}.")
            lines.extend([*callout("jobs", f"{len(company_jobs)} tracked openings", job_rows), ""])
        if company and company.get("sources"):
            lines.extend(["## Source ledger", ""])
            for source in company["sources"]:
                lines.append(f"- {markdown_link(source['title'], source['url'])} — {source.get('date', '')}")
        lines.extend(["", *callout(
            "privacy", "Public record boundary",
            ["Career preparation and outreach remain private and outside this repository."],
        )])
        write(org_paths[org_id], "\n".join(lines))

    contacts_index = [
        frontmatter(
            type="map-of-content", aliases=["Research Contacts"], tags=["moc", "contacts"],
            source="intelligence/entities.json", cssclasses=["research-note", "hub-note", "contacts-hub"],
        ),
        nav("Contacts/Contacts.md", "Research Contacts"), "",
        "# Research Contacts", "",
        *callout(
            "person", "People behind the research",
            [
                "Verified public researchers and contributors connected to the knowledge graph.",
                "", f"**{len(people)} verified public records** · updated **{entities['updated_on']}**",
            ],
        ), "",
        *link_callout(
            "People directory",
            ((person_paths[person["id"]], person["name"]) for person in sorted(people.values(), key=lambda item: item["name"])),
            "people",
        ), "",
        *callout(
            "privacy", "Boundary",
            ["This is public provenance, not a networking CRM. Private prioritization, outreach, and follow-up records stay outside the repository."],
        ),
    ]
    write("Contacts/Contacts.md", "\n".join(contacts_index))

    by_kind: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for org_id, org in organizations.items():
        kind = org.get("kind", "company").replace("-", " ").title()
        by_kind[kind].append((org_paths[org_id], org["name"]))
    organizations_index = [
        frontmatter(
            type="map-of-content", aliases=["Organizations"], tags=["moc", "organizations"],
            cssclasses=["research-note", "hub-note", "organizations-hub"],
        ),
        nav("Organizations/Organizations.md", "Organizations"), "",
        "# Organizations", "",
        *callout(
            "organization", "Labs, universities, and robotics companies",
            ["Distinct public records connected to concepts, people, jobs, and intelligence reports.", "", f"**{len(organizations)} tracked organizations**"],
        ), "",
    ]
    for kind in sorted(by_kind):
        organizations_index.extend([*link_callout(kind, sorted(by_kind[kind], key=lambda item: item[1]), "organizations"), ""])
    write("Organizations/Organizations.md", "\n".join(organizations_index))
    return person_paths, org_paths


def build_robotics_intelligence(org_paths: dict[str, str]) -> None:
    ecosystem = load_json("intelligence/ecosystem.json")
    jobs = load_json("intelligence/jobs.json")
    companies = sorted(ecosystem["companies"], key=lambda item: item["name"])
    company_paths = {company["name"]: org_paths.get(company["company_id"]) for company in companies}
    overview = [
        frontmatter(
            type="map-of-content", aliases=["Robotics Intelligence"], tags=["moc", "robotics-intelligence"],
            as_of=ecosystem["as_of"], cssclasses=["research-note", "hub-note", "intelligence-hub"],
        ),
        nav("Robotics Intelligence/Robotics Intelligence.md", "Robotics Intelligence"), "",
        "# Robotics Intelligence", "",
        *callout(
            "intelligence", "Evidence before narrative",
            [ecosystem["scope"], "", f"**Ecosystem:** {ecosystem['as_of']} · **jobs checked:** {jobs['last_checked']}"],
        ), "",
        *link_callout(
            "Intelligence desks",
            [
                ("Robotics Intelligence/Current Openings.md", "Current Openings"),
                ("Robotics Intelligence/Skill Signals.md", "Recurring Skill Signals"),
                ("Reports/Daily Reports.md", "Dated Intelligence Reports"),
            ],
            "desks",
        ), "",
        *link_callout(
            "Tracked companies",
            ((org_paths[company["company_id"]], company["name"]) for company in companies if company["company_id"] in org_paths),
            "organizations",
        ), "",
        *callout("method", "Methodology", [ecosystem["funding_methodology"], "", ecosystem["valuation_methodology"]]),
    ]
    write("Robotics Intelligence/Robotics Intelligence.md", "\n".join(overview))

    sorted_openings = sorted(jobs["openings"], key=lambda row: (row["company"], row["title"]))
    by_company: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in sorted_openings:
        by_company[item["company"]].append(item)
    early_career = [
        item for item in sorted_openings
        if str(item.get("seniority", "")).lower() in {"internship", "new grad", "entry level"}
    ]
    openings = [
        frontmatter(
            type="dataset-view", aliases=["Current Robotics Openings"], tags=["jobs", "robotics-intelligence"],
            last_checked=jobs["last_checked"], cssclasses=["research-note", "dataset-note", "jobs-note"],
        ),
        nav("Robotics Intelligence/Robotics Intelligence.md", "Robotics Intelligence"), "",
        "# Current Openings", "",
        *callout(
            "jobs", "Official-board snapshot",
            [jobs["methodology"], "", f"**{len(sorted_openings)} openings** · checked **{jobs['last_checked']}** · always verify the official page"],
        ), "",
    ]
    if early_career:
        early_rows = [
            f"- **{item['company']} —** {markdown_link(item['title'], item['url'])} · {item['location']}"
            for item in early_career
        ]
        openings.extend([*callout("current", f"Early-career roles · {len(early_career)}", early_rows), ""])
    for company_name, company_openings in sorted(by_company.items()):
        company_heading = wiki(company_paths[company_name], company_name) if company_paths.get(company_name) else company_name
        openings.extend([
            f"## {company_heading} · {len(company_openings)}", "",
            "| Role | Location | Seniority | Last seen |", "|---|---|---|---|",
        ])
        for item in company_openings:
            role = markdown_link(table_cell(item["title"]), item["url"])
            openings.append(f"| {role} | {table_cell(item['location'])} | {table_cell(item['seniority'])} | {table_cell(item['last_seen'])} |")
        openings.append("")
    write("Robotics Intelligence/Current Openings.md", "\n".join(openings))

    signals = [
        frontmatter(
            type="dataset-view", aliases=["Robotics Skill Signals"], tags=["skills", "robotics-intelligence"],
            last_checked=jobs["last_checked"], cssclasses=["research-note", "dataset-note", "signals-note"],
        ),
        nav("Robotics Intelligence/Robotics Intelligence.md", "Robotics Intelligence"), "",
        "# Recurring Skill Signals", "",
        *callout(
            "signal", "Repeated requirements, not career advice",
            ["Patterns across official boards, kept distinct from personal outreach and private planning.", "", f"**{len(jobs['requirement_signals'])} tracked signals** · checked **{jobs['last_checked']}**"],
        ), "",
    ]
    for signal in jobs["requirement_signals"]:
        signals.extend([
            *callout(
                "skill", signal["skill"],
                [f"**Category:** {signal['category']}", f"**Evidence:** {signal['evidence']}", f"**Portfolio response:** {signal['portfolio_response']}"],
            ), "",
        ])
    write("Robotics Intelligence/Skill Signals.md", "\n".join(signals))


def extract_streamlit_article(source: Path) -> str:
    """Export literal Streamlit teaching prose to durable Markdown.

    Interactive widgets and generated plots remain in the app; headings, prose,
    equations, code, cautions, captions, and literal video links become part of
    the corresponding Obsidian lesson.
    """
    tree = ast.parse(source.read_text(encoding="utf-8"))
    article = next(
        (node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "_render_article"),
        None,
    )
    if article is None:
        return ""

    def literal(node: ast.AST) -> Any | None:
        try:
            return ast.literal_eval(node)
        except (ValueError, TypeError, SyntaxError):
            return None

    functions = {
        node.name: node for node in tree.body if isinstance(node, ast.FunctionDef)
    }

    def streamlit_calls(function: ast.FunctionDef, seen: set[str] | None = None) -> list[ast.Call]:
        seen = set(seen or ())
        if function.name in seen:
            return []
        seen.add(function.name)
        candidates = sorted(
            (node for node in ast.walk(function) if isinstance(node, ast.Call)),
            key=lambda node: (node.lineno, node.col_offset),
        )
        result: list[ast.Call] = []
        for call_node in candidates:
            if (
                isinstance(call_node.func, ast.Attribute)
                and isinstance(call_node.func.value, ast.Name)
                and call_node.func.value.id == "st"
            ):
                result.append(call_node)
            elif isinstance(call_node.func, ast.Name) and call_node.func.id in functions:
                helper = functions[call_node.func.id]
                if helper.name.startswith("_render_"):
                    result.extend(streamlit_calls(helper, seen))
        return result

    rendered: list[str] = []
    calls = streamlit_calls(article)
    for node in calls:
        method = node.func.attr
        if not node.args:
            continue
        value = literal(node.args[0])
        if not isinstance(value, str):
            continue
        value = textwrap.dedent(value).strip()
        if not value:
            continue
        if method == "header":
            rendered.extend([f"## {value}", ""])
        elif method == "subheader":
            rendered.extend([f"### {value}", ""])
        elif method == "markdown":
            if re.search(r"<[A-Za-z][^>]*>", value):
                value = html_to_markdown(value, heading_style="ATX", bullets="-", strip=["div", "span"]).strip()
                value = value.replace("  \n", "\\\n")
            rendered.extend([value, ""])
        elif method == "latex":
            rendered.extend(["$$", value, "$$", ""])
        elif method == "code":
            language = ""
            for keyword in node.keywords:
                if keyword.arg == "language":
                    candidate = literal(keyword.value)
                    if isinstance(candidate, str):
                        language = candidate
            rendered.extend([f"```{language}", value, "```", ""])
        elif method == "caption":
            rendered.extend([f"*{value}*", ""])
        elif method in {"info", "warning"}:
            rendered.extend([*callout(method, method.title(), value.splitlines()), ""])
        elif method == "video":
            rendered.extend([f"> [!video] Lecture companion\n> [Open video]({value})", ""])
    markdown = "\n".join(rendered)
    markdown = re.sub(r"\n{3,}", "\n\n", markdown)
    return markdown.strip()


def build_curriculum(node_paths: dict[str, str]) -> None:
    plan = load_json("curriculum_plan.json")
    state = load_json("curriculum_state.json")
    learning = load_json("learning_log.json")
    mindmap = load_json("intelligence/mindmap.json")
    nodes = mindmap["nodes"]
    node_labels = {node["id"]: node["label"] for node in nodes}
    entries = {item["day"]: item for item in learning["entries"]}
    domain_roots = {
        "Machine Learning": ("learning",),
        "Computer Vision": ("perception",),
        "Embodied AI & RL Robotics": ("policy", "systems"),
    }
    lessons_by_day: dict[int, tuple[dict[str, Any], str, str]] = {}
    related_by_day: dict[int, list[str]] = {}
    for lesson in plan["lessons"]:
        day = int(lesson["day"])
        title = f"Day {day:02d} - {safe_filename(lesson['topic'])}"
        relative = f"Curriculum/Lessons/{title}.md"
        lessons_by_day[day] = (lesson, relative, title)
        text = " ".join([lesson["topic"], *lesson.get("foundation_threads", [])])
        related_by_day[day] = related_node_ids(text, nodes, roots=domain_roots.get(lesson["domain"], ()), limit=6)

    papers_by_node: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for spec in PAPER_SPECS.values():
        for node_id in spec["nodes"]:
            papers_by_node[node_id].append((f"Papers/{spec['title']}.md", spec["title"]))

    for day, (lesson, relative, _) in lessons_by_day.items():
        record = entries.get(day)
        related_ids = related_by_day[day]
        related_concepts = [(node_paths[node_id], node_labels[node_id]) for node_id in related_ids if node_id in node_paths]
        related_papers = list(dict.fromkeys(
            paper for node_id in related_ids for paper in papers_by_node.get(node_id, [])
        ))[:6]
        previous_link = lessons_by_day.get(day - 1)
        next_link = lessons_by_day.get(day + 1)
        sequence_links = []
        if previous_link:
            sequence_links.append((previous_link[1], f"← Day {day - 1:02d}"))
        sequence_links.append(("Curriculum/Curriculum.md", "Curriculum map"))
        if next_link:
            sequence_links.append((next_link[1], f"Day {day + 1:02d} →"))
        status = record["status"] if record else lesson["status"]
        module_source = ROOT / "modules" / f"module_{day:02d}.py"
        authored_content = extract_streamlit_article(module_source) if module_source.exists() else ""
        canonical_sources = ["curriculum_plan.json"]
        if authored_content:
            canonical_sources.append(f"modules/{module_source.name}")
        lines = [
            frontmatter(
                type="curriculum-lesson", aliases=[lesson["topic"]], day=day, cycle=lesson["cycle"],
                domain=lesson["domain"], stage=lesson["stage"], status=status,
                source=canonical_sources, tags=["curriculum", lesson["domain"], lesson["stage"]],
                cssclasses=["research-note", "curriculum-note"],
                related_concepts=[path for path, _ in related_concepts],
                related_papers=[path for path, _ in related_papers],
            ),
            nav("Curriculum/Curriculum.md", "Curriculum"), "",
            f"# Day {day:02d} — {lesson['topic']}", "",
            *callout(
                "curriculum", f"{lesson['domain']} · {lesson['stage']}",
                [
                    f"**Cycle {lesson['cycle']}** · **status: {status}**",
                    lesson["content_policy"],
                ],
            ), "",
            *link_callout("Learning sequence", sequence_links, "sequence"), "",
        ]
        if related_concepts:
            lines.extend([*link_callout("Knowledge-graph concepts", related_concepts, "concepts"), ""])
        if related_papers:
            lines.extend([*link_callout("Paper companions", related_papers, "study"), ""])
        lines.extend(["## Foundation threads", "", *[f"- {item}" for item in lesson.get("foundation_threads", [])], ""])
        prerequisites = lesson.get("prerequisites", [])
        if prerequisites:
            prerequisite_links = []
            for item in prerequisites:
                if isinstance(item, int) and item in lessons_by_day:
                    prerequisite_links.append((lessons_by_day[item][1], lessons_by_day[item][2]))
                else:
                    prerequisite_links.append(("Curriculum/Curriculum.md", str(item)))
            lines.extend([*link_callout("Prerequisites", prerequisite_links, "prerequisite"), ""])
        if record:
            lines.extend([
                "## Learning record", "",
                "| Status | Confidence | Minutes | Revisit |", "|---|---|---|---|",
                f"| {record['status']} | {record.get('confidence') or 'Not recorded'} | {record.get('minutes_spent') or 'Not recorded'} | {'Yes' if record.get('revisit', False) else 'No'} |", "",
            ])
            if record.get("notes"):
                lines.extend([record["notes"], ""])
        if day == state["current_day"]:
            lines.extend([*callout(
                "current", "Current due lesson",
                ["Generate or deepen this lesson just in time rather than pre-authoring future modules."],
            ), ""])
        if authored_content:
            lines.extend([
                "---", "",
                *callout(
                    "lesson", "Authored technical lesson",
                    [
                        "The complete static chapter is exported from the canonical Streamlit module.",
                        "Interactive plots and controls remain available in the research-lab application.",
                    ],
                ), "",
                authored_content, "",
            ])
        write(relative, "\n".join(lines))

    domains = plan["policy"]["rotation"]
    by_cycle: dict[Any, dict[str, tuple[str, str]]] = defaultdict(dict)
    for lesson, relative, title in lessons_by_day.values():
        by_cycle[lesson["cycle"]][lesson["domain"]] = (relative, title)
    current = lessons_by_day[state["current_day"]]
    overview = [
        frontmatter(
            type="map-of-content", aliases=["AI Research Curriculum"], tags=["moc", "curriculum"],
            updated=plan["updated_on"], cssclasses=["research-note", "hub-note", "curriculum-hub"],
        ),
        nav("Curriculum/Curriculum.md", "Curriculum"), "",
        "# AI Research Curriculum", "",
        *callout(
            "curriculum", "A perpetual ML → CV → Embodied AI spiral",
            [
                plan["policy"]["coverage"], "",
                f"**Current:** {wiki(current[1], current[2])} · **{len(plan['lessons'])} mapped lessons** · no terminal day",
            ],
        ), "",
        "## Roadmap", "",
        f"| Cycle | {domains[0]} | {domains[1]} | {domains[2]} |",
        "|---:|---|---|---|",
    ]
    for cycle in sorted(by_cycle):
        cells = [wiki(*by_cycle[cycle][domain]) if domain in by_cycle[cycle] else "—" for domain in domains]
        overview.append(f"| {cycle} | {' | '.join(cells)} |")
    overview.extend([
        "", *callout(
            "method", "Rolling-horizon policy",
            [plan["horizon_policy"]["extension_rule"], plan["policy"]["frontier_refresh"], plan["policy"]["archive"]],
        ),
    ])
    write("Curriculum/Curriculum.md", "\n".join(overview))


def build_reports(node_paths: dict[str, str], org_paths: dict[str, str]) -> None:
    source_dir = ROOT / "intelligence" / "reports"
    reports = sorted(source_dir.glob("*.md"), reverse=True)
    mindmap = load_json("intelligence/mindmap.json")
    nodes = mindmap["nodes"]
    node_labels = {node["id"]: node["label"] for node in nodes}
    entities = load_json("intelligence/entities.json")
    ecosystem = load_json("intelligence/ecosystem.json")
    organization_names = {item["id"]: item["name"] for item in entities["organizations"]}
    organization_names.update({item["company_id"]: item["name"] for item in ecosystem["companies"]})
    paper_by_node: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for spec in PAPER_SPECS.values():
        for node_id in spec["nodes"]:
            paper_by_node[node_id].append((f"Papers/{spec['title']}.md", spec["title"]))

    links = []
    for index, source in enumerate(reports):
        title = source.stem
        relative = f"Reports/{title}.md"
        links.append((relative, title))
        body = source.read_text(encoding="utf-8").strip()
        related_ids = related_node_ids(body, nodes, limit=10)
        related_concepts = [(node_paths[node_id], node_labels[node_id]) for node_id in related_ids if node_id in node_paths]
        body_lower = body.lower()
        related_orgs = [
            (org_paths[org_id], name)
            for org_id, name in sorted(organization_names.items(), key=lambda item: item[1])
            if org_id in org_paths and name.lower() in body_lower
        ]
        related_papers = list(dict.fromkeys(
            paper for node_id in related_ids for paper in paper_by_node.get(node_id, [])
        ))
        first_line, separator, remainder = body.partition("\n")
        heading = first_line if first_line.startswith("# ") else f"# Intelligence Report — {title}"
        report_body = remainder if separator and first_line.startswith("# ") else body
        sequence = []
        if index + 1 < len(reports):
            sequence.append((f"Reports/{reports[index + 1].stem}.md", "← Older"))
        sequence.append(("Reports/Daily Reports.md", "Report archive"))
        if index > 0:
            sequence.append((f"Reports/{reports[index - 1].stem}.md", "Newer →"))
        note = [
            frontmatter(
                type="intelligence-report", report_date=title, source=f"intelligence/reports/{source.name}",
                tags=["report", "robotics-intelligence"], cssclasses=["research-note", "report-note"],
                related_concepts=[path for path, _ in related_concepts],
                related_organizations=[path for path, _ in related_orgs],
            ),
            nav("Reports/Daily Reports.md", "Daily Reports"), "", heading, "",
            *callout(
                "report", f"Source-led intelligence · {title}",
                [f"**{len(related_orgs)} organizations** · **{len(related_concepts)} concepts** connected to the wider vault"],
            ), "",
            *link_callout("Report sequence", sequence, "sequence"), "",
        ]
        if related_orgs:
            note.extend([*link_callout("Organizations in this report", related_orgs, "organizations"), ""])
        if related_concepts:
            note.extend([*link_callout("Research concepts", related_concepts, "concepts"), ""])
        if related_papers:
            note.extend([*link_callout("Paper companions", related_papers, "study"), ""])
        note.extend(["---", "", report_body])
        write(relative, "\n".join(note))
    index_note = [
        frontmatter(
            type="map-of-content", aliases=["Daily Intelligence Reports"], tags=["moc", "reports"],
            cssclasses=["research-note", "hub-note", "reports-hub"],
        ),
        nav("Reports/Daily Reports.md", "Daily Reports"), "",
        "# Daily Intelligence Reports", "",
        *callout(
            "report", "Dated evidence, including quiet days",
            ["Source-led observations. No-change days remain explicit rather than being filled with speculation.", "", f"**{len(links)} archived reports**"],
        ), "",
        *link_callout("Report archive", links, "reports"),
    ]
    write("Reports/Daily Reports.md", "\n".join(index_note))


def build_lectures() -> None:
    hub = [
        frontmatter(
            type="map-of-content", aliases=["Lecture Notes"], tags=["moc", "lectures"],
            cssclasses=["research-note", "hub-note", "lecture-hub"],
        ),
        nav("Lectures/Lecture Notes.md", "Lectures"), "",
        "# Lecture Notes", "",
        *callout(
            "lecture", "Capture → transcribe → distill → connect",
            [
                "Record the lecture locally, preserve the raw transcript, then turn only durable ideas into linked concept notes.",
                "", "The graph is built from deliberate links—not from auto-linking every word in a transcript.",
            ],
        ), "",
        *link_callout(
            "Lecture workspace",
            [("Lectures/Courses.md", "Courses"), ("Lectures/Concepts.md", "Lecture concepts"), ("_Templates/Lecture Note.md", "Lecture-note template"), ("_Templates/Lecture Concept.md", "Concept template")],
            "map",
        ), "",
        "## Capture workflow", "",
        "1. Run **Templater: Create new note from template** and choose **Lecture Note**.",
        "2. Fill the course, module, lecturer, and status properties.",
        "3. Start **Voice Scribe: Record voice note**. Keep the audio embed and transcript in the lecture note.",
        "4. During class, write only cues, equations, diagrams, and questions under **Live notes**.",
        "5. After class, distill the mechanism and worked examples; create atomic concept notes only for reusable ideas.",
        "6. Link each concept back to its source lecture, related concepts, papers, and curriculum notes.", "",
        *callout(
            "privacy", "Local transcription boundary",
            [
                "Voice Scribe runs Whisper on-device after a one-time model download. No API key is required.",
                "Do not record a lecture unless the instructor and institutional rules permit it.",
            ],
        ), "",
        "## All lecture notes", "",
        "```dataview",
        "TABLE WITHOUT ID file.link AS \"Lecture\", course AS \"Course\", module AS \"Module\", date AS \"Date\", status AS \"Status\"",
        "FROM \"Lectures/Notes\"",
        "WHERE type = \"lecture-note\"",
        "SORT date DESC",
        "```", "",
        "## Review queue", "",
        "```dataview",
        "TABLE WITHOUT ID file.link AS \"Lecture\", course AS \"Course\", status AS \"Status\"",
        "FROM \"Lectures/Notes\"",
        "WHERE type = \"lecture-note\" AND status != \"distilled\"",
        "SORT date ASC",
        "```",
    ]
    write("Lectures/Lecture Notes.md", "\n".join(hub))

    courses = [
        frontmatter(type="map-of-content", aliases=["Courses"], tags=["moc", "lectures", "courses"], cssclasses=["research-note", "hub-note", "course-hub"]),
        nav("Lectures/Lecture Notes.md", "Lectures"), "", "# Courses", "",
        *callout("lecture", "Course-level maps", ["A course hub should connect lectures in sequence and expose the concepts that recur across them."]), "",
        "```dataview",
        "TABLE WITHOUT ID rows.file.link AS \"Lectures\"",
        "FROM \"Lectures/Notes\"",
        "WHERE type = \"lecture-note\" AND course",
        "GROUP BY course",
        "SORT key ASC",
        "```", "",
        *callout("method", "Create a course hub", ["Use the **Course Hub** template, then give every lecture in that course the exact same `course` property."]),
    ]
    write("Lectures/Courses.md", "\n".join(courses))

    concepts = [
        frontmatter(type="map-of-content", aliases=["Lecture Concepts"], tags=["moc", "lectures", "concepts"], cssclasses=["research-note", "hub-note", "lecture-concepts-hub"]),
        nav("Lectures/Lecture Notes.md", "Lectures"), "", "# Lecture Concepts", "",
        *callout("concept", "Atomic, reusable understanding", ["Create a concept note when an idea has its own mechanism, equation, failure mode, or reusable explanation—not merely because a term appeared in a transcript."]), "",
        "```dataview",
        "TABLE WITHOUT ID file.link AS \"Concept\", course AS \"Course\", confidence AS \"Confidence\", source_lectures AS \"Source lectures\"",
        "FROM \"Lectures/Concepts\"",
        "WHERE type = \"lecture-concept\"",
        "SORT file.name ASC",
        "```", "",
        *callout("graph", "Build a useful local graph", ["Link each concept to one source lecture, one broader concept or course hub, and—when real—one paper, curriculum lesson, or neighboring concept."]),
    ]
    write("Lectures/Concepts.md", "\n".join(concepts))

    write_template("_Templates/Lecture Note.md", '''---
type: lecture-note
aliases: ["<% tp.file.title %>"]
date: "<% tp.date.now('YYYY-MM-DD') %>"
course: ""
module: ""
lecturer: ""
status: captured
source_audio: ""
related_concepts: []
related_papers: []
tags: [lecture]
cssclasses: [research-note, lecture-note]
---

[[Home|Research Lab]]  /  [[Lectures/Lecture Notes|Lectures]]

# <% tp.file.title %>

> [!lecture] Course · Module · Date
> Fill the properties first. Keep raw capture separate from distilled understanding.

> [!sequence] Learning sequence
> - Previous lecture:
> - [[Lectures/Lecture Notes|Lecture index]]
> - Next lecture:

## Learning objectives

-

## Live notes

> [!tip] Capture selectively
> Record equations, diagrams, examples, claims, and questions. Let Voice Scribe preserve the spoken detail.

## Core concepts and links

- Create or link atomic notes under `Lectures/Concepts/`.

## Mechanism

Explain what transforms into what, in order.

## Equations and assumptions

$$

$$

## Worked example

## Evidence and caveats

## Open questions

- [ ]

## Distilled summary

> [!summary] Five-minute reconstruction
> Write this only after processing the lecture.

## Transcript and recording

> [!recording] Raw source
> Use **Voice Scribe** here. Preserve the audio embed and transcript; do not mistake the transcript for the final note.
''')

    write_template("_Templates/Lecture Concept.md", '''---
type: lecture-concept
aliases: ["<% tp.file.title %>"]
course: ""
confidence: seed
source_lectures: []
related_concepts: []
related_papers: []
tags: [lecture-concept]
cssclasses: [research-note, lecture-concept-note]
---

[[Home|Research Lab]]  /  [[Lectures/Concepts|Lecture Concepts]]

# <% tp.file.title %>

> [!concept] One reusable idea
> State the idea precisely enough that it can stand outside the source lecture.

## Definition

## Intuition

## Mechanism

1.

## Equations and assumptions

## Worked example

## Failure modes and boundaries

## Connections

- **Broader concept:**
- **Neighboring concept:**
- **Source lecture:**
- **Paper or curriculum link:**

## Retrieval check

> [!question] Can I reconstruct it?
> Write one question whose answer requires the mechanism, not just the definition.
''')

    write_template("_Templates/Course Hub.md", '''---
type: course-hub
aliases: ["<% tp.file.title %>"]
course: "<% tp.file.title %>"
semester: ""
instructor: ""
tags: [course, lectures]
cssclasses: [research-note, hub-note, course-note]
---

[[Home|Research Lab]]  /  [[Lectures/Courses|Courses]]

# <% tp.file.title %>

> [!lecture] Course map
> Scope, sequence, recurring mechanisms, and unresolved questions.

## Course objectives

## Lecture sequence

```dataview
TABLE WITHOUT ID file.link AS "Lecture", module AS "Module", date AS "Date", status AS "Status"
FROM "Lectures/Notes"
WHERE type = "lecture-note" AND course = this.course
SORT date ASC
```

## Concept network

```dataview
TABLE WITHOUT ID file.link AS "Concept", confidence AS "Confidence", source_lectures AS "Sources"
FROM "Lectures/Concepts"
WHERE type = "lecture-concept" AND course = this.course
SORT file.name ASC
```

## Recurring mechanisms

## Open questions
''')


def build_home() -> None:
    surfaces = [
        ("Mind Map/Embodied AI.md", "Embodied AI Knowledge Graph"),
        ("Papers/Paper Guides.md", "Paper Reading Guides"),
        ("Curriculum/Curriculum.md", "Research Curriculum"),
        ("Robotics Intelligence/Robotics Intelligence.md", "Robotics Intelligence"),
        ("Contacts/Contacts.md", "Research Contacts"),
        ("Organizations/Organizations.md", "Organizations"),
        ("Reports/Daily Reports.md", "Daily Intelligence Reports"),
        ("Lectures/Lecture Notes.md", "Lecture Notes & Knowledge Graphs"),
    ]
    home = [
        frontmatter(
            type="home", aliases=["AI Research Lab"], tags=["home", "moc"],
            cssclasses=["research-note", "hub-note", "home-note"],
        ),
        "# AI Research Lab", "",
        *callout(
            "home", "One research system, several evidence layers",
            [
                "Concepts explain the field; papers explain mechanisms; curriculum schedules learning; people and organizations provide provenance; reports track change.",
                "", "Every surface remains distinct, but meaningful links connect them in the native Obsidian graph.",
            ],
        ), "",
        *link_callout("Research surfaces", surfaces, "map"), "",
        "## How the vault connects", "",
        "| From | Follow links to | Why |", "|---|---|---|",
        "| Concepts | Papers, curriculum, people, organizations | Move from an idea to evidence and study |",
        "| Papers | Concepts and curriculum | Place mechanisms inside the wider field |",
        "| Curriculum | Concepts, papers, prerequisites, adjacent days | Learn in sequence without losing context |",
        "| Organizations | Concepts, people, jobs, reports | Separate institutions while retaining provenance |",
        "| Reports | Organizations, concepts, papers, dated neighbors | Turn daily observations into cumulative knowledge |",
        "| Lectures | Course hubs, atomic concepts, papers, curriculum | Convert captured speech into durable understanding |", "",
        *callout(
            "graph", "Navigate with native Graph View",
            [
                "Open **Graph View** for the complete system. Colors separate research surfaces.",
                "Open a note's **Local Graph** at depth one or two for a readable neighborhood.",
            ],
        ), "",
        *callout(
            "palette", "Graph cluster key",
            [
                f"🔵 {wiki('Mind Map/Embodied AI.md', 'Concepts')} · 🟠 {wiki('Papers/Paper Guides.md', 'Papers')} · 🟢 {wiki('Curriculum/Curriculum.md', 'Curriculum')}",
                f"🩷 {wiki('Contacts/Contacts.md', 'People')} · 🟡 {wiki('Organizations/Organizations.md', 'Organizations')} · 🔴 {wiki('Reports/Daily Reports.md', 'Reports')}",
                f"🟣 {wiki('Lectures/Lecture Notes.md', 'Lectures')} · 🩵 {wiki('Robotics Intelligence/Robotics Intelligence.md', 'Robotics intelligence')}",
                "Cross-cluster edges stay visible: they are the evidence, provenance, and study paths joining these areas.",
            ],
        ), "",
        *callout(
            "source", "Canonical-source rule",
            ["The vault is generated from repository JSON, HTML, and Markdown. Edit canonical sources, then run `python scripts/build_obsidian_vault.py`."],
        ), "",
        *callout(
            "privacy", "Public/private boundary",
            ["Contacts are verified public provenance, not a CRM. Private career preparation, outreach, and follow-up remain outside this repository."],
        ),
    ]
    write("Home.md", "\n".join(home))
    readme = f"""# Obsidian research vault

Open this **`obsidian/` directory** as an Obsidian vault. Start at `Home.md`.

## Install the reading tools

The vault uses a compatibility-pinned Minimal theme and a deliberately small plugin stack:

- **Style Settings + Minimal Theme Settings + Homepage** — editorial presentation and a stable landing page
- **Dataview + Omnisearch + Advanced Tables** — structured indexes, retrieval, and comfortable Markdown authoring
- **Templater + Voice Scribe** — lecture templates and local, on-device Whisper transcription

```bash
python scripts/install_obsidian_reading_tools.py
```

Third-party theme/plugin code is installed locally under `.obsidian/` and ignored by Git. The tracked configuration enables the plugins and opens `Home.md` in Reading View. Release assets are version-pinned and checksum-verified by the installer.

## Lecture capture

Start at `Lectures/Lecture Notes.md`. Templater is preconfigured to use `_Templates/`; Voice Scribe downloads its Whisper model on first use and then transcribes locally. Use the lecture template for capture, the concept template for reusable ideas, and deliberate wikilinks to build the graph. Recording permission remains the user's responsibility.

## Rebuild

```bash
python scripts/build_obsidian_vault.py
```

Canonical sources remain outside the vault:

- `intelligence/mindmap.json` — concepts and semantic edges
- `intelligence/entities.json` — verified public people and organizations
- `intelligence/ecosystem.json` and `jobs.json` — dated robotics observations
- `site/papers-*.html` — canonical full paper guides
- `curriculum_plan.json`, `curriculum_state.json`, `learning_log.json` — roadmap and study state
- `intelligence/reports/*.md` — dated reports

Generated Markdown files carry `generated_by: {GENERATOR}`. The builder only removes files carrying that marker, so ordinary hand-written notes placed in the vault are preserved. The concept network uses Obsidian's native Graph View rather than a separately maintained Canvas. Do not hand-edit generated notes because the next build will replace them.

## Privacy boundary

This repository is public. The Contacts area contains only verified public provenance from `entities.json`. Never add rankings, contact history, outreach drafts, readiness notes, or follow-up plans here.
"""
    write("README.md", frontmatter(type="documentation", tags=["obsidian", "maintenance"], cssclasses=["research-note", "documentation-note"]) + readme)


def validate_vault() -> dict[str, int]:
    markdown_files = list(VAULT.rglob("*.md"))
    known = {path.relative_to(VAULT).with_suffix("").as_posix() for path in markdown_files}
    missing: list[tuple[str, str]] = []
    for path in markdown_files:
        text = path.read_text(encoding="utf-8")
        for target in WIKILINK_RE.findall(text):
            normalized = target.replace("\\", "/").strip().removesuffix(".md")
            if normalized not in known:
                missing.append((path.relative_to(VAULT).as_posix(), normalized))
    if missing:
        preview = "\n".join(f"{source} -> {target}" for source, target in missing[:20])
        raise ValueError(f"Unresolved Obsidian links ({len(missing)}):\n{preview}")
    canvas_path = VAULT / "Mind Map/Embodied AI.canvas"
    if canvas_path.exists():
        raise ValueError("The generated Canvas should be absent; use native Obsidian Graph View")
    mindmap = load_json("intelligence/mindmap.json")
    node_files = list((VAULT / "Mind Map/Nodes").glob("*.md"))
    graph_links = sum(len(WIKILINK_RE.findall(path.read_text(encoding="utf-8"))) for path in node_files)
    return {
        "markdown_notes": len(markdown_files),
        "mindmap_notes": len(node_files),
        "graph_links": graph_links,
        "semantic_edges": len(mindmap["edges"]),
        "paper_guides": len(list((VAULT / "Papers").glob("*.md"))) - 1,
        "contact_notes": len(list((VAULT / "Contacts").glob("*.md"))) - 1,
        "organization_notes": len(list((VAULT / "Organizations").glob("*.md"))) - 1,
        "curriculum_lessons": len(list((VAULT / "Curriculum/Lessons").glob("*.md"))),
        "reports": len(list((VAULT / "Reports").glob("20*.md"))),
    }


def build() -> dict[str, int]:
    VAULT.mkdir(parents=True, exist_ok=True)
    clean_generated_files()
    build_settings()
    node_paths = build_mindmap()
    build_papers(node_paths)
    _, org_paths = build_contacts(node_paths)
    build_robotics_intelligence(org_paths)
    build_curriculum(node_paths)
    build_reports(node_paths, org_paths)
    build_lectures()
    build_home()
    return validate_vault()


if __name__ == "__main__":
    counts = build()
    summary = ", ".join(f"{key}={value}" for key, value in counts.items())
    print(f"Obsidian vault built and verified: {summary}")
