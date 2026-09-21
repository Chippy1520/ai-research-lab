---
generated_by: "build_obsidian_vault.py"
type: "documentation"
tags: ["obsidian", "maintenance"]
cssclasses: ["research-note", "documentation-note"]
---
# Obsidian research vault

Open this **`obsidian/` directory** as an Obsidian vault. Start at `Home.md`.

## Install the reading tools

The vault uses the free Minimal theme, a native CSS snippet, and exactly one free/open-source community plugin:

- **QuickAdd** — creates routed concept, paper, and lecture notes from ordinary Markdown templates.

Everything else is built into Obsidian: Search, Bases, Graph, Canvas, Properties, Bookmarks, backlinks, and Local Graph.

```bash
python scripts/install_obsidian_reading_tools.py
```

Third-party theme/plugin code is installed locally under `.obsidian/` and ignored by Git. Release assets are version-pinned and checksum-verified by the installer. The installer also removes the retired plugin directories from the older, redundant stack.

## Daily workflow

1. Open `Home.md` or `Research Dashboard.canvas`.
2. Add research with `QuickAdd: New concept`, `QuickAdd: New paper`, or `QuickAdd: New lecture`.
3. Browse structured records in `Library/Research Library.base`.
4. Retrieve everything with native Search (`Ctrl+Shift+F`). Useful operators include `path:`, `tag:`, `[property:value]`, quoted phrases, and `task-todo:`.
5. Use Local Graph for one note's neighborhood and global Graph for the full linked system.

`Research Dashboard.canvas` keeps the eight domains in fixed positions. Native Graph is force-directed: path colors and hub links create coherent clusters, but Canvas is the stable map when coordinates must not drift.

## Templates and capture

QuickAdd reads `_Templates/` directly. The main commands route new notes to `Mind Map/Notes/`, `Papers/Notes/`, and `Lectures/Notes/`. Every template links to its domain hub so new notes join the correct graph cluster immediately.

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

Generated Markdown, Base, and Canvas files carry a generator marker. The builder only removes files carrying that marker, so ordinary hand-written notes are preserved. Do not hand-edit generated files because the next build will replace them.

## Privacy boundary

This repository is public. The Contacts area contains only verified public provenance from `entities.json`. Never add rankings, contact history, outreach drafts, readiness notes, or follow-up plans here.
