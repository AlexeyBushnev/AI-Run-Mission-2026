-- Schema version: 1.0.0 | Created: 2026-07-02 | Approved by: Aleksei Bushnev

-- gold_daily_sales: daily sales by product category at date x category x region grain
CREATE TABLE IF NOT EXISTS gold_daily_sales (
    daily_sales_id VARCHAR PRIMARY KEY,
    order_date DATE NOT NULL,
    region_id VARCHAR NOT NULL,
    region_name VARCHAR NOT NULL,
    product_category VARCHAR NOT NULL,
    order_count INTEGER NOT NULL,
    sold_quantity INTEGER NOT NULL,
    total_revenue_amount DOUBLE NOT NULL,
    return_order_count INTEGER NOT NULL DEFAULT 0,
    is_late_arriving_data BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

-- gold_returns_rate: return-rate KPI at date x region grain
CREATE TABLE IF NOT EXISTS gold_returns_rate (
    returns_rate_id VARCHAR PRIMARY KEY,
    order_date DATE NOT NULL,
    region_id VARCHAR NOT NULL,
    region_name VARCHAR NOT NULL,
    completed_or_returned_order_count INTEGER NOT NULL,
    returned_order_count INTEGER NOT NULL,
    return_rate DOUBLE NOT NULL,
    is_late_arriving_data BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

-- dim_region: access-control and conformed region dimension
CREATE TABLE IF NOT EXISTS dim_region (
    region_id VARCHAR PRIMARY KEY,
    region_name VARCHAR NOT NULL,
    region_manager_name VARCHAR,
    region_manager_role VARCHAR,
    assigned_region_code VARCHAR NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    effective_start_date DATE NOT NULL,
    effective_end_date DATE,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

CREATE UNIQUE INDEX IF NOT EXISTS ux_gold_daily_sales_grain
ON gold_daily_sales(order_date, region_id, product_category);

CREATE UNIQUE INDEX IF NOT EXISTS ux_gold_returns_rate_grain
ON gold_returns_rate(order_date, region_id);
