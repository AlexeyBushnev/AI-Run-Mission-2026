*Reviewed by: Aleksei Bushnev, 2026-07-02*

# 00-data-prd.md — Regional Sales Performance Report

## 0. Product summary

**Data product name:** Regional Sales Performance Report  
**Purpose:** Provide weekly and monthly performance reporting for regional managers and board reporting consumers.  
**Business requirement:** Build a weekly sales performance report for regional managers. Each manager sees only their own region's data. The report must show revenue by product category, return rate, and top 5 products by volume. Data must be fresh within 24 hours of each day's close. Retain data for 3 years. The report is used for weekly planning meetings and monthly board reports.  
**Primary consumers:** Regional Managers, Board Reporting Analysts, Executive / Board audience  
**Human sign-off status:** Reviewed and signed off for downstream schema, contract, DQ, and serving work.

## 1. Assumptions confirmed during specification

1. **Revenue** means completed sales only, excluding cancelled and pending orders.  
2. **Return rate** means returned orders divided by completed + returned orders, not all orders including pending/cancelled.  
3. **Top 5 products by volume** means highest total sold quantity from completed sales at weekly grain within the viewer's allowed region.  
4. **Fresh within 24 hours of each day's close** means the daily underlying data load for the previous business day must be available within 24 hours after day-end close.  
5. **Regional managers must be restricted by row-level security** on `region`, not only by application role.  
6. **Retention** is 3 years because the business requirement states 3 years; reviewed annually for continued business purpose and regulatory fit.

## 2. Source-to-Target Mapping (STTM)

### 2.1 Source entities assumed

- `silver_sales_order`
- `silver_sales_order_line`
- `silver_product`
- `silver_return`
- `silver_store`
- `silver_region_manager_assignment`

### 2.2 STTM table

| Source column(s) | Target column | Transformation SQL | Business rule | Data type | Nullable |
|---|---|---|---|---|---|
| `o.order_id` | `order_id` | `o.order_id` | Unique sales order identifier from silver | VARCHAR | No |
| `o.order_date` | `order_date` | `CAST(o.order_date AS DATE)` | Order date normalized to date grain | DATE | No |
| `DATE_TRUNC('week', o.order_date)` | `week_start_date` | `DATE_TRUNC('week', o.order_date)` | Reporting week anchor | DATE | No |
| `s.region_name` | `region` | `s.region_name` | Manager-facing security and reporting region | VARCHAR | No |
| `p.category_name` | `product_category` | `p.category_name` | Product category used for revenue breakout | VARCHAR | No |
| `l.product_id` | `product_id` | `l.product_id` | Product identifier for top-5 ranking | VARCHAR | No |
| `p.product_name` | `product_name` | `p.product_name` | Business-readable product name | VARCHAR | No |
| `l.quantity` | `sold_quantity` | `CASE WHEN o.status = 'completed' THEN l.quantity ELSE 0 END` | Only completed sales count toward sold volume | INTEGER | No |
| `l.extended_amount` | `completed_revenue_amount` | `CASE WHEN o.status = 'completed' THEN l.extended_amount ELSE 0 END` | Revenue is completed sales only | DECIMAL(18,2) | No |
| `r.return_id` | `return_flag` | `CASE WHEN r.return_id IS NOT NULL THEN 1 ELSE 0 END` | Indicates whether the order line was returned | INTEGER | No |
| `r.return_quantity` | `returned_quantity` | `COALESCE(r.return_quantity, 0)` | Quantity returned | INTEGER | No |
| `o.order_id, r.return_id` | `return_rate_numerator_flag` | `CASE WHEN r.return_id IS NOT NULL AND o.status IN ('completed','returned') THEN 1 ELSE 0 END` | Numerator for return-rate KPI | INTEGER | No |
| `o.order_id, o.status` | `return_rate_denominator_flag` | `CASE WHEN o.status IN ('completed','returned') THEN 1 ELSE 0 END` | Denominator excludes pending and cancelled orders | INTEGER | No |
| `manager.assigned_region` | `viewer_region_scope` | `manager.assigned_region` | Region used to enforce row-level filtering | VARCHAR | No |
| `CURRENT_TIMESTAMP` | `etl_loaded_at` | `CURRENT_TIMESTAMP` | Load audit timestamp | TIMESTAMP | No |

## 3. KPI Definitions

### 3.1 KPI table

| KPI | Definition | Formula | Grain | Cadence | Dispute owner |
|---|---|---|---|---|---|
| Revenue by product category | Total completed-sales revenue grouped by region, week, and product category | `SUM(completed_revenue_amount)` where source rows already apply `o.status = 'completed'` | Region × Week × Product Category | Weekly view, daily refreshed | Regional Sales Analytics Owner |
| Return rate | Share of completed-or-returned orders that had a return event | `SUM(return_rate_numerator_flag) / NULLIF(SUM(return_rate_denominator_flag), 0)` | Region × Week | Weekly view, daily refreshed | Returns Operations Owner |
| Top 5 products by volume | Five products with highest sold quantity in the region and reporting week | `RANK() OVER (PARTITION BY region, week_start_date ORDER BY SUM(sold_quantity) DESC)` and keep `rank <= 5` | Region × Week × Product | Weekly view, daily refreshed | Merchandising Analytics Owner |

### 3.2 Manual verification notes

**Revenue formula check:** verified conceptually against the business rule: completed sales only.  
**Return-rate denominator check:** verified against the stated requirement that pending/cancelled orders must not dilute the rate.

Worked mini-example for return rate:

| order_id | status | returned? |
|---|---|---|
| O-100 | completed | no |
| O-101 | completed | yes |
| O-102 | pending | no |

Correct result:  
- numerator = 1 (`O-101`)  
- denominator = 2 (`O-100`, `O-101`)  
- return rate = `1 / 2 = 0.5 = 50%`

This confirms that using `COUNT(returned) / COUNT(all orders)` would be wrong because it would incorrectly include pending orders in the denominator.

## 4. SLA and Late-Data Policy

### 4.1 SLA

- **Freshness requirement:** data must be available within **24 hours of each day's close**
- **Availability target:** **99.0%** successful scheduled publication of the daily refresh
- **Consumer-facing cadence:** weekly report with daily data refresh
- **Intended business use:** weekly planning meetings and monthly board reports

### 4.2 Late-data policy

**Policy:** hold the previous published version and alert; do not publish a partial or late refresh as the new official version.

**Rationale:** board and regional-planning use cases favor consistency over partially refreshed numbers. A stale-but-known prior version is safer than a mixed or partial daily version that can create false week-over-week conclusions.

**Operational action when source arrives late:**
1. mark refresh as late
2. retain last good published snapshot
3. send alert to data product owner
4. rerun load when late source arrives
5. append incident note to operational log

## 5. DQ Expectations

| Dimension | Rule | Threshold | Gate or mark | Business rationale |
|---|---|---:|---|---|
| Accuracy | Completed revenue in gold must match silver completed-sales aggregation | ±0.5% max variance | Gate | Revenue used in board reporting |
| Completeness | Required keys (`order_id`, `order_date`, `region`, `product_id`, `category_name`) populated | ≥ 99.0% fill rate | Gate | Missing keys break grouping and security |
| Timeliness | Latest successful load age relative to prior business close | ≤ 24 hours | Gate | Explicit business freshness requirement |
| Consistency | Revenue by region must reconcile against source control totals | ±0.1% cross-source tolerance | Mark | Small reconciliation noise may be investigated without full stop |
| Uniqueness | Duplicate `order_id + product_id + week_start_date` rows in gold aggregate base | 0 duplicates allowed | Gate | Duplicate facts distort KPIs |
| Validity | `status` in allowed set; non-negative quantities; revenue amount >= 0 for sales rows | 100% valid rows | Gate | Prevents semantic corruption |

## 6. Access Control Specification

### 6.1 Roles

- **Regional Manager**
- **Board Reporting Analyst**
- **Executive / Board Consumer**
- **Data Engineering Support**
- **Finance Analyst**

### 6.2 Row-level security

| Role | Row-level rule |
|---|---|
| Regional Manager | Can see only rows where `region = user.assigned_region` |
| Board Reporting Analyst | Can see all regions |
| Executive / Board Consumer | Can see all regions |
| Data Engineering Support | Can see all regions in non-production support context only; production access requires approved support workflow |
| Finance Analyst | Can see all regions |

**Mandatory control:** row-level security must be enforced in the serving layer or semantic model, not only in UI navigation. A West manager who knows a report URL must still be unable to query East rows.

### 6.3 Column-level security

| Column / field group | Allowed roles | Restricted roles | Rule |
|---|---|---|---|
| `region`, `week_start_date`, `product_category`, `product_name`, KPI outputs | All consumer roles | None | Standard business reporting fields |
| Low-level operational load metadata (`etl_loaded_at`) | Data Engineering Support, Board Reporting Analyst | Regional Manager, Executive / Board Consumer | Not needed for standard consumption |
| Margin / cost columns if later added | Finance Analyst, Executive / Board Consumer | Regional Manager by default | Sensitive financial detail excluded unless explicitly approved |
| Raw customer-level identifiers if later joined | None in this product by default | All consumer roles | Out of scope for this data product |

## 7. Retention and Compliance

- **Retention period:** **3 years**
- **Rationale:** explicitly aligned with business requirement for weekly planning and monthly board reporting history; reviewed annually for continued business need
- **Compliance stance:** apply purpose limitation and data minimization; do not retain fields not needed for the reporting purpose
- **Review cadence:** annual retention review by data product owner and governance contact
- **PII handling:** this product should avoid direct customer-level PII; if upstream joins later introduce PII, column tagging and access restriction must be updated before release

## 8. Open decisions / future considerations

1. Confirm whether board-facing output requires finance-only cost or margin fields later.
2. Confirm whether weekly reporting week starts Monday across all regions.
3. Confirm whether return rate is measured at order level or order-line level in the final serving semantic layer; current PRD assumes order-level numerator/denominator flags.
4. If store-level drilldown is added later, update row-level rules and DQ reconciliation logic.

## 9. Sign-off

**Human reviewer:** Aleksei Bushnev  
**Review date:** 2026-07-02  
**Review statement:** I verified the KPI denominators, filtered aggregation logic, row-level region security requirement, late-data policy, DQ thresholds, and retention rationale before sign-off.
