# Plan: KBSource Bug Fix

## Problem

Die KBSource-Implementierung ist komplett falsch. Wir haben angenommen, dass KBSource Buchstabencodes wie "A", "G", "U" verwendet, aber die offizielle VTAP-Dokumentation zeigt, dass es **Hexadezimale Bitmasks** sind.

## Offizielle Dokumentation

Quelle: https://help.vtapnfc.com/en/Content/VTAP-Commands/Config-txt-KB-settings.htm

| Bit | Hex | Bedeutung |
|-----|-----|-----------|
| 7 | 0x80 | Mobile Pass (Apple VAS / Google Smart Tap) |
| 6 | 0x40 | STUID |
| 5 | 0x20 | Card Emulation Write Mode |
| 4 | 0x10 | RFU (Reserved) |
| 3 | 0x08 | RFU (Reserved) |
| 2 | 0x04 | Scanners |
| 1 | 0x02 | Command Interface Messages |
| 0 | 0x01 | Card/Tag UID |

**Beispiele:**
- `KBSource=80` → nur Mobile Passes (0x80)
- `KBSource=A1` → Passes + Cards + Card Emulation (0x80+0x20+0x01 = 0xA1)
- `KBSource=A5` → Default (0x80+0x20+0x04+0x01 = 0xA5)

## Aktueller (falscher) Code

```python
class KBSourceBuilder:
    _SOURCE_CODES = {
        "apple_vas": "A",      # FALSCH - A ist kein Code, sondern Hex-Digit
        "google_smarttap": "G", # FALSCH - G ist ungültig in Hex
        ...
    }
```

## Lösung

### 1. KBSourceBuilder komplett neu schreiben

```python
class KBSourceBuilder:
    """Builder for KBSource hex bitmask values."""

    MOBILE_PASS = 0x80      # Bit 7: Apple VAS / Google Smart Tap
    STUID = 0x40            # Bit 6: STUID
    CARD_EMULATION = 0x20   # Bit 5: Card Emulation Write Mode
    SCANNERS = 0x04         # Bit 2: Scanners
    COMMAND_INTERFACE = 0x02 # Bit 1: Command Interface
    CARD_TAG_UID = 0x01     # Bit 0: Card/Tag UID

    def __init__(self):
        self._value = 0

    def mobile_pass(self) -> "KBSourceBuilder":
        self._value |= self.MOBILE_PASS
        return self

    def card_tag_uid(self) -> "KBSourceBuilder":
        self._value |= self.CARD_TAG_UID
        return self

    # ... weitere Methoden

    def build(self) -> str:
        return f"{self._value:02X}"  # z.B. "A5"
```

### 2. KeyboardConfig.source Default korrigieren

Der Default `A5` ist korrekt (ist bereits Hex), aber die Beschreibung muss angepasst werden.

### 3. Dokumentation korrigieren

Dateien die korrigiert werden müssen:
- `docs/configuration/keyboard.md` - KBSourceBuilder API komplett neu
- `docs/configuration/overview.md` - KBSource Erklärung korrigieren
- `docs/configuration/settings_reference.md` - KBSource Tabelle korrigieren
- `docs/api.md` - API Beispiele korrigieren

### 4. Tests aktualisieren

Tests für KBSourceBuilder müssen die neuen Hex-Werte prüfen.

## Implementierungsreihenfolge

1. ✅ Plan schreiben
2. ✅ Tests für neuen KBSourceBuilder schreiben (TDD)
3. ✅ KBSourceBuilder in keyboard.py neu implementieren
4. ✅ Tests laufen lassen
5. ✅ Dokumentation korrigieren
6. ✅ TUI Help-Texte korrigieren
7. ✅ Commit

## Betroffene Dateien

| Datei | Änderung | Status |
|-------|----------|--------|
| `src/vtap100/models/keyboard.py` | KBSourceBuilder neu schreiben | ✅ |
| `tests/test_keyboard.py` | Tests anpassen | ✅ |
| `docs/configuration/keyboard.md` | Komplett überarbeiten | ✅ |
| `docs/configuration/overview.md` | KBSource Sektion korrigieren | ✅ |
| `docs/configuration/settings_reference.md` | KBSource Tabelle korrigieren | ✅ |
| `docs/api.md` | KBSourceBuilder Beispiel korrigieren | ✅ |
| `src/vtap100/tui/help/en/keyboard.yaml` | TUI Help korrigieren | ✅ |
| `src/vtap100/tui/help/de/keyboard.yaml` | TUI Help korrigieren | ✅ |
