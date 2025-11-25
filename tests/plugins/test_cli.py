"""Unit tests for the Plugin CLI module."""
import tempfile
import sys
from pathlib import Path
from unittest.mock import patch, Mock
import argparse
import json
import yaml

from AgentQMS.agent_tools.core.plugins.cli import (
    create_parser,
    format_human_output,
    format_json_output,
    main
)
from AgentQMS.agent_tools.core.plugins.registry import PluginRegistry, PluginMetadata, PluginValidationError


def test_create_parser():
    """Test that CLI argument parser is created correctly."""
    parser = create_parser()
    
    # Test that required arguments exist
    args = parser.parse_args(['--list'])
    assert args.list is True
    
    args = parser.parse_args(['--validate'])
    assert args.validate is True
    
    args = parser.parse_args(['--artifact-types'])
    assert args.artifact_types is True
    
    args = parser.parse_args(['--json'])
    assert args.json is True
    
    args = parser.parse_args(['--show', 'test_plugin'])
    assert args.show == 'test_plugin'


def test_format_human_output_list():
    """Test human-readable output formatting."""
    registry = PluginRegistry(loaded_at="2023-01-01T00:00:00Z")
    registry.artifact_types = {
        "change_request": {
            "name": "change_request", 
            "version": "1.0",
            "description": "A request to change something"
        }
    }
    registry.context_bundles = {
        "dev_bundle": {
            "name": "dev_bundle",
            "title": "Development Bundle"
        }
    }
    registry.validators = {"prefixes": {"REQ": "requirements"}}
    
    args = argparse.Namespace(
        list=True,
        artifact_types=False,
        context_bundles=False,
        validators=False,
        show=None,
        validate=False,
        json=False
    )
    
    discovery_paths = {
        "framework": "/framework/path",
        "project": "/project/path"
    }
    
    output = format_human_output(registry, args, discovery_paths)
    
    assert "AGENTQMS PLUGIN REGISTRY" in output
    assert "change_request (v1.0)" in output
    assert "dev_bundle" in output
    assert "A request to change something" in output
    assert "Loaded at: 2023-01-01T00:00:00Z" in output


def test_format_human_output_with_validation_errors():
    """Test human output with validation errors."""
    registry = PluginRegistry()
    registry.validation_errors.append(PluginValidationError(
        plugin_path="/test/path",
        plugin_type="artifact_type",
        error_message="Test validation error"
    ))
    
    args = argparse.Namespace(
        list=True,
        artifact_types=False,
        context_bundles=False,
        validators=False,
        show=None,
        validate=True,  # Show validation results
        json=False
    )
    
    discovery_paths = {}
    
    output = format_human_output(registry, args, discovery_paths)
    
    assert "❌ /test/path" in output
    assert "Test validation error" in output


def test_format_human_output_show_specific_plugin():
    """Test showing a specific plugin."""
    registry = PluginRegistry()
    registry.artifact_types = {
        "test_artifact": {
            "name": "test_artifact",
            "description": "Test artifact description"
        }
    }
    
    args = argparse.Namespace(
        list=False,
        artifact_types=False,
        context_bundles=False,
        validators=False,
        show="test_artifact",
        validate=False,
        json=False
    )
    
    discovery_paths = {}
    
    output = format_human_output(registry, args, discovery_paths)
    
    assert "🔍 Plugin Details: test_artifact" in output
    assert "test_artifact" in output
    assert "Test artifact description" in output


def test_format_json_output_summary():
    """Test JSON output for summary."""
    registry = PluginRegistry()
    registry.artifact_types = {"type1": {"name": "type1"}}
    registry.context_bundles = {"bundle1": {"name": "bundle1"}}
    registry.validators = {"prefixes": {"REQ": "requirements"}}
    
    args = argparse.Namespace(
        artifact_types=False,
        context_bundles=False,
        validators=False,
        show=None,
        json=True
    )
    
    output = format_json_output(registry, args)
    parsed = json.loads(output)
    
    assert "artifact_types" in parsed
    assert parsed["artifact_types"] == ["type1"]
    assert parsed["context_bundles"] == ["bundle1"]
    assert parsed["validators"] is True


def test_format_json_output_specific_artifact_type():
    """Test JSON output for specific artifact type."""
    registry = PluginRegistry()
    registry.artifact_types = {
        "test_artifact": {
            "name": "test_artifact",
            "description": "Test description"
        }
    }
    
    args = argparse.Namespace(
        artifact_types=False,
        context_bundles=False,
        validators=False,
        show="test_artifact",
        json=True
    )
    
    output = format_json_output(registry, args)
    parsed = json.loads(output)
    
    assert parsed["name"] == "test_artifact"
    assert parsed["description"] == "Test description"


def test_format_json_output_nonexistent_plugin():
    """Test JSON output when plugin doesn't exist."""
    registry = PluginRegistry()
    
    args = argparse.Namespace(
        artifact_types=False,
        context_bundles=False,
        validators=False,
        show="nonexistent",
        json=True
    )
    
    output = format_json_output(registry, args)
    parsed = json.loads(output)
    
    assert parsed["error"] == "Plugin 'nonexistent' not found"


def test_main_with_argv():
    """Test main function with command line arguments."""
    with patch('AgentQMS.agent_tools.core.plugins.loader.PluginLoader.load') as mock_load, \
         patch('AgentQMS.agent_tools.utils.paths.get_project_root') as mock_get_project_root, \
         patch('builtins.print') as mock_print:
        
        mock_get_project_root.return_value = Path("/test")
        
        # Mock registry
        mock_registry = Mock()
        mock_registry.has_errors.return_value = False
        mock_registry.artifact_types = {}
        mock_registry.validators = {}
        mock_registry.context_bundles = {}
        mock_registry.validation_errors = []
        mock_registry.loaded_at = "2023-01-01T00:00:00Z"
        mock_load.return_value = mock_registry
        
        # Call main with --list argument
        result = main(['--list', '--project-root', '/test'])
        
        assert result == 0  # Exit code should be 0
        mock_load.assert_called_once()


def test_main_with_validation_errors():
    """Test main function when registry has validation errors."""
    with patch('AgentQMS.agent_tools.core.plugins.loader.PluginLoader.load') as mock_load, \
         patch('AgentQMS.agent_tools.utils.paths.get_project_root') as mock_get_project_root:

        mock_get_project_root.return_value = Path("/test")

        # Mock registry with validation errors
        mock_registry = Mock()
        mock_registry.has_errors.return_value = True  # Has errors
        mock_registry.artifact_types = {}
        mock_registry.validators = {}
        mock_registry.context_bundles = {}
        mock_registry.validation_errors = [PluginValidationError(
            plugin_path="/test/path",
            plugin_type="artifact_type",
            error_message="Test error"
        )]
        mock_registry.loaded_at = "2023-01-01T00:00:00Z"
        mock_load.return_value = mock_registry

        # Call main - should return exit code 1 due to errors
        result = main(['--validate'])

        assert result == 1  # Exit code should be 1 due to validation errors


def test_main_default_behavior():
    """Test main function default behavior (no arguments specified)."""
    with patch('AgentQMS.agent_tools.core.plugins.loader.PluginLoader.load') as mock_load, \
         patch('AgentQMS.agent_tools.utils.paths.get_project_root') as mock_get_project_root, \
         patch('builtins.print') as mock_print:
        
        mock_get_project_root.return_value = Path("/test")
        
        # Mock registry
        mock_registry = Mock()
        mock_registry.has_errors.return_value = False
        mock_registry.artifact_types = {}
        mock_registry.validators = {}
        mock_registry.context_bundles = {}
        mock_registry.validation_errors = []
        mock_registry.loaded_at = "2023-01-01T00:00:00Z"
        mock_load.return_value = mock_registry
        
        # Call main with no args - should default to --list
        result = main([])  # Empty argv
        
        assert result == 0  # Exit code should be 0
        mock_load.assert_called_once()