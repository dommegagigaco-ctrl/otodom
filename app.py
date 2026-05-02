import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("🏠 Otodom: Łowca Okazji")

url = "https://docs.google.com/spreadsheets/d/13skyeoJL9MZvM5iCRtHUI7tyfu9BHArse154eizQ_L8/export?format=csv&gid=0"
df = pd.read_csv(url)

# Poprawny format linku (zamiana /ad/ na /oferta/)
df['url'] = df['url'].str.replace('/ad/', '/oferta/')

psqm_col = 'listingDetails/pricePerSquareMeter/value'
price_col = 'price'

# Obliczenie okazji
rynek_median_psqm = df[psqm_col].median()
df['czy_okazja'] = df[psqm_col] < (rynek_median_psqm * 0.9)

# Sekcja Okazji z klikalnymi linkami
st.subheader("🎯 Okazje (poniżej 10% średniej rynkowej)")
okazje = df[df['czy_okazja'] == True].sort_values(by=psqm_col)

# Tabela z klikalnymi linkami
st.dataframe(
    okazje[['title', price_col, psqm_col, 'url']],
    column_config={
        "url": st.column_config.LinkColumn("Link do oferty", display_text="Otwórz ofertę")
    },
    use_container_width=True
)

# Wykres
st.subheader("Rynek: Cena za m² w zależności od metrażu")
fig = px.scatter(df, x='areaSqm', y=psqm_col, color='czy_okazja', hover_data=['title'])
st.plotly_chart(fig, use_container_width=True)
