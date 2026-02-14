# Snowflake Supply Chain Analytics  
### Cloud-Based Analytics System using Snowflake & Streamlit

---

##  Project Overview

This project is an end-to-end Supply Chain Analytics Platform built using:

- Snowflake as a cloud data warehouse  
- Streamlit for interactive visualization  
- GitHub + Streamlit Cloud for deployment  

The platform enables real-time analysis of warehouse performance, inventory efficiency, revenue trends, and product-level insights.

---

##  Architecture

Snowflake (Cloud Data Warehouse)  
        ↓  
SQL Views (Business Semantic Layer)  
        ↓  
Streamlit Dashboard (Visualization Layer)  
        ↓  
Streamlit Cloud Deployment  

---

##  Dataset Overview

Synthetic enterprise-scale dataset including:

- 50 Products  
- 10 Warehouses  
- 500 Inventory records  
- 5,000+ Sales transactions  

The dataset simulates a multi-warehouse retail distribution environment.

---

##  Data Engineering & Cleaning

Performed:

- Duplicate detection checks  
- Null validation  
- Business rule validation (selling price > cost price)  
- Referential integrity checks  
- Structured dimensional modeling (Fact & Dimension tables)  

---

##  Key Features

###  Revenue KPIs
- Total Revenue
- Total Units Sold

###  Trend Analysis
- Monthly Revenue Growth

###  Warehouse Analytics
- Revenue Ranking by Warehouse
- Performance comparison

###  Product Intelligence
- Slow-moving products detection
- Category-level revenue breakdown

###  Inventory Optimization
- Stock Turnover Ratio (Top 10 Products)

---

##  Data Modeling

Dimension Tables:
- products
- warehouses

Fact Tables:
- sales
- inventory

Business Views:
- v_total_revenue
- v_warehouse_performance
- v_product_performance
- v_stock_turnover

---

##  Tech Stack

- Python
- Snowflake
- SQL
- Streamlit
- Pandas
- GitHub
- Streamlit Cloud

---

##  Security

Snowflake credentials are securely stored using st.secrets and are not hardcoded in the application.

 
---

##  Business Impact

This platform enables:

- Identification of high-performing warehouses  
- Detection of low-performing inventory  
- Revenue trend monitoring  
- Inventory efficiency optimization  
- Data-driven supply chain decisions  

---

 
 
