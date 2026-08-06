# Contributing Guide

This repository is primarily a personal financial research knowledge base, but the same rules help whether changes come from manual editing, Codex, or future collaborators.

## Core Rules

- Do not overwrite existing research files unless the update is intentional and reviewed.
- Keep raw inputs and finished notes separate.
- Prefer templates and framework documents over one-off note formats.
- Record dates, sources, assumptions, and follow-up questions whenever possible.

## Recommended Workflow

1. Add raw material to `90_Inbox/incoming/` or save it with `scripts/kb_capture.sh`.
2. Promote useful material into the proper section with `scripts/kb_promote.sh`.
3. Update framework or template files only when the change will improve repeatability.
4. Review the diff before committing.

## Branching

- Use `main` for the stable latest version.
- Create a feature branch before making changes.
- Keep commits focused and easy to understand.

## Content Standards

- Prefer Markdown.
- Use clear titles.
- Keep company notes, review notes, and methodology notes in separate files.
- Distinguish facts, interpretations, and open questions.

## Verification

Before committing:

- Check links and file paths when you add documentation.
- Confirm scripts still run without syntax errors.
- Confirm no existing file was unintentionally replaced.
