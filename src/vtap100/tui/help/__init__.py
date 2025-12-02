"""Help system for VTAP100 TUI Editor.

Loads context-sensitive help from YAML files with i18n support.
"""

from pathlib import Path

import yaml

from vtap100.tui.i18n import get_language


class HelpLoader:
    """Loads help content from YAML files with language support.

    Help files are stored in language-specific subdirectories:
    - help/de/*.yaml for German
    - help/en/*.yaml for English

    Each YAML file corresponds to a configuration section (vas.yaml, smarttap.yaml, etc.).

    The loader creates a flat dictionary structure:
    - "vas" -> section-level help
    - "vas.merchant_id" -> field-level help
    """

    HELP_DIR = Path(__file__).parent
    _cache: dict[str, dict[str, dict]] = {}

    @classmethod
    def load_all(cls) -> dict[str, dict]:
        """Load all help files for current language.

        Returns:
            Dictionary with section and field help.
            Keys are like "vas", "vas.merchant_id", "smarttap.collector_id".
        """
        lang = get_language().value  # "de" or "en"

        # Return cached data if available for this language
        if lang in cls._cache:
            return cls._cache[lang]

        result: dict[str, dict] = {}
        lang_dir = cls.HELP_DIR / lang

        if not lang_dir.exists():
            # Fallback to German if language dir doesn't exist
            lang_dir = cls.HELP_DIR / "de"

        for yaml_file in lang_dir.glob("*.yaml"):
            section = yaml_file.stem  # "vas", "smarttap", etc.
            try:
                with open(yaml_file, encoding="utf-8") as f:
                    data = yaml.safe_load(f) or {}

                # Section-level help
                if "section" in data:
                    result[section] = data["section"]

                # Field-level help: "vas.merchant_id"
                for field_name, field_help in data.get("fields", {}).items():
                    result[f"{section}.{field_name}"] = field_help

            except Exception:
                # Skip files that can't be parsed
                pass

        # Cache the result for this language
        cls._cache[lang] = result
        return result

    @classmethod
    def get_help(cls, context: str) -> dict:
        """Get help for a specific context.

        Args:
            context: The help context key (e.g., "vas.merchant_id").

        Returns:
            Dictionary with help content, or empty dict if not found.
        """
        return cls.load_all().get(context, {})

    @classmethod
    def clear_cache(cls) -> None:
        """Clear the help cache (useful for language switching and testing)."""
        cls._cache.clear()
