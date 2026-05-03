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
        st.secrets["gcp_service_account"], scopes=SCOPES
    )
    return gspread.authorize(creds)

def get_reviews_sheet():
    client = get_gspread_client()
    spreadsheet = client.open_by_key(SHEET_ID)
    try:
        return spreadsheet.worksheet(REVIEW_TAB)
    except gspread.exceptions.WorksheetNotFound:
        ws = spreadsheet.add_worksheet(title=REVIEW_TAB, rows=1000, cols=6)
        ws.append_row(["id", "ulubione", "widzialem", "komentarz", "data_oceny", "tytul"])
        return ws

@st.cache_data(ttl=60)
def load_reviews():
    try:
        ws = get_reviews_sheet()
        records = ws.get_all_records()
        return {str(r['id']): r for r in records}
    except Exception:
        return {}

def save_all_reviews(edited_df):
    """Zapisuje wszystkie zmodyfikowane wiersze do arkusza"""
    try:
        ws = get_reviews_sheet()
        records = ws.get_all_records()
        existing_ids = {str(r['id']): i + 2 for i, r in enumerate(records)}

        for _, row in edited_df.iterrows():
            offer_id = str(row['id'])
            data = [
                offer_id,
                bool(row.get('\u2764\ufe0f', False)),
                bool(row.get('\U0001f441\ufe0f', False)),
                str(row.get('\U0001f4ac Komentarz', '')),
                datetime.now().strftime("%Y-%m-%d %H:%M"),
                str(row.get('title', ''))
            ]
            if offer_id in existing_ids:
                row_num = existing_ids[offer_id]
                ws.update(f'A{row_num}:F{row_num}', [data])
            else:
                ws.append_row(data)

        load_reviews.clear()
        return True
    except Exception as e:
        st.error(f"Błąd zapisu: {e}")
        return False

def enrich_with_reviews(df):
    """Dodaje kolumny ocen do dataframe"""
    reviews = load_reviews()

    def get_val(offer_id, key, default):
        return reviews.get(str(offer_id), {}).get(key, default)

    df = df.copy()
    df['\u2764\ufe0f']           = df['id'].apply(lambda x: bool(get_val(x, 'ulubione', False)))
    df['\U0001f441\ufe0f']          = df['id'].apply(lambda x: bool(get_val(x, 'widzialem', False)))
    df['\U0001f4ac Komentarz'] = df['id'].apply(lambda x: str(get_val(x, 'komentarz', '')))
    return df
