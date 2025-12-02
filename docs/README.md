# VTAP100 Documentation

Welcome to the VTAP100 Configuration Generator documentation.

## Table of Contents

### Getting Started
- [Quickstart](quickstart.md) - Get started in minutes
- [Installation](quickstart.md#installation) - Installation guide

### Configuration (Phase 1-5 - Complete)
- [Overview](configuration/overview.md) - config.txt format and basics
- [Apple VAS](configuration/apple_vas.md) - Apple Wallet Value Added Services
- [Google Smart Tap](configuration/google_smarttap.md) - Google Wallet Smart Tap
- [Keyboard Emulation](configuration/keyboard.md) - Keyboard emulation settings
- [NFC Tags](configuration/nfc_tags.md) - NFC tag types (Type 2, 4, 5)
- [MIFARE DESFire](configuration/desfire.md) - DESFire configuration
- [LED/Beep](configuration/led_beep.md) - Visual and audio feedback

### Deployment
- [Upload to Reader](deployment/upload_to_reader.md) - File transfer

### Examples (integrated in documentation)
Examples can be found in the respective configuration pages:
- Apple VAS examples: see [Apple VAS](configuration/apple_vas.md)
- Google Smart Tap examples: see [Google Smart Tap](configuration/google_smarttap.md)
- Combined configuration: see [Quickstart](quickstart.md)

### Development
- [Developer Guide](development.md) - TDD, code style, contributing
- [Implementation Plan](PLAN.md) - Project plan and specification

### Reference
- [Reference Sources](references/sources.md) - All sources and links used

## About the Project

The VTAP100 Configuration Generator is a Python tool for easily creating configuration files for the [dotOrigin VTAP100](https://www.vtapnfc.com/) NFC Reader.

### Features (Phase 1-5 - Complete)

- Apple VAS support
- Google Smart Tap support
- Keyboard emulation (extended)
- NFC tag support (Type 2, 4, 5)
- MIFARE DESFire support
- LED/Buzzer configuration
- Validation
- Rich CLI with colored output

### Quickstart

```bash
# Installation
uv sync

# Generate Apple VAS configuration
vtap100 generate --apple-vas pass.com.example.mypass --key-slot 1

# Interactive wizard
vtap100 wizard
```

## Further Information

- [GitHub Repository](https://github.com/your-org/vtap100)
- [dotOrigin Website](https://www.dotorigin.com/)
- [VTAP NFC Website](https://www.vtapnfc.com/)
