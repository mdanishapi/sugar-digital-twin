import streamlit as st
import pandas as pd
import plotly.express as px

# --- PAGE CONFIG ---
st.set_page_config(page_title="Sugar Digital Twin", layout="wide")

# --- DATASET (Updated with 2025 Market Realities) ---
# Quetta recently hit record highs of 225-229 PKR/kg in late 2025.
market_data = pd.DataFrame({
    'City': ['Quetta', 'Peshawar', 'Karachi', 'Lahore', 'Islamabad'],
    'Retail_Price': [225, 200, 195, 210, 185],
    'Ex_Mill_Price': [170, 168, 165, 172, 168],
    'Current_Stock_MT': [15000, 45000, 120000, 250000, 35000],
    'Avg_Monthly_Cons_MT': [12000, 38000, 95000, 110000, 28000]
})

st.title("🇵🇰 MNFSR Sugar Sector Digital Twin")
tab1, tab2, tab3, tab4 = st.tabs(["📊 Executive Summary", "💸 Price & Spread", "📦 Inventory Deep-Dive", "⚖️ Policy Simulator"])

# --- TAB 2: PRICE & SPREAD ANALYSIS ---
with tab2:
    st.header("Detailed Price & Spread Analysis")
    st.info("The 'Spread' represents the markup between Ex-Mill gate prices and the final consumer price. High spreads indicate potential supply chain friction or hoarding.")
    
    market_data['Spread'] = market_data['Retail_Price'] - market_data['Ex_Mill_Price']
    
    col1, col2 = st.columns([2, 1])
    with col1:
        # Visualizing the Spread vs Prices
        fig_spread = px.bar(market_data, x='City', y=['Ex_Mill_Price', 'Spread'], 
                            title="Price Component Breakdown (PKR/kg)",
                            barmode='stack', color_discrete_sequence=['#1f77b4', '#ef553b'])
        st.plotly_chart(fig_spread, use_container_width=True)
        
    with col2:
        st.write("### 🚨 Spread Alerts")
        highest_spread_city = market_data.loc[market_data['Spread'].idxmax()]
        st.error(f"**Critical Spread:** {highest_spread_city['City']} has a markup of {highest_spread_city['Spread']} PKR/kg.")
        st.warning("Note: Quetta prices (225+) reflect high logistics costs and regional supply tightening.")

# --- TAB 3: INVENTORY DEEP-DIVE ---
with tab3:
    st.header("National & Regional Stock Surveillance")
    
    # Calculate Stock Coverage (Days)
    # Formula: (Current Stock / Monthly Consumption) * 30 days
    market_data['Days_Remaining'] = (market_data['Current_Stock_MT'] / market_data['Avg_Monthly_Cons_MT']) * 30
    
    c1, c2, c3 = st.columns(3)
    total_stock = market_data
