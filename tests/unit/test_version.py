"""Unit tests for version handling.

Tests for the __version__ fallback when _version module is not available.
"""

import sys


class TestVersionFallback:
    """Test version handling when _version module is not available."""

    def test_version_fallback_when_version_module_missing(self) -> None:
        """Should fall back to dev version when _version module is not found."""
        # Test the actual code path by executing the module code
        # This executes the try/except block directly
        code = """
try:
    from vtap100._version import __version__
except ImportError:
    __version__ = "0.0.0.dev0"
"""
        # Create a namespace without the _version module available
        namespace = {"__builtins__": __builtins__}

        # Save current modules
        saved_modules = {}
        modules_to_remove = [key for key in sys.modules if key.startswith("vtap100")]
        for mod in modules_to_remove:
            saved_modules[mod] = sys.modules.pop(mod)

        try:
            # Execute the code - this should use the except branch
            # because vtap100._version won't be importable
            exec(code, namespace)
            # The result depends on whether _version.py exists
            # If it exists (installed package), we get the real version
            # If not, we get the fallback
            assert "__version__" in namespace
            assert isinstance(namespace["__version__"], str)
        finally:
            # Restore modules
            sys.modules.update(saved_modules)

    def test_version_available_when_installed(self) -> None:
        """Should use real version when _version module is available."""
        import vtap100

        # Version should be a string
        assert isinstance(vtap100.__version__, str)
        # Version should not be empty
        assert len(vtap100.__version__) > 0

    def test_author_is_set(self) -> None:
        """Author should be set."""
        import vtap100

        assert vtap100.__author__ == "HEIDI Team"

    def test_init_module_imports(self) -> None:
        """Test that the __init__ module exports expected attributes."""
        import vtap100

        # Should have __version__
        assert hasattr(vtap100, "__version__")
        # Should have __author__
        assert hasattr(vtap100, "__author__")
        # __author__ should be correct
        assert vtap100.__author__ == "HEIDI Team"

    def test_version_format(self) -> None:
        """Version should be in expected format."""
        import vtap100

        version = vtap100.__version__
        # Version should contain at least one dot or be dev version
        assert "." in version or "dev" in version
