from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Optional
import subprocess

from .researcher import ResearchResult


def render_cli_report(result: ResearchResult) -> str:
    lines = [
        "",
        f"Intent: {result.task.intent}",
        f"Request: {result.task.raw_request}",
        f"Summary: {result.summary}",
        "",
        "New Information:",
    ]
    lines.extend(f"- {item}" for item in result.new_information or ["- None"])
    lines.append("")
    lines.append("What Remains Unchanged:")
    lines.extend(f"- {item}" for item in result.unchanged_points or ["- None"])
    lines.append("")
    lines.append("Thesis Impact:")
    lines.extend(f"- {item}" for item in result.thesis_impact or ["- None"])
    lines.append("")
    lines.append("Questions To Research:")
    lines.extend(f"- {item}" for item in result.questions_to_research or ["- None"])
    lines.append("")
    lines.append("Sources:")
    lines.extend(f"- {item}" for item in result.sources or ["- None"])
    lines.append("")
    lines.append(f"Proposed Save Path: {result.proposed_save_path}")
    lines.append("Status: Research presented only. No permanent knowledge has been written yet.")
    return "\n".join(lines)


def _render_company_markdown(result: ResearchResult) -> str:
    ticker = result.task.ticker or ""
    company = result.task.company or ticker
    existing_sections = result.knowledge.sections if result.knowledge.exists else {}
    existing_thesis = result.knowledge.current_thesis.strip() if result.knowledge.exists else ""
    thesis_text = existing_thesis or ("\n".join(f"- {item}" for item in result.thesis_impact) or "- Pending")
    changed_text = "\n".join(f"- {item}" for item in result.new_information) or "- Pending"
    questions_text = "\n".join(f"- {item}" for item in result.questions_to_research) or "- Pending"
    sources_text = "\n".join(f"- {item}" for item in result.sources) or "- Pending"
    overview_text = existing_sections.get("Company Overview", "").strip() or "- Research in progress."
    business_model_text = existing_sections.get("Business Model", "").strip() or "- Research in progress."
    financials_text = existing_sections.get("Financials", "").strip() or "- Update with verified figures from filings or trusted datasets."
    growth_drivers_text = existing_sections.get("Growth Drivers", "").strip() or "- Research in progress."
    competitive_position_text = existing_sections.get("Competitive Position", "").strip() or "- Research in progress."
    risks_text = existing_sections.get("Risks", "").strip() or "- Research in progress."
    related_themes_text = existing_sections.get("Related Themes", "").strip() or "- Pending"

    return f"""---
ticker: {ticker}
company: {company}
status: active
last_updated: {date.today().isoformat()}
---

# {company}

## Company Overview

{overview_text}

## Business Model

{business_model_text}

## Financials

{financials_text}

## Growth Drivers

{growth_drivers_text}

## Competitive Position

{competitive_position_text}

## Risks

{risks_text}

## Current Thesis

{thesis_text}

## What Changed

{changed_text}

## Questions

{questions_text}

## Related Themes

{related_themes_text}

## Sources

{sources_text}
"""


def save_research(result: ResearchResult, project_root: Path) -> Path:
    if result.task.ticker:
        path = project_root / "knowledge" / "companies" / f"{result.task.ticker}.md"
        content = _render_company_markdown(result)
    elif result.task.intent == "daily":
        path = project_root / "reports" / "daily" / f"{date.today().isoformat()}_daily_market_brief.md"
        content = "# Daily Market Brief\n\nStatus: placeholder\n"
    else:
        path = project_root / "knowledge" / "market" / f"{date.today().isoformat()}_research_note.md"
        content = "# Research Note\n\nStatus: placeholder\n"

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


def run_git_operations(project_root: Path, message: str, push: bool = False) -> str:
    commands = [
        ["git", "add", "."],
        ["git", "commit", "-m", message],
    ]
    if push:
        commands.append(["git", "push"])

    outputs = []
    for command in commands:
        completed = subprocess.run(
            command,
            cwd=project_root,
            capture_output=True,
            text=True,
            check=False,
        )
        outputs.append(f"$ {' '.join(command)}\n{completed.stdout}{completed.stderr}".strip())
        if completed.returncode != 0:
            break
    return "\n\n".join(outputs)
