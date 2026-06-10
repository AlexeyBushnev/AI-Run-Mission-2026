-- Build gold metrics from silver/transactions_clean.parquet

CREATE OR REPLACE VIEW silver_tx AS
SELECT *
FROM read_parquet('/mnt/data/silver/transactions_clean.parquet');

CREATE OR REPLACE TABLE daily_sales_by_category AS
SELECT
    order_date,
    region,
    product_category,
    SUM(CASE WHEN status = 'completed' THEN amount ELSE 0 END) AS total_revenue,
    COUNT(DISTINCT CASE WHEN status = 'completed' THEN order_id ELSE NULL END) AS order_count
FROM silver_tx
GROUP BY order_date, region, product_category;

CREATE OR REPLACE TABLE returns_rate AS
WITH per_day AS (
    SELECT
        order_date,
        COUNT(DISTINCT CASE WHEN status IN ('completed', 'returned') THEN order_id ELSE NULL END) AS total_orders,
        COUNT(DISTINCT CASE WHEN status = 'returned' THEN order_id ELSE NULL END) AS returned_orders
    FROM silver_tx
    GROUP BY order_date
)
SELECT
    order_date,
    total_orders,
    returned_orders,
    ROUND(COALESCE((returned_orders * 100.0) / NULLIF(total_orders, 0), 0.0), 2) AS returns_rate_pct
FROM per_day;

COPY daily_sales_by_category TO '/mnt/data/gold/daily_sales_by_category.parquet' (FORMAT PARQUET);
COPY returns_rate TO '/mnt/data/gold/returns_rate.parquet' (FORMAT PARQUET);

-- Verification queries
SELECT COUNT(*) AS total_rows,
       COUNT(DISTINCT CAST(order_date AS VARCHAR) || '|' || region || '|' || product_category) AS unique_combos
FROM daily_sales_by_category;

SELECT COUNT(*) AS total_rows
FROM returns_rate;

SELECT MIN(returns_rate_pct) AS min_returns_rate_pct,
       MAX(returns_rate_pct) AS max_returns_rate_pct
FROM returns_rate;
