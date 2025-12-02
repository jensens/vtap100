# Google Smart Tap Konfiguration

Google Smart Tap ermöglicht das Auslesen von Google Wallet Pässen über NFC.

## Voraussetzungen

1. Ein Google Pay & Wallet Console Account
2. Ein Collector ID (von Google bereitgestellt)
3. Ein ECDSA-Schlüsselpaar für die Authentifizierung
4. Der öffentliche Schlüssel muss bei Google registriert sein

## Parameter

### ST#CollectorID

Die von Google zugewiesene Collector ID.

```ini
ST1CollectorID=96972794
```

### ST#KeySlot

Der Slot (1-6) in dem der private Schlüssel gespeichert ist.

```ini
ST1KeySlot=2
```

Der Wert 0 bedeutet automatische Auswahl.

### ST#KeyVersion

Die Versionsnummer des verwendeten Schlüssels.

```ini
ST1KeyVersion=1
```

## Vollständiges Beispiel

```ini
!VTAPconfig
; Google Smart Tap Configuration
ST1CollectorID=96972794
ST1KeySlot=2
ST1KeyVersion=1

; Keyboard Emulation für Smart Tap Daten
KBLogMode=1
KBSource=G1
```

## CLI-Verwendung

### Einfache Konfiguration

```bash
vtap100 generate --google-st 96972794 --key-slot 2 --key-version 1
```

### Mit Apple VAS kombiniert

```bash
vtap100 generate \
    --google-st 96972794 \
    --apple-vas pass.com.example.myapp \
    --key-slot 1
```

### Interaktiver Wizard

```bash
vtap100 wizard
```

## Python API

```python
from vtap100.models.smarttap import GoogleSmartTapConfig
from vtap100.models.config import VTAPConfig
from vtap100.generator import ConfigGenerator

# Smart Tap Konfiguration erstellen
st = GoogleSmartTapConfig(
    collector_id="96972794",
    key_slot=2,
    key_version=1
)

# Vollständige Konfiguration
config = VTAPConfig(smarttap_configs=[st])

# config.txt generieren
generator = ConfigGenerator(config)
print(generator.generate())
```

## Mehrere Collector IDs

Es können bis zu 6 verschiedene Collector IDs konfiguriert werden:

```ini
!VTAPconfig
ST1CollectorID=96972794
ST1KeySlot=1
ST1KeyVersion=1

ST2CollectorID=12345678
ST2KeySlot=2
ST2KeyVersion=1
```

## Smart Tap Daten auslesen

Mit aktivierter Keyboard-Emulation werden die Smart Tap Daten automatisch ausgegeben:

```ini
KBLogMode=1
KBSource=G5    ; Alle Bytes von Google Smart Tap
```

## Default Passes

Zusätzlich zu eigenen Collector IDs können Standard-Pässe aktiviert werden:

```python
from vtap100.models.smarttap import SmartTapDefaultPassesConfig

defaults = SmartTapDefaultPassesConfig(
    loyalty=True,      # Loyalty-Karten
    gift_card=True,    # Geschenkkarten
    offer=True,        # Angebote
    transit=False,     # Nahverkehr
    event_ticket=True, # Event-Tickets
    flight=True,       # Flugtickets
    boarding=True      # Boarding-Pässe
)
```

## Fehlerbehebung

### "No Smart Tap data received"

- Prüfen Sie die Collector ID
- Stellen Sie sicher, dass der private Key im richtigen Slot liegt
- Prüfen Sie, ob die Key Version übereinstimmt

### "Authentication failed"

- Der öffentliche Schlüssel ist möglicherweise nicht bei Google registriert
- Die Key Version stimmt nicht überein

## Siehe auch

- [config.txt Format](overview.md)
- [Apple VAS Konfiguration](apple_vas.md)
- [Keyboard Emulation](keyboard.md)
- [Quellensammlung](../references/sources.md)
