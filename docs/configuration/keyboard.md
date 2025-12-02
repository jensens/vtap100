# Keyboard Emulation

Keyboard emulation allows the VTAP100 to send NFC data as keyboard input.

## How It Works

When enabled, the VTAP100 acts as a USB keyboard and automatically "types" the read data. This is useful for:

- POS systems without NFC API
- Legacy applications
- Quick integration without programming

## Parameters

### KBLogMode

Enables or disables keyboard emulation.

```ini
KBLogMode=1    ; Enabled
KBLogMode=0    ; Disabled
```

### KBSource

Defines which data should be output. The value is a hex string.

**Data sources:**
- `A` = Apple VAS data
- `G` = Google Smart Tap data
- `U` = UID of the NFC card/smartphone

**Data amount:**
- `1` = First byte
- `2` = First two bytes
- `3` = First three bytes
- `4` = First four bytes
- `5` = All bytes (complete data)

**Examples:**
```ini
KBSource=A1     ; First byte of Apple VAS
KBSource=G5     ; All bytes of Google Smart Tap
KBSource=AG1    ; First byte of Apple and Google
KBSource=U1     ; First byte of UID
KBSource=AGU5   ; All data from all sources
```

### KBEnable

Enables or disables the USB keyboard device.

```ini
KBEnable=1    ; USB keyboard enabled
KBEnable=0    ; USB keyboard disabled
```

### KBPrefix

Optional: Output prefix before the data.

```ini
KBPrefix=$t          ; Timestamp as prefix
KBPrefix=%0A         ; Newline as prefix
KBPrefix=ID:         ; Fixed text as prefix
```

**Variables:**
- `$t` - Current timestamp
- `%XX` - ASCII hex character (e.g., `%0A` = newline)

### KBPostfix

Suffix after the data (default: `%0A` = newline).

```ini
KBPostfix=%0A        ; Newline (default)
KBPostfix=%0D%0A     ; CRLF (Windows)
KBPostfix=%09        ; Tab
```

### KBDelayMS

Delay between keystrokes in milliseconds (5-255).

```ini
KBDelayMS=5          ; Fast (default)
KBDelayMS=50         ; Slower for older systems
KBDelayMS=100        ; Very slow
```

### KBPassMode

Enables extraction from the pass payload.

```ini
KBPassMode=1         ; Extraction enabled
KBPassMode=0         ; Disabled (default)
```

### KBPassSection

Which section from the payload is extracted (when PassMode is enabled).

```ini
KBPassSection=0      ; First section (default)
KBPassSection=1      ; Second section
KBPassSection=2      ; Third section
```

### KBPassSeparator

Separator between sections in the payload.

```ini
KBPassSeparator=|    ; Pipe (default)
KBPassSeparator=;    ; Semicolon
KBPassSeparator=,    ; Comma
```

### KBPassStart / KBPassLength

Start position and length of extraction.

```ini
KBPassStart=0        ; From beginning (default)
KBPassStart=10       ; From position 10

KBPassLength=0       ; All (default)
KBPassLength=16      ; Only 16 characters
```

## CLI Usage

```bash
# With keyboard emulation (default)
vtap100 generate --apple-vas pass.com.example.test --keyboard

# Without keyboard emulation
vtap100 generate --apple-vas pass.com.example.test --no-keyboard
```

## Python API

### Simple Configuration

```python
from vtap100.models.keyboard import KeyboardConfig

kb = KeyboardConfig(
    log_mode=True,
    source="AG",
    enable=True
)

print(kb.to_config_lines())
# ['KBLogMode=1', 'KBSource=AG']
```

### Extended Configuration

```python
from vtap100.models.keyboard import KeyboardConfig

kb = KeyboardConfig(
    log_mode=True,
    source="AG",
    prefix="$t:",           # Timestamp as prefix
    postfix="%0D%0A",       # CRLF instead of LF
    delay_ms=50,            # Slower output
    pass_mode=True,         # Payload extraction
    pass_section=1,         # Second section
    pass_separator=";",     # Semicolon separation
    pass_length=32,         # Max 32 characters
)

print(kb.to_config_lines())
# ['KBLogMode=1', 'KBSource=AG', 'KBPrefix=$t:', 'KBPostfix=%0D%0A',
#  'KBDelayMS=50', 'KBPassMode=1', 'KBPassSection=1',
#  'KBPassSeparator=;', 'KBPassLength=32']
```

### KBSource Builder

For more complex configurations there is a builder:

```python
from vtap100.models.keyboard import KBSourceBuilder

# Fluent API
source = (KBSourceBuilder()
    .apple_vas()
    .google_smarttap()
    .all_bytes()
    .build())

print(source)  # "AG5"

# With UID
source = (KBSourceBuilder()
    .uid()
    .first_byte()
    .build())

print(source)  # "U1"
```

### Builder Methods

**Data sources:**
- `.apple_vas()` - Add Apple VAS
- `.google_smarttap()` - Add Google Smart Tap
- `.uid()` - Add UID

**Data amount:**
- `.first_byte()` - First byte only
- `.first_two_bytes()` - First two bytes
- `.first_three_bytes()` - First three bytes
- `.first_four_bytes()` - First four bytes
- `.all_bytes()` - All bytes

## Complete Example

```ini
!VTAPconfig
; Apple VAS Configuration
VAS1MerchantID=pass.com.example.myapp
VAS1KeySlot=1

; Google Smart Tap Configuration
ST1CollectorID=96972794
ST1KeySlot=2
ST1KeyVersion=1

; Keyboard Emulation - Output all data
KBLogMode=1
KBSource=AG5
KBEnable=1
```

## Output Format

Data is output as a hex string, followed by Enter:

```
A1B2C3D4E5F6<Enter>
```

## Use Case Examples

### POS System Integration

```ini
; Only Apple VAS data, first byte
KBLogMode=1
KBSource=A1
```

### Logging/Debugging

```ini
; All available data
KBLogMode=1
KBSource=AGU5
```

### UID-based Access Control

```ini
; Output only UID
KBLogMode=1
KBSource=U5
```

## Tips

1. **Test first with `U1`** - The UID is always available
2. **For production systems**: Use specific sources (A or G), not all
3. **For troubleshooting**: Check with `KBSource=AGU5` which data is actually arriving

## See Also

- [config.txt Format](overview.md)
- [Apple VAS Configuration](apple_vas.md)
- [Google Smart Tap Configuration](google_smarttap.md)
