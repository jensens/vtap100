# VTAP100 Configuration Generator

Ein Python-Tool zur Generierung von Konfigurationsdateien für den **dotOrigin VTAP100** NFC Reader.

## Features

- **Apple VAS** (Value Added Services) Konfiguration
- **Google Smart Tap** Konfiguration
- **Keyboard-Emulation** Einstellungen
- **NFC Tag** Unterstützung (Type 2, 4, 5)
- **MIFARE DESFire** Konfiguration
- **LED/Buzzer** Feedback-Einstellungen
- **Validierung** aller Parameter
- **Rich CLI** mit farbiger Ausgabe

## Installation

```bash
# Mit uv (empfohlen)
uv sync

# Entwicklungsabhängigkeiten
uv sync --extra dev

# Alternativ mit pip
pip install -e ".[dev]"
```

## Schnellstart

### Apple VAS Konfiguration

```bash
vtap100 generate --apple-vas pass.com.example.mypass --key-slot 1 --output ./config.txt
```

### Google Smart Tap Konfiguration

```bash
vtap100 generate --google-st 96972794 --key-slot 2 --key-version 1 --output ./config.txt
```

### Interaktiver Modus

```bash
vtap100 wizard
```

### Konfiguration validieren

```bash
vtap100 validate ./config.txt
```

## Dokumentation

Ausführliche Dokumentation findest du im [docs/](docs/) Verzeichnis:

- [Schnelleinstieg](docs/quickstart.md)
- [Apple VAS Konfiguration](docs/configuration/apple_vas.md)
- [Google Smart Tap Konfiguration](docs/configuration/google_smarttap.md)
- [Keyboard-Emulation](docs/configuration/keyboard.md)
- [Deployment auf den Reader](docs/deployment/upload_to_reader.md)
- [Quellensammlung](docs/references/sources.md)

## Entwicklung

Dieses Projekt verwendet **Test-Driven Development (TDD)**.

```bash
# Tests ausführen
uv run pytest

# Mit Coverage
uv run pytest --cov=vtap100 --cov-report=html

# Linting
uv run ruff check src tests
uv run ruff format src tests

# Type-Checking
uv run mypy src
```

## Lizenz

MIT License - siehe [LICENSE](LICENSE) für Details.

## Links

- [dotOrigin Website](https://www.dotorigin.com/)
- [VTAP NFC Website](https://www.vtapnfc.com/)
- [VTAP Configuration Guide (PDF)](https://www.vtapnfc.com/downloads/VTAP_Configuration_Guide.pdf)
