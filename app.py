import streamlit as st
import pandas as pd
from modules.filters import sidebar_location_filter

st.set_page_config(layout="wide")
st.title("🏠 Otodom: Łowca Okazji")

url = "https://docs.google.com/spreadsheets/d/13skyeoJL9MZvM5iCRtHUI7tyfu9BHArse154eizQ_L8/export?format=csv&gid=0"
df = pd.read_csv(url)

if 'id' in df.columns:
    df = df.drop_duplicates(subset=['id'], keep='last')

df['url'] = df['url'].str.replace('/ad/', '/oferta/')
df['dateCreated'] = pd.to_datetime(df['dateCreated'])
df['dni_na_rynku'] = (pd.Timestamp.now() - df['dateCreated']).dt.days

df_f = sidebar_location_filter(df)

psqm_col = 'listingDetails/pricePerSquareMeter/value'
# Dodana kolumna do wyświetlania
lvl3_col = 'development/location/reverseGeocoding/locations/3/name'

st.subheader(f"🎯 Znaleziono ofert: {len(df_f)}")

# Wybieramy kolumny do tabeli, dodając nową
cols_to_show = ['title', 'price', psqm_col, 'dni_na_rynku', lvl3_col, 'url']
# Filtrujemy tylko te kolumny, które naprawdę istnieją w danych
cols_to_show = [c for c in cols_to_show if c in df_f.columns]

st.dataframe(
    df_f[cols_to_show].sort_values('dni_na_rynku'),
    column_config={
        "url": st.column_config.LinkColumn("Link", display_text="Otwórz"),
        "price": st.column_config.NumberColumn("Cena", format="%d PLN"),
        psqm_col: st.column_config.NumberColumn("Cena za m²", format="%d PLN")
    },
    use_container_width=True
)
