"""Unit tests for the PluginLoader module."""
import tempfile
from pathlib import Path
from unittest.mock import patch, Mock
from AgentQMS.agent_tools.core.plugins.loader import PluginLoader
from AgentQMS.agent_tools.core.plugins.registry import PluginRegistry


@patch('AgentQMS.agent_tools.utils.paths.get_project_root')
def test_plugin_loader_initialization(mock_get_project_root):
    """Test that PluginLoader initializes correctly."""
    with tempfile.TemporaryDirectory() as temp_dir:
        project_root = Path(temp_dir)
        mock_get_project_root.return_value = project_root
        
        loader = PluginLoader(project_root=project_root)
        
        assert loader.project_root == project_root
        assert loader.framework_root == project_root / "AgentQMS"


@patch('AgentQMS.agent_tools.utils.paths.get_project_root')
def test_load_with_caching(mock_get_project_root):
    """Test that PluginLoader caches the registry."""
    with tempfile.TemporaryDirectory() as temp_dir:
        project_root = Path(temp_dir)
        mock_get_project_root.return_value = project_root
        
        loader = PluginLoader(project_root=project_root)
        
        # First load
        registry1 = loader.load()
        # Second load (should return cached)
        registry2 = loader.load()
        
        assert registry1 is registry2
        
        # Force reload (should return new instance)
        registry3 = loader.load(force=True)
        assert registry1 is not registry3


@patch('AgentQMS.agent_tools.utils.paths.get_project_root')
def test_load_empty_discovery(mock_get_project_root):
    """Test loading when no plugins are discovered."""
    with tempfile.TemporaryDirectory() as temp_dir:
        project_root = Path(temp_dir)
        mock_get_project_root.return_value = project_root
        
        loader = PluginLoader(project_root=project_root)
        registry = loader.load()
        
        assert isinstance(registry, PluginRegistry)
        assert registry.artifact_types == {}
        assert registry.validators == {}
        assert registry.context_bundles == {}


def test_load_yaml():
    """Test loading YAML files."""
    with tempfile.TemporaryDirectory() as temp_dir:
        project_root = Path(temp_dir)
        framework_root = project_root / "AgentQMS"
        
        loader = PluginLoader.__new__(PluginLoader)  # Create without __init__
        loader.project_root = project_root
        loader.framework_root = framework_root
        
        # Create test YAML file
        test_file = Path(temp_dir) / "test.yaml"
        test_file.write_text("name: test\nversion: 1.0")
        
        data = loader._load_yaml(test_file)
        # YAML parses version: 1.0 as a float, not string
        assert data == {"name": "test", "version": 1.0}


def test_load_yaml_invalid_format():
    """Test loading YAML that's not a dictionary."""
    with tempfile.TemporaryDirectory() as temp_dir:
        project_root = Path(temp_dir)
        framework_root = project_root / "AgentQMS"
        
        loader = PluginLoader.__new__(PluginLoader)
        loader.project_root = project_root
        loader.framework_root = framework_root
        
        # Create test YAML file with list instead of dict
        test_file = Path(temp_dir) / "test.yaml"
        test_file.write_text("- item1\n- item2")
        
        try:
            loader._load_yaml(test_file)
            assert False, "Should have raised ValueError"
        except ValueError:
            pass  # Expected


def test_merge_validators():
    """Test merging validator configurations."""
    with tempfile.TemporaryDirectory() as temp_dir:
        project_root = Path(temp_dir)
        framework_root = project_root / "AgentQMS"
        
        loader = PluginLoader.__new__(PluginLoader)
        loader.project_root = project_root
        loader.framework_root = framework_root
        
        base = {
            "prefixes": {"REQ": "requirements"},
            "types": ["bug"],
            "categories": ["security"],
            "statuses": ["open"],
            "rules": {"rule1": "value1"},
            "custom_validators": ["validator1"],
            "disabled_validators": ["disabled1"]
        }
        
        override = {
            "prefixes": {"REQ": "req_new", "ARCH": "architecture"},  # Should override REQ, add ARCH
            "types": ["feature", "bug"],  # Should merge with unique values
            "categories": ["performance"],  # Should add to existing
            "statuses": ["closed", "open"],  # Should merge with existing
            "rules": {"rule2": "value2"},  # Should add new rule
            "custom_validators": ["validator2"],  # Should append
            "disabled_validators": ["disabled2"]  # Should merge with existing
        }
        
        loader._merge_validators(base, override)
        
        # Check prefixes - override should win for existing keys
        assert base["prefixes"] == {"REQ": "req_new", "ARCH": "architecture"}
        # Check types - should be unique sorted values
        assert set(base["types"]) == {"bug", "feature"}
        assert len(base["types"]) == 2  # Should be sorted
        # Check categories - should be merged
        assert set(base["categories"]) == {"security", "performance"}
        # Check statuses - should be merged
        assert set(base["statuses"]) == {"open", "closed"}
        # Check rules - should be merged
        assert base["rules"] == {"rule1": "value1", "rule2": "value2"}
        # Check custom validators - should be appended
        assert base["custom_validators"] == ["validator1", "validator2"]
        # Check disabled validators - should be merged
        assert set(base["disabled_validators"]) == {"disabled1", "disabled2"}


def test_should_override_logic():
    """Test the override logic for plugins."""
    with tempfile.TemporaryDirectory() as temp_dir:
        project_root = Path(temp_dir)
        framework_root = project_root / "AgentQMS"
        
        loader = PluginLoader.__new__(PluginLoader)
        loader.project_root = project_root
        loader.framework_root = framework_root
        
        # Create a registry with an existing framework plugin
        registry = PluginRegistry()
        from AgentQMS.agent_tools.core.plugins.registry import PluginMetadata
        registry.metadata.append(PluginMetadata(
            name="test_type",
            version="1.0",
            source="framework",
            path="/test/path",
            plugin_type="artifact_type"
        ))
        
        # Project should override framework
        assert loader._should_override(registry, "test_type", "artifact_type", "project")
        
        # Framework should not override project
        registry.metadata.clear()
        registry.metadata.append(PluginMetadata(
            name="test_type",
            version="1.0",
            source="project",
            path="/test/path",
            plugin_type="artifact_type"
        ))
        assert not loader._should_override(registry, "test_type", "artifact_type", "framework")
        
        # Same source should override (later wins)
        assert loader._should_override(registry, "test_type", "artifact_type", "project")
        
        # No existing plugin should be allowed
        registry.metadata.clear()
        assert loader._should_override(registry, "test_type", "artifact_type", "framework")


def test_get_discovery_paths():
    """Test getting discovery paths from loader."""
    with tempfile.TemporaryDirectory() as temp_dir:
        project_root = Path(temp_dir)
        mock_project_root = project_root
        mock_framework_root = mock_project_root / "AgentQMS"
        
        loader = PluginLoader.__new__(PluginLoader)
        loader.project_root = mock_project_root
        loader.framework_root = mock_framework_root
        loader.discovery = Mock()
        loader.discovery.get_discovery_paths.return_value = {
            "framework": "/mock/framework",
            "project": "/mock/project"
        }
        
        paths = loader.get_discovery_paths()
        assert paths == {"framework": "/mock/framework", "project": "/mock/project"}