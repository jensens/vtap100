# VTAP100 Configuration Generator

A Python tool for generating configuration files for the **dotOrigin VTAP100** NFC Reader.

## Features

- **Apple VAS** (Value Added Services) configuration
- **Google Smart Tap** configuration
- **Keyboard emulation** settings
- **NFC Tag** support (Type 2, 4, 5)
- **MIFARE DESFire** configuration
- **LED/Buzzer** feedback settings
- **Validation** of all parameters
- **Rich CLI** with colored output

## Installation

```bash
# With uv (recommended)
uv sync

# Development dependencies
uv sync --extra dev

# Alternatively with pip
pip install -e ".[dev]"
```

## Quickstart

### Apple VAS Configuration

```bash
vtap100 generate --apple-vas pass.com.example.mypass --key-slot 1 --output ./config.txt
```

### Google Smart Tap Configuration

```bash
vtap100 generate --google-st 96972794 --key-slot 2 --key-version 1 --output ./config.txt
```

### Interactive Mode

```bash
vtap100 wizard
```

### Validate Configuration

```bash
vtap100 validate ./config.txt
```

## Documentation

Detailed documentation can be found in the [docs/](docs/) directory:

- [Quickstart](docs/quickstart.md)
- [Apple VAS Configuration](docs/configuration/apple_vas.md)
- [Google Smart Tap Configuration](docs/configuration/google_smarttap.md)
- [Keyboard Emulation](docs/configuration/keyboard.md)
- [Deployment to Reader](docs/deployment/upload_to_reader.md)
- [Reference Sources](docs/references/sources.md)

## Development

This project uses **Test-Driven Development (TDD)**.

```bash
# Run tests
uv run pytest

# With coverage
uv run pytest --cov=vtap100 --cov-report=html

# Linting
uv run ruff check src tests
uv run ruff format src tests

# Type checking
uv run mypy src
```

## License

MIT License - see [LICENSE](LICENSE) for details.

## Links

- [dotOrigin Website](https://www.dotorigin.com/)
- [VTAP NFC Website](https://www.vtapnfc.com/)
- [VTAP Configuration Guide (PDF)](https://www.vtapnfc.com/downloads/VTAP_Configuration_Guide.pdf)
