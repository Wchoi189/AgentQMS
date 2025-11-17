# Configuration Schema Design

**Date**: 2025-11-09  
**Design Scope**: Framework Configuration System  
**Status**: Design Proposal

## Executive Summary

This document defines the configuration schema for the containerized framework, enabling configurable output paths, framework-to-project mapping, and custom directory structures while maintaining sensible defaults.

---

## Configuration Architecture

### Configuration Hierarchy

```
1. Framework Defaults (hardcoded in code)
   ↓
2. Framework Config (AgentQMS/config/framework.yaml)
   ↓
3. Project Config (.agentqms/config.yaml)
   ↓
4. Environment Variables (override)
   ↓
5. Command-line Arguments (highest priority)
```

### Configuration Locations

| Level | Location | Purpose | Scope |
|-------|----------|---------|-------|
| Framework Defaults | Code | Built-in defaults | All projects |
| Framework Config | `AgentQMS/config/framework.yaml` | Framework-wide settings | All projects |
| Project Config | `.agentqms/config.yaml` | Project-specific overrides | Single project |
| Environment | `AGENTQMS_*` vars | Runtime overrides | Current session |
| CLI Args | Command line | One-time overrides | Single command |

---

## Configuration Schema

### Framework Configuration

**Location**: `AgentQMS/config/framework.yaml`

```yaml
# Framework Configuration
# This file contains framework-wide settings

framework:
  name: "AgentQMS"
  version: "0.1.0"
  container_name: "AgentQMS"  # Framework container directory name

# Path Configuration
paths:
  # Default output paths (relative to project root)
  artifacts: "artifacts"
  docs: "docs"
  
  # Framework internal paths (relative to AgentQMS/)
  agent_interface: "agent"
  implementation: "agent_tools"
  conventions: "conventions"
  scripts: "agent_scripts"
  config: "config"
  templates: "templates"

# Artifact Configuration
artifacts:
  # Default artifact types and their directories
  types:
    implementation_plan:
      directory: "implementation_plans"
      prefix: "implementation_plan_"
    assessment:
      directory: "assessments"
      prefix: "assessment-"
    design:
      directory: "design_documents"
      prefix: "design-"
    research:
      directory: "research"
      prefix: "research-"
    template:
      directory: "templates"
      prefix: "template-"
    bug_report:
      directory: "bug_reports"
      prefix: "BUG_"
    user_guide:
      directory: "user-guides"
      prefix: "user-guide_"

# Validation Configuration
validation:
  # Enable/disable validation checks
  enabled: true
  strict_mode: false  # Fail on warnings
  
  # Validation rules
  rules:
    naming: true
    frontmatter: true
    structure: true
    links: true
    boundaries: true

# Documentation Configuration
documentation:
  # Handbook structure
  handbook:
    root: "docs/ai_handbook"
    sections:
      - "onboarding"
      - "protocols"
      - "references"
      - "changelog"
  
  # Index generation
  indexes:
    auto_regenerate: false
    cache_metadata: true
    parallel_processing: true

# Automation Configuration
automation:
  # Pre-commit hooks
  pre_commit:
    enabled: false
    validate_artifacts: true
    validate_links: true
  
  # CI/CD integration
  ci:
    validate_on_push: true
    validate_on_pr: true
  
  # Scheduled tasks
  scheduled:
    check_stale_indexes: false
    check_dependencies: false
```

---

### Project Configuration

**Location**: `.agentqms/config.yaml`

```yaml
# Project-Specific Configuration
# This file overrides framework defaults for this project

project:
  name: "My Project"
  description: "Project description"
  
# Path Overrides
paths:
  # Override default paths (relative to project root or absolute)
  artifacts: "output/artifacts"  # Custom artifacts location
  docs: "documentation"          # Custom docs location
  
  # Absolute paths also supported
  # artifacts: "/var/project/artifacts"

# Artifact Customization
artifacts:
  # Add custom artifact types
  custom_types:
    proposal:
      directory: "proposals"
      prefix: "proposal-"
  
  # Override default types
  types:
    implementation_plan:
      directory: "plans"  # Override default directory

# Validation Overrides
validation:
  strict_mode: true  # Enable strict mode for this project
  rules:
    links: false  # Disable link validation for this project

# Framework Integration
framework:
  # Framework container location (if not standard)
  container_path: "AgentQMS"  # Default, can be overridden
  
  # Framework version (for compatibility checking)
  required_version: ">=0.1.0"
  
  # Auto-update settings
  auto_update: false
  update_channel: "stable"  # stable, beta, alpha
```

---

## Configuration Loading

### Configuration Loader Implementation

```python
# AgentQMS/agent_tools/utils/config.py

from pathlib import Path
from typing import Dict, Any, Optional
import yaml
import os

class ConfigLoader:
    """Load and merge configuration from multiple sources."""
    
    def __init__(self):
        self.framework_root = self._get_framework_root()
        self.project_root = self.framework_root.parent
        self.config = {}
    
    def load(self) -> Dict[str, Any]:
        """Load configuration with hierarchy."""
        # 1. Load framework defaults
        config = self._load_framework_defaults()
        
        # 2. Load framework config file
        framework_config = self._load_framework_config()
        config = self._merge_config(config, framework_config)
        
        # 3. Load project config file
        project_config = self._load_project_config()
        config = self._merge_config(config, project_config)
        
        # 4. Apply environment overrides
        env_overrides = self._load_environment_overrides()
        config = self._merge_config(config, env_overrides)
        
        return config
    
    def _load_framework_defaults(self) -> Dict[str, Any]:
        """Load hardcoded framework defaults."""
        return {
            "framework": {
                "name": "AgentQMS",
                "version": "0.1.0",
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
    
    def _load_framework_config(self) -> Dict[str, Any]:
        """Load framework config file."""
        config_path = self.framework_root / "config" / "framework.yaml"
        if config_path.exists():
            with open(config_path) as f:
                return yaml.safe_load(f) or {}
        return {}
    
    def _load_project_config(self) -> Dict[str, Any]:
        """Load project config file."""
        config_path = self.project_root / ".agentqms" / "config.yaml"
        if config_path.exists():
            with open(config_path) as f:
                return yaml.safe_load(f) or {}
        return {}
    
    def _load_environment_overrides(self) -> Dict[str, Any]:
        """Load environment variable overrides."""
        overrides = {}
        
        # AGENTQMS_PATHS_ARTIFACTS=...
        if artifacts := os.getenv("AGENTQMS_PATHS_ARTIFACTS"):
            overrides.setdefault("paths", {})["artifacts"] = artifacts
        
        if docs := os.getenv("AGENTQMS_PATHS_DOCS"):
            overrides.setdefault("paths", {})["docs"] = docs
        
        # AGENTQMS_VALIDATION_STRICT_MODE=true
        if strict := os.getenv("AGENTQMS_VALIDATION_STRICT_MODE"):
            overrides.setdefault("validation", {})["strict_mode"] = (
                strict.lower() == "true"
            )
        
        return overrides
    
    def _merge_config(self, base: Dict, override: Dict) -> Dict:
        """Deep merge configuration dictionaries."""
        result = base.copy()
        
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_config(result[key], value)
            else:
                result[key] = value
        
        return result
    
    def get_path(self, path_key: str) -> Path:
        """Get resolved path from configuration."""
        config = self.load()
        path_value = config.get("paths", {}).get(path_key)
        
        if not path_value:
            raise ValueError(f"Path '{path_key}' not found in configuration")
        
        path = Path(path_value)
        
        # If absolute, return as-is
        if path.is_absolute():
            return path
        
        # If relative, resolve from project root
        return self.project_root / path
    
    def _get_framework_root(self) -> Path:
        """Get framework root directory."""
        # Implementation from paths.py
        ...
```

---

## Path Resolution

### Path Resolution Functions

```python
# AgentQMS/agent_tools/utils/paths.py

from pathlib import Path
from typing import Optional
from .config import ConfigLoader

_config_loader = None

def get_config_loader() -> ConfigLoader:
    """Get singleton config loader."""
    global _config_loader
    if _config_loader is None:
        _config_loader = ConfigLoader()
    return _config_loader

def get_framework_root() -> Path:
    """Get AgentQMS framework root directory."""
    # Look for AgentQMS/ directory
    current = Path(__file__).resolve()
    for parent in [current] + list(current.parents):
        framework_root = parent / "AgentQMS"
        if framework_root.exists() and framework_root.is_dir():
            return framework_root
    
    # Fallback: look for .agentqms/ marker
    for parent in [current] + list(current.parents):
        marker = parent / ".agentqms"
        if marker.exists():
            container_name = get_config_loader().load().get(
                "framework", {}
            ).get("container_name", "AgentQMS")
            return parent / container_name
    
    raise RuntimeError(
        "Could not locate AgentQMS framework root.\n"
        "Expected AgentQMS/ directory or .agentqms/ marker."
    )

def get_project_root() -> Path:
    """Get project root (parent of AgentQMS/)."""
    return get_framework_root().parent

def get_artifacts_dir() -> Path:
    """Get artifacts directory (from config)."""
    return get_config_loader().get_path("artifacts")

def get_docs_dir() -> Path:
    """Get documentation directory (from config)."""
    return get_config_loader().get_path("docs")

def get_framework_path(component: str) -> Path:
    """Get path to framework component."""
    config = get_config_loader().load()
    framework_root = get_framework_root()
    
    # Get component path from config
    component_path = config.get("paths", {}).get(component)
    if component_path:
        return framework_root / component_path
    
    # Fallback to standard structure
    return framework_root / component
```

---

## Custom Directory Structures

### Example: Custom Artifacts Location

**Project Config** (`.agentqms/config.yaml`):
```yaml
paths:
  artifacts: "output/generated/artifacts"
  docs: "documentation/ai"
```

**Result**:
- Artifacts: `project_root/output/generated/artifacts/`
- Docs: `project_root/documentation/ai/`

---

### Example: Absolute Paths

**Project Config** (`.agentqms/config.yaml`):
```yaml
paths:
  artifacts: "/var/project/artifacts"
  docs: "/var/project/docs"
```

**Result**:
- Artifacts: `/var/project/artifacts/`
- Docs: `/var/project/docs/`

---

### Example: Environment Override

**Environment**:
```bash
export AGENTQMS_PATHS_ARTIFACTS="tmp/artifacts"
```

**Result**: Overrides config file, uses `tmp/artifacts/`

---

## Configuration Validation

### Schema Validation

```python
# AgentQMS/agent_tools/compliance/validate_config.py

import jsonschema
from pathlib import Path

CONFIG_SCHEMA = {
    "type": "object",
    "properties": {
        "framework": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "version": {"type": "string"},
                "container_name": {"type": "string"},
            },
        },
        "paths": {
            "type": "object",
            "properties": {
                "artifacts": {"type": "string"},
                "docs": {"type": "string"},
            },
        },
        # ... more schema
    },
}

def validate_config(config_path: Path) -> bool:
    """Validate configuration file against schema."""
    with open(config_path) as f:
        config = yaml.safe_load(f)
    
    try:
        jsonschema.validate(config, CONFIG_SCHEMA)
        return True
    except jsonschema.ValidationError as e:
        print(f"❌ Config validation error: {e.message}")
        return False
```

---

## Configuration Examples

### Minimal Configuration

**No config files needed** - framework uses defaults:
- Artifacts: `artifacts/`
- Docs: `docs/`

---

### Custom Paths

**`.agentqms/config.yaml`**:
```yaml
paths:
  artifacts: "output/artifacts"
  docs: "documentation"
```

---

### Custom Artifact Types

**`.agentqms/config.yaml`**:
```yaml
artifacts:
  custom_types:
    proposal:
      directory: "proposals"
      prefix: "proposal-"
    review:
      directory: "reviews"
      prefix: "review-"
```

---

### Strict Validation

**`.agentqms/config.yaml`**:
```yaml
validation:
  strict_mode: true
  rules:
    naming: true
    frontmatter: true
    links: true
```

---

## Migration from Current Structure

### Backward Compatibility

The configuration system supports both old and new structures:

```python
def detect_structure() -> str:
    """Detect current project structure."""
    project_root = get_project_root()
    
    # Check for new structure
    if (project_root / "AgentQMS").exists():
        return "containerized"
    
    # Check for old structure
    if (project_root / "agent_tools").exists():
        return "scattered"
    
    return "unknown"

def get_paths_compatible():
    """Get paths compatible with both structures."""
    structure = detect_structure()
    
    if structure == "containerized":
        return get_paths_containerized()
    elif structure == "scattered":
        return get_paths_scattered()
    else:
        raise RuntimeError("Unknown project structure")
```

---

## Best Practices

### 1. Use Relative Paths
Prefer relative paths in config for portability:
```yaml
paths:
  artifacts: "artifacts"  # ✅ Good
  # artifacts: "/absolute/path"  # ❌ Avoid (not portable)
```

### 2. Version Configuration
Include version in project config for compatibility:
```yaml
framework:
  required_version: ">=0.1.0"
```

### 3. Document Custom Paths
Document custom paths in project README:
```markdown
## Framework Configuration

Artifacts are stored in `output/artifacts/` (configured in `.agentqms/config.yaml`).
```

### 4. Validate on Load
Always validate configuration on load:
```python
config = ConfigLoader().load()
if not validate_config(config):
    raise RuntimeError("Invalid configuration")
```

---

## Next Steps

1. **Implement ConfigLoader** with hierarchy support
2. **Create schema files** for validation
3. **Update path resolution** to use config
4. **Add config validation** to framework startup
5. **Document configuration** in framework README

---

**See Also**:
- `06_containerization_design.md` - Container structure
- `09_boundary_enforcement.md` - Boundary validation
- `07_migration_strategy.md` - Migration from current structure

