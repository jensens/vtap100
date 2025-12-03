"""Quit Confirmation Dialog for VTAP100 TUI Editor.

Provides a modal dialog asking the user to confirm quitting
when there are unsaved changes.
"""

from textual.app import ComposeResult
from textual.containers import Container
from textual.containers import Horizontal
from textual.screen import ModalScreen
from textual.widgets import Button
from textual.widgets import Label
from vtap100.tui.i18n import t


class QuitConfirmDialog(ModalScreen[bool | None]):
    """Modal dialog for quit confirmation.

    Returns True if the user confirms quit, None if cancelled.
    """

    CSS = """
    QuitConfirmDialog {
        align: center middle;
    }

    #quit-dialog-container {
        width: 50;
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

    #quit-buttons {
        width: 100%;
        height: auto;
        align: right middle;
        margin-top: 1;
    }

    #quit-buttons Button {
        margin-left: 1;
    }
    """

    BINDINGS = [
        ("escape", "cancel", "Cancel"),
    ]

    def compose(self) -> ComposeResult:
        """Compose the quit confirmation dialog layout."""
        with Container(id="quit-dialog-container"):
            yield Label(t("quit.title"), classes="dialog-title")
            yield Label(t("quit.message"), classes="dialog-message")

            with Horizontal(id="quit-buttons"):
                yield Button(t("common.buttons.cancel"), id="cancel-btn", variant="default")
                yield Button(t("quit.button"), id="quit-btn", variant="error")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "cancel-btn":
            self.dismiss(None)
        elif event.button.id == "quit-btn":
            self.dismiss(True)

    def action_cancel(self) -> None:
        """Cancel and close the dialog."""
        self.dismiss(None)
