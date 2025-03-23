import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from openai import OpenAI

# Авторизация в Google Sheets
creds_json = os.getenv("GOOGLE_CREDS")
creds_dict = json.loads(creds_json)

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/spreadsheets']
credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(credentials)

# Открытие таблицы и листа
sheet = client.open("GPT").worksheet("Лист1")

# Создание поста с помощью GPT (меня)
openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

completion = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "Напиши интересный пост о криптопроекте
