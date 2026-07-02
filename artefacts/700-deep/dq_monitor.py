
from __future__ import annotations

import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List

import duckdb

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "dq_pipeline.duckdb"
LOCAL_ISSUES_PATH = BASE_DIR / "dq_issues.md"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def connect():
    return duckdb.connect(str(DB_PATH))


def setup_demo_data() -> None:
    if DB_PATH.exists():
        DB_PATH.unlink()
    if LOCAL_ISSUES_PATH.exists():
        LOCAL_ISSUES_PATH.unlink()
    con = connect()
    try:
        con.execute("""
            CREATE TABLE bronze_transactions (
                order_id VARCHAR,
                customer_id INTEGER,
                order_date DATE,
                product_category VARCHAR,
                amount DOUBLE,
                quantity INTEGER,
                status VARCHAR
            );
        """)
        con.execute("""
            CREATE TABLE silver_transactions (
                order_id VARCHAR,
                customer_id INTEGER,
                order_date DATE,
                product_category VARCHAR,
                amount DOUBLE,
                quantity INTEGER,
                status VARCHAR
            );
        """)
        con.execute("""
            CREATE TABLE daily_sales_by_category (
                order_date DATE,
                product_category VARCHAR,
                total_revenue DOUBLE
            );
        """)
        con.execute("""
            CREATE TABLE returns_rate (
                order_date DATE,
                product_category VARCHAR,
                returns_rate_pct DOUBLE
            );
        """)

        con.execute("""
            INSERT INTO bronze_transactions
            SELECT
                'ORD-' || LPAD(CAST(i AS VARCHAR), 5, '0') AS order_id,
                1000 + i AS customer_id,
                DATE '2026-06-26' + CAST((i % 7) AS INTEGER) AS order_date,
                CASE
                    WHEN i % 4 = 0 THEN 'Electronics'
                    WHEN i % 4 = 1 THEN 'Home'
                    WHEN i % 4 = 2 THEN 'Beauty'
                    ELSE 'Sports'
                END AS product_category,
                CASE
                    WHEN i % 5 = 0 THEN 20.0
                    WHEN i % 5 = 1 THEN 35.0
                    WHEN i % 5 = 2 THEN 40.0
                    WHEN i % 5 = 3 THEN 55.0
                    ELSE 80.0
                END AS amount,
                1 + (i % 3) AS quantity,
                CASE
                    WHEN i % 10 = 0 THEN 'returned'
                    WHEN i % 10 IN (1,2) THEN 'pending'
                    ELSE 'completed'
                END AS status
            FROM range(1, 501) tbl(i);
        """)

        con.execute("INSERT INTO silver_transactions SELECT * FROM bronze_transactions;")

        con.execute("""
            INSERT INTO daily_sales_by_category
            SELECT
                order_date,
                product_category,
                SUM(amount) AS total_revenue
            FROM silver_transactions
            WHERE status = 'completed'
            GROUP BY order_date, product_category
            ORDER BY order_date, product_category;
        """)

        con.execute("""
            INSERT INTO returns_rate
            WITH base AS (
                SELECT
                    order_date,
                    product_category,
                    SUM(CASE WHEN status = 'returned' THEN 1 ELSE 0 END) AS returned_count,
                    SUM(CASE WHEN status IN ('completed', 'returned') THEN 1 ELSE 0 END) AS eligible_count
                FROM silver_transactions
                GROUP BY order_date, product_category
            )
            SELECT
                order_date,
                product_category,
                CASE WHEN eligible_count = 0 THEN 0 ELSE (returned_count * 100.0) / eligible_count END AS returns_rate_pct
            FROM base
            ORDER BY order_date, product_category;
        """)
    finally:
        con.close()


def check_result(check_name: str, layer: str, passed: bool, expected: str, actual: str, failing_row_count: int, blast_radius: str) -> Dict:
    return {
        "check_name": check_name,
        "layer": layer,
        "status": "PASS" if passed else "FAIL",
        "expected": expected,
        "actual": actual,
        "failing_row_count": int(failing_row_count),
        "blast_radius": blast_radius,
    }


def bronze_row_volume() -> Dict:
    con = connect()
    try:
        count = con.execute("SELECT COUNT(*) FROM bronze_transactions").fetchone()[0]
        passed = 400 <= count <= 600
        return check_result("bronze_row_volume", "bronze", passed, "row count between 400 and 600", f"row_count={count}", 0 if passed else abs(count - 500), "Upstream ingestion confidence degraded; all downstream layers potentially affected.")
    finally:
        con.close()


def bronze_freshness() -> Dict:
    con = connect()
    try:
        max_date = con.execute("SELECT MAX(order_date) FROM bronze_transactions").fetchone()[0]
        cutoff = datetime(2026, 7, 2).date() - timedelta(days=7)
        passed = max_date is not None and max_date >= cutoff
        return check_result("bronze_freshness", "bronze", passed, f"max(order_date) >= {cutoff.isoformat()}", f"max(order_date)={max_date}", 0 if passed else 1, "Stale source data may invalidate silver cleansed data and all gold reports.")
    finally:
        con.close()


def silver_no_null_amount() -> Dict:
    con = connect()
    try:
        failing = con.execute("SELECT COUNT(*) FROM silver_transactions WHERE amount IS NULL").fetchone()[0]
        passed = failing == 0
        return check_result("silver_no_null_amount", "silver", passed, "COUNT(*) WHERE amount IS NULL = 0", f"null_amount_rows={failing}", failing, "Revenue and return calculations may be wrong in weekly_sales_dashboard and finance_report_api.")
    finally:
        con.close()


def silver_no_duplicate_orders() -> Dict:
    con = connect()
    try:
        total, distinct_total = con.execute("SELECT COUNT(*), COUNT(DISTINCT order_id) FROM silver_transactions").fetchone()
        failing = total - distinct_total
        passed = failing == 0
        return check_result("silver_no_duplicate_orders", "silver", passed, "COUNT(*) - COUNT(DISTINCT order_id) = 0", f"duplicate_rows={failing}", failing, "Duplicate facts can inflate downstream revenue and order counts in all gold consumers.")
    finally:
        con.close()


def silver_valid_status() -> Dict:
    con = connect()
    try:
        failing = con.execute("SELECT COUNT(*) FROM silver_transactions WHERE status NOT IN ('completed', 'returned', 'pending') OR status IS NULL").fetchone()[0]
        passed = failing == 0
        return check_result("silver_valid_status", "silver", passed, "all status values in ('completed', 'returned', 'pending')", f"invalid_status_rows={failing}", failing, "Business logic branches by status; invalid values can misroute facts into gold KPIs.")
    finally:
        con.close()


def silver_no_zero_completed() -> Dict:
    con = connect()
    try:
        failing = con.execute("SELECT COUNT(*) FROM silver_transactions WHERE status = 'completed' AND amount = 0").fetchone()[0]
        passed = failing == 0
        return check_result("silver_no_zero_completed", "silver", passed, "COUNT(*) WHERE status='completed' AND amount = 0 = 0", f"zero_amount_completed_rows={failing}", failing, "Commercially wrong completed orders will distort revenue in weekly_sales_dashboard and finance_report_api.")
    finally:
        con.close()


def gold_revenue_positive() -> Dict:
    con = connect()
    try:
        min_value = con.execute("SELECT MIN(total_revenue) FROM daily_sales_by_category").fetchone()[0]
        passed = min_value is not None and min_value > 0
        return check_result("gold_revenue_positive", "gold", passed, "MIN(total_revenue) > 0", f"min(total_revenue)={min_value}", 0 if passed else 1, "weekly_sales_dashboard and finance_report_api show invalid revenue totals.")
    finally:
        con.close()


def gold_rate_bounds() -> Dict:
    con = connect()
    try:
        min_value, max_value = con.execute("SELECT MIN(returns_rate_pct), MAX(returns_rate_pct) FROM returns_rate").fetchone()
        passed = min_value is not None and max_value is not None and min_value >= 0 and max_value <= 100
        return check_result("gold_rate_bounds", "gold", passed, "0 <= returns_rate_pct <= 100", f"min={min_value}, max={max_value}", 0 if passed else 1, "Return-rate KPI is invalid for weekly_sales_dashboard and finance_report_api.")
    finally:
        con.close()


def gold_grain() -> Dict:
    con = connect()
    try:
        total, distinct_total = con.execute("SELECT COUNT(*), COUNT(DISTINCT CAST(order_date AS VARCHAR) || '|' || product_category) FROM daily_sales_by_category").fetchone()
        passed = total == distinct_total
        failing = max(total - distinct_total, 0)
        return check_result("gold_grain", "gold", passed, "COUNT(*) = COUNT(DISTINCT order_date || '|' || product_category)", f"rows={total}, distinct_grain={distinct_total}", failing, "Duplicate gold grain causes repeated rows in weekly_sales_dashboard and finance_report_api.")
    finally:
        con.close()


def gold_silver_reconciliation() -> Dict:
    con = connect()
    try:
        gold_sum = con.execute("SELECT COALESCE(SUM(total_revenue), 0) FROM daily_sales_by_category").fetchone()[0]
        silver_sum = con.execute("SELECT COALESCE(SUM(amount), 0) FROM silver_transactions WHERE status = 'completed'").fetchone()[0]
        diff = abs(float(gold_sum) - float(silver_sum))
        passed = diff <= 0.01
        return check_result("gold_silver_reconciliation", "gold", passed, "SUM(total_revenue) equals SUM(amount) over completed silver orders within 0.01", f"gold_sum={gold_sum}, silver_sum={silver_sum}, diff={diff}", 0 if passed else 1, "All gold-facing consumers affected; revenue drift between silver and gold breaks trust in published metrics.")
    finally:
        con.close()


def issue_markdown(check_result: Dict) -> str:
    return f"""## Data Quality Failure
**Check:** {check_result['check_name']}
**Layer:** {check_result['layer']}
**Expected:** {check_result['expected']}
**Actual:** {check_result['actual']}
**Failing rows:** {check_result['failing_row_count']}
**Blast radius:** {check_result['blast_radius']}
**Timestamp:** {utc_now()}
**Next steps:**
1. Check source inputs and latest landed batch for missing, null, or malformed values.
2. Check transformation logic between layers for filter, join, or aggregation drift.
3. Check schema drift / contract expectations and confirm whether upstream structure changed.
"""


def create_github_issue(check_result: Dict, repo: str) -> Dict:
    if check_result["status"] != "FAIL":
        return {"created": False, "reason": "check passed"}

    title = f"[DQ FAIL] {check_result['check_name']} — {check_result['layer']} layer"
    body = issue_markdown(check_result)
    labels = ["bug", "data-quality", check_result["layer"]]

    token = os.environ.get("GITHUB_TOKEN")
    if token:
        import requests
        url = f"https://api.github.com/repos/{repo}/issues"
        resp = requests.post(
            url,
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github+json",
            },
            json={"title": title, "body": body, "labels": labels},
            timeout=30,
        )
        return {"created": resp.status_code == 201, "status_code": resp.status_code, "response": resp.text[:1000], "title": title}

    with LOCAL_ISSUES_PATH.open("a", encoding="utf-8") as f:
        f.write(f"# {title}\n\n")
        f.write(body)
        f.write(f"**Labels:** {', '.join(labels)}\n\n---\n\n")
    return {"created": True, "mode": "local_fallback", "title": title, "path": str(LOCAL_ISSUES_PATH)}


def all_checks() -> List[Dict]:
    return [
        bronze_row_volume(),
        bronze_freshness(),
        silver_no_null_amount(),
        silver_no_duplicate_orders(),
        silver_valid_status(),
        silver_no_zero_completed(),
        gold_revenue_positive(),
        gold_rate_bounds(),
        gold_grain(),
        gold_silver_reconciliation(),
    ]


def run_dq_monitoring(repo: str) -> Dict:
    results = all_checks()
    issues = []
    for r in results:
        if r["status"] == "FAIL":
            issues.append(create_github_issue(r, repo))
    return {"results": results, "issues": issues}


def inject_silver_null_amount_break() -> None:
    con = connect()
    try:
        con.execute("INSERT INTO silver_transactions VALUES ('ORD-99999', NULL, NULL, 'Electronics', NULL, 1, 'completed')")
    finally:
        con.close()


def delete_injected_break() -> None:
    con = connect()
    try:
        con.execute("DELETE FROM silver_transactions WHERE order_id = 'ORD-99999'")
    finally:
        con.close()


def main():
    setup_demo_data()
    clean = run_dq_monitoring("example/dq-test")
    inject_silver_null_amount_break()
    failed = run_dq_monitoring("example/dq-test")
    delete_injected_break()
    recovered = run_dq_monitoring("example/dq-test")
    print(json.dumps({"clean": clean, "failed": failed, "recovered": recovered}, indent=2))


if __name__ == "__main__":
    main()
