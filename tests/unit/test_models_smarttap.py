"""Unit tests for Google Smart Tap configuration model.

TDD Red Phase: These tests define the expected behavior of the GoogleSmartTapConfig model.
Tests should fail until the implementation is complete.
"""

from pydantic import ValidationError
import pytest


class TestGoogleSmartTapConfig:
    """Tests for GoogleSmartTapConfig model."""

    def test_smarttap_config_requires_collector_id(self) -> None:
        """Smart Tap config must have a collector_id - it's a required field."""
        from vtap100.models.smarttap import GoogleSmartTapConfig

        with pytest.raises(ValidationError):
            GoogleSmartTapConfig(key_slot=1)  # type: ignore[call-arg]

    def test_smarttap_config_valid_minimal(self) -> None:
        """Valid Smart Tap config with collector_id and key_slot should be created."""
        from vtap100.models.smarttap import GoogleSmartTapConfig

        # key_slot is now required (1-6), no longer has default
        config = GoogleSmartTapConfig(collector_id="96972794", key_slot=1)
        assert config.collector_id == "96972794"
        assert config.key_slot == 1
        assert config.key_version == 0  # Default value

    def test_smarttap_config_requires_key_slot(self) -> None:
        """Smart Tap config must have a key_slot - it's a required field."""
        from vtap100.models.smarttap import GoogleSmartTapConfig

        with pytest.raises(ValidationError):
            GoogleSmartTapConfig(collector_id="96972794")  # Missing key_slot

    def test_smarttap_config_key_slot_zero_invalid(self) -> None:
        """Key slot 0 (auto-detect) is no longer valid - must be 1-6."""
        from vtap100.models.smarttap import GoogleSmartTapConfig

        with pytest.raises(ValidationError):
            GoogleSmartTapConfig(
                collector_id="96972794",
                key_slot=0,
            )

    def test_smarttap_config_valid_with_key_slot(self) -> None:
        """Valid Smart Tap config with collector_id and key_slot."""
        from vtap100.models.smarttap import GoogleSmartTapConfig

        config = GoogleSmartTapConfig(
            collector_id="96972794",
            key_slot=2,
        )
        assert config.collector_id == "96972794"
        assert config.key_slot == 2

    def test_smarttap_config_valid_with_all_fields(self) -> None:
        """Valid Smart Tap config with all fields."""
        from vtap100.models.smarttap import GoogleSmartTapConfig

        config = GoogleSmartTapConfig(
            collector_id="96972794",
            key_slot=2,
            key_version=1,
        )
        assert config.collector_id == "96972794"
        assert config.key_slot == 2
        assert config.key_version == 1

    def test_smarttap_config_collector_id_numeric_string(self) -> None:
        """Collector ID should be a numeric string."""
        from vtap100.models.smarttap import GoogleSmartTapConfig

        # Valid numeric strings
        config = GoogleSmartTapConfig(collector_id="12345678", key_slot=1)
        assert config.collector_id == "12345678"

    def test_smarttap_config_collector_id_empty_invalid(self) -> None:
        """Empty string is not a valid collector_id."""
        from vtap100.models.smarttap import GoogleSmartTapConfig

        with pytest.raises(ValidationError):
            GoogleSmartTapConfig(collector_id="")

    def test_smarttap_config_key_slot_valid_range(self) -> None:
        """Key slot must be between 1 and 6 (0 is no longer valid)."""
        from vtap100.models.smarttap import GoogleSmartTapConfig

        # Valid slots are now 1-6 only
        for slot in range(1, 7):  # 1-6
            config = GoogleSmartTapConfig(
                collector_id="96972794",
                key_slot=slot,
            )
            assert config.key_slot == slot

    def test_smarttap_config_key_slot_invalid_negative(self) -> None:
        """Negative key slot should be invalid."""
        from vtap100.models.smarttap import GoogleSmartTapConfig

        with pytest.raises(ValidationError):
            GoogleSmartTapConfig(
                collector_id="96972794",
                key_slot=-1,
            )

    def test_smarttap_config_key_slot_invalid_too_high(self) -> None:
        """Key slot > 6 should be invalid."""
        from vtap100.models.smarttap import GoogleSmartTapConfig

        with pytest.raises(ValidationError):
            GoogleSmartTapConfig(
                collector_id="96972794",
                key_slot=7,
            )

    def test_smarttap_config_key_version_default(self) -> None:
        """Key version should default to 0."""
        from vtap100.models.smarttap import GoogleSmartTapConfig

        config = GoogleSmartTapConfig(collector_id="96972794", key_slot=1)
        assert config.key_version == 0

    def test_smarttap_config_key_version_positive(self) -> None:
        """Key version can be any non-negative integer."""
        from vtap100.models.smarttap import GoogleSmartTapConfig

        config = GoogleSmartTapConfig(
            collector_id="96972794",
            key_slot=1,
            key_version=10,
        )
        assert config.key_version == 10

    def test_smarttap_config_key_version_invalid_negative(self) -> None:
        """Negative key version should be invalid."""
        from vtap100.models.smarttap import GoogleSmartTapConfig

        with pytest.raises(ValidationError):
            GoogleSmartTapConfig(
                collector_id="96972794",
                key_version=-1,
            )


class TestGoogleSmartTapConfigOutput:
    """Tests for GoogleSmartTapConfig config.txt output generation."""

    def test_to_config_lines_always_includes_key_slot_and_version(self) -> None:
        """Config should always generate CollectorID, KeySlot and KeyVersion lines."""
        from vtap100.models.smarttap import GoogleSmartTapConfig

        config = GoogleSmartTapConfig(collector_id="96972794", key_slot=1)
        lines = config.to_config_lines(slot_number=1)

        assert "ST1CollectorID=96972794" in lines
        # KeySlot is now always output (required for reader to work)
        assert "ST1KeySlot=1" in lines
        # KeyVersion is now always output (required for Google Smart Tap)
        assert "ST1KeyVersion=0" in lines

    def test_to_config_lines_with_key_slot(self) -> None:
        """Config with key_slot should include KeySlot line."""
        from vtap100.models.smarttap import GoogleSmartTapConfig

        config = GoogleSmartTapConfig(
            collector_id="96972794",
            key_slot=2,
        )
        lines = config.to_config_lines(slot_number=1)

        assert "ST1CollectorID=96972794" in lines
        assert "ST1KeySlot=2" in lines

    def test_to_config_lines_with_key_version(self) -> None:
        """Config with key_version should include KeyVersion line."""
        from vtap100.models.smarttap import GoogleSmartTapConfig

        config = GoogleSmartTapConfig(
            collector_id="96972794",
            key_slot=2,
            key_version=1,
        )
        lines = config.to_config_lines(slot_number=1)

        assert "ST1CollectorID=96972794" in lines
        assert "ST1KeySlot=2" in lines
        assert "ST1KeyVersion=1" in lines

    def test_to_config_lines_different_slot_numbers(self) -> None:
        """Config lines should use correct slot number prefix."""
        from vtap100.models.smarttap import GoogleSmartTapConfig

        config = GoogleSmartTapConfig(
            collector_id="96972794",
            key_slot=3,
            key_version=1,
        )

        # Test different slot numbers
        for slot_num in range(1, 7):
            lines = config.to_config_lines(slot_number=slot_num)
            assert f"ST{slot_num}CollectorID=96972794" in lines
            assert f"ST{slot_num}KeySlot=3" in lines
            assert f"ST{slot_num}KeyVersion=1" in lines

    def test_to_config_lines_returns_list(self) -> None:
        """to_config_lines should return a list of strings."""
        from vtap100.models.smarttap import GoogleSmartTapConfig

        config = GoogleSmartTapConfig(collector_id="96972794", key_slot=1)
        lines = config.to_config_lines(slot_number=1)

        assert isinstance(lines, list)
        assert all(isinstance(line, str) for line in lines)


class TestSTDefaultPassesEnabled:
    """Tests for STDefaultPassesEnabled setting."""

    def test_default_passes_enabled_default(self) -> None:
        """Default should be all passes enabled (1-6)."""
        from vtap100.models.smarttap import STDefaultPassesEnabled

        config = STDefaultPassesEnabled()
        assert config.enabled_passes == [1, 2, 3, 4, 5, 6]

    def test_default_passes_enabled_custom(self) -> None:
        """Should accept custom list of enabled passes."""
        from vtap100.models.smarttap import STDefaultPassesEnabled

        config = STDefaultPassesEnabled(enabled_passes=[1, 3, 5])
        assert config.enabled_passes == [1, 3, 5]

    def test_default_passes_enabled_single(self) -> None:
        """Should accept single pass enabled."""
        from vtap100.models.smarttap import STDefaultPassesEnabled

        config = STDefaultPassesEnabled(enabled_passes=[2])
        assert config.enabled_passes == [2]

    def test_default_passes_enabled_to_config_line(self) -> None:
        """Should generate correct config line."""
        from vtap100.models.smarttap import STDefaultPassesEnabled

        config = STDefaultPassesEnabled(enabled_passes=[1, 3, 5])
        line = config.to_config_line()
        assert line == "STDefaultPassesEnabled=1,3,5"

    def test_default_passes_enabled_invalid_pass_number(self) -> None:
        """Pass numbers must be between 1 and 6."""
        from vtap100.models.smarttap import STDefaultPassesEnabled

        with pytest.raises(ValidationError):
            STDefaultPassesEnabled(enabled_passes=[0, 1, 2])

        with pytest.raises(ValidationError):
            STDefaultPassesEnabled(enabled_passes=[1, 7])

    def test_default_passes_enabled_empty_invalid(self) -> None:
        """Empty list should be invalid - at least one pass required."""
        from vtap100.models.smarttap import STDefaultPassesEnabled

        with pytest.raises(ValidationError):
            STDefaultPassesEnabled(enabled_passes=[])
