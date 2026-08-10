from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from email.utils import parsedate_to_datetime
from pathlib import Path
import json
from typing import Dict, List, Optional
from urllib.parse import quote_plus
from xml.etree import ElementTree

import requests

from .knowledge import KnowledgeSnapshot, load_company_knowledge
from .router import Task


@dataclass
class Finding:
    title: str
    source_name: str
    source_type: str
    published_at: str
    url: str
    significance: str
    notes: str


@dataclass
class ResearchResult:
    task: Task
    knowledge: KnowledgeSnapshot
    findings: List[Finding] = field(default_factory=list)
    new_information: List[str] = field(default_factory=list)
    unchanged_points: List[str] = field(default_factory=list)
    thesis_impact: List[str] = field(default_factory=list)
    questions_to_research: List[str] = field(default_factory=list)
    sources: List[str] = field(default_factory=list)
    proposed_save_path: str = ""
    summary: str = ""


def _load_sources(project_root: Path) -> Dict[str, object]:
    path = project_root / "config" / "sources.yaml"
    return json.loads(path.read_text(encoding="utf-8"))


def _fetch_json(url: str, user_agent: str) -> dict:
    response = requests.get(url, headers={"User-Agent": user_agent}, timeout=20)
    response.raise_for_status()
    return response.json()


def _fetch_text(url: str, user_agent: str) -> str:
    response = requests.get(url, headers={"User-Agent": user_agent}, timeout=20)
    response.raise_for_status()
    return response.text


def _normalize_date(value: str) -> str:
    if not value:
        return "unknown"
    try:
        return parsedate_to_datetime(value).date().isoformat()
    except Exception:
        return value[:10]


def _parse_iso_date(value: str) -> Optional[datetime]:
    if not value or value == "unknown":
        return None
    try:
        return datetime.fromisoformat(value[:10])
    except ValueError:
        return None


def _rank_significance(title: str) -> str:
    lowered = title.lower()
    high_terms = ["earnings", "guidance", "8-k", "10-q", "10-k", "acquires", "investigation", "sec"]
    medium_terms = ["product", "launch", "partnership", "data center", "ai", "forecast"]
    if any(term in lowered for term in high_terms):
        return "HIGH"
    if any(term in lowered for term in medium_terms):
        return "MEDIUM"
    return "LOW"


def _period_window_days(period: str) -> int:
    if period == "today":
        return 2
    if period == "yesterday":
        return 3
    if period == "last_month":
        return 31
    if period == "last_three_months":
        return 93
    return 7


def _recent_sec_findings(company_cfg: dict, cfg: dict, period: str, intent: str) -> List[Finding]:
    cik = company_cfg.get("cik", "").zfill(10)
    if not cik:
        return []

    submissions_url = cfg["sec_submissions_url_template"].format(cik=cik)
    data = _fetch_json(submissions_url, cfg["user_agent"])
    recent = data.get("filings", {}).get("recent", {})
    forms = recent.get("form", [])[:8]
    dates = recent.get("filingDate", [])[:8]
    accession_numbers = recent.get("accessionNumber", [])[:8]
    results: List[Finding] = []
    allowed_forms = {"10-K", "10-Q", "8-K", "DEF 14A", "SC 13G", "SC 13D"}
    if intent == "sec":
        allowed_forms.update({"4", "SCHEDULE 13G", "SCHEDULE 13D"})
    cutoff_days = _period_window_days(period)
    now = datetime.now()
    for form, date, accession in zip(forms, dates, accession_numbers):
        normalized_form = form.upper()
        if normalized_form not in allowed_forms:
            continue
        parsed = _parse_iso_date(date)
        if parsed is not None and (now - parsed).days > cutoff_days:
            continue
        accession_clean = accession.replace("-", "")
        url = (
            f"https://www.sec.gov/Archives/edgar/data/"
            f"{int(cik)}/{accession_clean}/{accession}-index.htm"
        )
        results.append(
            Finding(
                title=f"{company_cfg['company']} filed {form}",
                source_name="SEC EDGAR",
                source_type="regulatory",
                published_at=date,
                url=url,
                significance="HIGH" if normalized_form in {"10-K", "10-Q", "8-K"} else "MEDIUM",
                notes=f"Recent SEC filing: {form}",
            )
        )
    return results


def _news_findings(query: str, cfg: dict, limit: int = 6) -> List[Finding]:
    rss_url = cfg["news_rss_url_template"].format(query=quote_plus(query))
    rss_text = _fetch_text(rss_url, cfg["user_agent"])
    root = ElementTree.fromstring(rss_text)
    channel = root.find("channel")
    if channel is None:
        return []

    findings: List[Finding] = []
    reputable_sources = [
        "Reuters",
        "Yahoo Finance",
        "Seeking Alpha",
        "Bloomberg",
        "CNBC",
        "MarketWatch",
        "Barron's",
        "Financial Times",
        "The Wall Street Journal",
        "NVIDIA Newsroom",
        "Apple",
        "Microsoft",
        "AMD",
    ]
    for item in channel.findall("item")[:limit]:
        title = item.findtext("title", default="Untitled")
        link = item.findtext("link", default="")
        pub_date = _normalize_date(item.findtext("pubDate", default=""))
        source_name = "Google News RSS"
        source_tag = item.find("source")
        if source_tag is not None and source_tag.text:
            source_name = source_tag.text.strip()
        if reputable_sources and not any(source.lower() in source_name.lower() for source in reputable_sources):
            continue
        findings.append(
            Finding(
                title=title,
                source_name=source_name,
                source_type="news",
                published_at=pub_date,
                url=link,
                significance=_rank_significance(title),
                notes="Recent news item from RSS search",
            )
        )
    return findings


def _sort_findings(findings: List[Finding]) -> List[Finding]:
    significance_rank = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    return sorted(
        findings,
        key=lambda item: (
            significance_rank.get(item.significance, 9),
            item.published_at,
        ),
        reverse=False,
    )


def _dedupe_findings(findings: List[Finding]) -> List[Finding]:
    seen = set()
    results: List[Finding] = []
    for finding in findings:
        key = (finding.title.lower().strip(), finding.url.strip())
        if key in seen:
            continue
        seen.add(key)
        results.append(finding)
    return results


def _build_company_result(task: Task, project_root: Path) -> ResearchResult:
    cfg = _load_sources(project_root)
    company_cfg = cfg.get("companies", {}).get(task.ticker or "", {})
    knowledge = load_company_knowledge(project_root, task.ticker)
    findings: List[Finding] = []

    if company_cfg:
        try:
            findings.extend(_recent_sec_findings(company_cfg, cfg, task.period, task.intent))
        except Exception as exc:
            findings.append(
                Finding(
                    title="SEC EDGAR lookup failed",
                    source_name="System",
                    source_type="system",
                    published_at=datetime.now().date().isoformat(),
                    url="",
                    significance="LOW",
                    notes=str(exc),
                )
            )

        period_terms = {
            "today": "when:1d",
            "yesterday": "when:2d",
            "last_month": "when:30d",
            "last_three_months": "when:90d",
            "recent": "when:7d",
        }
        query = f"{task.ticker} {company_cfg.get('company', '')} {period_terms.get(task.period, 'when:7d')}"
        try:
            findings.extend(_news_findings(query, cfg, limit=12))
        except Exception as exc:
            findings.append(
                Finding(
                    title="News search failed",
                    source_name="System",
                    source_type="system",
                    published_at=datetime.now().date().isoformat(),
                    url="",
                    significance="LOW",
                    notes=str(exc),
                )
            )

        ir_url = company_cfg.get("ir_url", "")
        if ir_url:
            findings.append(
                Finding(
                    title=f"{task.ticker} official investor relations home",
                    source_name="Company IR",
                    source_type="official",
                    published_at=datetime.now().date().isoformat(),
                    url=ir_url,
                    significance="MEDIUM",
                    notes="Primary source entry point for presentations, releases, and call materials",
                )
            )

    findings = _sort_findings(_dedupe_findings(findings))

    new_information = [f"{f.significance}: {f.title} ({f.source_name}, {f.published_at})" for f in findings[:8]]
    unchanged_points: List[str] = []
    if knowledge.exists and knowledge.current_thesis:
        unchanged_points.append(f"Current thesis on file from {knowledge.last_updated}: {knowledge.current_thesis}")
    else:
        unchanged_points.append("No prior formal thesis was found, so this looks like a fresh or lightly seeded research cycle.")

    thesis_impact: List[str] = []
    for finding in findings[:5]:
        lowered = finding.title.lower()
        if any(term in lowered for term in ["earnings", "guidance", "data center", "ai", "regulation", "investigation"]):
            thesis_impact.append(
                f"{finding.title}: may affect growth expectations, regulation view, or the current thesis depending on underlying details."
            )
    if not thesis_impact:
        thesis_impact.append("Most items currently look like monitoring inputs rather than clear thesis-breaking evidence.")

    questions = [
        "Which of these developments are actually new versus repeated coverage of the same event?",
        "Do any recent filings or releases change revenue, margin, or competitive assumptions?",
        "Does the newest information support or weaken the existing thesis on file?",
    ]
    if task.period == "today":
        questions.append("Which of today's items materially changes the company view rather than just intraday narrative?")

    sources = [f"{finding.source_name}: {finding.url}" for finding in findings if finding.url]
    proposed_save_path = f"knowledge/companies/{task.ticker}.md" if task.ticker else "knowledge/market/"
    summary = f"Completed {task.intent} research for {task.ticker or 'request'} using existing knowledge, SEC, official IR, and recent news."

    return ResearchResult(
        task=task,
        knowledge=knowledge,
        findings=findings,
        new_information=new_information,
        unchanged_points=unchanged_points,
        thesis_impact=thesis_impact,
        questions_to_research=questions,
        sources=sources,
        proposed_save_path=proposed_save_path,
        summary=summary,
    )


def _build_status_result(task: Task, project_root: Path) -> ResearchResult:
    cfg = _load_sources(project_root)
    tickers = list(cfg.get("companies", {}).keys())
    findings: List[Finding] = []
    for ticker in tickers:
        snap = load_company_knowledge(project_root, ticker)
        findings.append(
            Finding(
                title=f"{ticker} knowledge status",
                source_name="Knowledge Base",
                source_type="internal",
                published_at=snap.last_updated,
                url=str(snap.path) if snap.path else "",
                significance="MEDIUM",
                notes="Has existing knowledge" if snap.exists else "Needs first note",
            )
        )
    return ResearchResult(
        task=task,
        knowledge=KnowledgeSnapshot(ticker=None, path=None, exists=False),  # type: ignore[name-defined]
        findings=findings,
        new_information=[f"{f.title}: {f.notes}" for f in findings],
        unchanged_points=[],
        thesis_impact=[],
        questions_to_research=["Which watchlist names have stale notes and need a new update cycle?"],
        sources=[],
        proposed_save_path="knowledge/companies/",
        summary="Watchlist status snapshot created.",
    )


def research(task: Task, project_root: Path) -> ResearchResult:
    if task.intent in {"research", "update", "analyze", "compare", "sec"} and task.ticker:
        return _build_company_result(task, project_root)
    if task.intent == "status":
        return _build_status_result(task, project_root)

    fallback_knowledge = load_company_knowledge(project_root, task.ticker)
    return ResearchResult(
        task=task,
        knowledge=fallback_knowledge,
        new_information=["This intent is recognized, but V0.1 focuses on the core company research loop first."],
        unchanged_points=["No permanent knowledge was modified."],
        thesis_impact=["Use this prototype mainly for research, update, and save flows."],
        questions_to_research=["What is the next smallest implementation that materially improves the research loop?"],
        sources=[],
        proposed_save_path="knowledge/",
        summary=f"Intent '{task.intent}' was classified successfully but is only minimally implemented in V0.1.",
    )
