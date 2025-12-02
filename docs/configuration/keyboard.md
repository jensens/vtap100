# Keyboard Emulation

Die Keyboard-Emulation ermöglicht es dem VTAP100, NFC-Daten als Tastatureingaben zu senden.

## Funktionsweise

Wenn aktiviert, verhält sich der VTAP100 wie eine USB-Tastatur und "tippt" die gelesenen Daten automatisch ein. Dies ist nützlich für:

- POS-Systeme ohne NFC-API
- Legacy-Anwendungen
- Schnelle Integration ohne Programmierung

## Parameter

### KBLogMode

Aktiviert oder deaktiviert die Keyboard-Emulation.

```ini
KBLogMode=1    ; Aktiviert
KBLogMode=0    ; Deaktiviert
```

### KBSource

Definiert welche Daten ausgegeben werden sollen. Der Wert ist ein Hex-String.

**Datenquellen:**
- `A` = Apple VAS Daten
- `G` = Google Smart Tap Daten
- `U` = UID der NFC-Karte/des Smartphones

**Datenmenge:**
- `1` = Erstes Byte
- `2` = Erste zwei Bytes
- `3` = Erste drei Bytes
- `4` = Erste vier Bytes
- `5` = Alle Bytes (vollständige Daten)

**Beispiele:**
```ini
KBSource=A1     ; Erstes Byte von Apple VAS
KBSource=G5     ; Alle Bytes von Google Smart Tap
KBSource=AG1    ; Erstes Byte von Apple und Google
KBSource=U1     ; Erstes Byte der UID
KBSource=AGU5   ; Alle Daten von allen Quellen
```

### KBEnable

Aktiviert oder deaktiviert das USB-Keyboard-Device.

```ini
KBEnable=1    ; USB-Keyboard aktiviert
KBEnable=0    ; USB-Keyboard deaktiviert
```

### KBPrefix

Optional: Präfix vor den Daten ausgeben.

```ini
KBPrefix=$t          ; Timestamp als Präfix
KBPrefix=%0A         ; Zeilenumbruch als Präfix
KBPrefix=ID:         ; Fester Text als Präfix
```

**Variablen:**
- `$t` - Aktueller Timestamp
- `%XX` - ASCII-Hex-Zeichen (z.B. `%0A` = Newline)

### KBPostfix

Suffix nach den Daten (Standard: `%0A` = Newline).

```ini
KBPostfix=%0A        ; Newline (Standard)
KBPostfix=%0D%0A     ; CRLF (Windows)
KBPostfix=%09        ; Tab
```

### KBDelayMS

Verzögerung zwischen Tastendrücken in Millisekunden (5-255).

```ini
KBDelayMS=5          ; Schnell (Standard)
KBDelayMS=50         ; Langsamer für ältere Systeme
KBDelayMS=100        ; Sehr langsam
```

### KBPassMode

Aktiviert die Extraktion aus dem Pass-Payload.

```ini
KBPassMode=1         ; Extraktion aktiviert
KBPassMode=0         ; Deaktiviert (Standard)
```

### KBPassSection

Welcher Abschnitt aus dem Payload extrahiert wird (bei aktiviertem PassMode).

```ini
KBPassSection=0      ; Erster Abschnitt (Standard)
KBPassSection=1      ; Zweiter Abschnitt
KBPassSection=2      ; Dritter Abschnitt
```

### KBPassSeparator

Trennzeichen zwischen Abschnitten im Payload.

```ini
KBPassSeparator=|    ; Pipe (Standard)
KBPassSeparator=;    ; Semikolon
KBPassSeparator=,    ; Komma
```

### KBPassStart / KBPassLength

Start-Position und Länge der Extraktion.

```ini
KBPassStart=0        ; Ab Anfang (Standard)
KBPassStart=10       ; Ab Position 10

KBPassLength=0       ; Alles (Standard)
KBPassLength=16      ; Nur 16 Zeichen
```

## CLI-Verwendung

```bash
# Mit Keyboard-Emulation (Standard)
vtap100 generate --apple-vas pass.com.example.test --keyboard

# Ohne Keyboard-Emulation
vtap100 generate --apple-vas pass.com.example.test --no-keyboard
```

## Python API

### Einfache Konfiguration

```python
from vtap100.models.keyboard import KeyboardConfig

kb = KeyboardConfig(
    log_mode=True,
    source="AG",
    enable=True
)

print(kb.to_config_lines())
# ['KBLogMode=1', 'KBSource=AG']
```

### Erweiterte Konfiguration

```python
from vtap100.models.keyboard import KeyboardConfig

kb = KeyboardConfig(
    log_mode=True,
    source="AG",
    prefix="$t:",           # Timestamp als Präfix
    postfix="%0D%0A",       # CRLF statt LF
    delay_ms=50,            # Langsamere Ausgabe
    pass_mode=True,         # Payload-Extraktion
    pass_section=1,         # Zweiter Abschnitt
    pass_separator=";",     # Semikolon-Trennung
    pass_length=32,         # Max 32 Zeichen
)

print(kb.to_config_lines())
# ['KBLogMode=1', 'KBSource=AG', 'KBPrefix=$t:', 'KBPostfix=%0D%0A',
#  'KBDelayMS=50', 'KBPassMode=1', 'KBPassSection=1',
#  'KBPassSeparator=;', 'KBPassLength=32']
```

### KBSource Builder

Für komplexere Konfigurationen gibt es einen Builder:

```python
from vtap100.models.keyboard import KBSourceBuilder

# Fluent API
source = (KBSourceBuilder()
    .apple_vas()
    .google_smarttap()
    .all_bytes()
    .build())

print(source)  # "AG5"

# Mit UID
source = (KBSourceBuilder()
    .uid()
    .first_byte()
    .build())

print(source)  # "U1"
```

### Builder-Methoden

**Datenquellen:**
- `.apple_vas()` - Apple VAS hinzufügen
- `.google_smarttap()` - Google Smart Tap hinzufügen
- `.uid()` - UID hinzufügen

**Datenmenge:**
- `.first_byte()` - Nur erstes Byte
- `.first_two_bytes()` - Erste zwei Bytes
- `.first_three_bytes()` - Erste drei Bytes
- `.first_four_bytes()` - Erste vier Bytes
- `.all_bytes()` - Alle Bytes

## Vollständiges Beispiel

```ini
!VTAPconfig
; Apple VAS Configuration
VAS1MerchantID=pass.com.example.myapp
VAS1KeySlot=1

; Google Smart Tap Configuration
ST1CollectorID=96972794
ST1KeySlot=2
ST1KeyVersion=1

; Keyboard Emulation - Alle Daten ausgeben
KBLogMode=1
KBSource=AG5
KBEnable=1
```

## Ausgabeformat

Die Daten werden als Hex-String ausgegeben, gefolgt von Enter:

```
A1B2C3D4E5F6<Enter>
```

## Anwendungsbeispiele

### POS-System Integration

```ini
; Nur Apple VAS Daten, erstes Byte
KBLogMode=1
KBSource=A1
```

### Logging/Debugging

```ini
; Alle verfügbaren Daten
KBLogMode=1
KBSource=AGU5
```

### UID-basierte Zugangskontrolle

```ini
; Nur UID ausgeben
KBLogMode=1
KBSource=U5
```

## Tipps

1. **Testen Sie zuerst mit `U1`** - Die UID ist immer verfügbar
2. **Für Produktiv-Systeme**: Verwenden Sie spezifische Quellen (A oder G), nicht alle
3. **Bei Problemen**: Prüfen Sie mit `KBSource=AGU5` welche Daten überhaupt ankommen

## Siehe auch

- [config.txt Format](overview.md)
- [Apple VAS Konfiguration](apple_vas.md)
- [Google Smart Tap Konfiguration](google_smarttap.md)
