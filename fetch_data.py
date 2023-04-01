import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json

license = {'dossammul': '한글화를 진행하며 도스샘물을 사용하였습니다.<br>Copyright (c) 2016-2022 Damheo Lee (이담허) (leedheo@gmail.com),<br>with Reserved Font Name DOSMyungjo, DOSGothic, DOSSaemmul, Sam3KRFont, MiraeroNormal, and DOSIyagi,',
'galmuri9': '한글화를 진행하며 갈무리9를 사용하였습니다.<br>Copyright &copy; 2019-2023 Minseo Lee (itoupluk427@gmail.com)',
'neodgm': '한글화를 진행하며 Neo둥근모를 사용하였습니다.<br>Copyright © 2017-2022, Eunbin Jeong (Dalgona.) <project-neodgm@dalgona.dev> with reserved font name "Neo둥근모" and "NeoDunggeunmo".'}


def make_key_file():
    # 서비스 계정 키 가져오기
    service_account_key = os.environ.get("SERVICE_ACCOUNT_KEY")
    key_file_path = "key.json"

    # 키를 JSON 형태로 변환하여 임시 파일에 저장
    with open(key_file_path, "w") as key_file:
        key_file.write(service_account_key)

    return key_file_path

def get_google_sheet(key_file_path):
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

    return sheet


def get_translate_data(sheet):
    # "csv파일" 시트에서 A열과 C열의 2번째 행부터 끝까지 데이터 읽기
    csv_sheet = sheet.worksheet("csv파일")
    rows = csv_sheet.get_all_values()
    formatted_rows = []

    for row in rows[1:]:
        formatted_rows.append(f"{row[0]};{row[2]}")

    return formatted_rows


def make_translate_file(translate_data_list):
    # 경로 설정 및 "english.csv" 파일에 저장
base_directory = os.environ.get("VERSION_FILE_PATH", "")
subdirectories = license.keys()

for subdir in subdirectories:
    target_directory = os.path.join(base_directory, subdir, "StreamingAssets", "gamedata", "language")
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)

    file_path = os.path.join(target_directory, "english.csv")

    with open(file_path, "w", encoding="utf-8") as file:
        for index, translate_row in enumerate(translate_data_list):
            # <KOREAN_FONT_LICENSE> 텍스트를 찾아 해당 키의 값으로 대체
            if "<KOREAN_FONT_LICENSE>" in translate_row:
                translate_row = translate_row.replace("<KOREAN_FONT_LICENSE>", license[subdir])
            
            # 인덱스가 마지막 요소인지 확인
            if index == len(translate_data_list) - 1:
                file.write(f"{translate_row}")
            else:
                file.write(f"{translate_row}\n")


def make_translate_data():
    key_file_path = make_key_file()
    sheet = get_google_sheet(key_file_path) # 구글 시트 열기

    translate_data_list = get_translate_data(sheet) # 번역 데이터 가져오기

    make_translate_file(translate_data_list) # 번역 파일 생성

    # 임시 키 파일 제거
    os.remove(key_file_path)

make_translate_data()
