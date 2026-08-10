# Financial Research Copilot v0.1

Minimal personal financial research knowledge system.

Core loop:

```text
Natural language -> Research -> Analyze -> Markdown -> GitHub Knowledge Base
```

This prototype is intentionally small. It focuses on a CLI workflow and a basic research loop instead of dashboards, databases, or heavy infrastructure.

## Structure

```text
financial-research-copilot/
├── README.md
├── config/
│   ├── sources.yaml
│   └── watchlist.yaml
├── knowledge/
│   ├── companies/
│   ├── market/
│   └── themes/
├── reports/
│   ├── daily/
│   └── weekly/
├── sources/
└── app/
    ├── __init__.py
    ├── knowledge.py
    ├── main.py
    ├── researcher.py
    ├── router.py
    └── writer.py
```

## Run

From this directory:

```bash
python3 -m app.main
```

Example prompt:

```text
What changed with NVDA today?
```

The system will:

1. classify the request,
2. load existing company knowledge if available,
3. search recent SEC filings and current news,
4. produce a structured research response,
5. keep the result in memory,
6. wait for an explicit save instruction.

Example save request in the same session:

```text
Save this research to the knowledge base.
```

## Notes

- `config/*.yaml` are stored as JSON-compatible YAML so the prototype does not require PyYAML.
- Research uses lightweight public web access:
  - SEC EDGAR submissions JSON
  - Company IR links from config
  - Google News RSS search
- This is a V0.1 prototype. It does not try to be exhaustive or production-grade.

## Limits

- No authentication
- No database
- No vector search
- No auto-save on research
- No automatic git commit/push unless you wire that into your own workflow
