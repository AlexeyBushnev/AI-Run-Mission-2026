# schema-change-runbook-v1.md

## Change summary

**Change type:** Breaking schema change  
**Affected table:** `gold_daily_sales`  
**Old column:** `amount_cents INTEGER`  
**New columns:**  
- `order_total_usd DOUBLE`  
- `currency_code VARCHAR DEFAULT 'USD'`

**Why this is breaking**
1. Column rename: `amount_cents` → `order_total_usd`
2. Type change: `INTEGER` → `DOUBLE`
3. Semantic change: value is divided by 100, so the numeric meaning changes from cents to dollars

---

## 1. Impact analysis

| Consumer | Affected column(s) | Change impact | Migration action required | Effort estimate | Migration owner |
|---|---|---|---|---:|---|
| Weekly Sales Dashboard | `amount_cents` | Bar chart calculation fails or shows wrong units if still reading cents | Update dashboard queries and calculations to read `order_total_usd`; confirm formatting in USD | 3h | Dashboard owner (TBD) |
| Finance Report API | `amount_cents` | Revenue aggregation endpoint breaks or silently returns incorrect totals if unit conversion is not applied | Update API query/model to use `order_total_usd`; return `currency_code` where needed | 4h | API owner (TBD) |
| Executive PowerPoint | indirect via Finance Report API | PowerPoint refresh breaks if API contract breaks | No direct SQL change; verify API output and report template mapping after API migration | 2h | Executive reporting owner (TBD) |

### Direct and indirect dependency check

- **Direct readers:** Weekly Sales Dashboard, Finance Report API
- **Indirect reader:** Executive PowerPoint through Finance Report API

No consumer is considered complete until both direct and indirect dependencies are acknowledged.

---

## 2. Migration SQL

### Step 1 — add `order_total_usd` and backfill from cents

```sql
ALTER TABLE gold_daily_sales ADD COLUMN order_total_usd DOUBLE;

UPDATE gold_daily_sales
SET order_total_usd = amount_cents / 100.0
WHERE order_total_usd IS NULL;
```

**Verification query**
```sql
SELECT order_date, product_category, amount_cents, order_total_usd
FROM gold_daily_sales
ORDER BY order_date, product_category
LIMIT 20;
```

Expected: `order_total_usd = amount_cents / 100.0`

---

### Step 2 — add `currency_code` with default USD

```sql
ALTER TABLE gold_daily_sales ADD COLUMN currency_code VARCHAR DEFAULT 'USD';

UPDATE gold_daily_sales
SET currency_code = COALESCE(currency_code, 'USD');
```

**Verification query**
```sql
SELECT COUNT(*) AS non_usd_count
FROM gold_daily_sales
WHERE currency_code IS NULL OR currency_code <> 'USD';
```

Expected: `0`

---

### Step 3 — create compatibility view for deprecation window

```sql
CREATE OR REPLACE VIEW v_gold_daily_sales_compat AS
SELECT
    order_date,
    product_category,
    CAST(ROUND(order_total_usd * 100) AS INTEGER) AS amount_cents,
    order_total_usd,
    currency_code
FROM gold_daily_sales;
```

**Verification query**
```sql
SELECT order_date, product_category, amount_cents, order_total_usd, currency_code
FROM v_gold_daily_sales_compat
ORDER BY order_date, product_category
LIMIT 20;
```

Expected:
- old consumers can still read `amount_cents`
- migrated consumers can read `order_total_usd`
- both fields return equivalent values by unit conversion

---

### Step 4 — after deprecation window, remove old path

DuckDB does not always support drop-column workflows the same way as warehouse engines, so the safe pattern is table recreation.

```sql
CREATE OR REPLACE TABLE gold_daily_sales_new AS
SELECT
    order_date,
    product_category,
    order_total_usd,
    currency_code
FROM gold_daily_sales;

DROP VIEW IF EXISTS v_gold_daily_sales_compat;
DROP TABLE gold_daily_sales;
ALTER TABLE gold_daily_sales_new RENAME TO gold_daily_sales;
```

**Verification query**
```sql
PRAGMA table_info('gold_daily_sales');
```

Expected: `amount_cents` no longer exists

---

## 3. Deprecation timeline

Minimum deprecation window: **6 weeks**  
Reason: this breaking change affects 3 consumers, including one indirect consumer.

| Milestone | Date / window | Action | Responsible | Verification |
|---|---|---|---|---|
| Week 0 | 2026-07-02 | Announce change, publish compatibility view, notify all consumers | Data engineer + data product owner | Notification sent; compatibility view query works |
| Sprint 1 | Weeks 1–2 | Weekly Sales Dashboard and Finance Report API migrate to `order_total_usd` | Consumer owners | Consumer test queries pass using new column |
| Sprint 2 | Weeks 3–4 | Reminder + final warning; Executive PowerPoint validated against migrated API output | Data product owner + reporting owner | API contract verified; report refresh succeeds |
| Week 5 | 1 week before removal | Final readiness review; confirm no open migration blockers | Data platform lead | Signed migration checklist |
| Week 6 | End of deprecation window | Remove `amount_cents` path and drop compatibility view | Data engineer | Post-cutover smoke tests pass |

**Rule:** no removal before at least **2 sprints / 4 weeks**. This runbook uses **6 weeks**.

---

## 4. Consumer notification template

**Subject:** Breaking schema change planned for `gold_daily_sales`: `amount_cents` → `order_total_usd`

Hello team,

We are planning a breaking schema change to `gold_daily_sales`.

### What is changing
- `amount_cents` will be replaced by `order_total_usd`
- revenue values will be expressed in **USD**, not cents
- a new `currency_code` field will be added with default value `USD`

### What you need to do
1. Update your consumer logic to read `order_total_usd`
2. Validate numeric formatting and aggregation logic with the compatibility view before the removal date

### Deadline
Please complete migration before **Week 6** of the deprecation timeline.

### Migration help
During the deprecation window, use `v_gold_daily_sales_compat`, which exposes both:
- `amount_cents`
- `order_total_usd`

### Contact
Contact the **Data Product Owner** or **Data Engineering owner** if you need help validating your migration.

---

## 5. Rollback plan

Rollback target: restore `amount_cents INTEGER` using SQL only, in under **10 minutes**.

### Trigger conditions
- consumer errors after cutover
- incorrect units in downstream reporting
- failed migration validation in production
- report/API output mismatch discovered after drop

### Rollback SQL

```sql
CREATE OR REPLACE TABLE gold_daily_sales_rollback AS
SELECT
    order_date,
    product_category,
    CAST(ROUND(order_total_usd * 100) AS INTEGER) AS amount_cents
FROM gold_daily_sales;

DROP TABLE gold_daily_sales;
ALTER TABLE gold_daily_sales_rollback RENAME TO gold_daily_sales;
```

### Rollback verification

```sql
SELECT order_date, product_category, amount_cents
FROM gold_daily_sales
ORDER BY order_date, product_category
LIMIT 20;
```

Expected: values match the original cents-based numbers.

### Rollback execution estimate

- SQL execution: 1–3 minutes on moderate table size
- smoke-test verification: 2–5 minutes
- total expected rollback time: **under 10 minutes**

**Note:** a backup restore is not the rollback plan. The rollback is the SQL above.

---

## 6. Test evidence from DuckDB dry run

The migration path and rollback path were tested on a sample table.

### Verified
- compatibility view exposed both `amount_cents` and `order_total_usd`
- post-drop table shape removed `amount_cents`
- rollback restored `amount_cents` values correctly using `order_total_usd * 100`

---

## 7. Pre-cutover checklist

- [ ] all direct consumers identified
- [ ] indirect consumers identified
- [ ] compatibility view published
- [ ] migration guide sent
- [ ] consumer owners acknowledged deadline
- [ ] smoke tests prepared
- [ ] rollback SQL tested
- [ ] rollback owner assigned
