"""Unit tests for TUI Forms - Phase 5.

Tests for:
- KeyboardConfigForm
- NFCConfigForm
- FeedbackConfigForm

Note: DESFire is more complex and will be handled separately.
"""

import pytest
from vtap100.models.config import VTAPConfig
from vtap100.models.feedback import FeedbackConfig
from vtap100.models.feedback import LEDConfig
from vtap100.models.feedback import LEDMode
from vtap100.models.keyboard import KeyboardConfig
from vtap100.models.nfc import NFCTagConfig
from vtap100.models.nfc import NFCTagMode


class TestKeyboardFormImports:
    """Test that keyboard form can be imported."""

    def test_import_keyboard_form(self) -> None:
        """KeyboardConfigForm should be importable."""
        from vtap100.tui.widgets.forms.keyboard import KeyboardConfigForm

        assert KeyboardConfigForm is not None


class TestKeyboardConfigForm:
    """Test KeyboardConfigForm widget."""

    def test_keyboard_form_section_name(self) -> None:
        """KeyboardConfigForm should have correct section name."""
        from vtap100.tui.widgets.forms.keyboard import KeyboardConfigForm

        form = KeyboardConfigForm()
        assert form.SECTION_NAME == "keyboard"


class TestKeyboardConfigFormAsync:
    """Async tests for KeyboardConfigForm."""

    @pytest.mark.asyncio
    async def test_keyboard_form_has_log_mode_switch(self) -> None:
        """KeyboardConfigForm should have log_mode switch."""
        from textual.widgets import Switch
        from textual.widgets import Tree
        from vtap100.tui.app import VTAPEditorApp

        app = VTAPEditorApp()
        app.config = VTAPConfig(keyboard=KeyboardConfig(log_mode=True))

        async with app.run_test() as pilot:
            await pilot.pause()

            # Select Keyboard section
            sidebar = app.screen.query_one("#sidebar")
            tree = sidebar.query_one(Tree)
            # Keyboard is 3rd section (index 2)
            keyboard_node = tree.root.children[2]
            tree.select_node(keyboard_node)
            await pilot.pause()
            await pilot.pause()

            main_content = app.screen.query_one("#main-content")
            switch = main_content.query_one("#log_mode", Switch)
            assert switch is not None
            assert switch.value is True

    @pytest.mark.asyncio
    async def test_keyboard_form_has_source_switches(self) -> None:
        """KeyboardConfigForm should have source bit switches."""
        from textual.widgets import Switch
        from textual.widgets import Tree
        from vtap100.tui.app import VTAPEditorApp

        app = VTAPEditorApp()
        # A5 = mobile_pass + card_emulation + scanners + card_tag_uid
        app.config = VTAPConfig(keyboard=KeyboardConfig(source="A5"))

        async with app.run_test() as pilot:
            await pilot.pause()

            sidebar = app.screen.query_one("#sidebar")
            tree = sidebar.query_one(Tree)
            keyboard_node = tree.root.children[2]
            tree.select_node(keyboard_node)
            await pilot.pause()
            await pilot.pause()

            main_content = app.screen.query_one("#main-content")
            # Check that source bit switches exist and have correct values for A5
            mobile_pass = main_content.query_one("#source_mobile_pass", Switch)
            assert mobile_pass.value is True
            card_emulation = main_content.query_one("#source_card_emulation", Switch)
            assert card_emulation.value is True
            scanners = main_content.query_one("#source_scanners", Switch)
            assert scanners.value is True
            card_tag_uid = main_content.query_one("#source_card_tag_uid", Switch)
            assert card_tag_uid.value is True
            # STUID and command_interface should be False for A5
            stuid = main_content.query_one("#source_stuid", Switch)
            assert stuid.value is False

    @pytest.mark.asyncio
    async def test_keyboard_form_saves_config(self) -> None:
        """KeyboardConfigForm should save changes to app.config."""
        from textual.widgets import Button
        from textual.widgets import Switch
        from textual.widgets import Tree
        from vtap100.tui.app import VTAPEditorApp

        app = VTAPEditorApp()
        app.config = VTAPConfig(keyboard=KeyboardConfig(log_mode=False))

        async with app.run_test() as pilot:
            await pilot.pause()

            sidebar = app.screen.query_one("#sidebar")
            tree = sidebar.query_one(Tree)
            keyboard_node = tree.root.children[2]
            tree.select_node(keyboard_node)
            await pilot.pause()
            await pilot.pause()

            main_content = app.screen.query_one("#main-content")

            # Toggle log_mode on
            switch = main_content.query_one("#log_mode", Switch)
            switch.toggle()
            await pilot.pause()

            # Click save
            save_btn = main_content.query_one("#save", Button)
            save_btn.press()
            await pilot.pause()

            # Config should be updated
            assert app.config.keyboard is not None
            assert app.config.keyboard.log_mode is True

    @pytest.mark.asyncio
    async def test_keyboard_section_shows_checkmark_when_configured(self) -> None:
        """Keyboard section should show checkmark when configured."""
        from textual.widgets import Tree
        from vtap100.tui.app import VTAPEditorApp

        app = VTAPEditorApp()
        app.config = VTAPConfig(keyboard=KeyboardConfig(log_mode=True))

        async with app.run_test() as pilot:
            await pilot.pause()

            sidebar = app.screen.query_one("#sidebar")
            tree = sidebar.query_one(Tree)
            keyboard_node = tree.root.children[2]
            label = str(keyboard_node.label)
            # Should show checkmark
            assert "✓" in label


class TestKeyboardHelpYaml:
    """Test keyboard help YAML exists and has content."""

    def test_keyboard_help_exists(self) -> None:
        """Keyboard help should be loaded."""
        from vtap100.tui.help import HelpLoader

        result = HelpLoader.load_all()
        assert "keyboard" in result

    def test_keyboard_log_mode_help_exists(self) -> None:
        """Keyboard log_mode help should exist."""
        from vtap100.tui.help import HelpLoader

        result = HelpLoader.load_all()
        assert "keyboard.log_mode" in result


# ============================================================================
# NFC Config Form Tests
# ============================================================================


class TestNFCFormImports:
    """Test that NFC form can be imported."""

    def test_import_nfc_form(self) -> None:
        """NFCConfigForm should be importable."""
        from vtap100.tui.widgets.forms.nfc import NFCConfigForm

        assert NFCConfigForm is not None


class TestNFCConfigForm:
    """Test NFCConfigForm widget."""

    def test_nfc_form_section_name(self) -> None:
        """NFCConfigForm should have correct section name."""
        from vtap100.tui.widgets.forms.nfc import NFCConfigForm

        form = NFCConfigForm()
        assert form.SECTION_NAME == "nfc"


class TestNFCConfigFormAsync:
    """Async tests for NFCConfigForm."""

    @pytest.mark.asyncio
    async def test_nfc_form_has_type2_select(self) -> None:
        """NFCConfigForm should have type2 Select."""
        from textual.widgets import Select
        from textual.widgets import Tree
        from vtap100.tui.app import VTAPEditorApp

        app = VTAPEditorApp()
        app.config = VTAPConfig(nfc=NFCTagConfig(type2=NFCTagMode.UID))

        async with app.run_test() as pilot:
            await pilot.pause()

            # Select NFC section (index 3)
            sidebar = app.screen.query_one("#sidebar")
            tree = sidebar.query_one(Tree)
            nfc_node = tree.root.children[3]
            tree.select_node(nfc_node)
            await pilot.pause()
            await pilot.pause()

            main_content = app.screen.query_one("#main-content")
            select = main_content.query_one("#type2", Select)
            assert select is not None

    @pytest.mark.asyncio
    async def test_nfc_form_saves_config(self) -> None:
        """NFCConfigForm should save changes to app.config."""
        from textual.widgets import Button
        from textual.widgets import Tree
        from vtap100.tui.app import VTAPEditorApp

        app = VTAPEditorApp()
        app.config = VTAPConfig(nfc=NFCTagConfig())

        async with app.run_test() as pilot:
            await pilot.pause()

            sidebar = app.screen.query_one("#sidebar")
            tree = sidebar.query_one(Tree)
            nfc_node = tree.root.children[3]
            tree.select_node(nfc_node)
            await pilot.pause()
            await pilot.pause()

            main_content = app.screen.query_one("#main-content")

            # Click save
            save_btn = main_content.query_one("#save", Button)
            save_btn.press()
            await pilot.pause()

            # Config should be updated
            assert app.config.nfc is not None


class TestNFCHelpYaml:
    """Test NFC help YAML exists."""

    def test_nfc_help_exists(self) -> None:
        """NFC help should be loaded."""
        from vtap100.tui.help import HelpLoader

        result = HelpLoader.load_all()
        assert "nfc" in result


# ============================================================================
# Feedback Config Form Tests
# ============================================================================


class TestFeedbackFormImports:
    """Test that Feedback form can be imported."""

    def test_import_feedback_form(self) -> None:
        """FeedbackConfigForm should be importable."""
        from vtap100.tui.widgets.forms.feedback import FeedbackConfigForm

        assert FeedbackConfigForm is not None


class TestFeedbackConfigForm:
    """Test FeedbackConfigForm widget."""

    def test_feedback_form_section_name(self) -> None:
        """FeedbackConfigForm should have correct section name."""
        from vtap100.tui.widgets.forms.feedback import FeedbackConfigForm

        form = FeedbackConfigForm()
        assert form.SECTION_NAME == "feedback"


class TestFeedbackConfigFormAsync:
    """Async tests for FeedbackConfigForm."""

    @pytest.mark.asyncio
    async def test_feedback_form_has_led_mode_select(self) -> None:
        """FeedbackConfigForm should have LED mode Select."""
        from textual.widgets import Select
        from textual.widgets import Tree
        from vtap100.tui.app import VTAPEditorApp

        app = VTAPEditorApp()
        app.config = VTAPConfig(feedback=FeedbackConfig(led=LEDConfig(mode=LEDMode.STATUS)))

        async with app.run_test() as pilot:
            await pilot.pause()

            # Select Feedback section (index 5)
            sidebar = app.screen.query_one("#sidebar")
            tree = sidebar.query_one(Tree)
            feedback_node = tree.root.children[5]
            tree.select_node(feedback_node)
            await pilot.pause()
            await pilot.pause()

            main_content = app.screen.query_one("#main-content")
            select = main_content.query_one("#led_mode", Select)
            assert select is not None


class TestFeedbackHelpYaml:
    """Test Feedback help YAML exists."""

    def test_feedback_help_exists(self) -> None:
        """Feedback help should be loaded."""
        from vtap100.tui.help import HelpLoader

        result = HelpLoader.load_all()
        assert "feedback" in result


# ============================================================================
# DESFire Config Form Tests
# ============================================================================


class TestDESFireFormImports:
    """Test that DESFire form can be imported."""

    def test_import_desfire_form(self) -> None:
        """DESFireConfigForm should be importable."""
        from vtap100.tui.widgets.forms.desfire import DESFireConfigForm

        assert DESFireConfigForm is not None


class TestDESFireConfigForm:
    """Test DESFireConfigForm widget."""

    def test_desfire_form_section_name(self) -> None:
        """DESFireConfigForm should have correct section name."""
        from vtap100.tui.widgets.forms.desfire import DESFireConfigForm

        form = DESFireConfigForm()
        assert form.SECTION_NAME == "desfire"


class TestDESFireConfigFormAsync:
    """Async tests for DESFireConfigForm."""

    @pytest.mark.asyncio
    async def test_desfire_form_has_app_id_input(self) -> None:
        """DESFireConfigForm should have app_id input."""
        from textual.widgets import Input
        from textual.widgets import Tree
        from vtap100.models.desfire import DESFireAppConfig
        from vtap100.models.desfire import DESFireConfig
        from vtap100.tui.app import VTAPEditorApp

        app = VTAPEditorApp()
        app.config = VTAPConfig(desfire=DESFireConfig(apps=[DESFireAppConfig(app_id="AABBCC")]))

        async with app.run_test() as pilot:
            await pilot.pause()

            # Select DESFire section (index 4) and first entry
            sidebar = app.screen.query_one("#sidebar")
            tree = sidebar.query_one(Tree)
            desfire_node = tree.root.children[4]
            desfire_node.expand()
            await pilot.pause()
            # Select first entry
            tree.select_node(desfire_node.children[0])
            await pilot.pause()
            await pilot.pause()

            main_content = app.screen.query_one("#main-content")
            input_widget = main_content.query_one("#app_id", Input)
            assert input_widget is not None
            assert input_widget.value == "AABBCC"

    @pytest.mark.asyncio
    async def test_desfire_form_has_crypto_select(self) -> None:
        """DESFireConfigForm should have crypto Select."""
        from textual.widgets import Select
        from textual.widgets import Tree
        from vtap100.models.desfire import DESFireAppConfig
        from vtap100.models.desfire import DESFireConfig
        from vtap100.models.desfire import DESFireCryptoMode
        from vtap100.tui.app import VTAPEditorApp

        app = VTAPEditorApp()
        app.config = VTAPConfig(
            desfire=DESFireConfig(
                apps=[DESFireAppConfig(app_id="AABBCC", crypto=DESFireCryptoMode.AES)]
            )
        )

        async with app.run_test() as pilot:
            await pilot.pause()

            sidebar = app.screen.query_one("#sidebar")
            tree = sidebar.query_one(Tree)
            desfire_node = tree.root.children[4]
            desfire_node.expand()
            await pilot.pause()
            tree.select_node(desfire_node.children[0])
            await pilot.pause()
            await pilot.pause()

            main_content = app.screen.query_one("#main-content")
            select = main_content.query_one("#crypto", Select)
            assert select is not None

    @pytest.mark.asyncio
    async def test_desfire_form_saves_config(self) -> None:
        """DESFireConfigForm should save changes to app.config."""
        from textual.widgets import Button
        from textual.widgets import Input
        from textual.widgets import Tree
        from vtap100.models.desfire import DESFireAppConfig
        from vtap100.models.desfire import DESFireConfig
        from vtap100.tui.app import VTAPEditorApp

        app = VTAPEditorApp()
        app.config = VTAPConfig(desfire=DESFireConfig(apps=[DESFireAppConfig(app_id="AABBCC")]))

        async with app.run_test() as pilot:
            await pilot.pause()

            sidebar = app.screen.query_one("#sidebar")
            tree = sidebar.query_one(Tree)
            desfire_node = tree.root.children[4]
            desfire_node.expand()
            await pilot.pause()
            tree.select_node(desfire_node.children[0])
            await pilot.pause()
            await pilot.pause()

            main_content = app.screen.query_one("#main-content")

            # Change app_id
            app_id_input = main_content.query_one("#app_id", Input)
            app_id_input.value = "112233"
            await pilot.pause()

            # Click save
            save_btn = main_content.query_one("#save", Button)
            save_btn.press()
            await pilot.pause()

            # Config should be updated
            assert app.config.desfire is not None
            assert len(app.config.desfire.apps) == 1
            assert app.config.desfire.apps[0].app_id == "112233"

    @pytest.mark.asyncio
    async def test_desfire_add_new_entry(self) -> None:
        """DESFireConfigForm should allow adding new entries."""
        from textual.widgets import Button
        from textual.widgets import Input
        from textual.widgets import Tree
        from vtap100.models.desfire import DESFireConfig
        from vtap100.tui.app import VTAPEditorApp

        app = VTAPEditorApp()
        app.config = VTAPConfig(desfire=DESFireConfig(apps=[]))

        async with app.run_test() as pilot:
            await pilot.pause()

            sidebar = app.screen.query_one("#sidebar")
            tree = sidebar.query_one(Tree)
            desfire_node = tree.root.children[4]
            desfire_node.expand()
            await pilot.pause()
            # Select "+ Neuer Eintrag"
            tree.select_node(desfire_node.children[0])
            await pilot.pause()
            await pilot.pause()

            main_content = app.screen.query_one("#main-content")

            # Fill in required app_id
            app_id_input = main_content.query_one("#app_id", Input)
            app_id_input.value = "DDEEFF"
            await pilot.pause()

            # Click add
            add_btn = main_content.query_one("#add", Button)
            add_btn.press()
            await pilot.pause()

            # Config should have new entry
            assert len(app.config.desfire.apps) == 1
            assert app.config.desfire.apps[0].app_id == "DDEEFF"


class TestDESFireHelpYaml:
    """Test DESFire help YAML exists."""

    def test_desfire_help_exists(self) -> None:
        """DESFire help should be loaded."""
        from vtap100.tui.help import HelpLoader

        result = HelpLoader.load_all()
        assert "desfire" in result

    def test_desfire_app_id_help_exists(self) -> None:
        """DESFire app_id help should exist."""
        from vtap100.tui.help import HelpLoader

        result = HelpLoader.load_all()
        assert "desfire.app_id" in result
