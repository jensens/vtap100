# Changelog

Alle nennenswerten Änderungen an diesem Projekt werden in dieser Datei dokumentiert.

Das Format basiert auf [Keep a Changelog](https://keepachangelog.com/de/1.0.0/),
und dieses Projekt verwendet [Semantic Versioning](https://semver.org/lang/de/).

## [Unreleased]

*Alle Phasen abgeschlossen*

## [0.5.0] - Phase 5: LED/Beep Feedback

### Added - LED Models
- `LEDMode` - LED-Betriebsmodus (OFF, ON, STATUS, CUSTOM)
- `LEDSelect` - LED-Typ (EXTERNAL, ONBOARD_COMPACT, ONBOARD_SQUARE, SERIAL)
- `LEDSequence` - LED-Sequenz (Farbe, Timing, Wiederholungen)
- `LEDConfig` - LED-Konfiguration

### Added - Beep Models
- `BeepSequence` - Beep-Sequenz (Timing, Wiederholungen, Frequenz)
- `BeepConfig` - Beep-Konfiguration
- `FeedbackConfig` - Kombinierte LED/Beep-Konfiguration

### Added - LED Parameter
- `LEDMode` - Betriebsmodus (0-3)
- `LEDSelect` - LED-Typ (0-3)
- `LEDDefaultRGB` - Standard-Farbe (Hex)
- `PassLED` - LED bei Pass-Read
- `TagLED` - LED bei Tag-Read
- `PassErrorLED` - LED bei Fehler
- `StartLED` - LED beim Start

### Added - Beep Parameter
- `PassBeep` - Beep bei Pass-Read
- `TagBeep` - Beep bei Tag-Read
- `PassErrorBeep` - Beep bei Fehler
- `StartBeep` - Beep beim Start

### Added - Tests
- 67 neue Unit-Tests für LED/Beep Model
- Gesamt: 269 Unit-Tests

### Updated - Dokumentation
- LED/Beep Dokumentation erstellt
- Alle Phasen abgeschlossen

## [0.4.0] - Phase 4: MIFARE DESFire

### Added - DESFire Models
- `DESFireCryptoMode` - Kryptographische Modi (NONE, DES3, AES)
- `DESFireDataFormat` - Datenformate (RAW, KEYID_V1, KEYID_V2)
- `DESFireAppConfig` - Einzelne DESFire-App Konfiguration
- `DESFireConfig` - Mehrere DESFire-Apps (max 9)

### Added - DESFire Parameter
- `DESFire#AppID` - Application ID (6 Hex-Zeichen)
- `DESFire#FileID` - File ID (1-255)
- `DESFire#KeyNum` - Key-Nummer
- `DESFire#KeySlot` - Key-Slot (1-9)
- `DESFire#Crypto` - Krypto-Modus (0, 1, 3)
- `DESFire#Format` - Ausgabeformat (0, 1, 2)
- `DESFire#ReadLength` - Leselänge (1-255)
- `DESFire#ReadOffset` - Lese-Offset (0-255)
- `DESFire#Diversification` - Key-Diversifizierung
- `DESFireSeparator` - Trennzeichen für mehrere Apps

### Added - Tests
- 46 neue Unit-Tests für DESFire Model
- Gesamt: 202 Unit-Tests

### Updated - Dokumentation
- MIFARE DESFire Dokumentation erstellt

## [0.3.0] - Phase 3: NFC Tag Support

### Added - NFC Tag-Typen
- `NFCType2` - NFC Type 2 Tags (NTAG, MIFARE Ultralight)
- `NFCType4` - NFC Type 4 Tags (DESFire, ISO 14443-4)
- `NFCType5` - NFC Type 5 Tags (ICODE, ISO 15693)
- Lese-Modi: UID, NDEF, Block, DESFire

### Added - NFC Optionen
- `NFCReportReadError` - Fehler-Reporting
- `IgnoreRandomUID` - Zufällige UIDs filtern
- `TagByteOrder` - Byte-Reihenfolge umkehren

### Added - Block-Lese-Konfiguration
- `TagReadBlockNum` - Block-Nummer (0-255)
- `TagReadKeySlot` - Key-Slot (1-9)
- `TagReadKeyType` - Key-Typ (A, B, C)
- `TagReadOffset` - Start-Byte (0-15)
- `TagReadLength` - Länge (1-16)
- `TagReadFormat` - Format (ASCII, Decimal, Hex)
- `TagReadMinDigits` - Min. Ziffern für UID

### Added - Tests
- 49 neue Unit-Tests für NFC Tag Model
- Gesamt: 156 Unit-Tests

### Updated - Dokumentation
- NFC Tags Dokumentation erstellt

## [0.2.0] - Phase 2: Erweiterte Keyboard-Emulation

### Added - Erweiterte Keyboard-Parameter
- `KBPrefix` - Präfix vor Daten (ASCII-Hex oder Variablen wie `$t`)
- `KBPostfix` - Suffix nach Daten (Standard: `%0A`)
- `KBDelayMS` - Verzögerung zwischen Tastendrücken (5-255ms)
- `KBPassMode` - Payload-Extraktion aktivieren
- `KBPassSection` - Abschnitt auswählen
- `KBPassSeparator` - Trennzeichen für Abschnitte
- `KBPassStart` - Startposition der Extraktion
- `KBPassLength` - Länge der Extraktion

### Added - Tests
- 30 neue Unit-Tests für erweiterte Keyboard-Parameter
- Gesamt: 107 Unit-Tests

### Updated - Dokumentation
- Keyboard-Emulation Dokumentation erweitert
- Neue Python API Beispiele

## [0.1.0] - Phase 1 Abgeschlossen

### Added - Apple VAS (Value Added Services)
- `AppleVASConfig` Model mit Pydantic-Validierung
- Merchant ID Validierung (muss mit `pass.` beginnen)
- Key Slot Support (0-6)
- Optional: Merchant URL
- `VASDefaultPassesConfig` für Standard-Pässe (ECP, Payment, Access)

### Added - Google Smart Tap
- `GoogleSmartTapConfig` Model mit Pydantic-Validierung
- Collector ID Support
- Key Slot und Key Version Support
- `SmartTapDefaultPassesConfig` für Standard-Pässe
  - Loyalty, Gift Card, Offer
  - Transit, Event Ticket, Flight, Boarding

### Added - Keyboard Emulation
- `KeyboardConfig` Model
- KBLogMode, KBSource, KBEnable Parameter
- `KBSourceBuilder` Fluent API für einfache KBSource-Erstellung
- Datenquellen: Apple VAS (A), Google Smart Tap (G), UID (U)
- Byte-Auswahl: 1-5 (einzeln bis alle Bytes)

### Added - config.txt Generator
- `ConfigGenerator` Klasse
- Generiert vollständige config.txt Dateien
- Support für Kommentare
- Datei- und Stream-Output

### Added - CLI (Command Line Interface)
- `vtap100 generate` - Konfiguration generieren
- `vtap100 wizard` - Interaktiver Assistent
- `vtap100 validate` - Bestehende Konfiguration prüfen
- `vtap100 docs` - Dokumentation anzeigen
- Rich-Formatierung mit farbiger Ausgabe

### Added - Dokumentation
- Quickstart Guide
- Konfigurationsreferenz (Apple VAS, Google Smart Tap, Keyboard)
- Deployment-Anleitung
- Entwickler-Guide mit TDD-Workflow
- Quellensammlung mit externen Links

### Added - Tests
- 77 Unit-Tests (TDD Red-Green-Refactor)
- 60%+ Code Coverage

### Technical Details
- Python 3.11+
- Pydantic 2.0+ für Validierung
- Click für CLI-Framework
- Rich für Terminal-Formatierung
- pytest für Tests
- ruff für Linting/Formatting
