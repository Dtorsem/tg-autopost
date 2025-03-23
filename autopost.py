import os
import gspread
import requests
from oauth2client.service_account import ServiceAccountCredentials
from openai import OpenAI

# Авторизация в Google Sheets
creds_json = os.getenv("GOOGLE_CREDS")
creds_dict = eval(creds_json)
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client_gspread = gspread.authorize(credentials)

# Получаем таблицу и лист
sheet = client_gspread.open("GPT").sheet1

# Получаем текущие посты из таблицы
posts = sheet.col_values(1)[1:]  #
