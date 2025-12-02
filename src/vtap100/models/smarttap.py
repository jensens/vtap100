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
from pydantic import field_validator


class GoogleSmartTapConfig(BaseModel):
    """Configuration for a single Google Smart Tap pass type.

    Attributes:
        collector_id: The Google Collector ID (numeric string).
            Provided by Google to uniquely identify your passes.
        key_slot: The private key slot (1-6) where the decryption key is stored.
            Use 0 for auto-detection (default).
        key_version: The key version number that must match the Google dashboard.
            Use 0 for default (no specific version).
    """

    collector_id: str = Field(
        ...,
        description="Google Collector ID (numeric string)",
        min_length=1,
    )
    key_slot: int = Field(
        default=0,
        ge=0,
        le=6,
        description="Private key slot (0=auto, 1-6=specific slot)",
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

        # Only include key_slot if it's not 0 (auto-detect)
        if self.key_slot > 0:
            lines.append(f"ST{slot_number}KeySlot={self.key_slot}")

        # Only include key_version if it's not 0 (default)
        if self.key_version > 0:
            lines.append(f"ST{slot_number}KeyVersion={self.key_version}")

        return lines


class STDefaultPassesEnabled(BaseModel):
    """Configuration for which Smart Tap pass slots are enabled at startup.

    This setting restricts which Smart Tap passes are checked at startup,
    reducing processing time when not all slots are in use.

    Note: Android supports only one Collector ID at a time.

    Attributes:
        enabled_passes: List of enabled pass numbers (1-6).
            Default is all passes enabled [1, 2, 3, 4, 5, 6].
    """

    enabled_passes: list[int] = Field(
        default=[1, 2, 3, 4, 5, 6],
        min_length=1,
        description="List of enabled Smart Tap pass numbers (1-6)",
    )

    @field_validator("enabled_passes")
    @classmethod
    def validate_pass_numbers(cls, v: list[int]) -> list[int]:
        """Validate that all pass numbers are between 1 and 6.

        Args:
            v: The list of pass numbers to validate.

        Returns:
            The validated list of pass numbers.

        Raises:
            ValueError: If any pass number is outside the range 1-6.
        """
        for pass_num in v:
            if pass_num < 1 or pass_num > 6:
                raise ValueError(f"Pass number {pass_num} must be between 1 and 6")
        return v

    def to_config_line(self) -> str:
        """Generate config.txt line for STDefaultPassesEnabled.

        Returns:
            A config.txt line (e.g., 'STDefaultPassesEnabled=1,3,5').
        """
        passes_str = ",".join(str(p) for p in self.enabled_passes)
        return f"STDefaultPassesEnabled={passes_str}"
