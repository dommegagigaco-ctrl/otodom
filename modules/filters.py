import streamlit as st

def sidebar_location_filter(df):
    st.sidebar.subheader("💰 Zakres cenowy")
    
    # 1. Filtr cenowy
    min_price = int(df['price'].min())
    max_price = int(df['price'].max())
    price_range = st.sidebar.slider("Zakres cen (PLN):", min_price, max_price, (min_price, max_price))
    df = df[(df['price'] >= price_range[0]) & (df['price'] <= price_range[1])]

    # 2. NOWOŚĆ: Filtr powierzchni
    st.sidebar.subheader("📐 Powierzchnia (m²)")
    min_sqm = float(df['areaSqm'].min())
    max_sqm = float(df['areaSqm'].max())
    area_range = st.sidebar.slider("Wybierz metraż (m²):", min_sqm, max_sqm, (min_sqm, max_sqm))
    df = df[(df['areaSqm'] >= area_range[0]) & (df['areaSqm'] <= area_range[1])]

    # 3. Filtry lokalizacji
    st.sidebar.subheader("📍 Precyzyjna lokalizacja")
    
    prov_col = 'locationDetails/address/province/name'
    if prov_col in df.columns:
        provs = ["Wszystkie"] + sorted(df[prov_col].dropna().unique().tolist())
        prov = st.sidebar.selectbox("Województwo", options=provs)
        if prov != "Wszystkie":
            df = df[df[prov_col] == prov]

    city_col = 'locationDetails/address/city/name'
    if city_col in df.columns:
        cities = ["Wszystkie"] + sorted(df[city_col].dropna().unique().tolist())
        city = st.sidebar.selectbox("Miasto", options=cities)
        if city != "Wszystkie":
            df = df[df[city_col] == city]

    dist_col = 'locationDetails/reverseGeocoding/locations/0/name'
    if dist_col in df.columns:
        dists = ["Wszystkie"] + sorted(df[dist_col].dropna().unique().tolist())
        dist = st.sidebar.selectbox("Dzielnica", options=dists)
        if dist != "Wszystkie":
            df = df[df[dist_col] == dist]
            
    return df
