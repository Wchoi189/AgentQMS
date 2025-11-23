---
type: "implementation_plan"
category: "framework-cleanup"
status: "active"
version: "0.1"
tags: ["cleanup", "structure", "consolidation"]
title: "Implementation Plan: Framework Cleanup and Consolidation"
date: "2025-11-21 03:30 (KST)"
author: "Project Maintainers"
---

# Implementation Plan: Framework Cleanup and Consolidation

## Objective

Clean up the AgentQMS framework by removing duplicates, consolidating structure, removing unnecessary archives, and addressing the nested AgentQMS/ folder structure issue.

## Current Problems

1. **Nested agent_tools**: `AgentQMS/agent_scripts/agent_tools/` contains only empty `__pycache__` directories
2. **Archive folder**: `AgentQMS/_archive/` contains 382KB of archived content that may not be needed
3. **Duplicate utilities**: Both `utils/` and `utilities/` directories exist
4. **Java code in main branch**: Java toolchain should be in separate branch
5. **Framework folder naming**: Framework folder is named `AgentQMS/` which creates confusion with project root

## Cleanup Actions

### Phase 1: Remove Nested Duplicates (Immediate)

1. **Remove nested agent_tools**
   - Delete `AgentQMS/agent_scripts/agent_tools/` (only contains __pycache__)
   - Verified: No code references this nested directory

2. **Clean agent_scripts/utilities**
   - Check if `AgentQMS/agent_scripts/utilities/` has any actual files
   - If only __pycache__, remove it
   - If empty or minimal, consider removing entire `agent_scripts/` directory if not needed

### Phase 2: Archive Cleanup

3. **Review and remove archive content**
   - `AgentQMS/_archive/` contains:
     - `python_legacy/` - Archived Python code (21 Python files)
     - `rebuild-tracker/` - Legacy rebuild tracker (not needed)
     - `alternative-architecture.md` - Alternative design (archive or remove)
   - **Decision**: Keep `python_legacy/` for reference but remove other content
   - Remove `rebuild-tracker/` (unrelated legacy project)
   - Remove `alternative-architecture.md` (outdated design)

### Phase 3: Consolidate Utilities

4. **Consolidate utils/ and utilities/**
   - Current state:
     - `AgentQMS/agent_tools/utils/` - Core utilities (paths.py, config.py, runtime.py)
     - `AgentQMS/agent_tools/utilities/` - Application utilities (view_logs.py, get_context.py, etc.)
   - **Decision**: Keep both but document distinction clearly
   - OR: Merge into single `utils/` directory
   - **Recommendation**: Keep separate but add README explaining distinction

### Phase 4: Java Branch Migration Note

5. **Document Java branch requirement**
   - Create note in README about Java code belonging in separate branch
   - Add to .gitignore if Java code accidentally appears in main

### Phase 5: Framework Naming (Future Consideration)

6. **Address AgentQMS/ folder naming**
   - Current: Framework folder is `AgentQMS/` inside project root
   - Issue: Creates confusion with project structure
   - **Future consideration**: Rename to `framework/` or `qms_framework/`
   - **Note**: This is a larger refactor - document for future work

## Implementation Steps

### Step 1: Remove Nested Directories
```bash
# Remove nested agent_tools (only __pycache__)
rm -rf AgentQMS/agent_scripts/agent_tools/

# Check and clean agent_scripts/utilities
# If empty or only __pycache__, remove it
```

### Step 2: Clean Archive
```bash
# Remove rebuild-tracker (legacy project, not related)
rm -rf AgentQMS/_archive/rebuild-tracker/

# Remove alternative architecture doc
rm AgentQMS/_archive/alternative-architecture.md

# Keep python_legacy/ for reference
```

### Step 3: Add Documentation
- Add README to `agent_tools/utils/` explaining it's for core framework utilities
- Add README to `agent_tools/utilities/` explaining it's for application utilities
- Update main README with Java branch note

### Step 4: Update References
- Verify no broken imports after cleanup
- Update any documentation referencing removed paths

## Expected Outcomes

- **Reduced size**: Remove ~200-300KB of unnecessary archive content
- **Clearer structure**: No nested duplicates, clearer directory purposes
- **Easier navigation**: Less confusion about where code lives
- **Maintainability**: Cleaner codebase easier to maintain

## Risks & Mitigations

- **Risk**: Removing archive might lose reference material
  - **Mitigation**: Keep `python_legacy/` for reference, only remove unrelated content

- **Risk**: Breaking imports if we consolidate utils/
  - **Mitigation**: Keep both directories, just document distinction clearly

- **Risk**: Missing references to removed directories
  - **Mitigation**: Search codebase before removal, verify no references

## Success Criteria

- [ ] Nested `agent_scripts/agent_tools/` removed
- [ ] Archive cleaned (rebuild-tracker and alternative-architecture removed)
- [ ] Utils directories documented
- [ ] Java branch migration documented
- [ ] No broken imports or references
- [ ] Framework size reduced
- [ ] Structure clearer and easier to navigate

