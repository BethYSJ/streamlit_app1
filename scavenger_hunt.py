#import packages
import streamlit as st
import pandas as pd
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
market_lat, market_lon = 30.6195, 114.2577

cluster_count = int(total_cases * cluster_pct/100)
noise_count = total_cases - cluster_count

cluster_lats = np.random.normal(market_lat, 0.005, cluster_count)
cluster_lons = np.random.normal(market_lon, 0.005, cluster_count)

noise_lats = np.random.uniform(30.5, 30.7, noise_count)
noise_lons = np.random.uniform(114.2, 114.4, noise_count)

cases = pd.DataFrame({
  'lat': np.concate([cluster_lats, noise_lats]),
  'lon': np.concate([cluster_lons, noise_lons])})

pois = pd.DataFrame({
    'name': ['Wuhan International Plaza', 'Huanan Seafood Market', 'Hankou Railway Station', 'Wuhan CDC'],
    'lat':  [30.584,   30.6195, 30.618, 30.612],
    'lon':  [114.271,  114.2577, 114.250, 114.265],
    'is_source': [False, True, False, False]
})

# build map

m = folium.Map(location = [30.61, 114.28],
               zoom_start = 13,
               tiles = 'cartodbpositron'
              )
HeatMap(cases[['lat', 'lon']].values.to.list(), raduis = 12, blur =15).add_to(m)

for _, poi in pois.iterrows():
    if poi['is_source'] and show_source:
        color = 'red'
        label = f"TRUE SOURCE: {poi['name']}"
    else:
        color = 'black'
        label = poi['name']

    folium.Marker(
        location=[poi['lat'], poi['lon']],
        popup=label,
        tooltip=label,
        icon=folium.Icon(color=color, icon='question-sign'),
    ).add_to(m)
  
st_folium(m, width = 900, height = 550)

                     
