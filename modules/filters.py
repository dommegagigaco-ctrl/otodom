import streamlit as st

def sidebar_location_filter(df):
    params = st.query_params

    st.sidebar.subheader("💰 Zakresy")

    # --- CENA ---
    min_price = int(df['price'].min())
    max_price = int(df['price'].max())
    saved_price_min = int(params.get("price_min", min_price))
    saved_price_max = int(params.get("price_max", max_price))
    saved_price_min = max(min_price, min(saved_price_min, max_price))
    saved_price_max = max(min_price, min(saved_price_max, max_price))
    price_range = st.sidebar.slider(
        "Zakres cen (PLN):", min_price, max_price,
        (saved_price_min, saved_price_max), key="price_range"
    )
    st.query_params["price_min"] = price_range[0]
    st.query_params["price_max"] = price_range[1]
    df = df[(df['price'] >= price_range[0]) & (df['price'] <= price_range[1])]

    # --- METRAŻ ---
    min_sqm = float(df['areaSqm'].min())
    max_sqm = float(df['areaSqm'].max())
    saved_sqm_min = float(params.get("sqm_min", min_sqm))
    saved_sqm_max = float(params.get("sqm_max", max_sqm))
    saved_sqm_min = max(min_sqm, min(saved_sqm_min, max_sqm))
    saved_sqm_max = max(min_sqm, min(saved_sqm_max, max_sqm))
    area_range = st.sidebar.slider(
        "Metraż (m²):", min_sqm, max_sqm,
        (saved_sqm_min, saved_sqm_max), key="area_range"
    )
    st.query_params["sqm_min"] = area_range[0]
    st.query_params["sqm_max"] = area_range[1]
    df = df[(df['areaSqm'] >= area_range[0]) & (df['areaSqm'] <= area_range[1])]

    # --- CENA ZA M² ---
    psqm_col = 'listingDetails/pricePerSquareMeter/value'
    if psqm_col in df.columns:
        df[psqm_col] = pd.to_numeric(df[psqm_col], errors='coerce')
        df_psqm = df[psqm_col].dropna()
        if not df_psqm.empty:
            min_psqm = int(df_psqm.min())
            max_psqm = int(df_psqm.max())
            saved_psqm_min = int(params.get("psqm_min", min_psqm))
            saved_psqm_max = int(params.get("psqm_max", max_psqm))
            saved_psqm_min = max(min_psqm, min(saved_psqm_min, max_psqm))
            saved_psqm_max = max(min_psqm, min(saved_psqm_max, max_psqm))
            psqm_range = st.sidebar.slider(
                "Cena za m² (PLN):", min_psqm, max_psqm,
                (saved_psqm_min, saved_psqm_max), key="psqm_range"
            )
            st.query_params["psqm_min"] = psqm_range[0]
            st.query_params["psqm_max"] = psqm_range[1]
            df = df[(df[psqm_col] >= psqm_range[0]) & (df[psqm_col] <= psqm_range[1])]

    st.sidebar.subheader("📍 Precyzyjna lokalizacja")

    # --- WOJEWÓDZTWO ---
    prov_col = 'locationDetails/address/province/name'
    if prov_col in df.columns:
        provs = ["Wszystkie"] + sorted(df[prov_col].dropna().unique().tolist())
        saved_prov = params.get("prov", "Wszystkie")
        prov_idx = provs.index(saved_prov) if saved_prov in provs else 0
        prov = st.sidebar.selectbox("Województwo", options=provs, index=prov_idx, key="prov_sel")
        st.query_params["prov"] = prov
        if prov != "Wszystkie":
            df = df[df[prov_col] == prov]

    # --- MIASTO ---
    city_col = 'locationDetails/address/city/name'
    if city_col in df.columns:
        cities = ["Wszystkie"] + sorted(df[city_col].dropna().unique().tolist())
        saved_city = params.get("city", "Wszystkie")
        city_idx = cities.index(saved_city) if saved_city in cities else 0
        city = st.sidebar.selectbox("Miasto", options=cities, index=city_idx, key="city_sel")
        st.query_params["city"] = city
        if city != "Wszystkie":
            df = df[df[city_col] == city]

    # --- DZIELNICA ---
    dist_col = 'locationDetails/reverseGeocoding/locations/0/name'
    if dist_col in df.columns:
        dists = ["Wszystkie"] + sorted(df[dist_col].dropna().unique().tolist())
        saved_dist = params.get("dist", "Wszystkie")
        dist_idx = dists.index(saved_dist) if saved_dist in dists else 0
        dist = st.sidebar.selectbox("Dzielnica", options=dists, index=dist_idx, key="dist_sel")
        st.query_params["dist"] = dist
        if dist != "Wszystkie":
            df = df[df[dist_col] == dist]

    return df
