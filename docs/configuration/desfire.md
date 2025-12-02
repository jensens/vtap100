# MIFARE DESFire Konfiguration

Der VTAP100 kann MIFARE DESFire Karten lesen und authentifizierte Daten auslesen.

## Grundlagen

DESFire ist ein kontaktloser Smartcard-Typ von NXP mit Verschlüsselungsfunktionen.
Der VTAP100 unterstützt bis zu 9 DESFire-Anwendungskonfigurationen.

## Parameter

### DESFire#AppID

Application ID der DESFire-Anwendung (6 Hex-Zeichen).

```ini
DESFire1AppID=AABBCC
DESFire2AppID=112233
```

### DESFire#FileID

File ID zum Lesen (1-255).

```ini
DESFire1FileID=1
```

### DESFire#KeyNum

Key-Nummer für Authentifizierung.

```ini
DESFire1KeyNum=0
```

### DESFire#KeySlot

Key-Slot für Authentifizierung (1-9).

```ini
DESFire1KeySlot=1
```

### DESFire#Crypto

Kryptographischer Modus.

```ini
DESFire1Crypto=0    ; Keine Verschlüsselung
DESFire1Crypto=1    ; 3DES
DESFire1Crypto=3    ; AES
```

| Wert | Modus |
|------|-------|
| 0 | Keine Verschlüsselung |
| 1 | 3DES |
| 3 | AES |

### DESFire#Format

Daten-Ausgabeformat.

```ini
DESFire1Format=0    ; Raw-Daten
DESFire1Format=1    ; KEY-ID v1
DESFire1Format=2    ; KEY-ID v2
```

| Wert | Format |
|------|--------|
| 0 | Raw-Daten |
| 1 | KEY-ID v1 |
| 2 | KEY-ID v2 |

### DESFire#ReadLength

Anzahl zu lesender Bytes (1-255, Standard: 3).

```ini
DESFire1ReadLength=16
```

### DESFire#ReadOffset

Start-Offset im File (0-255, Standard: 0).

```ini
DESFire1ReadOffset=4
```

### DESFire#Diversification

Key-Diversifizierung aktivieren.

```ini
DESFire1Diversification=1    ; Aktiviert
```

### DESFireSeparator

Trennzeichen für mehrere Apps (Standard: `,`).

```ini
DESFireSeparator=;
```

## Python API

### Einfache Konfiguration

```python
from vtap100.models.desfire import DESFireConfig, DESFireAppConfig

# Einzelne DESFire-App
app = DESFireAppConfig(
    app_id="AABBCC",
    file_id=1,
    key_slot=1,
)

config = DESFireConfig(apps=[app])
print(config.to_config_lines())
# ['DESFire1AppID=AABBCC', 'DESFire1FileID=1', 'DESFire1KeySlot=1']
```

### Mit Verschlüsselung

```python
from vtap100.models.desfire import (
    DESFireConfig,
    DESFireAppConfig,
    DESFireCryptoMode,
    DESFireDataFormat,
)

app = DESFireAppConfig(
    app_id="AABBCC",
    file_id=1,
    key_num=0,
    key_slot=1,
    crypto=DESFireCryptoMode.AES,
    format=DESFireDataFormat.KEYID_V1,
    read_length=16,
)

config = DESFireConfig(apps=[app])
print(config.to_config_lines())
# ['DESFire1AppID=AABBCC', 'DESFire1FileID=1', 'DESFire1KeyNum=0',
#  'DESFire1KeySlot=1', 'DESFire1Crypto=3', 'DESFire1Format=1',
#  'DESFire1ReadLength=16']
```

### Mehrere Apps

```python
from vtap100.models.desfire import DESFireConfig, DESFireAppConfig

apps = [
    DESFireAppConfig(app_id="111111", file_id=1),
    DESFireAppConfig(app_id="222222", file_id=2),
    DESFireAppConfig(app_id="333333", file_id=3),
]

config = DESFireConfig(apps=apps, separator=";")
print(config.to_config_lines())
# ['DESFire1AppID=111111', 'DESFire1FileID=1',
#  'DESFire2AppID=222222', 'DESFire2FileID=2',
#  'DESFire3AppID=333333', 'DESFire3FileID=3',
#  'DESFireSeparator=;']
```

### Mit VTAPConfig kombinieren

```python
from vtap100.models.config import VTAPConfig
from vtap100.models.desfire import DESFireConfig, DESFireAppConfig, DESFireCryptoMode
from vtap100.models.keyboard import KeyboardConfig
from vtap100.generator import ConfigGenerator

# DESFire + Keyboard kombinieren
desfire = DESFireConfig(
    apps=[
        DESFireAppConfig(
            app_id="AABBCC",
            file_id=1,
            key_slot=1,
            crypto=DESFireCryptoMode.AES,
        )
    ]
)

kb = KeyboardConfig(
    log_mode=True,
    source="D1",  # DESFire App 1
)

config = VTAPConfig(desfire=desfire, keyboard=kb)

generator = ConfigGenerator(config)
print(generator.generate())
```

## Vollständiges Beispiel

```ini
!VTAPconfig
; MIFARE DESFire Settings
DESFire1AppID=AABBCC
DESFire1FileID=1
DESFire1KeyNum=0
DESFire1KeySlot=1
DESFire1Crypto=3
DESFire1ReadLength=16

; Keyboard Emulation
KBLogMode=1
KBSource=D1
```

## Siehe auch

- [config.txt Format](overview.md)
- [Keyboard-Emulation](keyboard.md)
- [NFC Tags](nfc_tags.md)
