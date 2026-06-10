# gold-verify

## Output files
- `gold/daily_sales_by_category.parquet`
- `gold/returns_rate.parquet`

## Grain verification — daily_sales_by_category
- total rows: 454
- unique (order_date, region, product_category) combos: 454
- grain check verdict: PASS

## Returns-rate verification
- returns_rate row count: 267
- min returns_rate_pct: 0.0
- max returns_rate_pct: 100.0
- range check verdict: PASS

## Manual spot-checks (2 rows)
- 2024-01-01: total_orders=3, returned_orders=0, manual_pct=0.0, output_pct=0.0, verdict=PASS
- 2024-01-02: total_orders=1, returned_orders=0, manual_pct=0.0, output_pct=0.0, verdict=PASS

## Zero-returns edge case
- order_date: 2024-01-01
- total_orders: 3
- returned_orders: 0
- returns_rate_pct: 0.0
- zero-returns verdict: PASS

## Row counts
- daily_sales_by_category rows: 454
- returns_rate rows: 267
