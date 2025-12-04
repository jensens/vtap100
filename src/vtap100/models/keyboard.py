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
    """Builder for constructing KBSource hex values.

    KBSource is a bitwise combination of pass type characters that
    determines which data types trigger keyboard output.

    Characters:
        A = Apple VAS Pass
        G = Google Smart Tap Pass
        0 = MIFARE Card/Tag
        2 = NFC Type 2
        4 = NFC Type 4
        6 = NFC Type 5
        E = Card Emulation
        X = Apple Wallet Access/ECP2 (iPhone)
        W = Apple Wallet Access/ECP2 (Apple Watch)

    Example:
        >>> source = KBSourceBuilder().apple_vas().google_smarttap().build()
        >>> source
        'AG'
    """

    # Mapping of method names to source codes
    _SOURCE_CODES: dict[str, str] = {
        "apple_vas": "A",
        "google_smarttap": "G",
        "mifare": "0",
        "nfc_type2": "2",
        "nfc_type4": "4",
        "nfc_type5": "6",
        "card_emulation": "E",
        "apple_wallet_iphone": "X",
        "apple_wallet_watch": "W",
    }

    def __init__(self) -> None:
        """Initialize an empty KBSource builder."""
        self._sources: list[str] = []

    def _add(self, code: str) -> "KBSourceBuilder":
        """Add a source code if not already present.

        Args:
            code: The source code character to add.

        Returns:
            Self for method chaining.
        """
        if code not in self._sources:
            self._sources.append(code)
        return self

    def apple_vas(self) -> "KBSourceBuilder":
        """Add Apple VAS pass type to source."""
        return self._add(self._SOURCE_CODES["apple_vas"])

    def google_smarttap(self) -> "KBSourceBuilder":
        """Add Google Smart Tap pass type to source."""
        return self._add(self._SOURCE_CODES["google_smarttap"])

    def mifare(self) -> "KBSourceBuilder":
        """Add MIFARE card/tag type to source."""
        return self._add(self._SOURCE_CODES["mifare"])

    def nfc_type2(self) -> "KBSourceBuilder":
        """Add NFC Type 2 tag type to source."""
        return self._add(self._SOURCE_CODES["nfc_type2"])

    def nfc_type4(self) -> "KBSourceBuilder":
        """Add NFC Type 4 tag type to source."""
        return self._add(self._SOURCE_CODES["nfc_type4"])

    def nfc_type5(self) -> "KBSourceBuilder":
        """Add NFC Type 5 tag type to source."""
        return self._add(self._SOURCE_CODES["nfc_type5"])

    def card_emulation(self) -> "KBSourceBuilder":
        """Add card emulation type to source."""
        return self._add(self._SOURCE_CODES["card_emulation"])

    def apple_wallet_iphone(self) -> "KBSourceBuilder":
        """Add Apple Wallet Access/ECP2 iPhone type to source."""
        return self._add(self._SOURCE_CODES["apple_wallet_iphone"])

    def apple_wallet_watch(self) -> "KBSourceBuilder":
        """Add Apple Wallet Access/ECP2 Apple Watch type to source."""
        return self._add(self._SOURCE_CODES["apple_wallet_watch"])

    def build(self) -> str:
        """Build the final KBSource string.

        Returns:
            A string combining all selected source types.
            Returns "0" if no sources were selected.
        """
        if not self._sources:
            return "0"
        return "".join(self._sources)
