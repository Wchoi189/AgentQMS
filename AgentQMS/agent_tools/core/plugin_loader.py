#!/usr/bin/env python3
"""
Plugin Loader for AgentQMS

Discovers, validates, and merges plugins from framework and project sources.
Provides a unified registry for artifact types, validators, and context bundles.

This is the canonical implementation in agent_tools.

Usage:
    from AgentQMS.agent_tools.core.plugin_loader import PluginLoader, get_plugin_registry

    # Get singleton registry
    registry = get_plugin_registry()

    # Access plugin data
    artifact_types = registry.get_artifact_types()
    validators = registry.get_validators()
    context_bundles = registry.get_context_bundles()
"""

from __future__ import annotations

import json
import sys
from copy import deepcopy
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML not installed. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

try:
    import jsonschema
    from jsonschema import ValidationError, validate
except ImportError:
    jsonschema = None  # type: ignore
    ValidationError = Exception  # type: ignore
    validate = None  # type: ignore

from AgentQMS.agent_tools.utils.paths import get_project_root
from AgentQMS.agent_tools.utils.runtime import ensure_project_root_on_sys_path

ensure_project_root_on_sys_path()


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------


@dataclass
class PluginValidationError:
    """Represents a plugin validation error."""

    plugin_path: str
    plugin_type: str
    error_message: str
    schema_path: Optional[str] = None


@dataclass
class PluginMetadata:
    """Metadata about a loaded plugin."""

    name: str
    version: str
    source: str  # 'framework' or 'project'
    path: str
    plugin_type: str  # 'artifact_type', 'validator', 'context_bundle'
    scope: str = "project"
    description: str = ""


@dataclass
class PluginRegistry:
    """
    Central registry holding all discovered and validated plugins.

    Provides access to merged plugin configurations for:
    - Artifact types
    - Validators
    - Context bundles
    """

    artifact_types: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    validators: Dict[str, Any] = field(default_factory=dict)
    context_bundles: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    metadata: List[PluginMetadata] = field(default_factory=list)
    validation_errors: List[PluginValidationError] = field(default_factory=list)
    loaded_at: Optional[str] = None

    def get_artifact_types(self) -> Dict[str, Dict[str, Any]]:
        """Get all registered artifact types."""
        return deepcopy(self.artifact_types)

    def get_artifact_type(self, name: str) -> Optional[Dict[str, Any]]:
        """Get a specific artifact type by name."""
        return deepcopy(self.artifact_types.get(name))

    def get_validators(self) -> Dict[str, Any]:
        """Get merged validator configuration."""
        return deepcopy(self.validators)

    def get_context_bundles(self) -> Dict[str, Dict[str, Any]]:
        """Get all registered context bundles."""
        return deepcopy(self.context_bundles)

    def get_context_bundle(self, name: str) -> Optional[Dict[str, Any]]:
        """Get a specific context bundle by name."""
        return deepcopy(self.context_bundles.get(name))

    def has_errors(self) -> bool:
        """Check if any validation errors occurred during loading."""
        return len(self.validation_errors) > 0

    def get_plugin_names(self, plugin_type: str) -> List[str]:
        """Get names of all plugins of a given type."""
        if plugin_type == "artifact_type":
            return list(self.artifact_types.keys())
        elif plugin_type == "context_bundle":
            return list(self.context_bundles.keys())
        elif plugin_type == "validator":
            return ["validators"] if self.validators else []
        return []


# ---------------------------------------------------------------------------
# Plugin Loader
# ---------------------------------------------------------------------------


class PluginLoader:
    """
    Loads and merges plugins from framework and project sources.

    Discovery paths:
    1. Framework plugins: AgentQMS/conventions/plugins/ (builtin)
    2. Project plugins: .agentqms/plugins/ (project-specific)

    Plugins are validated against JSON schemas before being added to registry.
    """

    def __init__(self, project_root: Optional[Path] = None):
        """
        Initialize the plugin loader.

        Args:
            project_root: Project root directory. If None, auto-detected.
        """
        self.project_root = project_root or get_project_root()
        self.framework_root = self.project_root / "AgentQMS"

        # Plugin discovery paths
        self.framework_plugins_dir = self.framework_root / "conventions" / "plugins"
        self.project_plugins_dir = self.project_root / ".agentqms" / "plugins"

        # Schema paths
        self.schemas_dir = self.framework_root / "conventions" / "schemas"

        # Cached registry
        self._registry: Optional[PluginRegistry] = None

    # -----------------------------------------------------------------------
    # Public API
    # -----------------------------------------------------------------------

    def load(self, force: bool = False) -> PluginRegistry:
        """
        Load and merge all plugins into a registry.

        Args:
            force: If True, reload even if already cached.

        Returns:
            PluginRegistry containing all discovered plugins.
        """
        if self._registry is not None and not force:
            return self._registry

        registry = PluginRegistry(loaded_at=datetime.now(timezone.utc).isoformat())

        # Load artifact types
        self._load_artifact_types(registry)

        # Load validators
        self._load_validators(registry)

        # Load context bundles
        self._load_context_bundles(registry)

        # Write runtime snapshot
        self._write_runtime_snapshot(registry)

        self._registry = registry
        return registry

    def validate_plugin(
        self, plugin_data: Dict[str, Any], plugin_type: str
    ) -> List[str]:
        """
        Validate plugin data against its schema.

        Args:
            plugin_data: Plugin configuration dictionary.
            plugin_type: Type of plugin ('artifact_type', 'validators', 'context_bundle').

        Returns:
            List of validation error messages (empty if valid).
        """
        if jsonschema is None or validate is None:
            # jsonschema not installed, skip validation
            return []

        schema_map = {
            "artifact_type": "plugin_artifact_type.json",
            "validators": "plugin_validators.json",
            "context_bundle": "plugin_context_bundle.json",
        }

        schema_file = schema_map.get(plugin_type)
        if not schema_file:
            return [f"Unknown plugin type: {plugin_type}"]

        schema_path = self.schemas_dir / schema_file
        if not schema_path.exists():
            return [f"Schema not found: {schema_path}"]

        try:
            with schema_path.open("r", encoding="utf-8") as f:
                schema = json.load(f)

            validate(instance=plugin_data, schema=schema)
            return []

        except ValidationError as e:
            return [f"{e.message} (path: {list(e.path)})"]
        except json.JSONDecodeError as e:
            return [f"Invalid schema JSON: {e}"]
        except Exception as e:
            return [f"Validation error: {e}"]

    def discover_plugins(self) -> Dict[str, List[Path]]:
        """
        Discover all plugin files from registered sources.

        Returns:
            Dictionary mapping plugin types to lists of plugin file paths.
        """
        discovered: Dict[str, List[Path]] = {
            "artifact_type": [],
            "validators": [],
            "context_bundle": [],
        }

        # Framework plugins (if directory exists)
        if self.framework_plugins_dir.exists():
            discovered = self._discover_from_directory(
                self.framework_plugins_dir, discovered
            )

        # Project plugins (if directory exists)
        if self.project_plugins_dir.exists():
            discovered = self._discover_from_directory(
                self.project_plugins_dir, discovered
            )

        return discovered

    # -----------------------------------------------------------------------
    # Private: Discovery
    # -----------------------------------------------------------------------

    def _discover_from_directory(
        self, base_dir: Path, discovered: Dict[str, List[Path]]
    ) -> Dict[str, List[Path]]:
        """Discover plugins from a base directory."""

        # Artifact types: base_dir/artifact_types/*.yaml
        artifact_types_dir = base_dir / "artifact_types"
        if artifact_types_dir.exists():
            for yaml_file in artifact_types_dir.glob("*.yaml"):
                discovered["artifact_type"].append(yaml_file)

        # Validators: base_dir/validators.yaml
        validators_file = base_dir / "validators.yaml"
        if validators_file.exists():
            discovered["validators"].append(validators_file)

        # Context bundles: base_dir/context_bundles/*.yaml
        context_bundles_dir = base_dir / "context_bundles"
        if context_bundles_dir.exists():
            for yaml_file in context_bundles_dir.glob("*.yaml"):
                discovered["context_bundle"].append(yaml_file)

        return discovered

    def _determine_source(self, plugin_path: Path) -> str:
        """Determine if a plugin is from 'framework' or 'project'."""
        try:
            plugin_path.relative_to(self.framework_plugins_dir)
            return "framework"
        except ValueError:
            return "project"

    # -----------------------------------------------------------------------
    # Private: Loading
    # -----------------------------------------------------------------------

    def _load_yaml(self, path: Path) -> Dict[str, Any]:
        """Load YAML file and return dictionary."""
        with path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        if not isinstance(data, dict):
            raise ValueError(f"Invalid YAML format (expected dict): {path}")
        return data

    def _load_artifact_types(self, registry: PluginRegistry) -> None:
        """Load and merge artifact type plugins."""
        discovered = self.discover_plugins()

        for plugin_path in discovered["artifact_type"]:
            try:
                plugin_data = self._load_yaml(plugin_path)
                source = self._determine_source(plugin_path)

                # Validate
                errors = self.validate_plugin(plugin_data, "artifact_type")
                if errors:
                    for error in errors:
                        registry.validation_errors.append(
                            PluginValidationError(
                                plugin_path=str(plugin_path),
                                plugin_type="artifact_type",
                                error_message=error,
                                schema_path=str(
                                    self.schemas_dir / "plugin_artifact_type.json"
                                ),
                            )
                        )
                    continue

                # Extract name and add to registry
                name = plugin_data.get("name", plugin_path.stem)

                # Check for conflicts (project overrides framework)
                if name in registry.artifact_types:
                    existing_source = next(
                        (
                            m.source
                            for m in registry.metadata
                            if m.name == name and m.plugin_type == "artifact_type"
                        ),
                        None,
                    )
                    # Only override if project overriding framework
                    if source == "project" and existing_source == "framework":
                        pass  # Allow override
                    elif source == existing_source:
                        # Same source, later file wins (alphabetical order)
                        pass
                    else:
                        # Framework trying to override project - skip
                        continue

                registry.artifact_types[name] = plugin_data
                registry.metadata.append(
                    PluginMetadata(
                        name=name,
                        version=plugin_data.get("version", "1.0"),
                        source=source,
                        path=str(plugin_path),
                        plugin_type="artifact_type",
                        scope=plugin_data.get("scope", "project"),
                        description=plugin_data.get("description", ""),
                    )
                )

            except Exception as e:
                registry.validation_errors.append(
                    PluginValidationError(
                        plugin_path=str(plugin_path),
                        plugin_type="artifact_type",
                        error_message=str(e),
                    )
                )

    def _load_validators(self, registry: PluginRegistry) -> None:
        """Load and merge validator plugins."""
        discovered = self.discover_plugins()

        merged_validators: Dict[str, Any] = {
            "prefixes": {},
            "types": [],
            "categories": [],
            "statuses": [],
            "rules": {},
            "custom_validators": [],
            "disabled_validators": [],
        }

        for plugin_path in discovered["validators"]:
            try:
                plugin_data = self._load_yaml(plugin_path)
                source = self._determine_source(plugin_path)

                # Validate
                errors = self.validate_plugin(plugin_data, "validators")
                if errors:
                    for error in errors:
                        registry.validation_errors.append(
                            PluginValidationError(
                                plugin_path=str(plugin_path),
                                plugin_type="validators",
                                error_message=error,
                                schema_path=str(
                                    self.schemas_dir / "plugin_validators.json"
                                ),
                            )
                        )
                    continue

                # Merge validators
                self._merge_validators(merged_validators, plugin_data)

                registry.metadata.append(
                    PluginMetadata(
                        name="validators",
                        version=plugin_data.get("version", "1.0"),
                        source=source,
                        path=str(plugin_path),
                        plugin_type="validator",
                        description=plugin_data.get("description", ""),
                    )
                )

            except Exception as e:
                registry.validation_errors.append(
                    PluginValidationError(
                        plugin_path=str(plugin_path),
                        plugin_type="validators",
                        error_message=str(e),
                    )
                )

        # Only add to registry if we have data
        if any(
            merged_validators[k]
            for k in ["prefixes", "types", "categories", "statuses"]
        ):
            registry.validators = merged_validators

    def _merge_validators(
        self, base: Dict[str, Any], override: Dict[str, Any]
    ) -> None:
        """Merge validator configurations (mutates base)."""
        # Merge prefixes (override wins)
        if "prefixes" in override:
            base["prefixes"].update(override["prefixes"])

        # Merge lists (unique values only)
        for key in ["types", "categories", "statuses"]:
            if key in override:
                existing = set(base.get(key, []))
                existing.update(override.get(key, []))
                base[key] = sorted(existing)

        # Merge rules (override wins)
        if "rules" in override:
            base.setdefault("rules", {}).update(override["rules"])

        # Append custom validators
        if "custom_validators" in override:
            base.setdefault("custom_validators", []).extend(
                override["custom_validators"]
            )

        # Append disabled validators
        if "disabled_validators" in override:
            existing = set(base.get("disabled_validators", []))
            existing.update(override.get("disabled_validators", []))
            base["disabled_validators"] = sorted(existing)

    def _load_context_bundles(self, registry: PluginRegistry) -> None:
        """Load and merge context bundle plugins."""
        discovered = self.discover_plugins()

        for plugin_path in discovered["context_bundle"]:
            try:
                plugin_data = self._load_yaml(plugin_path)
                source = self._determine_source(plugin_path)

                # Validate
                errors = self.validate_plugin(plugin_data, "context_bundle")
                if errors:
                    for error in errors:
                        registry.validation_errors.append(
                            PluginValidationError(
                                plugin_path=str(plugin_path),
                                plugin_type="context_bundle",
                                error_message=error,
                                schema_path=str(
                                    self.schemas_dir / "plugin_context_bundle.json"
                                ),
                            )
                        )
                    continue

                # Extract name and add to registry
                name = plugin_data.get("name", plugin_path.stem)

                # Check for conflicts (project overrides framework)
                if name in registry.context_bundles:
                    existing_source = next(
                        (
                            m.source
                            for m in registry.metadata
                            if m.name == name and m.plugin_type == "context_bundle"
                        ),
                        None,
                    )
                    if source == "project" and existing_source == "framework":
                        pass  # Allow override
                    elif source == existing_source:
                        pass  # Later file wins
                    else:
                        continue

                registry.context_bundles[name] = plugin_data
                registry.metadata.append(
                    PluginMetadata(
                        name=name,
                        version=plugin_data.get("version", "1.0"),
                        source=source,
                        path=str(plugin_path),
                        plugin_type="context_bundle",
                        scope=plugin_data.get("scope", "project"),
                        description=plugin_data.get("description", ""),
                    )
                )

            except Exception as e:
                registry.validation_errors.append(
                    PluginValidationError(
                        plugin_path=str(plugin_path),
                        plugin_type="context_bundle",
                        error_message=str(e),
                    )
                )

    # -----------------------------------------------------------------------
    # Private: Runtime Snapshot
    # -----------------------------------------------------------------------

    def _write_runtime_snapshot(self, registry: PluginRegistry) -> Path:
        """
        Write merged plugin state to .agentqms/state/plugins.yaml.

        Returns:
            Path to the written snapshot file.
        """
        state_dir = self.project_root / ".agentqms" / "state"
        state_dir.mkdir(parents=True, exist_ok=True)

        snapshot_path = state_dir / "plugins.yaml"

        # Build snapshot data
        snapshot = {
            "metadata": {
                "generated_at": registry.loaded_at,
                "generator": "AgentQMS PluginLoader",
                "schema_version": "1.0",
            },
            "discovery_paths": {
                "framework": str(self.framework_plugins_dir),
                "project": str(self.project_plugins_dir),
            },
            "plugins_loaded": {
                "artifact_types": list(registry.artifact_types.keys()),
                "validators": bool(registry.validators),
                "context_bundles": list(registry.context_bundles.keys()),
            },
            "plugin_metadata": [
                {
                    "name": m.name,
                    "type": m.plugin_type,
                    "version": m.version,
                    "source": m.source,
                    "path": m.path,
                }
                for m in registry.metadata
            ],
            "validation_errors": [
                {
                    "path": e.plugin_path,
                    "type": e.plugin_type,
                    "error": e.error_message,
                }
                for e in registry.validation_errors
            ],
            "resolved": {
                "artifact_types": registry.artifact_types,
                "validators": registry.validators,
                "context_bundles": registry.context_bundles,
            },
        }

        with snapshot_path.open("w", encoding="utf-8") as f:
            yaml.safe_dump(snapshot, f, sort_keys=False, default_flow_style=False)

        return snapshot_path


# ---------------------------------------------------------------------------
# Singleton Access
# ---------------------------------------------------------------------------

_plugin_loader: Optional[PluginLoader] = None


def get_plugin_loader() -> PluginLoader:
    """Return a singleton plugin loader instance."""
    global _plugin_loader
    if _plugin_loader is None:
        _plugin_loader = PluginLoader()
    return _plugin_loader


def get_plugin_registry(force: bool = False) -> PluginRegistry:
    """
    Get the plugin registry (convenience function).

    Args:
        force: If True, reload plugins from disk.

    Returns:
        PluginRegistry containing all discovered plugins.
    """
    return get_plugin_loader().load(force=force)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> int:
    """Main entry point for CLI usage."""
    import argparse

    parser = argparse.ArgumentParser(description="AgentQMS Plugin Loader")
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all discovered plugins",
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Validate all plugins and show errors",
    )
    parser.add_argument(
        "--artifact-types",
        action="store_true",
        help="List artifact type plugins",
    )
    parser.add_argument(
        "--context-bundles",
        action="store_true",
        help="List context bundle plugins",
    )
    parser.add_argument(
        "--show",
        type=str,
        metavar="NAME",
        help="Show details for a specific plugin",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output in JSON format",
    )

    args = parser.parse_args()

    loader = PluginLoader()
    registry = loader.load()

    if args.json:
        # JSON output mode
        output: Dict[str, Any] = {}

        if args.artifact_types:
            output["artifact_types"] = registry.artifact_types
        elif args.context_bundles:
            output["context_bundles"] = registry.context_bundles
        elif args.show:
            if args.show in registry.artifact_types:
                output = registry.artifact_types[args.show]
            elif args.show in registry.context_bundles:
                output = registry.context_bundles[args.show]
            else:
                output = {"error": f"Plugin '{args.show}' not found"}
        else:
            output = {
                "artifact_types": list(registry.artifact_types.keys()),
                "context_bundles": list(registry.context_bundles.keys()),
                "validators": bool(registry.validators),
                "errors": len(registry.validation_errors),
            }

        print(json.dumps(output, indent=2))
        return 0

    # Human-readable output
    print("=" * 60)
    print("AGENTQMS PLUGIN REGISTRY")
    print("=" * 60)

    if args.validate or registry.has_errors():
        print("\n📋 Validation Results:")
        if registry.validation_errors:
            for error in registry.validation_errors:
                print(f"   ❌ {error.plugin_path}")
                print(f"      Type: {error.plugin_type}")
                print(f"      Error: {error.error_message}")
        else:
            print("   ✅ All plugins validated successfully")

    if args.list or args.artifact_types:
        print("\n📦 Artifact Types:")
        if registry.artifact_types:
            for name, data in registry.artifact_types.items():
                source = next(
                    (
                        m.source
                        for m in registry.metadata
                        if m.name == name and m.plugin_type == "artifact_type"
                    ),
                    "unknown",
                )
                print(f"   • {name} (v{data.get('version', '?')}) [{source}]")
                if data.get("description"):
                    desc = data["description"].split("\n")[0][:60]
                    print(f"     {desc}...")
        else:
            print("   (none)")

    if args.list or args.context_bundles:
        print("\n📚 Context Bundles:")
        if registry.context_bundles:
            for name, data in registry.context_bundles.items():
                source = next(
                    (
                        m.source
                        for m in registry.metadata
                        if m.name == name and m.plugin_type == "context_bundle"
                    ),
                    "unknown",
                )
                print(f"   • {name} [{source}]")
                if data.get("title"):
                    print(f"     {data['title']}")
        else:
            print("   (none)")

    if args.list:
        print("\n⚙️  Validators:")
        if registry.validators:
            v = registry.validators
            print(f"   Prefixes: {len(v.get('prefixes', {}))}")
            print(f"   Types: {len(v.get('types', []))}")
            print(f"   Categories: {len(v.get('categories', []))}")
            print(f"   Custom validators: {len(v.get('custom_validators', []))}")
        else:
            print("   (no extensions)")

    if args.show:
        print(f"\n🔍 Plugin Details: {args.show}")
        if args.show in registry.artifact_types:
            print(yaml.dump(registry.artifact_types[args.show], default_flow_style=False))
        elif args.show in registry.context_bundles:
            print(yaml.dump(registry.context_bundles[args.show], default_flow_style=False))
        else:
            print(f"   Plugin '{args.show}' not found")

    print("\n" + "=" * 60)
    print(f"Loaded at: {registry.loaded_at}")
    print("=" * 60)

    return 0 if not registry.has_errors() else 1


if __name__ == "__main__":
    sys.exit(main())

