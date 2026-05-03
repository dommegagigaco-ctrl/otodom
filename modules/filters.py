import streamlit as st

def sidebar_location_filter(df):
    st.sidebar.subheader("📍 Precyzyjna lokalizacja")
    
    # Filtr Miasta
    cities = ["Wszystkie"] + sorted(df['city'].dropna().unique().tolist())
    city = st.sidebar.selectbox("Miasto", options=cities)
    
    if city != "Wszystkie":
        df = df[df['city'] == city]
        
    # Filtr Dzielnicy (z reverseGeocoding)
    loc_col = 'locationDetails/reverseGeocoding/locations/0/name'
    if loc_col in df.columns:
        districts = ["Wszystkie"] + sorted(df[loc_col].dropna().unique().tolist())
        dist = st.sidebar.selectbox("Dzielnica / Obszar", options=districts)
        if dist != "Wszystkie":
            df = df[df[loc_col] == dist]
            
    return df
