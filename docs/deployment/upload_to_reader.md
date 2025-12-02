# Upload to VTAP100 Reader

This guide describes how to transfer configuration files to the VTAP100 NFC reader.

## Overview

The VTAP100 is recognized as a USB mass storage device. Configuration is done by:

1. Copying `config.txt` to the reader
2. Copying private key files (`private#.pem`)
3. Safely ejecting the reader
4. Restarting the reader

## Step-by-Step Guide

### 1. Connect the Reader

Connect the VTAP100 via USB to your computer. The reader will be recognized as a removable drive.

**Linux:**
```bash
# Reader is automatically mounted, e.g., at:
/media/$USER/VTAP100/
# or
/run/media/$USER/VTAP100/
```

**macOS:**
```bash
# Reader appears at:
/Volumes/VTAP100/
```

**Windows:**
The reader appears as a new drive (e.g., `E:`).

### 2. Generate Configuration

```bash
# With vtap100 CLI
vtap100 generate \
    --apple-vas pass.com.example.myapp \
    --key-slot 1 \
    --output config.txt

# Or interactively
vtap100 wizard
```

### 3. Copy Files

**Copy config.txt:**

```bash
# Linux/macOS
cp config.txt /media/$USER/VTAP100/

# Windows (PowerShell)
Copy-Item config.txt E:\
```

**Copy private keys (if required):**

```bash
# Linux/macOS
cp private1.pem /media/$USER/VTAP100/

# Windows (PowerShell)
Copy-Item private1.pem E:\
```

### 4. Safely Eject the Reader

**Linux:**
```bash
# With udisksctl
udisksctl unmount -b /dev/sdX1
udisksctl power-off -b /dev/sdX

# Or via file manager
```

**macOS:**
```bash
diskutil eject /Volumes/VTAP100
```

**Windows:**
Click "Safely Remove Hardware" in the taskbar.

### 5. Restart the Reader

Briefly disconnect the reader from USB and reconnect it. The new configuration will be loaded at startup.

## File Structure on the Reader

```
VTAP100/
├── config.txt          # Main configuration
├── private1.pem        # Private key slot 1
├── private2.pem        # Private key slot 2 (optional)
├── ...
└── private6.pem        # Private key slot 6 (optional)
```

## Validate Configuration

You can validate the configuration before uploading:

```bash
# Validate local file
vtap100 validate config.txt

# Validate file on reader
vtap100 validate /media/$USER/VTAP100/config.txt
```

## Automated Deployment

### Bash Script

```bash
#!/bin/bash
# deploy_vtap.sh

MOUNT_POINT="/media/$USER/VTAP100"
CONFIG_FILE="config.txt"

# Check if reader is mounted
if [ ! -d "$MOUNT_POINT" ]; then
    echo "VTAP100 not found!"
    exit 1
fi

# Validate configuration
vtap100 validate "$CONFIG_FILE"
if [ $? -ne 0 ]; then
    echo "Configuration invalid!"
    exit 1
fi

# Copy
cp "$CONFIG_FILE" "$MOUNT_POINT/"
echo "config.txt copied"

# Copy private keys (if present)
for i in 1 2 3 4 5 6; do
    if [ -f "private$i.pem" ]; then
        cp "private$i.pem" "$MOUNT_POINT/"
        echo "private$i.pem copied"
    fi
done

# Sync and unmount
sync
echo "Deployment complete. Please safely eject the reader."
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
        raise FileNotFoundError(f"VTAP100 not found: {mount_point}")

    # Copy config.txt
    shutil.copy(config_path, mount_point / "config.txt")
    print(f"config.txt copied to {mount_point}")

    # Copy private keys
    for i in range(1, 7):
        key_file = Path(f"private{i}.pem")
        if key_file.exists():
            shutil.copy(key_file, mount_point / key_file.name)
            print(f"{key_file.name} copied")

if __name__ == "__main__":
    import sys
    config = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("config.txt")
    mount = Path("/media") / Path.home().name / "VTAP100"
    deploy_config(config, mount)
```

## Troubleshooting

### Reader Not Recognized

1. Check the USB connection
2. Try a different USB port
3. On Windows: Perform driver update

### Configuration Not Applied

1. Ensure the file is named `config.txt` (not `config.txt.txt`)
2. Verify the file starts with `!VTAPconfig`
3. Safely eject the reader before disconnecting

### Private Key Not Recognized

1. Filename must be `private1.pem` through `private6.pem`
2. PEM format must be correct (ECDSA)
3. Key slot in config.txt must match

## Security Notes

- **Never share private keys** - they enable reading all passes
- **Physically secure the reader** - unauthorized access allows key extraction
- **Backup your keys** - if lost, new keys must be generated

## See Also

- [Quickstart](../quickstart.md)
- [config.txt Format](../configuration/overview.md)
- [Reference Sources](../references/sources.md)
