import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("📊 iPhone Sales Analytics & Allocation Optimizer")

# --- File Upload ---
uploaded_file = st.file_uploader("📂 Upload your iPhone sales CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # --- Preprocessing ---
    df['Year'] = df['Quarter'].str.extract(r'(\d{4})').astype(int)
    df['Q'] = df['Quarter'].str.extract(r'(Q\d)').squeeze()
    quarter_map = {'Q1': '01', 'Q2': '04', 'Q3': '07', 'Q4': '10'}
    df['Month'] = df['Q'].map(quarter_map)
    df['Date'] = pd.to_datetime(df['Year'].astype(str) + '-' + df['Month'])

    st.success("✅ Data successfully uploaded and processed!")
    st.dataframe(df.head(), use_container_width=True)

    tab1, tab2, tab3 = st.tabs([
        "📍 Sales Trends", 
        "💱 Currency & Revenue", 
        "📦 Product Allocation"
    ])

    # ---------------------------
    # Tab 1: Regional Sales Trends
    # ---------------------------
    with tab1:
        st.subheader("📍 Regional iPhone Sales Trends")
        regional_sales = df.groupby(['Date', 'Region'])['Units Sold'].sum().reset_index()
        fig1 = px.line(regional_sales, x='Date', y='Units Sold', color='Region', markers=True)
        st.plotly_chart(fig1, use_container_width=True)

        st.subheader("📍 Sales Trends by iPhone Model")
        model_sales = df.groupby(['Date', 'iPhone Model'])['Units Sold'].sum().reset_index()
        fig2 = px.line(model_sales, x='Date', y='Units Sold', color='iPhone Model')
        st.plotly_chart(fig2, use_container_width=True)

    # ---------------------------
    # Tab 2: Currency & Revenue Analysis
    # ---------------------------
    with tab2:
        st.subheader("💱 Exchange Rate Volatility")
        ex_trend = df.groupby(['Date', 'Currency'])['Exchange Rate'].mean().reset_index()
        fig3 = px.line(ex_trend, x='Date', y='Exchange Rate', color='Currency')
        st.plotly_chart(fig3, use_container_width=True)

        st.subheader("💵 Revenue Difference Due to Currency")
        df['Revenue Diff'] = df['Revenue (USD)'] - (df['Revenue (Local)'] * df['Exchange Rate'])
        avg_diff = df.groupby('Currency')['Revenue Diff'].mean().reset_index()
        fig4 = px.bar(avg_diff, x='Currency', y='Revenue Diff',
                      title='Average Revenue Difference (USD)')
        st.plotly_chart(fig4, use_container_width=True)

    # ---------------------------
    # Tab 3: Product Allocation Optimization
    # ---------------------------
    with tab3:
        st.subheader("📦 Product Allocation Strategy")
        df['Revenue_per_Unit'] = df['Revenue (USD)'] / df['Units Sold']

        alloc = df.groupby(['Region', 'iPhone Model']).agg({
            'Units Sold': 'mean',
            'Revenue_per_Unit': 'mean'
        }).reset_index().sort_values(by=['Units Sold', 'Revenue_per_Unit'], ascending=False)

        st.markdown("### 🔝 Top 10 Region-Model Combinations")
        st.dataframe(alloc.head(10), use_container_width=True)

        top_alloc = alloc.groupby('Region').head(1).sort_values(by='Revenue_per_Unit', ascending=False)
        st.markdown("### ✅ Best iPhone Model Allocation per Region")
        st.dataframe(top_alloc, use_container_width=True)

else:
    st.info("👈 Please upload a CSV file to start the analysis.")
