# 03-scd2-verification.md

## Artifact summary

This note documents execution of the SCD Type 2 loader for Kata 7.4.

## Main artifact

- `scd2_loader.py`

## Scenario results

### 1. Initial load

```json
{
  "skipped": false,
  "row_count": 20
}
```

Observed snapshot:

```json
{
  "row_count": 20,
  "current_count": 20,
  "distinct_product_ids": 20,
  "historical_count": 0,
  "duplicate_current_count": 0,
  "top_changed": [
    [
      "PROD-001",
      1
    ],
    [
      "PROD-002",
      1
    ],
    [
      "PROD-003",
      1
    ],
    [
      "PROD-004",
      1
    ],
    [
      "PROD-005",
      1
    ]
  ],
  "old_rows": []
}
```

Verification:
- 20 rows in `dim_products`: **yes**
- all rows current after initial load: **yes**
- all `valid_to` values NULL after initial load: **yes**

### 2. First incremental load (3 category changes on 2024-06-01)

```json
{
  "changed_rows": 3,
  "skipped_rows": 0
}
```

Observed snapshot:

```json
{
  "row_count": 23,
  "current_count": 20,
  "distinct_product_ids": 20,
  "historical_count": 3,
  "duplicate_current_count": 0,
  "top_changed": [
    [
      "PROD-001",
      2
    ],
    [
      "PROD-007",
      2
    ],
    [
      "PROD-015",
      2
    ],
    [
      "PROD-002",
      1
    ],
    [
      "PROD-003",
      1
    ]
  ],
  "old_rows": [
    [
      "PROD-001",
      "Product 001",
      "Electronics",
      "2024-01-01",
      "2024-05-31",
      false
    ],
    [
      "PROD-007",
      "Product 007",
      "Garden",
      "2024-01-01",
      "2024-05-31",
      false
    ],
    [
      "PROD-015",
      "Product 015",
      "Toys",
      "2024-01-01",
      "2024-05-31",
      false
    ]
  ]
}
```

Verification:
- total rows = 23: **yes**
- exactly 3 historical rows: **yes**
- changed products show 2 versions each: **yes**
- no product_id has two rows with `is_current = TRUE`: **yes**
- old rows closed at `2024-05-31`: **yes**

### 3. Idempotency run (same 3 changes again)

```json
{
  "changed_rows": 0,
  "skipped_rows": 3
}
```

Observed snapshot:

```json
{
  "row_count": 23,
  "current_count": 20,
  "distinct_product_ids": 20,
  "historical_count": 3,
  "duplicate_current_count": 0,
  "top_changed": [
    [
      "PROD-001",
      2
    ],
    [
      "PROD-007",
      2
    ],
    [
      "PROD-015",
      2
    ],
    [
      "PROD-002",
      1
    ],
    [
      "PROD-003",
      1
    ]
  ],
  "old_rows": [
    [
      "PROD-001",
      "Product 001",
      "Electronics",
      "2024-01-01",
      "2024-05-31",
      false
    ],
    [
      "PROD-007",
      "Product 007",
      "Garden",
      "2024-01-01",
      "2024-05-31",
      false
    ],
    [
      "PROD-015",
      "Product 015",
      "Toys",
      "2024-01-01",
      "2024-05-31",
      false
    ]
  ]
}
```

Verification:
- row count remains 23 on rerun: **yes**
- no additional active duplicates created: **yes**
- same update set is skipped rather than inserted again: **yes**

### 4. Leap-year boundary check

```json
{
  "leap_first": {
    "changed_rows": 1,
    "skipped_rows": 0
  },
  "leap_old_row": [
    "PROD-002",
    "2024-02-29"
  ]
}
```

Verification:
- `2024-03-01 - 1 day = 2024-02-29`: **yes**

## Verdict

The loader implements:
- initial SCD2 load from CSV
- incremental SCD2 versioning
- idempotency guard using the natural-key version signature `(product_id, valid_from, product_category)`
- exactly one current row per natural key
- leap-year-safe date closure logic

Key kata conditions met:
- after the first incremental load: **23 rows**
- historical rows after first change set: **3**
- rerun with same change set: **still 23 rows**
- duplicate current rows: **0**
