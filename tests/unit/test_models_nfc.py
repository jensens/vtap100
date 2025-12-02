"""Unit tests for NFC Tag configuration model.

TDD Red Phase: These tests define the expected behavior of the NFCTagConfig model.
Tests should fail until the implementation is complete.

Phase 3 focuses on NFC Tag settings: NFCType2/4/5, TagRead parameters.
"""

from pydantic import ValidationError
import pytest


class TestNFCTagMode:
    """Tests for NFCTagMode enum."""

    def test_nfc_mode_disabled(self) -> None:
        """Mode 0 means disabled."""
        from vtap100.models.nfc import NFCTagMode

        assert NFCTagMode.DISABLED.value == "0"

    def test_nfc_mode_uid(self) -> None:
        """Mode U means read UID."""
        from vtap100.models.nfc import NFCTagMode

        assert NFCTagMode.UID.value == "U"

    def test_nfc_mode_ndef(self) -> None:
        """Mode N means read NDEF records."""
        from vtap100.models.nfc import NFCTagMode

        assert NFCTagMode.NDEF.value == "N"

    def test_nfc_mode_block(self) -> None:
        """Mode B means read block data."""
        from vtap100.models.nfc import NFCTagMode

        assert NFCTagMode.BLOCK.value == "B"


class TestNFCTagConfig:
    """Tests for NFCTagConfig model."""

    def test_nfc_config_defaults(self) -> None:
        """NFC config should have sensible defaults (all disabled)."""
        from vtap100.models.nfc import NFCTagConfig

        config = NFCTagConfig()
        assert config.type2 is None  # Disabled by default
        assert config.type4 is None
        assert config.type5 is None
        assert config.report_read_error is False
        assert config.ignore_random_uid is False
        assert config.byte_order_reversed is False

    def test_nfc_type2_uid_mode(self) -> None:
        """Can enable Type 2 in UID mode."""
        from vtap100.models.nfc import NFCTagConfig
        from vtap100.models.nfc import NFCTagMode

        config = NFCTagConfig(type2=NFCTagMode.UID)
        assert config.type2 == NFCTagMode.UID

    def test_nfc_type2_ndef_mode(self) -> None:
        """Can enable Type 2 in NDEF mode."""
        from vtap100.models.nfc import NFCTagConfig
        from vtap100.models.nfc import NFCTagMode

        config = NFCTagConfig(type2=NFCTagMode.NDEF)
        assert config.type2 == NFCTagMode.NDEF

    def test_nfc_type4_uid_mode(self) -> None:
        """Can enable Type 4 in UID mode."""
        from vtap100.models.nfc import NFCTagConfig
        from vtap100.models.nfc import NFCTagMode

        config = NFCTagConfig(type4=NFCTagMode.UID)
        assert config.type4 == NFCTagMode.UID

    def test_nfc_type4_desfire_mode(self) -> None:
        """Type 4 supports DESFire mode."""
        from vtap100.models.nfc import NFCTagConfig
        from vtap100.models.nfc import NFCTagMode

        config = NFCTagConfig(type4=NFCTagMode.DESFIRE)
        assert config.type4 == NFCTagMode.DESFIRE

    def test_nfc_type5_block_mode(self) -> None:
        """Can enable Type 5 in block mode."""
        from vtap100.models.nfc import NFCTagConfig
        from vtap100.models.nfc import NFCTagMode

        config = NFCTagConfig(type5=NFCTagMode.BLOCK)
        assert config.type5 == NFCTagMode.BLOCK

    def test_nfc_report_read_error(self) -> None:
        """Can enable read error reporting."""
        from vtap100.models.nfc import NFCTagConfig

        config = NFCTagConfig(report_read_error=True)
        assert config.report_read_error is True

    def test_nfc_ignore_random_uid(self) -> None:
        """Can enable random UID filtering."""
        from vtap100.models.nfc import NFCTagConfig

        config = NFCTagConfig(ignore_random_uid=True)
        assert config.ignore_random_uid is True

    def test_nfc_byte_order_reversed(self) -> None:
        """Can reverse byte order."""
        from vtap100.models.nfc import NFCTagConfig

        config = NFCTagConfig(byte_order_reversed=True)
        assert config.byte_order_reversed is True


class TestTagReadConfig:
    """Tests for TagReadConfig model."""

    def test_tag_read_defaults(self) -> None:
        """Tag read config should have sensible defaults."""
        from vtap100.models.nfc import TagReadConfig

        config = TagReadConfig()
        assert config.block_num is None
        assert config.key_slot is None
        assert config.key_type is None
        assert config.offset == 0
        assert config.length is None
        assert config.format is None
        assert config.min_digits is None

    def test_tag_read_block_num(self) -> None:
        """Can set block number to read (0-255)."""
        from vtap100.models.nfc import TagReadConfig

        config = TagReadConfig(block_num=10)
        assert config.block_num == 10

    def test_tag_read_block_num_max(self) -> None:
        """Block number can be up to 255."""
        from vtap100.models.nfc import TagReadConfig

        config = TagReadConfig(block_num=255)
        assert config.block_num == 255

    def test_tag_read_block_num_invalid(self) -> None:
        """Block number above 255 should fail."""
        from vtap100.models.nfc import TagReadConfig

        with pytest.raises(ValidationError):
            TagReadConfig(block_num=256)

    def test_tag_read_key_slot_valid(self) -> None:
        """Key slot must be 1-9."""
        from vtap100.models.nfc import TagReadConfig

        config = TagReadConfig(key_slot=1)
        assert config.key_slot == 1

        config = TagReadConfig(key_slot=9)
        assert config.key_slot == 9

    def test_tag_read_key_slot_invalid_zero(self) -> None:
        """Key slot 0 should fail."""
        from vtap100.models.nfc import TagReadConfig

        with pytest.raises(ValidationError):
            TagReadConfig(key_slot=0)

    def test_tag_read_key_slot_invalid_high(self) -> None:
        """Key slot above 9 should fail."""
        from vtap100.models.nfc import TagReadConfig

        with pytest.raises(ValidationError):
            TagReadConfig(key_slot=10)

    def test_tag_read_key_type_a(self) -> None:
        """Key type can be A."""
        from vtap100.models.nfc import TagKeyType
        from vtap100.models.nfc import TagReadConfig

        config = TagReadConfig(key_type=TagKeyType.A)
        assert config.key_type == TagKeyType.A

    def test_tag_read_key_type_b(self) -> None:
        """Key type can be B."""
        from vtap100.models.nfc import TagKeyType
        from vtap100.models.nfc import TagReadConfig

        config = TagReadConfig(key_type=TagKeyType.B)
        assert config.key_type == TagKeyType.B

    def test_tag_read_offset_valid(self) -> None:
        """Offset must be 0-15."""
        from vtap100.models.nfc import TagReadConfig

        config = TagReadConfig(offset=0)
        assert config.offset == 0

        config = TagReadConfig(offset=15)
        assert config.offset == 15

    def test_tag_read_offset_invalid(self) -> None:
        """Offset above 15 should fail."""
        from vtap100.models.nfc import TagReadConfig

        with pytest.raises(ValidationError):
            TagReadConfig(offset=16)

    def test_tag_read_length_valid(self) -> None:
        """Length must be 1-16."""
        from vtap100.models.nfc import TagReadConfig

        config = TagReadConfig(length=1)
        assert config.length == 1

        config = TagReadConfig(length=16)
        assert config.length == 16

    def test_tag_read_length_invalid_zero(self) -> None:
        """Length 0 should fail."""
        from vtap100.models.nfc import TagReadConfig

        with pytest.raises(ValidationError):
            TagReadConfig(length=0)

    def test_tag_read_length_invalid_high(self) -> None:
        """Length above 16 should fail."""
        from vtap100.models.nfc import TagReadConfig

        with pytest.raises(ValidationError):
            TagReadConfig(length=17)

    def test_tag_read_format_ascii(self) -> None:
        """Format can be ASCII."""
        from vtap100.models.nfc import TagReadConfig
        from vtap100.models.nfc import TagReadFormat

        config = TagReadConfig(format=TagReadFormat.ASCII)
        assert config.format == TagReadFormat.ASCII

    def test_tag_read_format_decimal(self) -> None:
        """Format can be decimal."""
        from vtap100.models.nfc import TagReadConfig
        from vtap100.models.nfc import TagReadFormat

        config = TagReadConfig(format=TagReadFormat.DECIMAL)
        assert config.format == TagReadFormat.DECIMAL

    def test_tag_read_format_hex(self) -> None:
        """Format can be hex."""
        from vtap100.models.nfc import TagReadConfig
        from vtap100.models.nfc import TagReadFormat

        config = TagReadConfig(format=TagReadFormat.HEX)
        assert config.format == TagReadFormat.HEX

    def test_tag_read_min_digits_numeric(self) -> None:
        """Min digits can be 1-20."""
        from vtap100.models.nfc import TagReadConfig

        config = TagReadConfig(min_digits=10)
        assert config.min_digits == 10

    def test_tag_read_min_digits_auto(self) -> None:
        """Min digits can be 'A' for auto."""
        from vtap100.models.nfc import TagReadConfig

        config = TagReadConfig(min_digits="A")
        assert config.min_digits == "A"


class TestNFCTagConfigOutput:
    """Tests for NFCTagConfig config.txt output generation."""

    def test_to_config_lines_empty(self) -> None:
        """Empty config should generate no lines."""
        from vtap100.models.nfc import NFCTagConfig

        config = NFCTagConfig()
        lines = config.to_config_lines()

        assert lines == []

    def test_to_config_lines_type2_uid(self) -> None:
        """Type 2 UID mode should generate NFCType2=U."""
        from vtap100.models.nfc import NFCTagConfig
        from vtap100.models.nfc import NFCTagMode

        config = NFCTagConfig(type2=NFCTagMode.UID)
        lines = config.to_config_lines()

        assert "NFCType2=U" in lines

    def test_to_config_lines_type4_ndef(self) -> None:
        """Type 4 NDEF mode should generate NFCType4=N."""
        from vtap100.models.nfc import NFCTagConfig
        from vtap100.models.nfc import NFCTagMode

        config = NFCTagConfig(type4=NFCTagMode.NDEF)
        lines = config.to_config_lines()

        assert "NFCType4=N" in lines

    def test_to_config_lines_type5_block(self) -> None:
        """Type 5 block mode should generate NFCType5=B."""
        from vtap100.models.nfc import NFCTagConfig
        from vtap100.models.nfc import NFCTagMode

        config = NFCTagConfig(type5=NFCTagMode.BLOCK)
        lines = config.to_config_lines()

        assert "NFCType5=B" in lines

    def test_to_config_lines_report_read_error(self) -> None:
        """Report read error should generate NFCReportReadError=1."""
        from vtap100.models.nfc import NFCTagConfig

        config = NFCTagConfig(report_read_error=True)
        lines = config.to_config_lines()

        assert "NFCReportReadError=1" in lines

    def test_to_config_lines_ignore_random_uid(self) -> None:
        """Ignore random UID should generate IgnoreRandomUID=1."""
        from vtap100.models.nfc import NFCTagConfig

        config = NFCTagConfig(ignore_random_uid=True)
        lines = config.to_config_lines()

        assert "IgnoreRandomUID=1" in lines

    def test_to_config_lines_byte_order(self) -> None:
        """Reversed byte order should generate TagByteOrder=1."""
        from vtap100.models.nfc import NFCTagConfig

        config = NFCTagConfig(byte_order_reversed=True)
        lines = config.to_config_lines()

        assert "TagByteOrder=1" in lines

    def test_to_config_lines_all_types(self) -> None:
        """All NFC types enabled should generate all lines."""
        from vtap100.models.nfc import NFCTagConfig
        from vtap100.models.nfc import NFCTagMode

        config = NFCTagConfig(
            type2=NFCTagMode.UID,
            type4=NFCTagMode.NDEF,
            type5=NFCTagMode.BLOCK,
        )
        lines = config.to_config_lines()

        assert "NFCType2=U" in lines
        assert "NFCType4=N" in lines
        assert "NFCType5=B" in lines


class TestTagReadConfigOutput:
    """Tests for TagReadConfig config.txt output generation."""

    def test_to_config_lines_empty(self) -> None:
        """Empty config should generate no lines."""
        from vtap100.models.nfc import TagReadConfig

        config = TagReadConfig()
        lines = config.to_config_lines()

        assert lines == []

    def test_to_config_lines_block_num(self) -> None:
        """Block number should generate TagReadBlockNum."""
        from vtap100.models.nfc import TagReadConfig

        config = TagReadConfig(block_num=10)
        lines = config.to_config_lines()

        assert "TagReadBlockNum=10" in lines

    def test_to_config_lines_key_slot(self) -> None:
        """Key slot should generate TagReadKeySlot."""
        from vtap100.models.nfc import TagReadConfig

        config = TagReadConfig(key_slot=3)
        lines = config.to_config_lines()

        assert "TagReadKeySlot=3" in lines

    def test_to_config_lines_key_type(self) -> None:
        """Key type should generate TagReadKeyType."""
        from vtap100.models.nfc import TagKeyType
        from vtap100.models.nfc import TagReadConfig

        config = TagReadConfig(key_type=TagKeyType.B)
        lines = config.to_config_lines()

        assert "TagReadKeyType=B" in lines

    def test_to_config_lines_offset(self) -> None:
        """Non-zero offset should generate TagReadOffset."""
        from vtap100.models.nfc import TagReadConfig

        config = TagReadConfig(offset=5)
        lines = config.to_config_lines()

        assert "TagReadOffset=5" in lines

    def test_to_config_lines_length(self) -> None:
        """Length should generate TagReadLength."""
        from vtap100.models.nfc import TagReadConfig

        config = TagReadConfig(length=8)
        lines = config.to_config_lines()

        assert "TagReadLength=8" in lines

    def test_to_config_lines_format(self) -> None:
        """Format should generate TagReadFormat."""
        from vtap100.models.nfc import TagReadConfig
        from vtap100.models.nfc import TagReadFormat

        config = TagReadConfig(format=TagReadFormat.HEX)
        lines = config.to_config_lines()

        assert "TagReadFormat=h" in lines

    def test_to_config_lines_min_digits(self) -> None:
        """Min digits should generate TagReadMinDigits."""
        from vtap100.models.nfc import TagReadConfig

        config = TagReadConfig(min_digits=10)
        lines = config.to_config_lines()

        assert "TagReadMinDigits=10" in lines

    def test_to_config_lines_full_config(self) -> None:
        """Full config should generate all lines."""
        from vtap100.models.nfc import TagKeyType
        from vtap100.models.nfc import TagReadConfig
        from vtap100.models.nfc import TagReadFormat

        config = TagReadConfig(
            block_num=5,
            key_slot=2,
            key_type=TagKeyType.A,
            offset=4,
            length=8,
            format=TagReadFormat.ASCII,
            min_digits="A",
        )
        lines = config.to_config_lines()

        assert "TagReadBlockNum=5" in lines
        assert "TagReadKeySlot=2" in lines
        assert "TagReadKeyType=A" in lines
        assert "TagReadOffset=4" in lines
        assert "TagReadLength=8" in lines
        assert "TagReadFormat=a" in lines
        assert "TagReadMinDigits=A" in lines
