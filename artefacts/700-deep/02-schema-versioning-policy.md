# 02-schema-versioning-policy.md

## Schema versioning policy

**Current version:** 1.0.0  
**Semantic version format:** `MAJOR.MINOR.PATCH`

- **MAJOR**: breaking consumer change
- **MINOR**: additive backward-compatible change
- **PATCH**: non-breaking fix that does not change consumer query semantics

## Additive changes

A change is **additive** if an existing consumer can run the same query without error and without a silent meaning change in existing columns.

Typical additive examples:
1. Add a new nullable column such as `promotion_code`
2. Add a new table such as `gold_weekly_sales_summary`
3. Add a new non-null column **only if** historical rows are backfilled and the existing consumer-facing semantics do not change
4. Add a new quality rule in the contract without changing existing schema fields
5. Add a new allowed enum value that consumers already treat generically

### Clear additive example
Adding `sales_channel VARCHAR NULL` to `gold_daily_sales` is additive if existing consumers do not query it and existing rows may remain null safely.

## Breaking changes

A change is **breaking** if an existing consumer who does not modify their query gets a query error, a missing field, or materially different results.

Typical breaking examples:
1. Rename a column, for example `product_category` to `category_name`
2. Remove a column or table
3. Change a column's meaning or aggregation logic, for example revenue from completed-only sales to all orders
4. Tighten a column from nullable to not-null without safe backfill
5. Change grain, for example from `order_date + region_id + product_category` to weekly grain only

### Clear breaking example
Renaming `total_revenue_amount` to `revenue_amount` is breaking because downstream queries will fail until consumers update them.

## Edge case

### Adding a NOT NULL column
This is:
- **breaking** if existing rows would contain nulls or if consumers must now provide the field and cannot do so without code changes
- **additive** only if the new column is fully backfilled for all historical rows and the change does not alter existing query semantics

Worked example:
Adding `currency_code VARCHAR NOT NULL` is breaking if historical rows do not already have a safe default and downstream logic must be updated.
It can be additive only if every existing row is backfilled consistently and consumers reading the old columns still get the same results.

## Approval process for breaking changes

Breaking changes require:
1. approval from the **Data Product Owner**
2. approval from at least **one named consumer owner**
3. documented migration note in the contract or schema-change PR
4. minimum **10 business days** notice before production rollout, unless an emergency fix is explicitly approved

Recommended workflow:
- additive changes: standard PR review + CI validation
- breaking changes: PR review + CI validation + owner sign-off + consumer communication + version bump to next MAJOR version

## Version examples

- `1.0.0 -> 1.1.0`: add nullable `sales_channel`
- `1.1.0 -> 1.1.1`: fix description typo or contract metadata
- `1.1.0 -> 2.0.0`: rename `product_category` to `category_name`
