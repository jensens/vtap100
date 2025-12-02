"""NFC Tag configuration models.

This module provides Pydantic models for configuring NFC tag reading
on VTAP100 NFC readers. Supports Type 2, Type 4, and Type 5 NFC tags.

Example:
    >>> from vtap100.models.nfc import NFCTagConfig, NFCTagMode
    >>> config = NFCTagConfig(type2=NFCTagMode.UID, type4=NFCTagMode.NDEF)
    >>> config.to_config_lines()
    ['NFCType2=U', 'NFCType4=N']

References:
    - https://help.vtapnfc.com/en/Content/VTAP-Commands/Config-txt-tag-settings.htm
"""

from enum import Enum
from pydantic import BaseModel
from pydantic import Field


class NFCTagMode(str, Enum):
    """NFC tag reading mode.

    Defines how the VTAP100 reads NFC tags of a specific type.
    """

    DISABLED = "0"
    """Tag type disabled."""

    UID = "U"
    """Read only the UID (unique identifier)."""

    NDEF = "N"
    """Read NDEF records from the tag."""

    BLOCK = "B"
    """Read raw block data."""

    DESFIRE = "D"
    """Read DESFire secure data (Type 4 only)."""


class TagKeyType(str, Enum):
    """MIFARE key type for authentication."""

    A = "A"
    """Key type A."""

    B = "B"
    """Key type B."""

    C = "C"
    """Key type C (compatibility)."""


class TagReadFormat(str, Enum):
    """Output format for tag data."""

    ASCII = "a"
    """ASCII text format."""

    DECIMAL = "d"
    """Decimal number format."""

    HEX = "h"
    """Hexadecimal format."""


class TagReadConfig(BaseModel):
    """Configuration for reading tag block data.

    Used when NFCType is set to BLOCK mode. Defines which block to read
    and how to format the output.

    Attributes:
        block_num: Block number to read (0-255).
        key_slot: Key slot for authentication (1-9).
        key_type: Key type for MIFARE authentication (A, B, or C).
        offset: Start byte within the block (0-15).
        length: Number of bytes to read (1-16).
        format: Output format (ASCII, decimal, or hex).
        min_digits: Minimum digits for UID output (1-20, 'A' for auto).
    """

    block_num: int | None = Field(
        default=None,
        ge=0,
        le=255,
        description="Block number to read (TagReadBlockNum)",
    )
    key_slot: int | None = Field(
        default=None,
        ge=1,
        le=9,
        description="Key slot for authentication (TagReadKeySlot)",
    )
    key_type: TagKeyType | None = Field(
        default=None,
        description="Key type for MIFARE auth (TagReadKeyType)",
    )
    offset: int = Field(
        default=0,
        ge=0,
        le=15,
        description="Start byte in block (TagReadOffset)",
    )
    length: int | None = Field(
        default=None,
        ge=1,
        le=16,
        description="Bytes to read (TagReadLength)",
    )
    format: TagReadFormat | None = Field(
        default=None,
        description="Output format (TagReadFormat)",
    )
    min_digits: int | str | None = Field(
        default=None,
        description="Min digits for UID (TagReadMinDigits), 1-20 or 'A' for auto",
    )

    def to_config_lines(self) -> list[str]:
        """Generate config.txt lines for tag read settings.

        Returns:
            List of config.txt lines.
        """
        lines: list[str] = []

        if self.block_num is not None:
            lines.append(f"TagReadBlockNum={self.block_num}")

        if self.key_slot is not None:
            lines.append(f"TagReadKeySlot={self.key_slot}")

        if self.key_type is not None:
            lines.append(f"TagReadKeyType={self.key_type.value}")

        if self.offset != 0:
            lines.append(f"TagReadOffset={self.offset}")

        if self.length is not None:
            lines.append(f"TagReadLength={self.length}")

        if self.format is not None:
            lines.append(f"TagReadFormat={self.format.value}")

        if self.min_digits is not None:
            lines.append(f"TagReadMinDigits={self.min_digits}")

        return lines


class NFCTagConfig(BaseModel):
    """Configuration for NFC tag reading.

    Defines which NFC tag types are enabled and in which mode they operate.

    Attributes:
        type2: NFC Type 2 tag mode (e.g., NTAG, MIFARE Ultralight).
        type4: NFC Type 4 tag mode (e.g., DESFire, ISO 14443-4).
        type5: NFC Type 5 tag mode (e.g., ICODE, ISO 15693).
        report_read_error: Report error payload on read failures.
        ignore_random_uid: Filter out random Type 4 UIDs.
        byte_order_reversed: Reverse byte order in output.
        tag_read: Block read configuration (for BLOCK mode).
    """

    type2: NFCTagMode | None = Field(
        default=None,
        description="NFC Type 2 tag mode (NFCType2)",
    )
    type4: NFCTagMode | None = Field(
        default=None,
        description="NFC Type 4 tag mode (NFCType4)",
    )
    type5: NFCTagMode | None = Field(
        default=None,
        description="NFC Type 5 tag mode (NFCType5)",
    )
    report_read_error: bool = Field(
        default=False,
        description="Report error payload on failures (NFCReportReadError)",
    )
    ignore_random_uid: bool = Field(
        default=False,
        description="Filter random Type 4 UIDs (IgnoreRandomUID)",
    )
    byte_order_reversed: bool = Field(
        default=False,
        description="Reverse byte order (TagByteOrder)",
    )
    tag_read: TagReadConfig | None = Field(
        default=None,
        description="Block read configuration",
    )

    def to_config_lines(self) -> list[str]:
        """Generate config.txt lines for NFC tag settings.

        Returns:
            List of config.txt lines.
        """
        lines: list[str] = []

        if self.type2 is not None:
            lines.append(f"NFCType2={self.type2.value}")

        if self.type4 is not None:
            lines.append(f"NFCType4={self.type4.value}")

        if self.type5 is not None:
            lines.append(f"NFCType5={self.type5.value}")

        if self.report_read_error:
            lines.append("NFCReportReadError=1")

        if self.ignore_random_uid:
            lines.append("IgnoreRandomUID=1")

        if self.byte_order_reversed:
            lines.append("TagByteOrder=1")

        if self.tag_read is not None:
            lines.extend(self.tag_read.to_config_lines())

        return lines
