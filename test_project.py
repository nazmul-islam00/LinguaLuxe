from project import (
    generate_speech,
    detect_language,
    translate,
    get_synonym,
    get_antonym,
    get_meaning,
)
from gtts import tts
import pytest


def test_generate_speech():
    assert type(generate_speech("Hello world", "en", False)) is tts.gTTS
    with pytest.raises(ValueError):
        generate_speech()


def test_detect_language():
    assert detect_language("পরিসর") == "bn"
    assert detect_language("range") == "en"
    assert detect_language("العربية") == "ar"
    assert detect_language("Посольство") == "ru"
    with pytest.raises(ValueError):
        detect_language()


def test_translate():
    assert translate("life", "bn") == "জীবন"
    assert translate("hello", "bn") == "হ্যালো"
    assert translate("বিদায় পৃথিবী", "en") == "goodbye world"
    with pytest.raises(ValueError):
        translate()


def test_get_meaning():
    assert "Noun" in get_meaning("life")["parts_of_speech"]
    assert "Adjective" in get_meaning("good")["parts_of_speech"]
    with pytest.raises(ValueError):
        get_meaning()


def test_get_synonym():
    assert "activity" in get_synonym("life", "en")["synonyms"]
    assert "hi" in get_synonym("হ্যালো", "en")["synonyms"]
    with pytest.raises(ValueError):
        get_synonym()


def test_get_antonym():
    assert "end" in get_antonym("life", "en")["antonyms"]
    with pytest.raises(ValueError):
        get_antonym()
