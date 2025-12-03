"""Unit tests for TUI quit confirmation dialog.

Tests for:
- Dirty flag tracking (has_unsaved_changes)
- Quit confirmation dialog display
- Quit with/without unsaved changes
- Dialog button handling (Yes/No)
"""

import pytest


class TestDirtyFlagTracking:
    """Test dirty flag (has_unsaved_changes) tracking."""

    def test_app_starts_without_unsaved_changes(self) -> None:
        """App should start with has_unsaved_changes = False."""
        from vtap100.tui.app import VTAPEditorApp

        app = VTAPEditorApp()
        assert hasattr(app, "has_unsaved_changes")
        assert app.has_unsaved_changes is False

    def test_app_loaded_from_file_has_no_unsaved_changes(self, tmp_path) -> None:
        """App loaded from file should have has_unsaved_changes = False."""
        from vtap100.tui.app import VTAPEditorApp

        config_file = tmp_path / "config.txt"
        config_file.write_text("!VTAPconfig\nVASMerchantID=pass.test\n")

        app = VTAPEditorApp(input_path=config_file)
        assert app.has_unsaved_changes is False


class TestDirtyFlagAsync:
    """Async tests for dirty flag tracking with actual form changes."""

    @pytest.mark.asyncio
    async def test_dirty_flag_set_on_config_change(self) -> None:
        """Dirty flag should be set when a config value changes."""
        from vtap100.tui.app import VTAPEditorApp
        from vtap100.tui.widgets.forms.base import ConfigChanged

        app = VTAPEditorApp()
        async with app.run_test() as pilot:
            await pilot.pause()

            # Initially no unsaved changes
            assert app.has_unsaved_changes is False

            # Simulate a ConfigChanged message
            app.screen.post_message(
                ConfigChanged(section_id="vas", field_name="merchant_id", value="test")
            )
            await pilot.pause()

            # Now should have unsaved changes
            assert app.has_unsaved_changes is True

    @pytest.mark.asyncio
    async def test_dirty_flag_set_on_config_added(self) -> None:
        """Dirty flag should be set when a config is added."""
        from vtap100.tui.app import VTAPEditorApp
        from vtap100.tui.widgets.forms.base import ConfigAdded

        app = VTAPEditorApp()
        async with app.run_test() as pilot:
            await pilot.pause()

            assert app.has_unsaved_changes is False

            # Simulate adding a new config
            app.screen.post_message(ConfigAdded(section_id="vas", index=0))
            await pilot.pause()

            assert app.has_unsaved_changes is True

    @pytest.mark.asyncio
    async def test_dirty_flag_set_on_config_removed(self) -> None:
        """Dirty flag should be set when a config is removed."""
        from vtap100.tui.app import VTAPEditorApp
        from vtap100.tui.widgets.forms.base import ConfigRemoved

        app = VTAPEditorApp()
        async with app.run_test() as pilot:
            await pilot.pause()

            assert app.has_unsaved_changes is False

            # Simulate removing a config (the message itself triggers the flag,
            # regardless of whether there's actually something to remove)
            app.screen.post_message(ConfigRemoved(section_id="vas", index=0))
            await pilot.pause()

            assert app.has_unsaved_changes is True

    @pytest.mark.asyncio
    async def test_dirty_flag_cleared_on_save(self, tmp_path) -> None:
        """Dirty flag should be cleared after successful save."""
        from vtap100.tui.app import VTAPEditorApp
        from vtap100.tui.widgets.forms.base import ConfigChanged

        output_file = tmp_path / "config.txt"
        app = VTAPEditorApp(output_path=output_file)
        async with app.run_test() as pilot:
            await pilot.pause()

            # Make a change
            app.screen.post_message(
                ConfigChanged(section_id="vas", field_name="merchant_id", value="test")
            )
            await pilot.pause()
            assert app.has_unsaved_changes is True

            # Save
            await pilot.press("ctrl+s")
            await pilot.pause()

            # Dirty flag should be cleared
            assert app.has_unsaved_changes is False


class TestQuitConfirmDialog:
    """Test quit confirmation dialog behavior."""

    @pytest.mark.asyncio
    async def test_quit_without_changes_exits_immediately(self) -> None:
        """Ctrl+Q without unsaved changes should quit immediately."""
        from vtap100.tui.app import VTAPEditorApp

        app = VTAPEditorApp()
        async with app.run_test() as pilot:
            await pilot.pause()

            # No changes made, quit should work immediately
            assert app.has_unsaved_changes is False
            await pilot.press("ctrl+q")

            # App should have exited
            assert not app.is_running

    @pytest.mark.asyncio
    async def test_quit_with_changes_shows_dialog(self) -> None:
        """Ctrl+Q with unsaved changes should show confirmation dialog."""
        from vtap100.tui.app import VTAPEditorApp
        from vtap100.tui.screens.quit_confirm_dialog import QuitConfirmDialog
        from vtap100.tui.widgets.forms.base import ConfigChanged

        app = VTAPEditorApp()
        async with app.run_test() as pilot:
            await pilot.pause()

            # Make a change to set dirty flag
            app.screen.post_message(
                ConfigChanged(section_id="vas", field_name="merchant_id", value="test")
            )
            await pilot.pause()
            assert app.has_unsaved_changes is True

            # Try to quit
            await pilot.press("ctrl+q")
            await pilot.pause()

            # App should still be running (dialog shown)
            assert app.is_running

            # Dialog should be the current screen (modal screens get pushed)
            assert isinstance(app.screen, QuitConfirmDialog)

    @pytest.mark.asyncio
    async def test_quit_dialog_cancel_returns_to_editor(self) -> None:
        """Clicking Cancel in quit dialog should return to editor."""
        from vtap100.tui.app import VTAPEditorApp
        from vtap100.tui.screens.editor import EditorScreen
        from vtap100.tui.screens.quit_confirm_dialog import QuitConfirmDialog
        from vtap100.tui.widgets.forms.base import ConfigChanged

        app = VTAPEditorApp()
        async with app.run_test() as pilot:
            await pilot.pause()

            # Make a change
            app.screen.post_message(
                ConfigChanged(section_id="vas", field_name="merchant_id", value="test")
            )
            await pilot.pause()

            # Try to quit
            await pilot.press("ctrl+q")
            await pilot.pause()

            # Verify dialog is shown
            assert isinstance(app.screen, QuitConfirmDialog)

            # Press Escape to cancel
            await pilot.press("escape")
            await pilot.pause()

            # App should still be running
            assert app.is_running

            # Should be back to EditorScreen (dialog dismissed)
            assert isinstance(app.screen, EditorScreen)

    @pytest.mark.asyncio
    async def test_quit_dialog_confirm_exits_app(self) -> None:
        """Clicking Quit in quit dialog should exit the app."""
        from vtap100.tui.app import VTAPEditorApp
        from vtap100.tui.widgets.forms.base import ConfigChanged

        app = VTAPEditorApp()
        async with app.run_test() as pilot:
            await pilot.pause()

            # Make a change
            app.screen.post_message(
                ConfigChanged(section_id="vas", field_name="merchant_id", value="test")
            )
            await pilot.pause()

            # Try to quit
            await pilot.press("ctrl+q")
            await pilot.pause()

            # Click the quit button
            await pilot.click("#quit-btn")

            # App should have exited
            assert not app.is_running


class TestQuitConfirmDialogUI:
    """Test quit confirmation dialog UI elements."""

    @pytest.mark.asyncio
    async def test_dialog_has_cancel_and_quit_buttons(self) -> None:
        """Dialog should have Cancel and Quit buttons."""
        from textual.widgets import Button
        from vtap100.tui.app import VTAPEditorApp
        from vtap100.tui.screens.quit_confirm_dialog import QuitConfirmDialog
        from vtap100.tui.widgets.forms.base import ConfigChanged

        app = VTAPEditorApp()
        async with app.run_test() as pilot:
            await pilot.pause()

            # Make a change
            app.screen.post_message(
                ConfigChanged(section_id="vas", field_name="merchant_id", value="test")
            )
            await pilot.pause()

            # Show dialog
            await pilot.press("ctrl+q")
            await pilot.pause()

            # Verify dialog is the current screen
            assert isinstance(app.screen, QuitConfirmDialog)

            # Check buttons exist on the dialog screen
            cancel_btn = app.screen.query_one("#cancel-btn", Button)
            quit_btn = app.screen.query_one("#quit-btn", Button)
            assert cancel_btn is not None
            assert quit_btn is not None

    @pytest.mark.asyncio
    async def test_dialog_has_warning_message(self) -> None:
        """Dialog should display a warning message about unsaved changes."""
        from textual.widgets import Label
        from vtap100.tui.app import VTAPEditorApp
        from vtap100.tui.screens.quit_confirm_dialog import QuitConfirmDialog
        from vtap100.tui.widgets.forms.base import ConfigChanged

        app = VTAPEditorApp()
        async with app.run_test() as pilot:
            await pilot.pause()

            # Make a change
            app.screen.post_message(
                ConfigChanged(section_id="vas", field_name="merchant_id", value="test")
            )
            await pilot.pause()

            # Show dialog
            await pilot.press("ctrl+q")
            await pilot.pause()

            # Dialog should be the current screen
            assert isinstance(app.screen, QuitConfirmDialog)

            # Check that message label exists
            labels = app.screen.query(Label)
            assert len(labels) >= 2  # Title and message
