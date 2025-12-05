"""Unsaved Changes Dialog for VTAP100 TUI Editor.

Provides a modal dialog asking the user what to do when leaving
a form with unsaved changes.
"""

from enum import Enum
from textual.app import ComposeResult
from textual.containers import Container
from textual.containers import Horizontal
from textual.screen import ModalScreen
from textual.widgets import Button
from textual.widgets import Label
from vtap100.tui.i18n import t


class UnsavedChangesResult(Enum):
    """Result of the unsaved changes dialog."""

    SAVE = "save"
    DISCARD = "discard"
    CANCEL = "cancel"


class UnsavedChangesDialog(ModalScreen[UnsavedChangesResult]):
    """Modal dialog for unsaved changes confirmation.

    Returns UnsavedChangesResult indicating the user's choice:
    - SAVE: Save changes before leaving
    - DISCARD: Leave without saving
    - CANCEL: Stay on current form
    """

    CSS = """
    UnsavedChangesDialog {
        align: center middle;
    }

    #unsaved-dialog-container {
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

    .dialog-message {
        margin: 1 0;
    }

    #unsaved-buttons {
        width: 100%;
        height: auto;
        align: right middle;
        margin-top: 1;
    }

    #unsaved-buttons Button {
        margin-left: 1;
    }
    """

    BINDINGS = [
        ("escape", "cancel", "Cancel"),
    ]

    def compose(self) -> ComposeResult:
        """Compose the unsaved changes dialog layout."""
        with Container(id="unsaved-dialog-container"):
            yield Label(t("unsaved.title"), classes="dialog-title")
            yield Label(t("unsaved.message"), classes="dialog-message")

            with Horizontal(id="unsaved-buttons"):
                yield Button(t("unsaved.buttons.cancel"), id="cancel-btn", variant="default")
                yield Button(t("unsaved.buttons.discard"), id="discard-btn", variant="warning")
                yield Button(t("unsaved.buttons.save"), id="save-btn", variant="success")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "cancel-btn":
            self.dismiss(UnsavedChangesResult.CANCEL)
        elif event.button.id == "discard-btn":
            self.dismiss(UnsavedChangesResult.DISCARD)
        elif event.button.id == "save-btn":
            self.dismiss(UnsavedChangesResult.SAVE)

    def action_cancel(self) -> None:
        """Cancel and close the dialog (triggered by escape key)."""
        self.dismiss(UnsavedChangesResult.CANCEL)
