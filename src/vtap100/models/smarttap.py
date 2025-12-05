"""Google Smart Tap configuration models.

This module provides Pydantic models for configuring Google Wallet Smart Tap
on VTAP100 NFC readers. Smart Tap allows Google Wallet passes to be read
by NFC readers for loyalty, membership, and identity applications.

Example:
    >>> config = GoogleSmartTapConfig(
    ...     collector_id="96972794",
    ...     key_slot=2,
    ...     key_version=1,
    ... )
    >>> config.to_config_lines(slot_number=1)
    ['ST1CollectorID=96972794', 'ST1KeySlot=2', 'ST1KeyVersion=1']

References:
    - https://help.vtapnfc.com/en/Content/VTAP-Commands/Config-txt-ST-settings.htm
    - https://www.passmeister.com/en/b/nfc_setup_dot_origin_vtap100_google_wallet
"""

from pydantic import BaseModel
from pydantic import Field
from vtap100.models.base import DefaultPassesEnabled


class GoogleSmartTapConfig(BaseModel):
    """Configuration for a single Google Smart Tap pass type.

    Attributes:
        collector_id: The Google Collector ID (numeric string).
            Provided by Google to uniquely identify your passes.
        key_slot: The private key slot (1-6) where the decryption key is stored.
            Required for the reader to work correctly.
        key_version: The key version number that must match the Google dashboard.
            Defaults to 0 if not specified.
    """

    collector_id: str = Field(
        ...,
        description="Google Collector ID (numeric string)",
        min_length=1,
    )
    key_slot: int = Field(
        ...,
        ge=1,
        le=6,
        description="Private key slot (1-6, required for reader to work)",
    )
    key_version: int = Field(
        default=0,
        ge=0,
        description="Key version (must match Google dashboard)",
    )

    def to_config_lines(self, slot_number: int) -> list[str]:
        """Generate config.txt lines for this Smart Tap configuration.

        Args:
            slot_number: The ST slot number (1-6) to use in parameter names.

        Returns:
            List of config.txt lines (e.g., ['ST1CollectorID=...', 'ST1KeySlot=...']).
        """
        lines = [f"ST{slot_number}CollectorID={self.collector_id}"]

        # Always include key_slot (required for reader to work)
        lines.append(f"ST{slot_number}KeySlot={self.key_slot}")

        # Always include key_version (required for Google Smart Tap)
        lines.append(f"ST{slot_number}KeyVersion={self.key_version}")

        return lines


class STDefaultPassesEnabled(DefaultPassesEnabled):
    """Configuration for which Smart Tap pass slots are enabled at startup.

    This setting restricts which Smart Tap passes are checked at startup,
    reducing processing time when not all slots are in use.

    Note: Android supports only one Collector ID at a time.

    Attributes:
        enabled_passes: List of enabled pass numbers (1-6).
            Default is all passes enabled [1, 2, 3, 4, 5, 6].
    """

    CONFIG_PREFIX = "ST"
