from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import json
import re
from typing import List, Optional


INTENTS = [
    "research",
    "update",
    "daily",
    "sec",
    "theme",
    "compare",
    "ask",
    "analyze",
    "save",
    "status",
]


@dataclass
class Task:
    raw_request: str
    intent: str
    ticker: Optional[str] = None
    secondary_ticker: Optional[str] = None
    company: Optional[str] = None
    theme: Optional[str] = None
    period: str = "recent"
    save_requested: bool = False
    metadata: dict = field(default_factory=dict)


def _load_watchlist(project_root: Path) -> List[dict]:
    path = project_root / "config" / "watchlist.yaml"
    data = json.loads(path.read_text(encoding="utf-8"))
    return data.get("watchlist", [])


def _extract_period(text: str) -> str:
    lowered = text.lower()
    if "today" in lowered:
        return "today"
    if "yesterday" in lowered:
        return "yesterday"
    if "last month" in lowered:
        return "last_month"
    if "last three months" in lowered or "past three months" in lowered:
        return "last_three_months"
    if "recent" in lowered or "recently" in lowered:
        return "recent"
    return "recent"


def _find_tickers(text: str, watchlist: List[dict]) -> List[str]:
    lowered = text.lower()
    found: List[str] = []
    for item in watchlist:
        ticker = item["ticker"].upper()
        company = item["company"].lower()
        if re.search(rf"\b{re.escape(ticker.lower())}\b", lowered) or company in lowered:
            found.append(ticker)
    uppercase_hits = re.findall(r"\b[A-Z]{2,5}\b", text)
    for hit in uppercase_hits:
        if hit not in found and any(item["ticker"] == hit for item in watchlist):
            found.append(hit)
    return found


def route_request(request: str, project_root: Path) -> Task:
    text = request.strip()
    lowered = text.lower()
    watchlist = _load_watchlist(project_root)
    tickers = _find_tickers(text, watchlist)

    intent = "ask"
    if "save" in lowered:
        intent = "save"
    elif "what changed" in lowered or "update" in lowered:
        intent = "update"
    elif "daily report" in lowered or "daily brief" in lowered or "market daily" in lowered:
        intent = "daily"
    elif "sec filing" in lowered or "sec filings" in lowered:
        intent = "sec"
    elif "compare" in lowered:
        intent = "compare"
    elif "theme" in lowered or "developments" in lowered:
        intent = "theme"
    elif "analyze" in lowered:
        intent = "analyze"
    elif "status" in lowered or "need research updates" in lowered:
        intent = "status"
    elif "research" in lowered:
        intent = "research"

    primary = tickers[0] if tickers else None
    secondary = tickers[1] if len(tickers) > 1 else None
    company = None
    if primary:
        for item in watchlist:
            if item["ticker"] == primary:
                company = item["company"]
                break

    theme = None
    if intent == "theme":
        theme = text

    return Task(
        raw_request=text,
        intent=intent,
        ticker=primary,
        secondary_ticker=secondary,
        company=company,
        theme=theme,
        period=_extract_period(text),
        save_requested=intent == "save",
        metadata={"watchlist_size": len(watchlist)},
    )
