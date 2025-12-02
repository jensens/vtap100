# Plan: Export-Dialog mit Template-Modus

## Ziel

Neuer Export-Dialog im TUI (Shortcut `Ctrl+E`) mit zwei Modi:
1. **Vollständige config.txt** - Wie bisher, alles wird exportiert
2. **Template-Modus** - Ohne VAS/SmartTap, mit Jinja2-Platzhalter für Phil's Workflow

## Phil's Use-Case

Phil konfiguriert im TUI die statischen Teile (Keyboard, NFC, DESFire, LED/Beep) und verwendet sein eigenes Jinja2-Template für die dynamischen Passes (VAS/SmartTap):

```jinja2
!VTAPconfig

; === DYNAMIC PASSES (Jinja2) ===
{% for passinfo in passes %}
{% if passinfo.apple %}
VAS{{ passinfo.slot }}MerchantID={{ passinfo.apple.merchant_id }}
VAS{{ passinfo.slot }}KeySlot={{ passinfo.slot }}
{% endif %}
{% if passinfo.google %}
ST{{ passinfo.slot }}CollectorID={{ passinfo.google.collector_id }}
ST{{ passinfo.slot }}KeySlot={{ passinfo.slot }}
{% endif %}
{% endfor %}

; === STATIC CONFIGURATION (from TUI) ===
; Keyboard Emulation
KBLogMode=1
...
```

## Architektur

### Neue Dateien

```
src/vtap100/tui/
├── screens/
│   └── export_dialog.py    # NEU: ExportDialog ModalScreen
├── widgets/
│   └── (keine neuen)
└── i18n/translations/
    ├── de.yaml             # ERWEITERT: Export-Dialog Texte
    └── en.yaml             # ERWEITERT: Export-Dialog Texte

src/vtap100/
└── generator.py            # ERWEITERT: generate_template() Methode

tests/unit/
└── test_tui_export.py      # NEU: Tests für Export-Dialog
```

### Export-Dialog UI

```
┌─────────────────── Export ───────────────────┐
│                                              │
│  Exportformat:                               │
│                                              │
│    ○ Vollständige config.txt                 │
│    ● Template (ohne VAS/SmartTap)            │
│                                              │
│  ┌────────────────────────────────────────┐  │
│  │ Hinweis: Template-Modus exportiert     │  │
│  │ einen Jinja2-Platzhalter für Passes.   │  │
│  │ Keyboard, NFC, DESFire und LED/Beep    │  │
│  │ werden vollständig exportiert.         │  │
│  └────────────────────────────────────────┘  │
│                                              │
│  Ziel:                                       │
│    ○ Datei speichern                         │
│    ● In Zwischenablage kopieren              │
│                                              │
│         [Abbrechen]  [Exportieren]           │
└──────────────────────────────────────────────┘
```

## Implementierung (TDD)

### Phase 1: Tests schreiben

#### 1.1 Generator-Tests (`tests/unit/test_generator.py` erweitern)

```python
class TestTemplateGeneration:
    """Tests for Jinja2 template generation."""

    def test_generate_template_excludes_vas(self):
        """Template mode should exclude VAS configs."""
        vas = AppleVASConfig(merchant_id="pass.com.test", key_slot=1)
        config = VTAPConfig(vas_configs=[vas])
        generator = ConfigGenerator(config)

        result = generator.generate_template()

        assert "VAS1MerchantID" not in result
        assert "{% for passinfo in passes %}" in result

    def test_generate_template_excludes_smarttap(self):
        """Template mode should exclude SmartTap configs."""
        st = GoogleSmartTapConfig(collector_id="12345678", key_slot=1)
        config = VTAPConfig(smarttap_configs=[st])
        generator = ConfigGenerator(config)

        result = generator.generate_template()

        assert "ST1CollectorID" not in result

    def test_generate_template_includes_keyboard(self):
        """Template mode should include keyboard config."""
        kb = KeyboardConfig(log_mode=True, source="AG")
        config = VTAPConfig(keyboard=kb)
        generator = ConfigGenerator(config)

        result = generator.generate_template()

        assert "KBLogMode=1" in result
        assert "KBSource=AG" in result

    def test_generate_template_includes_jinja_placeholder(self):
        """Template mode should include Jinja2 placeholder."""
        config = VTAPConfig()
        generator = ConfigGenerator(config)

        result = generator.generate_template()

        assert "{% for passinfo in passes %}" in result
        assert "{% if passinfo.apple %}" in result
        assert "{% if passinfo.google %}" in result
        assert "{% endfor %}" in result

    def test_generate_template_has_correct_structure(self):
        """Template should have passes section before static config."""
        kb = KeyboardConfig(log_mode=True)
        config = VTAPConfig(keyboard=kb)
        generator = ConfigGenerator(config)

        result = generator.generate_template()

        # Jinja block should come before keyboard config
        jinja_pos = result.find("{% for passinfo")
        kb_pos = result.find("KBLogMode")
        assert jinja_pos < kb_pos
```

#### 1.2 Export-Dialog Tests (`tests/unit/test_tui_export.py`)

```python
"""Unit tests for TUI Export Dialog."""

import pytest
from unittest.mock import patch, MagicMock

class TestExportDialog:
    """Tests for ExportDialog ModalScreen."""

    @pytest.mark.asyncio
    async def test_dialog_opens_with_ctrl_e(self):
        """Ctrl+E should open the export dialog."""
        from vtap100.tui.app import VTAPEditorApp

        app = VTAPEditorApp()
        async with app.run_test() as pilot:
            await pilot.pause()
            await pilot.press("ctrl+e")

            # Dialog should be visible
            dialog = app.query_one("ExportDialog")
            assert dialog is not None

    @pytest.mark.asyncio
    async def test_dialog_has_format_options(self):
        """Dialog should have full and template export options."""
        from vtap100.tui.app import VTAPEditorApp

        app = VTAPEditorApp()
        async with app.run_test() as pilot:
            await pilot.pause()
            await pilot.press("ctrl+e")

            # Should have radio buttons for format
            dialog = app.query_one("ExportDialog")
            radios = dialog.query("RadioButton")
            assert len(radios) >= 2

    @pytest.mark.asyncio
    async def test_template_export_excludes_passes(self, tmp_path):
        """Template export should exclude VAS/SmartTap."""
        from vtap100.tui.app import VTAPEditorApp
        from vtap100.models.vas import AppleVASConfig
        from vtap100.models.keyboard import KeyboardConfig

        output_file = tmp_path / "template.txt"
        app = VTAPEditorApp(output_path=output_file)

        async with app.run_test() as pilot:
            await pilot.pause()

            # Add configs
            app.config.vas_configs.append(
                AppleVASConfig(merchant_id="pass.com.test", key_slot=1)
            )
            app.config.keyboard = KeyboardConfig(log_mode=True)

            # Open dialog, select template mode, export
            await pilot.press("ctrl+e")
            # ... select template radio, click export

            content = output_file.read_text()
            assert "VAS1MerchantID" not in content
            assert "KBLogMode=1" in content
            assert "{% for passinfo" in content

    @pytest.mark.asyncio
    async def test_clipboard_export(self):
        """Clipboard option should copy to clipboard."""
        from vtap100.tui.app import VTAPEditorApp

        app = VTAPEditorApp()
        async with app.run_test() as pilot:
            await pilot.pause()

            with patch('pyperclip.copy') as mock_copy:
                await pilot.press("ctrl+e")
                # ... select clipboard, click export

                mock_copy.assert_called_once()

    @pytest.mark.asyncio
    async def test_cancel_closes_dialog(self):
        """Cancel button should close dialog without action."""
        from vtap100.tui.app import VTAPEditorApp

        app = VTAPEditorApp()
        async with app.run_test() as pilot:
            await pilot.pause()
            await pilot.press("ctrl+e")

            # Press cancel or Escape
            await pilot.press("escape")

            # Dialog should be gone
            dialogs = app.query("ExportDialog")
            assert len(dialogs) == 0
```

### Phase 2: Generator erweitern

#### 2.1 Jinja2-Template-Konstante

```python
# In generator.py

JINJA_PASSES_TEMPLATE = """\
; === MOBILE WALLET PASSES ===
; (Generated by Jinja2 template - do not edit manually)
{% for passinfo in passes %}
{% if passinfo.apple %}
VAS{{ passinfo.slot }}MerchantID={{ passinfo.apple.merchant_id }}
VAS{{ passinfo.slot }}KeySlot={{ passinfo.slot }}
{% if passinfo.apple.merchant_url %}VAS{{ passinfo.slot }}MerchantURL={{ passinfo.apple.merchant_url }}{% endif %}
{% endif %}
{% if passinfo.google %}
ST{{ passinfo.slot }}CollectorID={{ passinfo.google.collector_id }}
ST{{ passinfo.slot }}KeySlot={{ passinfo.slot }}
{% if passinfo.google.key_version is defined %}ST{{ passinfo.slot }}KeyVersion={{ passinfo.google.key_version }}{% endif %}
{% endif %}
{% endfor %}
"""
```

#### 2.2 Neue Methode `generate_template()`

```python
def generate_template(self, comment: str | None = None) -> str:
    """Generate a Jinja2 template config without VAS/SmartTap.

    Args:
        comment: Optional comment to include after the header.

    Returns:
        Config content with Jinja2 placeholder for passes.
    """
    lines: list[str] = []

    # Header
    lines.append(self.HEADER)

    if comment:
        lines.append(f"; {comment}")

    # Jinja2 placeholder for passes
    lines.append(JINJA_PASSES_TEMPLATE)

    # Static configuration (excluding VAS/SmartTap)
    lines.append("; === STATIC CONFIGURATION ===")

    # Keyboard, NFC, DESFire, Feedback (same as generate())
    if self.config.keyboard:
        lines.append("; Keyboard Emulation")
        lines.extend(self.config.keyboard.to_config_lines())

    # ... rest same as generate()

    return "\n".join(lines)
```

### Phase 3: Export-Dialog implementieren

#### 3.1 ExportDialog ModalScreen

```python
# src/vtap100/tui/screens/export_dialog.py

from enum import Enum
from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Label, RadioButton, RadioSet, Static

from vtap100.tui.i18n import t


class ExportFormat(str, Enum):
    FULL = "full"
    TEMPLATE = "template"


class ExportTarget(str, Enum):
    FILE = "file"
    CLIPBOARD = "clipboard"


class ExportDialog(ModalScreen[tuple[ExportFormat, ExportTarget] | None]):
    """Modal dialog for export options."""

    CSS = """
    ExportDialog {
        align: center middle;
    }

    #export-dialog-container {
        width: 50;
        height: auto;
        border: thick $primary;
        background: $surface;
        padding: 1 2;
    }

    #export-buttons {
        width: 100%;
        height: auto;
        align: right middle;
        margin-top: 1;
    }
    """

    BINDINGS = [
        ("escape", "cancel", "Cancel"),
    ]

    def compose(self) -> ComposeResult:
        with Container(id="export-dialog-container"):
            yield Label(t("export.title"), classes="dialog-title")

            yield Label(t("export.format_label"))
            with RadioSet(id="format-options"):
                yield RadioButton(t("export.format_full"), id="format-full", value=True)
                yield RadioButton(t("export.format_template"), id="format-template")

            yield Static(t("export.template_hint"), id="template-hint")

            yield Label(t("export.target_label"))
            with RadioSet(id="target-options"):
                yield RadioButton(t("export.target_file"), id="target-file", value=True)
                yield RadioButton(t("export.target_clipboard"), id="target-clipboard")

            with Horizontal(id="export-buttons"):
                yield Button(t("common.buttons.cancel"), id="cancel-btn", variant="default")
                yield Button(t("export.button"), id="export-btn", variant="primary")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "cancel-btn":
            self.dismiss(None)
        elif event.button.id == "export-btn":
            format_set = self.query_one("#format-options", RadioSet)
            target_set = self.query_one("#target-options", RadioSet)

            export_format = (
                ExportFormat.TEMPLATE
                if format_set.pressed_index == 1
                else ExportFormat.FULL
            )
            export_target = (
                ExportTarget.CLIPBOARD
                if target_set.pressed_index == 1
                else ExportTarget.FILE
            )

            self.dismiss((export_format, export_target))

    def action_cancel(self) -> None:
        self.dismiss(None)
```

#### 3.2 App-Integration

```python
# In app.py - neue Binding und Action

BINDINGS = [
    # ... existing bindings
    ("ctrl+e", "export", "Export"),
]

async def action_export(self) -> None:
    """Open the export dialog."""
    from vtap100.tui.screens.export_dialog import ExportDialog, ExportFormat, ExportTarget

    def handle_export(result: tuple[ExportFormat, ExportTarget] | None) -> None:
        if result is None:
            return  # Cancelled

        export_format, export_target = result
        generator = ConfigGenerator(self.config)

        if export_format == ExportFormat.TEMPLATE:
            content = generator.generate_template()
        else:
            content = generator.generate()

        if export_target == ExportTarget.CLIPBOARD:
            try:
                import pyperclip
                pyperclip.copy(content)
                self.notify(t("export.copied_to_clipboard"))
            except ImportError:
                self.notify(t("export.clipboard_error"), severity="error")
        else:
            if self.output_path:
                self.output_path.write_text(content, encoding="utf-8")
                self.notify(t("export.saved_to_file", path=str(self.output_path)))
            else:
                self.notify(t("export.no_output_path"), severity="error")

    self.push_screen(ExportDialog(), handle_export)
```

### Phase 4: i18n erweitern

#### 4.1 Deutsche Übersetzungen

```yaml
# In de.yaml

export:
  title: "Export"
  format_label: "Exportformat:"
  format_full: "Vollständige config.txt"
  format_template: "Template (ohne VAS/SmartTap)"
  template_hint: |
    Template-Modus exportiert einen Jinja2-Platzhalter
    für Wallet-Passes. Keyboard, NFC, DESFire und
    LED/Beep werden vollständig exportiert.
  target_label: "Ziel:"
  target_file: "In Datei speichern"
  target_clipboard: "In Zwischenablage kopieren"
  button: "Exportieren"
  copied_to_clipboard: "In Zwischenablage kopiert"
  saved_to_file: "Gespeichert: {path}"
  no_output_path: "Kein Ausgabepfad angegeben"
  clipboard_error: "Clipboard nicht verfügbar (pyperclip fehlt)"
```

#### 4.2 Englische Übersetzungen

```yaml
# In en.yaml

export:
  title: "Export"
  format_label: "Export format:"
  format_full: "Full config.txt"
  format_template: "Template (without VAS/SmartTap)"
  template_hint: |
    Template mode exports a Jinja2 placeholder for
    wallet passes. Keyboard, NFC, DESFire and
    LED/Beep are fully exported.
  target_label: "Target:"
  target_file: "Save to file"
  target_clipboard: "Copy to clipboard"
  button: "Export"
  copied_to_clipboard: "Copied to clipboard"
  saved_to_file: "Saved: {path}"
  no_output_path: "No output path specified"
  clipboard_error: "Clipboard not available (pyperclip missing)"
```

### Phase 5: Optional - pyperclip Dependency

```toml
# In pyproject.toml

[project.optional-dependencies]
clipboard = ["pyperclip>=1.8.0"]
```

Oder als Standard-Dependency wenn Clipboard-Support wichtig ist.

## Reihenfolge der Implementierung

1. **Tests schreiben** (TDD!)
   - [ ] `test_generator.py` - Template-Generierung Tests
   - [ ] `test_tui_export.py` - Dialog Tests

2. **Generator erweitern**
   - [ ] `JINJA_PASSES_TEMPLATE` Konstante
   - [ ] `generate_template()` Methode

3. **Export-Dialog**
   - [ ] `export_dialog.py` - ModalScreen
   - [ ] CSS Styling

4. **App-Integration**
   - [ ] Neues Binding `ctrl+e`
   - [ ] `action_export()` Methode

5. **i18n**
   - [ ] `de.yaml` erweitern
   - [ ] `en.yaml` erweitern

6. **Optional**
   - [ ] `pyperclip` Dependency
   - [ ] Dokumentation

## Offene Fragen

1. **Dateiendung**: Soll Template als `.j2` oder `.txt` gespeichert werden?
2. **Clipboard-Fallback**: Was tun wenn `pyperclip` nicht installiert ist?
3. **Template anpassbar?**: Soll der Jinja2-Block anpassbar sein oder fix?

## Geschätzter Aufwand

- Tests: ~100 Zeilen
- Generator: ~50 Zeilen
- Export-Dialog: ~150 Zeilen
- i18n: ~40 Zeilen
- Integration: ~30 Zeilen

**Gesamt: ~370 Zeilen Code**
