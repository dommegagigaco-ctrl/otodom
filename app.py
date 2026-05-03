import streamlit as st
import pandas as pd
from modules.filters import sidebar_location_filter

st.set_page_config(layout="wide")
st.title("🏠 Otodom: Łowca Okazji")

# Wczytanie
url = "https://docs.google.com/spreadsheets/d/13skyeoJL9MZvM5iCRtHUI7tyfu9BHArse154eizQ_L8/export?format=csv&gid=0"
df = pd.read_csv(url)
df['url'] = df['url'].str.replace('/ad/', '/oferta/')

# Przetwarzanie daty
df['dateCreated'] = pd.to_datetime(df['dateCreated'])
df['dni_na_rynku'] = (pd.Timestamp.now() - df['dateCreated']).dt.days

# Filtrowanie lokalizacji (używamy zewnętrznego modułu)
df_f = sidebar_location_filter(df)

# Tabela
psqm_col = 'listingDetails/pricePerSquareMeter/value'
st.dataframe(
    df_f[['title', 'price', psqm_col, 'dni_na_rynku', 'url']].sort_values('dni_na_rynku'),
    column_config={"url": st.column_config.LinkColumn("Link", display_text="Otwórz")},
    use_container_width=True
)
