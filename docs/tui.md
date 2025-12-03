# TUI Editor

The TUI (Terminal User Interface) editor provides a visual way to create and edit VTAP100 configurations.

## Starting the Editor

```bash
# New configuration
vtap100 editor

# Edit existing file
vtap100 editor config.txt

# With output path
vtap100 editor -o output.txt
```

## Layout

```
+------------------+----------------------------------+-------------------+
|   SIDEBAR        |          MAIN CONTENT            |   HELP PANEL      |
|   (Navigation)   |          (Forms/Edit)            |   (Context help)  |
+------------------+----------------------------------+-------------------+
|                       LIVE PREVIEW (toggle Ctrl+O)                      |
+------------------------------------------------------------------------+
```

- **Sidebar**: Navigate between configuration sections (Apple VAS, Google Smart Tap, Keyboard, NFC, DESFire, LED/Beep)
- **Main Content**: Edit forms for the selected section
- **Help Panel**: Context-sensitive help for the focused field
- **Live Preview**: Shows the generated config.txt in real-time

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+S` | Save configuration |
| `Ctrl+E` | Open export dialog |
| `Ctrl+O` | Toggle live preview |
| `Ctrl+D` | Toggle help panel |
| `Ctrl+L` | Switch language (DE/EN) |
| `Ctrl+Q` | Quit |
| `Tab` | Next field |
| `Shift+Tab` | Previous field |

## Export Options

Press `Ctrl+E` to open the export dialog:

- **Full config.txt**: Exports complete configuration
- **Template mode**: Exports without VAS/SmartTap, with Jinja2 placeholder for dynamic passes

Target options:
- Save to file
- Copy to clipboard

## Language

The interface is available in English and German. Press `Ctrl+L` to switch. Form values are preserved when switching.
