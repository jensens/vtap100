"""Unit tests for TUI run function.

Tests for the vtap100.tui run function.
"""

from pathlib import Path
import tempfile
from unittest.mock import MagicMock
from unittest.mock import patch


class TestTUIRunFunction:
    """Test the TUI run function."""

    def test_run_function_exists(self) -> None:
        """Run function should be importable."""
        from vtap100.tui import run

        assert callable(run)

    def test_run_creates_app_with_no_args(self) -> None:
        """Run should create app with no arguments."""
        from vtap100.tui import VTAPEditorApp

        with patch.object(VTAPEditorApp, "run", return_value=None):
            from vtap100.tui import run

            run()
            # The app.run() should have been called
            VTAPEditorApp.run.assert_called_once()

    def test_run_creates_app_with_input_path(self) -> None:
        """Run should pass input_path to app."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "config.txt"
            config_path.write_text("!VTAPconfig\n")

            # Mock the VTAPEditorApp to verify it's called correctly
            mock_app = MagicMock()
            with patch("vtap100.tui.VTAPEditorApp", return_value=mock_app) as mock_class:
                from vtap100 import tui

                # Reimport to get fresh reference
                tui.run(input_path=config_path)

                mock_class.assert_called_once_with(input_path=config_path, output_path=None)
                mock_app.run.assert_called_once()

    def test_run_creates_app_with_output_path(self) -> None:
        """Run should pass output_path to app."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "output.txt"

            mock_app = MagicMock()
            with patch("vtap100.tui.VTAPEditorApp", return_value=mock_app) as mock_class:
                from vtap100 import tui

                tui.run(output_path=output_path)

                mock_class.assert_called_once_with(input_path=None, output_path=output_path)
                mock_app.run.assert_called_once()

    def test_run_creates_app_with_both_paths(self) -> None:
        """Run should pass both paths to app."""
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = Path(tmpdir) / "input.txt"
            input_path.write_text("!VTAPconfig\n")
            output_path = Path(tmpdir) / "output.txt"

            mock_app = MagicMock()
            with patch("vtap100.tui.VTAPEditorApp", return_value=mock_app) as mock_class:
                from vtap100 import tui

                tui.run(input_path=input_path, output_path=output_path)

                mock_class.assert_called_once_with(input_path=input_path, output_path=output_path)
                mock_app.run.assert_called_once()

    def test_module_all_exports(self) -> None:
        """Module should export run and VTAPEditorApp."""
        from vtap100 import tui

        assert "run" in tui.__all__
        assert "VTAPEditorApp" in tui.__all__
