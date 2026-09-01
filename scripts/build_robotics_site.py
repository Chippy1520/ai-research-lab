"""Build the static GitHub Pages payload for the AI Research Lab."""

from __future__ import annotations

import ast
import json
import re
import shutil
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
INTELLIGENCE_DIR = ROOT / "intelligence"
SITE_DIR = ROOT / "site"
DATA_DIR = SITE_DIR / "data"
REPORT_OUTPUT_DIR = DATA_DIR / "reports"


class _NullContext:
    def __enter__(self) -> "_NullContext":
        return self

    def __exit__(self, *_args: object) -> None:
        return None


class _ArticleCollector:
    """Capture a module's text-first Streamlit article as serializable blocks."""

    def __init__(self) -> None:
        self.blocks: list[dict[str, Any]] = []

    def _add(self, kind: str, content: object) -> None:
        self.blocks.append({"type": kind, "content": str(content).strip()})

    def header(self, content: object, *_args: object, **_kwargs: object) -> None:
        self._add("header", content)

    def subheader(self, content: object, *_args: object, **_kwargs: object) -> None:
        self._add("subheader", content)

    def markdown(self, content: object, *_args: object, **_kwargs: object) -> None:
        self._add("markdown", content)

    def latex(self, content: object, *_args: object, **_kwargs: object) -> None:
        self._add("latex", content)

    def caption(self, content: object, *_args: object, **_kwargs: object) -> None:
        self._add("caption", content)

    def video(self, content: object, *_args: object, **_kwargs: object) -> None:
        self._add("video", content)

    def code(
        self,
        content: object,
        *_args: object,
        language: str | None = None,
        **_kwargs: object,
    ) -> None:
        self.blocks.append(
            {
                "type": "code",
                "content": str(content).strip(),
                "language": language or "text",
            }
        )

    def dataframe(self, content: object, *_args: object, **_kwargs: object) -> None:
        if hasattr(content, "to_dict"):
            records = content.to_dict(orient="records")
        else:
            records = content
        self.blocks.append({"type": "table", "content": records})

    def columns(
        self,
        specification: int | list[object] | tuple[object, ...],
        *_args: object,
        **_kwargs: object,
    ) -> tuple[_NullContext, ...]:
        count = specification if isinstance(specification, int) else len(specification)
        return tuple(_NullContext() for _ in range(count))


def _read_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError(f"Expected a JSON object in {path}")
    return payload


def _literal_assignment(tree: ast.Module, name: str) -> Any:
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if any(isinstance(target, ast.Name) and target.id == name for target in node.targets):
            return ast.literal_eval(node.value)
    raise ValueError(f"Module does not define literal {name}")


def _article_functions(tree: ast.Module) -> list[ast.FunctionDef]:
    functions = {
        node.name: node for node in tree.body if isinstance(node, ast.FunctionDef)
    }
    selected: set[str] = set()
    pending = ["_render_article"]
    while pending:
        name = pending.pop()
        if name in selected or name not in functions:
            continue
        selected.add(name)
        for node in ast.walk(functions[name]):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                if node.func.id in functions:
                    pending.append(node.func.id)
    return [function for name, function in functions.items() if name in selected]


def _collect_article(tree: ast.Module, path: Path) -> list[dict[str, Any]]:
    collector = _ArticleCollector()
    future_imports = [
        node
        for node in tree.body
        if isinstance(node, ast.ImportFrom) and node.module == "__future__"
    ]
    article_tree = ast.Module(
        body=[*future_imports, *_article_functions(tree)],
        type_ignores=[],
    )
    ast.fix_missing_locations(article_tree)
    namespace: dict[str, Any] = {"st": collector}
    exec(compile(article_tree, str(path), "exec"), namespace)
    renderer = namespace.get("_render_article")
    if callable(renderer):
        renderer()
    return collector.blocks


def _module_payload(path: Path) -> dict[str, Any]:
    module_source = path.read_text(encoding="utf-8")
    tree = ast.parse(module_source, filename=str(path))
    experiment_names = re.findall(
        r"experiments[/\\]([A-Za-z0-9_]+\.py)", module_source
    )
    experiment_name = experiment_names[0] if experiment_names else None
    experiment_path = ROOT / "experiments" / experiment_name if experiment_name else None
    return {
        "slug": path.stem,
        "metadata": _literal_assignment(tree, "METADATA"),
        "article": _collect_article(tree, path),
        "module_source_url": (
            "https://github.com/Chippy1520/ai-research-lab/blob/main/"
            f"modules/{path.name}"
        ),
        "experiment_path": (
            f"experiments/{experiment_name}" if experiment_name else None
        ),
        "experiment_source": (
            experiment_path.read_text(encoding="utf-8")
            if experiment_path and experiment_path.is_file()
            else None
        ),
    }


def _build_curriculum_payload() -> dict[str, Any]:
    return {
        "plan": _read_json(ROOT / "curriculum_plan.json"),
        "state": _read_json(ROOT / "curriculum_state.json"),
        "learning_log": _read_json(ROOT / "learning_log.json"),
        "research_log": _read_json(ROOT / "research_log.json"),
        "modules": [
            _module_payload(path)
            for path in sorted((ROOT / "modules").glob("module_??.py"))
        ],
    }


def build() -> dict[str, Any]:
    """Copy validated source data and create the static site manifest."""
    ecosystem_path = INTELLIGENCE_DIR / "ecosystem.json"
    jobs_path = INTELLIGENCE_DIR / "jobs.json"
    reports_dir = INTELLIGENCE_DIR / "reports"

    ecosystem = _read_json(ecosystem_path)
    jobs = _read_json(jobs_path)
    curriculum = _build_curriculum_payload()
    report_paths = sorted(reports_dir.glob("????-??-??.md"), reverse=True)
    if not report_paths:
        raise ValueError("At least one dated intelligence report is required")

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ecosystem_path, DATA_DIR / "ecosystem.json")
    shutil.copy2(jobs_path, DATA_DIR / "jobs.json")
    with (DATA_DIR / "curriculum.json").open("w", encoding="utf-8") as handle:
        json.dump(curriculum, handle, indent=2, ensure_ascii=False)
        handle.write("\n")

    reports = []
    current_names = set()
    for report_path in report_paths:
        output_name = report_path.name
        current_names.add(output_name)
        shutil.copy2(report_path, REPORT_OUTPUT_DIR / output_name)
        reports.append(
            {
                "date": report_path.stem,
                "path": f"data/reports/{output_name}",
            }
        )
    for stale_path in REPORT_OUTPUT_DIR.glob("*.md"):
        if stale_path.name not in current_names:
            stale_path.unlink()

    openings = jobs.get("openings", [])
    early_career = [
        opening
        for opening in openings
        if opening.get("seniority") in {"internship", "new graduate"}
    ]
    companies = ecosystem.get("companies", [])
    manifest = {
        "site_title": "AI Research Lab",
        "ecosystem_as_of": ecosystem.get("as_of"),
        "jobs_last_checked": jobs.get("last_checked"),
        "company_count": len(companies),
        "humanoid_count": sum(
            str(company.get("category", "")).startswith("Humanoid")
            for company in companies
        ),
        "opening_count": len(openings),
        "early_career_count": len(early_career),
        "reports": reports,
        "curriculum": {
            "current_day": curriculum["state"].get("current_day"),
            "mapped_lessons": len(curriculum["plan"].get("lessons", [])),
            "generated_modules": len(curriculum["modules"]),
            "research_sources": sum(
                len(entry.get("sources", []))
                for entry in curriculum["research_log"].get("entries", [])
            ),
        },
    }
    with (DATA_DIR / "manifest.json").open("w", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
    return manifest


if __name__ == "__main__":
    result = build()
    print(
        "static site data built: "
        f"companies={result['company_count']}, "
        f"openings={result['opening_count']}, "
        f"modules={result['curriculum']['generated_modules']}, "
        f"reports={len(result['reports'])}"
    )
