# Removal Candidate List

**Date**: 2025-11-09  
**Audit Scope**: Quality Management Framework Cleanup  
**Status**: Critical Issues Identified

## Executive Summary

This document identifies project-specific artifacts, broken dependencies, and unnecessary components that must be removed or refactored to make the framework reusable across projects.

---

## 🔴 CRITICAL: Broken Dependencies (Must Fix)

### 1. Missing Bootstrap Module
**Location**: Referenced in `agent_tools/core/artifact_workflow.py`, `agent_tools/compliance/validate_artifacts.py`, `agent_tools/utilities/get_context.py`

**Issue**: All core tools call `_load_bootstrap()` expecting `scripts/_bootstrap.py`, but this file doesn't exist.

**Impact**: 
- Artifact creation fails immediately
- Validation cannot run
- Context bundling is broken
- **Framework is non-functional**

**Action**: 
- **Option A**: Create minimal bootstrap module with path resolution utilities
- **Option B**: Remove bootstrap dependency and use explicit relative imports + `sys.path` helper
- **Recommendation**: Option B (eliminate dependency)

**Files Affected**:
- `agent_tools/core/artifact_workflow.py` (lines 24-46)
- `agent_tools/compliance/validate_artifacts.py` (lines 23-46)
- `agent_tools/utilities/get_context.py` (similar pattern)
- `scripts/utilities/process_manager.py` (lines 25-45)

---

### 2. Missing `streamlit_app` Module Dependency
**Location**: `agent_interface/tools/*.py`, multiple documentation files

**Issue**: 54+ files import `streamlit_app.utils.path_utils` but `streamlit_app/` directory doesn't exist in framework export.

**Impact**:
- All agent wrapper tools fail (`discover.py`, `quality.py`, `feedback.py`, `ast_analysis.py`)
- MCP adapters (puppeteer, audio) cannot start
- Documentation references broken patterns

**Action**: 
- Extract path utilities into framework (`agent_tools/utils/path_utils.py`)
- Update all imports to use framework path utils
- Remove `streamlit_app` references from documentation

**Files Requiring Updates**:
- `agent_interface/tools/discover.py` (line 20)
- `agent_interface/tools/quality.py` (line 20)
- `agent_interface/tools/feedback.py` (line 20)
- `agent_interface/tools/ast_analysis.py` (line 22)
- `agent_interface/tools/puppeteer/agent_puppeteer_mcp.py` (line 14)
- `agent_interface/tools/audio/agent_audio_mcp.py` (line 15)
- `agent_tools/utilities/tracking/db.py` (line 11)
- All files in `ai_handbook/03_references/development/` (multiple)

---

### 3. Path Mismatch: `scripts/agent_tools` vs `agent_tools`
**Location**: `agent/Makefile`, `agent/workflows/*.sh`, documentation

**Issue**: Makefile and wrappers call `../scripts/agent_tools/...` but implementation lives in `agent_tools/` (root level).

**Impact**:
- Every `make` command fails with "No such file or directory"
- Agent interface is completely unusable
- Workflow scripts broken

**Action**: 
- Update all `../scripts/agent_tools/` references to `../agent_tools/`
- Update `agent_tools/core/discover.py` help text (line 36)
- Fix all documentation references

**Files Requiring Updates**:
- `agent/Makefile` (28 references: lines 28, 36, 46, 49, 52, 55, 58, 61, 65, 68, 71, 74, 84, 87, 90, 93, 96, 99, 107, 110, 113, 116, 119, 122, 179, 194, 197, 199, etc.)
- `agent/workflows/create-artifact.sh` (line 21)
- `docs/resources.md` (multiple references)
- `docs/export_guide.md` (multiple references)
- `docs/quick_start_export.md` (multiple references)

---

## 🟡 HIGH PRIORITY: Project-Specific Content

### 4. Korean Grammar Correction Project References
**Location**: Multiple files throughout codebase

**Issue**: 125+ references to "Korean Grammar Correction", "Upstage", "Solar Pro", "prompt-a-thon" project.

**Impact**: 
- Framework appears project-specific
- Confusing for new adopters
- Hardcoded project names in templates

**Action**: Replace with placeholders or remove entirely.

**Files to Clean**:
- `ai_handbook/index.md` (entire file - project-specific)
- `ai_handbook/01_onboarding/01_project_overview.md` (entire file)
- `ai_handbook/configuration_guidelines.md` (lines 77-97)
- `scripts/utilities/process_manager.py` (entire file - project-specific)
- `scripts/utilities/path_utils.py` (line 2 - project description)
- `scripts/adapt_project.py` (lines 36-42 - hardcoded project names)
- `agent_tools/utilities/adapt_project.py` (lines 36-42 - hardcoded project names)
- `agent_interface/tools/semantic_search/setup_agent_search.py` (line 95)
- All artifact examples in `agent/docs/artifacts/`

**Strategy**: 
- Create template versions with `{{PROJECT_NAME}}` placeholders
- Use `adapt_project.py` to replace during setup
- Remove hardcoded examples

---

### 5. Hardcoded Project Paths
**Location**: `agent_interface/tools/puppeteer/`, `agent_interface/tools/audio/`, artifact examples

**Issue**: Absolute paths like `/workspaces/upstage-prompt-hack-a-thon-dev` hardcoded in configs and examples.

**Impact**: 
- Tools fail in new environments
- Examples don't work
- Configuration requires manual editing

**Action**: 
- Replace with relative paths or environment variables
- Use `get_path_resolver()` for path resolution
- Update all README examples

**Files**:
- `agent_interface/tools/puppeteer/README.md` (lines 29, 32, 40, 150, 153)
- `agent_interface/tools/puppeteer/QUICK_SETUP.md` (lines 30, 33, 40)
- `agent_interface/tools/audio/README.md` (lines 29, 32, 40)
- `scripts/utilities/play_audio.sh` (line 4)
- Artifact examples with hardcoded paths

---

## 🟠 MEDIUM PRIORITY: Structural Issues

### 6. Duplicate Makefile Targets
**Location**: `agent/Makefile`

**Issue**: `context-list` defined twice (lines 121 and 178) with different implementations.

**Impact**: 
- Confusing behavior
- One target may be stale
- Silent failures

**Action**: Consolidate into single target, remove duplicate.

---

### 7. Deprecated Directory References
**Location**: `agent_tools/core/discover.py` (lines 42-48)

**Issue**: Code checks for `_deprecated/` directory that doesn't exist, but references it in help text.

**Impact**: 
- Misleading information
- Dead code

**Action**: Remove deprecated directory checks, or create it with README explaining deprecation policy.

---

### 8. Missing Dependency Declarations
**Location**: Root directory

**Issue**: No `requirements.txt`, `pyproject.toml`, or `setup.py` to declare dependencies.

**Impact**: 
- Users don't know what to install
- Version conflicts possible
- Framework may break with dependency updates

**Action**: Create `requirements.txt` or `pyproject.toml` with minimal dependencies:
- `pyyaml` (for YAML parsing)
- `jinja2` (for templating)
- `jsonschema` (for schema validation)

---

### 9. Stale Generated Indexes
**Location**: `agent_templates/INDEX.md`, other generated indexes

**Issue**: Generated indexes may contain truncated metadata or outdated information.

**Impact**: 
- Misleading documentation
- Broken links
- Stale information

**Action**: 
- Regenerate all indexes after fixing import paths
- Add validation to ensure indexes are current
- Add CI check for stale indexes

---

## 🟢 LOW PRIORITY: Cleanup Opportunities

### 10. Verbose Documentation
**Location**: `ai_handbook/`, `docs/`

**Issue**: Some documentation is overly verbose with redundant explanations.

**Impact**: 
- Harder to maintain
- Slower for agents to parse
- Information overload

**Action**: 
- Streamline protocols to essential information
- Remove redundant examples
- Use concise, action-oriented language

**Files to Review**:
- `ai_handbook/02_protocols/` (some protocols are very long)
- `docs/export_guide.md` (800+ lines, could be more concise)

---

### 11. Monolithic Validator
**Location**: `agent_tools/compliance/validate_artifacts.py` (~560 lines)

**Issue**: Single large file with hand-rolled YAML parsing, duplicated config, mixed concerns.

**Impact**: 
- High maintenance cost
- Hard to test
- Logic scattered across validation, workflow, docs

**Action**: Split into modules:
- `naming.py` - Naming convention validation
- `frontmatter.py` - Frontmatter schema validation
- `bundles.py` - Context bundle validation
- `config.py` - Shared configuration loading

**Note**: Lower priority - works but needs refactoring for maintainability.

---

### 12. Hardcoded Handbook Schema
**Location**: `agent_tools/documentation/auto_generate_index.py`

**Issue**: Directory taxonomy baked into code, duplicated in handbook docs.

**Impact**: 
- Schema changes require code updates in multiple places
- Drift between code and docs

**Action**: Extract to `docs/config/handbook.yaml` and have generator read it.

---

## 📋 Removal Summary

| Priority | Category | Files Affected | Effort | Impact |
|----------|----------|----------------|--------|--------|
| 🔴 Critical | Bootstrap dependency | 4 files | High | Framework non-functional |
| 🔴 Critical | streamlit_app dependency | 54+ files | High | All agent tools broken |
| 🔴 Critical | Path mismatches | 10+ files | Medium | Makefile unusable |
| 🟡 High | Project-specific content | 125+ references | Medium | Framework not reusable |
| 🟡 High | Hardcoded paths | 10+ files | Low | Tools fail in new envs |
| 🟠 Medium | Duplicate targets | 1 file | Low | Confusion |
| 🟠 Medium | Missing deps | Root | Low | Setup unclear |
| 🟠 Medium | Stale indexes | Multiple | Low | Misleading docs |
| 🟢 Low | Verbose docs | Multiple | Medium | Maintenance burden |
| 🟢 Low | Monolithic validator | 1 file | High | Technical debt |
| 🟢 Low | Hardcoded schema | 1 file | Medium | Drift risk |

---

## Implementation Priority

1. **Phase 1 (Critical - Blocking)**: Fix broken dependencies (#1, #2, #3)
2. **Phase 2 (High - Reusability)**: Remove project-specific content (#4, #5)
3. **Phase 3 (Medium - Quality)**: Fix structural issues (#6, #7, #8, #9)
4. **Phase 4 (Low - Optimization)**: Cleanup and refactoring (#10, #11, #12)

---

**Next Steps**: See `02_workflow_analysis.md` for workflow mapping and `03_restructure_proposal.md` for detailed implementation plan.

