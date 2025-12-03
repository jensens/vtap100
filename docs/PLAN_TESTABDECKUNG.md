# Plan: Testabdeckung auf 85-90% erhöhen

## Ergebnis
- **Ausgangslage:** 75.47%
- **Erreicht:** 85.79%
- **Status:** ABGESCHLOSSEN

## Änderungen
1. Neue Testdatei: `tests/unit/test_cli.py` (39 Tests)
2. Neue Testdatei: `tests/unit/test_tui_forms_extended.py` (12 Tests)
3. Neue Testdatei: `tests/unit/test_tui_app_extended.py` (11 Tests)
4. Erweitert: `tests/unit/test_models_keyboard.py` (8 neue Tests)
5. Fixture für Sprach-Reset: `tests/conftest.py`

---

## Ursprünglicher Plan

## Aktueller Stand
- **Aktuelle Abdeckung:** 75.47%
- **Ziel:** 85-90%
- **Fehlende Statements:** ca. 260-330

## Prioritätsliste

### 1. cli.py (HÖCHSTE PRIORITÄT)
**Aktuell:** 12% (293 fehlende Statements)
**Ziel:** 80%+

#### Zu testen:
- [ ] `print_header()`, `print_config_preview()`, `print_success()`, `print_error()`, `print_section()` - Hilfsfunktionen
- [ ] `generate` Command - mit verschiedenen Optionen (Apple VAS, Google ST, kombiniert)
- [ ] `validate` Command - gültige und ungültige Dateien
- [ ] `docs` Command - Dokumentationsausgabe
- [ ] `editor` Command - TUI-Start

#### Strategie:
- Click's `CliRunner` für CLI-Tests verwenden
- Mocking für `Console` output wo nötig
- Temporäre Dateien für `validate` Tests

### 2. tui/widgets/forms/smarttap.py (HOHE PRIORITÄT)
**Aktuell:** 66% (36 fehlende Statements)
**Ziel:** 90%+

#### Fehlende Zeilen (Beispiele):
- Zeilen 204-213, 223-225: Form-Validierung
- Zeilen 240-264: Event Handler

### 3. tui/widgets/forms/desfire.py (HOHE PRIORITÄT)
**Aktuell:** 70% (35 fehlende Statements)
**Ziel:** 90%+

#### Fehlende Zeilen:
- Zeilen 282-291, 317-356: App-Verwaltung, Validierung

### 4. tui/app.py (MITTLERE PRIORITÄT)
**Aktuell:** 74% (30 fehlende Statements)
**Ziel:** 85%+

#### Fehlende Zeilen:
- Zeilen 89-91, 162-175: App-Lifecycle
- Zeilen 196-216: Screen-Handling

### 5. tui/widgets/forms/feedback.py (MITTLERE PRIORITÄT)
**Aktuell:** 65% (20 fehlende Statements)
**Ziel:** 85%+

#### Fehlende Zeilen:
- Zeilen 156-194: LED/Beep Konfiguration

### 6. models/keyboard.py (NIEDRIGE PRIORITÄT)
**Aktuell:** 76% (15 fehlende Statements)
**Ziel:** 90%+

#### Fehlende Zeilen:
- Zeilen 204-266: Source-Validierung Edge Cases

## Implementierungsreihenfolge

1. **Schritt 1:** cli.py Tests (größter Impact)
   - Neue Testdatei: `tests/unit/test_cli.py`
   - Erwarteter Gewinn: ~200 Statements → +9% Coverage

2. **Schritt 2:** Form-Widget Tests erweitern
   - smarttap.py, desfire.py, feedback.py
   - Erwarteter Gewinn: ~70 Statements → +3% Coverage

3. **Schritt 3:** App-Tests erweitern
   - tui/app.py
   - Erwarteter Gewinn: ~25 Statements → +1% Coverage

4. **Schritt 4:** Model-Tests erweitern
   - keyboard.py
   - Erwarteter Gewinn: ~15 Statements → +0.7% Coverage

## Erwartetes Ergebnis
Nach allen Schritten: **~89% Testabdeckung**

## Hinweise
- TDD: Erst Tests schreiben, dann Code anpassen falls nötig
- `wizard` Command ist stark interaktiv - hier ist Mocking komplex
- Für TUI-Tests: `textual.testing` verwenden (bereits im Einsatz)
