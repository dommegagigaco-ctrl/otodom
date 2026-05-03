import streamlit as st
import pandas as pd
from modules.filters import sidebar_location_filter

st.set_page_config(layout="wide")
st.title("🏠 Otodom: Łowca Okazji")

# 1. Wczytanie
url = "https://docs.google.com/spreadsheets/d/13skyeoJL9MZvM5iCRtHUI7tyfu9BHArse154eizQ_L8/export?format=csv&gid=0"
df = pd.read_csv(url)

# 2. CZYSZCZENIE DANYCH (KLUCZOWE)
# Ujednolicenie linków, aby duplikaty były traktowane tak samo
df['url'] = df['url'].str.replace('/hpr/pl/', '/pl/')
df['url'] = df['url'].str.replace('/ad/', '/oferta/')

# Usuwamy duplikaty po ID
if 'id' in df.columns:
    df = df.drop_duplicates(subset=['id'], keep='last')

# Usuwamy wiersze, które nie mają daty lub są "śmieciami"
df = df.dropna(subset=['dateCreated', 'url'])

# 3. Przetwarzanie dat
df['dateCreated'] = pd.to_datetime(df['dateCreated'], errors='coerce')
df['dni_na_rynku'] = (pd.Timestamp.now() - df['dateCreated']).dt.days

# 4. Filtrowanie (przez moduł zewnętrzny)
df_f = sidebar_location_filter(df)

# 5. Definicja kolumn (kolejność w tabeli)
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

# 6. Wyświetlanie
st.subheader(f"🎯 Znaleziono unikalnych ofert: {len(df_f)}")
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
