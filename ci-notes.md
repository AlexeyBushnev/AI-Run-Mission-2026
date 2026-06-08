# ci-notes

## Workflow file
`.github/workflows/ci.yml`

## Expected checks
- `ruff check .`
- `pytest -v`

## Red → green record

### First CI result
- Status: RED
- Cause:
- Classification: code bug / test bug / workflow bug
- Evidence: paste the failing job step or error message here

### Fix applied
- What changed:
- Why this was the correct fix:
- Why weaker fixes were rejected (for example deleting a valid test):

### Second CI result
- Status: GREEN
- Evidence: paste the passing job summary or link here

## PR evidence
- Branch:
- PR title:
- What ran:
- What changed after CI failed:
