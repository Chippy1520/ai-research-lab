# Adding a paper reading guide

Canonical playbook for every new companion in this repo. Copy `site/papers-_template.html`, do not invent a new layout. Live index: `site/papers.html`.

Pedagogy source (do not host that paper here): CLIP-Meets-DINO-NoLA slides 6–11 — a real human case study first, then each numbered step mapped onto the method before jargon. Visual graphs, compare panes, architecture diagrams, and embedded lectures carry the argument; text-only stubs fail.

## Never

- Do not add CLIP-Meets-DINO / NoLA (separate project).
- Do not add FaultAdapt / faultadapt-gym.
- Do not link personal explainer repos. Embed the guide. Cite only primary sources (arXiv, official code, official blog/docs, named lectures).
- Do not fetch Markdown at runtime. GitHub Pages serves `site/`. The HTML file is the page.
- Do not stuff four papers into one `papers.html`. Hub cards stay short; each paper is `site/papers-<slug>.html`.
- Do not skip the human case study or the PDF-order walkthrough.

## Files to create or touch

| Path | Action |
| --- | --- |
| `site/papers-<slug>.html` | Copy from `site/papers-_template.html`. This is the live guide. |
| `site/papers.html` | Add one card (`tone-a`…`tone-d` cycle). Bump the Papers count. |
| `papers/<slug>.md` | Short notes + arXiv id. Not served. |
| `papers/README.md` | Add a table row. |
| `README.md` | Add a live-guide row under Paper Reading Guides. |

Reuse `site/assets/papers.css` + `curriculum.css`. Do not add a new stylesheet unless a visual primitive is missing.

## Research before writing

1. Open the PDF (ar5iv HTML is fine for quoting structure).
2. Extract every `#` / `##` / `###` heading, figure captions, and table numbers.
3. Pull the actual numbers you will quote (success rates, FLOPs, ablations). Do not paraphrase a table you did not read.
4. Find 2–4 primary lecture videos for *fundamentals* (transformers, SfM, VAE, flow matching, …), not recaps of this paper. Embed `youtube.com/embed/<id>`.
5. Official code + weights + blog if the authors published them.
6. Embed the paper’s own figures from `https://arxiv.org/html/<id>/<id>v1/...` and caption what to look at. Do not redraw a figure the PDF already has.
7. Knowledge graph is a **spoke-map**: claim in the center, foundations on the left, this-paper modules on the right. ASCII is a footnote, not the graph.

## Page order (fixed)

Keep this TOC, then add paper-specific items after `#walk`.

1. **Human case study** (`#case`) — concrete physical task, 4–6 steps. Left column: what a person does. Right column: the module that implements it. End with a one-sentence punch.
2. **The paper, in order** (`#walk`) — abstract paragraph by paragraph, then every numbered section, every important figure/table, then “what the paper does not claim.” Reader should be able to hold the PDF next to this and not get lost.
3. **Engineering tension** — why the paper exists, not a definition.
4. **Prerequisites** — only what this paper actually needs, with a lecture embed where a fundamental is assumed.
5. **Knowledge graph** — ASCII `knowledge-graph` *and* colored `graph-stack` nodes. Arrows are dependencies this paper uses.
6. **Architecture diagram** — `arch` / `arch-box` tones, not a wall of prose.
7. **Compare panes** — red “before / naive” vs green “this paper” for the core contrast.
8. **Paper-specific mechanics** — losses, algorithms, data hygiene, inference stack.
9. **Results, honestly** — quote the table, name the protocol (seeds, partial credit, GT cameras or not). Schematic bars are labelled schematic.
10. **Worked intuition** — one numerical or tensor-shape example.
11. **Caveats**
12. **Study plan** — 60–90 min route.
13. **Primary sources + BibTeX**

## Visual vocabulary (already in `papers.css`)

- `case-study` / `case-step` / `.human` / `.model`
- `figure-block` + `arch` + `arch-box tone-leaf|sky|gold|rose|lilac|ink`
- `kg-visual` + `graph-stack` + `kg-node`
- `compare` > `.pane.bad` / `.pane.good`
- `bar-chart` / `size-row` / `drift` / `path-svg` / `timeline`
- `video-embed` > iframe.youtube `embed/<id>` + caption
- `research-note` for a single sharp warning

Add a new CSS primitive only if none of these can say it.

## Hub card copy

Two or three sentences: the human case in miniature, then the paper’s name for those steps. No abstract dump.

## Verification

```text
# HTML + local assets (required)
python -c "from html.parser import HTMLParser; ..."  # or open the file and confirm
# existing site tests (do not expect them to cover papers-*.html)
.venv/Scripts/python.exe -m pytest tests/test_static_site.py -q
```

Confirm: case study present, `#walk` present, at least one diagram, at least one compare pane, YouTube embeds for fundamentals, arXiv + official code links, no third-party explainer URLs, hub card added.

## Ship

Commit under `site/` so Pages deploy (`Deploy Robotics Intelligence to GitHub Pages`) picks it up. Push `main`. Hard-refresh `https://chippy1520.github.io/ai-research-lab/papers.html` after the action finishes.

Existing references: `site/papers-smolvla.html`, `papers-vggt.html`, `papers-act.html`, `papers-stlight.html`.
