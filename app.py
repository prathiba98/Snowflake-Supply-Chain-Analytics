import streamlit as st
import snowflake.connector
import pandas as pd

st.set_page_config(page_title="Supply Chain Dashboard", layout="wide")

# ---------------------------
# Snowflake Connection
# ---------------------------
conn = snowflake.connector.connect(
    user=st.secrets["user"],
    password=st.secrets["password"],
    account=st.secrets["account"],
    warehouse="SUPPLY_CHAIN_WH",
    database="SUPPLY_CHAIN_DB",
    schema="PUBLIC"
)

def run_query(query):
    return pd.read_sql(query, conn)

# ---------------------------
# Sidebar Filters
# ---------------------------
st.sidebar.header("🔎 Filters")

category_df = run_query("SELECT DISTINCT category FROM products")
categories = category_df["CATEGORY"].tolist()
selected_category = st.sidebar.selectbox("Select Category", categories)

warehouse_df = run_query("SELECT DISTINCT warehouse_name FROM warehouses")
warehouses = warehouse_df["WAREHOUSE_NAME"].tolist()
selected_warehouse = st.sidebar.selectbox("Select Warehouse", warehouses)

# ---------------------------
# Header
# ---------------------------
st.title(" Supply Chain & Inventory Intelligence Platform")
st.markdown("Cloud-based analytics system powered by Snowflake and Streamlit.")

st.markdown("---")

# ---------------------------
# KPI Section
# ---------------------------
kpi_df = run_query("""
SELECT 
    SUM(s.quantity_sold * p.selling_price) AS total_revenue,
    SUM(s.quantity_sold) AS total_units_sold
FROM sales s
JOIN products p ON s.product_id = p.product_id
""")

col1, col2 = st.columns(2)

col1.metric(" Total Revenue", f"₹ {int(kpi_df['TOTAL_REVENUE'][0]):,}")
col2.metric(" Total Units Sold", f"{int(kpi_df['TOTAL_UNITS_SOLD'][0]):,}")

st.markdown("---")

# ---------------------------
# Monthly Revenue Trend
# ---------------------------
monthly_df = run_query("""
SELECT 
    DATE_TRUNC('month', sale_date) AS month,
    SUM(s.quantity_sold * p.selling_price) AS revenue
FROM sales s
JOIN products p ON s.product_id = p.product_id
GROUP BY month
ORDER BY month
""")

st.subheader(" Monthly Revenue Trend")
st.line_chart(monthly_df.set_index("MONTH"))

st.caption("Insight: Revenue trend helps identify seasonal demand patterns and growth trajectory.")

st.markdown("---")

# ---------------------------
# Warehouse Revenue
# ---------------------------
warehouse_perf = run_query("""
SELECT warehouse_name, warehouse_revenue
FROM v_warehouse_performance
ORDER BY warehouse_revenue DESC
""")

st.subheader(" Warehouse Revenue Ranking")
st.bar_chart(warehouse_perf.set_index("WAREHOUSE_NAME"))

st.caption("Insight: Top-performing warehouses drive majority of revenue and require capacity optimization.")

st.markdown("---")

# ---------------------------
# Category Revenue
# ---------------------------
category_rev = run_query("""
SELECT 
    p.category,
    SUM(s.quantity_sold * p.selling_price) AS revenue
FROM sales s
JOIN products p ON s.product_id = p.product_id
GROUP BY p.category
ORDER BY revenue DESC
""")

st.subheader(" Revenue by Category")
st.bar_chart(category_rev.set_index("CATEGORY"))

st.caption("Insight: Category contribution highlights high-margin segments.")

st.markdown("---")

# ---------------------------
# Slow Moving Products
# ---------------------------
slow_products = run_query("""
SELECT product_name, total_units_sold
FROM v_product_performance
ORDER BY total_units_sold ASC
LIMIT 10
""")

st.subheader(" Slow Moving Products")
st.dataframe(slow_products)

st.caption("Insight: Low-performing products may require discounting or stock optimization.")

st.markdown("---")

# ---------------------------
# Stock Turnover
# ---------------------------
turnover_df = run_query("""
SELECT product_name, stock_turnover
FROM v_stock_turnover
ORDER BY stock_turnover DESC
LIMIT 10
""")

st.subheader(" Top 10 Products by Stock Turnover")
st.bar_chart(turnover_df.set_index("PRODUCT_NAME"))

st.caption("Insight: High stock turnover indicates strong demand and efficient inventory management.")
 
 
