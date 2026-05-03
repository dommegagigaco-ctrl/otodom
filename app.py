import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("🏠 Otodom: Łowca Okazji")

# Wczytanie
url = "https://docs.google.com/spreadsheets/d/13skyeoJL9MZvM5iCRtHUI7tyfu9BHArse154eizQ_L8/export?format=csv&gid=0"
df = pd.read_csv(url)
df['url'] = df['url'].str.replace('/ad/', '/oferta/')

psqm_col = 'listingDetails/pricePerSquareMeter/value'
price_col = 'price'

# 1. Tabela (zawsze widoczna na górze)
st.subheader("🎯 Okazje rynkowe")
st.dataframe(
    df[['title', price_col, psqm_col, 'url']],
    column_config={"url": st.column_config.LinkColumn("Link", display_text="Otwórz")},
    use_container_width=True
)

# 2. Wykres z obsługą kliknięcia
st.subheader("Wykres interaktywny")
fig = px.scatter(df, x='areaSqm', y=psqm_col, color='title', hover_data=['title', price_col])
event = st.plotly_chart(fig, on_select="rerun")

# 3. Szczegóły kliknięcia (tylko jeśli coś wybrano)
if event and "selection" in event and event["selection"]["points"]:
    # Pobieramy index punktu z wykresu
    idx = event["selection"]["points"][0]["pointIndex"]
    selected_row = df.iloc[idx]
    
    st.divider()
    st.success(f"Wybrano: {selected_row['title']}")
    st.write(f"Cena: {selected_row[price_col]:,} PLN | Za m²: {selected_row[psqm_col]}")
    st.link_button("👉 Przejdź do oferty", selected_row['url'])
