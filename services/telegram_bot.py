import logging
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from config.config import Config
from google_generativeai import generate_text
from localization.localization.py import detect_language, translate_text
from database.db import update_conversation

logging.basicConfig(level=logging.INFO)

bot = Bot(token=Config.TELEGRAM_TOKEN)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('مرحبًا! أنا بوت تلجرام الذكي. كيف يمكنني مساعدتك اليوم؟')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    user_id = update.message.from_user.id

    language = detect_language(user_message)
    if language != 'en':
        user_message = translate_text(user_message, 'en')

    response = generate_text(user_message)

    if language != 'en':
        response = translate_text(response, language)

    await update.message.reply_text(response)
    update_conversation(user_id, user_message, response)

def main():
    application = Application.builder().token(Config.TELEGRAM_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    application.run_polling()

if __name__ == "__main__":
    main()
