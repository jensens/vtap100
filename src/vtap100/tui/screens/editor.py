"""Main Editor Screen.

The primary screen with 3-panel layout:
- Sidebar: Navigation tree
- Main Content: Configuration forms
- Help Panel: Context-sensitive help
- Preview Panel: Live config.txt preview (toggleable)
"""

from textual.app import ComposeResult
from textual.containers import Container
from textual.containers import Horizontal
from textual.containers import Vertical
from textual.containers import VerticalScroll
from textual.screen import Screen
from textual.widgets import Footer
from textual.widgets import Header
from textual.widgets import Label
from textual.widgets import Static
from vtap100.tui.i18n import t
from vtap100.tui.screens.unsaved_changes_dialog import UnsavedChangesDialog
from vtap100.tui.screens.unsaved_changes_dialog import UnsavedChangesResult
from vtap100.tui.widgets.forms.base import BaseConfigForm
from vtap100.tui.widgets.forms.base import ConfigAdded
from vtap100.tui.widgets.forms.base import ConfigChanged
from vtap100.tui.widgets.forms.base import ConfigRemoved
from vtap100.tui.widgets.forms.base import HelpContextChanged
from vtap100.tui.widgets.forms.base import SlotBasedConfigForm
from vtap100.tui.widgets.forms.desfire import DESFireConfigForm
from vtap100.tui.widgets.forms.feedback import FeedbackConfigForm
from vtap100.tui.widgets.forms.keyboard import KeyboardConfigForm
from vtap100.tui.widgets.forms.nfc import NFCConfigForm
from vtap100.tui.widgets.forms.smarttap import SmartTapConfigForm
from vtap100.tui.widgets.forms.vas import VASConfigForm
from vtap100.tui.widgets.help_panel import HelpPanel
from vtap100.tui.widgets.preview import ConfigPreview
from vtap100.tui.widgets.sidebar import ConfigSidebar
from vtap100.tui.widgets.sidebar import SectionSelected


class EditorScreen(Screen):
    """Main editor screen with 3-panel layout.

    Layout:
    ```
    +------------------+----------------------------------+-------------------+
    |   SIDEBAR        |          MAIN CONTENT            |   HELP PANEL      |
    |   (Navigation)   |          (Forms/Edit)            |   (Kontext F1)    |
    +------------------+----------------------------------+-------------------+
    |                       PREVIEW PANEL (toggle F2)                         |
    +------------------------------------------------------------------------+
    ```
    """

    def __init__(self, *args, **kwargs) -> None:
        """Initialize the editor screen."""
        super().__init__(*args, **kwargs)
        # Track currently displayed section to avoid unnecessary reloads
        self._current_section: tuple[str, int | None] | None = None
        # Store pending navigation for after dialog result
        self._pending_navigation: SectionSelected | None = None

    def compose(self) -> ComposeResult:
        """Compose the editor screen layout."""
        yield Header()

        with Vertical(id="editor-main"):
            # Top row: Sidebar | Main Content | Help Panel
            with Horizontal(id="top-row"):
                yield VerticalScroll(
                    ConfigSidebar(config=self.app.config, id="config-sidebar"),
                    id="sidebar",
                )

                yield VerticalScroll(
                    Static(t("common.messages.select_section"), classes="hint"),
                    id="main-content",
                )

                yield VerticalScroll(
                    HelpPanel(id="help-panel-widget"),
                    id="help-panel",
                )

            # Bottom: Preview Panel
            yield VerticalScroll(
                ConfigPreview(config=self.app.config, id="preview-widget"),
                id="preview-panel",
            )

        yield Footer()

    def _get_current_form(self) -> BaseConfigForm | None:
        """Get the currently displayed form, if any.

        Returns:
            The current form widget or None if no form is displayed.
        """
        main_content = self.query_one("#main-content")
        forms = main_content.query(BaseConfigForm)
        if forms:
            return forms.first()
        return None

    def _save_current_form(self) -> bool:
        """Save the current form.

        For SlotBasedConfigForm, calls the save() method directly.
        For other forms, simulates a save button click.

        Returns:
            True if save was successful, False otherwise.
        """
        form = self._get_current_form()
        if form is None:
            return False

        # SlotBasedConfigForm has a save() method we can call directly
        if isinstance(form, SlotBasedConfigForm):
            return form.save()

        # For other forms, press the save button
        from textual.widgets import Button

        try:
            save_btn = form.query_one("#save-btn", Button)
            save_btn.press()
            return True
        except Exception:
            return False

    def _handle_unsaved_changes_result(self, result: UnsavedChangesResult | None) -> None:
        """Handle the result from the unsaved changes dialog.

        Args:
            result: The user's choice from the dialog.
        """
        if result is None or result == UnsavedChangesResult.CANCEL:
            # User cancelled - stay on current form
            self._pending_navigation = None
            return

        if result == UnsavedChangesResult.SAVE:
            # Save changes first
            saved = self._save_current_form()
            if saved:
                # Refresh sidebar to show new/updated entry
                sidebar = self.query_one("#config-sidebar", ConfigSidebar)
                sidebar.refresh_tree()
                # Refresh preview
                self._refresh_preview()

        # For both SAVE and DISCARD, proceed with navigation
        if self._pending_navigation:
            event = self._pending_navigation
            self._pending_navigation = None
            # Navigate to the pending section
            self.call_later(self._do_navigation, event)

    async def _do_navigation(self, event: SectionSelected) -> None:
        """Actually perform the navigation to a new section.

        Args:
            event: The section selection event.
        """
        self._current_section = (event.section_id, event.index)
        main_content = self.query_one("#main-content")

        # Clear existing content (await to ensure removal completes before mounting new)
        await main_content.remove_children()

        # Load appropriate form based on section
        if event.section_id == "vas":
            if event.index is not None:
                self._load_vas_form(main_content, event.index)
            else:
                # Show form to add new VAS config
                self._load_vas_form(main_content, len(self.app.config.vas_configs), is_new=True)
        elif event.section_id == "smarttap":
            if event.index is not None:
                self._load_smarttap_form(main_content, event.index)
            else:
                # Show form to add new SmartTap config
                self._load_smarttap_form(
                    main_content, len(self.app.config.smarttap_configs), is_new=True
                )
        elif event.section_id == "desfire":
            if event.index is not None:
                self._load_desfire_form(main_content, event.index)
            else:
                # Show form to add new DESFire config
                apps_count = len(self.app.config.desfire.apps) if self.app.config.desfire else 0
                self._load_desfire_form(main_content, apps_count, is_new=True)
        elif event.section_id == "keyboard":
            self._load_keyboard_form(main_content)
        elif event.section_id == "nfc":
            self._load_nfc_form(main_content)
        elif event.section_id == "feedback":
            self._load_feedback_form(main_content)
        else:
            # Show placeholder for unknown sections
            main_content.mount(Static(f"{event.section_id.upper()}", classes="hint"))

    async def on_section_selected(self, event: SectionSelected) -> None:
        """Handle section selection from sidebar.

        Args:
            event: The section selection event.
        """
        # Skip reload if same section is already displayed
        new_section = (event.section_id, event.index)
        if self._current_section == new_section:
            return

        # Check if current form has unsaved changes
        current_form = self._get_current_form()
        if current_form is not None and current_form.is_dirty:
            # Store pending navigation and show dialog
            self._pending_navigation = event
            # Check if form is for a new entry (show "Add" instead of "Save")
            is_new_form = isinstance(current_form, SlotBasedConfigForm) and getattr(
                current_form, "is_new", False
            )
            self.app.push_screen(
                UnsavedChangesDialog(is_new=is_new_form),
                self._handle_unsaved_changes_result,
            )
            return

        # No unsaved changes - proceed directly
        await self._do_navigation(event)

    async def on_config_added(self, event: ConfigAdded) -> None:
        """Handle new configuration added.

        Refreshes the sidebar, loads the edit form, and shows success message.

        Args:
            event: The config added event.
        """
        # Refresh sidebar
        sidebar = self.query_one("#config-sidebar", ConfigSidebar)
        sidebar.refresh_tree()

        # Expand and select the new entry in the tree
        sidebar.select_entry(event.section_id, event.index)

        # Load the edit form for the new entry
        main_content = self.query_one("#main-content")
        await main_content.remove_children()

        # Update tracking to the new entry
        self._current_section = (event.section_id, event.index)

        # Load appropriate form and show success message in the form
        display_name = t(f"sections.{event.section_id}.label")
        if event.section_id == "vas":
            self._load_vas_form(main_content, event.index)
            form = main_content.query_one("#vas-form")
        elif event.section_id == "smarttap":
            self._load_smarttap_form(main_content, event.index)
            form = main_content.query_one("#smarttap-form")
        elif event.section_id == "desfire":
            self._load_desfire_form(main_content, event.index)
            form = main_content.query_one("#desfire-form")
        else:
            return

        # Mount success message in the form (so _clear_messages removes it)
        # Use form's timer so message auto-disappears
        if event.is_duplicate:
            msg = t("common.messages.config_duplicated", name=display_name)
        else:
            msg = t("common.messages.config_added", name=display_name)
        label = Label(msg, classes="success-message")
        form.mount(label)
        form.set_timer(form.MESSAGE_TIMEOUT, label.remove)

        # Refresh preview
        self._refresh_preview()

    async def on_config_removed(self, event: ConfigRemoved) -> None:
        """Handle configuration removed.

        Refreshes the sidebar and clears the form.

        Args:
            event: The config removed event.
        """
        # Reset current section tracking
        self._current_section = None

        # Clear form
        main_content = self.query_one("#main-content")
        await main_content.remove_children()
        main_content.mount(Static(t("common.messages.select_section"), classes="hint"))

        # Refresh sidebar and keep section expanded
        sidebar = self.query_one("#config-sidebar", ConfigSidebar)
        sidebar.refresh_tree()
        sidebar.expand_section(event.section_id)

        # Refresh preview
        self._refresh_preview()

    def on_help_context_changed(self, event: HelpContextChanged) -> None:
        """Handle help context changes from form fields.

        Updates the help panel to show context-sensitive help for the focused field.

        Args:
            event: The help context change event.
        """
        help_panel = self.query_one("#help-panel-widget", HelpPanel)
        help_panel.current_context = event.context

    def on_config_changed(self, event: ConfigChanged) -> None:
        """Handle config field changes from forms.

        Refreshes the preview to show current config state.

        Args:
            event: The config change event.
        """
        self._refresh_preview()

    def _refresh_preview(self) -> None:
        """Refresh the preview panel with current config."""
        try:
            preview = self.query_one("#preview-widget", ConfigPreview)
            preview.update_preview(self.app.config)
        except Exception:
            pass  # Preview may not be mounted yet

    def _load_vas_form(self, container: Container, index: int, is_new: bool = False) -> None:
        """Load VAS configuration form.

        Args:
            container: The container to mount the form in.
            index: The VAS config index.
            is_new: If True, this is a new config being added.
        """
        config = None
        if not is_new and index < len(self.app.config.vas_configs):
            config = self.app.config.vas_configs[index]

        form = VASConfigForm(config=config, index=index, is_new=is_new, id="vas-form")
        container.mount(form)

    def _load_smarttap_form(self, container: Container, index: int, is_new: bool = False) -> None:
        """Load Smart Tap configuration form.

        Args:
            container: The container to mount the form in.
            index: The Smart Tap config index.
            is_new: If True, this is a new config being added.
        """
        config = None
        if not is_new and index < len(self.app.config.smarttap_configs):
            config = self.app.config.smarttap_configs[index]

        form = SmartTapConfigForm(config=config, index=index, is_new=is_new, id="smarttap-form")
        container.mount(form)

    def _load_desfire_form(self, container: Container, index: int, is_new: bool = False) -> None:
        """Load DESFire configuration form.

        Args:
            container: The container to mount the form in.
            index: The DESFire app index.
            is_new: If True, this is a new config being added.
        """
        config = None
        if not is_new and self.app.config.desfire and index < len(self.app.config.desfire.apps):
            config = self.app.config.desfire.apps[index]

        form = DESFireConfigForm(config=config, index=index, is_new=is_new, id="desfire-form")
        container.mount(form)

    def _load_keyboard_form(self, container: Container) -> None:
        """Load keyboard configuration form.

        Args:
            container: The container to mount the form in.
        """
        config = self.app.config.keyboard
        form = KeyboardConfigForm(config=config, id="keyboard-form")
        container.mount(form)

    def _load_nfc_form(self, container: Container) -> None:
        """Load NFC tag configuration form.

        Args:
            container: The container to mount the form in.
        """
        config = self.app.config.nfc
        form = NFCConfigForm(config=config, id="nfc-form")
        container.mount(form)

    def _load_feedback_form(self, container: Container) -> None:
        """Load feedback (LED/Beep) configuration form.

        Args:
            container: The container to mount the form in.
        """
        config = self.app.config.feedback
        form = FeedbackConfigForm(config=config, id="feedback-form")
        container.mount(form)
