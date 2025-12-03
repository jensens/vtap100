"""VTAP100 Editor Application.

The main Textual App for editing VTAP100 configurations.
"""

from enum import Enum
from pathlib import Path
from textual.app import App
from textual.reactive import reactive
from vtap100 import __version__
from vtap100.generator import ConfigGenerator
from vtap100.models.config import VTAPConfig
from vtap100.parser import parse
from vtap100.tui.i18n import Language
from vtap100.tui.i18n import get_language
from vtap100.tui.i18n import set_language
from vtap100.tui.i18n import t
from vtap100.tui.screens.editor import EditorScreen


class PreviewMode(str, Enum):
    """Preview panel display modes."""

    DEFAULT = "default"  # Normal size at bottom
    MAXIMIZED = "maximized"  # Full screen (hides other panels)
    HIDDEN = "hidden"  # Not visible


class VTAPEditorApp(App):
    """Textual App for VTAP100 configuration editing.

    Provides a 3-panel TUI for editing VTAP100 config files:
    - Sidebar: Navigation tree for config sections
    - Main Content: Forms for editing the selected section
    - Help Panel: Context-sensitive help for the current field

    Attributes:
        input_path: Path to load configuration from.
        output_path: Path to save configuration to.
        config: The current VTAPConfig being edited.
        current_field: Currently focused field for context-sensitive help.
    """

    TITLE = f"VTAP100 Editor {__version__}"
    CSS_PATH = "styles/editor.tcss"

    BINDINGS = [
        ("ctrl+d", "toggle_help", "Doku"),
        ("ctrl+o", "toggle_preview", "Output"),
        ("ctrl+l", "toggle_language", "DE/EN"),
        ("ctrl+s", "save", "Save"),
        ("ctrl+e", "export", "Export"),
        ("ctrl+q", "quit", "Quit"),
    ]

    # Reactive state
    config: reactive[VTAPConfig] = reactive(VTAPConfig, init=False)
    current_field: reactive[str] = reactive("", init=False)

    def __init__(
        self,
        input_path: Path | None = None,
        output_path: Path | None = None,
    ) -> None:
        """Initialize the editor app.

        Args:
            input_path: Path to load an existing config.txt.
            output_path: Path for saving. Defaults to input_path if not specified.
        """
        super().__init__()
        self.input_path = input_path
        self.output_path = output_path or input_path
        self.config = self._load_config(input_path)
        self.current_field = ""
        self.preview_mode = PreviewMode.DEFAULT

    def _load_config(self, path: Path | None) -> VTAPConfig:
        """Load configuration from file or create empty one.

        Args:
            path: Path to config file, or None for empty config.

        Returns:
            Loaded or new VTAPConfig.
        """
        if path and path.exists():
            try:
                content = path.read_text(encoding="utf-8")
                return parse(content)
            except (OSError, ValueError):
                # If parsing fails, return empty config
                pass
        return VTAPConfig()

    def on_mount(self) -> None:
        """Push the EditorScreen when the app mounts."""
        self.push_screen(EditorScreen())

    def action_toggle_help(self) -> None:
        """Toggle the help panel visibility."""
        help_panel = self.screen.query_one("#help-panel")
        help_panel.display = not help_panel.display

    def action_toggle_preview(self) -> None:
        """Toggle the preview panel through 3 states: default -> maximized -> hidden.

        States:
        - DEFAULT: Normal size at bottom, other panels visible
        - MAXIMIZED: Full screen, only header/footer visible
        - HIDDEN: Preview not visible, other panels full size
        """
        preview_panel = self.screen.query_one("#preview-panel")
        top_row = self.screen.query_one("#top-row")

        # Cycle through states: DEFAULT -> MAXIMIZED -> HIDDEN -> DEFAULT
        if self.preview_mode == PreviewMode.DEFAULT:
            # Switch to MAXIMIZED
            self.preview_mode = PreviewMode.MAXIMIZED
            preview_panel.display = True
            preview_panel.add_class("preview-maximized")
            top_row.display = False

        elif self.preview_mode == PreviewMode.MAXIMIZED:
            # Switch to HIDDEN
            self.preview_mode = PreviewMode.HIDDEN
            preview_panel.display = False
            preview_panel.remove_class("preview-maximized")
            top_row.display = True

        else:  # HIDDEN
            # Switch back to DEFAULT
            self.preview_mode = PreviewMode.DEFAULT
            preview_panel.display = True
            preview_panel.remove_class("preview-maximized")
            top_row.display = True

    async def action_toggle_language(self) -> None:
        """Toggle between German and English language.

        Preserves the current section, form state, and tree expansion state.
        """
        from textual.widgets import Input
        from textual.widgets import Select
        from textual.widgets import Switch
        from textual.widgets import Tree
        from vtap100.tui.help import HelpLoader
        from vtap100.tui.widgets.help_panel import HelpPanel
        from vtap100.tui.widgets.sidebar import ConfigSidebar
        from vtap100.tui.widgets.sidebar import SectionSelected

        current = get_language()
        new_lang = Language.EN if current == Language.DE else Language.DE

        # Remember current section before refresh
        current_section = getattr(self.screen, "_current_section", None)

        # Save tree expansion state (which section nodes are expanded)
        sidebar = self.screen.query_one("#config-sidebar", ConfigSidebar)
        tree = sidebar.query_one(Tree)
        expanded_sections: set[str] = set()
        for node in tree.root.children:
            if node.is_expanded and node.data:
                expanded_sections.add(str(node.data))

        # Save current form values before language switch
        form_values: dict[str, str | int | bool | None] = {}
        main_content = self.screen.query_one("#main-content")
        for input_widget in main_content.query(Input):
            if input_widget.id:
                form_values[input_widget.id] = input_widget.value
        for select_widget in main_content.query(Select):
            if select_widget.id:
                form_values[select_widget.id] = select_widget.value
        for switch_widget in main_content.query(Switch):
            if switch_widget.id:
                form_values[switch_widget.id] = switch_widget.value

        # Now switch language
        set_language(new_lang)

        # Clear help cache so it reloads with new language
        HelpLoader.clear_cache()

        # Refresh sidebar with new translations
        sidebar.refresh_tree()

        # Restore tree expansion state
        tree = sidebar.query_one(Tree)
        for node in tree.root.children:
            if node.data and str(node.data) in expanded_sections:
                node.expand()

        # Refresh help panel with new language
        try:
            help_panel = self.screen.query_one("#help-panel-widget", HelpPanel)
            help_panel.refresh_help()
        except Exception:
            pass  # Help panel may not be visible

        # If a section was selected, reload it with new translations
        if current_section:
            section_id, index = current_section
            # Reset tracking so reload happens
            self.screen._current_section = None
            # Re-select the same section (triggers form reload with new labels)
            await self.screen.on_section_selected(SectionSelected(section_id, index))

            # Restore form values
            for input_widget in main_content.query(Input):
                if input_widget.id and input_widget.id in form_values:
                    input_widget.value = str(form_values[input_widget.id] or "")
            for select_widget in main_content.query(Select):
                if select_widget.id and select_widget.id in form_values:
                    select_widget.value = form_values[select_widget.id]
            for switch_widget in main_content.query(Switch):
                if switch_widget.id and switch_widget.id in form_values:
                    switch_widget.value = bool(form_values[switch_widget.id])

        # Notify user of language change
        lang_name = "English" if new_lang == Language.EN else "Deutsch"
        self.notify(f"Language: {lang_name}")

    def action_save(self) -> None:
        """Save the current configuration to output file."""
        if self.output_path:
            try:
                generator = ConfigGenerator(self.config)
                generator.write_to_file(self.output_path)
                self.notify(t("common.messages.config_saved"))
            except OSError as e:
                self.notify(
                    t("common.messages.error", message=str(e)),
                    severity="error",
                )
        else:
            self.notify(
                t("common.messages.error", message="No output file"),
                severity="error",
            )

    def action_export(self) -> None:
        """Open the export dialog."""
        from vtap100.tui.screens.export_dialog import ExportDialog
        from vtap100.tui.screens.export_dialog import ExportFormat
        from vtap100.tui.screens.export_dialog import ExportTarget

        def handle_export(result: tuple[ExportFormat, ExportTarget] | None) -> None:
            if result is None:
                return  # Cancelled

            export_format, export_target = result
            generator = ConfigGenerator(self.config)

            if export_format == ExportFormat.TEMPLATE:
                content = generator.generate_template()
            else:
                content = generator.generate()

            if export_target == ExportTarget.CLIPBOARD:
                try:
                    import pyperclip

                    pyperclip.copy(content)
                    self.notify(t("export.copied_to_clipboard"))
                except Exception as e:
                    self.notify(
                        t("export.clipboard_error", message=str(e)),
                        severity="error",
                    )
            else:
                # File export
                if self.output_path:
                    # Determine file extension based on format
                    output_file = self.output_path
                    if export_format == ExportFormat.TEMPLATE:
                        # Use .j2 extension for templates
                        output_file = self.output_path.with_suffix(".j2")

                    try:
                        output_file.write_text(content, encoding="utf-8")
                        self.notify(t("export.saved_to_file", path=str(output_file)))
                    except OSError as e:
                        self.notify(
                            t("common.messages.error", message=str(e)),
                            severity="error",
                        )
                else:
                    self.notify(t("export.no_output_path"), severity="error")

        self.push_screen(ExportDialog(), handle_export)
