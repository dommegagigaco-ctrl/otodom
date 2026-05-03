import streamlit as st

def sidebar_location_filter(df):
    st.sidebar.subheader("💰 Zakres cenowy")
    
    # 1. Filtr cenowy (widełki)
    min_val = int(df['price'].min())
    max_val = int(df['price'].max())
    price_range = st.sidebar.slider("Wybierz zakres cen (PLN):", min_val, max_val, (min_val, max_val))
    df = df[(df['price'] >= price_range[0]) & (df['price'] <= price_range[1])]

    st.sidebar.subheader("📍 Precyzyjna lokalizacja")
    
    # 2. Prowincja
    prov_col = 'locationDetails/address/province/name'
    if prov_col in df.columns:
        provs = ["Wszystkie"] + sorted(df[prov_col].dropna().unique().tolist())
        prov = st.sidebar.selectbox("Województwo", options=provs)
        if prov != "Wszystkie":
            df = df[df[prov_col] == prov]

    # 3. Miasto
    city_col = 'locationDetails/address/city/name'
    if city_col in df.columns:
        cities = ["Wszystkie"] + sorted(df[city_col].dropna().unique().tolist())
        city = st.sidebar.selectbox("Miasto", options=cities)
        if city != "Wszystkie":
            df = df[df[city_col] == city]

    # 4. Dzielnica
    dist_col = 'locationDetails/reverseGeocoding/locations/0/name'
    if dist_col in df.columns:
        dists = ["Wszystkie"] + sorted(df[dist_col].dropna().unique().tolist())
        dist = st.sidebar.selectbox("Dzielnica", options=dists)
        if dist != "Wszystkie":
            df = df[df[dist_col] == dist]

    return df
