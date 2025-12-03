"""Unit tests for Keyboard Emulation configuration model.

TDD Red Phase: These tests define the expected behavior of the KeyboardConfig model.
Tests should fail until the implementation is complete.

Phase 1 focuses on basic keyboard emulation: KBLogMode, KBSource, KBEnable
"""

from pydantic import ValidationError
import pytest


class TestKeyboardConfig:
    """Tests for KeyboardConfig model."""

    def test_keyboard_config_defaults(self) -> None:
        """Keyboard config should have sensible defaults."""
        from vtap100.models.keyboard import KeyboardConfig

        config = KeyboardConfig()
        assert config.log_mode is False  # KBLogMode=0 by default
        assert config.enable is True  # KBEnable=1 by default
        assert config.source == "A5"  # Default source

    def test_keyboard_config_log_mode_enabled(self) -> None:
        """Can enable keyboard log mode."""
        from vtap100.models.keyboard import KeyboardConfig

        config = KeyboardConfig(log_mode=True)
        assert config.log_mode is True

    def test_keyboard_config_log_mode_disabled(self) -> None:
        """Can disable keyboard log mode."""
        from vtap100.models.keyboard import KeyboardConfig

        config = KeyboardConfig(log_mode=False)
        assert config.log_mode is False

    def test_keyboard_config_enable_flag(self) -> None:
        """Can set USB keyboard device enable flag."""
        from vtap100.models.keyboard import KeyboardConfig

        config = KeyboardConfig(enable=False)
        assert config.enable is False

        config = KeyboardConfig(enable=True)
        assert config.enable is True

    def test_keyboard_config_source_valid_hex(self) -> None:
        """Source can be a valid hex string."""
        from vtap100.models.keyboard import KeyboardConfig

        config = KeyboardConfig(source="A1")
        assert config.source == "A1"

        config = KeyboardConfig(source="FF")
        assert config.source == "FF"

    def test_keyboard_config_source_common_values(self) -> None:
        """Source accepts common preset values."""
        from vtap100.models.keyboard import KeyboardConfig

        # A1 = Apple VAS only (A=Apple, 1=enable)
        config = KeyboardConfig(source="A1")
        assert config.source == "A1"

        # G1 = Google Smart Tap only
        config = KeyboardConfig(source="G1")
        assert config.source == "G1"

        # A5 = Default (Apple + various)
        config = KeyboardConfig(source="A5")
        assert config.source == "A5"


class TestKeyboardConfigOutput:
    """Tests for KeyboardConfig config.txt output generation."""

    def test_to_config_lines_default(self) -> None:
        """Default config should generate minimal output."""
        from vtap100.models.keyboard import KeyboardConfig

        config = KeyboardConfig()
        lines = config.to_config_lines()

        # log_mode=False means KBLogMode=0, which is default - might not be in output
        # enable=True means KBEnable=1, which is default - might not be in output
        # source=A5 is default - might not be in output
        assert isinstance(lines, list)

    def test_to_config_lines_log_mode_enabled(self) -> None:
        """Enabled log mode should generate KBLogMode=1."""
        from vtap100.models.keyboard import KeyboardConfig

        config = KeyboardConfig(log_mode=True)
        lines = config.to_config_lines()

        assert "KBLogMode=1" in lines

    def test_to_config_lines_log_mode_disabled(self) -> None:
        """Disabled log mode should generate KBLogMode=0."""
        from vtap100.models.keyboard import KeyboardConfig

        config = KeyboardConfig(log_mode=False)
        lines = config.to_config_lines()

        assert "KBLogMode=0" in lines

    def test_to_config_lines_enable_disabled(self) -> None:
        """Disabled keyboard should generate KBEnable=0."""
        from vtap100.models.keyboard import KeyboardConfig

        config = KeyboardConfig(enable=False)
        lines = config.to_config_lines()

        assert "KBEnable=0" in lines

    def test_to_config_lines_source(self) -> None:
        """Custom source should be included."""
        from vtap100.models.keyboard import KeyboardConfig

        config = KeyboardConfig(source="A1", log_mode=True)
        lines = config.to_config_lines()

        assert "KBSource=A1" in lines

    def test_to_config_lines_full_config(self) -> None:
        """Full config should generate all relevant lines."""
        from vtap100.models.keyboard import KeyboardConfig

        config = KeyboardConfig(
            log_mode=True,
            enable=True,
            source="A1",
        )
        lines = config.to_config_lines()

        assert "KBLogMode=1" in lines
        assert "KBSource=A1" in lines
        # KBEnable=1 is default, might not be in output

    def test_to_config_lines_returns_list(self) -> None:
        """to_config_lines should return a list of strings."""
        from vtap100.models.keyboard import KeyboardConfig

        config = KeyboardConfig()
        lines = config.to_config_lines()

        assert isinstance(lines, list)
        assert all(isinstance(line, str) for line in lines)


class TestKBSourceHelper:
    """Tests for KBSource helper to build source values."""

    def test_kb_source_apple_only(self) -> None:
        """Can create source for Apple VAS only."""
        from vtap100.models.keyboard import KBSourceBuilder

        source = KBSourceBuilder().apple_vas().build()
        assert "A" in source

    def test_kb_source_google_only(self) -> None:
        """Can create source for Google Smart Tap only."""
        from vtap100.models.keyboard import KBSourceBuilder

        source = KBSourceBuilder().google_smarttap().build()
        assert "G" in source

    def test_kb_source_combined(self) -> None:
        """Can create source for both Apple and Google."""
        from vtap100.models.keyboard import KBSourceBuilder

        source = KBSourceBuilder().apple_vas().google_smarttap().build()
        assert "A" in source
        assert "G" in source

    def test_kb_source_with_nfc_type2(self) -> None:
        """Can add NFC Type 2 to source."""
        from vtap100.models.keyboard import KBSourceBuilder

        source = KBSourceBuilder().nfc_type2().build()
        assert "2" in source

    def test_kb_source_with_nfc_type4(self) -> None:
        """Can add NFC Type 4 to source."""
        from vtap100.models.keyboard import KBSourceBuilder

        source = KBSourceBuilder().nfc_type4().build()
        assert "4" in source

    def test_kb_source_empty_default(self) -> None:
        """Empty builder should return default or raise."""
        from vtap100.models.keyboard import KBSourceBuilder

        # Building empty source might return "0" or raise
        source = KBSourceBuilder().build()
        assert source is not None

    def test_kb_source_mifare(self) -> None:
        """Can add MIFARE to source."""
        from vtap100.models.keyboard import KBSourceBuilder

        source = KBSourceBuilder().mifare().build()
        assert "0" in source

    def test_kb_source_nfc_type5(self) -> None:
        """Can add NFC Type 5 to source."""
        from vtap100.models.keyboard import KBSourceBuilder

        source = KBSourceBuilder().nfc_type5().build()
        assert "6" in source

    def test_kb_source_card_emulation(self) -> None:
        """Can add card emulation to source."""
        from vtap100.models.keyboard import KBSourceBuilder

        source = KBSourceBuilder().card_emulation().build()
        assert "E" in source

    def test_kb_source_apple_wallet_iphone(self) -> None:
        """Can add Apple Wallet iPhone to source."""
        from vtap100.models.keyboard import KBSourceBuilder

        source = KBSourceBuilder().apple_wallet_iphone().build()
        assert "X" in source

    def test_kb_source_apple_wallet_watch(self) -> None:
        """Can add Apple Wallet Watch to source."""
        from vtap100.models.keyboard import KBSourceBuilder

        source = KBSourceBuilder().apple_wallet_watch().build()
        assert "W" in source

    def test_kb_source_all_types(self) -> None:
        """Can combine all source types."""
        from vtap100.models.keyboard import KBSourceBuilder

        source = (
            KBSourceBuilder()
            .apple_vas()
            .google_smarttap()
            .mifare()
            .nfc_type2()
            .nfc_type4()
            .nfc_type5()
            .card_emulation()
            .apple_wallet_iphone()
            .apple_wallet_watch()
            .build()
        )
        assert "A" in source
        assert "G" in source
        assert "0" in source
        assert "2" in source
        assert "4" in source
        assert "6" in source
        assert "E" in source
        assert "X" in source
        assert "W" in source

    def test_kb_source_no_duplicates(self) -> None:
        """Adding same source twice should not create duplicates."""
        from vtap100.models.keyboard import KBSourceBuilder

        source = KBSourceBuilder().apple_vas().apple_vas().apple_vas().build()
        assert source.count("A") == 1


class TestKeyboardConfigExtended:
    """Tests for extended keyboard configuration (Phase 2)."""

    def test_keyboard_prefix_default(self) -> None:
        """Prefix should be None by default."""
        from vtap100.models.keyboard import KeyboardConfig

        config = KeyboardConfig()
        assert config.prefix is None

    def test_keyboard_prefix_ascii_hex(self) -> None:
        """Can set prefix as ASCII hex string."""
        from vtap100.models.keyboard import KeyboardConfig

        # %0A is newline in ASCII hex
        config = KeyboardConfig(prefix="%0A")
        assert config.prefix == "%0A"

    def test_keyboard_prefix_variable(self) -> None:
        """Can set prefix with variable like $t (timestamp)."""
        from vtap100.models.keyboard import KeyboardConfig

        config = KeyboardConfig(prefix="$t")
        assert config.prefix == "$t"

    def test_keyboard_postfix_default(self) -> None:
        """Postfix should default to %0A (newline)."""
        from vtap100.models.keyboard import KeyboardConfig

        config = KeyboardConfig()
        assert config.postfix == "%0A"

    def test_keyboard_postfix_custom(self) -> None:
        """Can set custom postfix."""
        from vtap100.models.keyboard import KeyboardConfig

        config = KeyboardConfig(postfix="%0D%0A")  # CRLF
        assert config.postfix == "%0D%0A"

    def test_keyboard_delay_default(self) -> None:
        """Delay should default to 5ms."""
        from vtap100.models.keyboard import KeyboardConfig

        config = KeyboardConfig()
        assert config.delay_ms == 5

    def test_keyboard_delay_valid_range(self) -> None:
        """Delay must be between 5 and 255."""
        from vtap100.models.keyboard import KeyboardConfig

        config = KeyboardConfig(delay_ms=5)
        assert config.delay_ms == 5

        config = KeyboardConfig(delay_ms=255)
        assert config.delay_ms == 255

        config = KeyboardConfig(delay_ms=100)
        assert config.delay_ms == 100

    def test_keyboard_delay_below_min_fails(self) -> None:
        """Delay below 5 should fail validation."""
        from vtap100.models.keyboard import KeyboardConfig

        with pytest.raises(ValidationError):
            KeyboardConfig(delay_ms=4)

    def test_keyboard_delay_above_max_fails(self) -> None:
        """Delay above 255 should fail validation."""
        from vtap100.models.keyboard import KeyboardConfig

        with pytest.raises(ValidationError):
            KeyboardConfig(delay_ms=256)

    def test_keyboard_pass_mode_default(self) -> None:
        """Pass mode should be disabled by default."""
        from vtap100.models.keyboard import KeyboardConfig

        config = KeyboardConfig()
        assert config.pass_mode is False

    def test_keyboard_pass_mode_enabled(self) -> None:
        """Can enable pass mode for payload extraction."""
        from vtap100.models.keyboard import KeyboardConfig

        config = KeyboardConfig(pass_mode=True)
        assert config.pass_mode is True

    def test_keyboard_pass_section_default(self) -> None:
        """Pass section should default to 0."""
        from vtap100.models.keyboard import KeyboardConfig

        config = KeyboardConfig()
        assert config.pass_section == 0

    def test_keyboard_pass_section_custom(self) -> None:
        """Can set custom pass section."""
        from vtap100.models.keyboard import KeyboardConfig

        config = KeyboardConfig(pass_section=2)
        assert config.pass_section == 2

    def test_keyboard_pass_separator_default(self) -> None:
        """Pass separator should default to pipe character."""
        from vtap100.models.keyboard import KeyboardConfig

        config = KeyboardConfig()
        assert config.pass_separator == "|"

    def test_keyboard_pass_separator_custom(self) -> None:
        """Can set custom pass separator."""
        from vtap100.models.keyboard import KeyboardConfig

        config = KeyboardConfig(pass_separator=";")
        assert config.pass_separator == ";"

    def test_keyboard_pass_start_default(self) -> None:
        """Pass start position should default to 0."""
        from vtap100.models.keyboard import KeyboardConfig

        config = KeyboardConfig()
        assert config.pass_start == 0

    def test_keyboard_pass_start_custom(self) -> None:
        """Can set custom pass start position."""
        from vtap100.models.keyboard import KeyboardConfig

        config = KeyboardConfig(pass_start=10)
        assert config.pass_start == 10

    def test_keyboard_pass_length_default(self) -> None:
        """Pass length should default to 0 (all data)."""
        from vtap100.models.keyboard import KeyboardConfig

        config = KeyboardConfig()
        assert config.pass_length == 0

    def test_keyboard_pass_length_custom(self) -> None:
        """Can set custom pass length."""
        from vtap100.models.keyboard import KeyboardConfig

        config = KeyboardConfig(pass_length=16)
        assert config.pass_length == 16


class TestKeyboardConfigExtendedOutput:
    """Tests for extended keyboard config.txt output generation."""

    def test_to_config_lines_with_prefix(self) -> None:
        """Prefix should generate KBPrefix line."""
        from vtap100.models.keyboard import KeyboardConfig

        config = KeyboardConfig(log_mode=True, prefix="$t")
        lines = config.to_config_lines()

        assert "KBPrefix=$t" in lines

    def test_to_config_lines_with_postfix(self) -> None:
        """Non-default postfix should generate KBPostfix line."""
        from vtap100.models.keyboard import KeyboardConfig

        config = KeyboardConfig(log_mode=True, postfix="%0D%0A")
        lines = config.to_config_lines()

        assert "KBPostfix=%0D%0A" in lines

    def test_to_config_lines_default_postfix_not_included(self) -> None:
        """Default postfix (%0A) should not be in output."""
        from vtap100.models.keyboard import KeyboardConfig

        config = KeyboardConfig(log_mode=True)
        lines = config.to_config_lines()

        # Default %0A should not be explicitly in output
        assert not any("KBPostfix=%0A" in line for line in lines)

    def test_to_config_lines_with_delay(self) -> None:
        """Non-default delay should generate KBDelayMS line."""
        from vtap100.models.keyboard import KeyboardConfig

        config = KeyboardConfig(log_mode=True, delay_ms=50)
        lines = config.to_config_lines()

        assert "KBDelayMS=50" in lines

    def test_to_config_lines_default_delay_not_included(self) -> None:
        """Default delay (5ms) should not be in output."""
        from vtap100.models.keyboard import KeyboardConfig

        config = KeyboardConfig(log_mode=True, delay_ms=5)
        lines = config.to_config_lines()

        assert not any("KBDelayMS" in line for line in lines)

    def test_to_config_lines_with_pass_mode(self) -> None:
        """Enabled pass mode should generate KBPassMode=1."""
        from vtap100.models.keyboard import KeyboardConfig

        config = KeyboardConfig(log_mode=True, pass_mode=True)
        lines = config.to_config_lines()

        assert "KBPassMode=1" in lines

    def test_to_config_lines_pass_section(self) -> None:
        """Non-zero pass section should generate KBPassSection line."""
        from vtap100.models.keyboard import KeyboardConfig

        config = KeyboardConfig(log_mode=True, pass_mode=True, pass_section=2)
        lines = config.to_config_lines()

        assert "KBPassSection=2" in lines

    def test_to_config_lines_pass_separator(self) -> None:
        """Non-default pass separator should generate KBPassSeparator line."""
        from vtap100.models.keyboard import KeyboardConfig

        config = KeyboardConfig(log_mode=True, pass_mode=True, pass_separator=";")
        lines = config.to_config_lines()

        assert "KBPassSeparator=;" in lines

    def test_to_config_lines_pass_start(self) -> None:
        """Non-zero pass start should generate KBPassStart line."""
        from vtap100.models.keyboard import KeyboardConfig

        config = KeyboardConfig(log_mode=True, pass_mode=True, pass_start=5)
        lines = config.to_config_lines()

        assert "KBPassStart=5" in lines

    def test_to_config_lines_pass_length(self) -> None:
        """Non-zero pass length should generate KBPassLength line."""
        from vtap100.models.keyboard import KeyboardConfig

        config = KeyboardConfig(log_mode=True, pass_mode=True, pass_length=16)
        lines = config.to_config_lines()

        assert "KBPassLength=16" in lines

    def test_to_config_lines_full_extended_config(self) -> None:
        """Full extended config should generate all relevant lines."""
        from vtap100.models.keyboard import KeyboardConfig

        config = KeyboardConfig(
            log_mode=True,
            source="AG",
            prefix="$t:",
            postfix="%0D%0A",
            delay_ms=50,
            pass_mode=True,
            pass_section=1,
            pass_separator=";",
            pass_start=0,
            pass_length=32,
        )
        lines = config.to_config_lines()

        assert "KBLogMode=1" in lines
        assert "KBSource=AG" in lines
        assert "KBPrefix=$t:" in lines
        assert "KBPostfix=%0D%0A" in lines
        assert "KBDelayMS=50" in lines
        assert "KBPassMode=1" in lines
        assert "KBPassSection=1" in lines
        assert "KBPassSeparator=;" in lines
        assert "KBPassLength=32" in lines
