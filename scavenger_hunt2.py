import streamlit as st
import pandas as pd
import numpy as np
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium

st.title("Outbreak Investigator")
st.write("Adjust the settings in the sidebar, then try to identify the source of the outbreak from the map.")

# --- SIDEBAR CONTROLS ---
st.sidebar.header("Settings")
total_cases = st.sidebar.slider("Total cases", 100, 1000, 500)
cluster_pct = st.sidebar.slider("% of cases near the source", 10, 90, 70)
show_source = st.sidebar.checkbox("Reveal the true source")

# --- GENERATE SYNTHETIC DATA ---
market_lat, market_lon = 30.6195, 114.2577

cluster_count = int(total_cases * cluster_pct / 100)
noise_count = total_cases - cluster_count

np.random.seed(420)
cluster_lats = np.random.normal(market_lat, 0.005, cluster_count)
cluster_lons = np.random.normal(market_lon, 0.005, cluster_count)
noise_lats = np.random.uniform(30.50, 30.70, noise_count)
noise_lons = np.random.uniform(114.20, 114.40, noise_count)

cases = pd.DataFrame({
    'lat': np.concatenate([cluster_lats, noise_lats]),
    'lon': np.concatenate([cluster_lons, noise_lons]),
})

pois = pd.DataFrame({
    'name': ['Wuhan International Plaza', 'Huanan Seafood Market', 'Hankou Railway Station', 'Wuhan CDC'],
    'lat':  [30.584,   30.6195, 30.618, 30.612],
    'lon':  [114.271,  114.2577, 114.250, 114.265],
    'is_source': [False, True, False, False],
})

# --- SHOW STATS ---
st.write(f"**Total cases:** {total_cases} — **Clustered:** {cluster_count} — **Scattered:** {noise_count}")

# --- BUILD MAP ---
m = folium.Map(location=[30.61, 114.28], zoom_start=13, tiles='cartodbpositron')

HeatMap(cases[['lat', 'lon']].values.tolist(), radius=12, blur=15).add_to(m)

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

st_folium(m, width=900, height=550)