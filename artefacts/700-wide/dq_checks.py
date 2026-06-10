
def _print_result(rule_name, fail_count, example_query=None, con=None):
    if fail_count == 0:
        print(f"PASS - {rule_name}")
    else:
        print(f"FAIL - {rule_name} | failing_row_count={fail_count}")
        if example_query and con is not None:
            rows = con.execute(example_query).fetchall()
            if rows:
                print(f"  examples={rows}")

def check_1_no_null_keys_in_sales(con):
    cnt = con.execute("""
    SELECT COUNT(*) FROM gold_sales
    WHERE order_date IS NULL OR region IS NULL OR product_category IS NULL
    """).fetchone()[0]
    _print_result("1. daily_sales: no null order_date/region/product_category", cnt,
                  "SELECT * FROM gold_sales WHERE order_date IS NULL OR region IS NULL OR product_category IS NULL LIMIT 3", con)
    return cnt == 0

def check_2_positive_revenue(con):
    cnt = con.execute("SELECT COUNT(*) FROM gold_sales WHERE total_revenue <= 0").fetchone()[0]
    _print_result("2. daily_sales: total_revenue > 0", cnt,
                  "SELECT order_date, region, product_category, total_revenue FROM gold_sales WHERE total_revenue <= 0 LIMIT 3", con)
    return cnt == 0

def check_3_positive_order_count(con):
    cnt = con.execute("SELECT COUNT(*) FROM gold_sales WHERE order_count <= 0").fetchone()[0]
    _print_result("3. daily_sales: order_count > 0", cnt,
                  "SELECT order_date, region, product_category, order_count FROM gold_sales WHERE order_count <= 0 LIMIT 3", con)
    return cnt == 0

def check_4_unique_grain(con):
    cnt = con.execute("""
    WITH d AS (
      SELECT order_date, region, product_category, COUNT(*) c
      FROM gold_sales
      GROUP BY 1,2,3
      HAVING COUNT(*) > 1
    )
    SELECT COUNT(*) FROM d
    """).fetchone()[0]
    _print_result("4. daily_sales: no duplicate (order_date, region, product_category)", cnt,
                  "SELECT order_date, region, product_category, COUNT(*) c FROM gold_sales GROUP BY 1,2,3 HAVING COUNT(*) > 1 LIMIT 3", con)
    return cnt == 0

def check_5_no_null_order_date_returns(con):
    cnt = con.execute("SELECT COUNT(*) FROM gold_returns WHERE order_date IS NULL").fetchone()[0]
    _print_result("5. returns_rate: no null order_date", cnt,
                  "SELECT * FROM gold_returns WHERE order_date IS NULL LIMIT 3", con)
    return cnt == 0

def check_6_returns_rate_range(con):
    cnt = con.execute("SELECT COUNT(*) FROM gold_returns WHERE returns_rate_pct < 0.0 OR returns_rate_pct > 100.0 OR returns_rate_pct IS NULL").fetchone()[0]
    _print_result("6. returns_rate: returns_rate_pct between 0 and 100 inclusive", cnt,
                  "SELECT order_date, returns_rate_pct FROM gold_returns WHERE returns_rate_pct < 0.0 OR returns_rate_pct > 100.0 OR returns_rate_pct IS NULL LIMIT 3", con)
    return cnt == 0

def check_7_returned_lte_total(con):
    cnt = con.execute("SELECT COUNT(*) FROM gold_returns WHERE returned_orders > total_orders").fetchone()[0]
    _print_result("7. returns_rate: returned_orders <= total_orders", cnt,
                  "SELECT order_date, total_orders, returned_orders FROM gold_returns WHERE returned_orders > total_orders LIMIT 3", con)
    return cnt == 0

def check_8_date_span(con):
    span = con.execute("SELECT DATE_DIFF('day', MIN(order_date), MAX(order_date)) FROM gold_returns").fetchone()[0]
    if span is not None and span >= 30:
        print(f"PASS - 8. returns_rate: order_date range spans at least 30 days | span_days={span}")
        return True
    print(f"FAIL - 8. returns_rate: order_date range spans at least 30 days | span_days={span}")
    return False

def run_all_checks(con):
    results = [
        check_1_no_null_keys_in_sales(con),
        check_2_positive_revenue(con),
        check_3_positive_order_count(con),
        check_4_unique_grain(con),
        check_5_no_null_order_date_returns(con),
        check_6_returns_rate_range(con),
        check_7_returned_lte_total(con),
        check_8_date_span(con),
    ]
    passed = sum(1 for r in results if r)
    print(f"{passed}/8 checks passed")
    return passed
