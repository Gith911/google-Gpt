from deep_translator import GoogleTranslator
from langdetect import detect

def detect_language(text):
    return detect(text)

def translate_text(text, target_language):
    return GoogleTranslator(source='auto', target=target_language).translate(text)
