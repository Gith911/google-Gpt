import os
import requests
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Dispatcher
from services.telegram_bot import handle_update
from config.config import TELEGRAM_API_KEY

app = Flask(__name__)

# إعداد التوزيع للرسائل
dispatcher = Dispatcher(Bot(token=TELEGRAM_API_KEY), None, use_context=True)

@app.route(f'/{TELEGRAM_API_KEY}', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(), dispatcher.bot)
    handle_update(update, dispatcher)
    return 'OK'

def set_webhook():
    webhook_url = f'https://google-gpt.onrender.com/{TELEGRAM_API_KEY}'  # استبدل <your-domain> بنطاقك الفعلي
    response = requests.get(f'https://api.telegram.org/bot{TELEGRAM_API_KEY}/setWebhook?url={webhook_url}')
    print(response.json())

if __name__ == '__main__':
    set_webhook()
    port = int(os.environ.get('PORT', 5000))  # الحصول على المنفذ من متغير البيئة PORT
    print(f"PORT environment variable is set to: {port}")  # تسجيل قيمة متغير البيئة PORT
    print(f"Running on host 0.0.0.0 and port {port}")  # تسجيل معلومات الاستضافة والمنفذ
    app.run(host='0.0.0.0', port=port)  # تأكد من تحديث المنفذ إذا لزم الأمر