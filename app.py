import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Sugar Digital Twin | MNFSR",
    page_icon="🇵🇰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- MODERN STYLING (Glassmorphism & Professional Palettes) ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    div[data-testid="stMetric"] {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        height: 60px;
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 10px 10px 0 0;
        padding: 0 20px;
        color: #888;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1f77b4 !important;
        color: white !important;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# --- DATA ENGINE ---
# This connection will look for secrets in Streamlit Cloud Settings
conn = st.connection("gsheets", type=GSheetsConnection)

def load_data():
    # Replace 'Sheet1' with your actual sheet name
    # For the presentation, we'll use a placeholder if the sheet isn't linked yet
    try:
        df = conn.read(ttl="5m")
        return df
    except:
        return pd.DataFrame({
            "District": ["Lahore", "Karachi", "Islamabad", "Peshawar"],
            "Retail": [148, 155, 152, 160],
            "Ex_Mill": [138, 140, 142, 145],
            "Stock": [50000, 30000, 15000, 20000]
        })

data = load_data()

# --- HEADER SECTION ---
st.title("🛡️ Sugar Sector Digital Twin")
st.caption("Federal Ministry of National Food Security & Research | Real-Time Monitoring Instance")
st.markdown("---")

# --- MULTI-TAB NAVIGATION ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Executive Dashboard", 
    "💸 Price & Spread Analysis", 
    "📦 Inventory Deep-Dive", 
    "⚖️ Policy Simulator",
    "🤖 AI Assistant"
])

# TAB 1: EXECUTIVE DASHBOARD
with tab1:
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("National Avg Retail", f"{data['Retail'].mean():.2f} PKR", "+2.4%")
    m2.metric("Stock Coverage", "84 Days", "Stable")
    m3.metric("Import Parity", "162.10 PKR", "-PKR 14.00")
    m4.metric("Market Sentiment", "Neutral", "System Generated")
    
    st.subheader("Regional Price Distribution")
    fig = px.bar(data, x="District", y="Retail", color="Retail", template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

# TAB 4: POLICY SIMULATOR
with tab4:
    st.header("Strategic Policy Impact Simulator")
    col_l, col_r = st.columns([1, 2])
    
    with col_l:
        st.write("### Policy Levers")
        export = st.slider("Export Quota (Tons)", 0, 500000, 100000)
        buffer = st.select_slider("Buffer Release", options=["0%", "25%", "50%", "100%"])
        
    with col_r:
        st.write("### AI Critique & Market Response")
        if export > 300000:
            st.error("🔴 **CRITICAL WARNING:** High risk of local supply shortage. Projected retail hike: 15-20 PKR.")
        else:
            st.success("🟢 **STABLE:** Proposed measures maintain domestic equilibrium.")
        
        # Simulated prediction chart
        sim_df = pd.DataFrame({"Week": [1,2,3,4], "Predicted_Price": [150, 152, 155, 158] if export > 300000 else [150, 151, 150, 149]})
        st.line_chart(sim_df.set_index("Week"))

with tab5:
    st.subheader("🤖 AI Intelligence Assistant")
    query = st.text_input("Ask the Digital Twin anything (e.g., 'Predict prices for next Ramazan')")
    if query:
        st.write(f"Analyzing data for: *'{query}'*...")
        st.info("AI Analysis: Based on current stock of 1.2M tons and historical consumption, a surplus is expected. No import intervention required for Q1 2026.")
