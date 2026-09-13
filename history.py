import os
import pandas as pd


HISTORY_FILE = "data/translation_history.csv"


def save_translation(
    source_language,
    target_language,
    original_text,
    translated_text
):
    os.makedirs("data", exist_ok=True)

    new_data = pd.DataFrame([
        {
            "Source Language": source_language,
            "Target Language": target_language,
            "Original Text": original_text,
            "Translated Text": translated_text
        }
    ])

    if os.path.exists(HISTORY_FILE):
        old_data = pd.read_csv(HISTORY_FILE)
        data = pd.concat([old_data, new_data], ignore_index=True)
    else:
        data = new_data

    data.to_csv(HISTORY_FILE, index=False)


def get_history():
    if os.path.exists(HISTORY_FILE):
        return pd.read_csv(HISTORY_FILE)

    return pd.DataFrame(
        columns=[
            "Source Language",
            "Target Language",
            "Original Text",
            "Translated Text"
        ]
    )