"""LED and Beep feedback configuration form.

Form for editing LED and buzzer feedback settings.
"""

from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widgets import Button
from textual.widgets import Input
from textual.widgets import Label
from textual.widgets import Select
from vtap100.models.feedback import BeepConfig
from vtap100.models.feedback import FeedbackConfig
from vtap100.models.feedback import LEDConfig
from vtap100.models.feedback import LEDMode
from vtap100.models.feedback import LEDSelect
from vtap100.tui.i18n import t
from vtap100.tui.widgets.forms.base import BaseConfigForm
from vtap100.tui.widgets.forms.base import ConfigChanged


class FeedbackConfigForm(BaseConfigForm):
    """Form for editing LED and Beep feedback configuration.

    This is a single-value section form.

    Fields:
    - led_mode: LED operating mode
    - led_select: LED type/position
    - default_rgb: Default RGB color

    Attributes:
        SECTION_NAME: Set to "feedback".
        MESSAGE_TIMEOUT: Seconds before success messages auto-disappear.
    """

    SECTION_NAME = "feedback"
    MESSAGE_TIMEOUT = 10.0

    @property
    def led_mode_options(self) -> list[tuple[str, LEDMode]]:
        """Get LED mode options with translated labels."""
        return [
            (t("forms.feedback.led_mode_off"), LEDMode.OFF),
            (t("forms.feedback.led_mode_on"), LEDMode.ON),
            (t("forms.feedback.led_mode_status"), LEDMode.STATUS),
            (t("forms.feedback.led_mode_custom"), LEDMode.CUSTOM),
        ]

    @property
    def led_select_options(self) -> list[tuple[str, LEDSelect]]:
        """Get LED select options with translated labels."""
        return [
            (t("forms.feedback.led_external"), LEDSelect.EXTERNAL),
            (t("forms.feedback.led_onboard_compact"), LEDSelect.ONBOARD_COMPACT),
            (t("forms.feedback.led_onboard_square"), LEDSelect.ONBOARD_SQUARE),
            (t("forms.feedback.led_serial"), LEDSelect.SERIAL),
        ]

    DEFAULT_CSS = """
    FeedbackConfigForm {
        width: 100%;
        height: auto;
    }

    FeedbackConfigForm .form-title {
        text-style: bold;
        color: $text;
        margin-bottom: 1;
    }

    FeedbackConfigForm .section-title {
        text-style: bold;
        margin-top: 2;
        margin-bottom: 1;
    }

    FeedbackConfigForm .buttons {
        margin-top: 1;
        height: auto;
    }

    FeedbackConfigForm Button {
        margin-right: 1;
    }

    FeedbackConfigForm .success-message {
        color: $success;
        margin-top: 1;
    }

    FeedbackConfigForm .error-message {
        color: $error;
        margin-top: 1;
    }
    """

    def __init__(
        self,
        config: FeedbackConfig | None = None,
        id: str | None = None,
    ) -> None:
        """Initialize the feedback form.

        Args:
            config: Existing feedback configuration to edit.
            id: Optional widget ID.
        """
        super().__init__(id=id)
        self._config = config or FeedbackConfig()
        # Ensure led and beep sub-configs exist
        if self._config.led is None:
            self._config = FeedbackConfig(led=LEDConfig(), beep=self._config.beep)
        if self._config.beep is None:
            self._config = FeedbackConfig(led=self._config.led, beep=BeepConfig())

    def compose(self) -> ComposeResult:
        """Compose the feedback form layout."""
        yield Label(t("sections.feedback.title"), classes="form-title")

        # LED Section
        yield Label(t("forms.feedback.led_section"), classes="section-title")

        yield Label(t("forms.feedback.led_mode"))
        led_mode = self._config.led.mode if self._config.led else None
        yield Select(
            self.led_mode_options,
            value=led_mode or LEDMode.OFF,
            id="led_mode",
        )

        yield Label(t("forms.feedback.led_select"))
        led_select = self._config.led.select if self._config.led else None
        yield Select(
            self.led_select_options,
            value=led_select or LEDSelect.EXTERNAL,
            id="led_select",
        )

        yield Label(t("forms.feedback.default_rgb"))
        default_rgb = self._config.led.default_rgb if self._config.led else ""
        yield Input(
            value=default_rgb or "",
            placeholder=t("forms.feedback.default_rgb_placeholder"),
            id="default_rgb",
        )

        with Horizontal(classes="buttons"):
            yield Button(t("common.buttons.save"), variant="success", id="save")

    def get_config(self) -> FeedbackConfig:
        """Get the current configuration from form values.

        Returns:
            FeedbackConfig with current form values.
        """
        led_mode_select = self.query_one("#led_mode", Select)
        led_select_select = self.query_one("#led_select", Select)
        default_rgb = self.query_one("#default_rgb", Input).value

        led_config = LEDConfig(
            mode=led_mode_select.value,
            select=led_select_select.value,
            default_rgb=default_rgb if default_rgb else None,
        )

        return FeedbackConfig(
            led=led_config,
            beep=self._config.beep,  # Preserve existing beep config
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

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        self._clear_messages()

        if event.button.id == "save":
            try:
                config = self.get_config()
                self.app.config.feedback = config
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
