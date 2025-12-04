# VTAP100 Configuration Generator

A Python tool for generating configuration files for the **Dot Origin VTAP100** NFC Reader.

## Features

- **TUI Editor** - Visual terminal interface for configuration
- **Apple VAS** (Value Added Services) configuration
- **Google Smart Tap** configuration
- **Keyboard emulation** settings
- **NFC Tag** support (Type 2, 4, 5)
- **MIFARE DESFire** configuration
- **LED/Buzzer** feedback settings
- **Validation** of all parameters
- **Rich CLI** with colored output

## Usage

### Run directly with uvx (no installation)

```bash
# TUI Editor
uvx vtap100 editor
uvx vtap100 editor config.txt

# Generate configuration
uvx vtap100 generate --apple-vas pass.com.example.mypass --key-slot 1

# Interactive wizard
uvx vtap100 wizard
```

### Install from PyPI

```bash
# With uv
uv tool install vtap100

# With pip
pip install vtap100
```

Then use without `uvx` prefix:

```bash
vtap100 editor config.txt
```

## TUI Editor

Launch the full-featured terminal user interface:

```bash
vtap100 editor              # New configuration
vtap100 editor config.txt   # Edit existing file
```

Features:
- Visual configuration of all settings
- Live preview of generated config.txt
- Context-sensitive help
- Load/Save/Export
- Bilingual (English/German)

See [TUI Editor Documentation](https://github.com/jensens/vtap100/blob/main/docs/tui.md) for keyboard shortcuts and details.

## Documentation

Detailed documentation can be found in the [docs/](https://github.com/jensens/vtap100/tree/main/docs) directory:

- [Quickstart](https://github.com/jensens/vtap100/blob/main/docs/quickstart.md)
- [Apple VAS Configuration](https://github.com/jensens/vtap100/blob/main/docs/configuration/apple_vas.md)
- [Google Smart Tap Configuration](https://github.com/jensens/vtap100/blob/main/docs/configuration/google_smarttap.md)
- [Keyboard Emulation](https://github.com/jensens/vtap100/blob/main/docs/configuration/keyboard.md)
- [Deployment to Reader](https://github.com/jensens/vtap100/blob/main/docs/deployment/upload_to_reader.md)
- [Reference Sources](https://github.com/jensens/vtap100/blob/main/docs/references/sources.md)

## Development

See [docs/development.md](https://github.com/jensens/vtap100/blob/main/docs/development.md) for the full development guide (TDD, testing, TUI architecture).

## License

MIT License - see [LICENSE](https://github.com/jensens/vtap100/blob/main/LICENSE) for details.

## Links

- [Dot Origin Website](https://www.dotorigin.com/)
- [VTAP NFC Website](https://www.vtapnfc.com/)
- [VTAP Configuration Guide (PDF)](https://www.vtapnfc.com/downloads/VTAP_Configuration_Guide.pdf)
