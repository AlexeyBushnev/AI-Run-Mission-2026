# CLAUDE.md

## Project context
Tiny CLI that summarises synthetic `events.csv` logs.
No real or customer data; synthetic data only.

## Conventions
Code lives in `src/`.
Tests live in `tests/`.
Sample data lives in `data/`.

## Utilities to prefer
Use Python 3.11 standard library first.
Prefer `ruff` for linting and `pytest` for tests.

## Escalation gates
Stop before adding dependencies.
Use synthetic data only.
Never overwrite `spec.md` after sign-off without asking.

Line count: 18
