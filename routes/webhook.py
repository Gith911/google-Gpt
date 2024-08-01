from flask import Flask, request
from telegram import Update
from telegram.ext import Dispatcher
from services.telegram_bot import handle_update
from config.config import TELEGRAM_API_KEY

app = Flask(__name__)

# إعداد التوزيع للرسائل
dispatcher = Dispatcher(None, None, use_context=True)

@app.route(f'/{TELEGRAM_API_KEY}', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(), dispatcher.bot)
    handle_update(update, dispatcher)
    return 'OK'

def set_webhook():
    import requests
    webhook_url = f'https://google-gpt.onrender.com/{7428721481:AAGRgS7a1brVowVN5m9ozi6DiWT5uQ8tBbs}'  # استبدل `your-domain.com` بنطاقك الفعلي
    response = requests.get(f'https://api.telegram.org/bot{TELEGRAM_API_KEY}/setWebhook?url={webhook_url}')
    print(response.json())

if __name__ == '__main__':
    set_webhook()
    app.run(host='0.0.0.0', port=5000)  # تأكد من تحديث المنفذ إذا لزم الأمر