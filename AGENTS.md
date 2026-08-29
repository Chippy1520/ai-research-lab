# AI Research Lab — Autonomous Curriculum Protocol

## Mission
Maintain a rigorous, open-ended research curriculum for Chathuka. Rotate strictly:
**Machine Learning → Computer Vision → Embodied AI & RL Robotics**. Integrate the
computer-science, mathematical, control, and systems foundations each topic genuinely
requires. Breadth is a long-horizon property; never compress the curriculum into survey
fluff or claim finite coverage of an evolving field.

## Just-in-time rule
- `curriculum_plan.json` is a prerequisite-aware map, not prewritten lesson content.
- Author exactly **one** module when the current chat receives `generate next`.
- The due day is `curriculum_state.json.current_day`; its domain must equal
  `current_domain_index` and the corresponding roadmap entry.
- Do not author later modules speculatively. Their literature and trends will stale.
- A module becomes historical after generation. Correct it by appending provenance or
  correction notes; do not silently rewrite the learner's past context.

## Perpetual rolling horizon
- There is no terminal curriculum day. The existing lesson list is only a mapped-ahead
  queue, never a completion boundary.
- Before `generate next`, calculate mapped days remaining after the current day. If fewer
  than `horizon_policy.minimum_mapped_ahead_days` remain, research and append
  `horizon_policy.extension_batch_cycles` complete ML→CV→EAI cycles.
- Append roadmap spines only—topic, stage, prerequisites, and foundation threads. Do not
  pre-author those modules.
- Choose extensions from unresolved learning-log questions, prerequisite gaps, adjacent
  computer-science foundations, maturing research areas, and generation-day literature.
- Preserve contiguous day/cycle numbers and strict domain rotation forever. Keep
  `horizon_policy.terminal_day` null.

## Generation-day deep research
Before writing any module:
1. Re-read its roadmap spine, prerequisites, and previous learning-log questions.
2. Search current literature. Prefer, in order: original papers/standards, official
   documentation or lab pages, high-quality surveys, reproducible implementations, then
   strong editorial explainers and lectures. Medium-style articles may inspire pacing or
   analogies but are not mathematical authority.
3. Verify titles, authors, dates, URLs, equations, and video IDs at the original source.
4. For modern/frontier topics, include at least one source checked on generation day and
   explain what changed recently. Distinguish established results from active hypotheses.
5. Record every used source and research date in `research_log.json`. Append later
   corrections; never erase provenance.
6. Update the roadmap only when evidence changes sequencing or coverage. Record its
   `updated_on` date and preserve strict rotation.

## Editorial and taste standard
Aim for the clarity of a strong technical magazine article and the precision of a paper:
- Open with a concrete engineering tension, not a dictionary definition.
- Use a concise lede and roadmap, then move intuition → formulation → derivation →
  implementation → failure analysis → research frontier.
- Prefer diagrams, small numerical examples, and interactive geometric explanations over
  decorative cards. Keep typography restrained, hierarchy obvious, and prose readable.
- Unroll important derivations without “it can be shown.” State assumptions and dimensions.
- Contrast methods under shared notation. Explain when a method fails and how one detects it.
- Cite claims near the relevant paragraph; include a primary-source ledger at the end.
- Do not imitate source phrasing. Synthesize independently and flag uncertainty.

## One-hour learning architecture
Design approximately: 5 min motivation/recall, 20 min theory and derivation, 15 min
interactive simulator, 15 min executable code/experiment, 5 min synthesis and research
questions. Depth may span multiple future days; do not force an oversized topic into one
module.

## Module contract
- Path: `modules/module_XX.py`, monotonic two-digit day.
- Export `METADATA` with `day`, `title`, `domain`, `duration_minutes`; export `render()`.
- Three top-level tabs: comprehensive article, interactive simulator, complete code.
- Keep real algorithms in `experiments/`; display that exact source in the code tab.
- Use full LaTeX, verified citations/video IDs, typed PEP-8 Python, validation, and
  deterministic defaults. No placeholders or invented experimental output.
- Create/update the matching entry in `learning_log.json` with status `ready`.

## Completion and archive
- Reflections, confidence, study time, notes, and revisit flags belong in
  `learning_log.json`; module files remain reusable archive artifacts.
- Advance state only after the learner marks the current module complete.
- If the next module does not exist, the dashboard must show a just-in-time generation
  brief rather than falling forward to a future module.

## Verification before completion
1. `python -W error -m compileall -q -f app.py curriculum.py modules experiments tests`
2. `python -m pytest -q`
3. Run the new module's executable experiment.
4. Exercise all dashboard views with `streamlit.testing.v1.AppTest`; assert no exceptions.
5. Start Streamlit and verify `/_stcore/health` before reporting success.

Never replace a requested working artifact with a plan or an unexecuted scaffold.
