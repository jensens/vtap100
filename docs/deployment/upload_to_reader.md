# Upload auf den VTAP100 Reader

Diese Anleitung beschreibt, wie die Konfigurationsdateien auf den VTAP100 NFC-Reader übertragen werden.

## Übersicht

Der VTAP100 wird als USB-Massenspeicher erkannt. Die Konfiguration erfolgt durch:

1. Kopieren der `config.txt` auf den Reader
2. Kopieren der Private Key Dateien (`private#.pem`)
3. Sicheres Auswerfen des Readers
4. Reader neu starten

## Schritt-für-Schritt Anleitung

### 1. Reader anschließen

Verbinden Sie den VTAP100 über USB mit Ihrem Computer. Der Reader wird als Wechseldatenträger erkannt.

**Linux:**
```bash
# Reader wird automatisch gemountet, z.B. unter:
/media/$USER/VTAP100/
# oder
/run/media/$USER/VTAP100/
```

**macOS:**
```bash
# Reader erscheint unter:
/Volumes/VTAP100/
```

**Windows:**
Der Reader erscheint als neues Laufwerk (z.B. `E:`).

### 2. Konfiguration generieren

```bash
# Mit vtap100 CLI
vtap100 generate \
    --apple-vas pass.com.example.myapp \
    --key-slot 1 \
    --output config.txt

# Oder interaktiv
vtap100 wizard
```

### 3. Dateien kopieren

**config.txt kopieren:**

```bash
# Linux/macOS
cp config.txt /media/$USER/VTAP100/

# Windows (PowerShell)
Copy-Item config.txt E:\
```

**Private Keys kopieren (falls erforderlich):**

```bash
# Linux/macOS
cp private1.pem /media/$USER/VTAP100/

# Windows (PowerShell)
Copy-Item private1.pem E:\
```

### 4. Reader sicher auswerfen

**Linux:**
```bash
# Mit udisksctl
udisksctl unmount -b /dev/sdX1
udisksctl power-off -b /dev/sdX

# Oder über Dateimanager
```

**macOS:**
```bash
diskutil eject /Volumes/VTAP100
```

**Windows:**
Klicken Sie auf "Hardware sicher entfernen" in der Taskleiste.

### 5. Reader neu starten

Trennen Sie den Reader kurz vom USB und verbinden Sie ihn erneut. Die neue Konfiguration wird beim Start geladen.

## Dateistruktur auf dem Reader

```
VTAP100/
├── config.txt          # Hauptkonfiguration
├── private1.pem        # Private Key Slot 1
├── private2.pem        # Private Key Slot 2 (optional)
├── ...
└── private6.pem        # Private Key Slot 6 (optional)
```

## Konfiguration validieren

Vor dem Upload können Sie die Konfiguration prüfen:

```bash
# Lokale Datei validieren
vtap100 validate config.txt

# Datei auf dem Reader validieren
vtap100 validate /media/$USER/VTAP100/config.txt
```

## Automatisiertes Deployment

### Bash Script

```bash
#!/bin/bash
# deploy_vtap.sh

MOUNT_POINT="/media/$USER/VTAP100"
CONFIG_FILE="config.txt"

# Prüfen ob Reader gemountet ist
if [ ! -d "$MOUNT_POINT" ]; then
    echo "VTAP100 nicht gefunden!"
    exit 1
fi

# Konfiguration validieren
vtap100 validate "$CONFIG_FILE"
if [ $? -ne 0 ]; then
    echo "Konfiguration ungültig!"
    exit 1
fi

# Kopieren
cp "$CONFIG_FILE" "$MOUNT_POINT/"
echo "config.txt kopiert"

# Private Keys kopieren (wenn vorhanden)
for i in 1 2 3 4 5 6; do
    if [ -f "private$i.pem" ]; then
        cp "private$i.pem" "$MOUNT_POINT/"
        echo "private$i.pem kopiert"
    fi
done

# Sync und unmount
sync
echo "Deployment abgeschlossen. Bitte Reader sicher auswerfen."
```

### Python Script

```python
#!/usr/bin/env python3
"""Deploy VTAP100 configuration."""

import shutil
from pathlib import Path

def deploy_config(config_path: Path, mount_point: Path) -> None:
    """Deploy config.txt to VTAP100 reader."""
    if not mount_point.exists():
        raise FileNotFoundError(f"VTAP100 nicht gefunden: {mount_point}")

    # config.txt kopieren
    shutil.copy(config_path, mount_point / "config.txt")
    print(f"config.txt nach {mount_point} kopiert")

    # Private Keys kopieren
    for i in range(1, 7):
        key_file = Path(f"private{i}.pem")
        if key_file.exists():
            shutil.copy(key_file, mount_point / key_file.name)
            print(f"{key_file.name} kopiert")

if __name__ == "__main__":
    import sys
    config = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("config.txt")
    mount = Path("/media") / Path.home().name / "VTAP100"
    deploy_config(config, mount)
```

## Fehlerbehebung

### Reader wird nicht erkannt

1. Prüfen Sie die USB-Verbindung
2. Versuchen Sie einen anderen USB-Port
3. Auf Windows: Treiber-Update durchführen

### Konfiguration wird nicht übernommen

1. Stellen Sie sicher, dass die Datei `config.txt` heißt (nicht `config.txt.txt`)
2. Prüfen Sie, dass die Datei mit `!VTAPconfig` beginnt
3. Werfen Sie den Reader sicher aus bevor Sie ihn trennen

### Private Key wird nicht erkannt

1. Dateiname muss `private1.pem` bis `private6.pem` sein
2. PEM-Format muss korrekt sein (ECDSA)
3. Key Slot in config.txt muss übereinstimmen

## Sicherheitshinweise

- **Private Keys niemals weitergeben** - sie ermöglichen das Auslesen aller Pässe
- **Reader physisch sichern** - unbefugter Zugriff ermöglicht Key-Extraktion
- **Backup der Keys erstellen** - bei Verlust müssen neue Keys generiert werden

## Siehe auch

- [Schnellstart](../quickstart.md)
- [config.txt Format](../configuration/overview.md)
- [Quellensammlung](../references/sources.md)
