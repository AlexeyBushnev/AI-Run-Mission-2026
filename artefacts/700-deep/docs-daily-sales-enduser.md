# docs-daily-sales-enduser.md

## Daily Sales by Category

### What this table contains

This table shows **how much was sold each day for each product type**.

A row in this table answers a simple business question:

> “On this calendar day, how many completed sales did we have for this product category, and how much revenue did they produce?”

This table is intended for reporting and analysis. It is not a raw transaction table.

### When it updates

- The table refreshes **daily**
- Data is expected to be available within **24 hours of each day’s close**

If the table is late, the previous published version may remain visible until the new load is complete.

### What each column means

- **order_date**  
  The calendar day the sales belong to.

- **product_category**  
  The product type being reported, such as Electronics, Home, Beauty, or Sports.

- **total_revenue**  
  The total money from completed sales for that date and category.

- **order_count**  
  The number of completed orders included in the total.

- **sold_quantity**  
  The number of items sold in that date and category.

### Use this table when you want to

1. **Track daily sales performance by product type**  
   Example: compare Electronics revenue this week versus last week.

2. **Prepare business summaries for dashboards or finance reporting**  
   Example: use daily category totals in a weekly sales review or a monthly management pack.

### Important usage notes

- This table is built from **completed sales**
- Cancelled or pending orders should not be treated as revenue in this table
- The table is already summarized, so it is best for trends and reporting, not for record-level investigation

### Who can use it

This table is intended for approved reporting and analytics users. Access may be restricted by business role or region depending on the reporting layer.

### What to do if the numbers look wrong

Check these first:
1. Is the table updated for the expected date?
2. Are you comparing the same product category definitions across reports?
3. Is another report using raw transactions instead of this summarized table?

### Contact

If the data looks wrong, contact:

- **Aleksei Bushnev**
- **Team:** Nordstar Customer 360 Data
- **Reason to contact:** missing dates, unexpected revenue shifts, category mismatch, or stale refresh

### Table identifier

`daily_sales_by_category`
