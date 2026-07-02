# 01-ingestion-verification.md

## Artifact summary

This verification note documents execution of the DuckDB ingestion module for Kata 7.2.

## Main artifact

- `ingestion_module.py`

## Scenario results

### 1. Clean run

```json
{
  "result": {
    "valid_rows": 8,
    "invalid_rows": 0,
    "checkpoint": "/mnt/data/700_kata_7_2/checkpoints/last_successful.json"
  },
  "bronze_count": 8,
  "checkpoint_exists": true,
  "dead_letter_files": 0
}
```

Verification:
- bronze table loaded: **yes**
- checkpoint written: **yes**
- dead-letter directory empty: **yes**

### 2. Schema failure

```json
{
  "raised": true,
  "message": "Schema validation failed: missing columns ['order_id']",
  "bronze_count": 0,
  "checkpoint_exists": false
}
```

Verification:
- schema failure raised clearly: **yes**
- no data written to bronze: **yes**
- no checkpoint written: **yes**

### 3. Dead-letter routing

```json
{
  "result": {
    "valid_rows": 3,
    "invalid_rows": 5,
    "checkpoint": "/mnt/data/700_kata_7_2/checkpoints/last_successful.json"
  },
  "bronze_count": 3,
  "dead_letter_file": "/mnt/data/700_kata_7_2/dead_letter/rejected_20260702T063603.csv",
  "dead_letter_count": 5,
  "reasons": [
    "null order_id"
  ]
}
```

Verification:
- 5 invalid rows routed to dead letter: **yes**
- rejection reason = `null order_id`: **yes**
- remaining valid rows loaded to bronze: **yes**

### 4. Retry with exponential backoff

```json
{
  "result": {
    "valid_rows": 8,
    "invalid_rows": 0,
    "checkpoint": "/mnt/data/700_kata_7_2/checkpoints/last_successful.json"
  },
  "bronze_count": 8,
  "checkpoint_exists": true
}
```

Verification:
- retry fired at least once: **yes**
- ingestion succeeded on retry: **yes**
- checkpoint written after success: **yes**

## Checkpoint file content

```json
{
  "batch_id": "batch_20260702T063609",
  "timestamp": "2026-07-02T06:36:09.250741",
  "row_count": 8,
  "source_file_hash": "91f3d395292da78769bba3ff7364ea10"
}
```

## Log excerpt

```text
2026-07-02 06:36:03,204 INFO Batch start
2026-07-02 06:36:03,204 WARNING Transient source read failure on attempt 1/3. Retrying in 2s. Error: Source file not found: /mnt/data/700_kata_7_2/source/transactions_batch.csv
2026-07-02 06:36:05,204 WARNING Transient source read failure on attempt 2/3. Retrying in 4s. Error: Source file not found: /mnt/data/700_kata_7_2/source/transactions_batch.csv
2026-07-02 06:36:09,205 INFO Volume validation passed for 8 rows
2026-07-02 06:36:09,205 INFO Freshness validation passed with latest order_date=2026-06-30
2026-07-02 06:36:09,205 INFO Dead-letter count: 0
2026-07-02 06:36:09,250 INFO Loaded 8 valid rows to bronze table bronze_transactions
2026-07-02 06:36:09,251 INFO Checkpoint written: /mnt/data/700_kata_7_2/checkpoints/last_successful.json

```

## Verdict

The module implements and verifies:
- validation at ingress
- schema rejection before persistence
- dead-letter routing before bronze insert
- retry with exponential backoff using `2 ** attempt`
- checkpoint writing only after successful load
- structured logging with Python's `logging` module

One practical caveat: this is a local file-based simulation rather than an HTTP connector, which is acceptable for the kata's allowed setup.
