"""Unit tests for unsaved changes dialog.

TDD Red Phase: These tests define the expected behavior of the
UnsavedChangesDialog.
"""

from enum import Enum
import pytest


class TestUnsavedChangesResult:
    """Tests for UnsavedChangesResult enum."""

    def test_result_has_save_option(self) -> None:
        """UnsavedChangesResult should have SAVE option."""
        from vtap100.tui.screens.unsaved_changes_dialog import UnsavedChangesResult

        assert hasattr(UnsavedChangesResult, "SAVE")

    def test_result_has_discard_option(self) -> None:
        """UnsavedChangesResult should have DISCARD option."""
        from vtap100.tui.screens.unsaved_changes_dialog import UnsavedChangesResult

        assert hasattr(UnsavedChangesResult, "DISCARD")

    def test_result_has_cancel_option(self) -> None:
        """UnsavedChangesResult should have CANCEL option."""
        from vtap100.tui.screens.unsaved_changes_dialog import UnsavedChangesResult

        assert hasattr(UnsavedChangesResult, "CANCEL")

    def test_result_is_enum(self) -> None:
        """UnsavedChangesResult should be an Enum."""
        from vtap100.tui.screens.unsaved_changes_dialog import UnsavedChangesResult

        assert issubclass(UnsavedChangesResult, Enum)


class TestUnsavedChangesDialogCreation:
    """Tests for UnsavedChangesDialog creation."""

    def test_dialog_can_be_instantiated(self) -> None:
        """UnsavedChangesDialog should be instantiable."""
        from vtap100.tui.screens.unsaved_changes_dialog import UnsavedChangesDialog

        dialog = UnsavedChangesDialog()
        assert dialog is not None

    def test_dialog_is_modal_screen(self) -> None:
        """UnsavedChangesDialog should be a ModalScreen."""
        from textual.screen import ModalScreen
        from vtap100.tui.screens.unsaved_changes_dialog import UnsavedChangesDialog

        dialog = UnsavedChangesDialog()
        assert isinstance(dialog, ModalScreen)


class TestUnsavedChangesDialogUI:
    """Tests for UnsavedChangesDialog UI elements."""

    @pytest.mark.asyncio
    async def test_dialog_has_title(self) -> None:
        """Dialog should have a title."""
        from textual.app import App
        from textual.widgets import Label
        from vtap100.tui.screens.unsaved_changes_dialog import UnsavedChangesDialog
        from vtap100.tui.screens.unsaved_changes_dialog import UnsavedChangesResult

        class TestApp(App[UnsavedChangesResult]):
            def on_mount(self) -> None:
                self.push_screen(UnsavedChangesDialog())

        async with TestApp().run_test() as pilot:
            await pilot.pause()
            # Verify dialog is the current screen
            assert isinstance(pilot.app.screen, UnsavedChangesDialog)
            # Should have a title label (query dialog screen directly)
            labels = pilot.app.screen.query(Label)
            titles = [lbl for lbl in labels if "dialog-title" in lbl.classes]
            assert len(titles) >= 1

    @pytest.mark.asyncio
    async def test_dialog_has_three_buttons(self) -> None:
        """Dialog should have three buttons: Save, Discard, Cancel."""
        from textual.app import App
        from textual.widgets import Button
        from vtap100.tui.screens.unsaved_changes_dialog import UnsavedChangesDialog
        from vtap100.tui.screens.unsaved_changes_dialog import UnsavedChangesResult

        class TestApp(App[UnsavedChangesResult]):
            def on_mount(self) -> None:
                self.push_screen(UnsavedChangesDialog())

        async with TestApp().run_test() as pilot:
            await pilot.pause()
            assert isinstance(pilot.app.screen, UnsavedChangesDialog)
            buttons = pilot.app.screen.query(Button)
            assert len(buttons) == 3

    @pytest.mark.asyncio
    async def test_dialog_has_save_button(self) -> None:
        """Dialog should have a Save button."""
        from textual.app import App
        from textual.widgets import Button
        from vtap100.tui.screens.unsaved_changes_dialog import UnsavedChangesDialog
        from vtap100.tui.screens.unsaved_changes_dialog import UnsavedChangesResult

        class TestApp(App[UnsavedChangesResult]):
            def on_mount(self) -> None:
                self.push_screen(UnsavedChangesDialog())

        async with TestApp().run_test() as pilot:
            await pilot.pause()
            assert isinstance(pilot.app.screen, UnsavedChangesDialog)
            save_btn = pilot.app.screen.query_one("#save-btn", Button)
            assert save_btn is not None

    @pytest.mark.asyncio
    async def test_dialog_has_discard_button(self) -> None:
        """Dialog should have a Discard button."""
        from textual.app import App
        from textual.widgets import Button
        from vtap100.tui.screens.unsaved_changes_dialog import UnsavedChangesDialog
        from vtap100.tui.screens.unsaved_changes_dialog import UnsavedChangesResult

        class TestApp(App[UnsavedChangesResult]):
            def on_mount(self) -> None:
                self.push_screen(UnsavedChangesDialog())

        async with TestApp().run_test() as pilot:
            await pilot.pause()
            assert isinstance(pilot.app.screen, UnsavedChangesDialog)
            discard_btn = pilot.app.screen.query_one("#discard-btn", Button)
            assert discard_btn is not None

    @pytest.mark.asyncio
    async def test_dialog_has_cancel_button(self) -> None:
        """Dialog should have a Cancel button."""
        from textual.app import App
        from textual.widgets import Button
        from vtap100.tui.screens.unsaved_changes_dialog import UnsavedChangesDialog
        from vtap100.tui.screens.unsaved_changes_dialog import UnsavedChangesResult

        class TestApp(App[UnsavedChangesResult]):
            def on_mount(self) -> None:
                self.push_screen(UnsavedChangesDialog())

        async with TestApp().run_test() as pilot:
            await pilot.pause()
            assert isinstance(pilot.app.screen, UnsavedChangesDialog)
            cancel_btn = pilot.app.screen.query_one("#cancel-btn", Button)
            assert cancel_btn is not None


class TestUnsavedChangesDialogActions:
    """Tests for UnsavedChangesDialog button actions."""

    @pytest.mark.asyncio
    async def test_clicking_save_returns_save_result(self) -> None:
        """Clicking Save button should return SAVE result."""
        from textual.app import App
        from vtap100.tui.screens.unsaved_changes_dialog import UnsavedChangesDialog
        from vtap100.tui.screens.unsaved_changes_dialog import UnsavedChangesResult

        result_holder: list[UnsavedChangesResult | None] = [None]

        class TestApp(App[None]):
            def on_mount(self) -> None:
                def callback(result: UnsavedChangesResult | None) -> None:
                    result_holder[0] = result

                self.push_screen(UnsavedChangesDialog(), callback)

        async with TestApp().run_test() as pilot:
            await pilot.pause()
            assert isinstance(pilot.app.screen, UnsavedChangesDialog)
            await pilot.click("#save-btn")
            await pilot.pause()
            assert result_holder[0] == UnsavedChangesResult.SAVE

    @pytest.mark.asyncio
    async def test_clicking_discard_returns_discard_result(self) -> None:
        """Clicking Discard button should return DISCARD result."""
        from textual.app import App
        from vtap100.tui.screens.unsaved_changes_dialog import UnsavedChangesDialog
        from vtap100.tui.screens.unsaved_changes_dialog import UnsavedChangesResult

        result_holder: list[UnsavedChangesResult | None] = [None]

        class TestApp(App[None]):
            def on_mount(self) -> None:
                def callback(result: UnsavedChangesResult | None) -> None:
                    result_holder[0] = result

                self.push_screen(UnsavedChangesDialog(), callback)

        async with TestApp().run_test() as pilot:
            await pilot.pause()
            assert isinstance(pilot.app.screen, UnsavedChangesDialog)
            await pilot.click("#discard-btn")
            await pilot.pause()
            assert result_holder[0] == UnsavedChangesResult.DISCARD

    @pytest.mark.asyncio
    async def test_clicking_cancel_returns_cancel_result(self) -> None:
        """Clicking Cancel button should return CANCEL result."""
        from textual.app import App
        from vtap100.tui.screens.unsaved_changes_dialog import UnsavedChangesDialog
        from vtap100.tui.screens.unsaved_changes_dialog import UnsavedChangesResult

        result_holder: list[UnsavedChangesResult | None] = [None]

        class TestApp(App[None]):
            def on_mount(self) -> None:
                def callback(result: UnsavedChangesResult | None) -> None:
                    result_holder[0] = result

                self.push_screen(UnsavedChangesDialog(), callback)

        async with TestApp().run_test() as pilot:
            await pilot.pause()
            assert isinstance(pilot.app.screen, UnsavedChangesDialog)
            await pilot.click("#cancel-btn")
            await pilot.pause()
            assert result_holder[0] == UnsavedChangesResult.CANCEL

    @pytest.mark.asyncio
    async def test_pressing_escape_returns_cancel_result(self) -> None:
        """Pressing Escape should return CANCEL result."""
        from textual.app import App
        from vtap100.tui.screens.unsaved_changes_dialog import UnsavedChangesDialog
        from vtap100.tui.screens.unsaved_changes_dialog import UnsavedChangesResult

        result_holder: list[UnsavedChangesResult | None] = [None]

        class TestApp(App[None]):
            def on_mount(self) -> None:
                def callback(result: UnsavedChangesResult | None) -> None:
                    result_holder[0] = result

                self.push_screen(UnsavedChangesDialog(), callback)

        async with TestApp().run_test() as pilot:
            await pilot.pause()
            await pilot.press("escape")
            await pilot.pause()
            assert result_holder[0] == UnsavedChangesResult.CANCEL
