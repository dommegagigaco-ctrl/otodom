import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("Otodom: Twój Łowca Okazji")

# Wczytanie danych z arkusza (użyjemy publicznego linku)
url = "https://docs.google.com/spreadsheets/d/13skyeoJL9MZvM5iCRtHUI7tyfu9BHArse154eizQ_L8/edit#gid=0"
df = pd.read_csv(url.replace("/edit#gid=", "/export?format=csv&gid="))

# Podstawowa analiza
st.write("Analiza ofert z Twojego arkusza:")
st.dataframe(df)

# Prosty kalkulator okazji
st.subheader("Wykrywanie okazji")
median_price = df['price'].median()
df['czy_okazja'] = df['price'] < (median_price * 0.9)
okazje = df[df['czy_okazja'] == True]

st.success(f"Znaleziono {len(okazje)} ofert poniżej 90% średniej ceny!")
st.dataframe(okazje[['title', 'price', 'url']])
