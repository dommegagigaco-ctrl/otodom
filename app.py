import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("🏠 Otodom: Łowca Okazji")

# 1. Wczytanie danych
url = "https://docs.google.com/spreadsheets/d/13skyeoJL9MZvM5iCRtHUI7tyfu9BHArse154eizQ_L8/export?format=csv&gid=0"
df = pd.read_csv(url)

# Poprawa linków
df['url'] = df['url'].str.replace('/ad/', '/oferta/')

# 2. Przetwarzanie daty i obliczanie "wieku" oferty
# Używamy kolumny dateCreated do obliczenia ile dni ogłoszenie jest na rynku
df['dateCreated'] = pd.to_datetime(df['dateCreated'])
df['dni_na_rynku'] = (pd.Timestamp.now() - df['dateCreated']).dt.days

# Definicje kolumn dla wygody
psqm_col = 'listingDetails/pricePerSquareMeter/value'
price_col = 'price'

# 3. Sidebar - Filtrowanie
st.sidebar.subheader("Filtry Inwestycyjne")
max_dni = st.sidebar.slider("Max wiek ogłoszenia (dni):", 0, 365, 30)
df_f = df[df['dni_na_rynku'] <= max_dni]

# 4. Tabela z datą
st.subheader(f"🎯 Oferty na rynku (maks {max_dni} dni)")
st.dataframe(
    df_f[['title', price_col, psqm_col, 'dni_na_rynku', 'url']].sort_values('dni_na_rynku'),
    column_config={"url": st.column_config.LinkColumn("Link", display_text="Otwórz")},
    use_container_width=True
)

# 5. Wykres (nieinteraktywny, tylko podgląd)
st.subheader("Rynek: Cena za m² w zależności od metrażu")
fig = px.scatter(df_f, x='areaSqm', y=psqm_col, color='dni_na_rynku', 
                 hover_data=['title', price_col],
                 color_continuous_scale='Viridis')
st.plotly_chart(fig, use_container_width=True)
