from PyMultiDictionary import MultiDictionary


class DictionaryProcessor:
    _multi_dictionary = MultiDictionary()

    @classmethod
    def get_meaning(cls, text: str = "", lang: str = "en") -> dict[str, list[str]]:
        response = cls._multi_dictionary.meaning(lang, text)
        return {"parts_of_speech": response[0], "meanings": list(response[1:])}

    @classmethod
    def get_synonym(cls, text: str = "", lang: str = "en") -> dict[str, list[str]]:
        return {"synonyms": cls._multi_dictionary.synonym(lang, text)}

    @classmethod
    def get_antonym(cls, text: str = "", lang: str = "en") -> dict[str, list[str]]:
        return {"antonyms": cls._multi_dictionary.antonym(lang, text)}
