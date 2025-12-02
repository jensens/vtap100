# VTAP100 Configuration Generator - Spezifikation

## Übersicht

Ein Tool zur Generierung von Konfigurationsdateien für den dotOrigin VTAP100 NFC Reader.

**Quellen:**
- [VTAP Configuration Guide PDF](https://www.vtapnfc.com/downloads/VTAP_Configuration_Guide.pdf)
- [VTAP Commands Reference Guide](https://www.vtapnfc.com/downloads/VTAP_Commands_Reference_Guide.pdf)
- [VTAP Help - Apple VAS Settings](https://help.vtapnfc.com/en/Content/VTAP-Commands/Config-txt-VAS_settings.htm)
- [VTAP Help - Google Smart Tap Settings](https://help.vtapnfc.com/en/Content/VTAP-Commands/Config-txt-ST-settings.htm)
- [VTAP Help - Keyboard Settings](https://help.vtapnfc.com/en/Content/VTAP-Commands/Config-txt-KB-settings.htm)
- [VTAP Help - DESFire Settings](https://help.vtapnfc.com/en/Content/VTAP-Commands/Config-txt-DESFire-settings.htm)
- [VTAP Help - LED Settings](https://help.vtapnfc.com/en/Content/VTAP-Commands/Config-txt-LED-settings.htm)

---

## 1. config.txt Dateiformat

### Header
- Muss mit `!VTAPconfig` beginnen
- Kommentare beginnen mit `;`
- Ein Parameter pro Zeile
- Format: `ParameterName=Wert`
- Reihenfolge der Parameter ist irrelevant
- Jeder Parameter darf nur einmal vorkommen (letzter gewinnt)

### Beispiel
```ini
!VTAPconfig
; Apple VAS Konfiguration
VAS1MerchantID=pass.com.example.mypass
VAS1KeySlot=1
; Keyboard Emulation
KBLogMode=1
KBSource=A1
```

---

## 2. Konfigurationsparameter

### 2.1 Apple VAS (Value Added Services)

| Parameter | Werte | Default | Beschreibung |
|-----------|-------|---------|--------------|
| VAS#MerchantID | String | - | Pass Type ID von Apple (z.B. `pass.com.company.passname`) |
| VAS#KeySlot | 1-6, 0 | 0 | Slot der private#.pem Datei |
| VAS#MerchantURL | URL | - | Optional: URL für Pass-Präsentation |
| VASDefaultPassesEnabled | Liste | 1,2,3,4,5,6 | Aktive VAS-Konfigurationen |

*# = 1-6 für bis zu 6 verschiedene Apple Pass-Konfigurationen*

### 2.2 Google Smart Tap

| Parameter | Werte | Default | Beschreibung |
|-----------|-------|---------|--------------|
| ST#CollectorID | Numerisch | - | Collector ID von Google |
| ST#KeySlot | 1-6, 0 | 0 | Slot der private#.pem Datei |
| ST#KeyVersion | Numerisch | 0 | Key-Version (muss mit Google Dashboard übereinstimmen) |
| STDefaultPassesEnabled | Liste | 1,2,3,4,5,6 | Aktive ST-Konfigurationen |

*# = 1-6 für bis zu 6 verschiedene Google Pass-Konfigurationen*

### 2.3 Keyboard Emulation

| Parameter | Werte | Default | Beschreibung |
|-----------|-------|---------|--------------|
| KBLogMode | 0, 1 | 0 | Keyboard-Emulation an/aus |
| KBEnable | 0, 1 | 1 | USB Keyboard Device aktivieren |
| KBSource | Hex | A5 | Bitwise: welche Daten als Keyboard ausgeben |
| KBDelayMS | 5-255 | 5 | Verzögerung zwischen Tastendrücken (ms) |
| KBPrefix | ASCII-Hex/Var | - | Präfix vor Daten (z.B. `%0A`, `$t`) |
| KBPostfix | ASCII-Hex/Var | %0A | Suffix nach Daten |
| KBPassMode | 0, 1 | 0 | Extraktion aus Pass-Payload aktivieren |
| KBPassSection | Numerisch | 0 | Welcher Abschnitt extrahiert wird |
| KBPassSeparator | Zeichen | \| | Trennzeichen für Abschnitte |
| KBPassStart | Numerisch | 0 | Startposition für Extraktion |
| KBPassLength | Numerisch | 0 | Länge der Extraktion (0=alles) |
| KBMap | Dateiref | - | Keyboard-Layout-Mapping |

**KBSource Werte (bitwise kombinierbar):**
- A = Apple VAS Pass
- G = Google Smart Tap Pass
- 0 = MIFARE Card/Tag
- 2 = NFC Type 2
- 4 = NFC Type 4
- 6 = NFC Type 5
- E = Card Emulation
- X = Apple Wallet Access/ECP2 (iPhone)
- W = Apple Wallet Access/ECP2 (Apple Watch)

### 2.4 NFC Card/Tag Einstellungen

| Parameter | Werte | Default | Beschreibung |
|-----------|-------|---------|--------------|
| NFCType2 | U, N, B, 0 | 0 | NFC Type 2 Tag Modus |
| NFCType4 | U, N, B, D, 0 | 0 | NFC Type 4 Tag Modus |
| NFCType5 | U, N, B, 0 | 0 | NFC Type 5 Tag Modus |
| NFCReportReadError | 0, 1 | 0 | Fehler-Payload bei Lesefehlern |
| IgnoreRandomUID | 0, 1 | 0 | Zufällige Type 4 UIDs filtern |
| TagByteOrder | 0, 1 | 0 | Byte-Reihenfolge umkehren |
| TagReadBlockNum | 0-255 | - | Block-Nummer zum Lesen |
| TagReadKeySlot | 1-9 | - | Key-Slot für Authentifizierung |
| TagReadKeyType | A, B, C | - | Key-Typ |
| TagReadOffset | 0-15 | 0 | Start-Byte im Block |
| TagReadLength | 1-16 | - | Anzahl zu lesender Bytes |
| TagReadFormat | a, d, h | - | Ausgabeformat (ASCII/Dezimal/Hex) |
| TagReadMinDigits | 1-20, A, X | - | Min. Ziffern für UID (A=auto) |

**NFCType Werte:**
- U oder 1 = UID lesen
- N oder 2 = NDEF Records lesen
- B oder 3 = Block-Daten lesen
- D = DESFire secure data (nur Type 4)
- 0 = Deaktiviert

### 2.5 MIFARE DESFire

| Parameter | Werte | Default | Beschreibung |
|-----------|-------|---------|--------------|
| DESFire#AppID | 6 Hex | - | Application ID (MSB first) |
| DESFire#FileID | 1-255 | - | File ID in der Application |
| DESFire#KeyNum | Numerisch | - | Key-Nummer für Zugriff |
| DESFire#KeySlot | 1-9 | - | Slot der appkey#.txt Datei |
| DESFire#Crypto | 0, 1, 3 | 3 | Verschlüsselung (0=keine, 1=3DES, 3=AES) |
| DESFire#Format | 0, 1, 2 | 0 | Datenformat (0=raw, 1=KEY-ID v1, 2=KEY-ID v2) |
| DESFire#ReadLength | 1-255 | 3 | Bytes zu lesen |
| DESFire#ReadOffset | 0-255 | 0 | Start-Position |
| DESFire#Diversification | 0, 1 | 0 | NXP AN10922 Key-Diversifikation |
| DESFire#PrivacyKeyNum | Num | - | Privacy Key Nummer |
| DESFire#PrivacyKeySlot | 1-9 | - | Privacy Key Slot |
| DESFire#SysIDKeySlot | 1-9 | - | System ID Key Slot |
| DESFire#SysIDLength | 0-16 | 0 | System ID Länge |
| DESFireSeparator | String | , | Trennzeichen zwischen mehreren Reads |

*# = 1-9 für bis zu 9 verschiedene DESFire-Konfigurationen*

### 2.6 LED Einstellungen

| Parameter | Werte | Default | Beschreibung |
|-----------|-------|---------|--------------|
| LEDMode | 0-3 | 0 | LED-Betriebsmodus |
| LEDSelect | 0-3 | 1 | LED-Typ/Position |
| LEDDefaultRGB | Hex | FFFFFF | Standard-Farbe |
| PassLED | Farbe,on,off,rep | - | LED bei Pass-Read |
| TagLED | Farbe,on,off,rep | - | LED bei Tag-Read |
| PassErrorLED | Farbe,on,off,rep | - | LED bei Fehler |
| StartLED | Farbe,on,off,rep | - | LED bei Start |

**LEDSelect Werte:**
- 0 = Externe RGB LED (common cathode)
- 1 = On-board LED (compact case)
- 2 = On-board LED (square case)
- 3 = Serial LEDs

**LED Format:** `RRGGBB,on_ms,off_ms,repeats`
- Beispiel: `00FF00,100,100,2` = 2x grünes Blinken, 100ms an/aus

### 2.7 Buzzer/Beep Einstellungen

| Parameter | Format | Beschreibung |
|-----------|--------|--------------|
| PassBeep | on,off,rep[,freq] | Beep bei Pass-Read |
| TagBeep | on,off,rep[,freq] | Beep bei Tag-Read |
| StartBeep | on,off,rep[,freq] | Beep bei Start |
| PassErrorBeep | on,off,rep[,freq] | Beep bei Fehler |

**Format:** `on_ms,off_ms,repeats[,frequency_hz]`
- Beispiel: `100,100,2` = 2 Beeps, 100ms an, 100ms Pause
- Frequenz default: 3136 Hz

---

## 3. Key-Dateien

### 3.1 Private Keys für VAS/Smart Tap
- Dateiname: `private#.pem` (# = 1-6)
- Format: Standard PEM
- Verwendung: Referenziert über VAS#KeySlot oder ST#KeySlot

### 3.2 Application Keys für DESFire/MIFARE
- Dateiname: `appkey#.txt` (# = 1-9)
- Verwendung: Referenziert über DESFire#KeySlot oder TagReadKeySlot

### 3.3 Wichtig
- Maximal 6 private Key-Dateien
- Maximal 9 appkey-Dateien
- Nach Reboot werden Keys in Hardware gespeichert und verschwinden aus dem Dateisystem

---

## 4. Lock-Datei (optional)

### Konfiguration sperren
```
!VTAPlock lock=meinpasswort
```

### Konfiguration entsperren
```
!VTAPlock unlock=meinpasswort
```

---

## 5. Prozess: Konfiguration auf den Reader übertragen

### Schritt 1: VTAP100 anschließen
- USB-Kabel verbinden
- Reader erscheint als Mass Storage Device (wie USB-Stick)
- Funktioniert mit Windows, Mac und Linux ohne Treiber

### Schritt 2: Dateien vorbereiten
1. `config.txt` erstellen/bearbeiten
2. Private Key(s) als `private#.pem` benennen
3. Optional: `appkey#.txt` für DESFire erstellen
4. Optional: `leds.ini` für komplexe LED-Sequenzen

### Schritt 3: Dateien übertragen
1. VTAP100-Laufwerk im Dateimanager öffnen
2. Alle Konfigurationsdateien auf das Laufwerk kopieren
3. Änderungen werden sofort wirksam (außer Reboot-erforderliche)

### Schritt 4: Aktivierung
- Die meisten Änderungen: Sofort aktiv
- Einige Änderungen (z.B. COM-Port Status): Reboot erforderlich
- Keys: Nach Reboot in Hardware gespeichert, nicht mehr sichtbar

### Schritt 5: Verifizierung
- LED/Beep beim Start prüfen
- Test-Pass oder Tag präsentieren
- Bei Keyboard-Emulation: Texteditor öffnen und Pass scannen

---

## 6. Technische Entscheidungen

- **Programmiersprache:** Python 3.11+
- **CLI Framework:** Rich (für formatierte Ausgabe, Tabellen, Progress)
- **Key-Management:** Nur existierende Keys referenzieren (keine Generierung)
- **Dokumentation:** Ausführlich im `docs/` Verzeichnis
- **Entwicklungsansatz:** Test-Driven Development (TDD)
- **Test Framework:** pytest mit pytest-cov für Coverage

---

## 6.1 Test-Driven Development (TDD) Workflow

### Grundprinzip: Red-Green-Refactor
1. **Red:** Test schreiben, der fehlschlägt
2. **Green:** Minimalen Code schreiben, damit Test besteht
3. **Refactor:** Code verbessern, Tests müssen weiter bestehen

### TDD für jedes Feature
Bevor Code geschrieben wird:
1. Dokumentation für das Feature schreiben (was soll es tun?)
2. Tests schreiben, die das erwartete Verhalten definieren
3. Implementation schreiben
4. Dokumentation finalisieren

### Test-Kategorien
```
tests/
├── unit/                    # Isolierte Unit-Tests
│   ├── test_models_vas.py
│   ├── test_models_smarttap.py
│   ├── test_models_keyboard.py
│   ├── test_generator.py
│   └── test_validator.py
├── integration/             # Integrationstests
│   ├── test_cli.py
│   └── test_full_workflow.py
└── fixtures/                # Test-Daten
    ├── valid_configs/
    ├── invalid_configs/
    └── expected_outputs/
```

### Beispiel TDD-Zyklus für VAS-Model

**1. Erst Test schreiben (tests/unit/test_models_vas.py):**
```python
import pytest
from vtap100.models.vas import AppleVASConfig

def test_vas_config_requires_merchant_id():
    """VAS config must have a merchant ID"""
    with pytest.raises(ValueError):
        AppleVASConfig(key_slot=1)

def test_vas_config_valid():
    """Valid VAS config should be created"""
    config = AppleVASConfig(
        merchant_id="pass.com.example.test",
        key_slot=1
    )
    assert config.merchant_id == "pass.com.example.test"
    assert config.key_slot == 1

def test_vas_config_generates_correct_output():
    """VAS config should generate correct config.txt lines"""
    config = AppleVASConfig(
        merchant_id="pass.com.example.test",
        key_slot=1
    )
    lines = config.to_config_lines(slot_number=1)
    assert "VAS1MerchantID=pass.com.example.test" in lines
    assert "VAS1KeySlot=1" in lines
```

**2. Dann Implementation (src/vtap100/models/vas.py):**
```python
from pydantic import BaseModel, field_validator

class AppleVASConfig(BaseModel):
    merchant_id: str
    key_slot: int = 0
    merchant_url: str | None = None

    @field_validator('merchant_id')
    @classmethod
    def validate_merchant_id(cls, v):
        if not v or not v.startswith('pass.'):
            raise ValueError('merchant_id must start with "pass."')
        return v

    def to_config_lines(self, slot_number: int) -> list[str]:
        lines = [f"VAS{slot_number}MerchantID={self.merchant_id}"]
        if self.key_slot > 0:
            lines.append(f"VAS{slot_number}KeySlot={self.key_slot}")
        if self.merchant_url:
            lines.append(f"VAS{slot_number}MerchantURL={self.merchant_url}")
        return lines
```

**3. Dann Dokumentation (docs/configuration/apple_vas.md):**
```markdown
# Apple VAS Konfiguration

## Parameter
| Parameter | Pflicht | Werte | Beschreibung |
|-----------|---------|-------|--------------|
| merchant_id | Ja | String (pass.*) | Apple Pass Type ID |
...
```

### Coverage-Ziel
- Minimum 90% Test-Coverage
- Kritische Pfade (Validierung, Generator) 100%

### CI/CD Integration
```yaml
# pyproject.toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "--cov=vtap100 --cov-report=term-missing --cov-fail-under=90"
```

---

## 6.2 Dokumentations-Workflow

### Prinzip: Docs-as-Code
Dokumentation wird parallel zum Code geschrieben und versioniert.

### Wann dokumentieren?
1. **Vor Implementation:** Feature-Beschreibung in docs/
2. **Während Implementation:** Inline-Docstrings
3. **Nach Implementation:** Beispiele und Tutorials aktualisieren

### Docstring-Standard (Google Style)
```python
def generate_config(config: VTAPConfig, output_path: Path) -> None:
    """Generate a VTAP100 config.txt file.

    Args:
        config: The VTAP configuration object containing all settings.
        output_path: Path where the config.txt will be written.

    Raises:
        ValidationError: If the configuration is invalid.
        FileExistsError: If output file exists and overwrite=False.

    Example:
        >>> config = VTAPConfig(vas=[AppleVASConfig(...)])
        >>> generate_config(config, Path("./config.txt"))
    """
```

### Changelog führen
```markdown
# CHANGELOG.md

## [Unreleased]
### Added
- Apple VAS configuration support
- Google Smart Tap configuration support

### Changed
- ...

### Fixed
- ...
```

---

## 7. Implementierungsplan (Phasen)

### Phase 1: Core + Mobile Wallet (Priorität: Hoch)
1. Projekt-Struktur anlegen
2. Datenmodelle für Konfiguration (Pydantic)
3. config.txt Generator
4. Apple VAS Konfiguration
5. Google Smart Tap Konfiguration
6. Keyboard-Emulation Basis (KBLogMode, KBSource)
7. CLI mit Rich
8. Validierung der Pflichtfelder

### Phase 2: Erweiterte Keyboard-Emulation
1. KBPrefix/KBPostfix
2. KBPassMode Extraktion
3. KBDelayMS und weitere KB-Parameter

### Phase 3: NFC Tags
1. NFCType2/4/5 Einstellungen
2. Tag-Read Parameter
3. UID-Formatierung

### Phase 4: MIFARE DESFire
1. DESFire-Konfigurationen (1-9)
2. Crypto-Einstellungen
3. Key-Diversifikation

### Phase 5: LED/Beep + Extras
1. LED-Konfiguration
2. Beep-Sequenzen
3. Lock-Datei Generierung

---

## 8. Projektstruktur

```
vtap100/
├── README.md                   # Projekt-Übersicht
├── CHANGELOG.md                # Änderungsprotokoll
├── pyproject.toml              # Projekt-Konfiguration (uv/pip)
├── src/
│   └── vtap100/
│       ├── __init__.py
│       ├── cli.py              # Rich CLI Haupteinstieg
│       ├── models/
│       │   ├── __init__.py
│       │   ├── config.py       # Haupt-Konfigurationsmodell
│       │   ├── vas.py          # Apple VAS Modelle
│       │   ├── smarttap.py     # Google Smart Tap Modelle
│       │   ├── keyboard.py     # Keyboard-Emulation Modelle
│       │   ├── nfc.py          # NFC Tag Modelle
│       │   ├── desfire.py      # DESFire Modelle
│       │   └── feedback.py     # LED/Beep Modelle
│       ├── generator.py        # config.txt Generator
│       ├── validator.py        # Validierungslogik
│       └── templates/          # Vordefinierte Konfigurationen
│           ├── __init__.py
│           ├── apple_vas.py
│           ├── google_smarttap.py
│           └── combined.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py             # pytest Fixtures
│   ├── unit/                   # Unit-Tests (isoliert)
│   │   ├── __init__.py
│   │   ├── test_models_vas.py
│   │   ├── test_models_smarttap.py
│   │   ├── test_models_keyboard.py
│   │   ├── test_models_nfc.py
│   │   ├── test_models_desfire.py
│   │   ├── test_models_feedback.py
│   │   ├── test_generator.py
│   │   └── test_validator.py
│   ├── integration/            # Integrationstests
│   │   ├── __init__.py
│   │   ├── test_cli.py
│   │   └── test_full_workflow.py
│   └── fixtures/               # Test-Daten
│       ├── valid_configs/
│       │   ├── apple_vas_simple.txt
│       │   ├── google_smarttap.txt
│       │   └── combined.txt
│       ├── invalid_configs/
│       │   ├── missing_merchant_id.txt
│       │   └── invalid_key_slot.txt
│       └── expected_outputs/
│           └── ...
├── docs/
│   ├── README.md               # Dokumentations-Übersicht
│   ├── PLAN.md                 # Dieser Implementierungsplan
│   ├── quickstart.md           # Schnelleinstieg
│   ├── development.md          # Entwickler-Guide (TDD, etc.)
│   ├── configuration/
│   │   ├── overview.md         # config.txt Format
│   │   ├── apple_vas.md        # Apple VAS Parameter
│   │   ├── google_smarttap.md  # Google Smart Tap Parameter
│   │   ├── keyboard.md         # Keyboard-Emulation
│   │   ├── nfc_tags.md         # NFC Tag Einstellungen
│   │   ├── desfire.md          # DESFire Konfiguration
│   │   └── led_beep.md         # LED/Beep Einstellungen
│   ├── deployment/
│   │   └── upload_to_reader.md # Prozess: Dateien auf Reader
│   ├── examples/
│   │   ├── apple_only.md
│   │   ├── google_only.md
│   │   └── combined.md
│   └── references/
│       └── sources.md          # Quellensammlung mit Links
└── examples/
    ├── apple_vas_simple.yaml   # Beispiel-Input
    ├── google_smarttap.yaml
    └── output/                 # Generierte config.txt Beispiele
```

---

## 9. CLI Design (mit Rich)

### Hauptbefehle

```bash
# Konfiguration generieren
vtap100 generate --apple-vas pass.com.example.mypass --key-slot 1 --output ./config.txt

# Interaktiver Modus
vtap100 wizard

# Konfiguration validieren
vtap100 validate ./config.txt

# Vorlagen anzeigen
vtap100 templates list
vtap100 templates show apple-vas

# Hilfe zu Parametern
vtap100 docs vas
vtap100 docs keyboard
```

### Rich Features
- Farbige Ausgabe für Erfolg/Fehler/Warnungen
- Tabellen für Parameter-Übersichten
- Progress-Bar beim Generieren
- Panels für Konfigurationsvorschau
- Syntax-Highlighting für generierte config.txt

---

## 10. Dokumentationsstruktur (docs/)

### docs/references/sources.md - Quellensammlung

```markdown
# VTAP100 Quellensammlung

## Offizielle Dokumentation
- [VTAP Configuration Guide (PDF)](https://www.vtapnfc.com/downloads/VTAP_Configuration_Guide.pdf)
- [VTAP Commands Reference Guide (PDF)](https://www.vtapnfc.com/downloads/VTAP_Commands_Reference_Guide.pdf)
- [VTAP Documentation Portal](https://www.vtapnfc.com/documentation/)

## VTAP Help Center
- [Apple VAS Settings](https://help.vtapnfc.com/en/Content/VTAP-Commands/Config-txt-VAS_settings.htm)
- [Google Smart Tap Settings](https://help.vtapnfc.com/en/Content/VTAP-Commands/Config-txt-ST-settings.htm)
- [Keyboard Emulation Settings](https://help.vtapnfc.com/en/Content/VTAP-Commands/Config-txt-KB-settings.htm)
- [NFC Card/Tag Settings](https://help.vtapnfc.com/en/Content/VTAP-Commands/Config-txt-Card-Tag-settings.htm)
- [DESFire Settings](https://help.vtapnfc.com/en/Content/VTAP-Commands/Config-txt-DESFire-settings.htm)
- [LED Settings](https://help.vtapnfc.com/en/Content/VTAP-Commands/Config-txt-LED-settings.htm)
- [Default config.txt](https://help.vtapnfc.com/en/Content/VTAP-Configuration-Guide/VTAPConfig-txt.htm)

## Tutorials
- [PassNinja: VTAP100 Configuration](https://www.passninja.com/tutorials/hardware/how-to-configure-a-dot-origin-vtap100-nfc-reader)
- [Passmeister: Apple Wallet Setup](https://www.passmeister.com/en/b/nfc_setup_dot_origin_vtap100_apple_wallet)
- [Passmeister: Google Wallet Setup](https://www.passmeister.com/en/b/nfc_setup_dot_origin_vtap100_google_wallet)

## Manuals (ManualsLib)
- [VTAP100 Installation Manual](https://www.manualslib.com/manual/2914074/Dot-Origin-Vtap100.html)
- [VTAP100 Basic Configuration Manual](https://www.manualslib.com/manual/2904969/Dot-Origin-Vtap-100.html)
- [VTAP Series Integration Manual](https://www.manualslib.com/manual/3364754/Dot-Origin-Vtap-Series.html)

## Hersteller
- [Dot Origin Website](https://www.dotorigin.com/)
- [VTAP NFC Website](https://www.vtapnfc.com/)
- [VTAP Shop](https://shop.vtapnfc.com/)

## Support
- E-Mail: vtap-support@dotorigin.com
```

---

## 11. Beispiel CLI-Ausgabe

```
╭─────────────────────────────────────────────────────────╮
│  VTAP100 Configuration Generator                        │
╰─────────────────────────────────────────────────────────╯

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Apple VAS Konfiguration                                 ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
  Merchant ID: pass.com.example.mypass
  Key Slot:    1
  Key File:    ✓ private1.pem gefunden

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Keyboard Emulation                                      ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
  Mode:   Aktiviert
  Source: Apple VAS (A1)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Generierte config.txt:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

!VTAPconfig
; Generated by VTAP100 Config Generator
; Apple VAS Configuration
VAS1MerchantID=pass.com.example.mypass
VAS1KeySlot=1
; Keyboard Emulation
KBLogMode=1
KBSource=A1

✓ Konfiguration gespeichert: ./config.txt
```
