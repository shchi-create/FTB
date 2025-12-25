import os
import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
import json

load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# Загружаем credentials из переменной окружения Railway
creds_json = os.getenv("GOOGLE_CREDS_JSON")
if not creds_json:
    raise ValueError("GOOGLE_CREDS_JSON не найден!")

creds_dict = json.loads(creds_json)
creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)

client = gspread.authorize(creds)

spreadsheet_key = os.getenv("GSHEET_KEY")
if not spreadsheet_key:
    raise ValueError("GSHEET_KEY не найден!")

spreadsheet = client.open_by_key(spreadsheet_key)
sheet = spreadsheet.worksheet("test")

def write_to_a1(text: str):
    """Записывает текст в ячейку A1"""
    sheet.update("A1", text)
