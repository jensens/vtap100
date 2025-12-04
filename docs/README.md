# VTAP100 Documentation

Welcome to the VTAP100 Configuration Generator documentation.

## Table of Contents

### Getting Started
- [Quickstart](quickstart.md) - Get started in minutes
- [Wizard Guide](wizard.md) - Interactive configuration wizard
- [TUI Editor](tui.md) - Visual configuration editor
- [Python API](api.md) - Use as a library

### Configuration
- [Settings Reference](configuration/settings_reference.md) - All parameters at a glance
- [Overview](configuration/overview.md) - config.txt format and basics
- [Apple VAS](configuration/apple_vas.md) - Apple Wallet Value Added Services
- [Google Smart Tap](configuration/google_smarttap.md) - Google Wallet Smart Tap
- [Keyboard Emulation](configuration/keyboard.md) - Keyboard emulation settings
- [NFC Tags](configuration/nfc_tags.md) - NFC tag types (Type 2, 4, 5)
- [MIFARE DESFire](configuration/desfire.md) - DESFire configuration
- [LED/Beep](configuration/led_beep.md) - Visual and audio feedback

### Deployment
- [Upload to Reader](deployment/upload_to_reader.md) - File transfer

### Troubleshooting
- [Troubleshooting](troubleshooting.md) - Common issues and solutions

### Reference
- [CLI Reference](references/cli.md) - All commands and options
- [Reference Sources](references/sources.md) - External links and resources

### Development
- [Developer Guide](development.md) - TDD, testing, contributing
- [Releasing](RELEASING.md) - Release process

## About the Project

The VTAP100 Configuration Generator is a Python tool for easily creating configuration files for the [Dot Origin VTAP100](https://www.vtapnfc.com/) NFC Reader.

### Features

- Apple VAS and Google Smart Tap support
- NFC tag support (Type 2, 4, 5) and MIFARE DESFire
- Keyboard emulation with flexible data sources
- LED/Buzzer feedback configuration
- Interactive wizard, TUI editor, and CLI
- Config validation

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
- [Dot Origin Website](https://www.dotorigin.com/)
- [VTAP NFC Website](https://www.vtapnfc.com/)
