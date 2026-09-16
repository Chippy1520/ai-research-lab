# Living embodied-AI mind map

Canonical data: `intelligence/mindmap.json`  
Live page: `site/mindmap.html` → https://chippy1520.github.io/ai-research-lab/mindmap.html  
Renderer: **skill tree** (vanilla SVG). One layer on screen: focus orb in the centre, children on a ring, breadcrumb to go up. Not Mind Elixir, not a force graph, not a starfield.  
Storage: every node has `parent` + `layer` (0 hub → 1 domain → 2 area/cluster → 3+ notes). New nodes attach under an existing **area**, never as a 20th sibling of a domain.  
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
- Videos must **cover the whole node**, not a fragment. Hub/domain/area get a full lecture **or playlist**. Edge papers get that paper’s talk or official product intro. Playlists embed as `youtube-nocookie.com/embed/videoseries?list=…`. If you have not confirmed the recording (oEmbed-200), omit the video — a paper URL is better than a title-matched clip.
- Append a `changelog` line with the date.
- After editing, run `python scripts/build_robotics_site.py` so Pages payload includes the graph. Commit + push `main` if the graph actually changed.

## Colors mean kind, not topic

- dark — hub (the field)
- green — domain (a branch)
- lilac — concept (an idea)
- olive — area (a cluster / subfield)
- gold — method (an algorithm you implement)
- blue — paper (one publication)
- terracotta — framework (code you run)
- grey — lab (company; jobs attach)

Do not recode colors for “importance.” Filter chips are domains; fill is kind.

`id, label, kind (hub|domain|area|concept|method|paper|framework|lab), domain, parent, layer, brief, why?, research_directions[], resources[{type,title,url}], company_id?`

Edges: `{from, to, rel}`.

## Public organizations and contributors / private career preparation

`intelligence/entities.json` is the public, dated provenance registry; the build exports it to `site/data/entities.json`. Its four collections are organizations, people, associations (node → organization), and contributions (node → person). Stable node IDs join it to the existing map without changing the tree layout.

- Each person, association, and contribution includes primary `sources[{url,title}]` and `verified_on`. Prefer direct researcher/project pages; never guess a LinkedIn slug.
- Separate current affiliations from publication-time affiliations. Company membership is not evidence of model authorship. Collective bylines remain collective.
- Broad concepts have multiple related examples, not a single owner. The panel exposes at most one graph hop of related work and labels it separately from direct development claims.
- Unresearched nodes say so explicitly. Initial coverage is Generalist/GEN-1.5, OpenVLA, SmolVLA and LeRobot—not a completed directory for every node.
- Public records must contain no shortlist ranking, contact history, readiness, drafts, or personal project plans. The build rejects unknown fields; this structural check does not replace reviewing free-text fields for private material.
- `#node=<id>` opens a node panel directly. Only explicit `?career=1` exposes an outbound link to a loopback-only private companion at `http://127.0.0.1:8767/#node=<id>`. The public page never fetches the local service.
- The private companion and its records live outside this repository. Never import them into the public build or commit them. No automated messages or connection requests.
- Validate with `python -m pytest tests/test_public_entities.py tests/test_static_site.py -q`, `node --check site/assets/mindmap.js`, and browser checks of the deep link, data render, missing coverage, and private-link opt-in.
