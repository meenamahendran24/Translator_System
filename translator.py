from deep_translator import GoogleTranslator
from deep_translator.exceptions import (
    InvalidSourceOrTargetLanguage,
    RequestError,
    TooManyRequests,
    TranslationNotFound,
)


ERROR_PREFIX = "Translation Error:"


def translate_text(text: str, source_language: str, target_language: str) -> str:
    """Translate text and return a clear user-facing message if it cannot finish."""
    if not text.strip():
        return ""

    try:
        return GoogleTranslator(
            source=source_language,
            target=target_language,
            timeout=15,
        ).translate(text)
    except TooManyRequests:
        return f"{ERROR_PREFIX} The translation service is busy. Please try again shortly."
    except InvalidSourceOrTargetLanguage:
        return f"{ERROR_PREFIX} One of the selected languages is not supported."
    except TranslationNotFound:
        return f"{ERROR_PREFIX} No translation was returned. Try shorter or simpler text."
    except RequestError:
        return f"{ERROR_PREFIX} The translation service could not be reached. Check your connection and try again."
    except Exception:
        return f"{ERROR_PREFIX} Translation is temporarily unavailable. Please try again."
