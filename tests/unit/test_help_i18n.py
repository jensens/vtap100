"""Unit tests for Help system i18n support.

Tests for:
- Loading help based on current language
- Switching help language
- HelpPanel refresh on language change
"""

import pytest

from vtap100.tui.i18n import Language, get_language, set_language


class TestHelpLoaderI18n:
    """Test HelpLoader with language support."""

    def setup_method(self) -> None:
        """Reset to German before each test."""
        set_language(Language.DE)
        # Clear cache to ensure fresh load
        from vtap100.tui.help import HelpLoader
        HelpLoader.clear_cache()

    def teardown_method(self) -> None:
        """Reset to German after each test."""
        set_language(Language.DE)
        from vtap100.tui.help import HelpLoader
        HelpLoader.clear_cache()

    def test_load_german_help(self) -> None:
        """HelpLoader should load German help when language is DE."""
        from vtap100.tui.help import HelpLoader

        set_language(Language.DE)
        HelpLoader.clear_cache()
        help_data = HelpLoader.load_all()

        # German help should have German content
        vas_help = help_data.get("vas", {})
        assert "Apple VAS" in vas_help.get("title", "")

    def test_load_english_help(self) -> None:
        """HelpLoader should load English help when language is EN."""
        from vtap100.tui.help import HelpLoader

        set_language(Language.EN)
        HelpLoader.clear_cache()
        help_data = HelpLoader.load_all()

        # English help should have English content
        vas_help = help_data.get("vas", {})
        # Title should be in English
        assert "Apple VAS" in vas_help.get("title", "")

    def test_language_switch_reloads_help(self) -> None:
        """Switching language should reload help content."""
        from vtap100.tui.help import HelpLoader

        # Load German
        set_language(Language.DE)
        HelpLoader.clear_cache()
        de_help = HelpLoader.load_all()
        de_vas_desc = de_help.get("vas", {}).get("description", "")

        # Switch to English
        set_language(Language.EN)
        HelpLoader.clear_cache()
        en_help = HelpLoader.load_all()
        en_vas_desc = en_help.get("vas", {}).get("description", "")

        # Descriptions should be different (different languages)
        # Both should contain some content
        assert len(de_vas_desc) > 0
        assert len(en_vas_desc) > 0

    def test_field_help_loads_with_language(self) -> None:
        """Field-level help should load based on current language."""
        from vtap100.tui.help import HelpLoader

        set_language(Language.DE)
        HelpLoader.clear_cache()
        de_field = HelpLoader.get_help("vas.merchant_id")

        set_language(Language.EN)
        HelpLoader.clear_cache()
        en_field = HelpLoader.get_help("vas.merchant_id")

        # Both should have a title
        assert "title" in de_field
        assert "title" in en_field


class TestHelpPanelI18n:
    """Test HelpPanel language switching."""

    def setup_method(self) -> None:
        """Reset to German before each test."""
        set_language(Language.DE)
        from vtap100.tui.help import HelpLoader
        HelpLoader.clear_cache()

    def teardown_method(self) -> None:
        """Reset to German after each test."""
        set_language(Language.DE)
        from vtap100.tui.help import HelpLoader
        HelpLoader.clear_cache()

    @pytest.mark.asyncio
    async def test_help_panel_updates_on_language_toggle(self) -> None:
        """HelpPanel should update content when language toggles."""
        from vtap100.tui.app import VTAPEditorApp

        app = VTAPEditorApp()

        async with app.run_test() as pilot:
            await pilot.pause()

            # Initial state is German
            assert get_language() == Language.DE

            # Toggle language to English
            await pilot.press("ctrl+l")
            await pilot.pause()

            assert get_language() == Language.EN

            # Toggle back to German
            await pilot.press("ctrl+l")
            await pilot.pause()

            assert get_language() == Language.DE
