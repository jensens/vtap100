"""Export Dialog for VTAP100 TUI Editor.

Provides a modal dialog for exporting configurations in different formats:
- Full config.txt (all settings)
- Template mode (Jinja2 placeholder for VAS/SmartTap, static config included)

Export targets:
- File (saves to output path)
- Clipboard (copies content to system clipboard)
"""

from enum import Enum

from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual.screen import ModalScreen
from textual.widgets import Button, Label, RadioButton, RadioSet, Static

from vtap100.tui.i18n import t


class ExportFormat(str, Enum):
    """Export format options."""

    FULL = "full"
    TEMPLATE = "template"


class ExportTarget(str, Enum):
    """Export target options."""

    FILE = "file"
    CLIPBOARD = "clipboard"


class ExportDialog(ModalScreen[tuple[ExportFormat, ExportTarget] | None]):
    """Modal dialog for export options.

    Returns a tuple of (format, target) on export, or None if cancelled.
    """

    CSS = """
    ExportDialog {
        align: center middle;
    }

    #export-dialog-container {
        width: 55;
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

    def compose(self) -> ComposeResult:
        """Compose the export dialog layout."""
        with Container(id="export-dialog-container"):
            yield Label(t("export.title"), classes="dialog-title")

            yield Label(t("export.format_label"), classes="section-label")
            with RadioSet(id="format-options"):
                yield RadioButton(
                    t("export.format_full"), id="format-full", value=True
                )
                yield RadioButton(t("export.format_template"), id="format-template")

            yield Static(t("export.template_hint"), id="template-hint")

            yield Label(t("export.target_label"), classes="section-label")
            with RadioSet(id="target-options"):
                yield RadioButton(t("export.target_file"), id="target-file", value=True)
                yield RadioButton(
                    t("export.target_clipboard"), id="target-clipboard"
                )

            with Horizontal(id="export-buttons"):
                yield Button(
                    t("common.buttons.cancel"), id="cancel-btn", variant="default"
                )
                yield Button(t("export.button"), id="export-btn", variant="primary")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
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
        """Cancel and close the dialog."""
        self.dismiss(None)
