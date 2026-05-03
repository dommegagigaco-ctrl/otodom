import streamlit as st
import pandas as pd
from modules.filters import sidebar_location_filter
from modules.reviews import render_review_panel

st.set_page_config(layout="wide")
st.title("🏠 Otodom: Łowca Okazji")

# 1. Wczytanie
url = "https://docs.google.com/spreadsheets/d/13skyeoJL9MZvM5iCRtHUI7tyfu9BHArse154eizQ_L8/export?format=csv&gid=0"
df = pd.read_csv(url)

# 2. Czyszczenie
df['url'] = df['url'].str.replace('/hpr/pl/', '/pl/')
df['url'] = df['url'].str.replace('/ad/', '/oferta/')
if 'id' in df.columns:
    df = df.drop_duplicates(subset=['id'], keep='last')
df = df.dropna(subset=['dateCreated', 'url'])

# 3. Daty
df['dateCreated'] = pd.to_datetime(df['dateCreated'], errors='coerce')
df['dni_na_rynku'] = (pd.Timestamp.now() - df['dateCreated']).dt.days

# 4. Filtry
df_f = sidebar_location_filter(df)

# 5. Definicja kolumn
all_cols = {
    'url':                                                        'Link',
    'title':                                                      'Tytuł oferty',
    'price':                                                      'Cena',
    'listingDetails/pricePerSquareMeter/value':                   'Cena/m²',
    'areaSqm':                                                    'Metraż (m²)',
    'dni_na_rynku':                                               'Dni',
    'floor':                                                      'Piętro',
    'listingDetails/location/address/street/name':                'Ulica',
    'listingDetails/location/reverseGeocoding/locations/3/name':  'Lokalizacja',
    'listingDetails/development/title':                           'Deweloper',
    'listingDetails/development/investmentState':                 'Stan inw.'
}

params = st.query_params

# 6. Sidebar: widoczne kolumny
st.sidebar.subheader("📋 Widoczne kolumny")
visible_cols = {}
for col_key, col_label in all_cols.items():
    param_name = f"col_{col_key.replace('/', '_')}"
    default_val = params.get(param_name, "1") == "1"
    is_visible = st.sidebar.checkbox(col_label, value=default_val, key=f"chk_{param_name}")
    st.query_params[param_name] = "1" if is_visible else "0"
    if is_visible:
        visible_cols[col_key] = col_label

# 7. Sidebar: sortowanie
st.sidebar.subheader("🔃 Sortowanie")
sortable = {k: v for k, v in all_cols.items() if k not in ['url', 'title']}
sort_options = list(sortable.values())
sort_keys   = list(sortable.keys())
saved_sort  = params.get("sort_col", "Cena")
sort_idx    = sort_options.index(saved_sort) if saved_sort in sort_options else 0
sort_label  = st.sidebar.selectbox("Sortuj wg:", sort_options, index=sort_idx, key="sort_col_sel")
sort_col    = sort_keys[sort_options.index(sort_label)]
st.query_params["sort_col"] = sort_label
saved_order = params.get("sort_asc", "1")
sort_asc    = st.sidebar.radio("Kolejność:", ["Rosnąco", "Malejąco"],
                               index=0 if saved_order == "1" else 1, key="sort_order_sel")
asc_flag    = sort_asc == "Rosnąco"
st.query_params["sort_asc"] = "1" if asc_flag else "0"

# 8. Tabela
df_sorted = df_f.sort_values(by=sort_col, ascending=asc_flag)
existing_visible = [c for c in visible_cols if c in df_sorted.columns]

st.subheader(f"🎯 Znaleziono ofert: {len(df_sorted)}")
st.dataframe(
    df_sorted[existing_visible],
    column_config={
        "url":                                      st.column_config.LinkColumn("Link", display_text="Otwórz"),
        "price":                                    st.column_config.NumberColumn("Cena", format="%d PLN"),
        "listingDetails/pricePerSquareMeter/value": st.column_config.NumberColumn("Cena/m²", format="%d PLN"),
        "areaSqm":                                  st.column_config.NumberColumn("Metraż (m²)", format="%.1f m²"),
        "dni_na_rynku":                             st.column_config.NumberColumn("Dni", format="%d")
    },
    use_container_width=True,
    hide_index=True
)

# 9. Panel ocen i komentarzy
st.divider()
render_review_panel(df_sorted)
