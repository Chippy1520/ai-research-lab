"""AI Research Lab: dynamically loaded, publication-grade daily modules."""

from __future__ import annotations

import importlib
import pkgutil
import time
from dataclasses import dataclass
from types import ModuleType
from typing import Any

import streamlit as st

from curriculum import DOMAINS, load_state

st.set_page_config(
    page_title="AI Research Lab",
    page_icon="∇",
    layout="wide",
    initial_sidebar_state="expanded",
)


@dataclass(frozen=True)
class LoadedModule:
    """Validated module metadata and imported implementation."""

    day: int
    title: str
    domain: str
    duration_minutes: int
    module: ModuleType


def discover_modules() -> list[LoadedModule]:
    """Discover ``modules.module_*`` files and validate their public contract."""
    package = importlib.import_module("modules")
    loaded: list[LoadedModule] = []
    for info in pkgutil.iter_modules(package.__path__, prefix="modules."):
        if not info.name.rsplit(".", maxsplit=1)[-1].startswith("module_"):
            continue
        implementation = importlib.import_module(info.name)
        metadata: dict[str, Any] = getattr(implementation, "METADATA", {})
        render = getattr(implementation, "render", None)
        required = {"day", "title", "domain", "duration_minutes"}
        missing = required.difference(metadata)
        if missing or not callable(render):
            raise RuntimeError(
                f"{info.name} violates the module contract; missing={sorted(missing)}"
            )
        loaded.append(
            LoadedModule(
                day=int(metadata["day"]),
                title=str(metadata["title"]),
                domain=str(metadata["domain"]),
                duration_minutes=int(metadata["duration_minutes"]),
                module=implementation,
            )
        )
    return sorted(loaded, key=lambda item: item.day)


def inject_styles() -> None:
    """Apply restrained research-dashboard styling."""
    st.markdown(
        """
        <style>
        .stApp {background: radial-gradient(circle at 85% 0%, #10233d 0%, #070b14 32%);}
        [data-testid="stSidebar"] {background: #0b1220; border-right: 1px solid #21314b;}
        .block-container {max-width: 1480px; padding-top: 2rem; padding-bottom: 5rem;}
        h1, h2, h3 {letter-spacing: -0.025em;}
        h1 {background: linear-gradient(90deg, #f8fafc, #38bdf8); -webkit-background-clip:
            text; -webkit-text-fill-color: transparent;}
        div[data-testid="stMetric"] {background: #0f172a; border: 1px solid #22324a;
            border-radius: 12px; padding: 0.65rem 1rem;}
        .research-note {border-left: 3px solid #38bdf8; background: #0d1728;
            padding: 0.9rem 1.1rem; border-radius: 0 10px 10px 0; margin: 0.7rem 0;}
        .citation {font-size: 0.92rem; color: #a9bad0;}
        code {font-size: 0.88em;}
        </style>
        """,
        unsafe_allow_html=True,
    )


@st.fragment(run_every=1.0)
def render_focus_timer(minutes: int = 60) -> None:
    """Render a non-blocking, session-persistent native Streamlit focus timer."""
    initial_seconds = minutes * 60
    if "focus_remaining" not in st.session_state:
        st.session_state.focus_remaining = float(initial_seconds)
        st.session_state.focus_running = False
        st.session_state.focus_last_tick = time.monotonic()

    now = time.monotonic()
    if st.session_state.focus_running:
        elapsed = now - st.session_state.focus_last_tick
        st.session_state.focus_remaining = max(
            0.0, st.session_state.focus_remaining - elapsed
        )
        if st.session_state.focus_remaining == 0.0:
            st.session_state.focus_running = False
    st.session_state.focus_last_tick = now

    remaining = int(round(st.session_state.focus_remaining))
    timer_color = "#4ade80" if remaining == 0 else "#e5edf7"
    st.markdown(
        f"<div style='font-size:11px;color:#8fa4bf;letter-spacing:.12em'>FOCUS BLOCK</div>"
        f"<div style='font:600 28px ui-monospace;color:{timer_color};margin:5px 0'>"
        f"{remaining // 60:02d}:{remaining % 60:02d}</div>",
        unsafe_allow_html=True,
    )
    start_column, reset_column = st.columns(2)
    if start_column.button(
        "Pause" if st.session_state.focus_running else "Start",
        key="focus_toggle",
        width="stretch",
    ):
        st.session_state.focus_running = not st.session_state.focus_running
        st.session_state.focus_last_tick = time.monotonic()
        st.rerun(scope="fragment")
    if reset_column.button("Reset", key="focus_reset", use_container_width=True):
        st.session_state.focus_remaining = float(initial_seconds)
        st.session_state.focus_running = False
        st.session_state.focus_last_tick = time.monotonic()
        st.rerun(scope="fragment")


def main() -> None:
    """Render dashboard shell and selected dynamically discovered module."""
    inject_styles()
    state = load_state()
    modules = discover_modules()
    if not modules:
        st.error("No curriculum modules were found in `modules/`.")
        st.stop()

    with st.sidebar:
        st.markdown("## ∇ AI Research Lab")
        st.caption("ML → CV → Embodied AI · strict daily rotation")
        render_focus_timer(60)
        labels = [f"Day {item.day:02d} · {item.domain} · {item.title}" for item in modules]
        selected_label = st.radio("Curriculum", labels, index=len(labels) - 1)
        selected = modules[labels.index(selected_label)]
        st.divider()
        st.metric("Current day", state.current_day)
        st.metric("Next rotation domain", DOMAINS[state.current_domain_index])
        st.caption(f"State updated: {state.last_updated}")

    st.title(f"Day {selected.day:02d} · {selected.title}")
    left, middle, right = st.columns(3)
    left.metric("Domain", selected.domain)
    middle.metric("Designed duration", f"{selected.duration_minutes} min")
    right.metric("Module count", len(modules))
    selected.module.render()


if __name__ == "__main__":
    main()
