---
generated_by: "build_obsidian_vault.py"
type: "documentation"
tags: ["obsidian", "maintenance"]
---
# Obsidian research vault

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

Generated Markdown files carry `generated_by: build_obsidian_vault.py`. The builder only removes files carrying that marker, so ordinary hand-written notes placed in the vault are preserved. The concept network uses Obsidian's native Graph View rather than a separately maintained Canvas. Do not hand-edit generated notes because the next build will replace them.

## Privacy boundary

This repository is public. The Contacts area contains only verified public provenance from `entities.json`. Never add rankings, contact history, outreach drafts, readiness notes, or follow-up plans here.
