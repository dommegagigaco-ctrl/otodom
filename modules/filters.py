import streamlit as st

def sidebar_location_filter(df):
    st.sidebar.subheader("💰 Zakresy")
    
    # Filtry z unikalnymi kluczami (key=...)
    min_price = int(df['price'].min())
    max_price = int(df['price'].max())
    price_range = st.sidebar.slider("Zakres cen (PLN):", min_price, max_price, (min_price, max_price), key="price_range")
    df = df[(df['price'] >= price_range[0]) & (df['price'] <= price_range[1])]

    min_sqm = float(df['areaSqm'].min())
    max_sqm = float(df['areaSqm'].max())
    area_range = st.sidebar.slider("Metraż (m²):", min_sqm, max_sqm, (min_sqm, max_sqm), key="area_range")
    df = df[(df['areaSqm'] >= area_range[0]) & (df['areaSqm'] <= area_range[1])]

    st.sidebar.subheader("📍 Precyzyjna lokalizacja")
    
    prov_col = 'locationDetails/address/province/name'
    if prov_col in df.columns:
        provs = ["Wszystkie"] + sorted(df[prov_col].dropna().unique().tolist())
        prov = st.sidebar.selectbox("Województwo", options=provs, key="prov_sel")
        if prov != "Wszystkie":
            df = df[df[prov_col] == prov]

    city_col = 'locationDetails/address/city/name'
    if city_col in df.columns:
        cities = ["Wszystkie"] + sorted(df[city_col].dropna().unique().tolist())
        city = st.sidebar.selectbox("Miasto", options=cities, key="city_sel")
        if city != "Wszystkie":
            df = df[df[city_col] == city]

    dist_col = 'locationDetails/reverseGeocoding/locations/0/name'
    if dist_col in df.columns:
        dists = ["Wszystkie"] + sorted(df[dist_col].dropna().unique().tolist())
        dist = st.sidebar.selectbox("Dzielnica", options=dists, key="dist_sel")
        if dist != "Wszystkie":
            df = df[df[dist_col] == dist]
            
    return df
