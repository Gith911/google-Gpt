# Telegram AI Bot Project

## وصف المشروع
بوت تلجرام يستخدم الذكاء الصناعي من Google لتقديم ردود ذكية على المستخدمين. البوت يتعرف على اللغة باستخدام مكتبة `deep-translator` ويتعامل مع الرسائل بذكاء.

## هيكلية المشروع

telegram-bot-project/
│
├── config/
│   ├── config.py            # ملف إعدادات المتغيرات البيئية
│
├── database/
│   ├── db.py                # الاتصال بقاعدة البيانات والعمليات المتعلقة بها
│   ├── reset_db.py          # سكربت لإعادة تهيئة قاعدة البيانات
│
├── localization/
│   ├── localization.py      # معالجة الترجمات اللغوية
│
├── routes/
│   ├── webhook.py           # نقطة الويب لبوت التلجرام
│   ├──__init__.py
│
├── services/
│   ├── telegram_bot.py      # وظائف بوت التلجرام
│
├── templates/
│   ├── support_message.txt  # قالب رسالة الدعم
│
├── tests/
│   ├── test_bot.py          # اختبارات لوظائف البوت
│
├──.env
├── requirements.txt         # قائمة الحزم المطلوبة
├── .gitignore               # ملفات ومجلدات يتم تجاهلها من نظام التحكم بالإصدارات
└── README.md                # توثيق المشروع
