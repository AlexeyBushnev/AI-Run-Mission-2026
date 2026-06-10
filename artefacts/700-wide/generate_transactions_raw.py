import re
import os
import random
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

random.seed(42)
np.random.seed(42)

os.makedirs("bronze", exist_ok=True)

row_count = 500
duplicate_count = 15
null_amount_count = 25
negative_amount_count = 10

regions = ["North", "South", "East", "West"]
categories = ["Electronics", "Clothing", "Food", "Home", "Sports"]
statuses = ["completed", "returned", "pending"]
status_probs = [0.80, 0.15, 0.05]
date_formats = [
    lambda d: d.strftime("%Y-%m-%d"),
    lambda d: d.strftime("%d/%m/%Y"),
    lambda d: d.strftime("%b %d %Y"),
]

start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 12, 31)
date_span = (end_date - start_date).days

base_rows = []
for i in range(row_count - duplicate_count):
    order_id = f"ORD-{10000 + i:05d}"
    customer_id = random.randint(1000, 9999)
    region = random.choice(regions)
    order_dt = start_date + timedelta(days=random.randint(0, date_span))
    order_date = random.choice(date_formats)(order_dt)
    product_category = random.choice(categories)
    amount = round(random.uniform(5.0, 500.0), 2)
    quantity = random.randint(1, 10)
    status = random.choices(statuses, weights=status_probs, k=1)[0]
    base_rows.append(
        {
            "order_id": order_id,
            "customer_id": customer_id,
            "region": region,
            "order_date": order_date,
            "product_category": product_category,
            "amount": amount,
            "quantity": quantity,
            "status": status,
        }
    )

# Add duplicate rows by reusing existing order_ids with slightly varied other fields
rows = base_rows.copy()
dup_indices = np.random.choice(len(base_rows), size=duplicate_count, replace=False)
for idx in dup_indices:
    dup = base_rows[idx].copy()
    dup["quantity"] = random.randint(1, 10)
    rows.append(dup)

# Apply null amounts to exactly 25 rows
null_indices = np.random.choice(len(rows), size=null_amount_count, replace=False)
for idx in null_indices:
    rows[idx]["amount"] = None

# Apply negative amounts to exactly 10 non-null rows
eligible = [i for i in range(len(rows)) if i not in set(null_indices)]
neg_indices = np.random.choice(eligible, size=negative_amount_count, replace=False)
for idx in neg_indices:
    rows[idx]["amount"] = -round(random.uniform(1.0, 200.0), 2)

df = pd.DataFrame(rows)
df.to_csv("bronze/transactions_raw.csv", index=False)

# Print checks
dup_count = int(df["order_id"].duplicated().sum())
null_count = int(df["amount"].isna().sum())

fmt_patterns = set()
for value in df["order_date"].astype(str):
    if "-" in value and re.match(r"^\d{4}-\d{2}-\d{2}$", value):
        fmt_patterns.add("YYYY-MM-DD")
    elif "/" in value and re.match(r"^\d{2}/\d{2}/\d{4}$", value):
        fmt_patterns.add("DD/MM/YYYY")
    else:
        fmt_patterns.add("Mon DD YYYY")

print("total rows:", len(df))
print("null count in amount:", null_count)
print("duplicate order_id count:", dup_count)
print("unique date formats found:", sorted(fmt_patterns))
