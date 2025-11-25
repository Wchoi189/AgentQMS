"""Unit tests for the PluginDiscovery module."""
import tempfile
from pathlib import Path
from AgentQMS.agent_tools.core.plugins.discovery import PluginDiscovery, DiscoveredPlugin


def test_plugin_discovery_initialization():
    """Test that PluginDiscovery initializes with correct paths."""
    with tempfile.TemporaryDirectory() as temp_dir:
        project_root = Path(temp_dir)
        framework_root = project_root / "AgentQMS"
        
        discovery = PluginDiscovery(project_root=project_root, framework_root=framework_root)
        
        assert discovery.project_root == project_root
        assert discovery.framework_root == framework_root
        assert discovery.framework_plugins_dir == framework_root / "conventions" / "plugins"
        assert discovery.project_plugins_dir == project_root / ".agentqms" / "plugins"


def test_discover_from_directory_with_artifact_types():
    """Test discovering artifact type plugins from directory."""
    with tempfile.TemporaryDirectory() as temp_dir:
        project_root = Path(temp_dir)
        framework_root = project_root / "AgentQMS"
        framework_plugins_dir = framework_root / "conventions" / "plugins"
        artifact_types_dir = framework_plugins_dir / "artifact_types"
        artifact_types_dir.mkdir(parents=True)
        
        # Create test YAML files
        (artifact_types_dir / "test1.yaml").write_text("name: test1")
        (artifact_types_dir / "test2.yaml").write_text("name: test2")
        
        discovery = PluginDiscovery(project_root=project_root, framework_root=framework_root)
        plugins = discovery._discover_from_directory(framework_plugins_dir, "framework")
        
        assert len(plugins) == 2
        assert all(p.source == "framework" for p in plugins)
        assert all(p.plugin_type == "artifact_type" for p in plugins)
        assert {p.path.name for p in plugins} == {"test1.yaml", "test2.yaml"}


def test_discover_from_directory_with_validators():
    """Test discovering validators plugin from directory."""
    with tempfile.TemporaryDirectory() as temp_dir:
        project_root = Path(temp_dir)
        framework_root = project_root / "AgentQMS"
        framework_plugins_dir = framework_root / "conventions" / "plugins"
        framework_plugins_dir.mkdir(parents=True)
        
        # Create validators.yaml
        (framework_plugins_dir / "validators.yaml").write_text("prefixes: {}")
        
        discovery = PluginDiscovery(project_root=project_root, framework_root=framework_root)
        plugins = discovery._discover_from_directory(framework_plugins_dir, "framework")
        
        assert len(plugins) == 1
        assert plugins[0].plugin_type == "validators"
        assert plugins[0].path.name == "validators.yaml"


def test_discover_from_directory_with_context_bundles():
    """Test discovering context bundle plugins from directory."""
    with tempfile.TemporaryDirectory() as temp_dir:
        project_root = Path(temp_dir)
        framework_root = project_root / "AgentQMS"
        framework_plugins_dir = framework_root / "conventions" / "plugins"
        context_bundles_dir = framework_plugins_dir / "context_bundles"
        context_bundles_dir.mkdir(parents=True)
        
        # Create test YAML files
        (context_bundles_dir / "bundle1.yaml").write_text("name: bundle1")
        (context_bundles_dir / "bundle2.yaml").write_text("name: bundle2")
        
        discovery = PluginDiscovery(project_root=project_root, framework_root=framework_root)
        plugins = discovery._discover_from_directory(framework_plugins_dir, "project")
        
        assert len(plugins) == 2
        assert all(p.source == "project" for p in plugins)
        assert all(p.plugin_type == "context_bundle" for p in plugins)
        assert {p.path.name for p in plugins} == {"bundle1.yaml", "bundle2.yaml"}


def test_discover_all_when_no_directories_exist():
    """Test discovering plugins when directories don't exist."""
    with tempfile.TemporaryDirectory() as temp_dir:
        project_root = Path(temp_dir)
        framework_root = project_root / "AgentQMS"
        
        discovery = PluginDiscovery(project_root=project_root, framework_root=framework_root)
        plugins = discovery.discover_all()
        
        assert plugins == []


def test_discover_all_with_both_directories():
    """Test discovering plugins from both framework and project directories."""
    with tempfile.TemporaryDirectory() as temp_dir:
        project_root = Path(temp_dir)
        framework_root = project_root / "AgentQMS"
        
        # Create framework plugins directory with artifact types
        framework_plugins_dir = framework_root / "conventions" / "plugins"
        framework_artifact_types_dir = framework_plugins_dir / "artifact_types"
        framework_artifact_types_dir.mkdir(parents=True)
        (framework_artifact_types_dir / "fw_artifact.yaml").write_text("name: fw_artifact")
        
        # Create project plugins directory with context bundles
        project_plugins_dir = project_root / ".agentqms" / "plugins"
        project_context_bundles_dir = project_plugins_dir / "context_bundles"
        project_context_bundles_dir.mkdir(parents=True)
        (project_context_bundles_dir / "proj_bundle.yaml").write_text("name: proj_bundle")
        
        discovery = PluginDiscovery(project_root=project_root, framework_root=framework_root)
        plugins = discovery.discover_all()
        
        assert len(plugins) == 2
        framework_plugin = next(p for p in plugins if p.source == "framework")
        project_plugin = next(p for p in plugins if p.source == "project")
        
        assert framework_plugin.plugin_type == "artifact_type"
        assert framework_plugin.path.name == "fw_artifact.yaml"
        assert project_plugin.plugin_type == "context_bundle"
        assert project_plugin.path.name == "proj_bundle.yaml"


def test_discover_by_type():
    """Test discovering plugins grouped by type."""
    with tempfile.TemporaryDirectory() as temp_dir:
        project_root = Path(temp_dir)
        framework_root = project_root / "AgentQMS"
        
        # Create framework plugins directory with artifact types and context bundles
        framework_plugins_dir = framework_root / "conventions" / "plugins"
        framework_artifact_types_dir = framework_plugins_dir / "artifact_types"
        framework_artifact_types_dir.mkdir(parents=True)
        (framework_artifact_types_dir / "artifact1.yaml").write_text("name: artifact1")
        
        framework_context_bundles_dir = framework_plugins_dir / "context_bundles"
        framework_context_bundles_dir.mkdir(parents=True)
        (framework_context_bundles_dir / "bundle1.yaml").write_text("name: bundle1")
        
        # Create project plugins directory with validators
        project_plugins_dir = project_root / ".agentqms" / "plugins"
        project_plugins_dir.mkdir(parents=True)
        (project_plugins_dir / "validators.yaml").write_text("prefixes: {}")
        
        discovery = PluginDiscovery(project_root=project_root, framework_root=framework_root)
        grouped = discovery.discover_by_type()
        
        assert len(grouped["artifact_type"]) == 1
        assert len(grouped["context_bundle"]) == 1
        assert len(grouped["validators"]) == 1
        assert grouped["artifact_type"][0].source == "framework"
        assert grouped["context_bundle"][0].source == "framework"
        assert grouped["validators"][0].source == "project"


def test_get_discovery_paths():
    """Test getting discovery paths."""
    with tempfile.TemporaryDirectory() as temp_dir:
        project_root = Path(temp_dir)
        framework_root = project_root / "AgentQMS"
        
        discovery = PluginDiscovery(project_root=project_root, framework_root=framework_root)
        paths = discovery.get_discovery_paths()
        
        assert "framework" in paths
        assert "project" in paths
        assert paths["framework"] == str(framework_root / "conventions" / "plugins")
        assert paths["project"] == str(project_root / ".agentqms" / "plugins")


def test_discovered_plugin_str():
    """Test string representation of DiscoveredPlugin."""
    plugin = DiscoveredPlugin(
        path=Path("/test/path.yaml"),
        plugin_type="artifact_type",
        source="framework"
    )
    
    assert str(plugin) == "artifact_type:path.yaml [framework]"