"""Unit tests for TUI Export Dialog.

Tests for:
- Export dialog opening with Ctrl+E
- Format selection (full vs template)
- Target selection (file vs clipboard)
- Cancel functionality
"""

import pytest
from unittest.mock import patch, MagicMock


class TestExportDialog:
    """Tests for ExportDialog ModalScreen."""

    @pytest.mark.asyncio
    async def test_dialog_opens_with_ctrl_e(self) -> None:
        """Ctrl+E should open the export dialog."""
        from vtap100.tui.app import VTAPEditorApp
        from vtap100.tui.screens.export_dialog import ExportDialog

        app = VTAPEditorApp()
        async with app.run_test() as pilot:
            await pilot.pause()
            await pilot.press("ctrl+e")
            await pilot.pause()

            # Dialog should be the current screen (modal)
            assert isinstance(app.screen, ExportDialog)

    @pytest.mark.asyncio
    async def test_dialog_has_format_options(self) -> None:
        """Dialog should have full and template export options."""
        from textual.widgets import RadioButton
        from vtap100.tui.app import VTAPEditorApp
        from vtap100.tui.screens.export_dialog import ExportDialog

        app = VTAPEditorApp()
        async with app.run_test() as pilot:
            await pilot.pause()
            await pilot.press("ctrl+e")
            await pilot.pause()

            # Should have radio buttons for format and target (4 total)
            assert isinstance(app.screen, ExportDialog)
            radios = app.screen.query(RadioButton)
            assert len(radios) == 4  # 2 format + 2 target

    @pytest.mark.asyncio
    async def test_cancel_closes_dialog_with_escape(self) -> None:
        """Escape should close dialog without action."""
        from vtap100.tui.app import VTAPEditorApp
        from vtap100.tui.screens.export_dialog import ExportDialog
        from vtap100.tui.screens.editor import EditorScreen

        app = VTAPEditorApp()
        async with app.run_test() as pilot:
            await pilot.pause()
            await pilot.press("ctrl+e")
            await pilot.pause()

            # Dialog should be open
            assert isinstance(app.screen, ExportDialog)

            # Press escape
            await pilot.press("escape")
            await pilot.pause()

            # Should be back to editor screen
            assert isinstance(app.screen, EditorScreen)

    @pytest.mark.asyncio
    async def test_cancel_button_closes_dialog(self) -> None:
        """Cancel button should close dialog without action."""
        from textual.widgets import Button
        from vtap100.tui.app import VTAPEditorApp
        from vtap100.tui.screens.export_dialog import ExportDialog
        from vtap100.tui.screens.editor import EditorScreen

        app = VTAPEditorApp()
        async with app.run_test() as pilot:
            await pilot.pause()
            await pilot.press("ctrl+e")
            await pilot.pause()

            # Click cancel button
            assert isinstance(app.screen, ExportDialog)
            cancel_btn = app.screen.query_one("#cancel-btn", Button)
            cancel_btn.press()
            await pilot.pause()

            # Should be back to editor screen
            assert isinstance(app.screen, EditorScreen)


class TestExportDialogFormats:
    """Tests for export format selection."""

    @pytest.mark.asyncio
    async def test_full_export_includes_vas(self, tmp_path) -> None:
        """Full export should include VAS configs."""
        from textual.widgets import Button
        from vtap100.models.vas import AppleVASConfig
        from vtap100.tui.app import VTAPEditorApp
        from vtap100.tui.screens.export_dialog import ExportDialog

        output_file = tmp_path / "config.txt"
        app = VTAPEditorApp(output_path=output_file)

        async with app.run_test() as pilot:
            await pilot.pause()

            # Add VAS config
            app.config.vas_configs.append(
                AppleVASConfig(merchant_id="pass.com.test", key_slot=1)
            )

            # Open dialog and export (full is default)
            await pilot.press("ctrl+e")
            await pilot.pause()

            assert isinstance(app.screen, ExportDialog)
            export_btn = app.screen.query_one("#export-btn", Button)
            export_btn.press()
            await pilot.pause()

            # File should contain VAS config
            content = output_file.read_text()
            assert "VAS1MerchantID=pass.com.test" in content

    @pytest.mark.asyncio
    async def test_template_export_excludes_vas(self, tmp_path) -> None:
        """Template export should exclude VAS configs and include Jinja placeholder."""
        from textual.widgets import Button, RadioButton
        from vtap100.models.vas import AppleVASConfig
        from vtap100.models.keyboard import KeyboardConfig
        from vtap100.tui.app import VTAPEditorApp
        from vtap100.tui.screens.export_dialog import ExportDialog

        output_file = tmp_path / "config.txt"
        app = VTAPEditorApp(output_path=output_file)

        async with app.run_test() as pilot:
            await pilot.pause()

            # Add configs
            app.config.vas_configs.append(
                AppleVASConfig(merchant_id="pass.com.test", key_slot=1)
            )
            app.config.keyboard = KeyboardConfig(log_mode=True)

            # Open dialog
            await pilot.press("ctrl+e")
            await pilot.pause()

            # Select template format
            assert isinstance(app.screen, ExportDialog)
            template_radio = app.screen.query_one("#format-template", RadioButton)
            template_radio.toggle()
            await pilot.pause()

            # Export
            export_btn = app.screen.query_one("#export-btn", Button)
            export_btn.press()
            await pilot.pause()

            # Template export uses .j2 extension
            template_file = tmp_path / "config.j2"
            content = template_file.read_text()
            assert "VAS1MerchantID" not in content
            assert "{% for passinfo in passes %}" in content
            assert "KBLogMode=1" in content


class TestExportDialogTargets:
    """Tests for export target selection."""

    @pytest.mark.asyncio
    async def test_file_export_writes_file(self, tmp_path) -> None:
        """File target should write to output file."""
        from textual.widgets import Button
        from vtap100.tui.app import VTAPEditorApp
        from vtap100.tui.screens.export_dialog import ExportDialog

        output_file = tmp_path / "config.txt"
        app = VTAPEditorApp(output_path=output_file)

        async with app.run_test() as pilot:
            await pilot.pause()
            await pilot.press("ctrl+e")
            await pilot.pause()

            # Export (file is default target)
            assert isinstance(app.screen, ExportDialog)
            export_btn = app.screen.query_one("#export-btn", Button)
            export_btn.press()
            await pilot.pause()

            # File should exist
            assert output_file.exists()
            content = output_file.read_text()
            assert "!VTAPconfig" in content

    @pytest.mark.asyncio
    async def test_clipboard_export_copies_to_clipboard(self) -> None:
        """Clipboard target should copy content to clipboard."""
        from textual.widgets import Button, RadioButton
        from vtap100.tui.app import VTAPEditorApp
        from vtap100.tui.screens.export_dialog import ExportDialog

        app = VTAPEditorApp()

        async with app.run_test() as pilot:
            await pilot.pause()
            await pilot.press("ctrl+e")
            await pilot.pause()

            # Select clipboard target
            assert isinstance(app.screen, ExportDialog)
            clipboard_radio = app.screen.query_one("#target-clipboard", RadioButton)
            clipboard_radio.toggle()
            await pilot.pause()

            # Mock pyperclip and export
            with patch("pyperclip.copy") as mock_copy:
                export_btn = app.screen.query_one("#export-btn", Button)
                export_btn.press()
                await pilot.pause()

                # Clipboard should have been called
                mock_copy.assert_called_once()
                # Check content starts with header
                call_args = mock_copy.call_args[0][0]
                assert "!VTAPconfig" in call_args

    @pytest.mark.asyncio
    async def test_export_without_output_path_shows_error(self) -> None:
        """Export to file without output path should show error."""
        from textual.widgets import Button
        from vtap100.tui.app import VTAPEditorApp
        from vtap100.tui.screens.export_dialog import ExportDialog

        # No output path set
        app = VTAPEditorApp()

        async with app.run_test() as pilot:
            await pilot.pause()
            await pilot.press("ctrl+e")
            await pilot.pause()

            # Export (file is default, but no path)
            assert isinstance(app.screen, ExportDialog)
            export_btn = app.screen.query_one("#export-btn", Button)
            export_btn.press()
            await pilot.pause()

            # Should not crash - error notification shown


class TestExportDialogCombinations:
    """Tests for combined format + target options."""

    @pytest.mark.asyncio
    async def test_template_to_clipboard(self) -> None:
        """Template format to clipboard should work correctly."""
        from textual.widgets import Button, RadioButton
        from vtap100.models.vas import AppleVASConfig
        from vtap100.tui.app import VTAPEditorApp
        from vtap100.tui.screens.export_dialog import ExportDialog

        app = VTAPEditorApp()

        async with app.run_test() as pilot:
            await pilot.pause()

            # Add VAS config (should be excluded in template)
            app.config.vas_configs.append(
                AppleVASConfig(merchant_id="pass.com.test", key_slot=1)
            )

            await pilot.press("ctrl+e")
            await pilot.pause()

            assert isinstance(app.screen, ExportDialog)

            # Select template format
            template_radio = app.screen.query_one("#format-template", RadioButton)
            template_radio.toggle()
            await pilot.pause()

            # Select clipboard target
            clipboard_radio = app.screen.query_one("#target-clipboard", RadioButton)
            clipboard_radio.toggle()
            await pilot.pause()

            # Export with mocked clipboard
            with patch("pyperclip.copy") as mock_copy:
                export_btn = app.screen.query_one("#export-btn", Button)
                export_btn.press()
                await pilot.pause()

                # Check clipboard content is template (no VAS, has Jinja)
                call_args = mock_copy.call_args[0][0]
                assert "VAS1MerchantID" not in call_args
                assert "{% for passinfo in passes %}" in call_args
