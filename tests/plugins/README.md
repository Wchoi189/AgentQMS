# AgentQMS Plugin Tests

This directory contains unit tests for the AgentQMS plugin system. The tests follow a modular design pattern to match the plugin system architecture.

## Test Structure

The tests are organized in a modular fashion that mirrors the plugin system itself:

- `test_registry.py` - Tests for the PluginRegistry data structure
- `test_discovery.py` - Tests for plugin file discovery logic
- `test_validation.py` - Tests for plugin schema validation
- `test_loader.py` - Tests for plugin loading and merging logic
- `test_snapshot.py` - Tests for runtime snapshot functionality
- `test_main.py` - Tests for main API functions and singletons
- `test_cli.py` - Tests for command-line interface

## Running Tests

To run all plugin tests:

```bash
uv run pytest tests/plugins/
```

To run specific test modules:

```bash
uv run pytest tests/plugins/test_registry.py
```

## Test Coverage

The test suite provides comprehensive coverage of:

- Core data structures and their methods
- File discovery and loading logic
- Schema validation functionality
- Plugin override and merge behavior
- Error handling and validation error reporting
- CLI functionality and output formatting
- Singleton management and caching behavior

## Dependencies

Tests require the following packages:
- pytest
- pyyaml
- jsonschema

These are installed when using the development dependencies specified in pyproject.toml.