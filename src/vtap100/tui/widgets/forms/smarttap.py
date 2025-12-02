"""Google Smart Tap configuration form.

Form for editing Google Smart Tap configurations.
"""

from pydantic import ValidationError
from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widgets import Button, Input, Label, Select, Static

from vtap100.models.smarttap import GoogleSmartTapConfig
from vtap100.tui.i18n import t
from vtap100.tui.widgets.forms.base import BaseConfigForm, ConfigAdded, ConfigRemoved


class SmartTapConfigForm(BaseConfigForm):
    """Form for editing Google Smart Tap configuration.

    Fields:
    - collector_id: Google Collector ID (required)
    - key_slot: Private key slot (0-6)
    - key_version: Key version number

    Attributes:
        SECTION_NAME: Set to "smarttap".
        MESSAGE_TIMEOUT: Seconds before success messages auto-disappear.
    """

    SECTION_NAME = "smarttap"
    MESSAGE_TIMEOUT = 10.0  # Seconds before success message disappears

    DEFAULT_CSS = """
    SmartTapConfigForm {
        width: 100%;
        height: auto;
    }

    SmartTapConfigForm .form-title {
        text-style: bold;
        color: $text;
        margin-bottom: 1;
    }

    SmartTapConfigForm .buttons {
        margin-top: 1;
        height: auto;
    }

    SmartTapConfigForm Button {
        margin-right: 1;
    }

    SmartTapConfigForm .error-message {
        color: $error;
        margin-top: 1;
    }
    """

    def __init__(
        self,
        config: GoogleSmartTapConfig | None = None,
        index: int = 0,
        is_new: bool = False,
        id: str | None = None,
    ) -> None:
        """Initialize the Smart Tap form.

        Args:
            config: Existing Smart Tap configuration to edit.
            index: Index in the smarttap_configs list.
            is_new: If True, this is a new config being created.
            id: Optional widget ID.
        """
        super().__init__(id=id)
        self.index = index
        self.is_new = is_new
        # Use placeholder collector_id for new configs (model requires non-empty string)
        self._config = config or GoogleSmartTapConfig(collector_id="00000000")

    def _get_used_key_slots(self) -> dict[int, str]:
        """Get key slots that are already in use by other configs.

        Returns:
            Dict mapping slot number to description (e.g., {1: "VAS #1", 3: "SmartTap #1"}).
            Excludes current config if editing.
        """
        used_slots: dict[int, str] = {}

        # Get all VAS config slots
        for i, vas_config in enumerate(self.app.config.vas_configs):
            used_slots[vas_config.key_slot] = f"VAS #{i + 1}"

        # Get all SmartTap config slots (except current if editing)
        for i, st_config in enumerate(self.app.config.smarttap_configs):
            if not self.is_new and i == self.index:
                continue  # Skip current config when editing
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
        """Compose the Smart Tap form layout."""
        if self.is_new:
            title = t("sections.smarttap.new_title")
        else:
            title = t("sections.smarttap.edit_title", num=self.index + 1)
        yield Label(title, classes="form-title")

        yield Label(t("forms.smarttap.collector_id"))
        yield Input(
            value=self._config.collector_id,
            placeholder=t("forms.smarttap.collector_id_placeholder"),
            id="collector_id",
        )

        yield Label(t("forms.smarttap.key_slot"))
        # Generate options for Select: 0 (Auto) and 1-6
        options = [(f"{i} ({t('common.labels.auto')})" if i == 0 else str(i), i) for i in range(7)]
        yield Select(options, value=self._config.key_slot, id="key_slot")
        yield Static(self._get_slot_info_text(), classes="slot-info")

        yield Label(t("forms.smarttap.key_version"))
        yield Input(
            value=str(self._config.key_version) if self._config.key_version else "",
            placeholder="1",
            id="key_version",
        )

        with Horizontal(classes="buttons"):
            if self.is_new:
                yield Button(t("common.buttons.add"), variant="success", id="add")
            else:
                yield Button(t("common.buttons.save"), variant="success", id="save")
                yield Button(t("common.buttons.duplicate"), variant="default", id="duplicate")
                yield Button(t("common.buttons.remove"), variant="error", id="remove")

    def get_config(self) -> GoogleSmartTapConfig:
        """Get the current configuration from form values.

        Returns:
            GoogleSmartTapConfig with current form values.
        """
        collector_id = self.query_one("#collector_id", Input).value
        select = self.query_one("#key_slot", Select)
        key_slot = select.value if select.value is not None else 0
        key_version_str = self.query_one("#key_version", Input).value
        key_version = int(key_version_str) if key_version_str else 0

        return GoogleSmartTapConfig(
            collector_id=collector_id,
            key_slot=key_slot,
            key_version=key_version,
        )

    def _clear_messages(self) -> None:
        """Clear previous validation errors and success messages from the form."""
        for error_label in self.query(".error-message"):
            error_label.remove()
        for success_label in self.query(".success-message"):
            success_label.remove()
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
                self.app.config.smarttap_configs.append(config)
                self.post_message(ConfigAdded(section_id=self.SECTION_NAME, index=self.index))
            except ValidationError as e:
                self._show_validation_error(e)

        elif event.button.id == "save":
            try:
                config = self.get_config()
                self.app.config.smarttap_configs[self.index] = config
                self._show_success_message(t("common.messages.config_saved"))
            except ValidationError as e:
                self._show_validation_error(e)

        elif event.button.id == "remove":
            del self.app.config.smarttap_configs[self.index]
            self.post_message(ConfigRemoved(section_id=self.SECTION_NAME, index=self.index))

        elif event.button.id == "duplicate":
            try:
                config = self.get_config()
                self.app.config.smarttap_configs.append(config)
                new_index = len(self.app.config.smarttap_configs) - 1
                self.post_message(
                    ConfigAdded(section_id=self.SECTION_NAME, index=new_index, is_duplicate=True)
                )
            except ValidationError as e:
                self._show_validation_error(e)
