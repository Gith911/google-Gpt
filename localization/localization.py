from deep_translator import GoogleTranslator

def translate_text(text, target_lang='en', src_lang='auto'):
    translator = GoogleTranslator(source=src_lang, target=target_lang)
    return translator.translate(text)
