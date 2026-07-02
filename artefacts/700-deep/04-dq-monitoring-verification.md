# 04-dq-monitoring-verification.md

## Artifact summary

This note documents execution of the DQ monitoring system for Kata 7.5.

## Main artifact

- `dq_monitor.py`

## GitHub token mode

`GITHUB_TOKEN` available in runtime: **False**

Because no token was available in this environment, the module used the kata-allowed fallback and wrote issue content to `dq_issues.md` instead of calling the GitHub API.

## Scenario results

### 1. Clean data run

```json
{
  "results": [
    {
      "check_name": "bronze_row_volume",
      "layer": "bronze",
      "status": "PASS",
      "expected": "row count between 400 and 600",
      "actual": "row_count=500",
      "failing_row_count": 0,
      "blast_radius": "Upstream ingestion confidence degraded; all downstream layers potentially affected."
    },
    {
      "check_name": "bronze_freshness",
      "layer": "bronze",
      "status": "PASS",
      "expected": "max(order_date) >= 2026-06-25",
      "actual": "max(order_date)=2026-07-02",
      "failing_row_count": 0,
      "blast_radius": "Stale source data may invalidate silver cleansed data and all gold reports."
    },
    {
      "check_name": "silver_no_null_amount",
      "layer": "silver",
      "status": "PASS",
      "expected": "COUNT(*) WHERE amount IS NULL = 0",
      "actual": "null_amount_rows=0",
      "failing_row_count": 0,
      "blast_radius": "Revenue and return calculations may be wrong in weekly_sales_dashboard and finance_report_api."
    },
    {
      "check_name": "silver_no_duplicate_orders",
      "layer": "silver",
      "status": "PASS",
      "expected": "COUNT(*) - COUNT(DISTINCT order_id) = 0",
      "actual": "duplicate_rows=0",
      "failing_row_count": 0,
      "blast_radius": "Duplicate facts can inflate downstream revenue and order counts in all gold consumers."
    },
    {
      "check_name": "silver_valid_status",
      "layer": "silver",
      "status": "PASS",
      "expected": "all status values in ('completed', 'returned', 'pending')",
      "actual": "invalid_status_rows=0",
      "failing_row_count": 0,
      "blast_radius": "Business logic branches by status; invalid values can misroute facts into gold KPIs."
    },
    {
      "check_name": "silver_no_zero_completed",
      "layer": "silver",
      "status": "PASS",
      "expected": "COUNT(*) WHERE status='completed' AND amount = 0 = 0",
      "actual": "zero_amount_completed_rows=0",
      "failing_row_count": 0,
      "blast_radius": "Commercially wrong completed orders will distort revenue in weekly_sales_dashboard and finance_report_api."
    },
    {
      "check_name": "gold_revenue_positive",
      "layer": "gold",
      "status": "PASS",
      "expected": "MIN(total_revenue) > 0",
      "actual": "min(total_revenue)=565.0",
      "failing_row_count": 0,
      "blast_radius": "weekly_sales_dashboard and finance_report_api show invalid revenue totals."
    },
    {
      "check_name": "gold_rate_bounds",
      "layer": "gold",
      "status": "PASS",
      "expected": "0 <= returns_rate_pct <= 100",
      "actual": "min=0.0, max=28.571428571428573",
      "failing_row_count": 0,
      "blast_radius": "Return-rate KPI is invalid for weekly_sales_dashboard and finance_report_api."
    },
    {
      "check_name": "gold_grain",
      "layer": "gold",
      "status": "PASS",
      "expected": "COUNT(*) = COUNT(DISTINCT order_date || '|' || product_category)",
      "actual": "rows=28, distinct_grain=28",
      "failing_row_count": 0,
      "blast_radius": "Duplicate gold grain causes repeated rows in weekly_sales_dashboard and finance_report_api."
    },
    {
      "check_name": "gold_silver_reconciliation",
      "layer": "gold",
      "status": "PASS",
      "expected": "SUM(total_revenue) equals SUM(amount) over completed silver orders within 0.01",
      "actual": "gold_sum=18250.0, silver_sum=18250.0, diff=0.0",
      "failing_row_count": 0,
      "blast_radius": "All gold-facing consumers affected; revenue drift between silver and gold breaks trust in published metrics."
    }
  ],
  "issues": []
}
```

Verification:
- all 10 checks PASS: **yes**
- no issues created: **yes**

### 2. Forced silver failure

Injected row:
```sql
INSERT INTO silver_transactions VALUES ('ORD-99999', NULL, NULL, 'Electronics', NULL, 1, 'completed');
```

```json
{
  "results": [
    {
      "check_name": "bronze_row_volume",
      "layer": "bronze",
      "status": "PASS",
      "expected": "row count between 400 and 600",
      "actual": "row_count=500",
      "failing_row_count": 0,
      "blast_radius": "Upstream ingestion confidence degraded; all downstream layers potentially affected."
    },
    {
      "check_name": "bronze_freshness",
      "layer": "bronze",
      "status": "PASS",
      "expected": "max(order_date) >= 2026-06-25",
      "actual": "max(order_date)=2026-07-02",
      "failing_row_count": 0,
      "blast_radius": "Stale source data may invalidate silver cleansed data and all gold reports."
    },
    {
      "check_name": "silver_no_null_amount",
      "layer": "silver",
      "status": "FAIL",
      "expected": "COUNT(*) WHERE amount IS NULL = 0",
      "actual": "null_amount_rows=1",
      "failing_row_count": 1,
      "blast_radius": "Revenue and return calculations may be wrong in weekly_sales_dashboard and finance_report_api."
    },
    {
      "check_name": "silver_no_duplicate_orders",
      "layer": "silver",
      "status": "PASS",
      "expected": "COUNT(*) - COUNT(DISTINCT order_id) = 0",
      "actual": "duplicate_rows=0",
      "failing_row_count": 0,
      "blast_radius": "Duplicate facts can inflate downstream revenue and order counts in all gold consumers."
    },
    {
      "check_name": "silver_valid_status",
      "layer": "silver",
      "status": "PASS",
      "expected": "all status values in ('completed', 'returned', 'pending')",
      "actual": "invalid_status_rows=0",
      "failing_row_count": 0,
      "blast_radius": "Business logic branches by status; invalid values can misroute facts into gold KPIs."
    },
    {
      "check_name": "silver_no_zero_completed",
      "layer": "silver",
      "status": "PASS",
      "expected": "COUNT(*) WHERE status='completed' AND amount = 0 = 0",
      "actual": "zero_amount_completed_rows=0",
      "failing_row_count": 0,
      "blast_radius": "Commercially wrong completed orders will distort revenue in weekly_sales_dashboard and finance_report_api."
    },
    {
      "check_name": "gold_revenue_positive",
      "layer": "gold",
      "status": "PASS",
      "expected": "MIN(total_revenue) > 0",
      "actual": "min(total_revenue)=565.0",
      "failing_row_count": 0,
      "blast_radius": "weekly_sales_dashboard and finance_report_api show invalid revenue totals."
    },
    {
      "check_name": "gold_rate_bounds",
      "layer": "gold",
      "status": "PASS",
      "expected": "0 <= returns_rate_pct <= 100",
      "actual": "min=0.0, max=28.571428571428573",
      "failing_row_count": 0,
      "blast_radius": "Return-rate KPI is invalid for weekly_sales_dashboard and finance_report_api."
    },
    {
      "check_name": "gold_grain",
      "layer": "gold",
      "status": "PASS",
      "expected": "COUNT(*) = COUNT(DISTINCT order_date || '|' || product_category)",
      "actual": "rows=28, distinct_grain=28",
      "failing_row_count": 0,
      "blast_radius": "Duplicate gold grain causes repeated rows in weekly_sales_dashboard and finance_report_api."
    },
    {
      "check_name": "gold_silver_reconciliation",
      "layer": "gold",
      "status": "PASS",
      "expected": "SUM(total_revenue) equals SUM(amount) over completed silver orders within 0.01",
      "actual": "gold_sum=18250.0, silver_sum=18250.0, diff=0.0",
      "failing_row_count": 0,
      "blast_radius": "All gold-facing consumers affected; revenue drift between silver and gold breaks trust in published metrics."
    }
  ],
  "issues": [
    {
      "created": true,
      "mode": "local_fallback",
      "title": "[DQ FAIL] silver_no_null_amount \u2014 silver layer",
      "path": "/mnt/data/700_kata_7_5/dq_issues.md"
    }
  ]
}
```

Verification:
- `silver_no_null_amount` fails: **yes**
- issue created with context: **yes**

### 3. Recovery run after fix

```json
{
  "results": [
    {
      "check_name": "bronze_row_volume",
      "layer": "bronze",
      "status": "PASS",
      "expected": "row count between 400 and 600",
      "actual": "row_count=500",
      "failing_row_count": 0,
      "blast_radius": "Upstream ingestion confidence degraded; all downstream layers potentially affected."
    },
    {
      "check_name": "bronze_freshness",
      "layer": "bronze",
      "status": "PASS",
      "expected": "max(order_date) >= 2026-06-25",
      "actual": "max(order_date)=2026-07-02",
      "failing_row_count": 0,
      "blast_radius": "Stale source data may invalidate silver cleansed data and all gold reports."
    },
    {
      "check_name": "silver_no_null_amount",
      "layer": "silver",
      "status": "PASS",
      "expected": "COUNT(*) WHERE amount IS NULL = 0",
      "actual": "null_amount_rows=0",
      "failing_row_count": 0,
      "blast_radius": "Revenue and return calculations may be wrong in weekly_sales_dashboard and finance_report_api."
    },
    {
      "check_name": "silver_no_duplicate_orders",
      "layer": "silver",
      "status": "PASS",
      "expected": "COUNT(*) - COUNT(DISTINCT order_id) = 0",
      "actual": "duplicate_rows=0",
      "failing_row_count": 0,
      "blast_radius": "Duplicate facts can inflate downstream revenue and order counts in all gold consumers."
    },
    {
      "check_name": "silver_valid_status",
      "layer": "silver",
      "status": "PASS",
      "expected": "all status values in ('completed', 'returned', 'pending')",
      "actual": "invalid_status_rows=0",
      "failing_row_count": 0,
      "blast_radius": "Business logic branches by status; invalid values can misroute facts into gold KPIs."
    },
    {
      "check_name": "silver_no_zero_completed",
      "layer": "silver",
      "status": "PASS",
      "expected": "COUNT(*) WHERE status='completed' AND amount = 0 = 0",
      "actual": "zero_amount_completed_rows=0",
      "failing_row_count": 0,
      "blast_radius": "Commercially wrong completed orders will distort revenue in weekly_sales_dashboard and finance_report_api."
    },
    {
      "check_name": "gold_revenue_positive",
      "layer": "gold",
      "status": "PASS",
      "expected": "MIN(total_revenue) > 0",
      "actual": "min(total_revenue)=565.0",
      "failing_row_count": 0,
      "blast_radius": "weekly_sales_dashboard and finance_report_api show invalid revenue totals."
    },
    {
      "check_name": "gold_rate_bounds",
      "layer": "gold",
      "status": "PASS",
      "expected": "0 <= returns_rate_pct <= 100",
      "actual": "min=0.0, max=28.571428571428573",
      "failing_row_count": 0,
      "blast_radius": "Return-rate KPI is invalid for weekly_sales_dashboard and finance_report_api."
    },
    {
      "check_name": "gold_grain",
      "layer": "gold",
      "status": "PASS",
      "expected": "COUNT(*) = COUNT(DISTINCT order_date || '|' || product_category)",
      "actual": "rows=28, distinct_grain=28",
      "failing_row_count": 0,
      "blast_radius": "Duplicate gold grain causes repeated rows in weekly_sales_dashboard and finance_report_api."
    },
    {
      "check_name": "gold_silver_reconciliation",
      "layer": "gold",
      "status": "PASS",
      "expected": "SUM(total_revenue) equals SUM(amount) over completed silver orders within 0.01",
      "actual": "gold_sum=18250.0, silver_sum=18250.0, diff=0.0",
      "failing_row_count": 0,
      "blast_radius": "All gold-facing consumers affected; revenue drift between silver and gold breaks trust in published metrics."
    }
  ],
  "issues": []
}
```

Verification:
- all checks PASS again: **yes**
- no new issue created on recovery: **yes**

## Local issue output

```markdown
# [DQ FAIL] silver_no_null_amount — silver layer

## Data Quality Failure
**Check:** silver_no_null_amount
**Layer:** silver
**Expected:** COUNT(*) WHERE amount IS NULL = 0
**Actual:** null_amount_rows=1
**Failing rows:** 1
**Blast radius:** Revenue and return calculations may be wrong in weekly_sales_dashboard and finance_report_api.
**Timestamp:** 2026-07-02T13:37:08.041036+00:00
**Next steps:**
1. Check source inputs and latest landed batch for missing, null, or malformed values.
2. Check transformation logic between layers for filter, join, or aggregation drift.
3. Check schema drift / contract expectations and confirm whether upstream structure changed.
**Labels:** bug, data-quality, silver

---


```

## Verdict

The module implements:
- 10 DQ checks across bronze, silver, and gold
- structured result payloads with `check_name`, `layer`, `status`, `expected`, `actual`, `failing_row_count`, `blast_radius`
- auto-ticket creation on failure
- GitHub-token path using `os.environ.get('GITHUB_TOKEN')`
- local fallback issue creation when no token is available
- issue body with RCA context sufficient for on-call triage
