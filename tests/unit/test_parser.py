"""Unit tests for config.txt parser.

TDD: Tests for parsing config.txt back into VTAPConfig.
"""

import pytest


class TestConfigParserImports:
    """Test that parser module can be imported."""

    def test_import_config_parser(self) -> None:
        """ConfigParser should be importable."""
        from vtap100.parser import ConfigParser

        assert ConfigParser is not None

    def test_import_parse_function(self) -> None:
        """parse function should be importable."""
        from vtap100.parser import parse

        assert callable(parse)


class TestConfigParserHeader:
    """Test header validation."""

    def test_parse_valid_header(self) -> None:
        """Valid config should start with !VTAPconfig."""
        from vtap100.parser import parse

        content = "!VTAPconfig\n"
        config = parse(content)
        assert config is not None

    def test_parse_missing_header_raises(self) -> None:
        """Missing header should raise ValueError."""
        from vtap100.parser import parse

        content = "VAS1MerchantID=pass.com.test\n"
        with pytest.raises(ValueError, match="header"):
            parse(content)

    def test_parse_empty_config(self) -> None:
        """Empty config (just header) should be valid."""
        from vtap100.parser import parse

        content = "!VTAPconfig"
        config = parse(content)
        assert config.vas_configs == []
        assert config.smarttap_configs == []


class TestConfigParserVAS:
    """Test VAS configuration parsing."""

    def test_parse_single_vas(self) -> None:
        """Parse single VAS config."""
        from vtap100.parser import parse

        content = """!VTAPconfig
VAS1MerchantID=pass.com.example.test
VAS1KeySlot=1
"""
        config = parse(content)
        assert len(config.vas_configs) == 1
        assert config.vas_configs[0].merchant_id == "pass.com.example.test"
        assert config.vas_configs[0].key_slot == 1

    def test_parse_vas_with_url(self) -> None:
        """Parse VAS config with optional merchant URL."""
        from vtap100.parser import parse

        content = """!VTAPconfig
VAS1MerchantID=pass.com.example.test
VAS1KeySlot=1
VAS1MerchantURL=https://example.com
"""
        config = parse(content)
        assert config.vas_configs[0].merchant_url == "https://example.com"

    def test_parse_multiple_vas(self) -> None:
        """Parse multiple VAS configs."""
        from vtap100.parser import parse

        content = """!VTAPconfig
VAS1MerchantID=pass.com.example.one
VAS1KeySlot=1
VAS2MerchantID=pass.com.example.two
VAS2KeySlot=2
"""
        config = parse(content)
        assert len(config.vas_configs) == 2
        assert config.vas_configs[0].merchant_id == "pass.com.example.one"
        assert config.vas_configs[1].merchant_id == "pass.com.example.two"


class TestConfigParserSmartTap:
    """Test Smart Tap configuration parsing."""

    def test_parse_single_smarttap(self) -> None:
        """Parse single Smart Tap config."""
        from vtap100.parser import parse

        content = """!VTAPconfig
ST1CollectorID=96972794
ST1KeySlot=2
ST1KeyVersion=1
"""
        config = parse(content)
        assert len(config.smarttap_configs) == 1
        assert config.smarttap_configs[0].collector_id == "96972794"
        assert config.smarttap_configs[0].key_slot == 2
        assert config.smarttap_configs[0].key_version == 1

    def test_parse_multiple_smarttap(self) -> None:
        """Parse multiple Smart Tap configs."""
        from vtap100.parser import parse

        content = """!VTAPconfig
ST1CollectorID=12345678
ST1KeySlot=1
ST2CollectorID=87654321
ST2KeySlot=2
"""
        config = parse(content)
        assert len(config.smarttap_configs) == 2


class TestConfigParserKeyboard:
    """Test keyboard configuration parsing."""

    def test_parse_keyboard_basic(self) -> None:
        """Parse basic keyboard config."""
        from vtap100.parser import parse

        content = """!VTAPconfig
KBLogMode=1
KBSource=A1
"""
        config = parse(content)
        assert config.keyboard is not None
        assert config.keyboard.log_mode is True
        assert config.keyboard.source == "A1"

    def test_parse_keyboard_log_mode_zero(self) -> None:
        """Parse keyboard with log_mode=0."""
        from vtap100.parser import parse

        content = """!VTAPconfig
KBLogMode=0
KBSource=AG
"""
        config = parse(content)
        assert config.keyboard.log_mode is False


class TestConfigParserComments:
    """Test comment handling."""

    def test_parse_ignores_comments(self) -> None:
        """Comments should be ignored."""
        from vtap100.parser import parse

        content = """!VTAPconfig
; This is a comment
VAS1MerchantID=pass.com.test
; Another comment
VAS1KeySlot=1
"""
        config = parse(content)
        assert len(config.vas_configs) == 1

    def test_parse_ignores_section_comments(self) -> None:
        """Section comments should be ignored."""
        from vtap100.parser import parse

        content = """!VTAPconfig
; Apple VAS Configuration
VAS1MerchantID=pass.com.test
VAS1KeySlot=1
; Google Smart Tap Configuration
ST1CollectorID=12345678
ST1KeySlot=2
"""
        config = parse(content)
        assert len(config.vas_configs) == 1
        assert len(config.smarttap_configs) == 1


class TestConfigParserCombined:
    """Test combined configuration parsing."""

    def test_parse_combined_config(self) -> None:
        """Parse config with VAS, Smart Tap, and Keyboard."""
        from vtap100.parser import parse

        content = """!VTAPconfig
; Apple VAS Configuration
VAS1MerchantID=pass.com.example.test
VAS1KeySlot=1
; Google Smart Tap Configuration
ST1CollectorID=96972794
ST1KeySlot=2
ST1KeyVersion=1
; Keyboard Emulation
KBLogMode=1
KBSource=AG
"""
        config = parse(content)
        assert len(config.vas_configs) == 1
        assert len(config.smarttap_configs) == 1
        assert config.keyboard is not None


class TestConfigParserRoundTrip:
    """Test generate -> parse roundtrip."""

    def test_roundtrip_vas(self) -> None:
        """Generate and parse VAS config."""
        from vtap100.generator import ConfigGenerator
        from vtap100.models.config import VTAPConfig
        from vtap100.models.vas import AppleVASConfig
        from vtap100.parser import parse

        original = VTAPConfig(
            vas_configs=[
                AppleVASConfig(merchant_id="pass.com.example.test", key_slot=1)
            ]
        )
        generator = ConfigGenerator(original)
        content = generator.generate()
        parsed = parse(content)

        assert len(parsed.vas_configs) == 1
        assert parsed.vas_configs[0].merchant_id == original.vas_configs[0].merchant_id
        assert parsed.vas_configs[0].key_slot == original.vas_configs[0].key_slot

    def test_roundtrip_combined(self) -> None:
        """Generate and parse combined config."""
        from vtap100.generator import ConfigGenerator
        from vtap100.models.config import VTAPConfig
        from vtap100.models.keyboard import KeyboardConfig
        from vtap100.models.smarttap import GoogleSmartTapConfig
        from vtap100.models.vas import AppleVASConfig
        from vtap100.parser import parse

        original = VTAPConfig(
            vas_configs=[
                AppleVASConfig(merchant_id="pass.com.example.test", key_slot=1)
            ],
            smarttap_configs=[
                GoogleSmartTapConfig(collector_id="96972794", key_slot=2, key_version=1)
            ],
            keyboard=KeyboardConfig(log_mode=True, source="AG"),
        )
        generator = ConfigGenerator(original)
        content = generator.generate()
        parsed = parse(content)

        assert len(parsed.vas_configs) == 1
        assert len(parsed.smarttap_configs) == 1
        assert parsed.keyboard is not None
        assert parsed.keyboard.log_mode is True
