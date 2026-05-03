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

# 1. Tabela
st.subheader("🎯 Okazje rynkowe")
st.dataframe(
    df[['title', price_col, psqm_col, 'url']],
    column_config={"url": st.column_config.LinkColumn("Link", display_text="Otwórz")},
    use_container_width=True
)

# 2. Wykres
st.subheader("Wykres interaktywny")
fig = px.scatter(df, x='areaSqm', y=psqm_col, color='title', hover_data=['title', price_col])
event = st.plotly_chart(fig, on_select="rerun")

# 3. Obsługa kliknięcia (z poprawnymi wcięciami!)
if event:
    if "selection" in event and event["selection"].get("points"):
        points = event["selection"]["points"]
        if len(points) > 0:
            idx = points[0].get("pointIndex")
            if idx is not None:
                selected_row = df.iloc[idx]
                st.divider()
                st.success(f"Wybrano: {selected_row['title']}")
                st.write(f"Cena: {selected_row[price_col]:,} PLN")
                st.link_button("👉 Przejdź do oferty", selected_row['url'])
