# Framework Containerization Design

**Date**: 2025-11-09  
**Design Scope**: Containerized Framework Structure  
**Status**: Design Proposal

## Executive Summary

This document proposes a containerized directory structure that isolates all framework content under a single parent directory (`AgentQMS/`), enabling clear separation from project content, easy framework updates, and configurable output paths.

---

## Problem Statement

### Current Issues

1. **Scattered Framework Content**: Framework directories (`agent/`, `agent_tools/`, `quality_management_framework/`) are mixed with project content at root level
2. **Unclear Boundaries**: Difficult to distinguish framework vs. project files
3. **Hard to Maintain**: Framework updates require touching multiple root-level directories
4. **No Isolation**: Project structure changes can break framework assumptions
5. **Difficult Removal**: Removing framework requires identifying scattered directories

### Impact

- Framework appears as project code
- Risk of accidental modification of framework files
- Complex path resolution logic
- Difficult to version framework independently
- Hard to share framework across projects

---

## Design Principles

1. **Single Container**: All framework content in one directory
2. **Clear Boundaries**: Explicit separation of framework vs. project
3. **Configurable Outputs**: Project artifacts in configurable locations
4. **Portable Framework**: Framework can be moved/updated as unit
5. **Backward Compatible**: Migration path from current structure

---

## Proposed Container Structure

### Refined Structure

```
project_root/
├── AgentQMS/                          # Framework container (all framework content)
│   ├── agent/                         # Agent interface layer
│   │   ├── Makefile                  # Agent commands
│   │   ├── config/                   # Agent configuration
│   │   ├── tools/                    # Agent tool wrappers
│   │   └── workflows/                # Workflow scripts
│   │
│   ├── agent_tools/                  # Implementation layer
│   │   ├── core/                     # Core automation
│   │   ├── compliance/               # Validation tools
│   │   ├── documentation/            # Doc management
│   │   ├── utilities/                # Helper functions
│   │   └── utils/                    # Framework utilities
│   │
│   ├── conventions/                  # Rules & standards (renamed from quality_management_framework)
│   │   ├── templates/                # Artifact templates
│   │   ├── schemas/                  # JSON schemas
│   │   ├── config/                   # Framework configuration
│   │   └── toolbelt/                 # Python toolbelt
│   │
│   ├── agent_scripts/                # Agent-specific scripts (renamed from scripts)
│   │   ├── adapt_project.py          # Project adaptation
│   │   ├── browser-automation/       # Browser tools
│   │   └── utilities/                # Utility scripts
│   │
│   ├── config/                       # Framework configuration
│   │   ├── framework.yaml            # Framework settings
│   │   ├── paths.yaml                # Path mappings
│   │   └── validation_rules.yaml     # Validation configuration
│   │
│   ├── templates/                    # Project setup templates
│   │   ├── project_config.yaml.template
│   │   └── handbook_templates/       # Handbook templates
│   │
│   └── README.md                     # Framework documentation
│
├── artifacts/                        # Project artifacts (configurable)
│   ├── implementation_plans/
│   ├── assessments/
│   ├── design_documents/
│   ├── research/
│   ├── templates/
│   ├── bug_reports/
│   └── user-guides/
│
├── docs/                             # Project documentation (configurable)
│   ├── ai_handbook/                  # AI agent docs
│   └── project/                      # Project-specific docs
│
└── .agentqms/                        # Framework metadata (hidden)
    ├── version                       # Framework version
    ├── installed                     # Installation timestamp
    └── config.yaml                   # Active configuration
```

### Structure Rationale

#### 1. `AgentQMS/` Container
**Purpose**: Single parent for all framework content

**Benefits**:
- Clear framework boundary
- Easy to identify framework files
- Simple framework updates (replace entire directory)
- Framework can be versioned independently

**Contents**:
- All framework code and configuration
- No project-specific content
- Self-contained and portable

---

#### 2. `AgentQMS/agent/` - Interface Layer
**Purpose**: Agent-facing commands and tools

**Rationale**: 
- Keeps agent interface separate from implementation
- Makes it clear these are framework tools, not project tools
- Maintains existing structure within container

---

#### 3. `AgentQMS/agent_tools/` - Implementation Layer
**Purpose**: Core automation and tooling

**Rationale**:
- Implementation separate from interface
- Clear separation of concerns
- Easy to test and maintain

---

#### 4. `AgentQMS/conventions/` - Standards & Rules
**Purpose**: Framework conventions, templates, schemas

**Rationale**:
- Renamed from `quality_management_framework` for clarity
- "Conventions" better describes content (rules, standards, templates)
- Shorter, clearer name

**Alternative Names Considered**:
- `quality_management_framework/` - Too long, unclear
- `qms/` - Too abbreviated
- `standards/` - Too generic
- `conventions/` - ✅ Clear, descriptive

---

#### 5. `AgentQMS/agent_scripts/` - Framework Scripts
**Purpose**: Framework utility scripts

**Rationale**:
- Renamed from `scripts/` to avoid confusion with project scripts
- Clear that these are framework scripts
- Prevents namespace collision with project `scripts/` directory

---

#### 6. `AgentQMS/config/` - Framework Configuration
**Purpose**: Framework-level configuration

**Rationale**:
- Centralized configuration location
- Separates framework config from project config
- Easy to find and modify

---

#### 7. Project Directories (`artifacts/`, `docs/`)
**Purpose**: Project-generated content

**Rationale**:
- Outside framework container
- Configurable paths (see Configuration Strategy)
- Clear separation: framework generates, project stores

---

#### 8. `.agentqms/` - Framework Metadata
**Purpose**: Framework installation metadata

**Rationale**:
- Hidden directory (starts with `.`)
- Stores framework state
- Not part of framework code (generated)
- Can be gitignored or committed (project choice)

---

## Directory Naming Rationale

### Why `AgentQMS/`?

**Options Considered**:
1. `AgentQMS/` - ✅ Clear, matches framework name
2. `agent-qms/` - ❌ Hyphens less common in directory names
3. `agent_qms/` - ❌ Underscores less common in directory names
4. `.agentqms/` - ❌ Hidden, might be confusing
5. `framework/` - ❌ Too generic

**Decision**: `AgentQMS/`
- Matches framework branding
- Clear and descriptive
- Follows common convention (PascalCase for top-level directories)
- Easy to identify in directory listings

---

## Component Organization

### Framework Components (Inside `AgentQMS/`)

| Component | Purpose | Location | Configurable? |
|-----------|---------|----------|---------------|
| Agent Interface | Commands and wrappers | `agent/` | No |
| Implementation | Core automation | `agent_tools/` | No |
| Conventions | Templates, schemas, rules | `conventions/` | No |
| Scripts | Framework utilities | `agent_scripts/` | No |
| Config | Framework settings | `config/` | Yes (content) |
| Templates | Project setup templates | `templates/` | No |

### Project Components (Outside `AgentQMS/`)

| Component | Purpose | Location | Configurable? |
|-----------|---------|----------|---------------|
| Artifacts | Generated artifacts | `artifacts/` | Yes (path) |
| Documentation | Project docs | `docs/` | Yes (path) |
| Metadata | Framework state | `.agentqms/` | No |

---

## Path Resolution Strategy

### Framework Path Resolution

```python
# AgentQMS/agent_tools/utils/paths.py

from pathlib import Path
from typing import Optional

def get_framework_root() -> Path:
    """Get AgentQMS framework root directory."""
    # Strategy 1: Look for AgentQMS/ directory from current location
    current = Path(__file__).resolve()
    for parent in [current] + list(current.parents):
        framework_root = parent / "AgentQMS"
        if framework_root.exists() and framework_root.is_dir():
            return framework_root
    
    # Strategy 2: Look for .agentqms/ marker
    for parent in [current] + list(current.parents):
        marker = parent / ".agentqms"
        if marker.exists():
            return parent / "AgentQMS"
    
    raise RuntimeError(
        "Could not locate AgentQMS framework root.\n"
        "Expected AgentQMS/ directory or .agentqms/ marker."
    )

def get_project_root() -> Path:
    """Get project root (parent of AgentQMS/)."""
    framework_root = get_framework_root()
    return framework_root.parent

def get_artifacts_dir() -> Path:
    """Get artifacts directory (configurable)."""
    config = load_framework_config()
    artifacts_path = config.get("paths", {}).get("artifacts", "artifacts")
    
    if Path(artifacts_path).is_absolute():
        return Path(artifacts_path)
    else:
        return get_project_root() / artifacts_path

def get_docs_dir() -> Path:
    """Get documentation directory (configurable)."""
    config = load_framework_config()
    docs_path = config.get("paths", {}).get("docs", "docs")
    
    if Path(docs_path).is_absolute():
        return Path(docs_path)
    else:
        return get_project_root() / docs_path
```

### Path Resolution Order

1. **Framework Root**: Look for `AgentQMS/` directory
2. **Marker File**: Fallback to `.agentqms/` marker
3. **Project Root**: Parent of framework root
4. **Output Paths**: Resolve from config (relative to project root or absolute)

---

## Boundary Definition

### Framework Boundary Rules

**Inside `AgentQMS/`** (Framework):
- ✅ Framework code and tools
- ✅ Framework configuration
- ✅ Framework templates and schemas
- ✅ Framework documentation
- ❌ No project-specific content
- ❌ No generated artifacts
- ❌ No project code

**Outside `AgentQMS/`** (Project):
- ✅ Project code
- ✅ Generated artifacts (in configurable location)
- ✅ Project documentation (in configurable location)
- ✅ Project configuration
- ❌ No framework code
- ❌ No framework modifications

### Boundary Validation

```python
# AgentQMS/agent_tools/compliance/validate_boundaries.py

class BoundaryValidator:
    """Validate framework vs. project boundaries."""
    
    def validate_framework_boundary(self) -> ValidationResult:
        """Ensure no project content in AgentQMS/."""
        framework_root = get_framework_root()
        violations = []
        
        # Check for project-specific patterns
        project_patterns = [
            "project_config.yaml",  # Should be in project root
            "requirements.txt",     # Project dependency file
            "*.py",                 # Project code (except framework)
        ]
        
        for pattern in project_patterns:
            matches = list(framework_root.rglob(pattern))
            for match in matches:
                # Allow framework files
                if not self._is_framework_file(match):
                    violations.append(f"Project file in framework: {match}")
        
        return ValidationResult(violations=violations)
    
    def validate_project_boundary(self) -> ValidationResult:
        """Ensure no framework code outside AgentQMS/."""
        project_root = get_project_root()
        framework_root = get_framework_root()
        violations = []
        
        # Check for framework files outside AgentQMS/
        framework_markers = [
            "agent_tools/",
            "quality_management_framework/",
            "agent/Makefile",  # Framework Makefile
        ]
        
        for marker in framework_markers:
            path = project_root / marker
            if path.exists() and not path.is_relative_to(framework_root):
                violations.append(f"Framework file outside AgentQMS/: {path}")
        
        return ValidationResult(violations=violations)
```

---

## Benefits of Containerized Structure

### 1. Clear Separation
- **Before**: Framework mixed with project
- **After**: All framework in `AgentQMS/`, project content clearly separate

### 2. Easy Updates
- **Before**: Update multiple scattered directories
- **After**: Replace `AgentQMS/` directory

### 3. Version Control
- **Before**: Framework files mixed with project commits
- **After**: Framework can be versioned independently (submodule, subtree, or separate repo)

### 4. Portability
- **Before**: Framework tied to project structure
- **After**: Framework is portable unit

### 5. Maintenance
- **Before**: Hard to identify framework files
- **After**: All framework files clearly in `AgentQMS/`

### 6. Removal
- **Before**: Must identify scattered directories
- **After**: Remove `AgentQMS/` and `.agentqms/`

---

## Migration Considerations

### Backward Compatibility

**Option 1: Dual Support** (Recommended)
- Support both old and new structures during transition
- Detect structure and use appropriate paths
- Gradual migration

**Option 2: Clean Break**
- Require migration to new structure
- Simpler code, but breaking change

**Recommendation**: Option 1 for smooth transition

### Migration Path

See `07_migration_strategy.md` for detailed migration plan.

---

## Alternative Structures Considered

### Alternative 1: `.agentqms/` (Hidden)
```
project_root/
├── .agentqms/
│   ├── agent/
│   ├── agent_tools/
│   └── ...
```

**Pros**: Hidden, doesn't clutter root
**Cons**: Hidden directories can be confusing, harder to discover

**Decision**: ❌ Rejected - visibility is important

---

### Alternative 2: `framework/` (Generic)
```
project_root/
├── framework/
│   ├── agent/
│   └── ...
```

**Pros**: Generic, clear purpose
**Cons**: Too generic, could conflict with other frameworks

**Decision**: ❌ Rejected - too generic

---

### Alternative 3: `qms/` (Abbreviated)
```
project_root/
├── qms/
│   ├── agent/
│   └── ...
```

**Pros**: Short, clear
**Cons**: Less descriptive, might be unclear

**Decision**: ❌ Rejected - not descriptive enough

---

### Alternative 4: Current Structure + Marker
```
project_root/
├── agent/              # Framework
├── agent_tools/        # Framework
├── .agentqms/          # Marker only
```

**Pros**: No migration needed
**Cons**: Still scattered, doesn't solve problem

**Decision**: ❌ Rejected - doesn't achieve containerization goal

---

## Recommendations

### Recommended Structure

✅ **Use `AgentQMS/` container** with structure as defined above

**Rationale**:
- Clear framework boundary
- Easy to identify and maintain
- Portable and updatable
- Follows common conventions

### Implementation Priority

1. **Phase 1**: Design and document structure
2. **Phase 2**: Implement path resolution with dual support
3. **Phase 3**: Create migration tools
4. **Phase 4**: Migrate existing projects
5. **Phase 5**: Remove backward compatibility (optional)

---

## Next Steps

1. **Review this design** with stakeholders
2. **Create configuration schema** (see `08_configuration_schema.md`)
3. **Design boundary enforcement** (see `09_boundary_enforcement.md`)
4. **Create migration strategy** (see `07_migration_strategy.md`)
5. **Implement path resolution** with dual support

---

**See Also**:
- `07_migration_strategy.md` - How to migrate existing projects
- `08_configuration_schema.md` - Configuration file structure
- `09_boundary_enforcement.md` - Boundary validation mechanisms
- `10_naming_conventions.md` - Naming recommendations

