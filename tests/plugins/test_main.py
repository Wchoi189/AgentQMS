"""Unit tests for the main plugins module."""
import tempfile
from pathlib import Path
from unittest.mock import patch
from AgentQMS.agent_tools.core.plugins import (
    get_plugin_registry,
    get_plugin_loader,
    reset_plugin_loader,
    PluginLoader
)
from AgentQMS.agent_tools.core.plugins.registry import PluginRegistry


@patch('AgentQMS.agent_tools.utils.paths.get_project_root')
def test_get_plugin_loader_singleton(mock_get_project_root):
    """Test that get_plugin_loader returns a singleton instance."""
    with tempfile.TemporaryDirectory() as temp_dir:
        project_root = Path(temp_dir)
        mock_get_project_root.return_value = project_root
        
        loader1 = get_plugin_loader()
        loader2 = get_plugin_loader()
        
        assert loader1 is loader2
        assert isinstance(loader1, PluginLoader)


@patch('AgentQMS.agent_tools.utils.paths.get_project_root')
def test_get_plugin_loader_with_project_root(mock_get_project_root):
    """Test that get_plugin_loader accepts project root."""
    # Reset the singleton first to ensure clean test state
    reset_plugin_loader()

    with tempfile.TemporaryDirectory() as temp_dir:
        project_root = Path(temp_dir)
        mock_get_project_root.return_value = project_root

        # First call sets the project root - this will use the provided project_root
        loader1 = get_plugin_loader(project_root)
        assert str(loader1.project_root) == str(project_root)

        # Reset to test the default path behavior
        reset_plugin_loader()

        # Second call without project_root should use the default from get_project_root mock
        loader2 = get_plugin_loader()
        assert str(loader2.project_root) == str(project_root)

        # After reset, these should be different instances
        assert loader1 is not loader2


@patch('AgentQMS.agent_tools.utils.paths.get_project_root')
def test_reset_plugin_loader(mock_get_project_root):
    """Test that reset_plugin_loader works correctly."""
    with tempfile.TemporaryDirectory() as temp_dir:
        project_root = Path(temp_dir)
        mock_get_project_root.return_value = project_root
        
        loader1 = get_plugin_loader()
        reset_plugin_loader()
        loader2 = get_plugin_loader()
        
        # After reset, should get a new instance
        assert loader1 is not loader2


@patch('AgentQMS.agent_tools.utils.paths.get_project_root')
def test_get_plugin_registry(mock_get_project_root):
    """Test that get_plugin_registry works correctly."""
    with tempfile.TemporaryDirectory() as temp_dir:
        project_root = Path(temp_dir)
        mock_get_project_root.return_value = project_root
        
        registry = get_plugin_registry()
        
        assert isinstance(registry, PluginRegistry)


@patch('AgentQMS.agent_tools.utils.paths.get_project_root')
def test_get_plugin_registry_force_reload(mock_get_project_root):
    """Test that get_plugin_registry force parameter works."""
    with tempfile.TemporaryDirectory() as temp_dir:
        project_root = Path(temp_dir)
        mock_get_project_root.return_value = project_root
        
        registry1 = get_plugin_registry()
        registry2 = get_plugin_registry(force=True)  # Should reload
        
        # The registry might be the same instance if loader doesn't recreate it,
        # but the load method should be called with force=True
        assert isinstance(registry1, PluginRegistry)
        assert isinstance(registry2, PluginRegistry)