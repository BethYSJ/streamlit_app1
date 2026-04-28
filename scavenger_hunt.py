#import packages
import streamlit as st
import pandads as pd
import folium
from folium.plugins import HeatMap
import numpy as np
from streamlit_folium import st_folium

# writing title
st.write("Wuhan Detective App")

#side bar
st.sidebar.header("Settings")
st.sidebar.write("Testing text")
total_cases = st.sidebar.slider("Total cases", 100, 10000, 500)
cluster_pct = st.sidebar.slider("Percentage of cases near source", 10, 90, 70)
show_source = st.sidebar.checkbox("Reveal true source?")

#make synth data 
market_lat, market_long = 30.6195, 114.2577

chart_data = pd.DataFrame(
  np.random.randn(1000,2)/[50,50] + 
