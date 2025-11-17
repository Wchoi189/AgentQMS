# Naming Convention Recommendations

**Date**: 2025-11-09  
**Design Scope**: Framework Naming Standards  
**Status**: Recommendations

## Executive Summary

This document provides naming convention recommendations for the containerized framework structure, ensuring clarity, consistency, and ease of maintenance.

---

## Framework Container Naming

### Primary Container: `AgentQMS/`

**Rationale**:
- ✅ Matches framework branding
- ✅ Clear and descriptive
- ✅ PascalCase follows common convention for top-level directories
- ✅ Easy to identify in directory listings
- ✅ Distinct from project directories

**Alternatives Considered**:
- `agent-qms/` - ❌ Hyphens less common
- `agent_qms/` - ❌ Underscores less common
- `.agentqms/` - ❌ Hidden, harder to discover
- `framework/` - ❌ Too generic
- `qms/` - ❌ Too abbreviated

**Decision**: ✅ **`AgentQMS/`**

---

## Directory Naming Conventions

### Framework Directories (Inside `AgentQMS/`)

| Current Name | New Name | Rationale |
|--------------|----------|-----------|
| `agent/` | `agent/` | ✅ Clear, no change needed |
| `agent_tools/` | `agent_tools/` | ✅ Clear, no change needed |
| `quality_management_framework/` | `conventions/` | ✅ Shorter, clearer purpose |
| `scripts/` | `agent_scripts/` | ✅ Prevents namespace collision |
| N/A | `config/` | ✅ New, centralized config |
| N/A | `templates/` | ✅ New, project setup templates |

### Naming Rules

1. **Use lowercase with underscores**: `agent_tools/`, `agent_scripts/`
2. **Be descriptive**: `conventions/` not `qms/`
3. **Avoid abbreviations**: `agent_scripts/` not `scripts/`
4. **Plural for collections**: `templates/`, `conventions/`
5. **Singular for single-purpose**: `config/`, `agent/`

---

## Component Naming

### Renamed Components

#### `quality_management_framework/` → `conventions/`

**Rationale**:
- **Shorter**: Easier to type and reference
- **Clearer**: "Conventions" better describes content (rules, standards, templates)
- **Consistent**: Matches purpose (conventions, not framework)

**Migration**:
```bash
mv quality_management_framework conventions
# Update all references
find . -type f -exec sed -i 's/quality_management_framework/conventions/g' {} \;
```

---

#### `scripts/` → `agent_scripts/`

**Rationale**:
- **Namespace clarity**: Prevents collision with project `scripts/` directory
- **Framework identification**: Makes it clear these are framework scripts
- **Consistency**: Matches `agent_tools/` naming pattern

**Migration**:
```bash
mv scripts agent_scripts
# Update all references
find . -type f -exec sed -i 's|scripts/|agent_scripts/|g' {} \;
```

---

## File Naming Conventions

### Configuration Files

| Purpose | Naming Pattern | Example |
|---------|---------------|---------|
| Framework config | `framework.yaml` | `AgentQMS/config/framework.yaml` |
| Project config | `config.yaml` | `.agentqms/config.yaml` |
| Path config | `paths.yaml` | `AgentQMS/config/paths.yaml` |
| Validation rules | `validation_rules.yaml` | `AgentQMS/config/validation_rules.yaml` |
| Boundary rules | `boundary_rules.yaml` | `AgentQMS/config/boundary_rules.yaml` |

**Rules**:
- Use lowercase with underscores
- Be descriptive: `framework.yaml` not `config.yaml`
- Group related configs: `validation_rules.yaml` not `rules.yaml`

---

### Python Module Naming

| Component | Naming Pattern | Example |
|-----------|---------------|---------|
| Utilities | `utils/` | `AgentQMS/agent_tools/utils/` |
| Path utilities | `paths.py` | `AgentQMS/agent_tools/utils/paths.py` |
| Config loader | `config.py` | `AgentQMS/agent_tools/utils/config.py` |
| Validators | `validate_*.py` | `AgentQMS/agent_tools/compliance/validate_boundaries.py` |

**Rules**:
- Use lowercase with underscores
- Be descriptive: `validate_boundaries.py` not `boundaries.py`
- Group by function: `utils/`, `compliance/`, `core/`

---

### Template Naming

| Purpose | Naming Pattern | Example |
|---------|---------------|---------|
| Artifact templates | `<type>_template.md` | `implementation_plan_template.md` |
| Project templates | `<name>.template` | `project_config.yaml.template` |
| Handbook templates | `<section>_template.md` | `onboarding_template.md` |

**Rules**:
- Include type in name: `implementation_plan_template.md`
- Use `.template` extension for config templates
- Be descriptive: `project_config.yaml.template` not `config.template`

---

## Variable and Function Naming

### Python Code

**Functions**:
```python
# ✅ Good
def get_framework_root() -> Path:
    """Get AgentQMS framework root directory."""
    ...

def validate_boundaries() -> bool:
    """Validate framework boundaries."""
    ...

# ❌ Bad
def get_root():  # Too generic
def validate():  # Too generic
```

**Variables**:
```python
# ✅ Good
framework_root = get_framework_root()
project_root = framework_root.parent
artifacts_dir = get_artifacts_dir()

# ❌ Bad
root = get_root()  # Unclear which root
dir = get_dir()    # Too generic
```

**Classes**:
```python
# ✅ Good
class BoundaryValidator:
    """Validate framework boundaries."""
    ...

class ConfigLoader:
    """Load framework configuration."""
    ...

# ❌ Bad
class Validator:  # Too generic
class Loader:     # Too generic
```

---

## Path Reference Naming

### In Code

**Functions**:
```python
# ✅ Good
get_framework_root()      # Returns AgentQMS/
get_project_root()        # Returns project root
get_artifacts_dir()       # Returns artifacts directory
get_docs_dir()            # Returns docs directory

# ❌ Bad
get_root()                # Unclear
get_dir()                 # Too generic
get_path()                # Too generic
```

**Variables**:
```python
# ✅ Good
framework_root = Path("AgentQMS")
project_root = framework_root.parent
artifacts_path = "artifacts"

# ❌ Bad
root = Path("AgentQMS")   # Unclear
path = "artifacts"        # Too generic
```

---

## Documentation Naming

### Documentation Files

| Purpose | Naming Pattern | Example |
|---------|---------------|---------|
| Framework README | `README.md` | `AgentQMS/README.md` |
| Component docs | `README.md` | `AgentQMS/agent_tools/README.md` |
| Design docs | `<topic>_design.md` | `containerization_design.md` |
| Migration guides | `migration_*.md` | `migration_strategy.md` |

**Rules**:
- Use descriptive names: `containerization_design.md`
- Group related docs: `migration_strategy.md`, `migration_checklist.md`
- Use consistent prefixes: `*_design.md`, `*_strategy.md`

---

## Environment Variable Naming

### Framework Environment Variables

**Pattern**: `AGENTQMS_<CATEGORY>_<NAME>`

**Examples**:
```bash
# Path overrides
AGENTQMS_PATHS_ARTIFACTS=output/artifacts
AGENTQMS_PATHS_DOCS=documentation

# Validation settings
AGENTQMS_VALIDATION_STRICT_MODE=true
AGENTQMS_VALIDATION_ENABLED=true

# Framework settings
AGENTQMS_FRAMEWORK_VERSION=0.1.0
AGENTQMS_FRAMEWORK_CONTAINER_NAME=AgentQMS
```

**Rules**:
- Prefix with `AGENTQMS_`
- Use uppercase with underscores
- Group by category: `PATHS_`, `VALIDATION_`, `FRAMEWORK_`
- Be descriptive: `AGENTQMS_PATHS_ARTIFACTS` not `AGENTQMS_ARTIFACTS`

---

## Command-Line Tool Naming

### CLI Commands

| Purpose | Command | Example |
|---------|---------|---------|
| Framework CLI | `agentqms` | `agentqms create artifact` |
| Migration tool | `migrate_structure.py` | `python migrate_structure.py` |
| Validation | `validate_boundaries.py` | `python validate_boundaries.py` |

**Rules**:
- Use lowercase with underscores for scripts
- Be descriptive: `validate_boundaries.py` not `validate.py`
- Use consistent prefixes: `validate_*.py`, `migrate_*.py`

---

## Git Repository Naming

### Framework Repository

**Recommended**: `agent-qms` or `AgentQMS`

**Rationale**:
- Matches framework name
- Clear and searchable
- Follows common conventions

---

## Summary of Naming Decisions

### Container
- ✅ **`AgentQMS/`** - Framework container directory

### Directories
- ✅ `agent/` - Agent interface (unchanged)
- ✅ `agent_tools/` - Implementation (unchanged)
- ✅ `conventions/` - Standards and rules (renamed from `quality_management_framework/`)
- ✅ `agent_scripts/` - Framework scripts (renamed from `scripts/`)
- ✅ `config/` - Framework configuration (new)
- ✅ `templates/` - Project setup templates (new)

### Files
- ✅ `framework.yaml` - Framework configuration
- ✅ `config.yaml` - Project configuration
- ✅ `*_template.md` - Artifact templates
- ✅ `validate_*.py` - Validation scripts
- ✅ `migrate_*.py` - Migration scripts

### Functions
- ✅ `get_framework_root()` - Get framework container
- ✅ `get_project_root()` - Get project root
- ✅ `get_artifacts_dir()` - Get artifacts directory
- ✅ `validate_boundaries()` - Validate boundaries

### Environment Variables
- ✅ `AGENTQMS_*` - Framework environment variables

---

## Naming Checklist

### For New Components

- [ ] Uses lowercase with underscores
- [ ] Descriptive and clear
- [ ] Consistent with existing patterns
- [ ] No abbreviations (unless standard)
- [ ] No conflicts with project names

### For Renamed Components

- [ ] Old name documented
- [ ] Migration path clear
- [ ] All references updated
- [ ] Backward compatibility considered

---

## Best Practices

### 1. Be Descriptive
```python
# ✅ Good
get_framework_root()
validate_boundaries()

# ❌ Bad
get_root()
validate()
```

### 2. Use Consistent Patterns
```python
# ✅ Good - consistent prefix
get_framework_root()
get_project_root()
get_artifacts_dir()

# ❌ Bad - inconsistent
get_framework_root()
project_root()
artifacts()
```

### 3. Avoid Abbreviations
```python
# ✅ Good
get_artifacts_directory()
validate_boundaries()

# ❌ Bad
get_art_dir()
validate_bounds()
```

### 4. Group Related Items
```python
# ✅ Good - grouped by function
validate_boundaries()
validate_artifacts()
validate_config()

# ❌ Bad - scattered
check_boundaries()
validate_artifacts()
verify_config()
```

---

## Migration Impact

### Files Requiring Updates

1. **Path References**:
   - `quality_management_framework/` → `conventions/`
   - `scripts/` → `agent_scripts/`

2. **Import Statements**:
   - Update Python imports
   - Update documentation references

3. **Configuration Files**:
   - Update path references
   - Update documentation

4. **Documentation**:
   - Update all examples
   - Update README files

---

## Next Steps

1. **Review naming decisions** with stakeholders
2. **Update code** with new names
3. **Update documentation** with new names
4. **Create migration script** for renaming
5. **Test** all references work

---

**See Also**:
- `06_containerization_design.md` - Container structure
- `07_migration_strategy.md` - Migration plan
- `04_standards_specification.md` - General standards

