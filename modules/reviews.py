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

def parse_bool(val):
    """Bezpieczne parsowanie bool z Google Sheets (unika bledu z pustym stringiem)"""
    if isinstance(val, bool):
        return val
    if isinstance(val, str):
        return val.upper() in ('TRUE', '1', 'TAK', 'YES')
    return bool(val)

@st.cache_data(ttl=60)
def load_reviews():
    """Wczytuje oceny jako slownik {id: {ulubione, widzialem, komentarz}}"""
    try:
        ws = get_reviews_sheet()
        records = ws.get_all_records()
        return {
            str(r['id']): {
                'ulubione':  parse_bool(r.get('ulubione', False)),
                'widzialem': parse_bool(r.get('widzialem', False)),
                'komentarz': str(r.get('komentarz', '')),
            }
            for r in records if r.get('id')
        }
    except Exception:
        return {}

def save_single_review(offer_id, title, ulubione, widzialem, komentarz):
    """Zapisuje lub aktualizuje JEDEN wiersz w arkuszu"""
    try:
        ws = get_reviews_sheet()
        records = ws.get_all_records()
        for i, row in enumerate(records, start=2):
            if str(row['id']) == str(offer_id):
                ws.update(f'A{i}:F{i}', [[
                    str(offer_id),
                    ulubione,
                    widzialem,
                    komentarz,
                    datetime.now().strftime("%Y-%m-%d %H:%M"),
                    str(title)
                ]])
                load_reviews.clear()
                return True
        # Nowy wpis
        ws.append_row([
            str(offer_id), ulubione, widzialem,
            komentarz, datetime.now().strftime("%Y-%m-%d %H:%M"), str(title)
        ])
        load_reviews.clear()
        return True
    except Exception as e:
        st.error(f"Błąd zapisu: {e}")
        return False

def enrich_with_reviews(df):
    """Dodaje kolumny ocen do dataframe na podstawie zapisanych danych"""
    reviews = load_reviews()
    df = df.copy()
    df['❤️']            = df['id'].apply(lambda x: reviews.get(str(x), {}).get('ulubione', False))
    df['👁️']           = df['id'].apply(lambda x: reviews.get(str(x), {}).get('widzialem', False))
    df['💬 Komentarz']  = df['id'].apply(lambda x: reviews.get(str(x), {}).get('komentarz', ''))
    return df
