#!/usr/bin/env python3
"""Build an Obsidian knowledge vault from the research lab's canonical data.

The JSON, HTML, and Markdown files elsewhere in this repository remain the source
of truth. Generated notes carry ``generated_by: build_obsidian_vault.py`` and may
be rebuilt safely; hand-written notes without that marker are left untouched.
"""
from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable

from bs4 import BeautifulSoup, Tag
from markdownify import markdownify as html_to_markdown

ROOT = Path(__file__).resolve().parents[1]
VAULT = ROOT / "obsidian"
GENERATOR = "build_obsidian_vault.py"
LIVE_ROOT = "https://chippy1520.github.io/ai-research-lab"

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


def frontmatter(**fields: Any) -> str:
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
    normalized = content.replace("\r\n", "\n").rstrip() + "\n"
    path.write_text(normalized, encoding="utf-8")
    return path


def wiki(path: str, label: str | None = None) -> str:
    target = path[:-3] if path.endswith(".md") else path
    return f"[[{target}|{label}]]" if label else f"[[{target}]]"


def bullet_links(items: Iterable[tuple[str, str]]) -> str:
    rows = [f"- {wiki(path, label)}" for path, label in items]
    return "\n".join(rows) if rows else "- None recorded."


def markdown_link(title: str, url: str) -> str:
    return f"[{title}]({url})"


def table_cell(value: Any) -> str:
    return str(value if value is not None else "—").replace("|", "\\|").replace("\n", " ")


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
        ".obsidian/community-plugins.json": ["obsidian-style-settings", "obsidian-minimal-settings", "homepage"],
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
                {"query": "path:\"Mind Map/Nodes\"", "color": {"a": 1, "rgb": 5162853}},
                {"query": "path:Papers", "color": {"a": 1, "rgb": 3389416}},
                {"query": "path:Curriculum", "color": {"a": 1, "rgb": 13408614}},
                {"query": "path:Contacts", "color": {"a": 1, "rgb": 11043118}},
                {"query": "path:Organizations", "color": {"a": 1, "rgb": 11369038}},
                {"query": "path:Reports", "color": {"a": 1, "rgb": 9470064}},
            ],
            "collapse-display": False, "showArrow": False, "textFadeMultiplier": 0,
            "nodeSizeMultiplier": 1.15, "lineSizeMultiplier": 0.85,
            "collapse-forces": False, "centerStrength": 0.45, "repelStrength": 12,
            "linkStrength": 0.9, "linkDistance": 220, "scale": 0.75, "close": True,
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
    neighbors: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for node in nodes:
        if node.get("parent"):
            children[node["parent"]].append(node)
    for edge in data["edges"]:
        neighbors[edge["from"]].append((edge["to"], edge["rel"]))
        neighbors[edge["to"]].append((edge["from"], edge["rel"]))

    entities = load_json("intelligence/entities.json")
    orgs = {item["id"]: item for item in entities["organizations"]}
    people = {item["id"]: item for item in entities["people"]}
    associations: dict[str, list[dict[str, Any]]] = defaultdict(list)
    contributions: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in entities["associations"]:
        associations[item["node_id"]].append(item)
    for item in entities["contributions"]:
        contributions[item["node_id"]].append(item)

    paths: dict[str, str] = {}
    for node in nodes:
        paths[node["id"]] = node_path(node["id"])
        lines = [
            frontmatter(
                type="mindmap-node", aliases=[node["label"]], node_id=node["id"],
                kind=node["kind"], domain=node["domain"], layer=node["layer"],
                source="intelligence/mindmap.json", updated=data["updated"], tags=["mindmap", node["domain"], node["kind"]],
            ),
            f"# {node['label']}", "", node.get("brief", "No brief recorded."), "", "> **Why it belongs**", f"> {node.get('why', 'No rationale recorded yet.')}", "",
        ]
        parent = node.get("parent")
        if parent and parent in by_id:
            lines.extend(["## Parent", "", f"- {wiki(node_path(parent), by_id[parent]['label'])}", ""])
        child_rows = sorted(children.get(node["id"], []), key=lambda item: item["label"].lower())
        if child_rows:
            lines.extend(["## Children", "", bullet_links((node_path(c["id"]), c["label"]) for c in child_rows), ""])
        if node.get("research_directions"):
            lines.extend(["## Research directions", "", *[f"- {item}" for item in node["research_directions"]], ""])
        related = sorted(neighbors.get(node["id"], []), key=lambda item: by_id[item[0]]["label"].lower())
        if related:
            lines.extend(["## Semantic connections", ""])
            for other_id, relation in related:
                lines.append(f"- {wiki(node_path(other_id), by_id[other_id]['label'])} — {relation}")
            lines.append("")
        if associations.get(node["id"]) or contributions.get(node["id"]):
            lines.extend(["## Verified public provenance", ""])
            for item in associations.get(node["id"], []):
                org = orgs[item["organization_id"]]
                org_link = wiki(f"Organizations/{org['id']}.md", org["name"])
                lines.append(f"- {org_link} — {item['relationship']} _(verified {item['verified_on']})_")
            for item in contributions.get(node["id"], []):
                person = people[item["person_id"]]
                person_link = wiki(f"Contacts/{person['id']}.md", person["name"])
                lines.append(f"- {person_link} — {item['relationship']} _(verified {item['verified_on']})_")
            lines.append("")
        if node.get("resources"):
            lines.extend(["## Primary resources", ""])
            for resource in node["resources"]:
                url = resource["url"]
                if not url.startswith(("http://", "https://")):
                    url = f"{LIVE_ROOT}/{url.lstrip('/')}"
                lines.append(f"- **{resource['type'].title()}:** {markdown_link(resource['title'], url)}")
            lines.append("")
        lines.extend(["## Source", "", f"- Canonical record: `intelligence/mindmap.json#{node['id']}`", f"- Live graph: {LIVE_ROOT}/mindmap.html#node={node['id']}"])
        write(paths[node["id"]], "\n".join(lines))

    domains = sorted((n for n in nodes if n["layer"] == 1), key=lambda item: item["label"])
    overview = [
        frontmatter(type="map-of-content", aliases=["Embodied AI Mind Map", "Embodied AI Knowledge Graph"], tags=["moc", "mindmap"], source="intelligence/mindmap.json"),
        "# Embodied AI Knowledge Graph", "", data["scope"], "",
        f"> [!abstract] Native graph", f"> **{len(nodes)} concepts** · **{len(data['edges'])} semantic relationships** · canonical data updated **{data['updated']}**", ">", "> Open **Graph View** from the left ribbon or command palette. Select any concept and use its local graph for a focused neighborhood.", "",
        "## Branches", "", bullet_links((node_path(n["id"]), n["label"]) for n in domains), "",
        "## How to read it", "",
        "- Solid note links encode parent and child hierarchy.",
        "- Each concept note lists selected semantic cross-links, people, organizations, and primary sources.",
        "- Global Graph View shows the whole research system; Local Graph shows the neighborhood of the current note.",
        "- Colors are assigned by research surface in `.obsidian/graph.json`.",
        "- Canonical concepts remain in `intelligence/mindmap.json`; rebuild after source changes.", "",
        "## Recent evolution", "",
    ]
    for item in reversed(data.get("changelog", [])[-10:]):
        overview.append(f"- **{item['date']}** — {item['note']}")
    write("Mind Map/Embodied AI.md", "\n".join(overview))
    return paths


def prepare_article(article: Tag, paper_file_map: dict[str, str]) -> str:
    clone = BeautifulSoup(str(article), "html.parser")
    for iframe in clone.find_all("iframe"):
        src = iframe.get("src", "")
        title = iframe.get("title", "Video")
        iframe.replace_with(clone.new_tag("p"))
        replacement = clone.find_all("p")[-1]
        replacement.string = f"Video: {title} — {src}"
    for anchor in clone.find_all("a"):
        href = anchor.get("href", "")
        file_name = href.split("#", 1)[0]
        if file_name in paper_file_map:
            label = anchor.get_text(" ", strip=True) or PAPER_SPECS[paper_file_map[file_name]]["title"]
            anchor.replace_with(f"[[Papers/{PAPER_SPECS[paper_file_map[file_name]]['title']}|{label}]]")
        elif href and not href.startswith(("http://", "https://", "#")):
            anchor["href"] = f"{LIVE_ROOT}/{href.lstrip('/')}"
    markdown = html_to_markdown(str(clone), heading_style="ATX", bullets="-", strip=["article", "div", "span"])
    markdown = re.sub(r"[ \t]+\n", "\n", markdown)
    markdown = re.sub(r"\n{3,}", "\n\n", markdown)
    markdown = markdown.replace("\\[", "$$\n").replace("\\]", "\n$$")
    return markdown.strip()


def build_papers(node_paths: dict[str, str]) -> dict[str, str]:
    paper_file_map = {f"papers-{slug}.html": slug for slug in PAPER_SPECS}
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
        aliases = [title]
        if display_title != title:
            aliases.append(display_title)
        related_nodes = [node_id for node_id in spec["nodes"] if node_id in node_paths]
        lines = [
            frontmatter(
                type="paper-guide", aliases=aliases, paper_slug=slug, source=f"site/papers-{slug}.html",
                live_url=f"{LIVE_ROOT}/papers-{slug}.html", tags=["paper", "reading-guide"],
                related_nodes=related_nodes,
            ),
            f"# {display_title}", "",
        ]
        if description and description.get("content"):
            lines.extend([f"> {description['content']}", ""])
        lines.extend([
            f"- **Canonical guide:** `site/papers-{slug}.html`",
            f"- **Live guide:** {LIVE_ROOT}/papers-{slug}.html",
            f"- **Companion source:** `papers/{spec['source']}`", "",
            "## Connected concepts", "",
            bullet_links((node_paths[node_id], node_id) for node_id in related_nodes), "",
            "---", "", prepare_article(article, paper_file_map),
        ])
        relative = f"Papers/{title}.md"
        output_paths[slug] = relative
        write(relative, "\n".join(lines))
    index = [
        frontmatter(type="map-of-content", aliases=["Paper Reading Guides"], tags=["moc", "papers"]),
        "# Paper Reading Guides", "",
        "Self-contained Obsidian companions generated from the canonical editorial HTML guides.", "",
        f"> {len(output_paths)} guides. CLIP-Meets-DINO and FaultAdapt remain intentionally excluded.", "",
        "## Guides", "", bullet_links((path, PAPER_SPECS[slug]["title"]) for slug, path in output_paths.items()), "",
        "## Editorial protocol", "",
        "- Human case study first.", "- Walk through the PDF in order.", "- Name the model mechanism precisely.",
        "- Keep results tied to their evaluation protocol.", "- Use primary sources; distinguish established results from active hypotheses.", "",
        f"Public hub: {LIVE_ROOT}/papers.html",
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

    for person_id, person in people.items():
        lines = [
            frontmatter(
                type="public-contact", aliases=[person["name"]], contact_id=person_id,
                organization_id=person.get("organization_id"), verified_on=person["verified_on"],
                source="intelligence/entities.json", tags=["contact", "public-record"],
            ),
            f"# {person['name']}", "", person["role"], "",
        ]
        org_id = person.get("organization_id")
        if org_id and org_id in organizations:
            lines.extend(["## Current public affiliation", "", f"- {wiki(org_paths[org_id], organizations[org_id]['name'])}", ""])
        lines.extend(["## Public profiles", "", f"- {markdown_link('Research profile', person['profile_url'])}"])
        if person.get("linkedin_url"):
            lines.append(f"- {markdown_link('Verified LinkedIn', person['linkedin_url'])}")
        lines.append("")
        if contrib_by_person.get(person_id):
            lines.extend(["## Verified contributions", ""])
            for item in contrib_by_person[person_id]:
                if item["node_id"] in node_paths:
                    lines.append(f"- {wiki(node_paths[item['node_id']], item['node_id'])} — {item['relationship']} _(verified {item['verified_on']})_")
            lines.append("")
        lines.extend(["## Source ledger", ""])
        for source in person["sources"]:
            lines.append(f"- {markdown_link(source['title'], source['url'])}")
        lines.extend(["", "> [!privacy]", "> Public provenance only. No outreach ranking, contact history, private notes, or message drafts belong in this repository."])
        write(person_paths[person_id], "\n".join(lines))

    for org_id, org in organizations.items():
        company = ecosystem_orgs.get(org_id)
        lines = [
            frontmatter(
                type="organization", aliases=[org["name"]], organization_id=org_id,
                organization_kind=org.get("kind", "company"), source="intelligence/entities.json" if org_id in provenance_orgs else "intelligence/ecosystem.json",
                tags=["organization", org.get("kind", "company")],
            ),
            f"# {org['name']}", "",
        ]
        if company:
            lines.extend([
                company["focus"], "", "## Ecosystem observation", "",
                f"- **Founded:** {company['founded']}", f"- **Location:** {company['hq_city']}, {company['hq_state']} · {company['cluster']}",
                f"- **Category:** {company['category']}", f"- **Stage:** {company['stage']}",
                f"- **Valuation observation:** {company['valuation_label']} ({company['valuation_type']}, {company['valuation_as_of']})",
                f"- **Careers:** {company['careers_url']}", "",
                "> [!note]", f"> {company['valuation_note']}", "",
            ])
        elif org.get("url"):
            lines.extend([f"- **Official site:** {org['url']}", ""])
        if org.get("map_node_id") in node_paths:
            lines.extend(["## Mind-map presence", "", f"- {wiki(node_paths[org['map_node_id']], org['name'])}", ""])
        if people_by_org.get(org_id):
            lines.extend(["## Verified public people", "", bullet_links((person_paths[p["id"]], p["name"]) for p in people_by_org[org_id]), ""])
        if assoc_by_org.get(org_id):
            lines.extend(["## Verified associations", ""])
            for item in assoc_by_org[org_id]:
                if item["node_id"] in node_paths:
                    lines.append(f"- {wiki(node_paths[item['node_id']], item['node_id'])} — {item['relationship']} _(verified {item['verified_on']})_")
            lines.append("")
        company_jobs = jobs_by_company.get(org["name"], [])
        if company_jobs:
            lines.extend(["## Current tracked openings", "", f"{len(company_jobs)} openings in the dated official-board snapshot.", ""])
            for opening in sorted(company_jobs, key=lambda item: item["title"])[:12]:
                lines.append(f"- {markdown_link(opening['title'], opening['url'])} — {opening['location']}")
            if len(company_jobs) > 12:
                lines.append(f"- …and {len(company_jobs) - 12} more in {wiki('Robotics Intelligence/Current Openings.md', 'Current Openings')}.")
            lines.append("")
        if company and company.get("sources"):
            lines.extend(["## Sources", ""])
            for source in company["sources"]:
                lines.append(f"- {markdown_link(source['title'], source['url'])} — {source.get('date', '')}")
        lines.extend(["", "> [!privacy]", "> Public organizational record only. Career preparation and outreach remain private and outside this repository."])
        write(org_paths[org_id], "\n".join(lines))

    contacts_index = [
        frontmatter(type="map-of-content", aliases=["Research Contacts"], tags=["moc", "contacts"], source="intelligence/entities.json"),
        "# Research Contacts", "", "Verified public researchers and contributors connected to work on the embodied-AI map.", "",
        f"> Coverage is intentionally incomplete: {len(people)} verified people as of **{entities['updated_on']}**. Absence is not evidence of non-contribution.", "",
        "## People", "", bullet_links((person_paths[p["id"]], p["name"]) for p in sorted(people.values(), key=lambda item: item["name"])), "",
        "## Boundary", "", "This public vault contains provenance, not a networking CRM. Private prioritization, outreach, and follow-up records stay outside the repository.",
    ]
    write("Contacts/Contacts.md", "\n".join(contacts_index))
    organizations_index = [
        frontmatter(type="map-of-content", aliases=["Organizations"], tags=["moc", "organizations"]),
        "# Organizations", "", "Research organizations and robotics companies represented in the public intelligence sources.", "",
        "## Directory", "", bullet_links((org_paths[org_id], organizations[org_id]["name"]) for org_id in sorted(organizations, key=lambda oid: organizations[oid]["name"])),
    ]
    write("Organizations/Organizations.md", "\n".join(organizations_index))
    return person_paths, org_paths


def build_robotics_intelligence(org_paths: dict[str, str]) -> None:
    ecosystem = load_json("intelligence/ecosystem.json")
    jobs = load_json("intelligence/jobs.json")
    companies = sorted(ecosystem["companies"], key=lambda item: item["name"])
    overview = [
        frontmatter(type="map-of-content", aliases=["Robotics Intelligence"], tags=["moc", "robotics-intelligence"], as_of=ecosystem["as_of"]),
        "# Robotics Intelligence", "", ecosystem["scope"], "", f"> Ecosystem observations as of **{ecosystem['as_of']}**; jobs last checked **{jobs['last_checked']}**.", "",
        "## Desks", "", f"- {wiki('Robotics Intelligence/Current Openings.md', 'Current Openings')}", f"- {wiki('Robotics Intelligence/Skill Signals.md', 'Recurring Skill Signals')}", f"- {wiki('Reports/Daily Reports.md', 'Dated Intelligence Reports')}", "",
        "## Companies", "", bullet_links((org_paths[c["company_id"]], c["name"]) for c in companies if c["company_id"] in org_paths), "",
        "## Methodology", "", f"> {ecosystem['funding_methodology']}", "", f"> {ecosystem['valuation_methodology']}",
    ]
    write("Robotics Intelligence/Robotics Intelligence.md", "\n".join(overview))

    openings = [
        frontmatter(type="dataset-view", aliases=["Current Robotics Openings"], tags=["jobs", "robotics-intelligence"], last_checked=jobs["last_checked"]),
        "# Current Openings", "", jobs["methodology"], "", f"> Snapshot contains **{len(jobs['openings'])}** openings; always verify the official page before acting.", "",
        "| Company | Role | Location | Seniority | Last seen |", "|---|---|---|---|---|",
    ]
    for item in sorted(jobs["openings"], key=lambda row: (row["company"], row["title"])):
        role = markdown_link(table_cell(item["title"]), item["url"])
        openings.append(f"| {table_cell(item['company'])} | {role} | {table_cell(item['location'])} | {table_cell(item['seniority'])} | {table_cell(item['last_seen'])} |")
    write("Robotics Intelligence/Current Openings.md", "\n".join(openings))

    signals = [
        frontmatter(type="dataset-view", aliases=["Robotics Skill Signals"], tags=["skills", "robotics-intelligence"], last_checked=jobs["last_checked"]),
        "# Recurring Skill Signals", "", "Repeated requirements across official boards, kept distinct from personal outreach or private planning.", "",
    ]
    for signal in jobs["requirement_signals"]:
        signals.extend([
            f"## {signal['skill']}", "", f"- **Category:** {signal['category']}",
            f"- **Evidence:** {signal['evidence']}", f"- **Portfolio response:** {signal['portfolio_response']}", "",
        ])
    write("Robotics Intelligence/Skill Signals.md", "\n".join(signals))


def build_curriculum() -> None:
    plan = load_json("curriculum_plan.json")
    state = load_json("curriculum_state.json")
    learning = load_json("learning_log.json")
    entries = {item["day"]: item for item in learning["entries"]}
    lesson_links: list[tuple[str, str]] = []
    for lesson in plan["lessons"]:
        day = int(lesson["day"])
        title = f"Day {day:02d} - {safe_filename(lesson['topic'])}"
        relative = f"Curriculum/Lessons/{title}.md"
        lesson_links.append((relative, title))
        record = entries.get(day)
        lines = [
            frontmatter(
                type="curriculum-lesson", aliases=[lesson["topic"]], day=day, cycle=lesson["cycle"],
                domain=lesson["domain"], stage=lesson["stage"], status=record["status"] if record else lesson["status"],
                source="curriculum_plan.json", tags=["curriculum", lesson["domain"], lesson["stage"]],
            ),
            f"# Day {day:02d} — {lesson['topic']}", "", f"- **Domain:** {lesson['domain']}", f"- **Cycle:** {lesson['cycle']}", f"- **Stage:** {lesson['stage']}",
            f"- **Content policy:** {lesson['content_policy']}", "", "## Foundation threads", "",
            *[f"- {item}" for item in lesson.get("foundation_threads", [])], "",
        ]
        prerequisites = lesson.get("prerequisites", [])
        if prerequisites:
            lines.extend(["## Prerequisites", "", *[f"- Day {int(item):02d}" if isinstance(item, int) else f"- {item}" for item in prerequisites], ""])
        if record:
            lines.extend(["## Learning record", "", f"- **Status:** {record['status']}", f"- **Confidence:** {record.get('confidence') or 'Not recorded'}", f"- **Minutes:** {record.get('minutes_spent') or 'Not recorded'}", f"- **Revisit:** {record.get('revisit', False)}", ""])
            if record.get("notes"):
                lines.extend([record["notes"], ""])
        if day == state["current_day"]:
            lines.extend(["> [!important]", "> This is the current due lesson. Generate or deepen it just in time rather than pre-authoring future modules."])
        write(relative, "\n".join(lines))
    by_cycle: dict[Any, list[tuple[str, str]]] = defaultdict(list)
    for lesson, link in zip(plan["lessons"], lesson_links):
        by_cycle[lesson["cycle"]].append(link)
    overview = [
        frontmatter(type="map-of-content", aliases=["AI Research Curriculum"], tags=["moc", "curriculum"], updated=plan["updated_on"]),
        "# AI Research Curriculum", "", "Machine Learning → Computer Vision → Embodied AI & RL Robotics, maintained as a perpetual rolling horizon.", "",
        f"> Current due day: **{state['current_day']}** · mapped roadmap entries: **{len(plan['lessons'])}** · terminal day: **none**.", "",
    ]
    for cycle in sorted(by_cycle):
        overview.extend([f"## Cycle {cycle}", "", bullet_links(by_cycle[cycle]), ""])
    write("Curriculum/Curriculum.md", "\n".join(overview))


def build_reports() -> None:
    source_dir = ROOT / "intelligence" / "reports"
    reports = sorted(source_dir.glob("*.md"), reverse=True)
    links = []
    for source in reports:
        title = source.stem
        relative = f"Reports/{title}.md"
        links.append((relative, title))
        body = source.read_text(encoding="utf-8")
        write(relative, frontmatter(type="intelligence-report", report_date=title, source=f"intelligence/reports/{source.name}", tags=["report", "robotics-intelligence"]) + body)
    index = [
        frontmatter(type="map-of-content", aliases=["Daily Intelligence Reports"], tags=["moc", "reports"]),
        "# Daily Intelligence Reports", "", "Dated, source-led observations. Quiet/no-change days remain explicit rather than being filled with speculation.", "",
        bullet_links(links),
    ]
    write("Reports/Daily Reports.md", "\n".join(index))


def build_home() -> None:
    home = [
        frontmatter(type="home", aliases=["AI Research Lab"], tags=["home", "moc"]),
        "# AI Research Lab", "", "A linked Obsidian workspace for the curriculum, embodied-AI concept map, paper companions, public provenance, and dated robotics intelligence.", "",
        "> [!important] Canonical sources", "> This vault is generated from the repository's JSON, HTML, and Markdown sources. Edit canonical files, then run `python scripts/build_obsidian_vault.py`.", "",
        "## Research surfaces", "",
        f"- {wiki('Mind Map/Embodied AI.md', 'Embodied AI Knowledge Graph')} — 113 concepts and their semantic relationships",
        f"- {wiki('Papers/Paper Guides.md', 'Paper Reading Guides')} — full guides converted from canonical editorial HTML",
        f"- {wiki('Curriculum/Curriculum.md', 'Research Curriculum')} — the rolling ML → CV → EAI roadmap",
        f"- {wiki('Robotics Intelligence/Robotics Intelligence.md', 'Robotics Intelligence')} — ecosystem, jobs, and repeated skill signals",
        f"- {wiki('Contacts/Contacts.md', 'Research Contacts')} — verified public contributors only",
        f"- {wiki('Organizations/Organizations.md', 'Organizations')} — labs, universities, and robotics companies",
        f"- {wiki('Reports/Daily Reports.md', 'Daily Intelligence Reports')} — archived source-led briefs", "",
        "## Navigate with Graph View", "",
        "> [!tip] Graph-first navigation", "> Open **Graph View** from the left ribbon or command palette. Colors separate concepts, papers, curriculum, people, organizations, and reports.", ">", "> For a quieter view, open a note's **Local Graph** and adjust depth to one or two hops.", "",
        "## Reading setup", "",
        "- **Minimal** provides the restrained editorial base theme.",
        "- **Minimal Theme Settings** and **Style Settings** expose typography, line width, and accent controls.",
        "- **Homepage** opens this note directly in Reading View.", "",
        "## Working rule", "", "Private career preparation and outreach do not enter this public repository. Contacts here are verified public provenance, not a CRM.",
    ]
    write("Home.md", "\n".join(home))
    readme = f"""# Obsidian research vault

Open this **`obsidian/` directory** as an Obsidian vault. Start at `Home.md`.

## Install the reading tools

The vault uses a compatibility-pinned Minimal theme plus Style Settings, Minimal Theme Settings, and Homepage:

```bash
python scripts/install_obsidian_reading_tools.py
```

Third-party theme/plugin code is installed locally under `.obsidian/` and ignored by Git. The tracked configuration enables the plugins and opens `Home.md` in Reading View.

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
    write("README.md", frontmatter(type="documentation", tags=["obsidian", "maintenance"]) + readme)


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
    build_curriculum()
    build_reports()
    build_home()
    return validate_vault()


if __name__ == "__main__":
    counts = build()
    summary = ", ".join(f"{key}={value}" for key, value in counts.items())
    print(f"Obsidian vault built and verified: {summary}")
