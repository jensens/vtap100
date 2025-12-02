# VTAP100 Textual Editor - Implementierungsplan

## Übersicht

Ein TUI-basierter Editor für VTAP100-Konfigurationen mit Textual.

**Ziele:**
- Hauptbereiche auswählen (Apple VAS, Google Smart Tap, Keyboard, NFC, DESFire, LED/Beep)
- Formulare zum Bearbeiten, Hinzufügen, Entfernen von Konfigurationen
- Kontextbezogene Hilfe ("on-the-fingertips")
- Live-Vorschau der config.txt

---

## 1. Architektur-Entscheidungen

### 1.1 Form-System: Explizite Definitionen
- Schnelle Implementierung (~1 Woche)
- Explizite Form-Definitionen pro Bereich statt generischer Pydantic-Reflection
- Einfacher zu debuggen und zu erweitern

### 1.2 Layout: 3-Panel mit Live-Preview
```
+------------------+----------------------------------+-------------------+
|   SIDEBAR        |          MAIN CONTENT            |   HELP PANEL      |
|   (Navigation)   |          (Forms/Edit)            |   (Kontext ^D)    |
+------------------+----------------------------------+-------------------+
|                  |                                  |                   |
| [x] Apple VAS    |  Merchant ID:                    | ## Merchant ID    |
|     ├─ VAS #1    |  [pass.com.example.myapp    ]    |                   |
|     └─ VAS #2    |                                  | Muss mit 'pass.'  |
| [ ] Google ST    |  Key Slot:                       | beginnen.         |
| [x] Keyboard     |  [ 1  v ]                        |                   |
| [ ] NFC Tags     |                                  | Beispiel:         |
| [ ] DESFire      |  [Entfernen] [Duplizieren]       | pass.com.acme.app |
| [ ] LED/Beep     |                                  |                   |
+------------------+----------------------------------+-------------------+
|                       LIVE PREVIEW (toggle ^O)                         |
| !VTAPconfig                                                            |
| VAS1MerchantID=pass.com.example.myapp                                  |
+------------------------------------------------------------------------+
```

### 1.3 Hilfe-System: Separate YAML-Dateien
- Hilfe aus `tui/help/*.yaml` laden
- Kontextbezogen: Hilfe-Panel zeigt immer Hilfe zum fokussierten Feld
- Kann unabhängig vom Code gepflegt werden

### 1.4 CLI-Integration
```bash
vtap100 editor                    # Neue leere Konfiguration
vtap100 editor config.txt         # Bestehende Datei öffnen
vtap100 editor --output out.txt   # Ausgabedatei festlegen
```

### 1.5 Persistenz: Kommentare in config.txt
- Kein separates JSON/YAML für Editor-Zustand
- Metadaten als Kommentare in config.txt:
```ini
!VTAPconfig
; @editor:expanded=vas,keyboard
; @editor:selected=vas.0
; Apple VAS Configuration
VAS1MerchantID=pass.com.example.myapp
```

---

## 2. Dateistruktur

```
src/vtap100/
├── parser.py                   # Config.txt Parser (Text → VTAPConfig)
├── generator.py                # Config.txt Generator (VTAPConfig → Text)
├── tui/
│   ├── __init__.py              # Entry Point: run(filename)
│   ├── app.py                   # VTAPEditorApp
│   ├── screens/
│   │   ├── __init__.py
│   │   └── editor.py            # Haupt-Editor-Screen
│   ├── widgets/
│   │   ├── __init__.py
│   │   ├── sidebar.py           # Navigation Tree
│   │   ├── help_panel.py        # Kontextbezogene Hilfe
│   │   ├── preview.py           # Live config.txt Preview
│   │   └── forms/
│   │       ├── __init__.py
│   │       ├── base.py          # BaseConfigForm
│   │       ├── vas.py           # Apple VAS Form
│   │       ├── smarttap.py      # Google Smart Tap Form
│   │       ├── keyboard.py      # Keyboard Form
│   │       ├── nfc.py           # NFC Tags Form
│   │       ├── desfire.py       # DESFire Form
│   │       └── feedback.py      # LED/Beep Form
│   ├── i18n/                    # Internationalisierung (DE/EN)
│   │   ├── __init__.py          # Language, t(), set_language(), get_language()
│   │   └── translations/
│   │       ├── de.yaml          # Deutsche Übersetzungen
│   │       └── en.yaml          # Englische Übersetzungen
│   ├── help/
│   │   ├── __init__.py          # HelpLoader
│   │   ├── vas.yaml             # Hilfe für VAS-Felder
│   │   ├── smarttap.yaml
│   │   ├── keyboard.yaml
│   │   ├── nfc.yaml
│   │   ├── desfire.yaml
│   │   └── feedback.yaml
│   └── styles/
│       └── editor.tcss          # Textual CSS
```

---

## 3. Komponenten-Design

### 3.1 VTAPEditorApp (app.py)

```python
class VTAPEditorApp(App):
    """Textual App für VTAP100 Konfiguration."""

    CSS_PATH = "styles/editor.tcss"
    BINDINGS = [
        ("ctrl+d", "toggle_help", "Doku"),       # Dokumentation/Hilfe
        ("ctrl+o", "toggle_preview", "Output"),  # Output/Preview
        ("ctrl+l", "toggle_language", "DE/EN"),  # Sprache wechseln
        ("ctrl+s", "save", "Save"),
        ("ctrl+q", "quit", "Quit"),
    ]

    # Reaktiver State
    config: reactive[VTAPConfig]
    current_field: reactive[str]  # Für kontextbezogene Hilfe

    def __init__(self, filename: Path | None = None):
        super().__init__()
        self.filename = filename
        self.config = self._load_config(filename)
```

### 3.2 Sidebar (widgets/sidebar.py)

```python
class ConfigSidebar(Widget):
    """Navigation mit Tree für alle Konfigurationsbereiche."""

    SECTIONS = [
        ("vas", "Apple VAS", "vas_configs"),
        ("smarttap", "Google Smart Tap", "smarttap_configs"),
        ("keyboard", "Keyboard", "keyboard"),
        ("nfc", "NFC Tags", "nfc"),
        ("desfire", "DESFire", "desfire"),
        ("feedback", "LED/Beep", "feedback"),
    ]

    def compose(self) -> ComposeResult:
        with Tree("Konfiguration") as tree:
            for section_id, label, attr in self.SECTIONS:
                # Badge mit Anzahl/Status
                items = self._get_section_items(section_id)
                badge = f" [{len(items)}]" if items else ""
                tree.root.add(f"{label}{badge}", data=section_id)
        yield tree
```

### 3.3 HelpPanel (widgets/help_panel.py)

```python
class HelpPanel(Widget):
    """Kontextbezogenes Hilfe-Panel."""

    current_context: reactive[str] = reactive("")

    def __init__(self):
        super().__init__()
        self.help_data = HelpLoader.load_all()

    def watch_current_context(self, context: str) -> None:
        """Update wenn sich der Kontext ändert."""
        # context = "vas.merchant_id" oder "keyboard.source"
        self.refresh()

    def render(self) -> RenderableType:
        help_content = self.help_data.get(self.current_context, {})
        return Markdown(self._format_help(help_content))
```

### 3.4 BaseConfigForm (widgets/forms/base.py)

```python
class BaseConfigForm(Widget):
    """Basis für alle Konfigurations-Formulare."""

    SECTION_NAME: str = ""  # Überschreiben in Subklassen

    def on_input_changed(self, event: Input.Changed) -> None:
        """Bei Feldänderung: Validieren und Hilfe aktualisieren."""
        field_name = event.input.id

        # Hilfe-Kontext setzen
        self.post_message(HelpContextChanged(f"{self.SECTION_NAME}.{field_name}"))

        # Validieren
        self._validate_field(field_name, event.value)

        # Live-Preview triggern
        self.post_message(ConfigChanged())

    def on_input_focus(self, event: Input.Focus) -> None:
        """Bei Fokus: Hilfe-Kontext setzen."""
        field_name = event.input.id
        self.post_message(HelpContextChanged(f"{self.SECTION_NAME}.{field_name}"))
```

### 3.5 VASConfigForm (widgets/forms/vas.py)

```python
class VASConfigForm(BaseConfigForm):
    """Formular für Apple VAS Konfiguration."""

    SECTION_NAME = "vas"

    def __init__(self, config: AppleVASConfig | None = None, index: int = 0):
        super().__init__()
        self.index = index
        self._config = config or AppleVASConfig(merchant_id="pass.")

    def compose(self) -> ComposeResult:
        yield Label("Apple VAS Konfiguration", classes="form-title")

        yield Label("Merchant ID")
        yield Input(
            value=self._config.merchant_id,
            placeholder="pass.com.example.myapp",
            id="merchant_id",
        )

        yield Label("Key Slot")
        yield Select(
            [(str(i), str(i)) for i in range(7)],
            value=str(self._config.key_slot),
            id="key_slot",
        )

        yield Label("Merchant URL (optional)")
        yield Input(
            value=self._config.merchant_url or "",
            placeholder="https://...",
            id="merchant_url",
        )

        with Horizontal():
            yield Button("Entfernen", variant="error", id="remove")
            yield Button("Duplizieren", id="duplicate")
```

---

## 4. Hilfe-System (YAML-Format)

### 4.1 Beispiel: tui/help/vas.yaml

```yaml
section:
  title: Apple VAS (Value Added Services)
  description: |
    Konfiguration für Apple Wallet Pässe.
    Bis zu 6 verschiedene Pass-Konfigurationen möglich.

fields:
  merchant_id:
    title: Merchant ID (Pass Type ID)
    description: |
      Die eindeutige ID deines Apple Wallet Passes.
      Wird im Apple Developer Portal erstellt.
    format: "Muss mit 'pass.' beginnen"
    example: "pass.com.example.loyalty"
    tip: |
      Findest du im Apple Developer Portal unter:
      Certificates, Identifiers & Profiles > Pass Type IDs

  key_slot:
    title: Key Slot
    description: |
      Slot (0-6) in dem der private Schlüssel gespeichert ist.
    values:
      - value: 0
        label: Automatisch
      - value: 1-6
        label: Spezifischer Slot
    tip: |
      Der Schlüssel muss als private1.pem (für Slot 1) etc.
      auf den Reader kopiert werden.

  merchant_url:
    title: Merchant URL
    description: Optional - URL für Pass-Präsentation
    required: false
```

### 4.2 HelpLoader

```python
# tui/help/__init__.py
import yaml
from pathlib import Path
from functools import lru_cache

class HelpLoader:
    """Lädt Hilfe-Inhalte aus YAML-Dateien."""

    HELP_DIR = Path(__file__).parent

    @classmethod
    @lru_cache(maxsize=1)
    def load_all(cls) -> dict[str, dict]:
        """Lädt alle Hilfe-Dateien und erstellt flache Struktur."""
        result = {}
        for yaml_file in cls.HELP_DIR.glob("*.yaml"):
            section = yaml_file.stem  # "vas", "keyboard", etc.
            with open(yaml_file) as f:
                data = yaml.safe_load(f)

            # Section-Level Hilfe
            result[section] = data.get("section", {})

            # Feld-Level Hilfe: "vas.merchant_id"
            for field_name, field_help in data.get("fields", {}).items():
                result[f"{section}.{field_name}"] = field_help

        return result
```

---

## 5. i18n System (Internationalisierung)

### 5.1 Architektur

```python
# tui/i18n/__init__.py
from enum import Enum

class Language(Enum):
    DE = "de"
    EN = "en"

_current_language = Language.DE

def set_language(lang: Language | str) -> None:
    """Sprache setzen."""
    global _current_language
    if isinstance(lang, str):
        lang = Language(lang)
    _current_language = lang

def get_language() -> Language:
    """Aktuelle Sprache abfragen."""
    return _current_language

def t(key: str, **kwargs) -> str:
    """Übersetzung für Key mit Platzhalter-Substitution."""
    # Lädt aus translations/{de,en}.yaml
    # z.B. t("common.buttons.save") → "Speichern" (DE) / "Save" (EN)
    # z.B. t("common.labels.slot", num=3) → "Slot 3"
    ...
```

### 5.2 YAML-Struktur

```yaml
# translations/de.yaml
common:
  buttons:
    save: "Speichern"
    add: "Hinzufügen"
    remove: "Entfernen"
    duplicate: "Duplizieren"
  labels:
    configuration: "Konfiguration"
    slot: "Slot {num}"
    auto: "Auto"
  messages:
    config_saved: "Konfiguration gespeichert"
    config_added: "{name} Konfiguration hinzugefügt"

sections:
  vas:
    label: "Apple VAS"
    new_title: "Neue VAS Konfiguration"
    edit_title: "VAS #{num} bearbeiten"

forms:
  vas:
    merchant_id: "Merchant ID (Pass Type ID)"
    merchant_id_placeholder: "pass.com.example.myapp"

help:
  vas:
    section:
      title: "Apple VAS Konfiguration"
      description: "..."
    fields:
      merchant_id:
        title: "Merchant ID"
        description: "..."
```

### 5.3 Sprachwechsel mit State-Erhalt

Bei Sprachwechsel (Ctrl+L) wird:
1. Aktuelle Section und Form-Werte gespeichert
2. Tree-Expansion-State gespeichert
3. Sprache gewechselt
4. Sidebar neu gerendert
5. Tree-Expansion-State wiederhergestellt
6. Form mit neuen Labels, aber alten Werten neu geladen

---

## 6. Speichern mit Metadaten

### 6.1 Config-Parser erweitern

```python
# tui/parser.py
import re
from vtap100.models.config import VTAPConfig

class ConfigParser:
    """Parst config.txt mit Editor-Metadaten."""

    METADATA_PATTERN = re.compile(r"^;\s*@editor:(\w+)=(.+)$")

    @classmethod
    def parse(cls, content: str) -> tuple[VTAPConfig, dict]:
        """Parst config.txt und extrahiert Metadaten."""
        metadata = {}
        config_lines = []

        for line in content.splitlines():
            match = cls.METADATA_PATTERN.match(line)
            if match:
                key, value = match.groups()
                metadata[key] = value
            else:
                config_lines.append(line)

        # TODO: config_lines zu VTAPConfig parsen
        config = cls._parse_config(config_lines)
        return config, metadata

    @classmethod
    def serialize(cls, config: VTAPConfig, metadata: dict) -> str:
        """Serialisiert VTAPConfig mit Metadaten."""
        from vtap100.generator import ConfigGenerator

        lines = ["!VTAPconfig"]

        # Metadaten als Kommentare
        for key, value in metadata.items():
            lines.append(f"; @editor:{key}={value}")

        # Rest der Konfiguration
        generator = ConfigGenerator(config)
        config_content = generator.generate()
        # Entferne den Header (bereits hinzugefügt)
        config_lines = config_content.split("\n")[1:]
        lines.extend(config_lines)

        return "\n".join(lines)
```

---

## 7. CLI-Integration

### 7.1 cli.py erweitern

```python
@main.command()
@click.argument("filename", required=False, type=click.Path())
@click.option("--output", "-o", type=click.Path(), help="Ausgabedatei")
def editor(filename: str | None, output: str | None) -> None:
    """Öffnet den interaktiven TUI-Editor.

    Examples:
        vtap100 editor                  # Neue Konfiguration
        vtap100 editor config.txt       # Datei öffnen
        vtap100 editor -o output.txt    # Mit Ausgabedatei
    """
    from vtap100.tui import run

    input_path = Path(filename) if filename else None
    output_path = Path(output) if output else input_path

    run(input_path=input_path, output_path=output_path)
```

---

## 8. Keyboard Shortcuts

| Shortcut | Aktion |
|----------|--------|
| `Ctrl+D` | Dokumentation/Hilfe-Panel toggle |
| `Ctrl+O` | Output/Live-Preview toggle |
| `Ctrl+L` | Sprache wechseln (DE/EN) |
| `Ctrl+S` | Speichern |
| `Ctrl+Q` | Beenden |
| `Tab` | Nächstes Feld |
| `Shift+Tab` | Vorheriges Feld |

**Hinweis:** F-Tasten (F1, F2, etc.) wurden vermieden, da sie in VSCode Terminal abgefangen werden.
`Ctrl+H` wurde vermieden, da es im Terminal als Backspace interpretiert wird.

---

## 9. Implementierungsreihenfolge

### Phase 1: Grundgerüst ✓
1. `tui/__init__.py` - Entry Point
2. `tui/app.py` - VTAPEditorApp mit State
3. `tui/screens/editor.py` - 3-Panel Layout
4. `tui/styles/editor.tcss` - Basis-Styling
5. CLI-Integration: `vtap100 editor`

### Phase 2: Sidebar + Navigation ✓
1. `tui/widgets/sidebar.py` - Tree mit Bereichen
2. Section-Auswahl und Navigation
3. Badges für Anzahl/Status

### Phase 3: Erste Forms ✓
1. `tui/widgets/forms/base.py` - BaseConfigForm
2. `tui/widgets/forms/vas.py` - Apple VAS
3. `tui/widgets/forms/smarttap.py` - Google Smart Tap
4. Add/Remove für Listen-Bereiche

### Phase 4: Hilfe-System ✓
1. `tui/help/*.yaml` - Hilfe-Dateien erstellen (vas, smarttap, keyboard, nfc, desfire, feedback)
2. `tui/help/__init__.py` - HelpLoader
3. `tui/widgets/help_panel.py` - Panel Widget
4. Kontextbezogene Updates bei Fokus

### Phase 4b: i18n System ✓ (neu hinzugefügt)
1. `tui/i18n/__init__.py` - Language enum, set_language(), get_language(), t()
2. `tui/i18n/translations/de.yaml` - Deutsche Übersetzungen
3. `tui/i18n/translations/en.yaml` - Englische Übersetzungen
4. Alle UI-Texte zweisprachig (Labels, Buttons, Hilfetexte)
5. Sprachwechsel mit Ctrl+L (erhält Formular-State und Tree-Expansion)

### Phase 5: Weitere Forms ✓
1. `tui/widgets/forms/keyboard.py` - Keyboard Emulation
2. `tui/widgets/forms/nfc.py` - NFC Tag-Typen
3. `tui/widgets/forms/desfire.py` - DESFire Konfiguration
4. `tui/widgets/forms/feedback.py` - LED/Beep Feedback

### Phase 6: Preview + Persistenz ✓
1. [x] `tui/widgets/preview.py` - Live-Preview Widget (ConfigPreview)
2. [x] `vtap100/parser.py` - Config.txt laden (Text → VTAPConfig)
3. [ ] Metadaten in Kommentaren - Optional für v1
4. [x] Speichern-Funktion mit ConfigGenerator (Ctrl+S)
5. [x] Preview aktualisiert bei ConfigAdded/ConfigRemoved/ConfigChanged
6. [x] TUI App lädt bestehende config.txt beim Start (input_path)

### Phase 7: Polish (in Arbeit)
1. [x] Validierungs-Feedback (Farben, error-message/success-message)
2. [x] Keyboard Shortcuts (Ctrl+D, Ctrl+O, Ctrl+L, Ctrl+S, Ctrl+Q)
3. [x] Tests für TUI (test_tui_app.py, test_tui_forms.py, test_tui_sidebar.py, etc.)
4. [x] Error Handling mit Pydantic ValidationError
5. [ ] Slot-Konflikt-Prüfung bei VAS/SmartTap Key-Slots

---

## 10. Abhängigkeiten

```toml
# pyproject.toml
dependencies = [
    "pydantic>=2.0",
    "rich>=13.0",
    "click>=8.0",
    "textual>=0.40.0",  # NEU
    "pyyaml>=6.0",      # Für Hilfe-Dateien
]
```

---

## 11. Kritische Dateien

Diese Dateien müssen vor der Implementierung gelesen werden:

1. **src/vtap100/models/config.py** - VTAPConfig Struktur
2. **src/vtap100/generator.py** - ConfigGenerator für Preview
3. **src/vtap100/cli.py** - CLI-Integration
4. **src/vtap100/models/vas.py** - Referenz für Pydantic-Patterns
5. **docs/configuration/*.md** - Inhalte für Hilfe-YAML

---

## 12. Offene Punkte

**Noch zu implementieren (Optional für v1):**
- [ ] Slot-Konflikt-Warnung bei doppelter Key-Slot-Verwendung
- [ ] Metadaten in config.txt Kommentaren (Editor-Zustand)

**Erledigt:**
- [x] Config.txt Parser (`vtap100/parser.py`) - parst VAS, SmartTap, Keyboard
- [x] TUI App lädt bestehende config.txt beim Start
- [x] Roundtrip-Tests (parse → generate → parse)
- [x] Live-Preview Widget (`tui/widgets/preview.py`)
- [x] Speichern-Funktion mit ConfigGenerator (Ctrl+S)
- [x] Validierungs-Feedback UI (error-message/success-message Klassen)
- [x] Test-Strategie für TUI (Textual Pilot Mode, 445+ Tests, 75% Coverage)
- [x] i18n System (DE/EN Übersetzungen)
- [x] Sprachwechsel mit State-Erhalt (Formular-Werte, Tree-Expansion)
- [x] Alle 6 Konfigurations-Formulare
- [x] Kontextbezogene Hilfe mit HelpPanel
- [x] Keyboard Shortcuts (Ctrl+D, Ctrl+O, Ctrl+L, Ctrl+S, Ctrl+Q)
