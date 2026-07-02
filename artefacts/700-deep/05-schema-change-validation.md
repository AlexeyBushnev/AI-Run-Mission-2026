# 05-schema-change-validation.md

## Migration / rollback test summary

This note records the DuckDB dry run for the schema-change management runbook.

## Files

- `schema-change-runbook-v1.md`
- `05-schema-change-test.sql`

## Migration verification

- Added `order_total_usd`
- Added `currency_code`
- Created compatibility view `v_gold_daily_sales_compat`

### Compatibility view rows

```json
[
  [
    "2026-06-29",
    "Electronics",
    12345,
    123.45,
    "USD"
  ],
  [
    "2026-06-29",
    "Home",
    4500,
    45.0,
    "USD"
  ],
  [
    "2026-06-30",
    "Beauty",
    999,
    9.99,
    "USD"
  ]
]
```

Interpretation:
- `amount_cents` remains available through the compatibility view
- `order_total_usd` is available for migrated consumers
- `currency_code` is present

## Post-drop verification

Columns after simulated drop:

```json
[
  "order_date",
  "product_category",
  "order_total_usd",
  "currency_code"
]
```

Expected: `amount_cents` removed

## Rollback verification

Rows after rollback:

```json
[
  [
    "2026-06-29",
    "Electronics",
    12345
  ],
  [
    "2026-06-29",
    "Home",
    4500
  ],
  [
    "2026-06-30",
    "Beauty",
    999
  ]
]
```

Columns after rollback:

```json
[
  "order_date",
  "product_category",
  "amount_cents"
]
```

Rollback restored original cents values correctly:
**True**

## Verdict

- impact analysis covers direct and indirect consumers
- compatibility view pattern works
- deprecation window is 6 weeks
- rollback is SQL-based and executable
- rollback path is suitable for sub-10-minute execution on a moderate table
