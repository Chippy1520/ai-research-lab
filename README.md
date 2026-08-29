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
- **Roadmap** — a 72-day, 24-cycle spine from foundations through systems and frontier work.
  These are planned titles, not prewritten lessons.
- **Research log** — source provenance, research dates, corrections, and live literature feeds.

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
| `AGENTS.md` | Generation-day research, editorial, archive, and verification protocol |

## Verification

```powershell
python -m pytest -q
python experiments\adamw_reference.py
```

The roadmap is intentionally extendable. “Coverage” means repeated, rigorous traversal of
foundations, modern methods, systems, evaluation, and changing frontiers—not pretending
that all of computer science can be finished in a fixed number of days.
