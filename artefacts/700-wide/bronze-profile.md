# bronze-profile

## File
`bronze/transactions_raw.csv`

## Row count
- total rows: 500

## Null count per column
- order_id: 0
- customer_id: 0
- region: 0
- order_date: 0
- product_category: 0
- amount: 25
- quantity: 0
- status: 0

## Duplicate order_id count
- duplicate order_ids: 15

## Amount profile
- min amount: -167.39
- max amount: 499.46

## Distinct status values
- completed, pending, returned

## Date format distribution
- YYYY-MM-DD: 164
- DD/MM/YYYY: 170
- Mon DD YYYY: 166

## Notes
- Dataset intentionally includes null amounts, duplicate `order_id` values, negative amounts for returns, and mixed date formats.
- Use this file as the bronze cleaning baseline for K 7.W.3.
