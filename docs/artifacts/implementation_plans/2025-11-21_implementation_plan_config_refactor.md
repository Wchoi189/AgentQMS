---
type: "implementation_plan"
category: "configuration"
status: "completed"
version: "0.1"
tags: ["configuration", "refactoring", "architecture"]
title: "Implementation Plan: Configuration Architecture Refactor"
date: "2025-11-21 04:35 (KST)"
author: "Project Maintainers"
---

# Implementation Plan: Configuration Architecture Refactor

## Objective

Simplify the configuration architecture by moving project config from hidden `.agentqms/project_config/` to visible `config/` directory, making it easier to find and edit project-specific settings.

## Problem

The previous architecture was confusing:
- **Hidden config**: `.agentqms/project_config/` was hard to find
- **Dual locations**: Code checked both `config/` and `.agentqms/project_config/`
- **Mixed responsibilities**: `.agentqms/` contained both user-editable config and runtime state
- **Complex logic**: Unclear precedence and fallback behavior

## Solution

**Simple Two-Layer Architecture:**

```
workspace_root/
├── config/                    # Project overrides (visible, user-editable)
│   ├── framework.yaml
│   ├── interface.yaml
│   ├── paths.yaml
│   ├── environments/
│   └── overrides/
├── config_defaults/           # Framework defaults (shipped, read-only)
│   ├── framework.yaml
│   ├── interface.yaml
│   ├── paths.yaml
│   └── tool_mappings.json
└── .agentqms/                 # Runtime state ONLY (generated, hidden)
    ├── effective.yaml         # Generated merged config
    └── state/                 # Runtime state
```

## Implementation Steps

### ✅ Completed

1. **Created `config/` directory** at project root
2. **Moved `.agentqms/project_config/*` → `config/`**
3. **Removed `.agentqms/project_config/` directory**
4. **Updated config loader** to only check `config/` (removed fallback logic)
5. **Created `config/README.md`** with documentation
6. **Updated `.gitignore`** to properly ignore runtime state

### Code Changes

**`agent_tools/utils/config.py`:**
- Simplified `_load_project_overrides()` method
- Removed fallback to `.agentqms/project_config/`
- Added clear documentation about configuration precedence
- Updated effective.yaml generation to note new structure

## Configuration Precedence

```
1. config_defaults/*.yaml          (Framework defaults - lowest priority)
2. config/*.yaml                   (Project overrides - medium priority)
3. config/environments/*.yaml       (Environment-specific - higher priority)
4. config/overrides/*.yaml          (Additional overrides - highest priority)
5. Environment variables            (Runtime overrides - highest priority)
6. .agentqms/effective.yaml         (Generated merged result - read-only)
```

## Benefits

- ✅ **Clearer**: Single visible location for project config
- ✅ **Simpler**: No hidden directories for user-editable files
- ✅ **Easier**: Developers can easily find and edit config
- ✅ **Cleaner**: Runtime state separate from configuration
- ✅ **Maintainable**: Less complex merge logic

## Migration Notes

- All files from `.agentqms/project_config/` have been moved to `config/`
- Old location no longer used
- Config loader automatically uses new location
- No breaking changes for existing projects (they can create `config/` if needed)

## Verification

- [x] Config files moved successfully
- [x] Old directory removed
- [x] Config loader updated
- [x] Documentation created
- [x] .gitignore updated

## Related Documents

- `docs/artifacts/assessments/2025-11-21_assessment_config_architecture.md` - Problem assessment
- `config/README.md` - User guide for configuration

