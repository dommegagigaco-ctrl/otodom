import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("🏠 Otodom: Łowca Okazji")

url = "https://docs.google.com/spreadsheets/d/13skyeoJL9MZvM5iCRtHUI7tyfu9BHArse154eizQ_L8/export?format=csv&gid=0"
df = pd.read_csv(url)
df['url'] = df['url'].str.replace('/ad/', '/oferta/')

# Sidebar - Wyszukiwarka
st.sidebar.subheader("Wyszukaj konkretną ofertę")
search_term = st.sidebar.text_input("Wpisz fragment tytułu:")
if search_term:
    df = df[df['title'].str.contains(search_term, case=False, na=False)]

# Tabela
st.dataframe(
    df[['title', 'price', 'listingDetails/pricePerSquareMeter/value', 'url']],
    column_config={"url": st.column_config.LinkColumn("Link", display_text="Otwórz")},
    use_container_width=True
)

# Wykres (bez klikania, tylko do podglądu)
fig = px.scatter(df, x='areaSqm', y='listingDetails/pricePerSquareMeter/value', 
                 color='title', hover_data=['title', 'price'])
st.plotly_chart(fig, use_container_width=True)
