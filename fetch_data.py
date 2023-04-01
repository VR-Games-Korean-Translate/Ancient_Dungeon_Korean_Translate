import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

def get_data():
    # 서비스 계정 키 파일 경로 설정
    key_file_path = os.environ.get("KEY_FILE_PATH")

    # Google API 인증 및 클라이언트 생성
    scopes = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive',
    ]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(key_file_path, scopes)
    client = gspread.authorize(credentials)

    # 구글 시트 열기
    sheet_url = os.environ.get("SHEET_URL")
    sheet = client.open_by_url(sheet_url)

    # "csv파일" 시트에서 A열과 C열의 2번째 행부터 끝까지 데이터 읽기
    csv_sheet = sheet.worksheet("csv파일")
    rows = csv_sheet.get_all_values()
    formatted_rows = []

    for row in rows[1:]:
        formatted_rows.append(f"{row[0]};{row[2]}")

    # 경로 설정 및 "english.csv" 파일에 저장
    file_path = os.environ.get("FILE_PATH", "english.csv")
    with open(file_path, "w", encoding="utf-8") as file:
        for formatted_row in formatted_rows:
            file.write(f"{formatted_row}\n")

get_data()