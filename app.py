import streamlit as st
import pandas as pd
import plotly.express as px
from modules.filters import sidebar_location_filter
from modules.reviews import enrich_with_reviews, save_single_review

st.set_page_config(layout="wide")
st.title("🏠 Otodom: Łowca Okazji – Magda i Wiktor")

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

# 5. Dodanie ocen
df_f = enrich_with_reviews(df_f)

# ── KPI ────────────────────────────────────────────────────────────────────────
df_c = df_f.copy()
df_c['_ppsm'] = pd.to_numeric(df_c.get('listingDetails/pricePerSquareMeter/value'), errors='coerce')
df_c['_price'] = pd.to_numeric(df_c.get('price'), errors='coerce')
df_c['_area']  = pd.to_numeric(df_c.get('areaSqm'), errors='coerce')
df_c['_dni']   = pd.to_numeric(df_c.get('dni_na_rynku'), errors='coerce')

k1, k2, k3, k4 = st.columns(4)
k1.metric('🏘️ Oferty',          len(df_c))
k2.metric('💰 Mediana ceny',     f"{int(df_c['_price'].median()):,} PLN".replace(',', ' ') if df_c['_price'].notna().any() else '–')
k3.metric('📐 Mediana ceny/m²',  f"{int(df_c['_ppsm'].median()):,} PLN".replace(',', ' ') if df_c['_ppsm'].notna().any() else '–')
k4.metric('❤️ Ulubione',        int(df_c['❤️'].fillna(False).sum()) if '❤️' in df_c.columns else 0)

# ── WYKRESY ────────────────────────────────────────────────────────────────────
st.markdown('---')
st.subheader('📊 Analiza ofert')

col_left, col_right = st.columns(2)

with col_left:
    hover_cols = [c for c in ['title', '_dni', '_ppsm', 'listingDetails/location/address/street/name'] if c in df_c.columns]
    fig1 = px.scatter(
        df_c.dropna(subset=['_area', '_price']),
        x='_area', y='_price',
        color='❤️' if '❤️' in df_c.columns else None,
        hover_data=hover_cols,
        labels={'_area': 'Metraż (m²)', '_price': 'Cena (PLN)', '❤️': 'Ulubione'},
        title='Cena vs metraż',
        color_discrete_map={True: '#e74c3c', False: '#3498db'}
    )
    fig1.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig1, use_container_width=True)

with col_right:
    fig2 = px.histogram(
        df_c.dropna(subset=['_ppsm']),
        x='_ppsm',
        color='❤️' if '❤️' in df_c.columns else None,
        nbins=25,
        labels={'_ppsm': 'Cena za m² (PLN)', '❤️': 'Ulubione'},
        title='Rozkład ceny za m²',
        color_discrete_map={True: '#e74c3c', False: '#3498db'}
    )
    median_val = df_c['_ppsm'].median()
    fig2.add_vline(x=median_val, line_dash='dash', line_color='orange',
                   annotation_text=f'Mediana: {int(median_val):,}'.replace(',', ' '),
                   annotation_position='top right')
    fig2.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)

hover_cols3 = [c for c in ['title', '_price', '_area', 'listingDetails/location/address/street/name'] if c in df_c.columns]
fig3 = px.scatter(
    df_c.dropna(subset=['_dni', '_ppsm']),
    x='_dni', y='_ppsm',
    color='❤️' if '❤️' in df_c.columns else None,
    hover_data=hover_cols3,
    labels={'_dni': 'Dni na rynku', '_ppsm': 'Cena za m² (PLN)', '❤️': 'Ulubione'},
    title='Czas na rynku vs cena za m²',
    color_discrete_map={True: '#e74c3c', False: '#3498db'}
)
fig3.update_layout(height=380, showlegend=False)
st.plotly_chart(fig3, use_container_width=True)

# ── TABELA ─────────────────────────────────────────────────────────────────────
st.markdown('---')

all_cols = {
    '❤️':                                                       '❤️',
    '👁️':                                                      '👁️',
    'url':                                                      'Link',
    'title':                                                    'Tytuł oferty',
    'price':                                                    'Cena',
    'listingDetails/pricePerSquareMeter/value':                 'Cena/m²',
    'areaSqm':                                                  'Metraż (m²)',
    'dni_na_rynku':                                             'Dni',
    'floor':                                                    'Piętro',
    'listingDetails/location/address/street/name':              'Ulica',
    'listingDetails/location/reverseGeocoding/locations/3/name':'Lokalizacja',
    'listingDetails/development/title':                         'Deweloper',
    'listingDetails/development/investmentState':               'Stan inw.',
    '💬 Komentarz':                                             '💬 Komentarz',
    'id':                                                       'ID'
}

params = st.query_params

st.sidebar.subheader('📋 Widoczne kolumny')
visible_cols = {}
default_hidden = {'id'}
for col_key, col_label in all_cols.items():
    param_name = f"col_{col_key.replace('/', '_')}"
    default_val = params.get(param_name, '0' if col_key in default_hidden else '1') == '1'
    is_visible = st.sidebar.checkbox(col_label, value=default_val, key=f'chk_{param_name}')
    st.query_params[param_name] = '1' if is_visible else '0'
    if is_visible:
        visible_cols[col_key] = col_label

if 'id' not in visible_cols:
    cols_to_show = list(visible_cols.keys()) + ['id']
else:
    cols_to_show = list(visible_cols.keys())

st.sidebar.subheader('🔃 Sortowanie')
sortable = {k: v for k, v in all_cols.items() if k not in ['❤️', '👁️', '💬 Komentarz', 'url', 'title', 'id']}
sort_options = list(sortable.values())
sort_keys    = list(sortable.keys())
saved_sort   = params.get('sort_col', 'Cena')
sort_idx     = sort_options.index(saved_sort) if saved_sort in sort_options else 0
sort_label   = st.sidebar.selectbox('Sortuj wg:', sort_options, index=sort_idx, key='sort_col_sel')
sort_col     = sort_keys[sort_options.index(sort_label)]
st.query_params['sort_col'] = sort_label
saved_order  = params.get('sort_asc', '1')
sort_asc     = st.sidebar.radio('Kolejność:', ['Rosnąco', 'Malejąco'], index=0 if saved_order == '1' else 1, key='sort_order_sel')
asc_flag     = sort_asc == 'Rosnąco'
st.query_params['sort_asc'] = '1' if asc_flag else '0'

df_sorted = df_f.sort_values(by=sort_col, ascending=asc_flag)
existing_cols = [c for c in cols_to_show if c in df_sorted.columns]

st.subheader(f'🎯 Znaleziono ofert: {len(df_sorted)}')
edited_df = st.data_editor(
    df_sorted[existing_cols],
    column_config={
        '❤️': st.column_config.CheckboxColumn('❤️', width='small'),
        '👁️': st.column_config.CheckboxColumn('👁️', width='small'),
        'url': st.column_config.LinkColumn('Link', display_text='Otwórz'),
        'price': st.column_config.NumberColumn('Cena', format='%d PLN'),
        'listingDetails/pricePerSquareMeter/value': st.column_config.NumberColumn('Cena/m²', format='%d PLN'),
        'areaSqm': st.column_config.NumberColumn('Metraż (m²)', format='%.1f m²'),
        'dni_na_rynku': st.column_config.NumberColumn('Dni', format='%d'),
        '💬 Komentarz': st.column_config.TextColumn('💬 Komentarz', width='medium'),
        'id': st.column_config.NumberColumn('ID', width='small')
    },
    use_container_width=True,
    hide_index=True,
    disabled=[c for c in existing_cols if c not in ['❤️', '👁️', '💬 Komentarz']]
)

original = df_sorted[existing_cols].reset_index(drop=True)
changed  = edited_df.reset_index(drop=True)

review_cols = [c for c in ['❤️', '👁️', '💬 Komentarz'] if c in changed.columns]
if review_cols and st.button('💾 Zapisz zmiany w ocenach'):
    saved = 0
    for i in range(len(changed)):
        orig_row = original.iloc[i]
        edit_row = changed.iloc[i]
        if any(orig_row[c] != edit_row[c] for c in review_cols if c in orig_row.index):
            save_single_review(
                offer_id  = edit_row['id'],
                title     = edit_row.get('title', ''),
                ulubione  = bool(edit_row.get('❤️', False)),
                widzialem = bool(edit_row.get('👁️', False)),
                komentarz = str(edit_row.get('💬 Komentarz', ''))
            )
            saved += 1
    if saved > 0:
        st.success(f'✅ Zapisano zmiany dla {saved} ofert')
        st.rerun()
    else:
        st.info('ℹ️ Nie wykryto żadnych zmian')
