---
type: "assessment"
category: "framework-structure"
status: "active"
version: "0.1"
tags: ["structure", "refactoring", "extraction"]
title: "Assessment: Nested AgentQMS Folder Extraction"
date: "2025-11-21 04:00 (KST)"
author: "Project Maintainers"
---

# Assessment: Nested AgentQMS Folder Extraction

## Summary

Successfully extracted all contents from the nested `AgentQMS/` folder to the project root and removed the empty folder. This eliminates the confusing nested structure where the framework folder had the same name as the project.

## Actions Completed

### ✅ Directory Extraction

1. **Moved directories to project root:**
   - `AgentQMS/_archive` → `_archive`
   - `AgentQMS/agent_interface` → `agent_interface`
   - `AgentQMS/agent_tools` → `agent_tools`
   - `AgentQMS/config_defaults` → `config_defaults`
   - `AgentQMS/project_conventions` → `project_conventions`
   - `AgentQMS/templates` → `templates`
   - `AgentQMS/java-tools` → `java-tools` (note: should be in separate branch)

2. **Moved README files:**
   - `AgentQMS/README_JAVA_BRANCH.md` → `README_JAVA_BRANCH.md`
   - `AgentQMS/README_JAVA_MIGRATION.md` → `README_JAVA_MIGRATION.md`

3. **Removed empty folder:**
   - `AgentQMS/` folder removed after extraction

### ✅ Path Reference Updates

4. **Updated Python configuration loader:**
   - `agent_tools/utils/config.py` - Changed framework root detection to look for `config_defaults` directory instead of `AgentQMS` folder
   - Updated `_detect_framework_root()` to detect by directory structure
   - Updated `_detect_project_root()` - framework root is now project root
   - Updated effective.yaml generation paths

5. **Updated Java PathResolver:**
   - `java-tools/core/src/main/java/com/agentqms/core/PathResolver.java`
   - Deprecated `agentQmsRoot()` method (returns repoRoot now)
   - Updated `conventionsRoot()` to use `repoRoot` directly
   - Updated documentation comments

6. **Updated Python tool references:**
   - `agent_tools/core/discover.py` - Removed `AgentQMS/` prefix from paths
   - `agent_tools/utils/migration.py` - Updated path mappings
   - `agent_tools/migration/migrate.py` - Updated config_defaults path
   - `agent_tools/documentation/regenerate_docs.py` - Updated script paths
   - `agent_tools/audit/README.md` - Updated all example paths

7. **Updated configuration files:**
   - `.agentqms/project_config/paths.yaml` - Removed `AgentQMS/` prefix from config_defaults path

## Before and After

### Before Structure
```
/workspaces/agent_qms/
├── AgentQMS/              # Nested framework folder
│   ├── _archive/
│   ├── agent_interface/
│   ├── agent_tools/
│   ├── config_defaults/
│   ├── project_conventions/
│   ├── templates/
│   └── java-tools/
├── docs/
└── ...
```

### After Structure
```
/workspaces/agent_qms/
├── _archive/              # Extracted to root
├── agent_interface/       # Extracted to root
├── agent_tools/           # Extracted to root
├── config_defaults/       # Extracted to root
├── project_conventions/   # Extracted to root
├── templates/             # Extracted to root
├── java-tools/            # Extracted to root (should be in branch)
├── docs/
└── ...
```

## Impact

### Benefits
- ✅ **Eliminated nested structure confusion** - No more `AgentQMS/AgentQMS/` ambiguity
- ✅ **Clearer project structure** - Framework components at project root level
- ✅ **Simpler path resolution** - Framework root is now project root
- ✅ **Easier navigation** - All framework directories directly accessible

### Changes Required
- ✅ **Path detection updated** - Framework root detection now uses directory structure
- ✅ **All references updated** - Code and config files updated to new structure
- ✅ **Documentation updated** - README files and examples updated

## Verification

- [x] All directories extracted successfully
- [x] Empty AgentQMS/ folder removed
- [x] Python config loader updated
- [x] Java PathResolver updated
- [x] All Python tool references updated
- [x] Configuration files updated
- [x] No broken imports (verified)

## Notes

- **Java code**: `java-tools/` is now at project root but should be moved to a separate branch
- **Framework root detection**: Now looks for `config_defaults/` and `agent_tools/` directories instead of `AgentQMS/` folder name
- **Backward compatibility**: Old code looking for `AgentQMS/` folder will fail gracefully with clear error messages

## Related Documents

- `docs/artifacts/assessments/2025-11-21_assessment_cleanup_summary.md` - Previous cleanup work
- `docs/artifacts/assessments/2025-11-21_assessment_project_structure_issues.md` - Original problem assessment

