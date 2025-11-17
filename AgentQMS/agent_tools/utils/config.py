"""Framework configuration loader for AgentQMS.

This module consolidates configuration data from the framework defaults,
framework-level configuration, project-level overrides, and environment
variables. The loader exposes helpers the rest of the toolchain can reuse,
ensuring every component resolves paths the same way.
"""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Dict, Optional
import os

import yaml


_DEFAULT_CONFIG: Dict[str, Any] = {
    "framework": {
        "name": "AgentQMS",
        "version": "0.2.0",
        "container_name": "AgentQMS",
    },
    "paths": {
        "artifacts": "artifacts",
        "docs": "docs",
    },
    "validation": {
        "enabled": True,
        "strict_mode": False,
    },
}


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
        config = self._merge_config(config, self._load_framework_config())
        config = self._merge_config(config, self._load_project_config())
        config = self._merge_config(config, self._load_environment_overrides())

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
        current = Path(__file__).resolve()
        for parent in (current,) + tuple(current.parents):
            if parent.name == "AgentQMS":
                return parent

        # Fallback: scattered layout (pre-containerization)
        for parent in (current,) + tuple(current.parents):
            if (parent / "agent_tools").exists() and (parent / "agent").exists():
                return parent
        raise RuntimeError("Could not determine framework root. Is AgentQMS installed?")

    def _detect_project_root(self, framework_root: Path) -> Path:
        if framework_root.name == "AgentQMS":
            return framework_root.parent
        return framework_root

    def _load_framework_config(self) -> Dict[str, Any]:
        framework_config = self.framework_root / "config" / "framework.yaml"
        if not framework_config.exists():
            return {}
        return self._load_yaml(framework_config)

    def _load_project_config(self) -> Dict[str, Any]:
        project_config = self.project_root / ".agentqms" / "config.yaml"
        if not project_config.exists():
            return {}
        return self._load_yaml(project_config)

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
