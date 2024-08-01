import unittest
from services.telegram_bot import detect_language, translate_text

class TestTelegramBot(unittest.TestCase):
    def test_detect_language(self):
        self.assertEqual(detect_language("Hello"), "en")
        self.assertEqual(detect_language("مرحبا"), "ar")

    def test_translate_text(self):
        self.assertEqual(translate_text("Hello", "ar"), "مرحبا")
        self.assertEqual(translate_text("مرحبا", "en"), "Hello")

if __name__ == "__main__":
    unittest.main()
