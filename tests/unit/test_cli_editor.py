"""Unit tests for CLI editor command."""

from click.testing import CliRunner
from vtap100.cli import main


class TestCLIEditorCommand:
    """Test the vtap100 editor CLI command."""

    def test_editor_command_exists(self) -> None:
        """The editor command should be registered."""
        runner = CliRunner()
        result = runner.invoke(main, ["editor", "--help"])
        assert result.exit_code == 0
        assert "Open the interactive TUI editor" in result.output

    def test_editor_command_help_shows_examples(self) -> None:
        """The editor command help should show usage examples."""
        runner = CliRunner()
        result = runner.invoke(main, ["editor", "--help"])
        assert "vtap100 editor" in result.output
        assert "--output" in result.output or "-o" in result.output
