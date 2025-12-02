# VTAP100 Documentation

Willkommen zur Dokumentation des VTAP100 Configuration Generator.

## Inhaltsverzeichnis

### Erste Schritte
- [Quickstart](quickstart.md) - Schnelleinstieg in wenigen Minuten
- [Installation](quickstart.md#installation) - Installationsanleitung

### Konfiguration (Phase 1-5 - Vollständig)
- [Übersicht](configuration/overview.md) - config.txt Format und Grundlagen
- [Apple VAS](configuration/apple_vas.md) - Apple Wallet Value Added Services
- [Google Smart Tap](configuration/google_smarttap.md) - Google Wallet Smart Tap
- [Keyboard-Emulation](configuration/keyboard.md) - Tastaturemulation Einstellungen
- [NFC Tags](configuration/nfc_tags.md) - NFC Tag-Typen (Type 2, 4, 5)
- [MIFARE DESFire](configuration/desfire.md) - DESFire Konfiguration
- [LED/Beep](configuration/led_beep.md) - Visuelles und akustisches Feedback

### Deployment
- [Upload auf den Reader](deployment/upload_to_reader.md) - Dateien übertragen

### Beispiele (in Dokumentation integriert)
Beispiele finden sich in den jeweiligen Konfigurationsseiten:
- Apple VAS Beispiele: siehe [Apple VAS](configuration/apple_vas.md)
- Google Smart Tap Beispiele: siehe [Google Smart Tap](configuration/google_smarttap.md)
- Kombinierte Konfiguration: siehe [Quickstart](quickstart.md)

### Entwicklung
- [Entwickler-Guide](development.md) - TDD, Code-Stil, Contributing
- [Implementierungsplan](PLAN.md) - Projektplan und Spezifikation

### Referenz
- [Quellensammlung](references/sources.md) - Alle verwendeten Quellen und Links

## Über das Projekt

Der VTAP100 Configuration Generator ist ein Python-Tool zur einfachen Erstellung von Konfigurationsdateien für den [dotOrigin VTAP100](https://www.vtapnfc.com/) NFC Reader.

### Features (Phase 1-5 - Vollständig)

- Apple VAS Unterstützung
- Google Smart Tap Unterstützung
- Keyboard-Emulation (erweitert)
- NFC Tag Support (Type 2, 4, 5)
- MIFARE DESFire Unterstützung
- LED/Buzzer Konfiguration
- Validierung
- Rich CLI mit farbiger Ausgabe

### Schnellstart

```bash
# Installation
uv sync

# Apple VAS Konfiguration generieren
vtap100 generate --apple-vas pass.com.example.mypass --key-slot 1

# Interaktiver Wizard
vtap100 wizard
```

## Weitere Informationen

- [GitHub Repository](https://github.com/your-org/vtap100)
- [dotOrigin Website](https://www.dotorigin.com/)
- [VTAP NFC Website](https://www.vtapnfc.com/)
