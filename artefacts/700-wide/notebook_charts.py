# Notebook-friendly chart code for K 7.6
import duckdb
import pandas as pd
import matplotlib.pyplot as plt

con = duckdb.connect(database=":memory:")
daily_df = con.execute("SELECT * FROM read_parquet('gold/daily_sales_by_category.parquet')").df()
returns_df = con.execute("SELECT * FROM read_parquet('gold/returns_rate.parquet')").df()

daily_df["order_date"] = pd.to_datetime(daily_df["order_date"])
returns_df["order_date"] = pd.to_datetime(returns_df["order_date"])

max_date = daily_df["order_date"].max()
min_date = max_date - pd.Timedelta(days=29)

daily_f = daily_df[(daily_df["order_date"] >= min_date) & (daily_df["order_date"] <= max_date)].copy()
returns_f = returns_df[(returns_df["order_date"] >= min_date) & (returns_df["order_date"] <= max_date)].copy()

bar_df = daily_f.groupby(["region", "product_category"], as_index=False)["total_revenue"].sum()
pivot = bar_df.pivot(index="region", columns="product_category", values="total_revenue").fillna(0)

pivot.plot(kind="bar", figsize=(10, 5))
plt.title("Revenue by Region and Category")
plt.xlabel("Region")
plt.ylabel("Total Revenue")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 4))
plt.plot(pd.to_datetime(returns_f["order_date"]), returns_f["returns_rate_pct"], marker="o")
plt.title("Returns Rate Over Time")
plt.xlabel("Order Date")
plt.ylabel("Returns Rate %")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# One thing to change later:
# Consider switching chart 1 from grouped bars to stacked bars or adding currency formatting for easier executive reading.
