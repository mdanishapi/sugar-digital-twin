
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Sugar Twin", layout="wide")
st.title("Sugar Industry Digital Twin")

# Basic Logic
price = st.slider("Simulate Market Price (Rs)", 100, 300, 175)
st.metric("Current Price", f"Rs. {price}")

# Simple Map Data
df = pd.DataFrame({
    'Region': ['Punjab', 'Sindh', 'KPK'],
    'lat': [31.17, 25.89, 34.01],
    'lon': [72.70, 68.52, 71.52],
    'Yield': [92, 85, 78]
})

fig = px.scatter_mapbox(df, lat="lat", lon="lon", size="Yield", 
                        zoom=4, mapbox_style="carto-positron")
st.plotly_chart(fig)
