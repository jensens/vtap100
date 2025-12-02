"""Internationalization (i18n) module for the TUI.

Provides a simple translation system using YAML files.

Usage:
    from vtap100.tui.i18n import t, set_language, get_language

    # Set language (default is 'de')
    set_language('en')

    # Get translation
    label = t('buttons.save')  # Returns "Save" or "Speichern"

    # With placeholders
    msg = t('messages.config_saved', name='VAS')  # "VAS configuration saved"
"""

from enum import Enum
from functools import lru_cache
from pathlib import Path
from typing import Any
import yaml


class Language(str, Enum):
    """Supported languages."""

    DE = "de"
    EN = "en"


# Global language setting
_current_language: Language = Language.DE


def set_language(lang: Language | str) -> None:
    """Set the current language.

    Args:
        lang: Language code ('de' or 'en') or Language enum.
    """
    global _current_language
    if isinstance(lang, str):
        lang = Language(lang)
    _current_language = lang
    # Clear cache when language changes
    _load_translations.cache_clear()


def get_language() -> Language:
    """Get the current language.

    Returns:
        The current Language enum value.
    """
    return _current_language


@lru_cache(maxsize=2)
def _load_translations(lang: Language) -> dict[str, Any]:
    """Load translations for a language.

    Args:
        lang: The language to load.

    Returns:
        Dictionary of translations.
    """
    translations_dir = Path(__file__).parent / "translations"
    file_path = translations_dir / f"{lang.value}.yaml"

    if not file_path.exists():
        return {}

    with open(file_path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _get_nested(data: dict, key: str, default: str = "") -> str:
    """Get a nested value from a dictionary using dot notation.

    Args:
        data: The dictionary to search.
        key: Dot-separated key path (e.g., 'buttons.save').
        default: Default value if key not found.

    Returns:
        The value at the key path, or default.
    """
    parts = key.split(".")
    current = data

    for part in parts:
        if isinstance(current, dict) and part in current:
            current = current[part]
        else:
            return default

    return str(current) if current is not None else default


def t(key: str, **kwargs: Any) -> str:
    """Get a translated string.

    Args:
        key: The translation key (dot notation, e.g., 'buttons.save').
        **kwargs: Placeholder values to substitute.

    Returns:
        The translated string with placeholders replaced.
    """
    translations = _load_translations(_current_language)
    text = _get_nested(translations, key, key)

    # Replace placeholders: {name} -> value
    if kwargs:
        for name, value in kwargs.items():
            text = text.replace(f"{{{name}}}", str(value))

    return text


def t_help(section: str, field: str | None = None, attr: str = "title") -> str:
    """Get help text translation.

    Uses the HelpLoader to get language-specific help content from YAML files.

    Args:
        section: The section name (e.g., 'vas', 'keyboard').
        field: Optional field name (e.g., 'merchant_id').
        attr: The attribute to get ('title', 'description', 'tip', etc.).

    Returns:
        The translated help text.
    """
    from vtap100.tui.help import HelpLoader

    if field:
        context = f"{section}.{field}"
    else:
        context = section

    help_data = HelpLoader.get_help(context)
    return help_data.get(attr, "")


# Convenience alias
_ = t
