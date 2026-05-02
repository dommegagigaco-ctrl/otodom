import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("🏠 Otodom: Łowca Okazji")

url = "https://docs.google.com/spreadsheets/d/13skyeoJL9MZvM5iCRtHUI7tyfu9BHArse154eizQ_L8/export?format=csv&gid=0"
df = pd.read_csv(url)

# Używane kolumny
psqm_col = 'listingDetails/pricePerSquareMeter/value'
price_col = 'price'

# 1. Obliczenie Mediany Rynkowej
rynek_median_psqm = df[psqm_col].median()

# 2. Sidebar - Filtrowanie okazji
st.sidebar.header("Filtry Inwestycyjne")
procent_okazji = st.sidebar.slider("Szukaj ofert tańszych o (min %):", 5, 30, 10)
df['czy_okazja'] = df[psqm_col] < (rynek_median_psqm * (1 - procent_okazji/100))

# 3. Sekcja Okazji
st.subheader(f"🎯 Okazje (poniżej {procent_okazji}% średniej rynkowej)")
okazje = df[df['czy_okazja'] == True].sort_values(by=psqm_col)
st.dataframe(okazje[['title', price_col, psqm_col, 'url']], use_container_width=True)

# 4. Wykres rozrzutu (Scatter)
st.subheader("Rynek: Cena za m² w zależności od metrażu")
fig = px.scatter(df, x='areaSqm', y=psqm_col, color='czy_okazja', 
                 hover_data=['title', price_col],
                 title="Okazje oznaczone na czerwono")
st.plotly_chart(fig, use_container_width=True)
