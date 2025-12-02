"""Apple VAS configuration form.

Form for editing Apple VAS (Value Added Services) configurations.
"""

from pydantic import ValidationError
from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widgets import Button
from textual.widgets import Input
from textual.widgets import Label
from textual.widgets import Select
from textual.widgets import Static
from vtap100.models.vas import AppleVASConfig
from vtap100.tui.i18n import t
from vtap100.tui.widgets.forms.base import BaseConfigForm
from vtap100.tui.widgets.forms.base import ConfigAdded
from vtap100.tui.widgets.forms.base import ConfigRemoved


class VASConfigForm(BaseConfigForm):
    """Form for editing Apple VAS configuration.

    Fields:
    - merchant_id: Pass Type ID (required, must start with 'pass.')
    - key_slot: Private key slot (0-6)
    - merchant_url: Optional URL

    Attributes:
        SECTION_NAME: Set to "vas".
        MESSAGE_TIMEOUT: Seconds before success messages auto-disappear.
    """

    SECTION_NAME = "vas"
    MESSAGE_TIMEOUT = 10.0  # Seconds before success message disappears

    DEFAULT_CSS = """
    VASConfigForm {
        width: 100%;
        height: auto;
    }

    VASConfigForm .form-title {
        text-style: bold;
        color: $text;
        margin-bottom: 1;
    }

    VASConfigForm .buttons {
        margin-top: 1;
        height: auto;
    }

    VASConfigForm Button {
        margin-right: 1;
    }

    VASConfigForm .error-message {
        color: $error;
        margin-top: 1;
    }
    """

    def __init__(
        self,
        config: AppleVASConfig | None = None,
        index: int = 0,
        is_new: bool = False,
        id: str | None = None,
    ) -> None:
        """Initialize the VAS form.

        Args:
            config: Existing VAS configuration to edit.
            index: Index in the vas_configs list.
            is_new: If True, this is a new config being created.
            id: Optional widget ID.
        """
        super().__init__(id=id)
        self.index = index
        self.is_new = is_new
        self._config = config or AppleVASConfig(merchant_id="pass.")

    def _get_used_key_slots(self) -> dict[int, str]:
        """Get key slots that are already in use by other configs.

        Returns:
            Dict mapping slot number to description (e.g., {1: "VAS #1", 3: "SmartTap #1"}).
            Excludes current config if editing.
        """
        used_slots: dict[int, str] = {}

        # Get all VAS config slots (except current if editing)
        for i, vas_config in enumerate(self.app.config.vas_configs):
            if not self.is_new and i == self.index:
                continue  # Skip current config when editing
            used_slots[vas_config.key_slot] = f"VAS #{i + 1}"

        # Get all SmartTap config slots
        for i, st_config in enumerate(self.app.config.smarttap_configs):
            used_slots[st_config.key_slot] = f"SmartTap #{i + 1}"

        return used_slots

    def _get_slot_info_text(self) -> str:
        """Get info text showing which slots are used/free.

        Returns:
            Info text like "Used: 1 (VAS #1), 3 (SmartTap #1) | Free: 2, 4, 5, 6".
        """
        used_slots = self._get_used_key_slots()

        # Build used list (excluding slot 0 which is special)
        used_parts = []
        for slot in sorted(used_slots.keys()):
            if slot > 0:  # Skip auto slot
                used_parts.append(f"{slot} ({used_slots[slot]})")

        # Build free list (slots 1-6 that are not used)
        free_slots = [str(i) for i in range(1, 7) if i not in used_slots]

        parts = []
        if used_parts:
            parts.append(f"{t('forms.vas.slot_info_used')}: {', '.join(used_parts)}")
        if free_slots:
            parts.append(f"{t('forms.vas.slot_info_free')}: {', '.join(free_slots)}")

        return " | ".join(parts) if parts else t("forms.vas.slot_info_all_free")

    def compose(self) -> ComposeResult:
        """Compose the VAS form layout."""
        if self.is_new:
            title = t("sections.vas.new_title")
        else:
            title = t("sections.vas.edit_title", num=self.index + 1)
        yield Label(title, classes="form-title")

        yield Label(t("forms.vas.merchant_id"))
        yield Input(
            value=self._config.merchant_id,
            placeholder=t("forms.vas.merchant_id_placeholder"),
            id="merchant_id",
        )

        yield Label(t("forms.vas.key_slot"))
        # Generate options for Select: 0 (Auto) and 1-6
        options = [(f"{i} ({t('common.labels.auto')})" if i == 0 else str(i), i) for i in range(7)]
        yield Select(options, value=self._config.key_slot, id="key_slot")
        yield Static(self._get_slot_info_text(), classes="slot-info")

        yield Label(t("forms.vas.merchant_url"))
        yield Input(
            value=self._config.merchant_url or "",
            placeholder=t("forms.vas.merchant_url_placeholder"),
            id="merchant_url",
        )

        with Horizontal(classes="buttons"):
            if self.is_new:
                yield Button(t("common.buttons.add"), variant="success", id="add")
            else:
                yield Button(t("common.buttons.save"), variant="success", id="save")
                yield Button(t("common.buttons.duplicate"), variant="default", id="duplicate")
                yield Button(t("common.buttons.remove"), variant="error", id="remove")

    def get_config(self) -> AppleVASConfig:
        """Get the current configuration from form values.

        Returns:
            AppleVASConfig with current form values.
        """
        merchant_id = self.query_one("#merchant_id", Input).value
        select = self.query_one("#key_slot", Select)
        key_slot = select.value if select.value is not None else 0
        merchant_url = self.query_one("#merchant_url", Input).value or None

        return AppleVASConfig(
            merchant_id=merchant_id,
            key_slot=key_slot,
            merchant_url=merchant_url,
        )

    def _clear_messages(self) -> None:
        """Clear previous validation errors and success messages from the form."""
        # Remove error messages
        for error_label in self.query(".error-message"):
            error_label.remove()
        # Remove success messages
        for success_label in self.query(".success-message"):
            success_label.remove()
        # Remove invalid class from inputs
        for input_widget in self.query(Input):
            input_widget.remove_class("invalid")

    def _clear_errors(self) -> None:
        """Clear previous validation errors from the form."""
        self._clear_messages()

    def _show_validation_error(self, error: ValidationError) -> None:
        """Show validation error on the form.

        Args:
            error: The pydantic validation error.
        """
        for err in error.errors():
            field = err["loc"][0] if err["loc"] else None
            msg = err["msg"]
            if field:
                try:
                    input_widget = self.query_one(f"#{field}", Input)
                    input_widget.add_class("invalid")
                except Exception:
                    pass
            # Mount error message after the buttons
            self.mount(Label(t("common.messages.error", message=msg), classes="error-message"))

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
        self._clear_errors()

        if event.button.id == "add":
            try:
                config = self.get_config()
                self.app.config.vas_configs.append(config)
                self.post_message(ConfigAdded(section_id=self.SECTION_NAME, index=self.index))
            except ValidationError as e:
                self._show_validation_error(e)

        elif event.button.id == "save":
            try:
                config = self.get_config()
                self.app.config.vas_configs[self.index] = config
                self._show_success_message(t("common.messages.config_saved"))
            except ValidationError as e:
                self._show_validation_error(e)

        elif event.button.id == "remove":
            del self.app.config.vas_configs[self.index]
            self.post_message(ConfigRemoved(section_id=self.SECTION_NAME, index=self.index))

        elif event.button.id == "duplicate":
            try:
                config = self.get_config()
                self.app.config.vas_configs.append(config)
                new_index = len(self.app.config.vas_configs) - 1
                self.post_message(
                    ConfigAdded(section_id=self.SECTION_NAME, index=new_index, is_duplicate=True)
                )
            except ValidationError as e:
                self._show_validation_error(e)
