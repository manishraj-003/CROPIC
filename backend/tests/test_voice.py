from app.services.voice import is_supported_language, normalize_transcript


def test_normalize_transcript():
    text = "  Heavy   rain   damaged crop  "
    assert normalize_transcript(text) == "heavy rain damaged crop"


def test_language_support():
    assert is_supported_language("hi")
    assert is_supported_language("en")
    assert not is_supported_language("xx")
