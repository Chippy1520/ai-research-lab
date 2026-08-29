# AI Research Lab

A local, dynamically extensible Streamlit curriculum for one-hour research modules in
Machine Learning, Computer Vision, and Embodied AI/RL Robotics.

## Run

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run app.py
```

The dashboard discovers `modules/module_*.py` dynamically; `app.py` does not need a
manual edit when a compliant module is added. Each module exports `METADATA` and a
`render()` function containing article, simulator, and code tabs.

## Current module

- **Day 1 · Machine Learning:** Optimization Dynamics & AdamW
- Full curvature/stability, momentum, bias-correction, and AdamW derivations
- Interactive rotated anisotropic-quadratic optimizer laboratory
- Executable from-scratch PyTorch implementation in `experiments/adamw_reference.py`

## State semantics

`curriculum_state.json` stores the currently available day and the next domain cursor.
Future generation advances domains strictly as ML → CV → EAI → ML. State utilities in
`curriculum.py` validate input and use atomic file replacement.

## Project structure

```text
ai_research_lab/
├── app.py
├── curriculum.py
├── curriculum_state.json
├── requirements.txt
├── modules/
│   └── module_01.py
├── experiments/
│   └── adamw_reference.py
└── .streamlit/
    └── config.toml
```
