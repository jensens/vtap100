"""Extended unit tests for TUI App.

Additional tests to improve coverage for:
- App initialization with invalid files
- Language toggle
- Save and export actions
- Preview mode toggle
"""

from pathlib import Path
import pytest
import tempfile
from vtap100.models.config import VTAPConfig
from vtap100.models.keyboard import KeyboardConfig
from vtap100.models.vas import AppleVASConfig


class TestAppLoadConfig:
    """Test app config loading."""

    @pytest.mark.asyncio
    async def test_app_loads_valid_config_file(self) -> None:
        """App should load valid config.txt file."""
        from vtap100.tui.app import VTAPEditorApp

        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "config.txt"
            config_path.write_text(
                "!VTAPconfig\n" "VAS1MerchantID=pass.com.example.test\n" "VAS1KeySlot=1\n"
            )

            app = VTAPEditorApp(input_path=config_path)
            assert len(app.config.vas_configs) == 1
            assert app.config.vas_configs[0].merchant_id == "pass.com.example.test"

    @pytest.mark.asyncio
    async def test_app_handles_invalid_config_file(self) -> None:
        """App should handle invalid config.txt gracefully."""
        from vtap100.tui.app import VTAPEditorApp

        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "config.txt"
            config_path.write_text("This is not a valid config file\n")

            # Should not crash, returns empty config
            app = VTAPEditorApp(input_path=config_path)
            assert app.config is not None

    @pytest.mark.asyncio
    async def test_app_handles_nonexistent_file(self) -> None:
        """App should handle nonexistent file gracefully."""
        from vtap100.tui.app import VTAPEditorApp

        app = VTAPEditorApp(input_path=Path("/nonexistent/path/config.txt"))
        # Should not crash, returns empty config
        assert app.config is not None


class TestPreviewModeToggle:
    """Test preview mode toggle functionality."""

    @pytest.mark.asyncio
    async def test_toggle_preview_cycles_through_modes(self) -> None:
        """Toggle preview should cycle: default -> maximized -> hidden -> default."""
        from vtap100.tui.app import PreviewMode
        from vtap100.tui.app import VTAPEditorApp

        app = VTAPEditorApp()

        async with app.run_test() as pilot:
            await pilot.pause()

            # Initial state is DEFAULT
            assert app.preview_mode == PreviewMode.DEFAULT

            # First toggle -> MAXIMIZED
            app.action_toggle_preview()
            await pilot.pause()
            assert app.preview_mode == PreviewMode.MAXIMIZED

            # Second toggle -> HIDDEN
            app.action_toggle_preview()
            await pilot.pause()
            assert app.preview_mode == PreviewMode.HIDDEN

            # Third toggle -> back to DEFAULT
            app.action_toggle_preview()
            await pilot.pause()
            assert app.preview_mode == PreviewMode.DEFAULT


class TestHelpToggle:
    """Test help panel toggle functionality."""

    @pytest.mark.asyncio
    async def test_toggle_help_hides_panel(self) -> None:
        """Toggle help should hide the help panel."""
        from vtap100.tui.app import VTAPEditorApp

        app = VTAPEditorApp()

        async with app.run_test() as pilot:
            await pilot.pause()

            help_panel = app.screen.query_one("#help-panel")
            initial_display = help_panel.display

            # Toggle
            app.action_toggle_help()
            await pilot.pause()

            # Display should have changed
            assert help_panel.display != initial_display

            # Toggle back
            app.action_toggle_help()
            await pilot.pause()
            assert help_panel.display == initial_display


class TestLanguageToggle:
    """Test language toggle functionality."""

    @pytest.mark.asyncio
    async def test_toggle_language_changes_language(self) -> None:
        """Toggle language should switch between DE and EN."""
        from vtap100.tui.app import VTAPEditorApp
        from vtap100.tui.i18n import Language
        from vtap100.tui.i18n import get_language
        from vtap100.tui.i18n import set_language

        # Ensure we start with DE
        set_language(Language.DE)

        app = VTAPEditorApp()

        async with app.run_test() as pilot:
            await pilot.pause()

            initial_lang = get_language()
            assert initial_lang == Language.DE

            # Toggle language
            await app.action_toggle_language()
            await pilot.pause()

            # Language should have changed
            new_lang = get_language()
            assert new_lang == Language.EN

            # Toggle back
            await app.action_toggle_language()
            await pilot.pause()

            assert get_language() == Language.DE


class TestSaveAction:
    """Test save action functionality."""

    @pytest.mark.asyncio
    async def test_save_writes_to_output_path(self) -> None:
        """Save should write config to output path."""
        from vtap100.tui.app import VTAPEditorApp

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "output.txt"
            app = VTAPEditorApp(output_path=output_path)
            app.config = VTAPConfig(
                vas_configs=[AppleVASConfig(merchant_id="pass.com.test", key_slot=1)]
            )

            async with app.run_test() as pilot:
                await pilot.pause()

                app.action_save()
                await pilot.pause()

                # File should exist
                assert output_path.exists()
                content = output_path.read_text()
                assert "!VTAPconfig" in content
                assert "pass.com.test" in content

    @pytest.mark.asyncio
    async def test_save_without_output_path_shows_error(self) -> None:
        """Save without output path should show error notification."""
        from vtap100.tui.app import VTAPEditorApp

        app = VTAPEditorApp()  # No output path

        async with app.run_test() as pilot:
            await pilot.pause()

            app.action_save()
            await pilot.pause()

            # Should not crash - just shows error notification


class TestExportAction:
    """Test export action functionality."""

    @pytest.mark.asyncio
    async def test_export_opens_dialog(self) -> None:
        """Export action should open export dialog."""
        from vtap100.tui.app import VTAPEditorApp
        from vtap100.tui.screens.export_dialog import ExportDialog

        app = VTAPEditorApp()

        async with app.run_test() as pilot:
            await pilot.pause()

            app.action_export()
            await pilot.pause()

            # Export dialog should be on screen stack
            assert isinstance(app.screen, ExportDialog)


class TestLanguageToggleWithFormValues:
    """Test that language toggle preserves form values."""

    @pytest.mark.asyncio
    async def test_toggle_language_preserves_expanded_sections(self) -> None:
        """Language toggle should preserve which sections are expanded."""
        from textual.widgets import Tree
        from vtap100.tui.app import VTAPEditorApp
        from vtap100.tui.i18n import Language
        from vtap100.tui.i18n import set_language

        set_language(Language.DE)

        app = VTAPEditorApp()
        app.config = VTAPConfig(keyboard=KeyboardConfig(log_mode=True))

        async with app.run_test() as pilot:
            await pilot.pause()

            # Expand keyboard section
            sidebar = app.screen.query_one("#sidebar")
            tree = sidebar.query_one(Tree)
            keyboard_node = tree.root.children[2]
            keyboard_node.expand()
            await pilot.pause()

            # Toggle language
            await app.action_toggle_language()
            await pilot.pause()

            # Keyboard section should still be expanded
            tree = sidebar.query_one(Tree)
            keyboard_node = tree.root.children[2]
            assert keyboard_node.is_expanded
