# Settings Reference

Quick reference for all VTAP100 config.txt parameters. For detailed usage, see the individual configuration guides.

## Apple VAS

| Parameter | Type | Range | Default | Description |
|-----------|------|-------|---------|-------------|
| `VAS#MerchantID` | string | must start with `pass.` | required | Apple Pass Type ID |
| `VAS#KeySlot` | int | 0-6 | 0 (auto) | Private key slot |
| `VAS#MerchantURL` | string | URL | - | Optional URL on pass presentation |
| `VASDefaultPassesEnabled` | string | 1-6 | 1,2,3,4,5,6 | Enabled pass slots |

*# = slot number 1-6*

## Google Smart Tap

| Parameter | Type | Range | Default | Description |
|-----------|------|-------|---------|-------------|
| `ST#CollectorID` | string | numeric | required | Google Collector ID |
| `ST#KeySlot` | int | 0-6 | 0 (auto) | Private key slot |
| `ST#KeyVersion` | int | 0-65535 | 0 | Key version (must match Google) |
| `STDefaultPassesEnabled` | string | 1-6 | 1,2,3,4,5,6 | Enabled pass slots |

*# = slot number 1-6*

## Keyboard Emulation

| Parameter | Type | Range | Default | Description |
|-----------|------|-------|---------|-------------|
| `KBLogMode` | bool | 0/1 | 0 | Enable keyboard output |
| `KBEnable` | bool | 0/1 | 1 | Enable USB keyboard device |
| `KBSource` | string | see below | A5 | Data sources to output |
| `KBPrefix` | string | ASCII-hex | - | Prefix before data |
| `KBPostfix` | string | ASCII-hex | %0A | Suffix after data (newline) |
| `KBDelayMS` | int | 5-255 | 5 | Keystroke delay in ms |
| `KBPassMode` | bool | 0/1 | 0 | Enable payload extraction |
| `KBPassSection` | int | 0-255 | 0 | Section to extract |
| `KBPassSeparator` | char | any | \| | Section separator |
| `KBPassStart` | int | 0-65535 | 0 | Extraction start position |
| `KBPassLength` | int | 0-255 | 0 | Extraction length (0=all) |

### KBSource Bitmask

KBSource uses hexadecimal bitmasks:

| Bit | Value | Source |
|-----|-------|--------|
| 7 | 0x80 | Mobile Pass (Apple VAS / Google Smart Tap) |
| 6 | 0x40 | STUID |
| 5 | 0x20 | Card Emulation |
| 2 | 0x04 | Scanners |
| 1 | 0x02 | Command Interface |
| 0 | 0x01 | Card/Tag UID |

Common values: `A5` (default), `81`, `80`, `01`

## NFC Tags

| Parameter | Type | Range | Default | Description |
|-----------|------|-------|---------|-------------|
| `NFCType2` | enum | 0,U,N,B | - | Type 2 mode (NTAG, Ultralight) |
| `NFCType4` | enum | 0,U,N,B,D | - | Type 4 mode (DESFire, ISO14443-4) |
| `NFCType5` | enum | 0,U,N,B | - | Type 5 mode (ICODE, ISO15693) |
| `NFCReportReadError` | bool | 0/1 | 0 | Report error on read failure |
| `IgnoreRandomUID` | bool | 0/1 | 0 | Filter random Type 4 UIDs |
| `TagByteOrder` | bool | 0/1 | 0 | Reverse byte order |

### NFC Tag Modes

| Mode | Description |
|------|-------------|
| 0 | Disabled |
| U | UID only |
| N | NDEF records |
| B | Block data |
| D | DESFire (Type 4 only) |

### Tag Block Reading

| Parameter | Type | Range | Default | Description |
|-----------|------|-------|---------|-------------|
| `TagReadBlockNum` | int | 0-255 | - | Block number |
| `TagReadKeySlot` | int | 1-9 | - | Auth key slot |
| `TagReadKeyType` | enum | A,B,C | - | MIFARE key type |
| `TagReadOffset` | int | 0-15 | 0 | Start byte in block |
| `TagReadLength` | int | 1-16 | - | Bytes to read |
| `TagReadFormat` | enum | a,d,h | - | Output: ASCII/decimal/hex |
| `TagReadMinDigits` | int/A | 1-20 or A | - | Min UID digits (A=auto) |

## DESFire

| Parameter | Type | Range | Default | Description |
|-----------|------|-------|---------|-------------|
| `DESFire#AppID` | string | 6 hex | required | Application ID |
| `DESFire#FileID` | int | 1-255 | - | File ID |
| `DESFire#KeyNum` | int | 0-255 | - | Key number |
| `DESFire#KeySlot` | int | 1-9 | - | Key slot |
| `DESFire#Crypto` | enum | 0,1,3 | - | 0=none, 1=3DES, 3=AES |
| `DESFire#Format` | enum | 0,1,2 | - | 0=raw, 1=KEY-ID v1, 2=v2 |
| `DESFire#ReadLength` | int | 1-255 | 3 | Bytes to read |
| `DESFire#ReadOffset` | int | 0-255 | 0 | Start offset |
| `DESFire#Diversification` | bool | 0/1 | - | Key diversification |
| `DESFire#PrivacyKeyNum` | int | 0-255 | - | Privacy key number |
| `DESFire#PrivacyKeySlot` | int | 1-9 | - | Privacy key slot |
| `DESFire#SysIDKeySlot` | int | 1-9 | - | System ID key slot |
| `DESFire#SysIDLength` | int | 0-16 | - | System ID length |
| `DESFireSeparator` | char | any | , | Multi-app separator |

*# = slot number 1-9*

## LED

| Parameter | Type | Range | Default | Description |
|-----------|------|-------|---------|-------------|
| `LEDMode` | enum | 0-3 | - | 0=off, 1=on, 2=status, 3=custom |
| `LEDSelect` | enum | 0-3 | - | 0=external, 1=compact, 2=square, 3=serial |
| `LEDDefaultRGB` | string | 6 hex | - | Default color (e.g., 00FF00) |
| `PassLED` | sequence | see below | - | Pass read LED |
| `TagLED` | sequence | see below | - | Tag read LED |
| `PassErrorLED` | sequence | see below | - | Error LED |
| `StartLED` | sequence | see below | - | Startup LED |

### LED Sequence Format

`RRGGBB,on_ms,off_ms,repeats`

Example: `00FF00,100,100,2` = green, 100ms on, 100ms off, 2 times

## Beep

| Parameter | Type | Range | Default | Description |
|-----------|------|-------|---------|-------------|
| `PassBeep` | sequence | see below | - | Pass read beep |
| `TagBeep` | sequence | see below | - | Tag read beep |
| `PassErrorBeep` | sequence | see below | - | Error beep |
| `StartBeep` | sequence | see below | - | Startup beep |

### Beep Sequence Format

`on_ms,off_ms,repeats[,frequency]`

- Frequency: 100-20000 Hz (optional, default 3136)
- Example: `100,100,2,3136` = 100ms on, 100ms off, 2 times, 3136 Hz

## Config File Format

```ini
!VTAPconfig
; Comment
Parameter=Value
```

- Header `!VTAPconfig` required
- Comments start with `;`
- Parameters: `Name=Value`
