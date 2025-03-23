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
posts = sheet.col_values(1)[1:]  # Берём все строки кроме заголовка
content = "\n\n".join(posts)

# Генерируем пост через OpenAI
client_openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client_openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "Напиши краткий интересный пост для Telegram-канала на основе следующей информации:"},
        {"role": "user", "content": content}
    ]
)

post_text = response.choices[0].message.content.strip()

# Отправляем сообщение в Telegram
bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
chat_id = os.getenv("TELEGRAM_CHAT_ID")

url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
requests.post(url, data={"chat_id": chat_id, "text": post_text})
