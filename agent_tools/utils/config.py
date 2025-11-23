"""Framework configuration loader for AgentQMS.

This module consolidates configuration data from the framework defaults,
framework-level configuration, project-level overrides, and environment
variables. The loader exposes helpers the rest of the toolchain can reuse,
ensuring every component resolves paths the same way.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
import json
from pathlib import Path
from typing import Any, Dict, Optional, Iterable
import os

import yaml



_DEFAULT_CONFIG: Dict[str, Any] = {}


class ConfigLoader:
    """Central configuration loader with caching."""

    def __init__(self) -> None:
        self._config_cache: Optional[Dict[str, Any]] = None
        self.framework_root = self._detect_framework_root()
        self.project_root = self._detect_project_root(self.framework_root)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def load(self, force: bool = False) -> Dict[str, Any]:
        """Load configuration following the precedence hierarchy."""
        if self._config_cache is not None and not force:
            return deepcopy(self._config_cache)

        config = deepcopy(_DEFAULT_CONFIG)
        config = self._merge_config(config, self._load_settings())
        config = self._merge_config(config, self._load_environment_overrides())
        self._write_runtime_snapshot(config)

        self._config_cache = config
        return deepcopy(config)

    def get_path(self, key: str) -> Path:
        """Return a project-relative path resolved from configuration."""
        config = self.load()
        value = config.get("paths", {}).get(key)
        if not value:
            raise KeyError(f"No path configured for '{key}'")

        candidate = Path(value)
        if candidate.is_absolute():
            return candidate
        return self.project_root / candidate

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _detect_framework_root(self) -> Path:
        """Detect framework root by looking for agent_tools directory."""
        current = Path(__file__).resolve()
        for parent in (current,) + tuple(current.parents):
            # Framework root contains agent_tools directory
            if (parent / "agent_tools").exists():
                return parent
        raise RuntimeError("Could not determine framework root. Is AgentQMS installed?")

    def _detect_project_root(self, framework_root: Path) -> Path:
        """Project root is the same as framework root when framework is at project root."""
        return framework_root

    def _load_settings(self) -> Dict[str, Any]:
        """Load configuration from .agentqms/settings/ directory.
        
        Single source of truth for all configuration. Framework ships with defaults,
        users can edit these files directly to customize behavior.
        """
        settings_dir = self.project_root / ".agentqms" / "settings"
        config: Dict[str, Any] = {}

        if not settings_dir.exists():
            return config

        # Load base configuration files
        yaml_files: Iterable[Path] = (
            settings_dir / "framework.yaml",
            settings_dir / "interface.yaml",
            settings_dir / "paths.yaml",
        )
        for path in yaml_files:
            config = self._merge_yaml_if_exists(config, path)

        # Load tool mappings if present
        tool_mappings = settings_dir / "tool_mappings.json"
        if tool_mappings.exists():
            with tool_mappings.open("r", encoding="utf-8") as handle:
                config["tool_mappings"] = json.load(handle)

        # Load environment-specific overrides (optional)
        config = self._merge_directory_overrides(config, settings_dir / "environments")
        
        # Load additional overrides (optional)
        config = self._merge_directory_overrides(config, settings_dir / "overrides")

        return config

    def _load_environment_overrides(self) -> Dict[str, Any]:
        overrides: Dict[str, Any] = {}

        artifacts = os.getenv("AGENTQMS_PATHS_ARTIFACTS")
        docs = os.getenv("AGENTQMS_PATHS_DOCS")
        strict_mode = os.getenv("AGENTQMS_VALIDATION_STRICT_MODE")

        if artifacts:
            overrides.setdefault("paths", {})["artifacts"] = artifacts
        if docs:
            overrides.setdefault("paths", {})["docs"] = docs
        if strict_mode is not None:
            overrides.setdefault("validation", {})["strict_mode"] = (
                strict_mode.lower() == "true"
            )
        return overrides

    def _load_yaml(self, path: Path) -> Dict[str, Any]:
        with path.open("r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle) or {}
        if not isinstance(data, dict):
            raise ValueError(f"Invalid configuration format: {path}")
        return data

    def _merge_yaml_if_exists(self, base: Dict[str, Any], path: Path) -> Dict[str, Any]:
        if not path.exists():
            return base
        return self._merge_config(base, self._load_yaml(path))

    def _merge_directory_overrides(self, base: Dict[str, Any], directory: Path) -> Dict[str, Any]:
        if not directory.exists():
            return base
        result = deepcopy(base)
        for path in sorted(directory.glob("*.yaml")):
            result = self._merge_yaml_if_exists(result, path)
        return result

    def _write_runtime_snapshot(self, config: Dict[str, Any]) -> None:
        runtime_dir = self.project_root / ".agentqms"
        runtime_dir.mkdir(parents=True, exist_ok=True)
        runtime_config = runtime_dir / "effective.yaml"

        payload = {
            "layers": {
                "settings": {
                    "framework": ".agentqms/settings/framework.yaml",
                    "interface": ".agentqms/settings/interface.yaml",
                    "paths": ".agentqms/settings/paths.yaml",
                    "tool_mappings": ".agentqms/settings/tool_mappings.json",
                    "environments": ".agentqms/settings/environments/",
                    "overrides": ".agentqms/settings/overrides/",
                },
                "note": "All configuration is in '.agentqms/settings/' directory. Framework ships with defaults, users can edit directly.",
            },
            "metadata": {
                "generated_at": datetime.utcnow().isoformat() + "Z",
                "generator": "AgentQMS ConfigLoader",
                "schema_version": "0.2",
            },
            "resolved": config,
        }

        with runtime_config.open("w", encoding="utf-8") as handle:
            yaml.safe_dump(payload, handle, sort_keys=False)

    def _merge_config(self, base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        result = deepcopy(base)
        for key, value in override.items():
            if (
                key in result
                and isinstance(result[key], dict)
                and isinstance(value, dict)
            ):
                result[key] = self._merge_config(result[key], value)
            else:
                result[key] = deepcopy(value)
        return result


_config_loader: Optional[ConfigLoader] = None


def get_config_loader() -> ConfigLoader:
    """Return a singleton configuration loader."""
    global _config_loader
    if _config_loader is None:
        _config_loader = ConfigLoader()
    return _config_loader


def load_config(force: bool = False) -> Dict[str, Any]:
    """Convenience helper for callers that only need the merged config."""
    return get_config_loader().load(force=force)
