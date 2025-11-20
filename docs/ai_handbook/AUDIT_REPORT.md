# AI Handbook Audit Report

**Date**: 2025-11-20
**Purpose**: Identify and prune project-specific artifacts from framework documentation

---

## Summary

The `docs/ai_handbook/` directory contains a mix of:
- ✅ **Framework-agnostic content** (generic protocols, standards, patterns)
- ❌ **Project-specific artifacts** (Korean Grammar Correction project, Streamlit app specifics)

This audit identifies which files should be **pruned** as they clutter the framework with project-specific implementation details.

---

## Files to PRUNE (Project-Specific)

### 🔴 High Priority - Clearly Project-Specific

#### `01_onboarding/` - Entire directory
- **`01_onboarding/01_project_overview.md`**
  - ❌ About "Korean Grammar Correction Project"
  - ❌ References `prompts.py`, `grammar_correction_utils.py`, `streamlit_app/`
  - ❌ Project-specific objectives and scope
  
- **`01_onboarding/quick-context-reference.md`**
  - ❌ Contains project-specific quick reference

**Action**: Remove entire `01_onboarding/` directory (project-specific onboarding)

---

#### `index.md` - Main handbook index
- ❌ Title: "AI Agent Handbook: Korean Grammar Correction Project"
- ❌ References project-specific files: `prompts.py`, `evaluate.py`, `streamlit_app/`
- ❌ Project-specific structure and tasks
- ❌ Links to project-specific artifacts in `../../artifacts/`

**Action**: Should be replaced with a framework-agnostic template

---

#### `03_references/development/` - Project-specific fixes

- **`03_references/development/ai_agent_context.md`**
  - ❌ "Korean Grammar Correction Streamlit project"
  - ❌ Streamlit app-specific import issues
  - ❌ Project-specific debugging methods
  
- **`03_references/development/schema_configuration_fix.md`**
  - ❌ Streamlit schema-driven page fixes
  - ❌ Project-specific error patterns
  - ❌ References `streamlit_app/page_schemas/`
  
- **`03_references/development/path_utils_migration_quickstart.md`**
  - ❌ References `streamlit_app/utils/path_utils.py`
  - ❌ Project-specific path resolution patterns
  
- **`03_references/development/utility_functions.md`**
  - ❌ About `streamlit_app/utils/path_utils.py`
  - ❌ Project-specific utility catalog
  - ❌ References `streamlit_app/config/`

**Action**: Remove all four files (project-specific development references)

---

#### `03_references/development/module_schema_reference.md`
- ⚠️ **Borderline**: Starts with "Korean GEC project" but content is generic
- ⚠️ Contains generic module schema patterns that could be useful
- **Action**: Review - either prune if too project-specific, or abstract to remove project references

---

#### `03_references/architecture-summary.md`
- ⚠️ **Need to check**: May contain project-specific architecture
- **Action**: Review content

---

#### `04_agent_system/coding_protocols/streamlit.md`
- ❌ Project-specific Streamlit coding protocol
- ❌ References `streamlit_app/page_schemas/`
- ❌ Project-specific file organization

**Action**: Remove (project-specific protocol, not framework-agnostic)

---

#### `05_changelog/` - Entire directory
- ❌ Project-specific changelog entries
- ❌ `2025-10/27_pydantic_v2_ai_instructions_update.md` - Project-specific
- ❌ `2025-10/27_modularity_principles_improvement.md` - Project-specific

**Action**: Remove entire `05_changelog/` directory (project changelogs don't belong in framework)

---

### 🟡 Medium Priority - Review Needed

#### `04_agent_system/tracking/`
- ⚠️ **Need to check**: May be framework-agnostic tracking system
- **Action**: Review to see if tracking is framework feature or project-specific

---

#### `templates/implementation_plan_instructions.md`
- ⚠️ **Need to check**: May contain project-specific references
- **Action**: Review for project-specific content

---

## Files to KEEP (Framework-Agnostic)

### ✅ Definitely Keep - Generic Protocols

#### `02_protocols/` - Entire directory structure
- ✅ `02_protocols/governance/` - Generic governance protocols
  - `01_artifact_management_protocol.md` - Generic artifact management
  - `02_implementation_plan_protocol.md` - Generic implementation planning
  - `03_blueprint_protocol_template.md` - Generic blueprint template
  - `04_bug_fix_protocol.md` - Generic bug fix protocol

- ✅ `02_protocols/development/` - Generic development protocols
  - `01_coding_standards_v2.md` - Generic coding standards
  - `22_proactive_modularity_protocol.md` - Generic modularity protocol
  - `23_import_handling_protocol.md` - Generic import handling
  - `code_generation_quality_protocol.md` - Generic quality protocol
  - `context-templates.md` - Generic context templates

- ✅ `02_protocols/testing/` - Generic testing protocols
  - `test_organization_protocol.md` - Generic test organization

- ✅ `02_protocols/templates/` - Generic templates
  - `prompts-artifact-guidelines.md` - Generic artifact guidelines

---

#### `03_references/development/` - Framework references

- ✅ `03_references/development/modularity_quick_reference.md`
  - Framework-agnostic modularity patterns
  
- ✅ `03_references/development/import_handling_reference.md`
  - Framework-agnostic import patterns
  
- ✅ `03_references/development/loader_path_resolution.md`
  - Framework feature for loader registry path resolution

---

#### `03_references/context_optimization/`

- ✅ `03_references/context_optimization/smart-context-loading.md`
  - Framework-agnostic context optimization

---

#### `04_agent_system/` - Core framework documentation

- ✅ `04_agent_system/system.md`
  - Core framework system documentation
  
- ✅ `04_agent_system/index.md`
  - Framework system index
  
- ✅ `04_agent_system/automation/`
  - `tooling_overview.md` - Framework automation overview
  - `tool_catalog.md` - Framework tool catalog
  - `changelog_process.md` - Framework changelog process

---

#### `configuration_guidelines.md`
- ✅ Framework configuration guidelines

---

## Recommended Actions

### Phase 1: Immediate Pruning (High Priority)
1. Delete `01_onboarding/` directory (entire)
2. Delete `05_changelog/` directory (entire)
3. Delete `04_agent_system/coding_protocols/streamlit.md`
4. Delete from `03_references/development/`:
   - `ai_agent_context.md`
   - `schema_configuration_fix.md`
   - `path_utils_migration_quickstart.md`
   - `utility_functions.md`

### Phase 2: Review and Abstract (Medium Priority)
1. Review `index.md` - create framework-agnostic template
2. Review `03_references/development/module_schema_reference.md` - abstract if needed
3. Review `03_references/architecture-summary.md` - check for project-specific content
4. Review `04_agent_system/tracking/` - determine if framework or project feature
5. Review `templates/implementation_plan_instructions.md` - check for project references

### Phase 3: Template Creation
1. Create framework-agnostic `index.md` template
2. Create framework-agnostic onboarding template (if needed)
3. Update all remaining files to remove any project-specific references

---

## Impact Assessment

**Files to Remove**: ~8-10 files
**Directories to Remove**: 2 (`01_onboarding/`, `05_changelog/`)

**Files Needing Review**: 4-5 files

**Expected Result**: Cleaner, more focused framework documentation that doesn't confuse users with project-specific artifacts.

---

## Notes

- The framework should be **completely agnostic** to what projects use it
- Project-specific implementations should live in consuming projects, not in the framework
- The handbook should focus on **framework usage patterns**, not project-specific details
- When in doubt, **prune** - it's better to have less documentation that's accurate than more that's confusing

