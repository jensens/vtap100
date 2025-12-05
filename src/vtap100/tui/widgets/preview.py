"""Live config.txt preview widget.

Shows a live preview of the generated config.txt content.
"""

from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Static
from vtap100.generator import ConfigGenerator
from vtap100.models.config import VTAPConfig


class ConfigPreview(Widget):
    """Live preview of the generated config.txt content.

    Shows the config.txt that would be generated from the current
    VTAPConfig state. Updates when update_preview() is called.

    Attributes:
        DEFAULT_CSS: Default styling for the preview.
    """

    DEFAULT_CSS = """
    ConfigPreview {
        width: 100%;
        height: auto;
    }

    ConfigPreview > Static {
        width: 100%;
        height: auto;
    }

    ConfigPreview .preview-line {
        color: $text;
    }

    ConfigPreview .preview-comment {
        color: $text-muted;
    }

    ConfigPreview .preview-header {
        color: $success;
        text-style: bold;
    }
    """

    def __init__(self, config: VTAPConfig | None = None, id: str | None = None) -> None:
        """Initialize the preview widget.

        Args:
            config: Initial config to preview.
            id: Optional widget ID.
        """
        super().__init__(id=id)
        self._config = config or VTAPConfig()
        self._content = ""

    def compose(self) -> ComposeResult:
        """Compose the preview content."""
        self._content = self._generate_content()
        yield Static(self._content, id="preview-content", markup=False)

    def _generate_content(self) -> str:
        """Generate the config.txt content from current config.

        Returns:
            The generated config.txt content.
        """
        generator = ConfigGenerator(self._config)
        return generator.generate()

    def update_preview(self, config: VTAPConfig) -> None:
        """Update the preview with new config.

        Args:
            config: The new config to preview.
        """
        self._config = config
        self._content = self._generate_content()

        # Update the static widget content
        try:
            static = self.query_one("#preview-content", Static)
            static.update(self._content)
        except Exception:
            pass  # Widget may not be mounted yet

    def get_preview_content(self) -> str:
        """Get the current preview content.

        Returns:
            The current config.txt content as a string.
        """
        return self._content
