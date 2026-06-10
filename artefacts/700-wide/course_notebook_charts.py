import duckdb, pandas as pd, matplotlib.pyplot as plt
con = duckdb.connect(database=":memory:")
daily = con.execute("SELECT * FROM read_parquet('daily_completions_by_category.parquet')").df()
dropout = con.execute("SELECT * FROM read_parquet('dropout_rate.parquet')").df()

daily["event_date"] = pd.to_datetime(daily["event_date"])
dropout["event_date"] = pd.to_datetime(dropout["event_date"])

max_date = daily["event_date"].max()
min_date = max_date - pd.Timedelta(days=29)

daily_f = daily[(daily["event_date"] >= min_date) & (daily["event_date"] <= max_date)].copy()
dropout_f = dropout[(dropout["event_date"] >= min_date) & (dropout["event_date"] <= max_date)].copy()

pivot = daily_f.pivot_table(index="event_date", columns="course_category", values="completion_count", aggfunc="sum").fillna(0)
pivot.plot(figsize=(11,5))
plt.title("Daily Completions by Category")
plt.tight_layout()
plt.show()

plt.figure(figsize=(11,4))
plt.plot(dropout_f["event_date"], dropout_f["dropout_rate_pct"], marker="o")
plt.title("Dropout Rate Over Time")
plt.tight_layout()
plt.show()
