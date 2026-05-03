import streamlit as st

def sidebar_location_filter(df):
    st.sidebar.subheader("📍 Precyzyjna lokalizacja")
    city = st.sidebar.selectbox("Miasto", options=["Wszystkie"] + sorted(df['city'].dropna().unique().tolist()))
    if city != "Wszystkie":
        df = df[df['city'] == city]
    return df
