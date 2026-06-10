-- Bronze profile copied from K 7.W.2
-- bronze_rows = 500
-- null_amount_rows = 25
-- duplicate_extra_rows = 15

CREATE OR REPLACE TABLE bronze_raw AS
SELECT *
FROM read_csv_auto('bronze/transactions_raw.csv', header=true, all_varchar=true);

CREATE OR REPLACE TABLE silver_clean AS
WITH typed_bronze AS (
    SELECT
        order_id,
        CAST(customer_id AS INTEGER) AS customer_id,
        region,
        order_date,
        product_category,
        TRY_CAST(amount AS DOUBLE) AS amount,
        CAST(quantity AS INTEGER) AS quantity,
        status
    FROM bronze_raw
),
non_null_amount AS (
    SELECT *
    FROM typed_bronze
    WHERE amount IS NOT NULL
),
standardized_dates AS (
    SELECT
        order_id,
        customer_id,
        region,
        CAST(
            COALESCE(
                TRY_STRPTIME(order_date, '%Y-%m-%d'),
                TRY_STRPTIME(order_date, '%d/%m/%Y'),
                TRY_STRPTIME(order_date, '%b %d %Y')
            ) AS DATE
        ) AS order_date,
        product_category,
        amount,
        quantity,
        status
    FROM non_null_amount
),
deduped AS (
    SELECT *,
           ROW_NUMBER() OVER (
               PARTITION BY order_id
               ORDER BY customer_id DESC
           ) AS rn
    FROM standardized_dates
)
SELECT
    order_id,
    customer_id,
    region,
    order_date,
    product_category,
    amount,
    quantity,
    status
FROM deduped
WHERE rn = 1;

COPY silver_clean TO 'silver/transactions_clean.parquet' (FORMAT PARQUET);

SELECT
    COUNT(*) AS silver_row_count,
    SUM(CASE WHEN amount IS NULL THEN 1 ELSE 0 END) AS null_amount_count,
    COUNT(*) - COUNT(DISTINCT order_id) AS duplicate_order_id_count
FROM silver_clean;
