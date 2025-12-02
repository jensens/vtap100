"""VTAP100 TUI Editor.

A Textual-based terminal user interface for editing VTAP100 configurations.

Example:
    >>> from vtap100.tui import run
    >>> run()  # Start with empty config
    >>> run(input_path=Path("config.txt"))  # Load existing config
"""

from pathlib import Path

from vtap100.tui.app import VTAPEditorApp

__all__ = ["run", "VTAPEditorApp"]


def run(
    input_path: Path | None = None,
    output_path: Path | None = None,
) -> None:
    """Run the VTAP100 TUI editor.

    Args:
        input_path: Optional path to load an existing config.txt.
        output_path: Optional path for saving. Defaults to input_path if provided.
    """
    app = VTAPEditorApp(input_path=input_path, output_path=output_path)
    app.run()
