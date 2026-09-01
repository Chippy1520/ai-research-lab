"""US robotics ecosystem, jobs, and daily-intelligence dashboard."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

ROOT = Path(__file__).resolve().parent
INTELLIGENCE_ROOT = ROOT / "intelligence"
ECOSYSTEM_PATH = INTELLIGENCE_ROOT / "ecosystem.json"
JOBS_PATH = INTELLIGENCE_ROOT / "jobs.json"
REPORTS_PATH = INTELLIGENCE_ROOT / "reports"


@dataclass(frozen=True)
class CompanyRecord:
    """A sourced company snapshot; monetary observations are explicitly dated."""

    company_id: str
    name: str
    founded: int
    hq_city: str
    hq_state: str
    latitude: float
    longitude: float
    cluster: str
    category: str
    focus: str
    stage: str
    funding_usd_millions: float | None
    valuation_usd_billions: float | None
    valuation_label: str
    valuation_as_of: str | None
    valuation_type: str
    valuation_note: str
    careers_url: str
    sources: tuple[dict[str, Any], ...]

    @classmethod
    def from_mapping(cls, payload: dict[str, Any]) -> "CompanyRecord":
        """Validate one company snapshot from JSON."""
        required = {
            "company_id",
            "name",
            "founded",
            "hq_city",
            "hq_state",
            "latitude",
            "longitude",
            "cluster",
            "category",
            "focus",
            "stage",
            "funding_usd_millions",
            "valuation_usd_billions",
            "valuation_label",
            "valuation_as_of",
            "valuation_type",
            "valuation_note",
            "careers_url",
            "sources",
        }
        missing = required.difference(payload)
        if missing:
            raise ValueError(f"company snapshot is missing {sorted(missing)}")
        company = cls(
            company_id=str(payload["company_id"]),
            name=str(payload["name"]),
            founded=int(payload["founded"]),
            hq_city=str(payload["hq_city"]),
            hq_state=str(payload["hq_state"]),
            latitude=float(payload["latitude"]),
            longitude=float(payload["longitude"]),
            cluster=str(payload["cluster"]),
            category=str(payload["category"]),
            focus=str(payload["focus"]),
            stage=str(payload["stage"]),
            funding_usd_millions=(
                None
                if payload["funding_usd_millions"] is None
                else float(payload["funding_usd_millions"])
            ),
            valuation_usd_billions=(
                None
                if payload["valuation_usd_billions"] is None
                else float(payload["valuation_usd_billions"])
            ),
            valuation_label=str(payload["valuation_label"]),
            valuation_as_of=(
                None
                if payload["valuation_as_of"] is None
                else str(payload["valuation_as_of"])
            ),
            valuation_type=str(payload["valuation_type"]),
            valuation_note=str(payload["valuation_note"]),
            careers_url=str(payload["careers_url"]),
            sources=tuple(payload["sources"]),
        )
        if not 1900 <= company.founded <= 2100:
            raise ValueError(f"invalid founding year for {company.name}")
        if not company.sources or not all(
            str(source.get("url", "")).startswith("https://")
            for source in company.sources
        ):
            raise ValueError(f"{company.name} requires HTTPS provenance")
        return company


def _read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as stream:
        payload = json.load(stream)
    if not isinstance(payload, dict):
        raise TypeError(f"{path.name} must contain a JSON object")
    return payload


def load_ecosystem(
    path: Path = ECOSYSTEM_PATH,
) -> tuple[dict[str, Any], list[CompanyRecord]]:
    """Load and validate ecosystem metadata and company observations."""
    payload = _read_json(path)
    companies = [CompanyRecord.from_mapping(item) for item in payload["companies"]]
    identifiers = [company.company_id for company in companies]
    if len(identifiers) != len(set(identifiers)):
        raise ValueError("company identifiers must be unique")
    return payload, companies


def load_jobs(path: Path = JOBS_PATH) -> dict[str, Any]:
    """Load the latest official-career-page scan."""
    payload = _read_json(path)
    if not {"last_checked", "openings", "requirement_signals", "targets"} <= set(
        payload
    ):
        raise ValueError("jobs intelligence violates its schema")
    for opening in payload["openings"]:
        if not str(opening.get("url", "")).startswith("https://"):
            raise ValueError("every opening requires an official HTTPS URL")
    return payload


def latest_report(reports_path: Path = REPORTS_PATH) -> tuple[str | None, str]:
    """Return the latest dated Markdown brief without mutating the archive."""
    reports = sorted(reports_path.glob("????-??-??.md"), reverse=True)
    if not reports:
        return None, "No daily report has been archived yet."
    latest = reports[0]
    return latest.stem, latest.read_text(encoding="utf-8")


def _valuation_table(companies: list[CompanyRecord]) -> list[dict[str, Any]]:
    """Create display rows without conflating incompatible monetary measures."""
    return [
        {
            "Company": company.name,
            "Founded": company.founded,
            "HQ / US base": f"{company.hq_city}, {company.hq_state}",
            "Cluster": company.cluster,
            "Category": company.category,
            "Stage": company.stage,
            "Funding observation": (
                "Undisclosed"
                if company.funding_usd_millions is None
                else f"${company.funding_usd_millions:,.0f}M"
            ),
            "Valuation observation": company.valuation_label,
            "Valuation basis": company.valuation_type,
            "Valuation date": company.valuation_as_of or "Not disclosed",
        }
        for company in companies
    ]


def _render_brief(metadata: dict[str, Any], jobs: dict[str, Any]) -> None:
    report_date, report = latest_report()
    top_left, top_middle, top_right = st.columns(3)
    top_left.metric("Ecosystem snapshot", metadata["as_of"])
    top_middle.metric("Latest jobs scan", jobs["last_checked"])
    top_right.metric("Archived brief", report_date or "Pending")
    st.markdown(report)


def _render_companies(
    metadata: dict[str, Any], companies: list[CompanyRecord]
) -> None:
    categories = sorted({company.category for company in companies})
    selected = st.multiselect("Company categories", categories, default=categories)
    filtered = [company for company in companies if company.category in selected]
    st.dataframe(
        _valuation_table(filtered), hide_index=True, width="stretch", height=500
    )
    st.caption(metadata["funding_methodology"])
    st.caption(metadata["valuation_methodology"])

    timeline_frame = pd.DataFrame(
        {
            "Company": [company.name for company in filtered],
            "Founded": [company.founded for company in filtered],
            "Cluster": [company.cluster for company in filtered],
            "Stage": [company.stage for company in filtered],
            "Category": [company.category for company in filtered],
        }
    )
    if not timeline_frame.empty:
        timeline = px.scatter(
            timeline_frame,
            x="Founded",
            y="Cluster",
            color="Category",
            hover_name="Company",
            hover_data=["Stage"],
            title="Company formation timeline by US robotics cluster",
        )
        timeline.update_traces(marker={"size": 13, "line": {"width": 1}})
        timeline.update_layout(template="plotly_dark", height=470)
        st.plotly_chart(timeline, width="stretch")

    st.subheader("Company evidence cards")
    for company in filtered:
        with st.expander(
            f"{company.name} · {company.category} · founded {company.founded}"
        ):
            st.write(company.focus)
            st.markdown(f"**Growth stage:** {company.stage}")
            st.markdown(
                f"**Valuation interpretation:** {company.valuation_note}"
            )
            st.markdown(f"[Official careers page ↗]({company.careers_url})")
            st.markdown("**Sources**")
            for source in company.sources:
                st.markdown(
                    f"- [{source['title']}]({source['url']}) — "
                    f"{source.get('date', 'access date not recorded')}"
                )


def _render_map(metadata: dict[str, Any], companies: list[CompanyRecord]) -> None:
    figure = go.Figure()
    figure.add_trace(
        go.Scattergeo(
            lon=[company.longitude for company in companies],
            lat=[company.latitude for company in companies],
            text=[
                f"<b>{company.name}</b><br>{company.hq_city}, {company.hq_state}"
                f"<br>{company.category}<br>{company.stage}"
                for company in companies
            ],
            mode="markers",
            marker={
                "size": 11,
                "color": "#49bff2",
                "line": {"width": 1, "color": "#d9f4ff"},
                "opacity": 0.82,
            },
            name="Companies / US bases",
        )
    )
    hubs = metadata["hubs"]
    figure.add_trace(
        go.Scattergeo(
            lon=[hub["longitude"] for hub in hubs],
            lat=[hub["latitude"] for hub in hubs],
            text=[f"<b>{hub['name']}</b><br>{hub['thesis']}" for hub in hubs],
            mode="markers",
            marker={
                "size": 24,
                "symbol": "circle-open",
                "color": "#f5ba72",
                "line": {"width": 3},
            },
            name="Ecosystem clusters",
        )
    )
    figure.update_geos(
        scope="usa",
        projection_type="albers usa",
        showland=True,
        landcolor="#101a2b",
        showlakes=True,
        lakecolor="#09111f",
        subunitcolor="#3a4c66",
        bgcolor="rgba(0,0,0,0)",
    )
    figure.update_layout(
        template="plotly_dark",
        height=610,
        margin={"l": 0, "r": 0, "t": 45, "b": 0},
        title="US robotics concentration: companies and enabling clusters",
        legend={"orientation": "h"},
    )
    st.plotly_chart(figure, width="stretch")

    for hub in hubs:
        tracked_count = sum(
            company.cluster == hub["name"] for company in companies
        )
        with st.expander(
            f"{hub['name']} · {tracked_count} tracked companies / US bases"
        ):
            st.markdown(f"**Concentration thesis:** {hub['thesis']}")
            st.markdown(f"**Institutions:** {', '.join(hub['institutions'])}")
            st.markdown(f"**Representative organizations:** {', '.join(hub['organizations'])}")
            st.markdown(f"**3–5 year watch:** {hub['outlook']}")

    st.info(metadata["evolution_thesis"])


def _render_jobs(jobs: dict[str, Any]) -> None:
    first, second, third = st.columns(3)
    openings = jobs["openings"]
    first.metric("Verified openings", len(openings))
    second.metric(
        "Intern / new-grad",
        sum(
            opening.get("seniority") in {"internship", "new graduate"}
            for opening in openings
        ),
    )
    second_delta = sum(opening.get("status") == "new" for opening in openings)
    third.metric("New since prior scan", second_delta)

    if openings:
        st.dataframe(
            [
                {
                    "Status": opening["status"],
                    "Company": opening["company"],
                    "Role": opening["title"],
                    "Location": opening["location"],
                    "Level": opening["seniority"],
                    "First seen": opening["first_seen"],
                    "Official posting": opening["url"],
                }
                for opening in openings
            ],
            hide_index=True,
            width="stretch",
            height=460,
            column_config={
                "Official posting": st.column_config.LinkColumn("Official posting")
            },
        )
        early_career = [
            opening
            for opening in openings
            if opening["seniority"] in {"internship", "new graduate"}
        ]
        if early_career:
            st.subheader("Early-career qualification notes")
            for opening in early_career:
                with st.expander(
                    f"{opening['company']} · {opening['title']} · {opening['location']}"
                ):
                    excerpt = opening.get(
                        "qualification_excerpt",
                        "Open the official posting for requirements.",
                    )
                    st.write(excerpt)
                    st.markdown(f"[Open official posting ↗]({opening['url']})")
    else:
        st.info(
            "No individual openings have completed verification yet. The daily scanner "
            "will only publish roles it can trace to an official company careers page."
        )

    st.subheader("Recurring qualification signals")
    signals = jobs["requirement_signals"]
    if signals:
        signal_frame = pd.DataFrame(signals).sort_values("company_mentions")
        chart = px.bar(
            signal_frame,
            x="company_mentions",
            y="skill",
            orientation="h",
            color="category",
            hover_data=["evidence", "portfolio_response"],
            labels={"company_mentions": "Companies mentioning skill", "skill": "Skill"},
        )
        chart.update_layout(template="plotly_dark", height=500)
        st.plotly_chart(chart, width="stretch")
        st.markdown("### Evidence-linked portfolio actions")
        for signal in sorted(
            signals, key=lambda item: int(item["company_mentions"]), reverse=True
        ):
            st.markdown(
                f"- **{signal['skill']}** ({signal['company_mentions']} companies): "
                f"{signal['portfolio_response']}"
            )

    st.subheader("Official career pages monitored daily")
    st.dataframe(
        jobs["targets"],
        hide_index=True,
        width="stretch",
        column_config={"careers_url": st.column_config.LinkColumn("Official careers page")},
    )
    st.caption(jobs["methodology"])


def render_robotics_intelligence() -> None:
    """Render the independent US robotics market-intelligence workspace."""
    metadata, companies = load_ecosystem()
    jobs = load_jobs()
    st.markdown("<div class='eyebrow'>US robotics intelligence</div>", unsafe_allow_html=True)
    st.title("Humanoids, embodied AI, and the companies hiring around them")
    st.markdown(
        "<div class='dek'>A sourced market map—not a hype leaderboard. Track company "
        "formation, geographic concentration, dated valuation observations, current "
        "technical signals, and official job openings.</div>",
        unsafe_allow_html=True,
    )
    metric_columns = st.columns(4)
    metric_columns[0].metric("Tracked companies", len(companies))
    metric_columns[1].metric(
        "Humanoid builders",
        sum(company.category.startswith("Humanoid") for company in companies),
    )
    metric_columns[2].metric("US clusters", len(metadata["hubs"]))
    metric_columns[3].metric("Snapshot date", metadata["as_of"])

    brief_tab, companies_tab, map_tab, jobs_tab = st.tabs(
        ["Daily brief", "Companies & timeline", "US concentration", "Jobs & skills"]
    )
    with brief_tab:
        _render_brief(metadata, jobs)
    with companies_tab:
        _render_companies(metadata, companies)
    with map_tab:
        _render_map(metadata, companies)
    with jobs_tab:
        _render_jobs(jobs)
