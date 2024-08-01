import os
from dotenv import load_dotenv

# تحميل المتغيرات البيئية من ملف .env
load_dotenv()

# تعيين مفاتيح API من المتغيرات البيئية
TELEGRAM_API_KEY = os.getenv('TELEGRAM_API_KEY')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
PORT = os.getenv('PORT', 5000)  # تعيين قيمة افتراضية للمنفذ إذا لم يتم تعيينه

# التحقق من القيم
print(f"TELEGRAM_API_KEY: {TELEGRAM_API_KEY}")
print(f"GOOGLE_API_KEY: {GOOGLE_API_KEY}")
print(f"PORT: {PORT}")