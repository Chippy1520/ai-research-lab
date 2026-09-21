---
generated_by: "build_obsidian_vault.py"
type: "documentation"
tags: ["obsidian", "maintenance"]
cssclasses: ["research-note", "documentation-note"]
---
# Obsidian research vault

Open this **`obsidian/` directory** as an Obsidian vault. Start at `Home.md`.

## Install the reading tools

The vault uses a compatibility-pinned Minimal theme and a deliberately small plugin stack:

- **Style Settings + Minimal Theme Settings + Homepage** — editorial presentation and a stable landing page
- **Dataview + Omnisearch + Advanced Tables** — structured indexes, retrieval, and comfortable Markdown authoring
- **Smart Lookup + Smart Connections** — local semantic topic search followed by a graph-and-list neighborhood around the selected note
- **Callout Manager** — discover and manage the vault's native, portable callout vocabulary
- **Templater + Voice Scribe** — lecture templates and local, on-device Whisper transcription

```bash
python scripts/install_obsidian_reading_tools.py
```

Third-party theme/plugin code is installed locally under `.obsidian/` and ignored by Git. The tracked configuration enables the plugins and opens `Home.md` in Reading View. Release assets are version-pinned and checksum-verified by the installer.

## Search and semantic graph workflow

Use the tools according to the question:

1. **Exact words, paths, or tags:** run Omnisearch.
2. **An idea described in your own words:** run `Smart Lookup: Open: Lookup view`, enter a concrete query, and inspect the ranked previews.
3. **A semantic neighborhood:** open the strongest result, then run `Smart Connections: Open: Connections view`. Its default Connections component renders related notes as both a graph and a list.
4. **Explicit authored relationships:** use native Graph View or Local Graph.

Smart Connections and Smart Lookup use a built-in local embedding model by default. Initial indexing can take several minutes and may download the model once. The generated embedding cache lives in `.smart-env/` and is ignored by Git.

The optional paid **Smart Graph** companion provides a direct typed-query-to-semantic-map workflow. It is deliberately not bundled: the free local workflow above reaches the graph by opening one inspected search result first, and no subscription should be assumed silently.

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

Generated Markdown files carry `generated_by: build_obsidian_vault.py`. The builder only removes files carrying that marker, so ordinary hand-written notes placed in the vault are preserved. The concept network uses Obsidian's native Graph View rather than a separately maintained Canvas. Do not hand-edit generated notes because the next build will replace them.

## Privacy boundary

This repository is public. The Contacts area contains only verified public provenance from `entities.json`. Never add rankings, contact history, outreach drafts, readiness notes, or follow-up plans here.
