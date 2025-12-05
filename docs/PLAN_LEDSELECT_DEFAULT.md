# Plan: LEDSelect Default auf 1 setzen

## Hintergrund
LEDSelect soll standardmäßig auf `1` (ONBOARD_COMPACT) gesetzt werden, damit die Konfiguration ohne manuelle Modifikation funktioniert.

## Aktuelle Situation
- `LEDSelect` Enum definiert in `src/vtap100/models/feedback.py`
- Im `LEDConfig` Model war `select: LEDSelect | None = Field(default=None)`
- In der TUI wurde `LEDSelect.EXTERNAL (0)` als Fallback verwendet

## Umgesetzte Änderungen

### 1. Model Default geändert
**Datei:** `src/vtap100/models/feedback.py`
- `LEDConfig.select` Default von `None` auf `LEDSelect.ONBOARD_COMPACT` geändert
- `to_config_lines()` gibt jetzt immer `LEDSelect=1` aus

### 2. TUI Fallback angepasst
**Datei:** `src/vtap100/tui/widgets/forms/feedback.py`
- Fallback von `LEDSelect.EXTERNAL` auf `LEDSelect.ONBOARD_COMPACT` geändert

### 3. Parser angepasst
**Datei:** `src/vtap100/parser.py`
- Fallback bei `_build_led_config()` auf `LEDSelect.ONBOARD_COMPACT` geändert

### 4. Tests aktualisiert
**Datei:** `tests/unit/test_models_feedback.py`
- `test_led_config_defaults`: Erwartet jetzt `LEDSelect.ONBOARD_COMPACT`
- `test_to_config_lines_empty` → `test_to_config_lines_default`: Erwartet `["LEDSelect=1"]`

## Status
Umgesetzt und committed am 2025-12-05.
