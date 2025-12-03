"""Export Dialog for VTAP100 TUI Editor.

Provides a modal dialog for exporting configurations in different formats:
- Full config.txt (all settings)
- Template mode (Jinja2 placeholder for VAS/SmartTap, static config included)

Export targets:
- File (saves to output path with editable filename)
- Clipboard (copies content to system clipboard)
"""

from __future__ import annotations

from enum import Enum
from pathlib import Path
from textual.app import ComposeResult
from textual.containers import Container
from textual.containers import Horizontal
from textual.screen import ModalScreen
from textual.widgets import Button
from textual.widgets import Input
from textual.widgets import Label
from textual.widgets import RadioButton
from textual.widgets import RadioSet
from textual.widgets import Static
from vtap100.tui.i18n import t


class ExportFormat(str, Enum):
    """Export format options."""

    FULL = "full"
    TEMPLATE = "template"


class ExportTarget(str, Enum):
    """Export target options."""

    FILE = "file"
    CLIPBOARD = "clipboard"


class ExportDialog(ModalScreen[tuple[ExportFormat, ExportTarget, Path | None] | None]):
    """Modal dialog for export options.

    Returns a tuple of (format, target, file_path) on export, or None if cancelled.
    file_path is None when target is clipboard.
    """

    CSS = """
    ExportDialog {
        align: center middle;
    }

    #export-dialog-container {
        width: 60;
        height: auto;
        border: thick $primary;
        background: $surface;
        padding: 1 2;
    }

    .dialog-title {
        text-style: bold;
        margin-bottom: 1;
    }

    .section-label {
        margin-top: 1;
    }

    #template-hint {
        margin: 1 0;
        padding: 1;
        background: $surface-lighten-1;
        color: $text-muted;
    }

    #filename-container {
        width: 100%;
        height: auto;
        margin-top: 1;
    }

    #filename-input {
        width: 100%;
    }

    #export-buttons {
        width: 100%;
        height: auto;
        align: right middle;
        margin-top: 1;
    }

    #export-buttons Button {
        margin-left: 1;
    }
    """

    BINDINGS = [
        ("escape", "cancel", "Cancel"),
    ]

    def __init__(self, default_filename: str = "") -> None:
        """Initialize the export dialog.

        Args:
            default_filename: Default value for the filename input field.
        """
        super().__init__()
        self._default_filename = default_filename

    def compose(self) -> ComposeResult:
        """Compose the export dialog layout."""
        with Container(id="export-dialog-container"):
            yield Label(t("export.title"), classes="dialog-title")

            yield Label(t("export.format_label"), classes="section-label")
            with RadioSet(id="format-options"):
                yield RadioButton(t("export.format_full"), id="format-full", value=True)
                yield RadioButton(t("export.format_template"), id="format-template")

            yield Static(t("export.template_hint"), id="template-hint")

            yield Label(t("export.target_label"), classes="section-label")
            with RadioSet(id="target-options"):
                yield RadioButton(t("export.target_file"), id="target-file", value=True)
                yield RadioButton(t("export.target_clipboard"), id="target-clipboard")

            with Container(id="filename-container"):
                yield Label(t("export.filename_label"), classes="section-label")
                yield Input(
                    value=self._default_filename,
                    placeholder=t("export.filename_placeholder"),
                    id="filename-input",
                )

            with Horizontal(id="export-buttons"):
                yield Button(t("common.buttons.cancel"), id="cancel-btn", variant="default")
                yield Button(t("export.button"), id="export-btn", variant="primary")

    def on_radio_set_changed(self, event: RadioSet.Changed) -> None:
        """Handle radio set changes to show/hide filename input."""
        if event.radio_set.id == "target-options":
            filename_input = self.query_one("#filename-input", Input)
            filename_label = self.query_one("#filename-container Label")
            # Show filename input only when file target is selected (index 0)
            is_file_target = event.index == 0
            filename_input.display = is_file_target
            filename_label.display = is_file_target

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "cancel-btn":
            self.dismiss(None)
        elif event.button.id == "export-btn":
            format_set = self.query_one("#format-options", RadioSet)
            target_set = self.query_one("#target-options", RadioSet)
            filename_input = self.query_one("#filename-input", Input)

            export_format = (
                ExportFormat.TEMPLATE if format_set.pressed_index == 1 else ExportFormat.FULL
            )
            export_target = (
                ExportTarget.CLIPBOARD if target_set.pressed_index == 1 else ExportTarget.FILE
            )

            # Get file path from input (only relevant for file target)
            file_path: Path | None = None
            if export_target == ExportTarget.FILE and filename_input.value.strip():
                file_path = Path(filename_input.value.strip())

            self.dismiss((export_format, export_target, file_path))

    def action_cancel(self) -> None:
        """Cancel and close the dialog."""
        self.dismiss(None)
