# Living embodied-AI mind map

Canonical data: `intelligence/mindmap.json`  
Live page: `site/mindmap.html` → https://chippy1520.github.io/ai-research-lab/mindmap.html  
Renderer: **Mind Elixir** (real mind-map tree: hub → domain branches → notes). Canonical data is still `intelligence/mindmap.json`; convert to a tree, do not show a force hairball.  
Build copies the JSON into `site/data/mindmap.json`.

## What it is

A single evolving graph of **concepts**, not a second paper-guide index. Hub = Embodied AI. Rings = perception, learning, policies/VLA, systems, labs. Click a node for a brief, why it is on the map, neighbors, primary resources, research directions, and (for labs) official jobs/internships from `intelligence/jobs.json`.

Paper ASCII trees (ACT chunks, SmolVLA flow, …) are local footnotes. This map is the whole field.

## Rules for daily updates

The graph is **living**. Prefer upgrading an existing node over adding a sibling.

- Direction: embodied AI, RL, CV, ML/DL, robot learning frameworks, VLAs, one-shot/in-context physical prompting, sim-to-real. Hardware/materials only if they change the learning problem.
- **Keep fundamentals.** Nodes with `domain: foundations` keep their id and meaning. You may add a newer lecture/resource; never rename, split, or delete them.
- **No redundancy.** Before adding a node, search ids, labels, and briefs for the same idea (Helix 02 → `helix`, GR00T N1.6 → `gr00t`, π₀.5 → `pi0`, a new flow-matching paper → `flow-matching`). If it matches, patch that node.
- Never delete a node. Deprecate with `"status": "superseded"` if needed.
- At most 3 **new** nodes per day unless a landmark (CVPR best paper, GEN-1.x, new π-family, new LeRobot policy). Unlimited in-place upgrades.
- First-party company numbers stay labeled first-party (GEN-1.5, Skild S1).
- New lab nodes must have a `company_id` matching `ecosystem.json` when the company is on the intel desk, so jobs attach.
- Videos must **cover the node**. Hub/domain/foundations get overview lectures. Edge papers get that paper’s talk or official demo. If you have not confirmed the recording, omit the video — a paper URL is better than a title-matched lecture.
- Append a `changelog` line with the date.
- After editing, run `python scripts/build_robotics_site.py` so Pages payload includes the graph. Commit + push `main` if the graph actually changed.

## Colors mean kind, not topic

- dark — hub (the field)
- green — domain (a branch)
- lilac — concept (an idea)
- gold — method (an algorithm you implement)
- blue — paper (one publication)
- terracotta — framework (code you run)
- grey — lab (company; jobs attach)

Do not recode colors for “importance.” Filter chips are domains; fill is kind.

`id, label, kind (hub|domain|concept|method|paper|framework|lab), domain, brief, why?, research_directions[], resources[{type,title,url}], company_id?`

Edges: `{from, to, rel}`.
