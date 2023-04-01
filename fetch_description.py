import gspread
from oauth2client.service_account import ServiceAccountCredentials
from fetch_data import make_key_file, get_google_sheet
import os

def get_translate_percentage():
    key_file_path = make_key_file()
    sheet = get_google_sheet(key_file_path)

    csv_sheet = sheet.worksheet("설명")

    cell_value = csv_sheet.acell("J2").value
    print(cell_value)