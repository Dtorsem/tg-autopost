import os
import json
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Авторизация в Google Sheets
creds_json = os.getenv("GOOGLE_CREDS")
creds_dict = json.loads(creds_json)

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(credentials)

# Подключаемся к таблице
sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1DuOrM_xyybIIIdgc_IfJp1fJSi-RKi3S3wf1hHsFDTE/edit?usp=sharing").sheet1

# Берём текст поста из ячейки A2
post_text = sheet.acell('A2').value

# Настройки Telegram
token = os.getenv("TELEGRAM_TOKEN")
chat_id = os.getenv("CHAT_ID")

url = f"https://api.telegram.org/bot{token}/sendMessage"

payload = {
    "chat_id": chat_id,
    "text": post_text,
    "parse_mode": "Markdown",
    "disable_web_page_preview": True
}

# Отправляем пост
res = requests.post(url, json=payload)

print("Статус:", res.status_code)
print("Ответ:", res.text)
