"""Unit tests for the PluginRegistry module."""
import pytest
from AgentQMS.agent_tools.core.plugins.registry import (
    PluginRegistry,
    PluginMetadata,
    PluginValidationError
)


def test_plugin_registry_initialization():
    """Test that PluginRegistry initializes with correct defaults."""
    registry = PluginRegistry(loaded_at="2023-01-01T00:00:00Z")
    
    assert registry.artifact_types == {}
    assert registry.validators == {}
    assert registry.context_bundles == {}
    assert registry.metadata == []
    assert registry.validation_errors == []
    assert registry.loaded_at == "2023-01-01T00:00:00Z"


def test_add_artifact_type():
    """Test adding artifact types to the registry."""
    registry = PluginRegistry()
    metadata = PluginMetadata(
        name="test_artifact",
        version="1.0",
        source="framework",
        path="/test/path",
        plugin_type="artifact_type"
    )
    
    registry.add_artifact_type(
        name="test_artifact",
        data={"name": "test_artifact", "version": "1.0"},
        metadata=metadata
    )
    
    assert "test_artifact" in registry.artifact_types
    assert registry.artifact_types["test_artifact"]["name"] == "test_artifact"
    assert len(registry.metadata) == 1
    assert registry.metadata[0].name == "test_artifact"


def test_add_context_bundle():
    """Test adding context bundles to the registry."""
    registry = PluginRegistry()
    metadata = PluginMetadata(
        name="test_bundle",
        version="1.0",
        source="project",
        path="/test/path",
        plugin_type="context_bundle"
    )
    
    registry.add_context_bundle(
        name="test_bundle",
        data={"name": "test_bundle", "title": "Test Bundle"},
        metadata=metadata
    )
    
    assert "test_bundle" in registry.context_bundles
    assert registry.context_bundles["test_bundle"]["title"] == "Test Bundle"
    assert len(registry.metadata) == 1


def test_add_validation_error():
    """Test adding validation errors to the registry."""
    registry = PluginRegistry()
    error = PluginValidationError(
        plugin_path="/test/path",
        plugin_type="artifact_type",
        error_message="Test error"
    )
    
    registry.add_validation_error(error)
    
    assert len(registry.validation_errors) == 1
    assert registry.validation_errors[0].error_message == "Test error"


def test_get_artifact_types():
    """Test getting all artifact types."""
    registry = PluginRegistry()
    registry.artifact_types = {"type1": {"name": "type1"}, "type2": {"name": "type2"}}
    
    result = registry.get_artifact_types()
    assert result == {"type1": {"name": "type1"}, "type2": {"name": "type2"}}
    
    # Verify the returned data is a copy (not reference to internal data)
    result["type1"]["modified"] = True
    assert "modified" not in registry.artifact_types["type1"]


def test_get_artifact_type():
    """Test getting a specific artifact type."""
    registry = PluginRegistry()
    registry.artifact_types = {"type1": {"name": "type1", "version": "1.0"}}
    
    result = registry.get_artifact_type("type1")
    assert result == {"name": "type1", "version": "1.0"}
    
    assert registry.get_artifact_type("nonexistent") is None


def test_get_validators():
    """Test getting validators configuration."""
    registry = PluginRegistry()
    registry.validators = {
        "prefixes": {"REQ": "requirements"},
        "types": ["bug", "feature"]
    }
    
    result = registry.get_validators()
    assert result == {"prefixes": {"REQ": "requirements"}, "types": ["bug", "feature"]}
    
    # Verify the returned data is a copy
    result["prefixes"]["NEW"] = "new"
    assert "NEW" not in registry.validators["prefixes"]


def test_get_context_bundles():
    """Test getting context bundles."""
    registry = PluginRegistry()
    registry.context_bundles = {
        "bundle1": {"name": "bundle1", "title": "Bundle 1"},
        "bundle2": {"name": "bundle2", "title": "Bundle 2"}
    }
    
    result = registry.get_context_bundles()
    assert len(result) == 2
    assert result["bundle1"]["title"] == "Bundle 1"


def test_get_context_bundle():
    """Test getting a specific context bundle."""
    registry = PluginRegistry()
    registry.context_bundles = {
        "bundle1": {"name": "bundle1", "title": "Bundle 1"}
    }
    
    result = registry.get_context_bundle("bundle1")
    assert result["title"] == "Bundle 1"
    
    assert registry.get_context_bundle("nonexistent") is None


def test_has_errors():
    """Test checking for validation errors."""
    registry = PluginRegistry()
    
    assert registry.has_errors() is False
    
    registry.add_validation_error(PluginValidationError(
        plugin_path="/test",
        plugin_type="artifact_type",
        error_message="Test error"
    ))
    
    assert registry.has_errors() is True


def test_get_plugin_names():
    """Test getting plugin names by type."""
    registry = PluginRegistry()
    registry.artifact_types = {"type1": {}, "type2": {}}
    registry.context_bundles = {"bundle1": {}}
    registry.validators = {"prefixes": {"REQ": "req"}}
    
    assert set(registry.get_plugin_names("artifact_type")) == {"type1", "type2"}
    assert registry.get_plugin_names("context_bundle") == ["bundle1"]
    assert registry.get_plugin_names("validator") == ["validators"]
    assert registry.get_plugin_names("unknown_type") == []


def test_get_metadata_for_plugin():
    """Test getting metadata for a specific plugin."""
    registry = PluginRegistry()
    metadata = PluginMetadata(
        name="test_type",
        version="1.0",
        source="framework",
        path="/test/path",
        plugin_type="artifact_type"
    )
    registry.metadata = [metadata]
    
    result = registry.get_metadata_for_plugin("test_type", "artifact_type")
    assert result is not None
    assert result.name == "test_type"
    
    assert registry.get_metadata_for_plugin("nonexistent", "artifact_type") is None


def test_to_summary_dict():
    """Test creating a summary dictionary."""
    registry = PluginRegistry()
    registry.artifact_types = {"type1": {}}
    registry.context_bundles = {"bundle1": {}}
    registry.validators = {"prefixes": {"REQ": "req"}}
    registry.validation_errors = [
        PluginValidationError(
            plugin_path="/test",
            plugin_type="artifact_type",
            error_message="Test error"
        )
    ]
    
    summary = registry.to_summary_dict()
    assert summary["artifact_types"] == ["type1"]
    assert summary["context_bundles"] == ["bundle1"]
    assert summary["validators"] is True
    assert summary["errors"] == 1