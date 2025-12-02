# Apple VAS Konfiguration

Apple VAS (Value Added Services) ermöglicht das Lesen von Apple Wallet Pässen
über NFC. Der VTAP100 ist von Apple zertifiziert für VAS-Transaktionen.

## Voraussetzungen

1. Apple Developer Account
2. Apple Wallet NFC-Zertifikat (Pass Type ID)
3. Private Key im PEM-Format

## Parameter

| Parameter | Werte | Default | Beschreibung |
|-----------|-------|---------|--------------|
| VAS#MerchantID | String | - | **Pflicht.** Apple Pass Type ID (z.B. `pass.com.company.passname`) |
| VAS#KeySlot | 0-6 | 0 | Slot der private#.pem Datei (0=auto) |
| VAS#MerchantURL | URL | - | Optional: URL für Pass-Präsentation |
| VASDefaultPassesEnabled | Liste | 1,2,3,4,5,6 | Aktive VAS-Konfigurationen |

*`#` = Slot-Nummer 1-6 für bis zu 6 verschiedene Pass-Typen*

## CLI Beispiele

### Einfache Konfiguration

```bash
vtap100 generate --apple-vas pass.com.example.myapp --key-slot 1
```

### Mit Ausgabe-Datei

```bash
vtap100 generate \
  --apple-vas pass.com.example.myapp \
  --key-slot 1 \
  --output /media/VTAP100/config.txt
```

## Python API

```python
from vtap100.models.vas import AppleVASConfig
from vtap100.models.config import VTAPConfig
from vtap100.generator import ConfigGenerator

# Einzelne VAS-Konfiguration
vas = AppleVASConfig(
    merchant_id="pass.com.example.myapp",
    key_slot=1,
)

# Mehrere VAS-Konfigurationen
vas1 = AppleVASConfig(merchant_id="pass.com.example.loyalty", key_slot=1)
vas2 = AppleVASConfig(merchant_id="pass.com.example.membership", key_slot=2)

config = VTAPConfig(vas_configs=[vas1, vas2])
generator = ConfigGenerator(config)
print(generator.generate())
```

## Generierte config.txt

```ini
!VTAPconfig
; Apple VAS Configuration
VAS1MerchantID=pass.com.example.myapp
VAS1KeySlot=1
```

## Key-Datei Setup

1. Exportiere deinen privaten Apple VAS Key als PEM-Datei
2. Benenne die Datei `private1.pem` (für KeySlot=1)
3. Kopiere die Datei auf den VTAP100
4. Nach Reboot wird der Key in Hardware gespeichert

**Wichtig:** Der Key verschwindet nach dem Reboot aus dem Dateisystem,
ist aber sicher im Reader gespeichert.

## Validierung

Der Generator validiert automatisch:
- Merchant ID muss mit `pass.` beginnen
- Key Slot muss zwischen 0 und 6 liegen
- Merchant ID darf nicht leer sein

```python
from vtap100.models.vas import AppleVASConfig
from pydantic import ValidationError

try:
    # Dies wirft einen Fehler
    vas = AppleVASConfig(merchant_id="invalid.id")
except ValidationError as e:
    print(e)  # "merchant_id must start with 'pass.' prefix"
```

## Referenzen

- [VTAP Help - Apple VAS Settings](https://help.vtapnfc.com/en/Content/VTAP-Commands/Config-txt-VAS_settings.htm)
- [Passmeister - Apple Wallet Setup](https://www.passmeister.com/en/b/nfc_setup_dot_origin_vtap100_apple_wallet)
