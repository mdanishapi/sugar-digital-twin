import streamlit as st
import pandas as pd
import plotly.express as px
import google.generativeai as genai

# Page Config
st.set_page_config(page_title="Sugar Industry Digital Twin", layout="wide", initial_sidebar_state="expanded")

# Initialize Gemini
try:
    # Use st.secrets to get the key from Streamlit Cloud dashboard
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.sidebar.warning("Gemini API Key not found in Secrets. AI features disabled.")
    model = None

# Custom CSS for a "Digital Twin" look
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

st.title("🚜 Sugar Industry Digital Twin")
st.markdown("---")

# Sidebar - Controls
st.sidebar.header("Factory Parameters")
crushing_capacity = st.sidebar.slider("Crushing Capacity (Tons/Day)", 1000, 15000, 8000)
recovery_rate = st.sidebar.slider("Recovery Rate (%)", 8.0, 14.0, 10.5)
market_price = st.sidebar.number_input("Market Price (per kg)", 50, 250, 140)

# Main Dashboard Layout
col1, col2, col3, col4 = st.columns(4)
daily_production = (crushing_capacity * recovery_rate) / 100
daily_revenue = (daily_production * 1000) * market_price

col1.metric("Daily Production", f"{daily_production:,.0f} kg")
col2.metric("Daily Revenue", f"PKR {daily_revenue:,.0f}")
col3.metric("Recovery Efficiency", f"{recovery_rate}%")
col4.metric("Status", "Operational", delta="Optimal")

# Map & Analytics
st.subheader("Regional Crop Health & Logistics")
tab1, tab2 = st.tabs(["Geospatial Twin", "AI Insights"])

with tab1:
    # Mock data for sugar mills/regions
    data = {
        'Region': ['Sargodha', 'Faisalabad', 'Hyderabad', 'Badin', 'Mardan'],
        'lat': [32.08, 31.45, 25.39, 24.65, 34.19],
        'lon': [72.67, 73.13, 68.37, 68.83, 72.04],
        'Yield_Index': [95, 88, 92, 78, 82]
    }
    df = pd.DataFrame(data)
    fig = px.scatter_mapbox(df, lat="lat", lon="lon", size="Yield_Index", 
                            color="Yield_Index", hover_name="Region",
                            color_continuous_scale=px.colors.sequential.Greens,
                            zoom=5, height=500)
    fig.update_layout(mapbox_style="carto-positron", margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig, use_container_with_width=True)

with tab2:
    st.write("### AI Process Advisor")
    user_query = st.text_input("Ask the Digital Twin (e.g., 'How can I improve recovery rate when humidity is high?')")
    
    if user_query:
        if model:
            with st.spinner("Analyzing data..."):
                prompt = f"As a Sugar Industry Expert, answer this based on a plant with {crushing_capacity} TCD capacity and {recovery_rate}% recovery: {user_query}"
                response = model.generate_content(prompt)
                st.info(response.text)
        else:
            st.error("Please add 'GEMINI_API_KEY' to Streamlit Secrets to use this feature.")

# Bottom Footer
st.markdown("---")
st.caption("Digital Twin Interface v1.2 | Real-time sensor simulation active.")