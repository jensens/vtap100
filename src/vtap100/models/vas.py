"""Apple VAS (Value Added Services) configuration models.

This module provides Pydantic models for configuring Apple Wallet VAS
on VTAP100 NFC readers. VAS allows Apple Wallet passes to be read
by NFC readers for loyalty, membership, and identity applications.

Example:
    >>> config = AppleVASConfig(
    ...     merchant_id="pass.com.example.myapp",
    ...     key_slot=1,
    ... )
    >>> config.to_config_lines(slot_number=1)
    ['VAS1MerchantID=pass.com.example.myapp', 'VAS1KeySlot=1']

References:
    - https://help.vtapnfc.com/en/Content/VTAP-Commands/Config-txt-VAS_settings.htm
    - https://www.passmeister.com/en/b/nfc_setup_dot_origin_vtap100_apple_wallet
"""

from pydantic import BaseModel, Field, field_validator


class AppleVASConfig(BaseModel):
    """Configuration for a single Apple VAS pass type.

    Attributes:
        merchant_id: The Apple Pass Type ID (e.g., 'pass.com.company.passname').
            Must start with 'pass.' prefix.
        key_slot: The private key slot (1-6) where the decryption key is stored.
            Use 0 for auto-detection (default).
        merchant_url: Optional URL to invoke when presenting a pass.
            Note: Currently unsupported by iOS for VAS-only transactions.
    """

    merchant_id: str = Field(
        ...,
        description="Apple Pass Type ID (must start with 'pass.')",
        min_length=1,
    )
    key_slot: int = Field(
        default=0,
        ge=0,
        le=6,
        description="Private key slot (0=auto, 1-6=specific slot)",
    )
    merchant_url: str | None = Field(
        default=None,
        description="Optional URL for pass presentation",
    )

    @field_validator("merchant_id")
    @classmethod
    def validate_merchant_id(cls, v: str) -> str:
        """Validate that merchant_id starts with 'pass.' prefix.

        Args:
            v: The merchant_id value to validate.

        Returns:
            The validated merchant_id.

        Raises:
            ValueError: If merchant_id doesn't start with 'pass.'.
        """
        if not v.startswith("pass."):
            raise ValueError("merchant_id must start with 'pass.' prefix")
        return v

    def to_config_lines(self, slot_number: int) -> list[str]:
        """Generate config.txt lines for this VAS configuration.

        Args:
            slot_number: The VAS slot number (1-6) to use in parameter names.

        Returns:
            List of config.txt lines (e.g., ['VAS1MerchantID=...', 'VAS1KeySlot=...']).
        """
        lines = [f"VAS{slot_number}MerchantID={self.merchant_id}"]

        # Only include key_slot if it's not 0 (auto-detect)
        if self.key_slot > 0:
            lines.append(f"VAS{slot_number}KeySlot={self.key_slot}")

        if self.merchant_url:
            lines.append(f"VAS{slot_number}MerchantURL={self.merchant_url}")

        return lines


class VASDefaultPassesEnabled(BaseModel):
    """Configuration for which VAS pass slots are enabled at startup.

    This setting restricts which VAS passes are checked at startup,
    reducing processing time when not all slots are in use.

    Attributes:
        enabled_passes: List of enabled pass numbers (1-6).
            Default is all passes enabled [1, 2, 3, 4, 5, 6].
    """

    enabled_passes: list[int] = Field(
        default=[1, 2, 3, 4, 5, 6],
        min_length=1,
        description="List of enabled VAS pass numbers (1-6)",
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
        """Generate config.txt line for VASDefaultPassesEnabled.

        Returns:
            A config.txt line (e.g., 'VASDefaultPassesEnabled=1,3,5').
        """
        passes_str = ",".join(str(p) for p in self.enabled_passes)
        return f"VASDefaultPassesEnabled={passes_str}"
