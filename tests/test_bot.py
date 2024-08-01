import unittest
from localization.localization import translate_text

class TestBot(unittest.TestCase):

    def test_translation(self):
        result = translate_text("مرحبا", target_lang='en', src_lang='auto')
        self.assertEqual(result, "Hello")  # تأكد من النتيجة الصحيحة

if __name__ == '__main__':
    unittest.main()
