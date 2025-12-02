"""config.txt file parser for VTAP100 NFC reader.

This module provides the ConfigParser class for parsing VTAP100
configuration files back into VTAPConfig objects.

Example:
    >>> from vtap100.parser import parse
    >>>
    >>> content = '''!VTAPconfig
    ... VAS1MerchantID=pass.com.example.test
    ... VAS1KeySlot=1
    ... '''
    >>> config = parse(content)
    >>> config.vas_configs[0].merchant_id
    'pass.com.example.test'
"""

import re
from dataclasses import dataclass, field

from vtap100.models.config import VTAPConfig
from vtap100.models.keyboard import KeyboardConfig
from vtap100.models.smarttap import GoogleSmartTapConfig
from vtap100.models.vas import AppleVASConfig


@dataclass
class _VASParseData:
    """Temporary data structure for parsing VAS configs."""

    merchant_id: str | None = None
    key_slot: int = 0
    merchant_url: str | None = None


@dataclass
class _SmartTapParseData:
    """Temporary data structure for parsing Smart Tap configs."""

    collector_id: str | None = None
    key_slot: int = 0
    key_version: int = 0


@dataclass
class _KeyboardParseData:
    """Temporary data structure for parsing Keyboard config."""

    log_mode: bool | None = None
    source: str | None = None


class ConfigParser:
    """Parser for VTAP100 config.txt files.

    This class parses the config.txt content and creates a VTAPConfig object.

    Attributes:
        content: The raw config.txt content to parse.
    """

    HEADER = "!VTAPconfig"

    # Regex patterns for parsing
    VAS_MERCHANT_ID = re.compile(r"^VAS(\d+)MerchantID=(.+)$")
    VAS_KEY_SLOT = re.compile(r"^VAS(\d+)KeySlot=(\d+)$")
    VAS_MERCHANT_URL = re.compile(r"^VAS(\d+)MerchantURL=(.+)$")

    ST_COLLECTOR_ID = re.compile(r"^ST(\d+)CollectorID=(.+)$")
    ST_KEY_SLOT = re.compile(r"^ST(\d+)KeySlot=(\d+)$")
    ST_KEY_VERSION = re.compile(r"^ST(\d+)KeyVersion=(\d+)$")

    KB_LOG_MODE = re.compile(r"^KBLogMode=(\d+)$")
    KB_SOURCE = re.compile(r"^KBSource=(.+)$")

    def __init__(self, content: str) -> None:
        """Initialize the parser with config content.

        Args:
            content: The raw config.txt content to parse.
        """
        self.content = content
        self._vas_data: dict[int, _VASParseData] = {}
        self._smarttap_data: dict[int, _SmartTapParseData] = {}
        self._keyboard_data: _KeyboardParseData = _KeyboardParseData()

    def parse(self) -> VTAPConfig:
        """Parse the config content into a VTAPConfig object.

        Returns:
            A VTAPConfig object with the parsed configuration.

        Raises:
            ValueError: If the config is missing the required header.
        """
        lines = self.content.strip().split("\n")

        if not lines or not lines[0].strip().startswith(self.HEADER):
            raise ValueError("Config must start with !VTAPconfig header")

        # Parse each line
        for line in lines[1:]:
            line = line.strip()

            # Skip empty lines and comments
            if not line or line.startswith(";"):
                continue

            self._parse_line(line)

        return self._build_config()

    def _parse_line(self, line: str) -> None:
        """Parse a single config line.

        Args:
            line: A single line from the config file.
        """
        # VAS configurations
        if match := self.VAS_MERCHANT_ID.match(line):
            slot = int(match.group(1))
            self._get_vas_data(slot).merchant_id = match.group(2)
            return

        if match := self.VAS_KEY_SLOT.match(line):
            slot = int(match.group(1))
            self._get_vas_data(slot).key_slot = int(match.group(2))
            return

        if match := self.VAS_MERCHANT_URL.match(line):
            slot = int(match.group(1))
            self._get_vas_data(slot).merchant_url = match.group(2)
            return

        # Smart Tap configurations
        if match := self.ST_COLLECTOR_ID.match(line):
            slot = int(match.group(1))
            self._get_smarttap_data(slot).collector_id = match.group(2)
            return

        if match := self.ST_KEY_SLOT.match(line):
            slot = int(match.group(1))
            self._get_smarttap_data(slot).key_slot = int(match.group(2))
            return

        if match := self.ST_KEY_VERSION.match(line):
            slot = int(match.group(1))
            self._get_smarttap_data(slot).key_version = int(match.group(2))
            return

        # Keyboard configuration
        if match := self.KB_LOG_MODE.match(line):
            self._keyboard_data.log_mode = match.group(1) == "1"
            return

        if match := self.KB_SOURCE.match(line):
            self._keyboard_data.source = match.group(1)
            return

    def _get_vas_data(self, slot: int) -> _VASParseData:
        """Get or create VAS data for a slot.

        Args:
            slot: The VAS slot number.

        Returns:
            The VAS parse data for the slot.
        """
        if slot not in self._vas_data:
            self._vas_data[slot] = _VASParseData()
        return self._vas_data[slot]

    def _get_smarttap_data(self, slot: int) -> _SmartTapParseData:
        """Get or create Smart Tap data for a slot.

        Args:
            slot: The Smart Tap slot number.

        Returns:
            The Smart Tap parse data for the slot.
        """
        if slot not in self._smarttap_data:
            self._smarttap_data[slot] = _SmartTapParseData()
        return self._smarttap_data[slot]

    def _build_config(self) -> VTAPConfig:
        """Build the final VTAPConfig from parsed data.

        Returns:
            A complete VTAPConfig object.
        """
        vas_configs: list[AppleVASConfig] = []
        smarttap_configs: list[GoogleSmartTapConfig] = []
        keyboard: KeyboardConfig | None = None

        # Build VAS configs in order
        for slot in sorted(self._vas_data.keys()):
            data = self._vas_data[slot]
            if data.merchant_id:
                vas_configs.append(
                    AppleVASConfig(
                        merchant_id=data.merchant_id,
                        key_slot=data.key_slot,
                        merchant_url=data.merchant_url,
                    )
                )

        # Build Smart Tap configs in order
        for slot in sorted(self._smarttap_data.keys()):
            data = self._smarttap_data[slot]
            if data.collector_id:
                smarttap_configs.append(
                    GoogleSmartTapConfig(
                        collector_id=data.collector_id,
                        key_slot=data.key_slot,
                        key_version=data.key_version,
                    )
                )

        # Build Keyboard config
        if self._keyboard_data.log_mode is not None or self._keyboard_data.source is not None:
            keyboard = KeyboardConfig(
                log_mode=self._keyboard_data.log_mode or False,
                source=self._keyboard_data.source or "A5",
            )

        return VTAPConfig(
            vas_configs=vas_configs,
            smarttap_configs=smarttap_configs,
            keyboard=keyboard,
        )


def parse(content: str) -> VTAPConfig:
    """Parse config.txt content into a VTAPConfig object.

    This is a convenience function that creates a ConfigParser and parses the content.

    Args:
        content: The raw config.txt content to parse.

    Returns:
        A VTAPConfig object with the parsed configuration.

    Raises:
        ValueError: If the config is missing the required header.

    Example:
        >>> content = '''!VTAPconfig
        ... VAS1MerchantID=pass.com.example.test
        ... VAS1KeySlot=1
        ... '''
        >>> config = parse(content)
        >>> config.vas_configs[0].merchant_id
        'pass.com.example.test'
    """
    parser = ConfigParser(content)
    return parser.parse()
