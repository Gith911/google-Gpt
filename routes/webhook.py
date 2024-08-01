from flask import Flask, request
from telegram import Update
from telegram.ext import Application
from services.telegram_bot import bot
from config.config import Config

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(), bot)
    application = Application.builder().token(Config.TELEGRAM_TOKEN).build()
    application.process_update(update)
    return "OK", 200

if __name__ == "__main__":
    bot.set_webhook(url=Config.WEBHOOK_URL)
    app.run(port=8443)
