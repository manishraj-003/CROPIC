SUPPORTED_LANGUAGES = [
    "hi",
    "en",
    "bn",
    "te",
    "mr",
    "ta",
    "ur",
    "gu",
    "kn",
    "ml",
    "pa",
]


def normalize_transcript(transcript: str) -> str:
    return " ".join(transcript.strip().split()).lower()


def is_supported_language(language: str) -> bool:
    return language.lower() in SUPPORTED_LANGUAGES
