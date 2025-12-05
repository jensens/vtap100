"""Base form widget for configuration sections.

Provides common functionality for all configuration forms.
"""

from abc import abstractmethod
from pydantic import BaseModel
from pydantic import ValidationError
from textual.events import DescendantFocus
from textual.message import Message
from textual.widget import Widget
from textual.widgets import Button
from textual.widgets import Input
from textual.widgets import Label
from textual.widgets import Select
from typing import Any
from typing import ClassVar
from vtap100.tui.i18n import t


class ConfigChanged(Message):
    """Message posted when a configuration value changes.

    Attributes:
        section_id: The section that changed (e.g., "vas", "keyboard").
        field_name: The field that changed (e.g., "merchant_id").
        value: The new value.
    """

    def __init__(self, section_id: str, field_name: str, value: str) -> None:
        """Initialize the message.

        Args:
            section_id: The section identifier.
            field_name: The field name.
            value: The new field value.
        """
        super().__init__()
        self.section_id = section_id
        self.field_name = field_name
        self.value = value


class HelpContextChanged(Message):
    """Message posted when the help context should change.

    Attributes:
        context: The help context key (e.g., "vas.merchant_id").
    """

    def __init__(self, context: str) -> None:
        """Initialize the message.

        Args:
            context: The help context key.
        """
        super().__init__()
        self.context = context


class ConfigAdded(Message):
    """Message posted when a new configuration is added.

    Attributes:
        section_id: The section that was added to (e.g., "vas", "smarttap").
        index: The index of the new configuration.
        is_duplicate: True if this was created by duplicating an existing config.
    """

    def __init__(self, section_id: str, index: int, is_duplicate: bool = False) -> None:
        """Initialize the message.

        Args:
            section_id: The section identifier.
            index: The index of the new config.
            is_duplicate: Whether this config was duplicated from another.
        """
        super().__init__()
        self.section_id = section_id
        self.index = index
        self.is_duplicate = is_duplicate


class ConfigRemoved(Message):
    """Message posted when a configuration is removed.

    Attributes:
        section_id: The section that was removed from (e.g., "vas", "smarttap").
        index: The index that was removed.
    """

    def __init__(self, section_id: str, index: int) -> None:
        """Initialize the message.

        Args:
            section_id: The section identifier.
            index: The index that was removed.
        """
        super().__init__()
        self.section_id = section_id
        self.index = index


class BaseConfigForm(Widget):
    """Base class for configuration forms.

    Provides common functionality:
    - Help context updates on field focus
    - Validation feedback
    - Config changed notifications

    Subclasses should override:
    - SECTION_NAME: The section identifier
    - compose(): The form layout
    """

    SECTION_NAME: str = ""

    DEFAULT_CSS = """
    BaseConfigForm {
        width: 100%;
        height: auto;
        padding: 1;
    }

    BaseConfigForm Label {
        margin-bottom: 0;
        margin-top: 1;
    }

    BaseConfigForm Input {
        margin-bottom: 1;
    }

    BaseConfigForm Select {
        margin-bottom: 1;
    }

    BaseConfigForm .form-title {
        text-style: bold;
        margin-bottom: 1;
    }

    BaseConfigForm .error {
        color: $error;
    }

    BaseConfigForm .valid {
        border: solid $success;
    }

    BaseConfigForm .invalid {
        border: solid $error;
    }
    """

    def on_mount(self) -> None:
        """Focus the first input field when the form is mounted."""
        inputs = self.query(Input)
        if inputs:
            inputs[0].focus()

    def on_input_changed(self, event: Input.Changed) -> None:
        """Handle input field changes.

        Posts ConfigChanged and triggers validation.

        Args:
            event: The input changed event.
        """
        if event.input.id:
            self.post_message(
                ConfigChanged(
                    section_id=self.SECTION_NAME,
                    field_name=event.input.id,
                    value=event.value,
                )
            )

    def on_descendant_focus(self, event: DescendantFocus) -> None:
        """Handle descendant focus events.

        Updates the help context when an Input or Select widget within the form gains focus.

        Args:
            event: The descendant focus event.
        """
        # Check if the focused widget is an Input or Select with an id
        widget = event.widget
        if isinstance(widget, Input | Select) and widget.id:
            self.post_message(HelpContextChanged(f"{self.SECTION_NAME}.{widget.id}"))


class SlotBasedConfigForm(BaseConfigForm):
    """Base class for slot-based configuration forms (VAS, SmartTap).

    Provides shared functionality for forms that manage configurations
    with key slots, including:
    - Slot info display (used/free slots)
    - Validation error display
    - Success message display
    - Add/Save/Remove/Duplicate button handling

    Subclasses must define:
        SECTION_NAME: The section identifier (e.g., "vas", "smarttap").
        CONFIG_LIST_ATTR: The attribute name on app.config (e.g., "vas_configs").

    Subclasses must implement:
        get_config(): Return the current config from form values.
        _get_used_key_slots(): Return dict of used slot numbers to descriptions.
    """

    CONFIG_LIST_ATTR: ClassVar[str] = ""
    MESSAGE_TIMEOUT: ClassVar[float] = 10.0  # Seconds before success message disappears

    # Form state - set by subclass __init__
    index: int
    is_new: bool
    _config: BaseModel

    def _get_config_list(self) -> list[Any]:
        """Get the config list from app.config.

        Returns:
            The list of configurations (e.g., app.config.vas_configs).
        """
        return getattr(self.app.config, self.CONFIG_LIST_ATTR)

    @abstractmethod
    def _get_used_key_slots(self) -> dict[int, str]:
        """Get key slots that are already in use by other configs.

        Returns:
            Dict mapping slot number to description (e.g., {1: "VAS #1"}).
        """
        ...

    @abstractmethod
    def get_config(self) -> BaseModel:
        """Get the current configuration from form values.

        Returns:
            The config model with current form values.
        """
        ...

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
        """Handle button presses for add/save/remove/duplicate.

        Args:
            event: The button pressed event.
        """
        self._clear_errors()
        config_list = self._get_config_list()

        if event.button.id == "add":
            try:
                config = self.get_config()
                config_list.append(config)
                self.post_message(ConfigAdded(section_id=self.SECTION_NAME, index=self.index))
            except ValidationError as e:
                self._show_validation_error(e)

        elif event.button.id == "save":
            try:
                config = self.get_config()
                config_list[self.index] = config
                self._show_success_message(t("common.messages.config_saved"))
                # Refresh preview
                self.post_message(
                    ConfigChanged(
                        section_id=self.SECTION_NAME,
                        field_name="saved",
                        value="",
                    )
                )
            except ValidationError as e:
                self._show_validation_error(e)

        elif event.button.id == "remove":
            del config_list[self.index]
            self.post_message(ConfigRemoved(section_id=self.SECTION_NAME, index=self.index))

        elif event.button.id == "duplicate":
            try:
                config = self.get_config()
                config_list.append(config)
                new_index = len(config_list) - 1
                self.post_message(
                    ConfigAdded(section_id=self.SECTION_NAME, index=new_index, is_duplicate=True)
                )
            except ValidationError as e:
                self._show_validation_error(e)
