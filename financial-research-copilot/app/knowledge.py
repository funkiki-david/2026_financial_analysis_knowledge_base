from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import re
from typing import Dict, Optional


@dataclass
class KnowledgeSnapshot:
    ticker: Optional[str]
    path: Optional[Path]
    exists: bool
    metadata: Dict[str, str] = field(default_factory=dict)
    sections: Dict[str, str] = field(default_factory=dict)

    @property
    def current_thesis(self) -> str:
        return self.sections.get("Current Thesis", "").strip()

    @property
    def last_updated(self) -> str:
        return self.metadata.get("last_updated", "unknown")

    @property
    def questions(self) -> str:
        return self.sections.get("Questions", "").strip()


def _parse_frontmatter(text: str) -> tuple[Dict[str, str], str]:
    metadata: Dict[str, str] = {}
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            for line in parts[1].splitlines():
                if ":" in line:
                    key, value = line.split(":", 1)
                    metadata[key.strip()] = value.strip()
            return metadata, parts[2].lstrip()
    return metadata, text


def _parse_sections(text: str) -> Dict[str, str]:
    matches = list(re.finditer(r"^##\s+(.+)$", text, flags=re.MULTILINE))
    if not matches:
        return {}

    sections: Dict[str, str] = {}
    for index, match in enumerate(matches):
        title = match.group(1).strip()
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections[title] = text[start:end].strip()
    return sections


def load_company_knowledge(project_root: Path, ticker: Optional[str]) -> KnowledgeSnapshot:
    if not ticker:
        return KnowledgeSnapshot(ticker=None, path=None, exists=False)

    path = project_root / "knowledge" / "companies" / f"{ticker.upper()}.md"
    if not path.exists():
        return KnowledgeSnapshot(ticker=ticker, path=path, exists=False)

    raw = path.read_text(encoding="utf-8")
    metadata, body = _parse_frontmatter(raw)
    sections = _parse_sections(body)
    return KnowledgeSnapshot(
        ticker=ticker,
        path=path,
        exists=True,
        metadata=metadata,
        sections=sections,
    )
