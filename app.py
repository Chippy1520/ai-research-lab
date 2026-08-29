"""AI Research Lab — just-in-time lessons, archive, roadmap, and provenance."""

from __future__ import annotations

import importlib
import pkgutil
import re
import time
from dataclasses import dataclass
from types import ModuleType
from typing import Any

import streamlit as st

from curriculum import (
    DOMAINS,
    PlannedLesson,
    advance_state,
    lesson_for_day,
    load_learning_log,
    load_plan,
    load_research_log,
    load_state,
    save_learning_reflection,
    save_state,
)

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

    @property
    def slug(self) -> str:
        """Return the stable archive identifier."""
        return f"module_{self.day:02d}"


def discover_modules() -> list[LoadedModule]:
    """Discover only canonical ``modules.module_XX`` files."""
    package = importlib.import_module("modules")
    loaded: list[LoadedModule] = []
    for info in pkgutil.iter_modules(package.__path__, prefix="modules."):
        short_name = info.name.rsplit(".", maxsplit=1)[-1]
        if re.fullmatch(r"module_\d{2}", short_name) is None:
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
    if len({item.day for item in loaded}) != len(loaded):
        raise RuntimeError("module day numbers must be unique")
    return sorted(loaded, key=lambda item: item.day)


def inject_styles() -> None:
    """Apply an editorial, long-form research-publication visual system."""
    st.markdown(
        """
        <style>
        :root {--ink:#e8eef7; --muted:#93a4ba; --rule:#20304a; --paper:#0b1220;
          --accent:#49bff2; --warm:#f5ba72; --green:#60d394;}
        .stApp {background:
          radial-gradient(circle at 88% -8%, rgba(33,93,145,.28), transparent 31rem),
          linear-gradient(180deg,#070b14 0%,#090e18 100%);}
        [data-testid="stSidebar"] {background:#090f1b; border-right:1px solid var(--rule);}
        .block-container {max-width:1440px; padding-top:2.4rem; padding-bottom:6rem;}
        h1,h2,h3 {font-weight:650; letter-spacing:-.032em; text-wrap:balance;}
        h1 {font-size:clamp(2.2rem,4vw,4rem)!important; line-height:1.02!important;
          background:linear-gradient(100deg,#f8fafc 15%,#67d2fa 72%);
          -webkit-background-clip:text; -webkit-text-fill-color:transparent;}
        h2 {margin-top:2.2rem!important;} p {line-height:1.72;}
        div[data-testid="stMetric"] {background:rgba(15,23,42,.78); border:1px solid var(--rule);
          border-radius:14px; padding:.7rem 1rem; box-shadow:0 14px 40px rgba(0,0,0,.12);}
        .eyebrow {font-size:.72rem; font-weight:700; color:var(--accent); letter-spacing:.16em;
          text-transform:uppercase; margin-bottom:.4rem;}
        .dek {max-width:780px; color:#aebdd0; font-size:1.08rem; line-height:1.65;}
        .research-note {border-left:3px solid var(--accent); background:#0d1728;
          padding:1rem 1.2rem; border-radius:0 11px 11px 0; margin:1rem 0;}
        .lesson-card {background:linear-gradient(145deg,rgba(17,29,49,.92),rgba(10,18,31,.92));
          border:1px solid var(--rule); padding:1.05rem 1.2rem; border-radius:14px; margin:.55rem 0;}
        .status-ready {color:var(--accent);font-weight:700}.status-completed{color:var(--green);font-weight:700}
        .status-planned {color:var(--muted);font-weight:650}.citation{font-size:.93rem;color:#a9bad0}
        code {font-size:.88em;} [data-testid="stDataFrame"] {border:1px solid var(--rule);border-radius:12px;}
        </style>
        """,
        unsafe_allow_html=True,
    )


@st.fragment(run_every=1.0)
def render_focus_timer(minutes: int = 60) -> None:
    """Render a non-blocking, session-persistent focus timer."""
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
    color = "#60d394" if remaining == 0 else "#e8eef7"
    st.markdown(
        f"<div class='eyebrow'>Focus block</div><div style='font:600 28px "
        f"ui-monospace;color:{color};margin:5px 0'>{remaining // 60:02d}:"
        f"{remaining % 60:02d}</div>",
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
    if reset_column.button("Reset", key="focus_reset", width="stretch"):
        st.session_state.focus_remaining = float(initial_seconds)
        st.session_state.focus_running = False
        st.session_state.focus_last_tick = time.monotonic()
        st.rerun(scope="fragment")


def _status_for_day(day: int, learning_entries: list[dict[str, Any]]) -> str:
    match = next((entry for entry in learning_entries if int(entry["day"]) == day), None)
    return str(match["status"]) if match else "planned"


def render_header(eyebrow: str, title: str, description: str) -> None:
    """Render consistent editorial page framing."""
    st.markdown(f"<div class='eyebrow'>{eyebrow}</div>", unsafe_allow_html=True)
    st.title(title)
    st.markdown(f"<div class='dek'>{description}</div>", unsafe_allow_html=True)


def render_today(
    modules: list[LoadedModule],
    current_lesson: PlannedLesson,
    learning_entries: list[dict[str, Any]],
) -> None:
    """Render exactly the current lesson, never a future pre-generated chapter."""
    current_module = next(
        (item for item in modules if item.day == current_lesson.day), None
    )
    render_header(
        f"Day {current_lesson.day:02d} · {current_lesson.domain}",
        current_lesson.topic,
        "One deliberate module, researched when it becomes due. Future roadmap entries "
        "remain titles—not stale prewritten lessons.",
    )
    left, middle, right = st.columns(3)
    left.metric("Stage", current_lesson.stage)
    middle.metric("Rotation", "ML → CV → EAI")
    right.metric("Status", _status_for_day(current_lesson.day, learning_entries).title())

    if current_module is None:
        st.info(
            "This lesson is intentionally not pre-generated. In the Fabric or ACP chat, "
            "send **generate next**. The agent will research current primary literature, "
            "author only this module, verify it, and append its provenance log."
        )
        st.markdown("### Research brief")
        st.markdown(
            "- Re-check the topic against current surveys, primary papers, and credible "
            "technical articles on the generation date.\n"
            "- Preserve the planned conceptual spine, but revise frontier emphasis when "
            "the evidence has moved.\n"
            "- Produce full derivations, an executable experiment, and an interactive "
            "simulator before advancing state."
        )
        return

    module_left, module_middle, module_right = st.columns(3)
    module_left.metric("Designed duration", f"{current_module.duration_minutes} min")
    module_middle.metric("Archive ID", current_module.slug)
    module_right.metric("Generated modules", len(modules))
    current_module.module.render()


def _render_reflection(module: LoadedModule, entry: dict[str, Any]) -> None:
    st.subheader("Learning reflection")
    with st.form(f"reflection_{module.day}"):
        minutes = st.number_input(
            "Minutes spent", min_value=0, max_value=480,
            value=int(entry.get("minutes_spent", 0)), step=5,
        )
        confidence = st.slider(
            "Confidence after study", 1, 5, int(entry.get("confidence") or 3),
            help="1 = cannot reconstruct; 5 = can derive, implement, and critique.",
        )
        notes = st.text_area(
            "Research notes, unresolved questions, and connections",
            value=str(entry.get("notes", "")), height=160,
        )
        revisit = st.checkbox("Add to revisit queue", value=bool(entry.get("revisit")))
        mark_complete = st.checkbox(
            "Mark module complete", value=entry.get("status") == "completed"
        )
        submitted = st.form_submit_button("Save reflection", type="primary")
    if submitted:
        saved = save_learning_reflection(
            module.day, int(minutes), int(confidence), notes, revisit, mark_complete
        )
        state = load_state()
        if mark_complete and module.day == state.current_day:
            save_state(advance_state(state, module.slug))
        st.success(f"Saved Day {module.day:02d} as {saved['status']}.")
        st.rerun()


def render_archive(
    modules: list[LoadedModule], learning_entries: list[dict[str, Any]]
) -> None:
    """Render immutable previous modules plus mutable personal reflections."""
    render_header(
        "Learning archive",
        "Return to any generated module",
        "Articles, simulators, code, provenance, confidence, and revisit flags remain "
        "available after the curriculum advances.",
    )
    labels = [f"Day {item.day:02d} · {item.domain} · {item.title}" for item in modules]
    selected_label = st.selectbox("Open archived module", labels)
    selected = modules[labels.index(selected_label)]
    entry = next(item for item in learning_entries if int(item["day"]) == selected.day)
    status = str(entry["status"])
    st.markdown(
        f"<div class='lesson-card'><span class='status-{status}'>{status.upper()}</span> · "
        f"Generated {entry['generated_on']} · "
        f"Confidence {entry.get('confidence') or 'not recorded'}/5</div>",
        unsafe_allow_html=True,
    )
    selected.module.render()
    st.divider()
    _render_reflection(selected, entry)


def render_roadmap(
    plan_metadata: dict[str, Any],
    lessons: list[PlannedLesson],
    learning_entries: list[dict[str, Any]],
    current_day: int,
) -> None:
    """Render breadth and sequence without pretending future titles are finished lessons."""
    render_header(
        "Open-ended curriculum",
        "A map, not a content dump",
        "The horizon preserves prerequisite order and breadth. Only the current day is "
        "researched and authored; frontier slots are refreshed when reached.",
    )
    completed = sum(
        _status_for_day(lesson.day, learning_entries) == "completed" for lesson in lessons
    )
    first, second, third, fourth = st.columns(4)
    first.metric("Planning horizon", f"{len(lessons)} days")
    second.metric("Completed", completed)
    third.metric("Current day", current_day)
    fourth.metric("Last roadmap review", plan_metadata["updated_on"])
    st.progress(completed / len(lessons) if lessons else 0.0)

    domain_filter = st.multiselect("Domains", DOMAINS, default=list(DOMAINS))
    stage_options = list(dict.fromkeys(lesson.stage for lesson in lessons))
    stage_filter = st.multiselect("Stages", stage_options, default=stage_options)
    rows = []
    for lesson in lessons:
        if lesson.domain not in domain_filter or lesson.stage not in stage_filter:
            continue
        status = _status_for_day(lesson.day, learning_entries)
        if lesson.day == current_day and status == "planned":
            status = "due · generate just in time"
        rows.append(
            {
                "Day": lesson.day,
                "Domain": lesson.domain,
                "Stage": lesson.stage,
                "Lesson spine": lesson.topic,
                "Status": status,
            }
        )
    st.dataframe(rows, hide_index=True, width="stretch", height=620)

    st.subheader("Supporting computer-science threads")
    st.markdown(
        "Every domain module pulls in the foundations it actually needs rather than "
        "isolating them into superficial survey days: **"
        + " · ".join(plan_metadata["supporting_cs_threads"])
        + "**."
    )
    st.caption(plan_metadata["policy"]["coverage"])


def render_research_log(
    plan_metadata: dict[str, Any], research_entries: list[dict[str, Any]]
) -> None:
    """Expose source provenance, corrections, and live frontier review signals."""
    render_header(
        "Research provenance",
        "What informed each module",
        "Archived chapters keep their original context. New evidence and corrections "
        "are appended rather than silently erasing what was previously studied.",
    )
    st.subheader("Live frontier review anchors")
    columns = st.columns(3)
    for column, anchor in zip(
        columns, plan_metadata["live_frontier_anchors"], strict=True
    ):
        with column:
            st.markdown(
                f"<div class='lesson-card'><div class='eyebrow'>{anchor['domain']}</div>"
                f"<b>Reviewed {anchor['reviewed_on']}</b><p>{anchor['signal']}</p>"
                f"<a href='{anchor['source']}'>Open recent literature feed ↗</a></div>",
                unsafe_allow_html=True,
            )

    st.subheader("Module source ledger")
    for entry in reversed(research_entries):
        with st.expander(
            f"Day {int(entry['day']):02d} · researched {entry['researched_on']}"
        ):
            st.write(entry.get("scope_note", ""))
            for source in entry["sources"]:
                st.markdown(
                    f"- **{source['title']}** — {source['authors']} ({source['year']})  "
                    f"[{source['kind']}]({source['url']})"
                )
            corrections = entry.get("corrections", [])
            if corrections:
                st.markdown("**Corrections and later evidence**")
                for correction in corrections:
                    st.markdown(f"- {correction}")
            else:
                st.caption("No corrections have been appended.")


def main() -> None:
    """Render the research curriculum workspace."""
    inject_styles()
    state = load_state()
    plan_metadata, lessons = load_plan()
    modules = discover_modules()
    learning_entries = load_learning_log()
    research_entries = load_research_log()
    current_lesson = lesson_for_day(state.current_day)

    with st.sidebar:
        st.markdown("## ∇ AI Research Lab")
        st.caption("One current lesson · permanent archive · live research")
        render_focus_timer(60)
        st.divider()
        view = st.radio(
            "Workspace",
            ["Today", "Archive", "Roadmap", "Research log"],
            label_visibility="collapsed",
        )
        st.divider()
        st.metric("Current day", state.current_day)
        st.metric("Current domain", DOMAINS[state.current_domain_index])
        st.caption(f"State updated: {state.last_updated}")

    if view == "Today":
        render_today(modules, current_lesson, learning_entries)
    elif view == "Archive":
        render_archive(modules, learning_entries)
    elif view == "Roadmap":
        render_roadmap(plan_metadata, lessons, learning_entries, state.current_day)
    else:
        render_research_log(plan_metadata, research_entries)


if __name__ == "__main__":
    main()
