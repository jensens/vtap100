"""Keyboard emulation configuration form.

Form for editing keyboard emulation settings.
"""

from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widgets import Button, Input, Label, Switch

from vtap100.models.keyboard import KeyboardConfig
from vtap100.tui.i18n import t
from vtap100.tui.widgets.forms.base import BaseConfigForm


class KeyboardConfigForm(BaseConfigForm):
    """Form for editing keyboard emulation configuration.

    This is a single-value section form (not a list like VAS/SmartTap).

    Fields:
    - log_mode: Enable keyboard emulation (switch)
    - source: Data sources for keyboard output
    - prefix: Optional prefix before data
    - postfix: Suffix after data
    - delay_ms: Delay between keystrokes

    Attributes:
        SECTION_NAME: Set to "keyboard".
        MESSAGE_TIMEOUT: Seconds before success messages auto-disappear.
    """

    SECTION_NAME = "keyboard"
    MESSAGE_TIMEOUT = 10.0

    DEFAULT_CSS = """
    KeyboardConfigForm {
        width: 100%;
        height: auto;
    }

    KeyboardConfigForm .form-title {
        text-style: bold;
        color: $text;
        margin-bottom: 1;
    }

    KeyboardConfigForm .buttons {
        margin-top: 1;
        height: auto;
    }

    KeyboardConfigForm Button {
        margin-right: 1;
    }

    KeyboardConfigForm .error-message {
        color: $error;
        margin-top: 1;
    }

    KeyboardConfigForm .success-message {
        color: $success;
        margin-top: 1;
    }

    KeyboardConfigForm .field-row {
        height: auto;
        margin-bottom: 1;
    }

    KeyboardConfigForm .field-label {
        width: 20;
    }
    """

    def __init__(
        self,
        config: KeyboardConfig | None = None,
        id: str | None = None,
    ) -> None:
        """Initialize the keyboard form.

        Args:
            config: Existing keyboard configuration to edit.
            id: Optional widget ID.
        """
        super().__init__(id=id)
        self._config = config or KeyboardConfig()

    def compose(self) -> ComposeResult:
        """Compose the keyboard form layout."""
        yield Label(t("sections.keyboard.title"), classes="form-title")

        # Log Mode (main enable switch)
        yield Label(t("forms.keyboard.enable"))
        yield Switch(value=self._config.log_mode, id="log_mode")

        # Source
        yield Label(t("forms.keyboard.source"))
        yield Input(
            value=self._config.source,
            placeholder=t("forms.keyboard.source_placeholder"),
            id="source",
        )

        # Prefix
        yield Label(t("forms.keyboard.prefix"))
        yield Input(
            value=self._config.prefix or "",
            placeholder=t("forms.keyboard.prefix_placeholder"),
            id="prefix",
        )

        # Postfix
        yield Label(t("forms.keyboard.postfix"))
        yield Input(
            value=self._config.postfix,
            placeholder=t("forms.keyboard.postfix_placeholder"),
            id="postfix",
        )

        # Delay
        yield Label(t("forms.keyboard.delay_ms"))
        yield Input(
            value=str(self._config.delay_ms),
            placeholder=t("forms.keyboard.delay_ms_placeholder"),
            id="delay_ms",
        )

        with Horizontal(classes="buttons"):
            yield Button(t("common.buttons.save"), variant="success", id="save")

    def get_config(self) -> KeyboardConfig:
        """Get the current configuration from form values.

        Returns:
            KeyboardConfig with current form values.
        """
        log_mode = self.query_one("#log_mode", Switch).value
        source = self.query_one("#source", Input).value
        prefix_val = self.query_one("#prefix", Input).value
        prefix = prefix_val if prefix_val else None
        postfix = self.query_one("#postfix", Input).value
        delay_str = self.query_one("#delay_ms", Input).value
        delay_ms = int(delay_str) if delay_str else 5

        return KeyboardConfig(
            log_mode=log_mode,
            source=source,
            prefix=prefix,
            postfix=postfix,
            delay_ms=delay_ms,
        )

    def _clear_messages(self) -> None:
        """Clear previous validation errors and success messages from the form."""
        for error_label in self.query(".error-message"):
            error_label.remove()
        for success_label in self.query(".success-message"):
            success_label.remove()
        for input_widget in self.query(Input):
            input_widget.remove_class("invalid")

    def _show_success_message(self, message: str) -> None:
        """Show success message on the form.

        The message auto-disappears after MESSAGE_TIMEOUT seconds.

        Args:
            message: The success message to display.
        """
        label = Label(message, classes="success-message")
        self.mount(label)
        self.set_timer(self.MESSAGE_TIMEOUT, label.remove)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses.

        Args:
            event: The button pressed event.
        """
        self._clear_messages()

        if event.button.id == "save":
            try:
                config = self.get_config()
                self.app.config.keyboard = config
                self._show_success_message(t("common.messages.config_saved"))
            except Exception as e:
                self.mount(Label(t("common.messages.error", message=str(e)), classes="error-message"))
