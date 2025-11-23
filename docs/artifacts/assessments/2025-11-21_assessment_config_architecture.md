---
type: "assessment"
category: "configuration"
status: "active"
version: "0.1"
tags: ["configuration", "architecture", "refactoring"]
title: "Assessment: Configuration Architecture Issues"
date: "2025-11-21 04:30 (KST)"
author: "Project Maintainers"
---

# Assessment: Configuration Architecture Issues

## Current Problems

### 1. Confusing Directory Structure

**Current Setup:**
```
workspace_root/
├── config_defaults/          # Framework defaults (visible)
│   ├── framework.yaml
│   ├── interface.yaml
│   ├── paths.yaml
│   └── tool_mappings.json
└── .agentqms/                 # Runtime state (hidden)
    ├── project_config/        # Project overrides (HIDDEN - confusing!)
    │   ├── framework.yaml
    │   ├── interface.yaml
    │   ├── paths.yaml
    │   ├── environments/
    │   └── overrides/
    ├── effective.yaml         # Generated merged config
    └── state/                 # Runtime state
```

### 2. Key Issues

1. **Hidden Project Config**: `.agentqms/project_config/` is hidden and hard to find
   - Users don't know where to edit project-specific settings
   - Hidden directories are not intuitive
   - Makes configuration management difficult

2. **Dual Location Logic**: Code checks both `config/` and `.agentqms/project_config/`
   - Complex fallback logic
   - Unclear which location is authoritative
   - Confusing for developers

3. **Mixed Responsibilities**: `.agentqms/` contains both:
   - User-editable config (project_config/)
   - Generated runtime state (effective.yaml, state/)
   - Should be separated

4. **Unclear Naming**:
   - `config_defaults/` - Framework defaults (OK)
   - `project_config/` - Project overrides (confusing location)
   - `config/` - Alternative project config (unused in framework project)

5. **Complex Merge Logic**: 
   - Checks `config/` first, then falls back to `.agentqms/project_config/`
   - Unclear precedence
   - Hard to debug

## Proposed Better Architecture

### Option 1: Simple Two-Layer (Recommended)

```
workspace_root/
├── config/                    # Project overrides (visible, user-editable)
│   ├── framework.yaml         # Project-specific framework settings
│   ├── interface.yaml         # Project-specific interface settings
│   ├── paths.yaml             # Project-specific paths
│   ├── environments/          # Environment-specific overrides
│   └── overrides/             # Additional overrides
├── config_defaults/           # Framework defaults (shipped, read-only)
│   ├── framework.yaml
│   ├── interface.yaml
│   ├── paths.yaml
│   └── tool_mappings.json
└── .agentqms/                 # Runtime state ONLY (generated, hidden)
    ├── effective.yaml         # Generated merged config
    └── state/                 # Runtime state
```

**Benefits:**
- ✅ Single visible location for project config (`config/`)
- ✅ Clear separation: defaults vs overrides vs runtime
- ✅ No hidden user-editable files
- ✅ Simple merge: `defaults → config/ → .agentqms/effective.yaml`
- ✅ Easy to find and edit project settings

**Migration:**
- Move `.agentqms/project_config/*` → `config/`
- Remove `.agentqms/project_config/` directory
- Update config loader to only check `config/`

### Option 2: Unified Config Directory

```
workspace_root/
├── config/
│   ├── defaults/              # Framework defaults (shipped)
│   │   ├── framework.yaml
│   │   ├── interface.yaml
│   │   └── paths.yaml
│   ├── project/               # Project overrides (user-editable)
│   │   ├── framework.yaml
│   │   ├── interface.yaml
│   │   └── paths.yaml
│   └── environments/          # Environment overrides
└── .agentqms/                 # Runtime state only
    ├── effective.yaml
    └── state/
```

**Benefits:**
- ✅ All config in one place
- ✅ Clear hierarchy within single directory
- ✅ Easy to understand structure

**Drawbacks:**
- ⚠️ Mixes shipped defaults with user config
- ⚠️ Harder to distinguish what's framework vs project

### Option 3: Keep Defaults, Simplify Project Config

```
workspace_root/
├── config_defaults/           # Framework defaults (keep as-is)
├── config/                    # Project overrides (single location)
└── .agentqms/                 # Runtime state only
```

**Benefits:**
- ✅ Minimal changes
- ✅ Clear separation
- ✅ Simple to understand

## Recommendation

**✅ Option 1: Simple Two-Layer Architecture**

### Rationale

1. **Visibility**: All user-editable config in visible `config/` directory
2. **Simplicity**: Two clear layers (defaults + overrides)
3. **Clarity**: Runtime state separate from configuration
4. **Maintainability**: Easy to find, edit, and version control project config
5. **Migration**: Straightforward - just move files

### Implementation Steps

1. **Create `config/` directory** at project root
2. **Move `.agentqms/project_config/*` → `config/`**
3. **Update config loader** to only check `config/` (remove `.agentqms/project_config/` fallback)
4. **Remove `.agentqms/project_config/`** directory
5. **Update documentation** to reflect new structure
6. **Add `.agentqms/` to .gitignore** (runtime state only)

### Configuration Precedence

```
1. config_defaults/*.yaml          (Framework defaults - lowest priority)
2. config/*.yaml                   (Project overrides - medium priority)
3. config/environments/*.yaml       (Environment-specific - higher priority)
4. config/overrides/*.yaml          (Additional overrides - highest priority)
5. Environment variables            (Runtime overrides - highest priority)
6. .agentqms/effective.yaml         (Generated merged result - read-only)
```

## Impact

### Files to Move
- `.agentqms/project_config/framework.yaml` → `config/framework.yaml`
- `.agentqms/project_config/interface.yaml` → `config/interface.yaml`
- `.agentqms/project_config/paths.yaml` → `config/paths.yaml`
- `.agentqms/project_config/environments/` → `config/environments/`
- `.agentqms/project_config/overrides/` → `config/overrides/`

### Code Changes
- `agent_tools/utils/config.py` - Simplify `_load_project_overrides()` to only check `config/`
- Remove fallback to `.agentqms/project_config/`
- Update path resolution logic

### Documentation Updates
- Update README files
- Update configuration guides
- Update design documents

## Benefits Summary

- ✅ **Clearer**: Single visible location for project config
- ✅ **Simpler**: No hidden directories for user-editable files
- ✅ **Easier**: Developers can easily find and edit config
- ✅ **Cleaner**: Runtime state separate from configuration
- ✅ **Maintainable**: Less complex merge logic

