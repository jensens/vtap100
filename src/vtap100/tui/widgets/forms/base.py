"""Base form widget for configuration sections.

Provides common functionality for all configuration forms.
"""

from textual.events import DescendantFocus
from textual.message import Message
from textual.widget import Widget
from textual.widgets import Input
from textual.widgets import Select


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
