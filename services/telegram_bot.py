import os
import logging
import sqlite3
import google.generativeai as genai
from collections import defaultdict
from langdetect import detect, DetectorFactory, LangDetectException
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

async def handle_update(update: Update, dispatcher) -> None:
    if update.message:
        await handle_message(update)
    elif update.callback_query:
        await handle_button(update)
    elif update.inline_query:
        await inline_query(update)

async def handle_message(update: Update) -> None:
    user_message = update.message.text
    user_id = update.message.from_user.id

    if not user_message.strip():
        await update.message.reply_text("يرجى إرسال رسالة تحتوي على نص.")
        return

    try:
        # زيادة عدد الرسائل للمستخدم
        c.execute('UPDATE users SET message_count = message_count + 1 WHERE user_id = ?', (user_id,))
        conn.commit()
        logger.info(f"Updated message count for user: {user_id}")

        # الكشف عن اللغة
        try:
            detected_lang = detect(user_message)
        except LangDetectException as e:
            logger.error(f"خطأ في كشف اللغة: {e}", exc_info=True)
            await update.message.reply_text("عذرًا، لم أستطع الكشف عن اللغة.")
            return

        logger.info(f"Detected language: {detected_lang} for user {user_id}")

        # ترجمة الرسالة إلى الإنجليزية إذا لم تكن باللغة الإنجليزية
        translated_message = user_message
        if detected_lang != 'en':
            translated_message = translate_text(user_message, target_lang='en', src_lang=detected_lang)

        # بدء جلسة الدردشة باستخدام نموذج الترجمة
        chat_session = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config={
                "temperature": 0.7,
                "top_p": 0.9,
                "top_k": 50,
                "max_output_tokens": 1000,
                "response_mime_type": "text/plain",
            }
        ).start_chat()
        response = chat_session.send_message(translated_message)

        if hasattr(response, 'safety_ratings'):
            logger.error(f"تم رفض الاستجابة لأسباب الأمان: {response.safety_ratings}")
            await update.message.reply_text("عذرًا، لا أستطيع معالجة هذا الطلب.")
            return

        if not response or not response.candidates:
            logger.error("Received an invalid response from the model.")
            await update.message.reply_text("عذرًا، لم أستطع معالجة الطلب.")
            return

        bot_reply = response.text.strip()

        # ترجمة الرد إلى اللغة الأصلية
        if detected_lang != 'en':
            bot_reply = translate_text(bot_reply, target_lang=detected_lang, src_lang='en')

        # إرسال الرد الطويل كرسائل متعددة
        for part in split_message(bot_reply):
            await update.message.reply_text(part)

        # تخزين المحادثة في قاعدة البيانات
        c.execute('INSERT INTO conversations (user_id, message, reply) VALUES (?, ?, ?)', (user_id, user_message, bot_reply))
        conn.commit()

        # إرسال رابط الدعم بعد كل 10 رسائل
        c.execute('SELECT message_count FROM users WHERE user_id = ?', (user_id,))
        result = c.fetchone()
        if result:
            message_count = result[0]
            logger.info(f"User {user_id} has sent {message_count} messages.")
            if message_count % 10 == 0:
                support_link = "https://link.space/@Gith911"
                await update.message.reply_text(f"إذا كنت بحاجة إلى مساعدة إضافية، يرجى زيارة {support_link}")

    except Exception as e:
        logger.error(f"Error occurred in chat function: {e}", exc_info=True)
        await update.message.reply_text("حدث خطأ أثناء معالجة طلبك. يرجى المحاولة مرة أخرى.")

async def handle_button(update: Update) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == 'info':
        # إرسال رابط الدعم عند النقر على زر "معلومات"
        support_link = "https://link.space/@Gith911"
        await query.message.reply_text(f"إذا كنت بحاجة إلى مساعدة إضافية، يرجى زيارة {support_link}")
    elif query.data == 'talk':
        # Handle 'talk' button
        await query.message.reply_text("مستعد للدردشة!")
    elif query.data == 'help':
        # Handle 'help' button
        await query.message.reply_text("يمكنك طرح أي سؤال وسأكون سعيدًا بالإجابة!")

async def inline_query(update: Update) -> None:
    query = update.inline_query.query
    results = [
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="الرد التلقائي",
            input_message_content=InputTextMessageContent(f"أنت سألت: {query}")
        )
    ]
    await update.inline_query.answer(results)

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))  # الحصول على المنفذ من متغير البيئة PORT
    app.run(host='0.0.0.0', port=port)