import streamlit as st
import pandas as pd
from modules.filters import sidebar_location_filter

st.set_page_config(layout="wide")
st.title("🏠 Otodom: Łowca Okazji")

# 1. Wczytanie
url = "https://docs.google.com/spreadsheets/d/13skyeoJL9MZvM5iCRtHUI7tyfu9BHArse154eizQ_L8/export?format=csv&gid=0"
df = pd.read_csv(url)

# 2. Inteligentne usuwanie duplikatów (id to unikalny klucz)
df = df.drop_duplicates(subset=['id'], keep='last')

# 3. Wybór NAJLEPSZYCH dat (używamy globalnych, są najbardziej stabilne)
df['dateCreated'] = pd.to_datetime(df['dateCreated'], errors='coerce')
df['dni_na_rynku'] = (pd.Timestamp.now() - df['dateCreated']).dt.days

# 4. Filtry
df_f = sidebar_location_filter(df)

# 5. Konfiguracja tabeli (tylko to co niezbędne)
cols = {
    'title': 'Tytuł oferty',
    'price': 'Cena (PLN)',
    'listingDetails/pricePerSquareMeter/value': 'Cena/m²',
    'dni_na_rynku': 'Wiek (dni)',
    'floor': 'Piętro',
    'listingDetails/location/address/street/name': 'Ulica',
    'listingDetails/location/reverseGeocoding/locations/3/name': 'Lokalizacja Lvl 3',
    'listingDetails/development/title': 'Deweloper',
    'url': 'Link'
}

# Wyświetl
st.dataframe(
    df_f[list(cols.keys())],
    column_config={
        "title": st.column_config.LinkColumn("Tytuł", display_text="title"),
        "url": st.column_config.LinkColumn("Link", display_text="Otwórz")
    },
    use_container_width=True
)
