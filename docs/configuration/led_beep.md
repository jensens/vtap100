# LED und Beep Konfiguration

Der VTAP100 bietet visuelles (LED) und akustisches (Beep) Feedback für verschiedene Ereignisse.

## LED Einstellungen

### LEDMode

LED-Betriebsmodus.

```ini
LEDMode=0    ; LEDs aus
LEDMode=1    ; LEDs an
LEDMode=2    ; Status-Anzeige
LEDMode=3    ; Benutzerdefinierte Sequenzen
```

| Wert | Modus | Beschreibung |
|------|-------|--------------|
| 0 | OFF | LEDs deaktiviert |
| 1 | ON | LEDs aktiviert |
| 2 | STATUS | Status-Indikator |
| 3 | CUSTOM | Benutzerdefinierte Sequenzen |

### LEDSelect

LED-Typ/Position auswählen.

```ini
LEDSelect=0    ; Externe RGB LED (common cathode)
LEDSelect=1    ; On-board LED (compact case)
LEDSelect=2    ; On-board LED (square case)
LEDSelect=3    ; Serial LEDs
```

| Wert | Typ |
|------|-----|
| 0 | Externe RGB LED |
| 1 | On-board (Compact) |
| 2 | On-board (Square) |
| 3 | Serial LEDs |

### LEDDefaultRGB

Standard-Farbe für LEDs (6 Hex-Zeichen).

```ini
LEDDefaultRGB=FFFFFF    ; Weiß
LEDDefaultRGB=00FF00    ; Grün
LEDDefaultRGB=FF0000    ; Rot
```

### LED Sequenzen

Für Pass-Read, Tag-Read, Fehler und Start können LED-Sequenzen definiert werden.

**Format:** `RRGGBB,on_ms,off_ms,repeats`

| Parameter | Bereich | Beschreibung |
|-----------|---------|--------------|
| RRGGBB | Hex | Farbe (6 Zeichen) |
| on_ms | 0-65535 | An-Zeit in ms |
| off_ms | 0-65535 | Aus-Zeit in ms |
| repeats | 1-255 | Wiederholungen |

```ini
; Grünes Blinken bei Pass-Read (2x, 100ms an/aus)
PassLED=00FF00,100,100,2

; Blaue LED bei Tag-Read
TagLED=0000FF,100,100,1

; Rotes Blinken bei Fehler (3x schnell)
PassErrorLED=FF0000,50,50,3

; Gelbe LED beim Start
StartLED=FFFF00,500,0,1
```

## Beep/Buzzer Einstellungen

Für Pass-Read, Tag-Read, Fehler und Start können Beep-Sequenzen definiert werden.

**Format:** `on_ms,off_ms,repeats[,frequency]`

| Parameter | Bereich | Beschreibung |
|-----------|---------|--------------|
| on_ms | 0-65535 | An-Zeit in ms |
| off_ms | 0-65535 | Aus-Zeit in ms |
| repeats | 1-255 | Wiederholungen |
| frequency | 100-20000 | Frequenz in Hz (optional, Standard: 3136) |

```ini
; 2 Beeps bei Pass-Read
PassBeep=100,100,2

; Kurzer Beep bei Tag-Read
TagBeep=50,50,1

; 3 Beeps bei Fehler (tieferer Ton)
PassErrorBeep=200,100,3,2000

; Langer Beep beim Start
StartBeep=500,0,1
```

## Python API

### LED Konfiguration

```python
from vtap100.models.feedback import (
    FeedbackConfig,
    LEDConfig,
    LEDMode,
    LEDSelect,
    LEDSequence,
)

# LED Grundeinstellungen
led = LEDConfig(
    mode=LEDMode.CUSTOM,
    select=LEDSelect.ONBOARD_COMPACT,
    default_rgb="FFFFFF",
)

print(led.to_config_lines())
# ['LEDMode=3', 'LEDSelect=1', 'LEDDefaultRGB=FFFFFF']
```

### LED Sequenzen

```python
from vtap100.models.feedback import LEDConfig, LEDSequence

led = LEDConfig(
    pass_led=LEDSequence(color="00FF00", on_ms=100, off_ms=100, repeats=2),
    tag_led=LEDSequence(color="0000FF"),
    pass_error_led=LEDSequence(color="FF0000", on_ms=50, off_ms=50, repeats=3),
)

print(led.to_config_lines())
# ['PassLED=00FF00,100,100,2', 'TagLED=0000FF,100,100,1',
#  'PassErrorLED=FF0000,50,50,3']
```

### Beep Konfiguration

```python
from vtap100.models.feedback import BeepConfig, BeepSequence

beep = BeepConfig(
    pass_beep=BeepSequence(on_ms=100, off_ms=100, repeats=2),
    tag_beep=BeepSequence(on_ms=50, off_ms=50, repeats=1),
    pass_error_beep=BeepSequence(on_ms=200, off_ms=100, repeats=3, frequency=2000),
)

print(beep.to_config_lines())
# ['PassBeep=100,100,2', 'TagBeep=50,50,1', 'PassErrorBeep=200,100,3,2000']
```

### Kombinierte Konfiguration

```python
from vtap100.models.feedback import (
    FeedbackConfig,
    LEDConfig,
    LEDMode,
    LEDSequence,
    BeepConfig,
    BeepSequence,
)

feedback = FeedbackConfig(
    led=LEDConfig(
        mode=LEDMode.CUSTOM,
        pass_led=LEDSequence(color="00FF00", repeats=2),
    ),
    beep=BeepConfig(
        pass_beep=BeepSequence(repeats=2),
    ),
)

print(feedback.to_config_lines())
# ['LEDMode=3', 'PassLED=00FF00,100,100,2', 'PassBeep=100,100,2']
```

### Mit VTAPConfig kombinieren

```python
from vtap100.models.config import VTAPConfig
from vtap100.models.feedback import (
    FeedbackConfig,
    LEDConfig,
    LEDMode,
    LEDSequence,
    BeepConfig,
    BeepSequence,
)
from vtap100.models.vas import AppleVASConfig
from vtap100.generator import ConfigGenerator

# Komplette Konfiguration
feedback = FeedbackConfig(
    led=LEDConfig(
        mode=LEDMode.CUSTOM,
        pass_led=LEDSequence(color="00FF00", repeats=2),
        pass_error_led=LEDSequence(color="FF0000", repeats=3),
    ),
    beep=BeepConfig(
        pass_beep=BeepSequence(repeats=2),
        pass_error_beep=BeepSequence(on_ms=200, repeats=3),
    ),
)

vas = AppleVASConfig(merchant_id="pass.com.example.mypass", key_slot=1)

config = VTAPConfig(
    vas_configs=[vas],
    feedback=feedback,
)

generator = ConfigGenerator(config)
print(generator.generate())
```

## Vollständiges Beispiel

```ini
!VTAPconfig
; Apple VAS Configuration
VAS1MerchantID=pass.com.example.mypass
VAS1KeySlot=1

; LED/Beep Settings
LEDMode=3
LEDSelect=1
PassLED=00FF00,100,100,2
PassErrorLED=FF0000,50,50,3
PassBeep=100,100,2
PassErrorBeep=200,100,3,2000
```

## Tipps

- **LEDMode=3** ist erforderlich für benutzerdefinierte LED-Sequenzen
- Beep-Frequenz ist optional, Standard ist 3136 Hz
- Kurze Zeiten (50-100ms) für schnelles Feedback
- Längere Zeiten (200-500ms) für deutlichere Signale

## Siehe auch

- [config.txt Format](overview.md)
- [Apple VAS](apple_vas.md)
- [Google Smart Tap](google_smarttap.md)
