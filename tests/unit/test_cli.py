"""Unit tests for CLI commands.

Tests for the vtap100 command-line interface including:
- generate command
- validate command
- docs command
- Helper functions
"""

from click.testing import CliRunner
from io import StringIO
from pathlib import Path
from rich.console import Console
import tempfile
from unittest.mock import patch
from vtap100.cli import main
from vtap100.cli import print_config_preview
from vtap100.cli import print_error
from vtap100.cli import print_header
from vtap100.cli import print_section
from vtap100.cli import print_success


class TestHelperFunctions:
    """Tests for CLI helper functions."""

    def test_print_header_outputs_version(self) -> None:
        """print_header should output version info."""
        output = StringIO()
        console = Console(file=output, force_terminal=True)
        with patch("vtap100.cli.console", console):
            print_header()
        result = output.getvalue()
        assert "VTAP100" in result

    def test_print_success_outputs_checkmark(self) -> None:
        """print_success should output a success message with checkmark."""
        output = StringIO()
        console = Console(file=output, force_terminal=True)
        with patch("vtap100.cli.console", console):
            print_success("Test message")
        result = output.getvalue()
        assert "Test message" in result

    def test_print_error_outputs_message(self) -> None:
        """print_error should output an error message."""
        output = StringIO()
        console = Console(file=output, force_terminal=True)
        with patch("vtap100.cli.console", console):
            print_error("Error message")
        result = output.getvalue()
        assert "Error message" in result

    def test_print_section_outputs_title(self) -> None:
        """print_section should output a section title."""
        output = StringIO()
        console = Console(file=output, force_terminal=True)
        with patch("vtap100.cli.console", console):
            print_section("Test Section")
        result = output.getvalue()
        assert "Test Section" in result

    def test_print_config_preview_outputs_config(self) -> None:
        """print_config_preview should output syntax-highlighted config."""
        output = StringIO()
        console = Console(file=output, force_terminal=True)
        with patch("vtap100.cli.console", console):
            print_config_preview("!VTAPconfig\nTestKey=TestValue")
        result = output.getvalue()
        assert "VTAPconfig" in result


class TestMainCommand:
    """Tests for the main CLI group."""

    def test_main_shows_help(self) -> None:
        """Main command should show help."""
        runner = CliRunner()
        result = runner.invoke(main, ["--help"])
        assert result.exit_code == 0
        assert "VTAP100 Configuration Generator" in result.output

    def test_main_shows_version(self) -> None:
        """Main command should show version."""
        runner = CliRunner()
        result = runner.invoke(main, ["--version"])
        assert result.exit_code == 0
        assert "vtap100" in result.output

    def test_main_lists_commands(self) -> None:
        """Main command should list available commands."""
        runner = CliRunner()
        result = runner.invoke(main, ["--help"])
        assert "generate" in result.output
        assert "validate" in result.output
        assert "docs" in result.output
        assert "editor" in result.output
        assert "wizard" in result.output


class TestGenerateCommand:
    """Tests for the generate command."""

    def test_generate_help(self) -> None:
        """Generate command should show help."""
        runner = CliRunner()
        result = runner.invoke(main, ["generate", "--help"])
        assert result.exit_code == 0
        assert "--apple-vas" in result.output
        assert "--google-st" in result.output

    def test_generate_requires_vas_or_st(self) -> None:
        """Generate should fail without VAS or Smart Tap."""
        runner = CliRunner()
        result = runner.invoke(main, ["generate"])
        assert result.exit_code == 1
        assert "Please provide at least --apple-vas or --google-st" in result.output

    def test_generate_with_apple_vas(self) -> None:
        """Generate should work with Apple VAS."""
        runner = CliRunner()
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = Path(tmpdir) / "config.txt"
            result = runner.invoke(
                main,
                [
                    "generate",
                    "--apple-vas",
                    "pass.com.example.test",
                    "--key-slot",
                    "1",
                    "--output",
                    str(output_file),
                ],
            )
            assert result.exit_code == 0
            assert output_file.exists()
            content = output_file.read_text()
            assert "!VTAPconfig" in content
            assert "VAS1MerchantID=pass.com.example.test" in content

    def test_generate_with_google_st(self) -> None:
        """Generate should work with Google Smart Tap."""
        runner = CliRunner()
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = Path(tmpdir) / "config.txt"
            result = runner.invoke(
                main,
                [
                    "generate",
                    "--google-st",
                    "96972794",
                    "--key-slot",
                    "2",
                    "--key-version",
                    "1",
                    "--output",
                    str(output_file),
                ],
            )
            assert result.exit_code == 0
            assert output_file.exists()
            content = output_file.read_text()
            assert "!VTAPconfig" in content
            assert "ST1CollectorID=96972794" in content

    def test_generate_with_both_vas_and_st(self) -> None:
        """Generate should work with both VAS and Smart Tap."""
        runner = CliRunner()
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = Path(tmpdir) / "config.txt"
            result = runner.invoke(
                main,
                [
                    "generate",
                    "--apple-vas",
                    "pass.com.example.test",
                    "--google-st",
                    "96972794",
                    "--key-slot",
                    "1",
                    "--output",
                    str(output_file),
                ],
            )
            assert result.exit_code == 0
            content = output_file.read_text()
            assert "VAS1MerchantID" in content
            assert "ST1CollectorID" in content

    def test_generate_with_keyboard_disabled(self) -> None:
        """Generate should work with keyboard disabled."""
        runner = CliRunner()
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = Path(tmpdir) / "config.txt"
            result = runner.invoke(
                main,
                [
                    "generate",
                    "--apple-vas",
                    "pass.com.example.test",
                    "--no-keyboard",
                    "--output",
                    str(output_file),
                ],
            )
            assert result.exit_code == 0
            content = output_file.read_text()
            assert "KBLogMode" not in content

    def test_generate_with_comment(self) -> None:
        """Generate should include custom comment."""
        runner = CliRunner()
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = Path(tmpdir) / "config.txt"
            result = runner.invoke(
                main,
                [
                    "generate",
                    "--apple-vas",
                    "pass.com.example.test",
                    "--comment",
                    "My custom comment",
                    "--output",
                    str(output_file),
                ],
            )
            assert result.exit_code == 0
            content = output_file.read_text()
            assert "My custom comment" in content

    def test_generate_invalid_apple_vas(self) -> None:
        """Generate should fail with invalid Apple VAS merchant ID."""
        runner = CliRunner()
        result = runner.invoke(
            main,
            [
                "generate",
                "--apple-vas",
                "invalid-merchant-id",  # Missing pass. prefix
            ],
        )
        assert result.exit_code == 1
        assert "Invalid Apple VAS configuration" in result.output

    def test_generate_invalid_google_st(self) -> None:
        """Generate should fail with invalid Google Smart Tap collector ID."""
        runner = CliRunner()
        result = runner.invoke(
            main,
            [
                "generate",
                "--google-st",
                "",  # Empty collector ID
            ],
        )
        assert result.exit_code == 1

    def test_generate_default_output_file(self) -> None:
        """Generate should use config.txt as default output."""
        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(
                main,
                [
                    "generate",
                    "--apple-vas",
                    "pass.com.example.test",
                ],
            )
            assert result.exit_code == 0
            assert Path("config.txt").exists()

    def test_generate_keyboard_source_from_vas(self) -> None:
        """Generate should set keyboard source based on VAS config."""
        runner = CliRunner()
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = Path(tmpdir) / "config.txt"
            result = runner.invoke(
                main,
                [
                    "generate",
                    "--apple-vas",
                    "pass.com.example.test",
                    "--output",
                    str(output_file),
                ],
            )
            assert result.exit_code == 0
            content = output_file.read_text()
            assert "KBSource=A1" in content

    def test_generate_keyboard_source_from_st(self) -> None:
        """Generate should set keyboard source based on ST config."""
        runner = CliRunner()
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = Path(tmpdir) / "config.txt"
            result = runner.invoke(
                main,
                [
                    "generate",
                    "--google-st",
                    "96972794",
                    "--output",
                    str(output_file),
                ],
            )
            assert result.exit_code == 0
            content = output_file.read_text()
            assert "KBSource=G1" in content

    def test_generate_keyboard_source_from_both(self) -> None:
        """Generate should set keyboard source from both VAS and ST."""
        runner = CliRunner()
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = Path(tmpdir) / "config.txt"
            result = runner.invoke(
                main,
                [
                    "generate",
                    "--apple-vas",
                    "pass.com.example.test",
                    "--google-st",
                    "96972794",
                    "--output",
                    str(output_file),
                ],
            )
            assert result.exit_code == 0
            content = output_file.read_text()
            assert "KBSource=AG1" in content


class TestValidateCommand:
    """Tests for the validate command."""

    def test_validate_help(self) -> None:
        """Validate command should show help."""
        runner = CliRunner()
        result = runner.invoke(main, ["validate", "--help"])
        assert result.exit_code == 0
        assert "Validate an existing config.txt file" in result.output

    def test_validate_valid_config(self) -> None:
        """Validate should accept a valid config file."""
        runner = CliRunner()
        with tempfile.TemporaryDirectory() as tmpdir:
            config_file = Path(tmpdir) / "config.txt"
            config_file.write_text(
                "!VTAPconfig\n; Comment\nVAS1MerchantID=pass.com.example.test\nVAS1KeySlot=1\n"
            )
            result = runner.invoke(main, ["validate", str(config_file)])
            assert result.exit_code == 0
            assert "No errors found" in result.output

    def test_validate_missing_vtapconfig_header(self) -> None:
        """Validate should detect missing !VTAPconfig header."""
        runner = CliRunner()
        with tempfile.TemporaryDirectory() as tmpdir:
            config_file = Path(tmpdir) / "config.txt"
            config_file.write_text("VAS1MerchantID=pass.com.example.test\n")
            result = runner.invoke(main, ["validate", str(config_file)])
            assert result.exit_code == 0
            assert "must start with '!VTAPconfig'" in result.output

    def test_validate_invalid_line_format(self) -> None:
        """Validate should detect invalid line format."""
        runner = CliRunner()
        with tempfile.TemporaryDirectory() as tmpdir:
            config_file = Path(tmpdir) / "config.txt"
            config_file.write_text("!VTAPconfig\nInvalidLineWithoutEquals\n")
            result = runner.invoke(main, ["validate", str(config_file)])
            assert result.exit_code == 0
            assert "Invalid format" in result.output
            assert "missing '='" in result.output

    def test_validate_nonexistent_file(self) -> None:
        """Validate should fail with nonexistent file."""
        runner = CliRunner()
        result = runner.invoke(main, ["validate", "/nonexistent/file.txt"])
        assert result.exit_code != 0

    def test_validate_empty_lines_and_comments(self) -> None:
        """Validate should skip empty lines and comments."""
        runner = CliRunner()
        with tempfile.TemporaryDirectory() as tmpdir:
            config_file = Path(tmpdir) / "config.txt"
            config_file.write_text(
                "!VTAPconfig\n\n; This is a comment\n  \nVAS1MerchantID=pass.com.example.test\n"
            )
            result = runner.invoke(main, ["validate", str(config_file)])
            assert result.exit_code == 0
            assert "No errors found" in result.output


class TestDocsCommand:
    """Tests for the docs command."""

    def test_docs_help(self) -> None:
        """Docs command should show help."""
        runner = CliRunner()
        result = runner.invoke(main, ["docs", "--help"])
        assert result.exit_code == 0

    def test_docs_shows_vas_parameters(self) -> None:
        """Docs should show Apple VAS parameters."""
        runner = CliRunner()
        result = runner.invoke(main, ["docs"])
        assert result.exit_code == 0
        assert "Apple VAS" in result.output
        assert "MerchantID" in result.output

    def test_docs_shows_smarttap_parameters(self) -> None:
        """Docs should show Google Smart Tap parameters."""
        runner = CliRunner()
        result = runner.invoke(main, ["docs"])
        assert result.exit_code == 0
        assert "Smart Tap" in result.output
        assert "CollectorID" in result.output

    def test_docs_shows_nfc_parameters(self) -> None:
        """Docs should show NFC Tag parameters."""
        runner = CliRunner()
        result = runner.invoke(main, ["docs"])
        assert result.exit_code == 0
        assert "NFC Tag" in result.output
        assert "NFCType2" in result.output

    def test_docs_shows_desfire_parameters(self) -> None:
        """Docs should show MIFARE DESFire parameters."""
        runner = CliRunner()
        result = runner.invoke(main, ["docs"])
        assert result.exit_code == 0
        assert "DESFire" in result.output
        assert "AppID" in result.output

    def test_docs_shows_keyboard_parameters(self) -> None:
        """Docs should show Keyboard Emulation parameters."""
        runner = CliRunner()
        result = runner.invoke(main, ["docs"])
        assert result.exit_code == 0
        assert "Keyboard" in result.output
        assert "KBLogMode" in result.output

    def test_docs_shows_led_parameters(self) -> None:
        """Docs should show LED parameters."""
        runner = CliRunner()
        result = runner.invoke(main, ["docs"])
        assert result.exit_code == 0
        assert "LED" in result.output
        assert "LEDMode" in result.output

    def test_docs_shows_beep_parameters(self) -> None:
        """Docs should show Beep parameters."""
        runner = CliRunner()
        result = runner.invoke(main, ["docs"])
        assert result.exit_code == 0
        assert "Beep" in result.output
        assert "PassBeep" in result.output


class TestEditorCommand:
    """Tests for the editor command."""

    def test_editor_help(self) -> None:
        """Editor command should show help."""
        runner = CliRunner()
        result = runner.invoke(main, ["editor", "--help"])
        assert result.exit_code == 0
        assert "TUI-Editor" in result.output

    def test_editor_accepts_filename(self) -> None:
        """Editor command should accept filename argument."""
        runner = CliRunner()
        result = runner.invoke(main, ["editor", "--help"])
        assert "FILENAME" in result.output or "filename" in result.output.lower()

    def test_editor_accepts_output_option(self) -> None:
        """Editor command should accept output option."""
        runner = CliRunner()
        result = runner.invoke(main, ["editor", "--help"])
        assert "--output" in result.output or "-o" in result.output


class TestWizardCommand:
    """Tests for the wizard command."""

    def test_wizard_help(self) -> None:
        """Wizard command should show help."""
        runner = CliRunner()
        result = runner.invoke(main, ["wizard", "--help"])
        assert result.exit_code == 0
        assert "Interactive wizard" in result.output
