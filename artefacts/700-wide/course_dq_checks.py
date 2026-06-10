import duckdb

def run_all_checks(con):
    checks = [
        ("silver: no null completion_pct", "SELECT COUNT(*) FROM silver_clean WHERE completion_pct IS NULL"),
        ("silver: no duplicate event_id", "SELECT COUNT(*) FROM (SELECT event_id, COUNT(*) c FROM silver_clean GROUP BY 1 HAVING COUNT(*) > 1)"),
        ("silver: completion_pct between 0 and 100", "SELECT COUNT(*) FROM silver_clean WHERE completion_pct < 0 OR completion_pct > 100"),
        ("gold daily: no null event_date/category", "SELECT COUNT(*) FROM daily_completions_by_category WHERE event_date IS NULL OR course_category IS NULL"),
        ("gold daily: unique (event_date, course_category)", "SELECT COUNT(*) FROM (SELECT event_date, course_category, COUNT(*) c FROM daily_completions_by_category GROUP BY 1,2 HAVING COUNT(*) > 1)"),
        ("gold dropout: dropout_rate_pct between 0 and 100", "SELECT COUNT(*) FROM dropout_rate WHERE dropout_rate_pct < 0 OR dropout_rate_pct > 100 OR dropout_rate_pct IS NULL"),
    ]
    passed = 0
    for name, q in checks:
        fail_count = con.execute(q).fetchone()[0]
        if fail_count == 0:
            print(f"PASS - {name}")
            passed += 1
        else:
            print(f"FAIL - {name} | failing_row_count={fail_count}")
    print(f"{passed}/6 checks passed")
