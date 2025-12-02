# Entwickler-Guide

Dieses Dokument beschreibt die Entwicklungspraktiken für das VTAP100-Projekt.

## Entwicklungsumgebung einrichten

```bash
# Repository klonen
git clone <repository-url>
cd vtap100

# Dependencies installieren mit uv
uv sync --extra dev

# Oder mit pip
pip install -e ".[dev]"
```

## Test-Driven Development (TDD)

Dieses Projekt verwendet TDD. Der Workflow ist:

### 1. Red: Test schreiben

```python
# tests/unit/test_new_feature.py
def test_new_feature_does_something():
    from vtap100.new_module import new_function

    result = new_function("input")
    assert result == "expected_output"
```

### 2. Green: Implementation

```python
# src/vtap100/new_module.py
def new_function(input: str) -> str:
    return "expected_output"
```

### 3. Refactor

Code verbessern, Tests müssen weiter bestehen.

## Tests ausführen

```bash
# Alle Tests
uv run pytest

# Mit Coverage
uv run pytest --cov=vtap100 --cov-report=html

# Einzelne Test-Datei
uv run pytest tests/unit/test_models_vas.py -v

# Ohne Coverage-Check
uv run pytest --no-cov
```

## Code-Qualität

### Linting mit Ruff

```bash
# Prüfen
uv run ruff check src tests

# Automatisch fixen
uv run ruff check --fix src tests

# Formatieren
uv run ruff format src tests
```

### Type-Checking mit mypy

```bash
uv run mypy src
```

## Projektstruktur

```
vtap100/
├── src/vtap100/          # Quellcode
│   ├── models/           # Pydantic-Modelle
│   ├── generator.py      # config.txt Generator
│   ├── cli.py            # CLI mit Rich
│   └── templates/        # Vordefinierte Konfigurationen
├── tests/
│   ├── unit/             # Unit-Tests
│   ├── integration/      # Integrationstests
│   └── fixtures/         # Test-Daten
└── docs/                 # Dokumentation
```

## Docstring-Standard

Wir verwenden Google-Style Docstrings:

```python
def generate_config(config: VTAPConfig, output_path: Path) -> None:
    """Generate a VTAP100 config.txt file.

    Args:
        config: The VTAP configuration object containing all settings.
        output_path: Path where the config.txt will be written.

    Raises:
        ValidationError: If the configuration is invalid.
        FileExistsError: If output file exists and overwrite=False.

    Example:
        >>> config = VTAPConfig(vas=[AppleVASConfig(...)])
        >>> generate_config(config, Path("./config.txt"))
    """
```

## Neue Features hinzufügen

1. **Dokumentation schreiben:** Was soll das Feature tun?
2. **Tests schreiben:** Definiere das erwartete Verhalten
3. **Implementation:** Code schreiben bis Tests bestehen
4. **Dokumentation finalisieren:** Beispiele und API-Docs aktualisieren
5. **Changelog aktualisieren:** Änderungen dokumentieren

## Phasen-Übersicht

- **Phase 1 (aktuell):** Apple VAS, Google Smart Tap, Keyboard-Emulation
- **Phase 2:** Erweiterte Keyboard-Emulation
- **Phase 3:** NFC Tags
- **Phase 4:** MIFARE DESFire
- **Phase 5:** LED/Beep + Extras

## Ressourcen

- [VTAP Configuration Guide](https://www.vtapnfc.com/downloads/VTAP_Configuration_Guide.pdf)
- [Quellensammlung](references/sources.md)
- [Implementierungsplan](PLAN.md)
