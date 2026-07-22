import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="NovaMart Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("NovaMart Dashboard — Muhammed Faraz")

@st.cache_data
def load_data():
    return pd.read_csv("output/novamart_clean.csv")
df = load_data()


st.sidebar.header("Filters")

category = st.sidebar.multiselect(
    "Select Category",
    options=df["category"].unique(),
    default=df["category"].unique()
)

month = st.sidebar.selectbox(
    "Select Month",
    options=["All"] + list(df["order_month"].unique())
)

filtered_df = df[df["category"].isin(category)]

if month != "All":
    filtered_df = filtered_df[
        filtered_df["order_month"] == month
    ]

# ===========================
# KPI CARDS
# ===========================

total_sales = filtered_df["sales"].sum()
total_profit = filtered_df["profit"].sum()
total_orders = filtered_df["order_id"].nunique()
total_quantity = filtered_df["quantity"].sum()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="💰 Total Sales",
        value=f"₹{total_sales:,.2f}"
    )

with col2:
    st.metric(
        label="📈 Total Profit",
        value=f"₹{total_profit:,.2f}"
    )

with col3:
    st.metric(
        label="📦 Total Orders",
        value=f"{total_orders:,}"
    )

with col4:
    st.metric(
        label="🛒 Quantity Sold",
        value=f"{total_quantity:,}"
    )

# ===========================
# Monthly Sales Trend
# ===========================

st.markdown("---")

st.subheader("📈 Monthly Sales Trend")

monthly_sales = (
    filtered_df
    .groupby("order_month")["sales"]
    .sum()
)

fig, ax = plt.subplots(figsize=(10,5))

ax.plot(
    monthly_sales.index,
    monthly_sales.values,
    marker="o",
    linewidth=3
)

ax.set_xlabel("Month")
ax.set_ylabel("Sales")
ax.set_title("Monthly Sales")

plt.xticks(rotation=45)

st.pyplot(fig)

# ===========================
# Sales by Category
# ===========================

st.markdown("---")

st.subheader("📊 Sales by Category")

category_sales = (
    filtered_df
    .groupby("category")["sales"]
    .sum()
)

fig, ax = plt.subplots(figsize=(8,5))

ax.bar(
    category_sales.index,
    category_sales.values
)

ax.set_xlabel("Category")
ax.set_ylabel("Sales")

st.pyplot(fig)

# ===========================
# Top 10 Products
# ===========================

st.markdown("---")

st.subheader("📦 Top 10 Products")

top_products = (
    filtered_df
    .groupby("product_name")["sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

fig, ax = plt.subplots(figsize=(10,6))

ax.barh(
    top_products.index,
    top_products.values
)

ax.invert_yaxis()

st.pyplot(fig)

# ===========================
# Filtered Data
# ===========================

st.markdown("---")

st.subheader("📋 Filtered Data")

st.dataframe(
    filtered_df,
    use_container_width=True
)
