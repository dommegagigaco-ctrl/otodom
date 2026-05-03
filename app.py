import streamlit as st
import pandas as pd
from modules.filters import sidebar_location_filter

st.set_page_config(layout="wide")
st.title("🏠 Otodom: Łowca Okazji")

# 1. Wczytanie danych
url = "https://docs.google.com/spreadsheets/d/13skyeoJL9MZvM5iCRtHUI7tyfu9BHArse154eizQ_L8/export?format=csv&gid=0"
df = pd.read_csv(url)

# 2. Usuwanie duplikatów (zostawiamy ostatnią wersję każdego ogłoszenia)
if 'id' in df.columns:
    df = df.drop_duplicates(subset=['id'], keep='last')

# 3. Przetwarzanie linków i dat
df['url'] = df['url'].str.replace('/ad/', '/oferta/')
df['dateCreated'] = pd.to_datetime(df['dateCreated'])
df['dni_na_rynku'] = (pd.Timestamp.now() - df['dateCreated']).dt.days

# 4. Filtrowanie (z modułu zewnętrznego)
df_f = sidebar_location_filter(df)

# 5. Tabela z wynikami
psqm_col = 'listingDetails/pricePerSquareMeter/value'
st.subheader(f"🎯 Znaleziono ofert: {len(df_f)}")

st.dataframe(
    df_f[['title', 'price', psqm_col, 'dni_na_rynku', 'url']].sort_values('dni_na_rynku'),
    column_config={
        "url": st.column_config.LinkColumn("Link", display_text="Otwórz"),
        "price": st.column_config.NumberColumn("Cena", format="%d PLN"),
        psqm_col: st.column_config.NumberColumn("Cena za m²", format="%d PLN")
    },
    use_container_width=True
)

# 6. Opcjonalny podgląd wykresu (zostawiamy, bo go nie używasz aktywnie)
if st.checkbox("Pokaż wykres rozrzutu"):
    import plotly.express as px
    fig = px.scatter(df_f, x='areaSqm', y=psqm_col, color='dni_na_rynku')
    st.plotly_chart(fig, use_container_width=True)
