import streamlit as st

from history import get_history, save_translation
from languages import LANGUAGES
from translator import translate_text


st.set_page_config(
    page_title="Lingua | Translator",
    page_icon=":material/translate:",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def initialize_state():
    """Set predictable defaults for the interactive translator."""
    defaults = {
        "source_language": "English",
        "target_language": "French",
        "source_text": "",
        "translation": "",
        "has_translation": False,
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)


def swap_languages():
    st.session_state.source_language, st.session_state.target_language = (
        st.session_state.target_language,
        st.session_state.source_language,
    )


def clear_translator():
    st.session_state.source_text = ""
    st.session_state.translation = ""
    st.session_state.has_translation = False


def is_translation_error(text):
    return text.startswith("Translation Error:")


initialize_state()

st.markdown(
    """
    <style>
        .stApp {
            background:
                radial-gradient(circle at 8% 0%, rgba(99, 102, 241, 0.11), transparent 28rem),
                radial-gradient(circle at 92% 5%, rgba(14, 165, 233, 0.10), transparent 24rem);
        }
        .block-container {
            max-width: 1180px;
            padding-top: 3.25rem;
            padding-bottom: 4rem;
        }
        .hero-eyebrow {
            color: #4f46e5;
            font-size: 0.8rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            margin-bottom: 0.35rem;
        }
        .hero-copy {
            color: #64748b;
            font-size: 1.05rem;
            max-width: 39rem;
            margin-bottom: 1.5rem;
        }
        .st-key-translator_card,
        .st-key-history_card {
            box-shadow: 0 16px 45px rgba(15, 23, 42, 0.08);
            transition: transform 180ms ease, box-shadow 180ms ease;
        }
        .st-key-translator_card:hover,
        .st-key-history_card:hover {
            transform: translateY(-2px);
            box-shadow: 0 20px 52px rgba(15, 23, 42, 0.12);
        }
        .st-key-translator_card {
            animation: fade-in 380ms ease-out;
        }
        .st-key-translate_button button {
            min-height: 2.9rem;
            font-weight: 700;
            transition: transform 160ms ease, box-shadow 160ms ease;
        }
        .st-key-translate_button button:hover {
            transform: translateY(-1px);
            box-shadow: 0 8px 20px rgba(79, 70, 229, 0.24);
        }
        @keyframes fade-in {
            from { opacity: 0; transform: translateY(8px); }
            to { opacity: 1; transform: translateY(0); }
        }
        @media (max-width: 640px) {
            .block-container { padding-top: 1.75rem; padding-left: 1rem; padding-right: 1rem; }
            .hero-copy { font-size: 0.98rem; }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("<p class='hero-eyebrow'>Clear communication, anywhere</p>", unsafe_allow_html=True)
st.title(":material/translate: Lingua translator")
st.markdown(
    "<p class='hero-copy'>Translate your words with a focused workspace designed for fast, natural language switching.</p>",
    unsafe_allow_html=True,
)

with st.container(border=True, key="translator_card", gap="medium"):
    top_left, top_middle, top_right = st.columns([1, 0.16, 1], vertical_alignment="bottom")

    with top_left:
        st.markdown("#### :material/input: Translate from")
        source_language = st.selectbox(
            "Source language",
            list(LANGUAGES.keys()),
            key="source_language",
            help="Choose the language your text is written in.",
        )

    with top_middle:
        st.button(
            "Swap",
            icon=":material/swap_horiz:",
            help="Swap source and target languages",
            on_click=swap_languages,
            key="swap_button",
            width="stretch",
        )

    with top_right:
        st.markdown("#### :material/output: Translate to")
        target_language = st.selectbox(
            "Target language",
            list(LANGUAGES.keys()),
            key="target_language",
            help="Choose the language you want to translate into.",
        )

    source_column, target_column = st.columns(2, gap="large")

    with source_column:
        st.caption("SOURCE TEXT")
        text = st.text_area(
            "Text to translate",
            key="source_text",
            height=230,
            placeholder="Type or paste text here…",
            label_visibility="collapsed",
        )
        st.caption(f"{len(text):,} characters")

    with target_column:
        st.caption("TRANSLATION")
        if st.session_state.has_translation:
            st.code(st.session_state.translation, language=None, wrap_lines=True)
            st.caption("Use the copy icon in the translation box to copy the result.")
        else:
            with st.container(border=True, height=230, key="translation_empty"):
                st.markdown("#### :material/auto_awesome: Ready when you are")
                st.caption("Your translation will appear here after you translate your text.")

    action_left, action_right = st.columns([3, 1], vertical_alignment="center")
    with action_left:
        translate_clicked = st.button(
            "Translate",
            icon=":material/translate:",
            type="primary",
            key="translate_button",
            width="stretch",
        )
    with action_right:
        st.button(
            "Clear",
            icon=":material/ink_eraser:",
            on_click=clear_translator,
            key="clear_button",
            width="stretch",
        )

if translate_clicked:
    if not text.strip():
        st.warning("Enter some text before translating.", icon=":material/edit_note:")
    elif source_language == target_language:
        st.info(
            "Choose two different languages to translate your text.",
            icon=":material/info:",
        )
    else:
        with st.spinner("Translating your text…"):
            translated_text = translate_text(
                text,
                LANGUAGES[source_language],
                LANGUAGES[target_language],
            )

        if is_translation_error(translated_text):
            st.session_state.has_translation = False
            st.error(translated_text, icon=":material/error:")
        else:
            st.session_state.translation = translated_text
            st.session_state.has_translation = True
            save_translation(source_language, target_language, text, translated_text)
            st.toast("Translation ready", icon=":material/check_circle:")
            st.rerun()

st.space("large")

with st.container(border=True, key="history_card", gap="small"):
    history_title, history_count = st.columns([4, 1], vertical_alignment="center")
    with history_title:
        st.subheader("Translation history", anchor=False)
        st.caption("Your most recent translations, saved locally on this app instance.")
    with history_count:
        history = get_history()
        st.badge(f"{len(history)} saved", icon=":material/history:", color="blue")

    if not history.empty:
        newest_first = history.iloc[::-1].reset_index(drop=True)
        st.dataframe(
            newest_first,
            column_config={
                "Source Language": st.column_config.TextColumn("From", width="small"),
                "Target Language": st.column_config.TextColumn("To", width="small"),
                "Original Text": st.column_config.TextColumn("Original", width="large"),
                "Translated Text": st.column_config.TextColumn("Translation", width="large"),
            },
            hide_index=True,
            width="stretch",
            height=min(380, 80 + len(newest_first) * 36),
        )
    else:
        with st.container(horizontal_alignment="center", gap="xsmall"):
            st.markdown("### :material/history: No translations yet")
            st.caption("Your completed translations will appear here for quick reference.")
