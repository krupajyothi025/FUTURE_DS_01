import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ==========================
# Modern Dashboard Settings
# ==========================
st.set_page_config(
    page_title="Sales Analytics Dashboard",
    layout="wide",
)

# ==========================
# CUSTOM CSS FOR PROFESSIONAL LOOK
# ==========================
st.markdown("""
    <style>
    .big-font {
        font-size:28px !important;
        font-weight:bold;
    }
    .kpi-box {
        padding: 20px;
        border-radius: 10px;
        background-color: #f8f9fa;
        text-align: center;
        border: 1px solid #ddd;
    }
    .section-title {
        font-size:22px !important;
        font-weight:bold;
        margin-top:20px;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================
# LOAD DATA
# ==========================
df = pd.read_csv("sales_data.csv")
df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Month'] = df['Order Date'].dt.month_name()

# ==========================
# SIDEBAR FILTERS
# ==========================
st.sidebar.header("🔍 Filter Your Data")
region = st.sidebar.multiselect("Select Regions", df['Region'].unique(), df['Region'].unique())
category = st.sidebar.multiselect("Select Category", df['Category'].unique(), df['Category'].unique())

filtered_df = df[(df['Region'].isin(region)) & (df['Category'].isin(category))]

# ==========================
# DASHBOARD TITLE
# ==========================
st.markdown("<h1 class='big-font'>📊 Sales Performance Dashboard</h1>", unsafe_allow_html=True)
st.write("An interactive dashboard to explore business sales trends, categories, regions and profitability.")

# ==========================
# KPI CARDS
# ==========================
total_sales = int(filtered_df['Sales'].sum())
total_profit = int(filtered_df['Profit'].sum())
total_orders = int(filtered_df.shape[0])

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"<div class='kpi-box'><h3>Total Sales</h3><h2>₹{total_sales:,}</h2></div>", unsafe_allow_html=True)

with col2:
    st.markdown(f"<div class='kpi-box'><h3>Total Profit</h3><h2>₹{total_profit:,}</h2></div>", unsafe_allow_html=True)

with col3:
    st.markdown(f"<div class='kpi-box'><h3>Total Orders</h3><h2>{total_orders:,}</h2></div>", unsafe_allow_html=True)

# ==========================
# MONTHLY SALES TREND
# ==========================
st.markdown("<p class='section-title'>📈 Monthly Sales Trend</p>", unsafe_allow_html=True)
monthly_sales = filtered_df.groupby('Month')['Sales'].sum().sort_values()

fig1, ax1 = plt.subplots()
monthly_sales.plot(kind="line", ax=ax1)
plt.xticks(rotation=45)
st.pyplot(fig1)

# ==========================
# REGION + CATEGORY CHARTS
# ==========================
colA, colB = st.columns(2)

with colA:
    st.markdown("<p class='section-title'>🌍 Sales by Region</p>", unsafe_allow_html=True)
    region_sales = filtered_df.groupby('Region')['Sales'].sum()
    fig2, ax2 = plt.subplots()
    region_sales.plot(kind='bar', ax=ax2)
    st.pyplot(fig2)

with colB:
    st.markdown("<p class='section-title'>📦 Sales by Category</p>", unsafe_allow_html=True)
    category_sales = filtered_df.groupby('Category')['Sales'].sum()
    fig3, ax3 = plt.subplots()
    category_sales.plot(kind='bar', ax=ax3)
    st.pyplot(fig3)

# ==========================
# TOP PRODUCTS
# ==========================
st.markdown("<p class='section-title'>🏆 Top 10 Products</p>", unsafe_allow_html=True)

top_products = (
    filtered_df.groupby('Product Name')['Sales']
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

fig4, ax4 = plt.subplots()
top_products.plot(kind='bar', ax=ax4)
plt.xticks(rotation=45)
st.pyplot(fig4)