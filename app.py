import streamlit as st
import pandas as pd
from modules.filters import sidebar_location_filter

st.set_page_config(layout="wide")
st.title("🏠 Otodom: Łowca Okazji")

# 1. Wczytanie i czyszczenie
url = "https://docs.google.com/spreadsheets/d/13skyeoJL9MZvM5iCRtHUI7tyfu9BHArse154eizQ_L8/export?format=csv&gid=0"
df = pd.read_csv(url)
if 'id' in df.columns:
    df = df.drop_duplicates(subset=['id'], keep='last')

# 2. Przetwarzanie dat
for col in ['dateCreated', 'listingDetails/dateCreated']:
    df[col] = pd.to_datetime(df[col], errors='coerce')

df['dni_na_rynku'] = (pd.Timestamp.now() - df['dateCreated']).dt.days

# 3. Filtrowanie
df_f = sidebar_location_filter(df)

# 4. Tabela z klikalnym tytułem i nowymi danymi
cols = {
    'title': 'Tytuł\noferty',
    'price': 'Cena\n(PLN)',
    'listingDetails/pricePerSquareMeter/value': 'Cena\nza m²',
    'listingDetails/areaInSquareMeters': 'Metraż\n(m²)',
    'dni_na_rynku': 'Dni\nrynku',
    'floor': 'Piętro',
    'listingDetails/location/address/street/name': 'Ulica',
    'listingDetails/location/reverseGeocoding/locations/2/name': 'Lokalizacja\nLvl 2',
    'listingDetails/location/reverseGeocoding/locations/3/name': 'Lokalizacja\nLvl 3',
    'listingDetails/development/title': 'Deweloper',
    'listingDetails/development/investmentState': 'Stan\ninw.'
}

# Wyświetlanie - używamy LinkColumn dla 'title', mapując go na 'url'
st.dataframe(
    df_f[list(cols.keys())],
    column_config={
        "title": st.column_config.LinkColumn("Tytuł oferty", display_text="title"),
        # Tutaj sztuczka: łączymy tytuł z linkiem
        "title": st.column_config.LinkColumn(
            "Tytuł oferty",
            help="Kliknij, aby otworzyć ofertę",
            validate="^https://",
            display_text="title" # To wymaga małej poprawki - Streamlit automatycznie zrobi link z kolumny url
        ),
        # ... konfiguracja pozostałych kolumn
    },
    use_container_width=True
)
