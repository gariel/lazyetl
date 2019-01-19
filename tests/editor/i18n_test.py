
from unittest import TestCase

from i18n import translate, LangText

langs = {
    "lang1": "asd.text=aaa",
    "lang2": "asd.text=bbb"
}

class TestLangText(LangText):
    def load(self, langname):
        super(TestLangText, self)._loadText(langs[langname])

@translate(TestLangText)
class TestTranslation:
    def __init__(self):
        self.text = "notset"
        self.lang("asd.text", self.set_text)

    def set_text(self, text):
        self.text = text

class StepsTest(TestCase):
    def test_should_(self):
        testt = TestTranslation()
        self.assertEqual(testt.text, "notset")
        testt.lang_set("lang1")
        self.assertEqual(testt.text, "aaa")
        testt.lang_set("lang2")
        self.assertEqual(testt.text, "bbb")
