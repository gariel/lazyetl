
import io
import os

class LangText:
    def load(self, langname):
        pass

    def _loadText(self, text):
        self.translations = {k:s for k, s in [l.split("=", 2) for l in text.splitlines()]}

    def get(self, key, fallback=None):
        if key in self.translations:
            return self.translations[key]
        if fallback:
            return fallback
        return "[{}]".format(key)


class LangTextFile(LangText):
    def __init__(self):
        dirname = os.path.dirname(__file__)
        self.langpath = os.path.join(dirname, "translations")

    def load(self, langname):
        langfile = os.path.join(self.langpath, "{}.tlang".format(langname))
        with io.open(langfile) as f:
            text = f.read()
        self._loadText(text)


def translate(langTextClass=LangTextFile):
    def decorator(window):
        lang_activators = {}
        lang_fallback = {}

        def lang(self, tkey, changer, fallback=None):
            key = tkey
            lang_activators[key] = changer
            if fallback:
                lang_fallback[key] = fallback

        def lang_set(self, langname):
            self.langtext = langTextClass()
            self.langtext.load(langname)
            for key, activator in lang_activators.items():
                activator(self.langtext.get(key, lang_fallback.get(key)))

        window.lang = lang
        window.lang_set = lang_set
        return window
    return decorator
