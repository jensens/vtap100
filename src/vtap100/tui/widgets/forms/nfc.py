"""NFC Tag configuration form.

Form for editing NFC tag reading settings.
"""

from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widgets import Button
from textual.widgets import Label
from textual.widgets import Select
from textual.widgets import Switch
from vtap100.models.nfc import NFCTagConfig
from vtap100.models.nfc import NFCTagMode
from vtap100.tui.i18n import t
from vtap100.tui.widgets.forms.base import BaseConfigForm
from vtap100.tui.widgets.forms.base import ConfigChanged


class NFCConfigForm(BaseConfigForm):
    """Form for editing NFC tag configuration.

    This is a single-value section form.

    Fields:
    - type2: NFC Type 2 tag mode
    - type4: NFC Type 4 tag mode
    - type5: NFC Type 5 tag mode
    - report_read_error: Report error payload
    - ignore_random_uid: Filter random UIDs
    - byte_order_reversed: Reverse byte order

    Attributes:
        SECTION_NAME: Set to "nfc".
        MESSAGE_TIMEOUT: Seconds before success messages auto-disappear.
    """

    SECTION_NAME = "nfc"
    MESSAGE_TIMEOUT = 10.0

    @property
    def tag_mode_options(self) -> list[tuple[str, NFCTagMode]]:
        """Get tag mode options with translated labels."""
        return [
            (t("forms.nfc.mode_disabled"), NFCTagMode.DISABLED),
            (t("forms.nfc.mode_uid"), NFCTagMode.UID),
            (t("forms.nfc.mode_ndef"), NFCTagMode.NDEF),
            (t("forms.nfc.mode_block"), NFCTagMode.BLOCK),
        ]

    @property
    def type4_mode_options(self) -> list[tuple[str, NFCTagMode]]:
        """Get Type 4 mode options with translated labels (includes DESFire)."""
        return [
            (t("forms.nfc.mode_disabled"), NFCTagMode.DISABLED),
            (t("forms.nfc.mode_uid"), NFCTagMode.UID),
            (t("forms.nfc.mode_ndef"), NFCTagMode.NDEF),
            (t("forms.nfc.mode_block"), NFCTagMode.BLOCK),
            (t("forms.nfc.mode_desfire"), NFCTagMode.DESFIRE),
        ]

    DEFAULT_CSS = """
    NFCConfigForm {
        width: 100%;
        height: auto;
    }

    NFCConfigForm .form-title {
        text-style: bold;
        color: $text;
        margin-bottom: 1;
    }

    NFCConfigForm .buttons {
        margin-top: 1;
        height: auto;
    }

    NFCConfigForm Button {
        margin-right: 1;
    }

    NFCConfigForm .success-message {
        color: $success;
        margin-top: 1;
    }

    NFCConfigForm .error-message {
        color: $error;
        margin-top: 1;
    }
    """

    def __init__(
        self,
        config: NFCTagConfig | None = None,
        id: str | None = None,
    ) -> None:
        """Initialize the NFC form.

        Args:
            config: Existing NFC configuration to edit.
            id: Optional widget ID.
        """
        super().__init__(id=id)
        self._config = config or NFCTagConfig()

    def compose(self) -> ComposeResult:
        """Compose the NFC form layout."""
        yield Label(t("sections.nfc.title"), classes="form-title")

        # Type 2
        yield Label(t("forms.nfc.type2"))
        yield Select(
            self.tag_mode_options,
            value=self._config.type2 or NFCTagMode.DISABLED,
            id="type2",
        )

        # Type 4
        yield Label(t("forms.nfc.type4"))
        yield Select(
            self.type4_mode_options,
            value=self._config.type4 or NFCTagMode.DISABLED,
            id="type4",
        )

        # Type 5
        yield Label(t("forms.nfc.type5"))
        yield Select(
            self.tag_mode_options,
            value=self._config.type5 or NFCTagMode.DISABLED,
            id="type5",
        )

        # Options
        yield Label(t("forms.nfc.report_read_error"))
        yield Switch(value=self._config.report_read_error, id="report_read_error")

        yield Label(t("forms.nfc.ignore_random_uid"))
        yield Switch(value=self._config.ignore_random_uid, id="ignore_random_uid")

        yield Label(t("forms.nfc.byte_order_reversed"))
        yield Switch(value=self._config.byte_order_reversed, id="byte_order_reversed")

        with Horizontal(classes="buttons"):
            yield Button(t("common.buttons.save"), variant="success", id="save")

    def get_config(self) -> NFCTagConfig:
        """Get the current configuration from form values.

        Returns:
            NFCTagConfig with current form values.
        """
        type2_select = self.query_one("#type2", Select)
        type4_select = self.query_one("#type4", Select)
        type5_select = self.query_one("#type5", Select)

        type2 = type2_select.value if type2_select.value != NFCTagMode.DISABLED else None
        type4 = type4_select.value if type4_select.value != NFCTagMode.DISABLED else None
        type5 = type5_select.value if type5_select.value != NFCTagMode.DISABLED else None

        return NFCTagConfig(
            type2=type2,
            type4=type4,
            type5=type5,
            report_read_error=self.query_one("#report_read_error", Switch).value,
            ignore_random_uid=self.query_one("#ignore_random_uid", Switch).value,
            byte_order_reversed=self.query_one("#byte_order_reversed", Switch).value,
        )

    def _clear_messages(self) -> None:
        """Clear previous validation errors and success messages."""
        for label in self.query(".error-message"):
            label.remove()
        for label in self.query(".success-message"):
            label.remove()

    def _show_success_message(self, message: str) -> None:
        """Show success message on the form."""
        label = Label(message, classes="success-message")
        self.mount(label)
        self.set_timer(self.MESSAGE_TIMEOUT, label.remove)

    def on_switch_changed(self, event: Switch.Changed) -> None:
        """Handle switch changes to update preview.

        Args:
            event: The switch changed event.
        """
        if event.switch.id:
            self.post_message(
                ConfigChanged(
                    section_id=self.SECTION_NAME,
                    field_name=event.switch.id,
                    value=str(event.value),
                )
            )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        self._clear_messages()

        if event.button.id == "save":
            try:
                config = self.get_config()
                self.app.config.nfc = config
                self._show_success_message(t("common.messages.config_saved"))
                # Refresh preview
                self.post_message(
                    ConfigChanged(
                        section_id=self.SECTION_NAME,
                        field_name="saved",
                        value="",
                    )
                )
            except Exception as e:
                self.mount(
                    Label(t("common.messages.error", message=str(e)), classes="error-message")
                )
