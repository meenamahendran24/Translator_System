from deep_translator import GoogleTranslator


def translate_text(text, source_language, target_language):
    """
    Translate text from source language to target language.
    """

    if not text.strip():
        return ""

    try:
        translator = GoogleTranslator(
            source=source_language,
            target=target_language
        )

        result = translator.translate(text)

        return result

    except Exception as e:
        return f"Translation Error: {e}"