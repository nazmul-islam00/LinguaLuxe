from deep_translator import GoogleTranslator
from langid import classify


class Translator:
    _google_translator = GoogleTranslator()

    @classmethod
    def detect_language(cls, text: str = "") -> str:
        return classify(text)[0]

    @classmethod
    def get_supported_languages(cls) -> dict[str, str]:
        return cls._google_translator.get_supported_languages(as_dict=True)

    @classmethod
    def translate(cls, text: str = "", lang: str = "en") -> str:
        cls._google_translator.source, cls._google_translator.target = "auto", lang
        return cls._google_translator.translate(text)
