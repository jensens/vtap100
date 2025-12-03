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

    def test_wizard_skipping_all_sections(self) -> None:
        """Wizard should work when all sections are skipped."""
        runner = CliRunner()
        # Answer 'n' to all config questions, then provide output filename
        inputs = "\n".join(
            [
                "n",  # Apple VAS
                "n",  # Google Smart Tap
                "n",  # NFC Tags
                "n",  # MIFARE DESFire
                "n",  # Keyboard Emulation
                "n",  # LED/Beep Feedback
                "wizard_output.txt",  # Output file
                "n",  # Don't save
            ]
        )
        result = runner.invoke(main, ["wizard"], input=inputs)
        assert result.exit_code == 0
        assert "VTAPconfig" in result.output or "Wizard" in result.output

    def test_wizard_with_apple_vas(self) -> None:
        """Wizard should configure Apple VAS."""
        runner = CliRunner()
        with runner.isolated_filesystem():
            inputs = "\n".join(
                [
                    "y",  # Apple VAS
                    "pass.com.example.test",  # Merchant ID
                    "1",  # Key slot
                    "n",  # Google Smart Tap
                    "n",  # NFC Tags
                    "n",  # MIFARE DESFire
                    "y",  # Keyboard Emulation
                    "A1",  # KBSource
                    "n",  # Extended keyboard options
                    "n",  # LED/Beep Feedback
                    "wizard_vas.txt",  # Output file
                    "y",  # Save
                ]
            )
            result = runner.invoke(main, ["wizard"], input=inputs)
            assert result.exit_code == 0
            assert Path("wizard_vas.txt").exists()
            content = Path("wizard_vas.txt").read_text()
            assert "VAS1MerchantID=pass.com.example.test" in content

    def test_wizard_with_google_smarttap(self) -> None:
        """Wizard should configure Google Smart Tap."""
        runner = CliRunner()
        with runner.isolated_filesystem():
            inputs = "\n".join(
                [
                    "n",  # Apple VAS
                    "y",  # Google Smart Tap
                    "96972794",  # Collector ID
                    "2",  # Key slot
                    "1",  # Key version
                    "n",  # NFC Tags
                    "n",  # MIFARE DESFire
                    "y",  # Keyboard Emulation
                    "G1",  # KBSource
                    "n",  # Extended keyboard options
                    "n",  # LED/Beep Feedback
                    "wizard_st.txt",  # Output file
                    "y",  # Save
                ]
            )
            result = runner.invoke(main, ["wizard"], input=inputs)
            assert result.exit_code == 0
            assert Path("wizard_st.txt").exists()
            content = Path("wizard_st.txt").read_text()
            assert "ST1CollectorID=96972794" in content

    def test_wizard_with_nfc_tags(self) -> None:
        """Wizard should configure NFC tags."""
        runner = CliRunner()
        with runner.isolated_filesystem():
            inputs = "\n".join(
                [
                    "n",  # Apple VAS
                    "n",  # Google Smart Tap
                    "y",  # NFC Tags
                    "U",  # Type 2 mode (UID)
                    "N",  # Type 4 mode (NDEF)
                    "0",  # Type 5 mode (disabled)
                    "n",  # Ignore random UID
                    "n",  # MIFARE DESFire
                    "y",  # Keyboard Emulation
                    "241",  # KBSource
                    "n",  # Extended keyboard options
                    "n",  # LED/Beep Feedback
                    "wizard_nfc.txt",  # Output file
                    "y",  # Save
                ]
            )
            result = runner.invoke(main, ["wizard"], input=inputs)
            assert result.exit_code == 0
            assert Path("wizard_nfc.txt").exists()
            content = Path("wizard_nfc.txt").read_text()
            assert "NFCType2=U" in content
            assert "NFCType4=N" in content

    def test_wizard_with_nfc_ignore_random_uid(self) -> None:
        """Wizard should configure NFC with ignore random UID."""
        runner = CliRunner()
        with runner.isolated_filesystem():
            inputs = "\n".join(
                [
                    "n",  # Apple VAS
                    "n",  # Google Smart Tap
                    "y",  # NFC Tags
                    "U",  # Type 2 mode
                    "0",  # Type 4 mode
                    "0",  # Type 5 mode
                    "y",  # Ignore random UID
                    "n",  # MIFARE DESFire
                    "n",  # Keyboard Emulation
                    "n",  # LED/Beep Feedback
                    "wizard_nfc_rand.txt",  # Output file
                    "y",  # Save
                ]
            )
            result = runner.invoke(main, ["wizard"], input=inputs)
            assert result.exit_code == 0
            assert Path("wizard_nfc_rand.txt").exists()
            content = Path("wizard_nfc_rand.txt").read_text()
            assert "IgnoreRandomUID=1" in content

    def test_wizard_with_desfire(self) -> None:
        """Wizard should configure MIFARE DESFire."""
        runner = CliRunner()
        with runner.isolated_filesystem():
            inputs = "\n".join(
                [
                    "n",  # Apple VAS
                    "n",  # Google Smart Tap
                    "n",  # NFC Tags
                    "y",  # MIFARE DESFire
                    "AABBCC",  # App ID
                    "1",  # File ID
                    "1",  # Key slot
                    "3",  # Crypto (AES)
                    "n",  # Add another app
                    "n",  # Keyboard Emulation
                    "n",  # LED/Beep Feedback
                    "wizard_desfire.txt",  # Output file
                    "y",  # Save
                ]
            )
            result = runner.invoke(main, ["wizard"], input=inputs)
            assert result.exit_code == 0
            assert Path("wizard_desfire.txt").exists()
            content = Path("wizard_desfire.txt").read_text()
            assert "DESFire1AppID=AABBCC" in content

    def test_wizard_with_keyboard_extended(self) -> None:
        """Wizard should configure extended keyboard options."""
        runner = CliRunner()
        with runner.isolated_filesystem():
            inputs = "\n".join(
                [
                    "n",  # Apple VAS
                    "n",  # Google Smart Tap
                    "n",  # NFC Tags
                    "n",  # MIFARE DESFire
                    "y",  # Keyboard Emulation
                    "A1",  # KBSource
                    "y",  # Extended keyboard options
                    "PREFIX_",  # Prefix
                    "%0D",  # Postfix
                    "10",  # Delay
                    "n",  # LED/Beep Feedback
                    "wizard_kb.txt",  # Output file
                    "y",  # Save
                ]
            )
            result = runner.invoke(main, ["wizard"], input=inputs)
            assert result.exit_code == 0
            assert Path("wizard_kb.txt").exists()
            content = Path("wizard_kb.txt").read_text()
            assert "KBPrefix=PREFIX_" in content
            assert "KBPostfix=%0D" in content

    def test_wizard_with_led_feedback(self) -> None:
        """Wizard should configure LED feedback."""
        runner = CliRunner()
        with runner.isolated_filesystem():
            inputs = "\n".join(
                [
                    "n",  # Apple VAS
                    "n",  # Google Smart Tap
                    "n",  # NFC Tags
                    "n",  # MIFARE DESFire
                    "n",  # Keyboard Emulation
                    "y",  # LED/Beep Feedback
                    "y",  # LED configuration
                    "3",  # LED mode (Custom)
                    "y",  # LED for successful scan
                    "00FF00",  # Color
                    "2",  # Repeats
                    "y",  # LED for error
                    "FF0000",  # Color
                    "3",  # Repeats
                    "n",  # Beep configuration
                    "wizard_led.txt",  # Output file
                    "y",  # Save
                ]
            )
            result = runner.invoke(main, ["wizard"], input=inputs)
            assert result.exit_code == 0
            assert Path("wizard_led.txt").exists()
            content = Path("wizard_led.txt").read_text()
            assert "LEDMode=3" in content
            assert "PassLED=" in content

    def test_wizard_with_beep_feedback(self) -> None:
        """Wizard should configure beep feedback."""
        runner = CliRunner()
        with runner.isolated_filesystem():
            inputs = "\n".join(
                [
                    "n",  # Apple VAS
                    "n",  # Google Smart Tap
                    "n",  # NFC Tags
                    "n",  # MIFARE DESFire
                    "n",  # Keyboard Emulation
                    "y",  # LED/Beep Feedback
                    "n",  # LED configuration
                    "y",  # Beep configuration
                    "y",  # Beep for successful scan
                    "2",  # Repeats
                    "y",  # Beep for error
                    "3",  # Repeats
                    "200",  # On time
                    "wizard_beep.txt",  # Output file
                    "y",  # Save
                ]
            )
            result = runner.invoke(main, ["wizard"], input=inputs)
            assert result.exit_code == 0
            assert Path("wizard_beep.txt").exists()
            content = Path("wizard_beep.txt").read_text()
            assert "PassBeep=" in content

    def test_wizard_invalid_apple_vas(self) -> None:
        """Wizard should handle invalid Apple VAS merchant ID."""
        runner = CliRunner()
        inputs = "\n".join(
            [
                "y",  # Apple VAS
                "invalid",  # Invalid Merchant ID (missing pass. prefix)
                "1",  # Key slot
                "n",  # Google Smart Tap
                "n",  # NFC Tags
                "n",  # MIFARE DESFire
                "n",  # Keyboard Emulation
                "n",  # LED/Beep Feedback
                "wizard_invalid.txt",  # Output file
                "n",  # Don't save
            ]
        )
        result = runner.invoke(main, ["wizard"], input=inputs)
        assert "Ungültige Konfiguration" in result.output

    def test_wizard_invalid_desfire_app_id(self) -> None:
        """Wizard should handle invalid DESFire App ID."""
        runner = CliRunner()
        inputs = "\n".join(
            [
                "n",  # Apple VAS
                "n",  # Google Smart Tap
                "n",  # NFC Tags
                "y",  # MIFARE DESFire
                "INVALID123",  # Invalid App ID (too long, not 6 hex chars)
                "1",  # File ID
                "1",  # Key slot
                "0",  # Crypto
                "n",  # Add another app
                "n",  # Keyboard Emulation
                "n",  # LED/Beep Feedback
                "wizard_invalid_df.txt",  # Output file
                "n",  # Don't save
            ]
        )
        result = runner.invoke(main, ["wizard"], input=inputs)
        assert "Ungültige Konfiguration" in result.output

    def test_wizard_with_multiple_desfire_apps(self) -> None:
        """Wizard should allow adding multiple DESFire apps."""
        runner = CliRunner()
        with runner.isolated_filesystem():
            inputs = "\n".join(
                [
                    "n",  # Apple VAS
                    "n",  # Google Smart Tap
                    "n",  # NFC Tags
                    "y",  # MIFARE DESFire
                    "AABBCC",  # App 1 ID
                    "1",  # File ID
                    "1",  # Key slot
                    "1",  # Crypto (3DES)
                    "y",  # Add another app
                    "DDEEFF",  # App 2 ID
                    "2",  # File ID
                    "0",  # Key slot (none)
                    "0",  # Crypto (none)
                    "n",  # Add another app
                    "n",  # Keyboard Emulation
                    "n",  # LED/Beep Feedback
                    "wizard_multi_df.txt",  # Output file
                    "y",  # Save
                ]
            )
            result = runner.invoke(main, ["wizard"], input=inputs)
            assert result.exit_code == 0
            assert Path("wizard_multi_df.txt").exists()
            content = Path("wizard_multi_df.txt").read_text()
            assert "DESFire1AppID=AABBCC" in content
            assert "DESFire2AppID=DDEEFF" in content

    def test_wizard_with_led_mode_non_custom(self) -> None:
        """Wizard should handle LED modes other than custom."""
        runner = CliRunner()
        with runner.isolated_filesystem():
            inputs = "\n".join(
                [
                    "n",  # Apple VAS
                    "n",  # Google Smart Tap
                    "n",  # NFC Tags
                    "n",  # MIFARE DESFire
                    "n",  # Keyboard Emulation
                    "y",  # LED/Beep Feedback
                    "y",  # LED configuration
                    "2",  # LED mode (Status)
                    "n",  # Beep configuration
                    "wizard_led_status.txt",  # Output file
                    "y",  # Save
                ]
            )
            result = runner.invoke(main, ["wizard"], input=inputs)
            assert result.exit_code == 0
            assert Path("wizard_led_status.txt").exists()
            content = Path("wizard_led_status.txt").read_text()
            assert "LEDMode=2" in content


class TestEditorCommandExecution:
    """Test actual execution of editor command."""

    def test_editor_calls_tui_run(self) -> None:
        """Editor command should call the TUI run function."""
        runner = CliRunner()
        with patch("vtap100.tui.run") as mock_run:
            result = runner.invoke(main, ["editor"])
            mock_run.assert_called_once_with(input_path=None, output_path=None)
            assert result.exit_code == 0

    def test_editor_with_input_file(self) -> None:
        """Editor command should pass input file to TUI."""
        runner = CliRunner()
        with runner.isolated_filesystem():
            Path("config.txt").write_text("!VTAPconfig\n")
            with patch("vtap100.tui.run") as mock_run:
                runner.invoke(main, ["editor", "config.txt"])
                mock_run.assert_called_once()
                call_args = mock_run.call_args
                assert call_args[1]["input_path"] == Path("config.txt")

    def test_editor_with_output_option(self) -> None:
        """Editor command should pass output option to TUI."""
        runner = CliRunner()
        with patch("vtap100.tui.run") as mock_run:
            runner.invoke(main, ["editor", "-o", "output.txt"])
            mock_run.assert_called_once()
            call_args = mock_run.call_args
            assert call_args[1]["output_path"] == Path("output.txt")

    def test_editor_with_both_input_and_output(self) -> None:
        """Editor command should pass both input and output to TUI."""
        runner = CliRunner()
        with runner.isolated_filesystem():
            Path("input.txt").write_text("!VTAPconfig\n")
            with patch("vtap100.tui.run") as mock_run:
                runner.invoke(main, ["editor", "input.txt", "-o", "output.txt"])
                mock_run.assert_called_once()
                call_args = mock_run.call_args
                assert call_args[1]["input_path"] == Path("input.txt")
                assert call_args[1]["output_path"] == Path("output.txt")
