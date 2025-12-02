# config.txt Format

Die VTAP100-Konfiguration erfolgt über eine `config.txt` Datei, die auf den Reader kopiert wird.

## Dateiformat

### Header

Jede gültige Konfigurationsdatei muss mit dem Header beginnen:

```
!VTAPconfig
```

### Kommentare

Kommentare werden mit einem Semikolon eingeleitet:

```
; Dies ist ein Kommentar
```

### Parameter

Parameter werden im Format `Name=Wert` angegeben:

```
VAS1MerchantID=pass.com.example.test
VAS1KeySlot=1
```

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

; Keyboard Emulation
KBLogMode=1
KBSource=AG1
```

## Parameter-Kategorien

### Apple VAS (Value Added Services)

| Parameter | Beschreibung | Werte |
|-----------|--------------|-------|
| VAS#MerchantID | Apple Pass Type ID | `pass.com.*` |
| VAS#KeySlot | Private Key Slot | 0-6 (0=auto) |
| VAS#MerchantURL | Optionale URL | URL-String |

Bis zu 6 VAS-Konfigurationen möglich (VAS1 bis VAS6).

### Google Smart Tap

| Parameter | Beschreibung | Werte |
|-----------|--------------|-------|
| ST#CollectorID | Google Collector ID | String |
| ST#KeySlot | Private Key Slot | 0-6 (0=auto) |
| ST#KeyVersion | Key Version | Integer |

Bis zu 6 Smart Tap-Konfigurationen möglich (ST1 bis ST6).

### Keyboard Emulation

| Parameter | Beschreibung | Werte |
|-----------|--------------|-------|
| KBLogMode | Aktiviert Keyboard-Ausgabe | 0, 1 |
| KBSource | Datenquellen | Hex-String |
| KBEnable | USB-Keyboard aktivieren | 0, 1 |

### KBSource-Werte

Der KBSource-Wert ist ein Hex-String, der die Datenquellen definiert:

- `A` = Apple VAS Daten
- `G` = Google Smart Tap Daten
- `U` = UID der NFC-Karte
- `1-5` = Datenbytes (1=erstes Byte, 5=alle Bytes)

Beispiele:
- `A1` = Erstes Byte von Apple VAS
- `AG5` = Alle Bytes von Apple und Google
- `U1` = Erstes Byte der UID

## Private Keys

Private Keys werden als PEM-Dateien im Root-Verzeichnis des Readers gespeichert:

- `private1.pem` - Key Slot 1
- `private2.pem` - Key Slot 2
- ... bis `private6.pem`

Der Key Slot 0 bedeutet automatische Auswahl.

## Siehe auch

- [Apple VAS Konfiguration](apple_vas.md)
- [Google Smart Tap Konfiguration](google_smarttap.md)
- [Keyboard Emulation](keyboard.md)
- [Upload auf Reader](../deployment/upload_to_reader.md)
