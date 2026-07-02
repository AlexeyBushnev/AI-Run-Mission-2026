
-- schema-change test harness
CREATE OR REPLACE TABLE gold_daily_sales (
    order_date DATE,
    product_category VARCHAR,
    amount_cents INTEGER
);

INSERT INTO gold_daily_sales VALUES
    (DATE '2026-06-29', 'Electronics', 12345),
    (DATE '2026-06-29', 'Home', 4500),
    (DATE '2026-06-30', 'Beauty', 999);

-- Step 1: add new column and backfill from amount_cents / 100.0
ALTER TABLE gold_daily_sales ADD COLUMN order_total_usd DOUBLE;
UPDATE gold_daily_sales
SET order_total_usd = amount_cents / 100.0
WHERE order_total_usd IS NULL;

-- Step 2: add currency_code with default USD and backfill
ALTER TABLE gold_daily_sales ADD COLUMN currency_code VARCHAR DEFAULT 'USD';
UPDATE gold_daily_sales
SET currency_code = COALESCE(currency_code, 'USD');

-- Step 3: create compatibility view exposing both old and new names during deprecation
CREATE OR REPLACE VIEW v_gold_daily_sales_compat AS
SELECT
    order_date,
    product_category,
    CAST(ROUND(order_total_usd * 100) AS INTEGER) AS amount_cents,
    order_total_usd,
    currency_code
FROM gold_daily_sales;

-- Verification after migration
CREATE OR REPLACE TABLE verify_migration AS
SELECT * FROM v_gold_daily_sales_compat ORDER BY order_date, product_category;

-- Simulate end-of-window drop by recreating table without amount_cents
CREATE OR REPLACE TABLE gold_daily_sales_post_drop AS
SELECT
    order_date,
    product_category,
    order_total_usd,
    currency_code
FROM gold_daily_sales;

DROP VIEW v_gold_daily_sales_compat;

-- Rollback under 10-minute SQL-only plan:
-- restore amount_cents from order_total_usd * 100 and restore original shape
CREATE OR REPLACE TABLE gold_daily_sales_rollback AS
SELECT
    order_date,
    product_category,
    CAST(ROUND(order_total_usd * 100) AS INTEGER) AS amount_cents
FROM gold_daily_sales_post_drop;

CREATE OR REPLACE TABLE verify_rollback AS
SELECT * FROM gold_daily_sales_rollback ORDER BY order_date, product_category;
