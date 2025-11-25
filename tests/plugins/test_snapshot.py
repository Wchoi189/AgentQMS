"""Unit tests for the SnapshotWriter module."""
import tempfile
from pathlib import Path
from AgentQMS.agent_tools.core.plugins.snapshot import SnapshotWriter
from AgentQMS.agent_tools.core.plugins.registry import PluginRegistry, PluginMetadata, PluginValidationError


def test_snapshot_writer_initialization():
    """Test that SnapshotWriter initializes correctly."""
    with tempfile.TemporaryDirectory() as temp_dir:
        state_dir = Path(temp_dir)
        writer = SnapshotWriter(state_dir=state_dir)
        
        assert writer.state_dir == state_dir
        assert writer.snapshot_path == state_dir / "plugins.yaml"


def test_write_snapshot():
    """Test writing a snapshot to disk."""
    with tempfile.TemporaryDirectory() as temp_dir:
        state_dir = Path(temp_dir)
        writer = SnapshotWriter(state_dir=state_dir)
        
        # Create a test registry
        registry = PluginRegistry(loaded_at="2023-01-01T00:00:00Z")
        registry.artifact_types = {"type1": {"name": "type1"}}
        registry.validators = {"prefixes": {"REQ": "requirements"}}
        registry.context_bundles = {"bundle1": {"name": "bundle1", "title": "Bundle 1"}}
        registry.metadata.append(PluginMetadata(
            name="type1",
            version="1.0",
            source="framework",
            path="/test/path",
            plugin_type="artifact_type"
        ))
        registry.validation_errors.append(PluginValidationError(
            plugin_path="/test/path",
            plugin_type="artifact_type",
            error_message="Test error"
        ))
        
        discovery_paths = {
            "framework": "/framework/path",
            "project": "/project/path"
        }
        
        snapshot_path = writer.write(registry, discovery_paths)
        
        assert snapshot_path.exists()
        assert snapshot_path == state_dir / "plugins.yaml"
        
        # Read and verify content
        import yaml
        with snapshot_path.open("r") as f:
            content = yaml.safe_load(f)
        
        assert content["metadata"]["generated_at"] == "2023-01-01T00:00:00Z"
        assert content["metadata"]["generator"] == "AgentQMS PluginLoader"
        assert content["discovery_paths"] == discovery_paths
        assert content["plugins_loaded"]["artifact_types"] == ["type1"]
        assert content["plugins_loaded"]["validators"] is True
        assert content["plugins_loaded"]["context_bundles"] == ["bundle1"]
        assert len(content["plugin_metadata"]) == 1
        assert len(content["validation_errors"]) == 1
        assert content["resolved"]["artifact_types"]["type1"]["name"] == "type1"


def test_write_snapshot_creates_directory():
    """Test that SnapshotWriter creates the directory if it doesn't exist."""
    with tempfile.TemporaryDirectory() as temp_dir:
        state_dir = Path(temp_dir) / "subdir"
        writer = SnapshotWriter(state_dir=state_dir)
        
        registry = PluginRegistry()
        discovery_paths = {}
        
        snapshot_path = writer.write(registry, discovery_paths)
        
        assert state_dir.exists()
        assert snapshot_path.exists()


def test_read_snapshot_when_file_doesnt_exist():
    """Test reading a snapshot when the file doesn't exist."""
    with tempfile.TemporaryDirectory() as temp_dir:
        state_dir = Path(temp_dir)
        writer = SnapshotWriter(state_dir=state_dir)
        
        content = writer.read()
        assert content == {}


def test_read_snapshot_valid_file():
    """Test reading a valid snapshot file."""
    with tempfile.TemporaryDirectory() as temp_dir:
        state_dir = Path(temp_dir)
        writer = SnapshotWriter(state_dir=state_dir)
        
        # Create a snapshot first
        registry = PluginRegistry()
        registry.artifact_types = {"test": {"name": "test"}}
        discovery_paths = {"framework": "/fw", "project": "/proj"}
        
        writer.write(registry, discovery_paths)
        
        # Now read it back
        content = writer.read()
        assert content["plugins_loaded"]["artifact_types"] == ["test"]
        assert content["discovery_paths"] == discovery_paths


def test_read_snapshot_invalid_file():
    """Test reading a snapshot when the file contains invalid content."""
    with tempfile.TemporaryDirectory() as temp_dir:
        state_dir = Path(temp_dir)
        writer = SnapshotWriter(state_dir=state_dir)

        # Create an invalid snapshot file that will cause a YAML parsing error
        snapshot_path = state_dir / "plugins.yaml"
        snapshot_path.write_text("{invalid: yaml: content}")  # This will cause ParserError

        content = writer.read()
        # When YAML parsing fails, the exception should be caught and return empty dict
        assert content == {}