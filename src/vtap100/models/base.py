"""Base models for VTAP100 configuration.

This module provides base classes for configuration models to reduce code duplication.
"""

from pydantic import BaseModel
from pydantic import Field
from pydantic import field_validator
from typing import ClassVar


class DefaultPassesEnabled(BaseModel):
    """Base class for default passes enabled configuration.

    This base class provides the shared logic for VAS and SmartTap
    default passes enabled settings.

    Attributes:
        enabled_passes: List of enabled pass numbers (1-6).
            Default is all passes enabled [1, 2, 3, 4, 5, 6].

    Subclasses must define:
        CONFIG_PREFIX: The config key prefix ("VAS" or "ST").
    """

    CONFIG_PREFIX: ClassVar[str] = ""

    enabled_passes: list[int] = Field(
        default=[1, 2, 3, 4, 5, 6],
        min_length=1,
        description="List of enabled pass numbers (1-6)",
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
        """Generate config.txt line for DefaultPassesEnabled.

        Returns:
            A config.txt line (e.g., 'VASDefaultPassesEnabled=1,3,5').
        """
        passes_str = ",".join(str(p) for p in self.enabled_passes)
        return f"{self.CONFIG_PREFIX}DefaultPassesEnabled={passes_str}"
