"""Save Dialog for VTAP100 TUI Editor.

Provides a simple modal dialog for entering a filename when saving
and no output path is specified.
"""

from __future__ import annotations

from pathlib import Path
from textual.app import ComposeResult
from textual.containers import Container
from textual.containers import Horizontal
from textual.screen import ModalScreen
from textual.widgets import Button
from textual.widgets import Input
from textual.widgets import Label
from vtap100.tui.i18n import t


class SaveDialog(ModalScreen[Path | None]):
    """Modal dialog for entering a save filename.

    Returns the Path to save to, or None if cancelled.
    """

    CSS = """
    SaveDialog {
        align: center middle;
    }

    #save-dialog-container {
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

    #filename-input {
        width: 100%;
        margin-top: 1;
    }

    #save-buttons {
        width: 100%;
        height: auto;
        align: right middle;
        margin-top: 1;
    }

    #save-buttons Button {
        margin-left: 1;
    }
    """

    BINDINGS = [
        ("escape", "cancel", "Cancel"),
        ("enter", "confirm", "Save"),
    ]

    def __init__(self, default_filename: str = "config.txt") -> None:
        """Initialize the save dialog.

        Args:
            default_filename: Default value for the filename input field.
        """
        super().__init__()
        self._default_filename = default_filename

    def compose(self) -> ComposeResult:
        """Compose the save dialog layout."""
        with Container(id="save-dialog-container"):
            yield Label(t("save.title"), classes="dialog-title")
            yield Label(t("save.filename_label"))
            yield Input(
                value=self._default_filename,
                placeholder=t("save.filename_placeholder"),
                id="filename-input",
            )

            with Horizontal(id="save-buttons"):
                yield Button(t("common.buttons.cancel"), id="cancel-btn", variant="default")
                yield Button(t("common.buttons.save"), id="save-btn", variant="primary")

    def on_mount(self) -> None:
        """Focus the input and select all text when dialog opens."""
        input_field = self.query_one("#filename-input", Input)
        input_field.focus()
        input_field.action_select_all()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "cancel-btn":
            self.dismiss(None)
        elif event.button.id == "save-btn":
            self._save()

    def action_cancel(self) -> None:
        """Cancel and close the dialog."""
        self.dismiss(None)

    def action_confirm(self) -> None:
        """Confirm and save."""
        self._save()

    def _save(self) -> None:
        """Process save action."""
        filename_input = self.query_one("#filename-input", Input)
        filename = filename_input.value.strip()

        if filename:
            self.dismiss(Path(filename))
        else:
            # Don't dismiss if no filename entered
            filename_input.focus()
