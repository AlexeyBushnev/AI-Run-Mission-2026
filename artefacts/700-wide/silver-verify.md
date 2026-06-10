# silver-verify

## Bronze baseline
- bronze row count: 500
- null `amount` rows: 25
- duplicate extra rows by `order_id`: 15

## Cleaning rules applied
- removed rows where `amount IS NULL`
- standardized `order_date` to `DATE` using three input formats
- deduplicated by `order_id`, keeping the highest `customer_id`
- preserved negative `amount` rows as valid returns

## Silver verification
- silver row count: 460
- null `amount` count: 0
- duplicate `order_id` count: 0
- null `order_date` count after parsing: 0
- negative `amount` rows preserved: 10

## Row-count math
- expected silver rows = bronze rows - null amount rows - duplicate extra rows
- expected = 500 - 25 - 15 = 460
- actual silver rows = 460
- difference = 0
- percent off expected = 0.00%

## Verdict
- Row-count math check: PASS
- No null amounts remaining: PASS
- One row per `order_id`: PASS
- `order_date` standardized to DATE without null parses: PASS

## Note
- `clean_transactions.sql` contains the intended DuckDB SQL for the notebook.
- `silver/transactions_clean.parquet` was materialized successfully.
