import streamlit as st
import pandas as pd
from modules.filters import sidebar_location_filter

st.set_page_config(layout="wide")
st.title("🏠 Otodom: Łowca Okazji")

# Wczytanie i duplikaty
url = "https://docs.google.com/spreadsheets/d/13skyeoJL9MZvM5iCRtHUI7tyfu9BHArse154eizQ_L8/export?format=csv&gid=0"
df = pd.read_csv(url)
if 'id' in df.columns:
    df = df.drop_duplicates(subset=['id'], keep='last')

# Przetwarzanie
df['url'] = df['url'].str.replace('/ad/', '/oferta/')
df['dateCreated'] = pd.to_datetime(df['dateCreated'], errors='coerce')
df['dni_na_rynku'] = (pd.Timestamp.now() - df['dateCreated']).dt.days

df_f = sidebar_location_filter(df)

# Definicja kolumn
cols = {
    'url': 'Link',
    'title': 'Tytuł oferty',
    'price': 'Cena',
    'listingDetails/pricePerSquareMeter/value': 'Cena/m²',
    'dni_na_rynku': 'Dni',
    'floor': 'Piętro',
    'listingDetails/location/address/street/name': 'Ulica',
    'listingDetails/location/reverseGeocoding/locations/3/name': 'Lokalizacja',
    'listingDetails/development/title': 'Deweloper',
    'listingDetails/development/investmentState': 'Stan inw.'
}

# Wyświetlanie
st.dataframe(
    df_f[list(cols.keys())],
    column_config={
        "url": st.column_config.LinkColumn("Link", display_text="Otwórz"),
        "price": st.column_config.NumberColumn("Cena", format="%d"),
        "listingDetails/pricePerSquareMeter/value": st.column_config.NumberColumn("Cena/m²", format="%d"),
        "dni_na_rynku": st.column_config.NumberColumn("Dni", format="%d")
    },
    use_container_width=True
)
