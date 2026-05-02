import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# 1. Konfiguracja strony
st.set_page_config(layout="wide")
st.title("Real Estate Dashboard: Praga-Północ")

# 2. Połączenie z arkuszem
conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read(spreadsheet="https://docs.google.com/spreadsheets/d/13skyeoJL9MZvM5iCRtHUI7tyfu9BHArse154eizQ_L8/edit")

# 3. Sidebar - Filtry (wykorzystując Twoje nowe nagłówki)
st.sidebar.header("Filtry")
min_price = st.sidebar.slider("Cena od", 0, int(df['price'].max()), 0)
max_price = st.sidebar.slider("Cena do", 0, int(df['price'].max()), int(df['price'].max()))
rooms = st.sidebar.multiselect("Liczba pokoi", options=df['rooms'].unique())

# 4. Filtrowanie danych
filtered_df = df[(df['price'] >= min_price) & (df['price'] <= max_price)]
if rooms:
    filtered_df = filtered_df[filtered_df['rooms'].isin(rooms)]

# 5. Wyświetlanie
st.metric("Liczba ofert", len(filtered_df))
st.dataframe(filtered_df[['title', 'price', 'areaSqm', 'pricePerSqm', 'url']])

# 6. Wykresy (np. rozkład cen)
st.bar_chart(filtered_df.set_index('title')['price'])
