import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from datetime import datetime

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

SHEET_ID = "13skyeoJL9MZvM5iCRtHUI7tyfu9BHArse154eizQ_L8"
REVIEW_TAB = "oceny"

@st.cache_resource
def get_gspread_client():
    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=SCOPES
    )
    return gspread.authorize(creds)

def get_reviews_sheet():
    client = get_gspread_client()
    spreadsheet = client.open_by_key(SHEET_ID)
    try:
        worksheet = spreadsheet.worksheet(REVIEW_TAB)
    except gspread.exceptions.WorksheetNotFound:
        # Tworzymy zakladke jesli nie istnieje
        worksheet = spreadsheet.add_worksheet(title=REVIEW_TAB, rows=1000, cols=6)
        worksheet.append_row(["id", "ulubione", "widzialem", "komentarz", "data_oceny", "tytul"])
    return worksheet

@st.cache_data(ttl=60)
def load_reviews():
    """Wczytuje wszystkie oceny z arkusza jako slownik {id: {...}}"""
    try:
        ws = get_reviews_sheet()
        records = ws.get_all_records()
        return {str(r['id']): r for r in records}
    except Exception:
        return {}

def save_review(offer_id, title, ulubione, widzialem, komentarz):
    """Zapisuje lub aktualizuje ocene w arkuszu"""
    try:
        ws = get_reviews_sheet()
        records = ws.get_all_records()
        # Szukamy czy juz istnieje wiersz z tym id
        for i, row in enumerate(records, start=2):  # start=2 bo wiersz 1 to naglowki
            if str(row['id']) == str(offer_id):
                ws.update(f'A{i}:F{i}', [[
                    offer_id, ulubione, widzialem,
                    komentarz, datetime.now().strftime("%Y-%m-%d %H:%M"), title
                ]])
                load_reviews.clear()
                return True
        # Nie ma jeszcze - dodajemy nowy wiersz
        ws.append_row([
            offer_id, ulubione, widzialem,
            komentarz, datetime.now().strftime("%Y-%m-%d %H:%M"), title
        ])
        load_reviews.clear()
        return True
    except Exception as e:
        st.error(f"Blad zapisu: {e}")
        return False

def render_review_panel(df_f):
    """Renderuje panel ocen pod tabela"""
    st.subheader("⭐ Oceny i komentarze")

    reviews = load_reviews()

    # Wybor oferty do ocenienia
    offer_options = df_f[['id', 'title']].dropna()
    offer_options['label'] = offer_options['title'].str[:60] + " [" + offer_options['id'].astype(str) + "]"
    selected_label = st.selectbox("Wybierz oferte do ocenienia:", offer_options['label'].tolist(), key="review_select")

    if selected_label:
        selected_id = str(offer_options[offer_options['label'] == selected_label]['id'].values[0])
        selected_title = offer_options[offer_options['label'] == selected_label]['title'].values[0]

        existing = reviews.get(selected_id, {})

        col1, col2 = st.columns(2)
        with col1:
            ulubione = st.checkbox("❤️ Ulubione", value=bool(existing.get('ulubione', False)), key=f"fav_{selected_id}")
            widzialem = st.checkbox("👁️ Widziałem", value=bool(existing.get('widzialem', False)), key=f"seen_{selected_id}")
        with col2:
            komentarz = st.text_area("💬 Komentarz:", value=existing.get('komentarz', ''), key=f"comment_{selected_id}", height=100)

        if st.button("💾 Zapisz ocenę", key=f"save_{selected_id}"):
            if save_review(selected_id, selected_title, ulubione, widzialem, komentarz):
                st.success("✅ Zapisano!")

    # Tabela zapisanych ocen
    if reviews:
        st.subheader("📋 Wszystkie oceny")
        df_reviews = pd.DataFrame(reviews.values())
        st.dataframe(df_reviews, use_container_width=True, hide_index=True)
