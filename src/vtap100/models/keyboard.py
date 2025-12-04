"""Keyboard emulation configuration models.

This module provides Pydantic models for configuring keyboard emulation
on VTAP100 NFC readers. Keyboard emulation sends pass data as keystrokes
to the connected computer, appearing as if typed on a keyboard.

Example:
    >>> config = KeyboardConfig(
    ...     log_mode=True,
    ...     source="A1",
    ... )
    >>> config.to_config_lines()
    ['KBLogMode=1', 'KBSource=A1']

References:
    - https://help.vtapnfc.com/en/Content/VTAP-Commands/Config-txt-KB-settings.htm
"""

from pydantic import BaseModel
from pydantic import Field


class KeyboardConfig(BaseModel):
    """Configuration for keyboard emulation.

    Keyboard emulation sends pass data as keystrokes to the host computer.
    When enabled, successful pass reads appear in any open text editor.

    Attributes:
        log_mode: Enable keyboard emulation (KBLogMode).
            True = send data as keystrokes, False = disabled.
        enable: Enable USB keyboard device function (KBEnable).
            Set False for Android integrations that don't need HID.
        source: Which data sources trigger keyboard output (KBSource).
            Hex string defining pass types (e.g., 'A1' for Apple VAS).
        prefix: Optional prefix before data (KBPrefix).
            Can be ASCII-hex (%0A) or variables ($t for timestamp).
        postfix: Suffix after data (KBPostfix). Default is newline (%0A).
        delay_ms: Delay between keystrokes in ms (KBDelayMS). Range: 5-255.
        pass_mode: Enable pass payload extraction (KBPassMode).
        pass_section: Which section to extract (KBPassSection).
        pass_separator: Separator character for sections (KBPassSeparator).
        pass_start: Start position for extraction (KBPassStart).
        pass_length: Length of extraction, 0 = all (KBPassLength).
    """

    log_mode: bool = Field(
        default=False,
        description="Enable keyboard emulation (KBLogMode)",
    )
    enable: bool = Field(
        default=True,
        description="Enable USB keyboard device function (KBEnable)",
    )
    source: str = Field(
        default="A5",
        description="Data sources for keyboard output (KBSource)",
    )
    prefix: str | None = Field(
        default=None,
        description="Prefix before data (KBPrefix), e.g., '$t' for timestamp",
    )
    postfix: str = Field(
        default="%0A",
        description="Suffix after data (KBPostfix), default is newline",
    )
    delay_ms: int = Field(
        default=5,
        ge=5,
        le=255,
        description="Delay between keystrokes in ms (KBDelayMS)",
    )
    pass_mode: bool = Field(
        default=False,
        description="Enable pass payload extraction (KBPassMode)",
    )
    pass_section: int = Field(
        default=0,
        ge=0,
        description="Which section to extract (KBPassSection)",
    )
    pass_separator: str = Field(
        default="|",
        description="Separator character for sections (KBPassSeparator)",
    )
    pass_start: int = Field(
        default=0,
        ge=0,
        description="Start position for extraction (KBPassStart)",
    )
    pass_length: int = Field(
        default=0,
        ge=0,
        description="Length of extraction, 0 = all (KBPassLength)",
    )

    def to_config_lines(self) -> list[str]:
        """Generate config.txt lines for keyboard emulation settings.

        Returns:
            List of config.txt lines (e.g., ['KBLogMode=1', 'KBSource=A1']).
        """
        lines: list[str] = []

        # Always include KBLogMode
        lines.append(f"KBLogMode={1 if self.log_mode else 0}")

        # Include KBEnable only if disabled (default is enabled)
        if not self.enable:
            lines.append("KBEnable=0")

        # Include KBSource if not default or if log_mode is enabled
        if self.source != "A5" or self.log_mode:
            lines.append(f"KBSource={self.source}")

        # Include prefix if set
        if self.prefix is not None:
            lines.append(f"KBPrefix={self.prefix}")

        # Include postfix only if not default (%0A)
        if self.postfix != "%0A":
            lines.append(f"KBPostfix={self.postfix}")

        # Include delay only if not default (5ms)
        if self.delay_ms != 5:
            lines.append(f"KBDelayMS={self.delay_ms}")

        # Pass extraction settings (only if pass_mode is enabled)
        if self.pass_mode:
            lines.append("KBPassMode=1")

            # Include pass_section only if not default (0)
            if self.pass_section != 0:
                lines.append(f"KBPassSection={self.pass_section}")

            # Include pass_separator only if not default (|)
            if self.pass_separator != "|":
                lines.append(f"KBPassSeparator={self.pass_separator}")

            # Include pass_start only if not default (0)
            if self.pass_start != 0:
                lines.append(f"KBPassStart={self.pass_start}")

            # Include pass_length only if not default (0)
            if self.pass_length != 0:
                lines.append(f"KBPassLength={self.pass_length}")

        return lines


class KBSourceBuilder:
    """Builder for constructing KBSource hex bitmask values.

    KBSource uses hexadecimal bitmasks per official VTAP documentation:
    - Bit 7 (0x80): Mobile Pass (Apple VAS / Google Smart Tap)
    - Bit 6 (0x40): STUID
    - Bit 5 (0x20): Card Emulation Write Mode
    - Bit 2 (0x04): Scanners
    - Bit 1 (0x02): Command Interface Messages
    - Bit 0 (0x01): Card/Tag UID

    Reference:
        https://help.vtapnfc.com/en/Content/VTAP-Commands/Config-txt-KB-settings.htm

    Example:
        >>> source = KBSourceBuilder().mobile_pass().card_tag_uid().build()
        >>> source
        '81'

        >>> # Default A5 configuration
        >>> source = (KBSourceBuilder()
        ...     .mobile_pass()
        ...     .card_emulation()
        ...     .scanners()
        ...     .card_tag_uid()
        ...     .build())
        >>> source
        'A5'
    """

    # Bit masks for KBSource
    MOBILE_PASS = 0x80  # Bit 7: Apple VAS / Google Smart Tap
    STUID = 0x40  # Bit 6: STUID
    CARD_EMULATION = 0x20  # Bit 5: Card Emulation Write Mode
    SCANNERS = 0x04  # Bit 2: Scanners
    COMMAND_INTERFACE = 0x02  # Bit 1: Command Interface Messages
    CARD_TAG_UID = 0x01  # Bit 0: Card/Tag UID

    def __init__(self) -> None:
        """Initialize an empty KBSource builder with value 0."""
        self._value: int = 0

    def mobile_pass(self) -> "KBSourceBuilder":
        """Enable mobile pass data (Apple VAS / Google Smart Tap)."""
        self._value |= self.MOBILE_PASS
        return self

    def stuid(self) -> "KBSourceBuilder":
        """Enable STUID data."""
        self._value |= self.STUID
        return self

    def card_emulation(self) -> "KBSourceBuilder":
        """Enable card emulation write mode."""
        self._value |= self.CARD_EMULATION
        return self

    def scanners(self) -> "KBSourceBuilder":
        """Enable scanner input."""
        self._value |= self.SCANNERS
        return self

    def command_interface(self) -> "KBSourceBuilder":
        """Enable command interface messages."""
        self._value |= self.COMMAND_INTERFACE
        return self

    def card_tag_uid(self) -> "KBSourceBuilder":
        """Enable card/tag UID data."""
        self._value |= self.CARD_TAG_UID
        return self

    def build(self) -> str:
        """Build the final KBSource hex string.

        Returns:
            Uppercase hex string (e.g., "A5", "80", "01").
        """
        return f"{self._value:02X}"
