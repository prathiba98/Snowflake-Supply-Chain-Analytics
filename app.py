import streamlit as st
import snowflake.connector
import pandas as pd

st.set_page_config(page_title="Supply Chain Dashboard", layout="wide")

st.title(" Supply Chain & Inventory Intelligence Platform")

# Snowflake connection
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

# Load KPIs
kpi_df = run_query("SELECT * FROM v_total_revenue")

total_revenue = kpi_df["TOTAL_REVENUE"][0]
total_units = kpi_df["TOTAL_UNITS_SOLD"][0]

col1, col2 = st.columns(2)

col1.metric(" Total Revenue", f"₹ {int(total_revenue):,}")
col2.metric(" Total Units Sold", f"{int(total_units):,}")
