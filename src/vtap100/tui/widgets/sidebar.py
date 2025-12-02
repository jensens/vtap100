"""Sidebar widget for navigation.

Provides a tree-based navigation for all VTAP100 configuration sections.
"""

from textual.app import ComposeResult
from textual.message import Message
from textual.widget import Widget
from textual.widgets import Tree

from vtap100.models.config import VTAPConfig
from vtap100.tui.i18n import t


class SectionSelected(Message):
    """Message posted when a section is selected in the sidebar.

    Attributes:
        section_id: The ID of the selected section (e.g., "vas", "keyboard").
        index: Optional index for list-based sections (e.g., VAS #2).
    """

    def __init__(self, section_id: str, index: int | None = None) -> None:
        """Initialize the message.

        Args:
            section_id: The section identifier.
            index: Optional index within the section.
        """
        super().__init__()
        self.section_id = section_id
        self.index = index


class ConfigSidebar(Widget):
    """Navigation sidebar with tree for all configuration sections.

    Displays a tree structure with all VTAP100 configuration areas.
    Each section shows a badge with the number of configured items.

    Attributes:
        SECTIONS: List of (section_id, label, config_attr) tuples.
    """

    @property
    def sections(self) -> list[tuple[str, str, str]]:
        """Get section definitions with translated labels."""
        return [
            ("vas", t("sections.vas.label"), "vas_configs"),
            ("smarttap", t("sections.smarttap.label"), "smarttap_configs"),
            ("keyboard", t("sections.keyboard.label"), "keyboard"),
            ("nfc", t("sections.nfc.label"), "nfc"),
            ("desfire", t("sections.desfire.label"), "desfire"),
            ("feedback", t("sections.feedback.label"), "feedback"),
        ]

    # Maximum number of entries per section (key slots 0-6 for VAS/SmartTap, 9 for DESFire)
    MAX_ENTRIES = 7
    MAX_DESFIRE_ENTRIES = 9

    DEFAULT_CSS = """
    ConfigSidebar {
        width: 100%;
        height: 100%;
    }

    ConfigSidebar > Tree {
        width: 100%;
        height: 1fr;
    }
    """

    def __init__(
        self,
        config: VTAPConfig | None = None,
        id: str | None = None,
    ) -> None:
        """Initialize the sidebar.

        Args:
            config: The VTAPConfig to display.
            id: Optional widget ID.
        """
        super().__init__(id=id)
        self._config = config or VTAPConfig()

    @property
    def config(self) -> VTAPConfig:
        """Get the current config."""
        return self._config

    @config.setter
    def config(self, value: VTAPConfig) -> None:
        """Set the config and refresh the tree."""
        self._config = value
        self._refresh_tree()

    def _get_entry_label(self, section_id: str, item: object, _index: int) -> str:
        """Get the display label for a tree entry.

        Args:
            section_id: The section identifier (e.g., "vas", "smarttap", "desfire").
            item: The config item (AppleVASConfig, GoogleSmartTapConfig, or DESFireAppConfig).
            _index: The item index (unused, kept for potential future use).

        Returns:
            Label like "pass.com.example (Slot 2)" or "96972794 (Auto)" or "AABBCC".
        """
        if section_id == "vas":
            merchant_id = getattr(item, "merchant_id", "?")
            key_slot = getattr(item, "key_slot", 0)
            slot_text = t("common.labels.auto") if key_slot == 0 else t("common.labels.slot", num=key_slot)
            return f"{merchant_id} ({slot_text})"
        elif section_id == "smarttap":
            collector_id = getattr(item, "collector_id", "?")
            key_slot = getattr(item, "key_slot", 0)
            slot_text = t("common.labels.auto") if key_slot == 0 else t("common.labels.slot", num=key_slot)
            return f"{collector_id} ({slot_text})"
        elif section_id == "desfire":
            app_id = getattr(item, "app_id", "?")
            return f"App {app_id}"
        return f"#{_index + 1}"

    def compose(self) -> ComposeResult:
        """Compose the sidebar with a navigation tree."""
        tree: Tree[str] = Tree(t("common.labels.configuration"))
        tree.root.expand()

        for section_id, label, attr in self.sections:
            badge = self._get_badge(section_id, attr)
            node = tree.root.add(f"{label}{badge}", data=section_id)

            # For list-based sections, add sub-nodes for each item
            if section_id in ("vas", "smarttap", "desfire"):
                items = self._get_section_items(attr, section_id)
                for i, item in enumerate(items):
                    entry_label = self._get_entry_label(section_id, item, i)
                    node.add(entry_label, data=f"{section_id}:{i}")
                # Add "New Entry" if slots available
                max_entries = self.MAX_DESFIRE_ENTRIES if section_id == "desfire" else self.MAX_ENTRIES
                if len(items) < max_entries:
                    node.add(t("common.labels.new_entry"), data=f"{section_id}:new")

        yield tree

    def _get_badge(self, section_id: str, attr: str) -> str:
        """Get badge text showing item count or status.

        Args:
            section_id: The section identifier.
            attr: The config attribute name.

        Returns:
            Badge string like " [2]" or empty string.
        """
        if section_id in ("vas", "smarttap", "desfire"):
            items = self._get_section_items(attr, section_id)
            if items:
                return f" [{len(items)}]"
        else:
            # For single-value sections, show checkmark if configured
            value = getattr(self._config, attr, None)
            if value is not None:
                return " [✓]"
        return ""

    def _get_section_items(self, attr: str, section_id: str = "") -> list:
        """Get items for a list-based section.

        Args:
            attr: The config attribute name.
            section_id: The section identifier (needed for desfire.apps).

        Returns:
            List of items or empty list.
        """
        if section_id == "desfire":
            # DESFireConfig has .apps list
            config = getattr(self._config, attr, None)
            return config.apps if config else []
        return getattr(self._config, attr, []) or []

    def refresh_tree(self) -> None:
        """Refresh the tree to reflect config changes.

        Syncs with app.config and rebuilds the tree.
        """
        # Sync with app config
        self._config = self.app.config
        self._refresh_tree()

    def _refresh_tree(self) -> None:
        """Refresh the tree to reflect config changes."""
        try:
            tree = self.query_one(Tree)
            # Clear and rebuild
            tree.root.remove_children()
            for section_id, label, attr in self.sections:
                badge = self._get_badge(section_id, attr)
                node = tree.root.add(f"{label}{badge}", data=section_id)

                if section_id in ("vas", "smarttap", "desfire"):
                    items = self._get_section_items(attr, section_id)
                    for i, item in enumerate(items):
                        entry_label = self._get_entry_label(section_id, item, i)
                        node.add(entry_label, data=f"{section_id}:{i}")
                    # Add "New Entry" if slots available
                    max_entries = self.MAX_DESFIRE_ENTRIES if section_id == "desfire" else self.MAX_ENTRIES
                    if len(items) < max_entries:
                        node.add(t("common.labels.new_entry"), data=f"{section_id}:new")
        except Exception:
            pass  # Tree may not be mounted yet

    def expand_section(self, section_id: str) -> None:
        """Expand a section without selecting any entry.

        Args:
            section_id: The section identifier (e.g., "vas", "smarttap").
        """
        # Force tree refresh and then expand the section
        tree = self.query_one(Tree)
        tree.refresh()
        tree.call_after_refresh(self._do_expand_section, section_id)

    def _do_expand_section(self, section_id: str) -> None:
        """Actually expand the section node and select it.

        Args:
            section_id: The section identifier (e.g., "vas", "smarttap").
        """
        tree = self.query_one(Tree)
        for section_node in tree.root.children:
            if section_node.data == section_id:
                section_node.expand()
                # Select the section node itself (call twice for Textual quirk)
                tree.select_node(section_node)
                tree.select_node(section_node)
                return

    def select_entry(self, section_id: str, index: int) -> None:
        """Expand the section and select a specific entry.

        Args:
            section_id: The section identifier (e.g., "vas", "smarttap").
            index: The entry index to select.
        """
        # Force tree refresh and then select the node
        tree = self.query_one(Tree)
        tree.refresh()
        tree.call_after_refresh(self._do_select_entry, section_id, index)

    def _do_select_entry(self, section_id: str, index: int) -> None:
        """Actually perform the tree node selection.

        Args:
            section_id: The section identifier (e.g., "vas", "smarttap").
            index: The entry index to select.
        """
        tree = self.query_one(Tree)
        target_data = f"{section_id}:{index}"
        # Find the section node
        for section_node in tree.root.children:
            if section_node.data == section_id:
                # Expand the section
                section_node.expand()
                # Find and select the entry node
                for entry_node in section_node.children:
                    if entry_node.data == target_data:
                        # Call select_node twice - first call assigns line number,
                        # second call actually moves cursor (Textual quirk)
                        tree.select_node(entry_node)
                        tree.select_node(entry_node)
                        return
                return
        return

    def on_tree_node_selected(self, event: Tree.NodeSelected) -> None:
        """Handle tree node selection.

        Args:
            event: The node selection event.
        """
        if event.node.data:
            data = str(event.node.data)
            if ":" in data:
                # Sub-item selected (e.g., "vas:0" or "vas:new")
                section_id, index_str = data.split(":", 1)
                if index_str == "new":
                    # New entry - pass None as index to signal new form
                    self.post_message(SectionSelected(section_id, index=None))
                else:
                    self.post_message(SectionSelected(section_id, int(index_str)))
            elif data not in ("vas", "smarttap", "desfire"):
                # Single-value section selected (keyboard, nfc, etc.)
                self.post_message(SectionSelected(data))
