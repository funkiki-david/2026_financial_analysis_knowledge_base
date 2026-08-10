from __future__ import annotations

from pathlib import Path

from .researcher import ResearchResult, research
from .router import route_request
from .writer import render_cli_report, save_research


def _project_root() -> Path:
    return Path(__file__).resolve().parent.parent


def main() -> None:
    project_root = _project_root()
    last_result: ResearchResult | None = None

    print("Financial Research Copilot v0.1")
    print("Type a research request, 'save this research to the knowledge base', or 'exit'.")

    while True:
        try:
            user_input = input("\n> ").strip()
        except EOFError:
            print()
            break

        if not user_input:
            continue
        if user_input.lower() in {"exit", "quit"}:
            break

        task = route_request(user_input, project_root)
        if task.intent == "save":
            if last_result is None:
                print("No in-memory research result is available yet. Run a research request first.")
                continue
            saved_path = save_research(last_result, project_root)
            print(f"Saved research to {saved_path}")
            continue

        result = research(task, project_root)
        last_result = result
        print(render_cli_report(result))


if __name__ == "__main__":
    main()
