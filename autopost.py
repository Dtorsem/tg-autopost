import os
import openai
import gspread
import requests
from oauth2client.service_account import ServiceAccountCredentials

# Получаем переменные окружения из GitHub Actions
creds_json = os.getenv('GOOGLE_CREDS')
openai.api_key = os.getenv('OPENAI_API_KEY')
telegram_token = os.getenv('TELEGRAM_TOKEN')
telegram_chat_id = os.getenv('CHAT_ID')

# Авторизация в Google Sheets
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_dict(eval(creds_json), scope)
client = gspread.authorize(credentials)

# Открываем таблицу и лист
sheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1DuOrM_xyybIIIdgc_IfJp1fJSi-RKi3S3wf1hHsFDTE/edit#gid=0').sheet1

# Генерируем контент через ChatGPT
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "Ты пишешь интересный пост для Телеграм канала про криптопроекты и airdrop."},
        {"role": "user", "content": "Напиши короткий живой пост с полезной информацией про перспективный криптопроект и его airdrop."}
    ],
    temperature=0.7
)

generated_text = response.choices[0].message['content']

# Записываем текст в Google Sheets
sheet.append_row([generated_text])

# Отправляем текст в Telegram
url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
requests.post(url, json={"chat_id": telegram_chat_id, "text": generated_text})
