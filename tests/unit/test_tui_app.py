"""Unit tests for TUI Editor - Phase 1: Foundation.

Tests for:
- VTAPEditorApp creation and initialization
- 3-Panel layout (Sidebar, Main Content, Help Panel)
- Basic keyboard bindings
- Editor screen mounting
"""

import pytest
from vtap100.models.config import VTAPConfig


class TestTUIModuleImports:
    """Test that TUI module can be imported and has expected exports."""

    def test_import_run_function(self) -> None:
        """Run function should be importable from tui module."""
        from vtap100.tui import run

        assert callable(run)

    def test_import_app_class(self) -> None:
        """VTAPEditorApp should be importable from tui.app."""
        from vtap100.tui.app import VTAPEditorApp

        assert VTAPEditorApp is not None

    def test_import_editor_screen(self) -> None:
        """EditorScreen should be importable from tui.screens."""
        from vtap100.tui.screens.editor import EditorScreen

        assert EditorScreen is not None


class TestVTAPEditorApp:
    """Test VTAPEditorApp class."""

    def test_app_creation_without_file(self) -> None:
        """App should be creatable without a filename."""
        from vtap100.tui.app import VTAPEditorApp

        app = VTAPEditorApp()
        assert app.input_path is None
        assert app.output_path is None

    def test_app_creation_with_file(self, tmp_path) -> None:
        """App should accept input and output paths."""
        from vtap100.tui.app import VTAPEditorApp

        input_file = tmp_path / "config.txt"
        input_file.write_text("!VTAPconfig\n")

        app = VTAPEditorApp(input_path=input_file, output_path=input_file)
        assert app.input_path == input_file
        assert app.output_path == input_file

    def test_app_has_config_reactive(self) -> None:
        """App should have a reactive config attribute."""
        from vtap100.tui.app import VTAPEditorApp

        app = VTAPEditorApp()
        assert hasattr(app, "config")
        assert isinstance(app.config, VTAPConfig)

    def test_app_has_bindings(self) -> None:
        """App should have expected key bindings."""
        from vtap100.tui.app import VTAPEditorApp

        app = VTAPEditorApp()
        # Get all binding keys from the BINDINGS class variable
        binding_keys = [b[0] for b in app.BINDINGS]
        assert "ctrl+d" in binding_keys  # Toggle help (Doku)
        assert "ctrl+o" in binding_keys  # Toggle preview (Output)
        assert "ctrl+l" in binding_keys  # Toggle language
        assert "ctrl+s" in binding_keys  # Save
        assert "ctrl+q" in binding_keys  # Quit


class TestVTAPEditorAppAsync:
    """Async tests using Textual's Pilot."""

    @pytest.mark.asyncio
    async def test_app_mounts_editor_screen(self) -> None:
        """App should mount EditorScreen on startup."""
        from vtap100.tui.app import VTAPEditorApp

        app = VTAPEditorApp()
        async with app.run_test():
            # Check that EditorScreen is mounted
            from vtap100.tui.screens.editor import EditorScreen

            assert isinstance(app.screen, EditorScreen)

    @pytest.mark.asyncio
    async def test_editor_screen_has_three_panels(self) -> None:
        """EditorScreen should have Sidebar, MainContent, and HelpPanel."""
        from vtap100.tui.app import VTAPEditorApp

        app = VTAPEditorApp()
        async with app.run_test() as pilot:
            # Wait for screen to be mounted
            await pilot.pause()

            # Check for the three main containers
            sidebar = app.screen.query_one("#sidebar")
            main_content = app.screen.query_one("#main-content")
            help_panel = app.screen.query_one("#help-panel")

            assert sidebar is not None
            assert main_content is not None
            assert help_panel is not None

    @pytest.mark.asyncio
    async def test_toggle_help_with_ctrl_d(self) -> None:
        """Ctrl+D should toggle the help panel visibility."""
        from vtap100.tui.app import VTAPEditorApp

        app = VTAPEditorApp()
        async with app.run_test() as pilot:
            await pilot.pause()
            help_panel = app.screen.query_one("#help-panel")
            initial_display = help_panel.display

            # Press Ctrl+D to toggle
            await pilot.press("ctrl+d")
            assert help_panel.display != initial_display

            # Press Ctrl+D again to toggle back
            await pilot.press("ctrl+d")
            assert help_panel.display == initial_display

    @pytest.mark.asyncio
    async def test_toggle_preview_with_ctrl_o(self) -> None:
        """Ctrl+O should cycle preview through 3 states."""
        from vtap100.tui.app import PreviewMode
        from vtap100.tui.app import VTAPEditorApp

        app = VTAPEditorApp()
        async with app.run_test() as pilot:
            await pilot.pause()

            # Initial state is DEFAULT
            assert app.preview_mode == PreviewMode.DEFAULT

            # Press Ctrl+O to go to MAXIMIZED
            await pilot.press("ctrl+o")
            assert app.preview_mode == PreviewMode.MAXIMIZED

            # Press Ctrl+O to go to HIDDEN
            await pilot.press("ctrl+o")
            assert app.preview_mode == PreviewMode.HIDDEN

            # Press Ctrl+O to cycle back to DEFAULT
            await pilot.press("ctrl+o")
            assert app.preview_mode == PreviewMode.DEFAULT

    @pytest.mark.asyncio
    async def test_quit_with_ctrl_q(self) -> None:
        """Ctrl+Q should quit the application."""
        from vtap100.tui.app import VTAPEditorApp

        app = VTAPEditorApp()
        async with app.run_test() as pilot:
            await pilot.press("ctrl+q")
            # App should have exited - pilot will raise if app is still running
            assert not app.is_running


class TestEditorScreen:
    """Test EditorScreen layout and structure."""

    def test_editor_screen_creation(self) -> None:
        """EditorScreen should be instantiable."""
        from vtap100.tui.screens.editor import EditorScreen

        screen = EditorScreen()
        assert screen is not None

    @pytest.mark.asyncio
    async def test_editor_screen_layout_structure(self) -> None:
        """EditorScreen should have correct layout structure."""
        from vtap100.tui.app import VTAPEditorApp

        app = VTAPEditorApp()
        async with app.run_test() as pilot:
            await pilot.pause()

            # Main container should exist
            main = app.screen.query_one("#editor-main")
            assert main is not None

            # Should have horizontal container with 3 panels
            top_row = app.screen.query_one("#top-row")
            assert top_row is not None

            # Should have preview at bottom (initially hidden or shown)
            preview = app.screen.query_one("#preview-panel")
            assert preview is not None
