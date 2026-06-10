import pandas as pd
import plotly.express as px
import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Sales Performance Dashboard", layout="wide")

st.title("Sales Performance Dashboard")

BASE_DIR = Path(__file__).resolve().parent
daily_path = BASE_DIR.parent / "gold" / "daily_sales_by_category.parquet"
returns_path = BASE_DIR.parent / "gold" / "returns_rate.parquet"

daily_df = pd.read_parquet(daily_path)
returns_df = pd.read_parquet(returns_path)

daily_df["order_date"] = pd.to_datetime(daily_df["order_date"])
returns_df["order_date"] = pd.to_datetime(returns_df["order_date"])

max_date = daily_df["order_date"].max().date()
min_available = daily_df["order_date"].min().date()
default_start = max(min_available, max_date - pd.Timedelta(days=29))

date_range = st.sidebar.date_input(
    "Date range",
    value=(default_start, max_date),
    min_value=min_available,
    max_value=max_date,
)

if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
else:
    start_date = pd.to_datetime(default_start)
    end_date = pd.to_datetime(max_date)

daily_f = daily_df[(daily_df["order_date"] >= start_date) & (daily_df["order_date"] <= end_date)].copy()
returns_f = returns_df[(returns_df["order_date"] >= start_date) & (returns_df["order_date"] <= end_date)].copy()

total_revenue = float(daily_f["total_revenue"].sum()) if not daily_f.empty else 0.0
avg_returns_rate = float(returns_f["returns_rate_pct"].mean()) if not returns_f.empty else 0.0

c1, c2 = st.columns(2)
c1.metric("Total Revenue", f"{total_revenue:,.2f}")
c2.metric("Average Returns Rate", f"{avg_returns_rate:.2f}%")

bar_df = daily_f.groupby(["region", "product_category"], as_index=False)["total_revenue"].sum()
fig1 = px.bar(
    bar_df,
    x="region",
    y="total_revenue",
    color="product_category",
    barmode="group",
    title="Revenue by Region",
)
st.plotly_chart(fig1, use_container_width=True)

fig2 = px.line(
    returns_f.sort_values("order_date"),
    x="order_date",
    y="returns_rate_pct",
    title="Returns Rate Over Time",
)
st.plotly_chart(fig2, use_container_width=True)

st.caption(f"Data last updated: {daily_df['order_date'].max().date()}")
