# PLAN: KBSource Checkbox-basierte Bitmask-Auswahl

**Status:** Implementiert

## Zusammenfassung

Ersetze das manuelle Hex-Input-Feld für KBSource durch eine benutzerfreundliche Checkbox-Gruppe. Der Hex-Wert wird automatisch berechnet und live angezeigt.

## Geänderte Dateien

| Datei | Änderung |
|-------|----------|
| `src/vtap100/models/keyboard.py` | Neue Funktionen `parse_kbsource_hex()` und `build_kbsource_from_flags()` |
| `src/vtap100/tui/widgets/forms/keyboard.py` | Input → 6 Switches + Hex-Anzeige |
| `tests/unit/test_models_keyboard.py` | TDD Tests für neue Funktionen |
| `src/vtap100/tui/i18n/translations/de.yaml` | Deutsche Labels für Checkboxen |
| `src/vtap100/tui/i18n/translations/en.yaml` | Englische Labels für Checkboxen |
| `src/vtap100/tui/help/de/keyboard.yaml` | Deutsche Hilfe-Texte |
| `src/vtap100/tui/help/en/keyboard.yaml` | Englische Hilfe-Texte |

## KBSource Bit-Definitionen

```
MOBILE_PASS      = 0x80  # Bit 7: Apple VAS / Google Smart Tap
STUID            = 0x40  # Bit 6: STUID
CARD_EMULATION   = 0x20  # Bit 5: Card Emulation Write Mode
SCANNERS         = 0x04  # Bit 2: Scanners
COMMAND_INTERFACE = 0x02  # Bit 1: Command Interface Messages
CARD_TAG_UID     = 0x01  # Bit 0: Card/Tag UID
```

## UI-Änderungen

Das Keyboard-Formular zeigt jetzt 6 Switches statt eines Text-Inputs:

```
Datenquellen (KBSource)
┌────────────────────────────────┐
│ Mobile Pass (VAS/SmartTap)  [X]│
│ STUID                       [ ]│
│ Card Emulation Write Mode   [X]│
│ Scanner                     [X]│
│ Command Interface           [ ]│
│ Card/Tag UID                [X]│
└────────────────────────────────┘
KBSource = A5
```

Die Hex-Anzeige aktualisiert sich live bei jeder Switch-Änderung.

## Architektur-Entscheidungen

- **Switch statt Checkbox**: Konsistent mit dem bestehenden TUI-Design
- **Vertikales Layout**: Alle 6 Optionen in einem Container
- **Live Hex-Anzeige**: Aktualisiert sich bei jeder Switch-Änderung
- **Bidirektionale Konvertierung**: Laden und Speichern funktioniert transparent
- **Help-Panel Support**: Switches triggern jetzt auch Help-Context-Updates
