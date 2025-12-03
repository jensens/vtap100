"""VTAP100 Configuration Generator.

A tool for generating configuration files for the dotOrigin VTAP100 NFC reader.
Supports Apple VAS, Google Smart Tap, NFC tags, and MIFARE DESFire configurations.

Example:
    >>> from vtap100.models.vas import AppleVASConfig
    >>> from vtap100.generator import generate_config
    >>> config = AppleVASConfig(merchant_id="pass.com.example.test", key_slot=1)
"""

try:
    from vtap100._version import __version__
except ImportError:  # pragma: no cover
    __version__ = "0.0.0.dev0"

__author__ = "HEIDI Team"
