# Living embodied-AI mind map

Canonical data: `intelligence/mindmap.json`  
Live page: `site/mindmap.html` → https://chippy1520.github.io/ai-research-lab/mindmap.html  
Build copies the JSON into `site/data/mindmap.json`.

## What it is

A single evolving graph of **concepts**, not a second paper-guide index. Hub = Embodied AI. Rings = perception, learning, policies/VLA, systems, labs. Click a node for a brief, why it is on the map, neighbors, primary resources, research directions, and (for labs) official jobs/internships from `intelligence/jobs.json`.

Paper ASCII trees (ACT chunks, SmolVLA flow, …) are local footnotes. This map is the whole field.

## Rules for daily updates

- Direction: embodied AI, RL, CV, ML/DL, robot learning frameworks, VLAs, one-shot/in-context physical prompting, sim-to-real. Hardware/materials only if they change the learning problem.
- Never delete a node. Deprecate with `"status": "superseded"` if needed.
- At most 5 new nodes per day unless a landmark paper (CVPR best paper, GEN-1.x, π-family, new LeRobot policy).
- First-party company numbers stay labeled first-party (GEN-1.5, Skild S1).
- New lab nodes must have a `company_id` matching `ecosystem.json` when the company is on the intel desk, so jobs attach.
- Every new node needs `brief`, `domain`, `kind`, and at least one primary `resources` URL.
- Append a `changelog` line with the date.
- After editing, run `python scripts/build_robotics_site.py` so Pages payload includes the graph. Commit + push `main` if the graph actually changed.

## Node schema

`id, label, kind (hub|domain|concept|method|paper|framework|lab), domain, brief, why?, research_directions[], resources[{type,title,url}], company_id?`

Edges: `{from, to, rel}`.
