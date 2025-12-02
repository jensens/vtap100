"""Unit tests for TUI i18n module.

Tests for:
- Language switching
- Translation loading
- Translation retrieval with placeholders
- Help text retrieval
"""


class TestI18nImports:
    """Test that i18n module can be imported."""

    def test_import_i18n(self) -> None:
        """i18n module should be importable."""
        from vtap100.tui.i18n import Language
        from vtap100.tui.i18n import get_language
        from vtap100.tui.i18n import set_language
        from vtap100.tui.i18n import t

        assert Language is not None
        assert t is not None
        assert set_language is not None
        assert get_language is not None

    def test_import_alias(self) -> None:
        """Underscore alias should be available."""
        from vtap100.tui.i18n import _

        assert _ is not None


class TestLanguageSwitching:
    """Test language switching functionality."""

    def test_default_language_is_german(self) -> None:
        """Default language should be German."""
        from vtap100.tui.i18n import Language
        from vtap100.tui.i18n import get_language
        from vtap100.tui.i18n import set_language

        # Reset to default
        set_language(Language.DE)
        assert get_language() == Language.DE

    def test_switch_to_english(self) -> None:
        """Should be able to switch to English."""
        from vtap100.tui.i18n import Language
        from vtap100.tui.i18n import get_language
        from vtap100.tui.i18n import set_language

        set_language(Language.EN)
        assert get_language() == Language.EN

        # Reset
        set_language(Language.DE)

    def test_switch_with_string(self) -> None:
        """Should be able to switch using string."""
        from vtap100.tui.i18n import Language
        from vtap100.tui.i18n import get_language
        from vtap100.tui.i18n import set_language

        set_language("en")
        assert get_language() == Language.EN

        set_language("de")
        assert get_language() == Language.DE


class TestTranslations:
    """Test translation retrieval."""

    def test_german_save_button(self) -> None:
        """Should return German translation for save button."""
        from vtap100.tui.i18n import Language
        from vtap100.tui.i18n import set_language
        from vtap100.tui.i18n import t

        set_language(Language.DE)
        assert t("common.buttons.save") == "Speichern"

    def test_english_save_button(self) -> None:
        """Should return English translation for save button."""
        from vtap100.tui.i18n import Language
        from vtap100.tui.i18n import set_language
        from vtap100.tui.i18n import t

        set_language(Language.EN)
        result = t("common.buttons.save")
        set_language(Language.DE)  # Reset
        assert result == "Save"

    def test_german_add_button(self) -> None:
        """Should return German translation for add button."""
        from vtap100.tui.i18n import Language
        from vtap100.tui.i18n import set_language
        from vtap100.tui.i18n import t

        set_language(Language.DE)
        assert t("common.buttons.add") == "Hinzufügen"

    def test_english_add_button(self) -> None:
        """Should return English translation for add button."""
        from vtap100.tui.i18n import Language
        from vtap100.tui.i18n import set_language
        from vtap100.tui.i18n import t

        set_language(Language.EN)
        result = t("common.buttons.add")
        set_language(Language.DE)
        assert result == "Add"

    def test_missing_key_returns_key(self) -> None:
        """Missing key should return the key itself."""
        from vtap100.tui.i18n import t

        result = t("nonexistent.key.path")
        assert result == "nonexistent.key.path"

    def test_placeholder_substitution(self) -> None:
        """Placeholders should be substituted."""
        from vtap100.tui.i18n import Language
        from vtap100.tui.i18n import set_language
        from vtap100.tui.i18n import t

        set_language(Language.DE)
        result = t("common.messages.config_added", name="VAS")
        assert "VAS" in result
        assert "Konfiguration" in result

    def test_english_placeholder_substitution(self) -> None:
        """Placeholders should work in English too."""
        from vtap100.tui.i18n import Language
        from vtap100.tui.i18n import set_language
        from vtap100.tui.i18n import t

        set_language(Language.EN)
        result = t("common.messages.config_added", name="VAS")
        set_language(Language.DE)
        assert "VAS" in result
        assert "configuration" in result


class TestSectionLabels:
    """Test section label translations."""

    def test_german_section_labels(self) -> None:
        """German section labels should be correct."""
        from vtap100.tui.i18n import Language
        from vtap100.tui.i18n import set_language
        from vtap100.tui.i18n import t

        set_language(Language.DE)
        assert t("sections.vas.label") == "Apple VAS"
        assert t("sections.keyboard.label") == "Keyboard"
        assert t("sections.nfc.label") == "NFC Tags"

    def test_english_section_labels(self) -> None:
        """English section labels should be correct."""
        from vtap100.tui.i18n import Language
        from vtap100.tui.i18n import set_language
        from vtap100.tui.i18n import t

        set_language(Language.EN)
        vas_label = t("sections.vas.label")
        keyboard_label = t("sections.keyboard.label")
        set_language(Language.DE)

        assert vas_label == "Apple VAS"
        assert keyboard_label == "Keyboard"


class TestFormFields:
    """Test form field translations."""

    def test_german_keyboard_fields(self) -> None:
        """German keyboard form fields should be correct."""
        from vtap100.tui.i18n import Language
        from vtap100.tui.i18n import set_language
        from vtap100.tui.i18n import t

        set_language(Language.DE)
        assert "Keyboard aktivieren" in t("forms.keyboard.enable")
        assert "Datenquellen" in t("forms.keyboard.source")

    def test_english_keyboard_fields(self) -> None:
        """English keyboard form fields should be correct."""
        from vtap100.tui.i18n import Language
        from vtap100.tui.i18n import set_language
        from vtap100.tui.i18n import t

        set_language(Language.EN)
        enable = t("forms.keyboard.enable")
        source = t("forms.keyboard.source")
        set_language(Language.DE)

        assert "Enable Keyboard" in enable
        assert "Data Sources" in source


class TestHelpContent:
    """Test help content translations (loaded from help/{lang}/*.yaml)."""

    def setup_method(self) -> None:
        """Reset to German and clear cache before each test."""
        from vtap100.tui.help import HelpLoader
        from vtap100.tui.i18n import Language
        from vtap100.tui.i18n import set_language

        set_language(Language.DE)
        HelpLoader.clear_cache()

    def teardown_method(self) -> None:
        """Reset to German and clear cache after each test."""
        from vtap100.tui.help import HelpLoader
        from vtap100.tui.i18n import Language
        from vtap100.tui.i18n import set_language

        set_language(Language.DE)
        HelpLoader.clear_cache()

    def test_german_vas_help(self) -> None:
        """German VAS help content should exist."""
        from vtap100.tui.help import HelpLoader
        from vtap100.tui.i18n import Language
        from vtap100.tui.i18n import set_language

        set_language(Language.DE)
        HelpLoader.clear_cache()
        help_data = HelpLoader.get_help("vas")

        assert "Apple VAS" in help_data.get("title", "")
        assert "Apple Wallet" in help_data.get("description", "")

    def test_english_vas_help(self) -> None:
        """English VAS help content should exist."""
        from vtap100.tui.help import HelpLoader
        from vtap100.tui.i18n import Language
        from vtap100.tui.i18n import set_language

        set_language(Language.EN)
        HelpLoader.clear_cache()
        help_data = HelpLoader.get_help("vas")

        assert "Apple VAS" in help_data.get("title", "")
        assert "Apple Wallet" in help_data.get("description", "")

    def test_german_merchant_id_help(self) -> None:
        """German merchant_id help should have all fields."""
        from vtap100.tui.help import HelpLoader
        from vtap100.tui.i18n import Language
        from vtap100.tui.i18n import set_language

        set_language(Language.DE)
        HelpLoader.clear_cache()
        help_data = HelpLoader.get_help("vas.merchant_id")

        assert "Merchant ID" in help_data.get("title", "")
        assert len(help_data.get("description", "")) > 20
        assert len(help_data.get("tip", "")) > 20

    def test_english_merchant_id_help(self) -> None:
        """English merchant_id help should have all fields."""
        from vtap100.tui.help import HelpLoader
        from vtap100.tui.i18n import Language
        from vtap100.tui.i18n import set_language

        set_language(Language.EN)
        HelpLoader.clear_cache()
        help_data = HelpLoader.get_help("vas.merchant_id")

        assert "Merchant ID" in help_data.get("title", "")
        assert "Apple Developer Portal" in help_data.get("description", "")


class TestTHelpFunction:
    """Test the t_help convenience function."""

    def setup_method(self) -> None:
        """Reset to German and clear cache before each test."""
        from vtap100.tui.help import HelpLoader
        from vtap100.tui.i18n import Language
        from vtap100.tui.i18n import set_language

        set_language(Language.DE)
        HelpLoader.clear_cache()

    def teardown_method(self) -> None:
        """Reset to German and clear cache after each test."""
        from vtap100.tui.help import HelpLoader
        from vtap100.tui.i18n import Language
        from vtap100.tui.i18n import set_language

        set_language(Language.DE)
        HelpLoader.clear_cache()

    def test_t_help_section(self) -> None:
        """t_help should get section help."""
        from vtap100.tui.help import HelpLoader
        from vtap100.tui.i18n import Language
        from vtap100.tui.i18n import set_language
        from vtap100.tui.i18n import t_help

        set_language(Language.DE)
        HelpLoader.clear_cache()
        title = t_help("vas", attr="title")
        assert "Apple VAS" in title

    def test_t_help_field(self) -> None:
        """t_help should get field help."""
        from vtap100.tui.help import HelpLoader
        from vtap100.tui.i18n import Language
        from vtap100.tui.i18n import set_language
        from vtap100.tui.i18n import t_help

        set_language(Language.DE)
        HelpLoader.clear_cache()
        title = t_help("vas", "merchant_id", "title")
        assert "Merchant ID" in title

    def test_t_help_english(self) -> None:
        """t_help should work in English."""
        from vtap100.tui.help import HelpLoader
        from vtap100.tui.i18n import Language
        from vtap100.tui.i18n import set_language
        from vtap100.tui.i18n import t_help

        set_language(Language.EN)
        HelpLoader.clear_cache()
        title = t_help("keyboard", attr="title")
        assert "Keyboard Emulation" in title
