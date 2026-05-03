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

# Mapowanie nazw pól na krótsze nagłówki
dev_title = 'listingDetails/development/title'
dev_state = 'listingDetails/development/investmentState'
psqm_col = 'listingDetails/pricePerSquareMeter/value'
lvl3_col = 'development/location/reverseGeocoding/locations/3/name'

st.subheader(f"🎯 Znaleziono ofert: {len(df_f)}")

# Wyświetlanie tabeli z konfiguracją szerokości i nazw
st.dataframe(
    df_f[['title', 'price', psqm_col, 'dni_na_rynku', dev_title, dev_state, lvl3_col, 'url']],
    column_config={
        "title": st.column_config.TextColumn("Tytuł\noferty", width="medium"),
        "price": st.column_config.NumberColumn("Cena\n(PLN)", format="%d"),
        psqm_col: st.column_config.NumberColumn("Cena\nza m²", format="%d"),
        "dni_na_rynku": st.column_config.NumberColumn("Dni na\nrynku", width="small"),
        dev_title: st.column_config.TextColumn("Deweloper\n/Nazwa", width="medium"),
        dev_state: st.column_config.TextColumn("Stan\ninwestycji", width="small"),
        lvl3_col: st.column_config.TextColumn("Lokalizacja\n(Lvl 3)", width="small"),
        "url": st.column_config.LinkColumn("Link", display_text="Otwórz", width="small")
    },
    use_container_width=True
)
