# AI Research Lab — Agent Instructions

## Purpose
Maintain an open-ended sequence of rigorous one-hour modules rotating strictly:
Machine Learning → Computer Vision → Embodied AI & RL Robotics.

## Module contract
- Place modules at `modules/module_XX.py` with monotonic two-digit day numbers.
- Export `METADATA` with `day`, `title`, `domain`, and `duration_minutes`.
- Export a zero-argument `render()` function.
- Render exactly three top-level tabs: technical article, interactive simulator, complete code.
- Keep executable algorithms in `experiments/`; display those exact source files in code tabs.
- Use full LaTeX derivations, primary-paper citations, verified video IDs, and no placeholders.
- Use typed, validated, PEP-8 Python and deterministic simulator defaults.

## State and rotation
- Read and validate `curriculum_state.json` through `curriculum.py`.
- Update state only after a new module passes tests and imports successfully.
- Use `advance_state` so domain rotation remains strict and state writes remain atomic.

## Verification before completion
1. `python -W error -m compileall -q -f app.py curriculum.py modules experiments tests`
2. `python -m pytest -q`
3. Run the executable experiment associated with the new module.
4. Exercise `app.py` with `streamlit.testing.v1.AppTest` and assert no exceptions.
5. Start Streamlit and check `/_stcore/health` before reporting success.

Never replace a requested working artifact with a plan or unexecuted scaffold.
