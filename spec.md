# spec

## Goal
Build a tiny CLI that reads `events.csv` and writes `summary.csv` with one row per event group.

## Inputs
- Input file: `events.csv`
- Required columns:
  - `timestamp`
  - `level`
  - `service`
  - `message`
- Input format: CSV with a header row
- `timestamp` is expected in ISO 8601 date-time format

## Outputs
- Output file: `summary.csv`
- One row per event group
- Output columns:
  - `level`
  - `service`
  - `message_normalized`
  - `count`
  - `first_seen`
  - `last_seen`

## Normalisation rules
- Trim leading and trailing whitespace from all string fields before processing.
- Treat `level` as case-insensitive for grouping; write it out in uppercase in `summary.csv`.
- Treat `service` as case-sensitive after trimming.
- For message grouping, normalize `message` as follows:
  - trim leading and trailing whitespace
  - collapse repeated internal whitespace to a single space
- Do not remove numbers, IDs, punctuation, or variable-looking substrings from `message`.
- If `message` is empty after trimming, keep it as an empty string.

## Grouping rule
The exact group key is:

`(level_normalized, service_trimmed, message_normalized)`

Rows belong to the same group only if all three values above are exactly equal after normalization.

## Aggregation
For each group, calculate:
- `count`: number of rows in the group
- `first_seen`: earliest valid timestamp in the group
- `last_seen`: latest valid timestamp in the group

`first_seen` and `last_seen` must be written in ISO 8601 format.

## Edge cases
- **Missing level**
  - If `level` is empty or missing, use `UNKNOWN` as the normalized level.
- **Malformed timestamp**
  - If a row has an invalid timestamp, do not include it in aggregation.
  - The CLI must report the row as skipped.
- **Missing required column**
  - If any required column is missing from the input header, exit with an error and do not write `summary.csv`.
- **Empty input file with header only**
  - Write `summary.csv` with header only and exit successfully.
- **Completely empty file**
  - Exit with an error because the header cannot be read.
- **Duplicate rows**
  - Count them normally; no deduplication is performed.

## CLI
Command shape:

```bash
python -m src.main --input events.csv --output summary.csv
```

Required flags:
- `--input`
- `--output`

Exit codes:
- `0` = success
- `1` = validation or input error
- `2` = runtime or unexpected processing error

CLI behavior:
- If processing succeeds, create or overwrite the output file.
- If required columns are missing, do not create the output file.
- If one or more rows are skipped because of malformed timestamps, still succeed if at least the file itself is valid, and print a warning summary to stderr.

## Out of scope
- Fuzzy grouping or semantic similarity between messages
- Log parsing beyond the four input columns
- Reading non-CSV formats
- Reading multiple input files in one run
- Sorting guarantees beyond grouped output correctness
- Real-time / streaming log ingestion
- Automatic repair of malformed timestamps
- Dependency on non-standard Python libraries

## Signed off
AB — 2026-06-08
