import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("🏠 Otodom Analiza Premium")

# Wczytanie danych
url = "https://docs.google.com/spreadsheets/d/13skyeoJL9MZvM5iCRtHUI7tyfu9BHArse154eizQ_L8/export?format=csv&gid=0"
df = pd.read_csv(url)

# Definicja kolumn (używamy Twoich nazw)
price_col = 'price' 
psqm_col = 'listingDetails/pricePerSquareMeter/value'

# Filtry
st.sidebar.header("Filtry")
min_price = st.sidebar.number_input("Min. Cena", value=0)
df_f = df[df[price_col] >= min_price]

# Metryki
col1, col2, col3 = st.columns(3)
col1.metric("Liczba ofert", len(df_f))
col2.metric("Średnia cena", f"{int(df_f[price_col].mean()):,} PLN")
# Sprawdzamy czy kolumna istnieje przed obliczeniem mediany
if psqm_col in df_f.columns:
    col3.metric("Mediana za m²", f"{int(df_f[psqm_col].median()):,} PLN")
else:
    col3.error("Brak kolumny z ceną za m²")

# Tabela ofert
st.subheader("Lista ofert")
st.dataframe(df_f[['title', price_col, psqm_col, 'url']], use_container_width=True)
