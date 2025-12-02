# Developer Guide

This document describes the development practices for the VTAP100 project.

## Setting Up Development Environment

```bash
# Clone repository
git clone <repository-url>
cd vtap100

# Install dependencies with uv
uv sync --extra dev

# Or with pip
pip install -e ".[dev]"
```

## Test-Driven Development (TDD)

This project uses TDD. The workflow is:

### 1. Red: Write Test

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

Improve code while tests continue to pass.

## Running Tests

```bash
# All tests
uv run pytest

# With coverage
uv run pytest --cov=vtap100 --cov-report=html

# Single test file
uv run pytest tests/unit/test_models_vas.py -v

# Without coverage check
uv run pytest --no-cov
```

## Code Quality

### Linting with Ruff

```bash
# Check
uv run ruff check src tests

# Auto-fix
uv run ruff check --fix src tests

# Format
uv run ruff format src tests
```

### Type Checking with mypy

```bash
uv run mypy src
```

## Project Structure

```
vtap100/
├── src/vtap100/          # Source code
│   ├── models/           # Pydantic models
│   ├── generator.py      # config.txt generator
│   ├── cli.py            # CLI with Rich
│   └── templates/        # Predefined configurations
├── tests/
│   ├── unit/             # Unit tests
│   ├── integration/      # Integration tests
│   └── fixtures/         # Test data
└── docs/                 # Documentation
```

## Docstring Standard

We use Google-style docstrings:

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

## Adding New Features

1. **Write documentation:** What should the feature do?
2. **Write tests:** Define expected behavior
3. **Implementation:** Write code until tests pass
4. **Finalize documentation:** Update examples and API docs
5. **Update changelog:** Document changes

## Phase Overview

- **Phase 1 (current):** Apple VAS, Google Smart Tap, Keyboard Emulation
- **Phase 2:** Extended Keyboard Emulation
- **Phase 3:** NFC Tags
- **Phase 4:** MIFARE DESFire
- **Phase 5:** LED/Beep + Extras

## Resources

- [VTAP Configuration Guide](https://www.vtapnfc.com/downloads/VTAP_Configuration_Guide.pdf)
- [Reference Sources](references/sources.md)
- [Implementation Plan](PLAN.md)
