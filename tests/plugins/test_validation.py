"""Unit tests for the PluginValidator module."""
import tempfile
from pathlib import Path
from AgentQMS.agent_tools.core.plugins.validation import PluginValidator, SchemaValidationError


def test_plugin_validator_initialization():
    """Test that PluginValidator initializes correctly."""
    with tempfile.TemporaryDirectory() as temp_dir:
        schemas_dir = Path(temp_dir)
        
        validator = PluginValidator(schemas_dir=schemas_dir)
        assert validator.schemas_dir == schemas_dir
        assert validator._schema_cache == {}


def test_plugin_validator_without_schemas_dir():
    """Test that PluginValidator is disabled without schemas_dir."""
    validator = PluginValidator(schemas_dir=None)
    assert validator.is_available is False


def test_validate_unknown_plugin_type():
    """Test validation with unknown plugin type."""
    with tempfile.TemporaryDirectory() as temp_dir:
        schemas_dir = Path(temp_dir)
        # Create a schema file for artifact_type to make validation available
        schema_file = schemas_dir / "plugin_artifact_type.json"
        schema_file.write_text('{"type": "object"}')
        
        validator = PluginValidator(schemas_dir=schemas_dir)
        errors = validator.validate({"name": "test"}, "unknown_type")
        
        assert len(errors) == 1
        assert "Unknown plugin type: unknown_type" in errors[0]


def test_validate_schema_not_found():
    """Test validation when schema file doesn't exist."""
    with tempfile.TemporaryDirectory() as temp_dir:
        schemas_dir = Path(temp_dir)
        
        validator = PluginValidator(schemas_dir=schemas_dir)
        errors = validator.validate({"name": "test"}, "artifact_type")
        
        assert len(errors) == 1
        assert "Schema not found for plugin type: artifact_type" in errors[0]


def test_validate_invalid_schema_content():
    """Test validation when schema file contains invalid JSON."""
    with tempfile.TemporaryDirectory() as temp_dir:
        schemas_dir = Path(temp_dir)
        schema_file = schemas_dir / "plugin_artifact_type.json"
        schema_file.write_text("invalid json {")  # Invalid JSON will cause load to fail

        validator = PluginValidator(schemas_dir=schemas_dir)
        errors = validator.validate({"name": "test"}, "artifact_type")

        # Schema not found because JSON is invalid will result in the error about schema not found
        assert len(errors) == 1
        assert "Schema not found for plugin type: artifact_type" in errors[0]


def test_validate_valid_plugin_data():
    """Test validation with valid plugin data."""
    with tempfile.TemporaryDirectory() as temp_dir:
        schemas_dir = Path(temp_dir)
        schema_file = schemas_dir / "plugin_artifact_type.json"
        # Simple schema that requires an 'name' property
        schema_content = '''
{
  "type": "object",
  "properties": {
    "name": {"type": "string"}
  },
  "required": ["name"]
}
'''
        schema_file.write_text(schema_content)
        
        validator = PluginValidator(schemas_dir=schemas_dir)
        errors = validator.validate({"name": "test"}, "artifact_type")
        
        assert errors == []  # Should be valid


def test_validate_invalid_plugin_data():
    """Test validation with invalid plugin data."""
    with tempfile.TemporaryDirectory() as temp_dir:
        schemas_dir = Path(temp_dir)
        schema_file = schemas_dir / "plugin_artifact_type.json"
        # Simple schema that requires an 'name' property
        schema_content = '''
{
  "type": "object",
  "properties": {
    "name": {"type": "string"}
  },
  "required": ["name"]
}
'''
        schema_file.write_text(schema_content)
        
        validator = PluginValidator(schemas_dir=schemas_dir)
        errors = validator.validate({"other": "test"}, "artifact_type")
        
        assert len(errors) == 1
        assert "'name' is a required property" in errors[0]


def test_validate_or_raise_valid():
    """Test validate_or_raise with valid data."""
    with tempfile.TemporaryDirectory() as temp_dir:
        schemas_dir = Path(temp_dir)
        schema_file = schemas_dir / "plugin_artifact_type.json"
        schema_content = '''
{
  "type": "object",
  "properties": {
    "name": {"type": "string"}
  },
  "required": ["name"]
}
'''
        schema_file.write_text(schema_content)
        
        validator = PluginValidator(schemas_dir=schemas_dir)
        
        # Should not raise an exception
        validator.validate_or_raise({"name": "test"}, "artifact_type")


def test_validate_or_raise_invalid():
    """Test validate_or_raise with invalid data."""
    with tempfile.TemporaryDirectory() as temp_dir:
        schemas_dir = Path(temp_dir)
        schema_file = schemas_dir / "plugin_artifact_type.json"
        schema_content = '''
{
  "type": "object",
  "properties": {
    "name": {"type": "string"}
  },
  "required": ["name"]
}
'''
        schema_file.write_text(schema_content)
        
        validator = PluginValidator(schemas_dir=schemas_dir)
        
        try:
            validator.validate_or_raise({"other": "test"}, "artifact_type")
            assert False, "Should have raised SchemaValidationError"
        except SchemaValidationError:
            pass  # Expected


def test_get_schema():
    """Test getting schema directly."""
    with tempfile.TemporaryDirectory() as temp_dir:
        schemas_dir = Path(temp_dir)
        schema_file = schemas_dir / "plugin_artifact_type.json"
        schema_content = '{"type": "object", "properties": {"name": {"type": "string"}}}'
        schema_file.write_text(schema_content)
        
        validator = PluginValidator(schemas_dir=schemas_dir)
        schema = validator.get_schema("artifact_type")
        
        assert schema == {
            "type": "object",
            "properties": {"name": {"type": "string"}}
        }


def test_get_schema_path():
    """Test getting schema path."""
    with tempfile.TemporaryDirectory() as temp_dir:
        schemas_dir = Path(temp_dir)
        schema_file = schemas_dir / "plugin_artifact_type.json"
        schema_file.write_text('{"type": "object"}')
        
        validator = PluginValidator(schemas_dir=schemas_dir)
        path = validator.get_schema_path("artifact_type")
        
        assert path == schema_file


def test_get_schema_path_nonexistent():
    """Test getting schema path when file doesn't exist."""
    with tempfile.TemporaryDirectory() as temp_dir:
        schemas_dir = Path(temp_dir)
        
        validator = PluginValidator(schemas_dir=schemas_dir)
        path = validator.get_schema_path("artifact_type")
        
        assert path is None


def test_schema_validation_disabled():
    """Test that validation returns empty list when not available."""
    validator = PluginValidator(schemas_dir=None)
    errors = validator.validate({"name": "test"}, "artifact_type")
    
    assert errors == []


def test_schema_caching():
    """Test that schemas are cached after first load."""
    with tempfile.TemporaryDirectory() as temp_dir:
        schemas_dir = Path(temp_dir)
        schema_file = schemas_dir / "plugin_artifact_type.json"
        schema_content = '{"type": "object", "properties": {"name": {"type": "string"}}}'
        schema_file.write_text(schema_content)
        
        validator = PluginValidator(schemas_dir=schemas_dir)
        
        # Load schema first time
        schema1 = validator.get_schema("artifact_type")
        # Load again - this should come from cache
        schema2 = validator.get_schema("artifact_type")
        
        assert schema1 == schema2