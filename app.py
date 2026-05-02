import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("🏠 Otodom Analiza Premium")

# Wczytanie danych
url = "https://docs.google.com/spreadsheets/d/13skyeoJL9MZvM5iCRtHUI7tyfu9BHArse154eizQ_L8/export?format=csv&gid=0"
df = pd.read_csv(url)

# 1. Moduł: Zaawansowane Filtrowanie
st.sidebar.header("Filtry")
min_m2 = st.sidebar.number_input("Min. Metraż", value=0)
max_price = st.sidebar.number_input("Max. Cena", value=int(df['price'].max()))
df_f = df[(df['areaSqm'] >= min_m2) & (df['price'] <= max_price)]

# 2. Moduł: Statystyki (Kluczowe wskaźniki)
col1, col2, col3 = st.columns(3)
col1.metric("Liczba ofert", len(df_f))
col2.metric("Średnia cena", f"{int(df_f['price'].mean()):,} PLN")
col3.metric("Mediana za m²", f"{int(df_f['pricePerSqm'].median()):,} PLN")

# 3. Moduł: Wykrywacz Okazji (z użyciem logiki)
st.subheader("🎯 Okazje Inwestycyjne (poniżej 90% mediany)")
okazje = df_f[df_f['pricePerSqm'] < (df_f['pricePerSqm'].median() * 0.9)]
st.dataframe(okazje[['title', 'price', 'areaSqm', 'pricePerSqm', 'url']], use_container_width=True)

# 4. Moduł: Wizualizacja
st.subheader("Rozkład cen w dzielnicach")
fig = px.scatter(df_f, x='areaSqm', y='price', color='district', hover_data=['title'])
st.plotly_chart(fig, use_container_width=True)
