# Boundary Enforcement Mechanism Design

**Date**: 2025-11-09  
**Design Scope**: Framework Boundary Validation  
**Status**: Design Proposal

## Executive Summary

This document designs automated mechanisms to enforce clear boundaries between framework content (inside `AgentQMS/`) and project content (outside), ensuring structural compliance and preventing boundary violations.

---

## Boundary Definition

### Framework Boundary

**Inside `AgentQMS/`** (Framework Territory):
- ✅ Framework code (`agent/`, `agent_tools/`, `project_conventions/`)
- ✅ Framework configuration (`config/`)
- ✅ Framework templates (`templates/`)
- ✅ Framework scripts (`agent_scripts/`)
- ✅ Framework documentation (framework README, etc.)
- ❌ No project-specific code
- ❌ No generated artifacts
- ❌ No project configuration

**Outside `AgentQMS/`** (Project Territory):
- ✅ Project code
- ✅ Generated artifacts (in configurable location)
- ✅ Project documentation (in configurable location)
- ✅ Project configuration
- ✅ `.agentqms/` metadata directory
- ❌ No framework code (except in `AgentQMS/`)
- ❌ No framework modifications outside container

---

## Enforcement Mechanisms

### 1. Static Boundary Validation

**Purpose**: Validate structure at rest (no active operations)

**Implementation**:
```python
# AgentQMS/agent_tools/compliance/validate_boundaries.py

from pathlib import Path
from typing import List, Tuple
from dataclasses import dataclass

@dataclass
class BoundaryViolation:
    """Represents a boundary violation."""
    path: Path
    violation_type: str
    message: str
    severity: str  # "error" | "warning"

class BoundaryValidator:
    """Validate framework vs. project boundaries."""
    
    def __init__(self):
        self.framework_root = self._get_framework_root()
        self.project_root = self.framework_root.parent
        self.violations: List[BoundaryViolation] = []
    
    def validate_all(self) -> Tuple[bool, List[BoundaryViolation]]:
        """Run all boundary validations."""
        self.violations = []
        
        # Check framework boundary (no project content in AgentQMS/)
        self._validate_framework_boundary()
        
        # Check project boundary (no framework code outside AgentQMS/)
        self._validate_project_boundary()
        
        # Check output paths (artifacts/docs in correct locations)
        self._validate_output_paths()
        
        # Check for orphaned framework files
        self._validate_orphaned_files()
        
        errors = [v for v in self.violations if v.severity == "error"]
        return len(errors) == 0, self.violations
    
    def _validate_framework_boundary(self):
        """Ensure no project content in AgentQMS/."""
        project_markers = [
            "requirements.txt",      # Project dependencies
            "setup.py",              # Project setup
            "pyproject.toml",        # Project config
            "package.json",          # Project config
            ".env",                  # Project environment
            ".env.local",            # Project environment
        ]
        
        for marker in project_markers:
            path = self.framework_root / marker
            if path.exists():
                self.violations.append(BoundaryViolation(
                    path=path,
                    violation_type="project_file_in_framework",
                    message=f"Project file '{marker}' found in framework container",
                    severity="error"
                ))
        
        # Check for project-specific patterns in framework code
        self._check_project_references_in_framework()
    
    def _validate_project_boundary(self):
        """Ensure no framework code outside AgentQMS/."""
        framework_markers = [
            "agent_tools/",                    # Old structure
            "quality_management_framework/",   # Old structure
            "agent/Makefile",                  # Framework Makefile
        ]
        
        for marker in framework_markers:
            path = self.project_root / marker
            if path.exists() and not path.is_relative_to(self.framework_root):
                self.violations.append(BoundaryViolation(
                    path=path,
                    violation_type="framework_file_outside_container",
                    message=f"Framework file '{marker}' found outside AgentQMS/",
                    severity="error"
                ))
    
    def _validate_output_paths(self):
        """Ensure artifacts/docs are in configured locations."""
        from ..utils.config import get_config_loader
        
        config = get_config_loader().load()
        artifacts_dir = Path(config.get("paths", {}).get("artifacts", "artifacts"))
        docs_dir = Path(config.get("paths", {}).get("docs", "docs"))
        
        # Resolve relative to project root
        if not artifacts_dir.is_absolute():
            artifacts_dir = self.project_root / artifacts_dir
        if not docs_dir.is_absolute():
            docs_dir = self.project_root / docs_dir
        
        # Check artifacts not in framework
        if artifacts_dir.is_relative_to(self.framework_root):
            self.violations.append(BoundaryViolation(
                path=artifacts_dir,
                violation_type="artifacts_in_framework",
                message="Artifacts directory configured inside framework container",
                severity="error"
            ))
        
        # Check docs not in framework (except framework docs)
        if docs_dir.is_relative_to(self.framework_root):
            self.violations.append(BoundaryViolation(
                path=docs_dir,
                violation_type="docs_in_framework",
                message="Documentation directory configured inside framework container",
                severity="warning"  # Framework might have its own docs
            ))
    
    def _validate_orphaned_files(self):
        """Check for orphaned framework files from old structure."""
        old_structure_dirs = [
            self.project_root / "agent_tools",
            self.project_root / "quality_management_framework",
        ]
        
        for old_dir in old_structure_dirs:
            if old_dir.exists() and old_dir.is_dir():
                # Check if it's actually old structure (not just similar name)
                if self._is_old_framework_structure(old_dir):
                    self.violations.append(BoundaryViolation(
                        path=old_dir,
                        violation_type="orphaned_framework_files",
                        message=f"Old framework structure found: {old_dir.name}/",
                        severity="warning"
                    ))
    
    def _check_project_references_in_framework(self):
        """Check for hardcoded project references in framework code."""
        project_patterns = [
            r"upstage",           # Project-specific term
            r"korean.*grammar",   # Project-specific term
            r"prompt.*hack",      # Project-specific term
        ]
        
        import re
        
        for py_file in self.framework_root.rglob("*.py"):
            if py_file.name.startswith("test_"):
                continue  # Skip test files
            
            content = py_file.read_text()
            for pattern in project_patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    self.violations.append(BoundaryViolation(
                        path=py_file,
                        violation_type="project_reference_in_framework",
                        message=f"Project-specific reference found: {pattern}",
                        severity="warning"
                    ))
    
    def _is_old_framework_structure(self, path: Path) -> bool:
        """Check if directory is old framework structure."""
        # Look for framework markers
        markers = [
            path / "core" / "artifact_workflow.py",
            path / "compliance" / "validate_artifacts.py",
        ]
        return any(m.exists() for m in markers)
    
    def _get_framework_root(self) -> Path:
        """Get framework root directory."""
        from ..utils.paths import get_framework_root
        return get_framework_root()
```

---

### 2. Runtime Boundary Checks

**Purpose**: Prevent boundary violations during operations

**Implementation**:
```python
# AgentQMS/agent_tools/core/artifact_workflow.py

def create_artifact(artifact_type: str, name: str, title: str):
    """Create artifact with boundary validation."""
    from ..compliance.validate_boundaries import BoundaryValidator
    
    # Validate boundaries before operation
    validator = BoundaryValidator()
    valid, violations = validator.validate_all()
    
    if not valid:
        errors = [v for v in violations if v.severity == "error"]
        if errors:
            raise RuntimeError(
                "Boundary violations detected. Cannot create artifact.\n" +
                "\n".join(f"  - {v.message}" for v in errors)
            )
    
    # Get artifacts directory (validated to be outside framework)
    artifacts_dir = get_artifacts_dir()
    
    # Ensure artifacts directory is not in framework
    framework_root = get_framework_root()
    if artifacts_dir.is_relative_to(framework_root):
        raise RuntimeError(
            f"Artifacts directory cannot be inside framework container.\n"
            f"Current: {artifacts_dir}\n"
            f"Framework: {framework_root}\n"
            f"Update .agentqms/config.yaml to set artifacts path outside AgentQMS/"
        )
    
    # Create artifact (boundary validated)
    ...
```

---

### 3. Pre-commit Boundary Validation

**Purpose**: Prevent boundary violations from being committed

**Implementation**:
```bash
#!/bin/bash
# .git/hooks/pre-commit

# Run boundary validation
python AgentQMS/agent_tools/compliance/validate_boundaries.py --pre-commit

if [ $? -ne 0 ]; then
    echo "❌ Boundary validation failed. Commit aborted."
    echo "Run 'make validate-boundaries' to see details."
    exit 1
fi

exit 0
```

**CLI Tool**:
```python
# AgentQMS/agent_tools/compliance/validate_boundaries.py

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Validate framework boundaries")
    parser.add_argument("--pre-commit", action="store_true",
                       help="Run in pre-commit mode (exit with error code)")
    parser.add_argument("--fix", action="store_true",
                       help="Attempt to fix violations automatically")
    
    args = parser.parse_args()
    
    validator = BoundaryValidator()
    valid, violations = validator.validate_all()
    
    if violations:
        print("⚠️  Boundary violations found:\n")
        for violation in violations:
            severity_icon = "❌" if violation.severity == "error" else "⚠️"
            print(f"{severity_icon} {violation.message}")
            print(f"   Path: {violation.path}")
            print()
    
    if not valid:
        if args.pre_commit:
            sys.exit(1)
        else:
            print("Run with --fix to attempt automatic fixes")
            sys.exit(1)
    else:
        print("✅ No boundary violations found")
        sys.exit(0)
```

---

### 4. CI/CD Boundary Checks

**Purpose**: Validate boundaries in continuous integration

**Implementation**:
```yaml
# .github/workflows/validate-boundaries.yml

name: Validate Boundaries

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  validate-boundaries:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: |
          pip install -r AgentQMS/requirements.txt
      
      - name: Validate boundaries
        run: |
          python AgentQMS/agent_tools/compliance/validate_boundaries.py
      
      - name: Check for orphaned files
        run: |
          python AgentQMS/agent_tools/compliance/validate_boundaries.py --check-orphaned
```

---

## Auto-Fix Capabilities

### Automatic Boundary Fixes

**Purpose**: Automatically fix common boundary violations

**Implementation**:
```python
# AgentQMS/agent_tools/compliance/fix_boundaries.py

class BoundaryFixer:
    """Automatically fix boundary violations."""
    
    def fix_all(self, violations: List[BoundaryViolation], dry_run: bool = False) -> List[str]:
        """Attempt to fix violations."""
        fixed = []
        
        for violation in violations:
            if violation.violation_type == "orphaned_framework_files":
                if self._can_migrate_orphaned(violation.path):
                    if not dry_run:
                        self._migrate_to_container(violation.path)
                    fixed.append(f"Migrated {violation.path} to AgentQMS/")
            
            elif violation.violation_type == "project_file_in_framework":
                if not dry_run:
                    # Move project file to project root
                    target = self.project_root / violation.path.name
                    violation.path.rename(target)
                fixed.append(f"Moved {violation.path.name} to project root")
        
        return fixed
    
    def _can_migrate_orphaned(self, path: Path) -> bool:
        """Check if orphaned directory can be migrated."""
        # Only migrate if it's clearly old framework structure
        return self._is_old_framework_structure(path)
    
    def _migrate_to_container(self, old_path: Path):
        """Migrate old framework structure to container."""
        framework_root = get_framework_root()
        
        # Determine target location in container
        if old_path.name == "agent_tools":
            target = framework_root / "agent_tools"
        elif old_path.name == "quality_management_framework":
            target = framework_root / "conventions"
        else:
            return  # Unknown structure
        
        # Move directory
        if target.exists():
            # Merge directories
            self._merge_directories(old_path, target)
        else:
            old_path.rename(target)
```

---

## Boundary Rules Configuration

### Configurable Boundary Rules

**Location**: `AgentQMS/config/boundary_rules.yaml`

```yaml
# Boundary Enforcement Rules

# Files that should NOT be in framework
framework_forbidden:
  patterns:
    - "requirements.txt"
    - "setup.py"
    - "pyproject.toml"
    - "package.json"
    - ".env*"
    - "*.log"
  
  directories:
    - "node_modules"
    - "__pycache__"
    - ".pytest_cache"

# Files that should NOT be outside framework
project_forbidden:
  patterns:
    - "agent_tools/**"
    - "quality_management_framework/**"
    - "agent/Makefile"
  
  # Allow these in project (they're project-specific)
  exceptions:
    - "agent/docs/artifacts/**"  # Project artifacts
    - "agent/config/project_*.yaml"  # Project config

# Output path validation
output_paths:
  # Artifacts must be outside framework
  artifacts:
    must_be_outside_framework: true
    default_location: "artifacts"
  
  # Docs can be anywhere (but recommended outside)
  docs:
    must_be_outside_framework: false
    default_location: "docs"
    recommended_outside: true

# Project reference patterns (warnings)
project_references:
  patterns:
    - "upstage"
    - "korean.*grammar"
    - "prompt.*hack"
  severity: "warning"  # error | warning
```

---

## Validation Modes

### Strict Mode

**Behavior**: All violations are errors, no warnings

**Use Case**: CI/CD, pre-commit hooks

**Configuration**:
```yaml
# .agentqms/config.yaml
validation:
  boundary_strict_mode: true
```

---

### Warning Mode

**Behavior**: Some violations are warnings (e.g., project references)

**Use Case**: Development, gradual migration

**Configuration**:
```yaml
# .agentqms/config.yaml
validation:
  boundary_strict_mode: false
```

---

## Integration Points

### 1. Artifact Creation

```python
def create_artifact(...):
    # Validate boundaries before creation
    validate_boundaries()
    # Create artifact in validated location
    ...
```

### 2. Path Resolution

```python
def get_artifacts_dir():
    # Resolve path
    path = resolve_path_from_config()
    # Validate boundary
    assert not path.is_relative_to(get_framework_root())
    return path
```

### 3. Configuration Loading

```python
def load_config():
    # Load config
    config = load_config_file()
    # Validate output paths
    validate_output_paths(config)
    return config
```

---

## Reporting

### Violation Report Format

```
Boundary Validation Report
==========================

Errors: 2
Warnings: 1

❌ ERROR: Project file in framework
   Path: AgentQMS/requirements.txt
   Fix: Move to project root

❌ ERROR: Framework file outside container
   Path: agent_tools/
   Fix: Migrate to AgentQMS/agent_tools/

⚠️  WARNING: Project reference in framework
   Path: AgentQMS/agent_tools/core/example.py
   Pattern: "upstage"
   Fix: Remove project-specific references
```

---

## Best Practices

### 1. Validate Early
Run boundary validation:
- Before artifact creation
- In pre-commit hooks
- In CI/CD pipelines
- During framework updates

### 2. Fix Automatically
Use `--fix` flag for automatic fixes:
```bash
python AgentQMS/agent_tools/compliance/validate_boundaries.py --fix
```

### 3. Document Exceptions
If exceptions are needed, document them:
```yaml
# .agentqms/config.yaml
boundary:
  exceptions:
    - "AgentQMS/docs/project-specific.md"  # Documented exception
```

### 4. Regular Audits
Run boundary validation regularly:
```bash
# Weekly audit
python AgentQMS/agent_tools/compliance/validate_boundaries.py --report
```

---

## Next Steps

1. **Implement BoundaryValidator** with all checks
2. **Create boundary rules config** file
3. **Add pre-commit hook** for boundary validation
4. **Integrate with artifact creation** workflow
5. **Add CI/CD checks** for boundaries

---

**See Also**:
- `06_containerization_design.md` - Container structure
- `08_configuration_schema.md` - Configuration system
- `07_migration_strategy.md` - Migration from old structure

