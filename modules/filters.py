import streamlit as st

def sidebar_location_filter(df):
    st.sidebar.subheader("📍 Precyzyjna lokalizacja")
    
    # 1. Prowincja
    prov_col = 'locationDetails/address/province/name'
    if prov_col in df.columns:
        provs = ["Wszystkie"] + sorted(df[prov_col].dropna().unique().tolist())
        prov = st.sidebar.selectbox("Województwo", options=provs)
        if prov != "Wszystkie":
            df = df[df[prov_col] == prov]

    # 2. Miasto
    city_col = 'locationDetails/address/city/name'
    if city_col in df.columns:
        cities = ["Wszystkie"] + sorted(df[city_col].dropna().unique().tolist())
        city = st.sidebar.selectbox("Miasto", options=cities)
        if city != "Wszystkie":
            df = df[df[city_col] == city]

    # 3. Dzielnica (Poziom 1 z reverseGeocoding)
    # Zazwyczaj locations/0/name to dzielnica
    dist_col = 'locationDetails/reverseGeocoding/locations/0/name'
    if dist_col in df.columns:
        dists = ["Wszystkie"] + sorted(df[dist_col].dropna().unique().tolist())
        dist = st.sidebar.selectbox("Dzielnica", options=dists)
        if dist != "Wszystkie":
            df = df[df[dist_col] == dist]

    # 4. Ulica
    street_col = 'locationDetails/address/street/name'
    if street_col in df.columns:
        streets = ["Wszystkie"] + sorted(df[street_col].dropna().unique().tolist())
        street = st.sidebar.selectbox("Ulica", options=streets)
        if street != "Wszystkie":
            df = df[df[street_col] == street]
            
    return df
