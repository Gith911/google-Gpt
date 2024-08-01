import os
import logging
import sqlite3
import google.generativeai as genai
from collections import defaultdict
from langdetect import detect, DetectorFactory, LangDetectException
from flask import Flask, request, jsonify
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent
from dotenv import load_dotenv

# تحميل المتغيرات البيئية من ملف .env
load_dotenv()

# الحصول على المفاتيح من المتغيرات البيئية
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
TELEGRAM_API_KEY = os.getenv('TELEGRAM_API_KEY')

# إعدادات السجلات
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# لضمان ثبات كشف اللغة
DetectorFactory.seed = 0

# تتبع عدد الرسائل لكل مستخدم
user_message_count = defaultdict(int)

# الاتصال بقاعدة البيانات
conn = sqlite3.connect('chatbot.db')
c = conn.cursor()

# إنشاء جدول المستخدمين إذا لم يكن موجوداً
c.execute('''CREATE TABLE IF NOT EXISTS users (
             user_id INTEGER PRIMARY KEY,
             username TEXT,
             message_count INTEGER DEFAULT 0
             )''')
conn.commit()

# إنشاء جدول المحادثات إذا لم يكن موجوداً
c.execute('''CREATE TABLE IF NOT EXISTS conversations (
             user_id INTEGER,
             message TEXT,
             reply TEXT,
             FOREIGN KEY (user_id) REFERENCES users (user_id)
             )''')
conn.commit()

def translate_text(text, target_lang='en', src_lang='auto'):
    # إعدادات الترجمة
    translation_config = {
        "temperature": 0.7,
        "top_p": 0.9,
        "top_k": 50,
        "max_output_tokens": 1000,
        "response_mime_type": "text/plain",
    }

    # بدء جلسة الترجمة
    translation_model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=translation_config,
    )

    chat_session = translation_model.start_chat()
    prompt = f"Translate the following text from {src_lang} to {target_lang}: {text}"
    response = chat_session.send_message(prompt)

    if not response or not response.candidates:
        raise ValueError("Failed to get translation response.")

    return response.text.strip()

def split_message(message, max_length=4096):
    """تقسيم الرسالة إلى أجزاء أصغر إذا كانت طويلة جدًا."""
    return [message[i:i+max_length] for i in range(0, len(message), max_length)]

# تعيين مفتاح API من Google Generative AI
genai.configure(api_key=GOOGLE_API_KEY)

# إعداد Flask
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(), bot)
    dispatcher.process_update(update)
    return jsonify({'status': 'ok'}), 200

def start_polling():
    # إعداد البوت والـ dispatcher هنا
    pass

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))  # الحصول على المنفذ من متغير البيئة PORT
    app.run(host='0.0.0.0', port=port)