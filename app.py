import streamlit as st
import pandas as pd
import plotly.express as px

# Title
st.set_page_config(layout="wide")
st.title("📱 iPhone Global Sales & Strategy Dashboard")

# Load data
df = pd.read_csv("iphone data.csv")

# Preprocess dates
df['Year'] = df['Quarter'].str.extract(r'(\d{4})').astype(int)
df['Q'] = df['Quarter'].str.extract(r'(Q\d)').squeeze()
quarter_map = {'Q1': '01', 'Q2': '04', 'Q3': '07', 'Q4': '10'}
df['Month'] = df['Q'].map(quarter_map)
df['Date'] = pd.to_datetime(df['Year'].astype(str) + '-' + df['Month'])

# Tabs for each analysis
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Sales Trends", 
    "💱 Currency & Revenue", 
    "📦 Product Allocation", 
    "🎯 Strategy & Insights"
])

# =======================
# Tab 1: Sales Trends
# =======================
with tab1:
    st.subheader("Regional iPhone Sales Over Time")
    region_trend = df.groupby(['Date', 'Region'])['Units Sold'].sum().reset_index()
    fig = px.line(region_trend, x='Date', y='Units Sold', color='Region', markers=True)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Sales by iPhone Model")
    model_trend = df.groupby(['Date', 'iPhone Model'])['Units Sold'].sum().reset_index()
    fig2 = px.line(model_trend, x='Date', y='Units Sold', color='iPhone Model')
    st.plotly_chart(fig2, use_container_width=True)

# =======================
# Tab 2: Currency & Revenue
# =======================
with tab2:
    st.subheader("Exchange Rate Volatility")
    ex_rate = df.groupby(['Date', 'Currency'])['Exchange Rate'].mean().reset_index()
    fig3 = px.line(ex_rate, x='Date', y='Exchange Rate', color='Currency')
    st.plotly_chart(fig3, use_container_width=True)

    st.subheader("Revenue Variance Due to Exchange Rates")
    df['Revenue Diff'] = df['Revenue (USD)'] - (df['Revenue (Local)'] * df['Exchange Rate'])
    revenue_vol = df.groupby('Currency')['Revenue Diff'].mean().reset_index()
    fig4 = px.bar(revenue_vol, x='Currency', y='Revenue Diff', title="Avg Revenue Difference (USD)")
    st.plotly_chart(fig4, use_container_width=True)

# =======================
# Tab 3: Product Allocation
# =======================
with tab3:
    st.subheader("Average Units Sold & Revenue Efficiency")
    df['Revenue_per_Unit'] = df['Revenue (USD)'] / df['Units Sold']
    allocation = df.groupby(['Region', 'iPhone Model']).agg({
        'Units Sold': 'mean',
        'Revenue_per_Unit': 'mean'
    }).reset_index().sort_values(by=['Units Sold', 'Revenue_per_Unit'], ascending=False)

    st.dataframe(allocation.head(10), use_container_width=True)

    st.subheader("Top Recommended Region-Model Allocation")
    top_alloc = allocation.groupby('Region').head(1).sort_values(by='Revenue_per_Unit', ascending=False)
    st.dataframe(top_alloc, use_container_width=True)

# =======================
# Tab 4: Strategic Insights
# =======================
with tab4:
    st.subheader("📌 Key Recommendations")
    st.markdown("""
    - ✅ **Prioritize iPhone 15 in EU** — High average units sold and highest revenue/unit.
    - ✅ **Expand iPhone 14 in US** — Strong consistent demand and profitability.
    - ⚠️ **Review Asian sales strategy** — Revenue/unit is disproportionately low (possibly currency misreporting or local pricing).
    - 💱 **Mitigate INR risk** — INR volatility impacts USD revenue heavily. Use hedging or dynamic pricing.
    - 📈 **Leverage Q4 holiday spikes** — Sales peak globally, ideal for launches and marketing.
    """)

    st.subheader("📎 Dataset Preview")
    st.dataframe(df.head(10), use_container_width=True)
