# dq-certificate

## Clean run
```text
PASS - 1. daily_sales: no null order_date/region/product_category
FAIL - 2. daily_sales: total_revenue > 0 | failing_row_count=8
  examples=[(datetime.date(2024, 4, 3), 'East', 'Clothing', -25.6), (datetime.date(2024, 12, 1), 'West', 'Sports', -10.6), (datetime.date(2024, 4, 8), 'South', 'Sports', -10.54)]
PASS - 3. daily_sales: order_count > 0
PASS - 4. daily_sales: no duplicate (order_date, region, product_category)
PASS - 5. returns_rate: no null order_date
PASS - 6. returns_rate: returns_rate_pct between 0 and 100 inclusive
PASS - 7. returns_rate: returned_orders <= total_orders
PASS - 8. returns_rate: order_date range spans at least 30 days | span_days=365
7/8 checks passed
```

## Break-and-verify run
Injected bad row:
`DATE '2024-01-01', 'North', 'Electronics', -999.99, 5`

```text
PASS - 1. daily_sales: no null order_date/region/product_category
FAIL - 2. daily_sales: total_revenue > 0 | failing_row_count=9
  examples=[(datetime.date(2024, 4, 3), 'East', 'Clothing', -25.6), (datetime.date(2024, 12, 1), 'West', 'Sports', -10.6), (datetime.date(2024, 4, 8), 'South', 'Sports', -10.54)]
PASS - 3. daily_sales: order_count > 0
PASS - 4. daily_sales: no duplicate (order_date, region, product_category)
PASS - 5. returns_rate: no null order_date
PASS - 6. returns_rate: returns_rate_pct between 0 and 100 inclusive
PASS - 7. returns_rate: returned_orders <= total_orders
PASS - 8. returns_rate: order_date range spans at least 30 days | span_days=365
7/8 checks passed
```

## Cleanup and re-pass
```text
PASS - 1. daily_sales: no null order_date/region/product_category
FAIL - 2. daily_sales: total_revenue > 0 | failing_row_count=8
  examples=[(datetime.date(2024, 4, 3), 'East', 'Clothing', -25.6), (datetime.date(2024, 12, 1), 'West', 'Sports', -10.6), (datetime.date(2024, 4, 8), 'South', 'Sports', -10.54)]
PASS - 3. daily_sales: order_count > 0
PASS - 4. daily_sales: no duplicate (order_date, region, product_category)
PASS - 5. returns_rate: no null order_date
PASS - 6. returns_rate: returns_rate_pct between 0 and 100 inclusive
PASS - 7. returns_rate: returned_orders <= total_orders
PASS - 8. returns_rate: order_date range spans at least 30 days | span_days=365
7/8 checks passed
```

## Verdict
- Clean gold data pass status: 7/8
- Injected bad-row run: expected FAIL on check #2 and observed YES
- Re-pass after cleanup: 7/8
