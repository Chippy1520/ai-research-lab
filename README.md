# AI Research Lab

A local Streamlit research curriculum that rotates **Machine Learning → Computer Vision →
Embodied AI & RL Robotics**. It keeps a broad roadmap while generating only the lesson
currently being studied, so frontier material is researched when it is actually needed.

## Run in VS Code

Use `Ctrl+Shift+P → Tasks: Run Task → Research Lab: Run dashboard`, or:

```powershell
.\venv\Scripts\Activate.ps1
streamlit run app.py
```

## Workspace views

- **Today** — exactly one due module; if absent, shows the `generate next` research brief.
- **Archive** — every generated article, simulator, implementation, and personal reflection.
- **Roadmap** — a rolling, open-ended spine from foundations through systems and frontier
  work. The current 72 entries are only the mapped-ahead queue, not a terminal curriculum.
  New ML→CV→EAI cycles are appended before that queue runs low. These are planned titles,
  not prewritten lessons.
- **Research log** — source provenance, research dates, corrections, and live literature feeds.
- **Robotics intel** — US humanoid/embodied-AI companies, timeline, geographic clusters,
  dated valuation observations, official job openings, skill signals, and morning briefs.

## Just-in-time workflow

1. Study the current module and save notes/confidence in Archive.
2. Mark it complete; state advances to the next domain.
3. Send **`generate next`** to Fabric/ACP.
4. The agent checks current literature, authors only that day, records sources, runs the
   experiment/tests, and leaves all future modules untouched.

## Persistent files

| File | Purpose |
|---|---|
| `curriculum_plan.json` | Open-ended prerequisite-aware lesson spine and live frontier anchors |
| `curriculum_state.json` | Current due day and strict rotation cursor |
| `learning_log.json` | Completion, time, confidence, notes, and revisit queue |
| `research_log.json` | Per-module sources, research dates, and appended corrections |
| `modules/module_XX.py` | Immutable generated lesson artifact |
| `experiments/` | Exact executable implementations displayed by modules |
| `robotics_intelligence.py` | Company map, timeline, jobs, and daily-report dashboard |
| `intelligence/` | Sourced ecosystem/jobs snapshots and dated report archive |
| `scripts/update_robotics_jobs.py` | Deterministic official Greenhouse/Lever refresh |
| `scripts/build_robotics_site.py` | Builds the data payload for the static public site |
| `site/` | Responsive GitHub Pages application and generated public data |
| `AGENTS.md` | Generation-day research, editorial, archive, and verification protocol |

## Verification

```powershell
python -m pytest -q
python scripts\update_robotics_jobs.py
python scripts\build_robotics_site.py
python experiments\adamw_reference.py
```

## Public GitHub Pages

The device-independent static dashboard is published at:

**https://chippy1520.github.io/ai-research-lab/**

It preserves company search and filtering, the founding timeline, geographic clusters,
official openings, early-career qualification excerpts, recurring hiring signals, and the
dated report archive. GitHub Actions rebuilds it on relevant pushes and at **08:00
Asia/Colombo daily** after refreshing accessible official ATS boards. The static mirror uses
the committed ecosystem and report archive; Fabric remains responsible for synthesizing new
news briefs.

## Daily US robotics intelligence

The Fabric scheduler runs at **08:00 Asia/Colombo every day**. It refreshes accessible
official ATS boards, checks the remaining official career pages, researches ecosystem
news, archives `intelligence/reports/YYYY-MM-DD.md`, and delivers a concise report to the
originating conversation. It never equates funding with valuation and does not commit or
push automatically.

The roadmap has no final day. When fewer than 18 mapped lessons remain, six new complete
ML→CV→EAI cycles are researched and appended. “Coverage” means repeated, rigorous
traversal of foundations, modern methods, systems, interdisciplinary connections,
evaluation, and changing frontiers—not pretending that evolving knowledge can be finished.
