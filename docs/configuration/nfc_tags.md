# NFC Tag Konfiguration

Der VTAP100 kann verschiedene NFC-Tag-Typen lesen: Type 2, Type 4 und Type 5.

## Tag-Typen

### NFC Type 2

Typische Tags: NTAG213/215/216, MIFARE Ultralight

```ini
NFCType2=U    ; UID lesen
NFCType2=N    ; NDEF Records lesen
NFCType2=B    ; Block-Daten lesen
NFCType2=0    ; Deaktiviert (Standard)
```

### NFC Type 4

Typische Tags: DESFire, ISO 14443-4 kompatibel

```ini
NFCType4=U    ; UID lesen
NFCType4=N    ; NDEF Records lesen
NFCType4=B    ; Block-Daten lesen
NFCType4=D    ; DESFire secure data
NFCType4=0    ; Deaktiviert (Standard)
```

### NFC Type 5

Typische Tags: ICODE, ISO 15693

```ini
NFCType5=U    ; UID lesen
NFCType5=N    ; NDEF Records lesen
NFCType5=B    ; Block-Daten lesen
NFCType5=0    ; Deaktiviert (Standard)
```

## Lese-Modi

| Modus | Wert | Beschreibung |
|-------|------|--------------|
| Disabled | 0 | Tag-Typ deaktiviert |
| UID | U | Nur UID lesen |
| NDEF | N | NDEF Records lesen |
| Block | B | Raw Block-Daten lesen |
| DESFire | D | DESFire secure data (nur Type 4) |

## Zusätzliche Parameter

### NFCReportReadError

Fehler-Payload bei Lesefehlern ausgeben.

```ini
NFCReportReadError=1    ; Fehler melden
NFCReportReadError=0    ; Ignorieren (Standard)
```

### IgnoreRandomUID

Zufällige Type 4 UIDs filtern (z.B. von Smartphones).

```ini
IgnoreRandomUID=1    ; Zufällige UIDs ignorieren
IgnoreRandomUID=0    ; Alle UIDs akzeptieren (Standard)
```

### TagByteOrder

Byte-Reihenfolge umkehren.

```ini
TagByteOrder=1    ; Bytes umkehren
TagByteOrder=0    ; Normal (Standard)
```

## Block-Daten lesen

Für den Block-Modus (B) gibt es weitere Parameter:

### TagReadBlockNum

Block-Nummer zum Lesen (0-255).

```ini
TagReadBlockNum=4    ; Block 4 lesen
```

### TagReadKeySlot

Key-Slot für Authentifizierung (1-9).

```ini
TagReadKeySlot=1    ; Key aus Slot 1 verwenden
```

### TagReadKeyType

Key-Typ für MIFARE (A, B, oder C).

```ini
TagReadKeyType=A    ; Key Typ A
TagReadKeyType=B    ; Key Typ B
```

### TagReadOffset

Start-Byte im Block (0-15).

```ini
TagReadOffset=0     ; Ab Anfang (Standard)
TagReadOffset=4     ; Ab Byte 4
```

### TagReadLength

Anzahl zu lesender Bytes (1-16).

```ini
TagReadLength=4     ; 4 Bytes lesen
TagReadLength=16    ; Ganzen Block lesen
```

### TagReadFormat

Ausgabeformat.

```ini
TagReadFormat=h     ; Hexadezimal
TagReadFormat=d     ; Dezimal
TagReadFormat=a     ; ASCII
```

### TagReadMinDigits

Minimale Ziffern für UID-Ausgabe.

```ini
TagReadMinDigits=10    ; Mindestens 10 Ziffern
TagReadMinDigits=A     ; Automatisch
```

## Python API

### Einfache Konfiguration

```python
from vtap100.models.nfc import NFCTagConfig, NFCTagMode

# Type 2 und Type 4 im UID-Modus aktivieren
nfc = NFCTagConfig(
    type2=NFCTagMode.UID,
    type4=NFCTagMode.UID,
)

print(nfc.to_config_lines())
# ['NFCType2=U', 'NFCType4=U']
```

### Block-Daten lesen

```python
from vtap100.models.nfc import (
    NFCTagConfig, NFCTagMode,
    TagReadConfig, TagKeyType, TagReadFormat
)

# MIFARE Block lesen
tag_read = TagReadConfig(
    block_num=4,
    key_slot=1,
    key_type=TagKeyType.A,
    length=16,
    format=TagReadFormat.HEX,
)

nfc = NFCTagConfig(
    type2=NFCTagMode.BLOCK,
    tag_read=tag_read,
)

print(nfc.to_config_lines())
# ['NFCType2=B', 'TagReadBlockNum=4', 'TagReadKeySlot=1',
#  'TagReadKeyType=A', 'TagReadLength=16', 'TagReadFormat=h']
```

### Mit VTAPConfig kombinieren

```python
from vtap100.models.config import VTAPConfig
from vtap100.models.nfc import NFCTagConfig, NFCTagMode
from vtap100.models.keyboard import KeyboardConfig
from vtap100.generator import ConfigGenerator

# NFC + Keyboard kombinieren
nfc = NFCTagConfig(
    type2=NFCTagMode.UID,
    type4=NFCTagMode.NDEF,
    ignore_random_uid=True,
)

kb = KeyboardConfig(
    log_mode=True,
    source="24",  # Type 2 und Type 4
)

config = VTAPConfig(nfc=nfc, keyboard=kb)

generator = ConfigGenerator(config)
print(generator.generate())
```

## Vollständiges Beispiel

```ini
!VTAPconfig
; NFC Tag Settings
NFCType2=U
NFCType4=N
IgnoreRandomUID=1

; Keyboard Emulation
KBLogMode=1
KBSource=24
```

## Siehe auch

- [config.txt Format](overview.md)
- [Keyboard-Emulation](keyboard.md)
- [MIFARE DESFire](desfire.md) *(Phase 4)*
