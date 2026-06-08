# context-load-check

## Prompt used
Summarise the rule file you loaded, by section, and cite the filename.

## Expected answer
Loaded file: `CLAUDE.md`

- **Project context:** tiny CLI that summarises synthetic `events.csv` logs; synthetic data only.
- **Conventions:** code in `src/`, tests in `tests/`, data in `data/`.
- **Utilities to prefer:** Python 3.11 standard library first; prefer `ruff` and `pytest`.
- **Escalation gates:** stop before adding dependencies; use synthetic data only; never overwrite `spec.md` after sign-off without asking.

## Verification note
The answer should cite `CLAUDE.md` explicitly and summarise all four sections.
