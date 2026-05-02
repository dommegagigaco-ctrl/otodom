import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("🏠 Otodom: Łowca Okazji")

url = "https://docs.google.com/spreadsheets/d/13skyeoJL9MZvM5iCRtHUI7tyfu9BHArse154eizQ_L8/export?format=csv&gid=0"
df = pd.read_csv(url)
df['url'] = df['url'].str.replace('/ad/', '/oferta/')

psqm_col = 'listingDetails/pricePerSquareMeter/value'
price_col = 'price'

# 1. Wykres z obsługą kliknięcia
st.subheader("Rynek: Cena za m² w zależności od metrażu")
fig = px.scatter(df, x='areaSqm', y=psqm_col, color='title', hover_data=['title', price_col])

# Dodajemy obsługę kliknięcia
event = st.plotly_chart(fig, on_select="rerun")

# 2. Jeśli użytkownik kliknął kropkę...
if event and event["selection"]["points"]:
    clicked_point = event["selection"]["points"][0]
    # Znajdujemy wiersz w ramce danych na podstawie kliknięcia
    selected_index = clicked_point["pointIndex"]
    selected_row = df.iloc[selected_index]
    
    # Wyświetlamy szczegóły klikniętej oferty
    st.divider()
    st.subheader(f"Szczegóły wybranej oferty:")
    st.write(f"### {selected_row['title']}")
    st.write(f"Cena: {selected_row[price_col]:,} PLN")
    st.link_button("Otwórz ofertę w nowym oknie", selected_row['url'])
