"""Context-sensitive help panel widget.

Displays help content based on the currently focused field.
"""

from textual.app import ComposeResult
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Static
from vtap100.tui.help import HelpLoader
from vtap100.tui.i18n import t


class HelpPanel(Widget):
    """Context-sensitive help panel.

    Displays help content from YAML files based on the current context.
    The context is typically set by form fields when they receive focus.

    Attributes:
        current_context: The current help context (e.g., "vas.merchant_id").
    """

    current_context: reactive[str] = reactive("")

    DEFAULT_CSS = """
    HelpPanel {
        width: 100%;
        height: 100%;
        padding: 1;
    }

    HelpPanel .help-title {
        text-style: bold;
        color: $text;
        margin-bottom: 1;
    }

    HelpPanel .help-description {
        color: $text;
        margin-bottom: 1;
    }

    HelpPanel .help-tip {
        color: $text-muted;
        text-style: italic;
    }

    HelpPanel .help-example {
        color: $success;
        margin-top: 1;
    }
    """

    def __init__(self, id: str | None = None) -> None:
        """Initialize the help panel.

        Args:
            id: Optional widget ID.
        """
        super().__init__(id=id)

    def compose(self) -> ComposeResult:
        """Compose the help panel layout."""
        yield Static("", id="help-content")

    def watch_current_context(self, context: str) -> None:
        """Update display when context changes.

        Args:
            context: The new help context.
        """
        self._update_content()

    def _update_content(self) -> None:
        """Update the help content display."""
        try:
            content_widget = self.query_one("#help-content", Static)
            content_widget.update(self._format_help())
        except Exception:
            pass  # Widget may not be mounted yet

    def refresh_help(self) -> None:
        """Refresh help content (call after language change)."""
        self._update_content()

    def _format_help(self) -> str:
        """Format help content for display.

        Returns:
            Formatted help text.
        """
        if not self.current_context:
            return t("help.select_field")

        # Get help data dynamically (respects current language)
        help_data = HelpLoader.get_help(self.current_context)

        if not help_data:
            return t("help.no_help", context=self.current_context)

        lines = []

        # Title
        title = help_data.get("title", self.current_context)
        lines.append(f"[bold]{title}[/bold]")
        lines.append("")

        # Description
        if "description" in help_data:
            lines.append(help_data["description"].strip())
            lines.append("")

        # Format
        if "format" in help_data:
            lines.append(f"[dim]{t('help.format')}:[/dim] {help_data['format']}")

        # Example
        if "example" in help_data:
            lines.append(f"[dim]{t('help.example')}:[/dim] [green]{help_data['example']}[/green]")

        # Tip
        if "tip" in help_data:
            lines.append("")
            lines.append(f"[italic]{help_data['tip'].strip()}[/italic]")

        return "\n".join(lines)

    def render(self) -> str:
        """Render the help panel.

        Returns:
            Rendered help content.
        """
        return self._format_help()
