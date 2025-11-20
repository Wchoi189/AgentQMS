# Restructure Proposal

**Date**: 2025-11-09  
**Audit Scope**: Framework Restructure Plan  
**Status**: Implementation Roadmap

## Executive Summary

This document proposes a comprehensive restructure of the Quality Management Framework to achieve systematic organization, scalability, automation, and robustness. The proposal is organized by implementation priority with clear success criteria.

---

## Restructure Principles

1. **Zero External Dependencies**: Framework must work standalone
2. **Self-Enforcing Standards**: Validation prevents violations
3. **Minimal Configuration**: Sensible defaults, easy customization
4. **Clear Error Messages**: Fail fast with actionable guidance
5. **Extensible Design**: Easy to add new artifact types, validators, tools

---

## Phase 1: Critical Fixes (Blocking Issues)

**Timeline**: Immediate  
**Priority**: 🔴 Critical  
**Goal**: Make framework functional

### 1.1 Fix Path Resolution

**Problem**: Three different path patterns, no single source of truth.

**Solution**:
```python
# agent_tools/utils/paths.py (NEW)
"""Centralized path resolution for framework."""

from pathlib import Path
from typing import Optional

def get_project_root() -> Path:
    """Find project root by looking for marker files."""
    current = Path(__file__).resolve()
    markers = ['.git', 'agent', 'agent_tools', 'quality_management_framework']
    
    for parent in [current] + list(current.parents):
        if any((parent / marker).exists() for marker in markers):
            return parent
    
    raise RuntimeError("Could not locate project root")

def get_agent_tools_dir() -> Path:
    """Get agent_tools directory."""
    root = get_project_root()
    tools_dir = root / "agent_tools"
    if tools_dir.exists():
        return tools_dir
    raise RuntimeError(f"agent_tools directory not found in {root}")

def get_framework_dir() -> Path:
    """Get quality_management_framework directory."""
    root = get_project_root()
    framework_dir = root / "quality_management_framework"
    if framework_dir.exists():
        return framework_dir
    raise RuntimeError(f"quality_management_framework directory not found in {root}")
```

**Actions**:
- [ ] Create `agent_tools/utils/paths.py`
- [ ] Update all tools to use `get_project_root()` instead of hardcoded paths
- [ ] Update Makefile to use relative paths from `agent/` directory
- [ ] Remove all `../scripts/agent_tools/` references
- [ ] Test path resolution in various directory contexts

**Success Criteria**:
- All tools can find required directories
- Works when run from any subdirectory
- Clear error messages if paths not found

---

### 1.2 Eliminate Bootstrap Dependency

**Problem**: All tools require non-existent `scripts/_bootstrap.py`.

**Solution**: Remove bootstrap entirely, use direct imports.

**Actions**:
- [ ] Remove `_load_bootstrap()` from all files
- [ ] Replace `setup_project_paths()` calls with direct path resolution
- [ ] Update imports to use relative imports within `agent_tools/`
- [ ] Remove bootstrap-related code from `scripts/utilities/process_manager.py`

**Files to Update**:
- `agent_tools/core/artifact_workflow.py` (remove lines 24-48)
- `agent_tools/compliance/validate_artifacts.py` (remove lines 23-46)
- `agent_tools/utilities/get_context.py` (similar pattern)
- `scripts/utilities/process_manager.py` (lines 25-45)

**Success Criteria**:
- No references to `scripts._bootstrap` in codebase
- All tools import successfully
- No runtime errors from missing bootstrap

---

### 1.3 Extract Path Utilities

**Problem**: 54+ files depend on `streamlit_app.utils.path_utils` that doesn't exist.

**Solution**: Extract path utilities to framework.

**Actions**:
- [ ] Create `agent_tools/utils/path_utils.py` with essential functions:
  ```python
  def setup_project_paths() -> None:
      """Add project root to sys.path."""
      root = get_project_root()
      if str(root) not in sys.path:
          sys.path.insert(0, str(root))
  
  def get_path_resolver():
      """Get path resolver for project paths."""
      # Minimal implementation, no external dependencies
      ...
  ```
- [ ] Update all imports from `streamlit_app.utils.path_utils` to `agent_tools.utils.path_utils`
- [ ] Update documentation examples
- [ ] Remove `streamlit_app` references from codebase

**Files to Update**:
- All files in `agent_interface/tools/` (5 files)
- `agent_tools/utilities/tracking/db.py`
- All files in `ai_handbook/03_references/development/` (multiple)
- Documentation files

**Success Criteria**:
- Zero references to `streamlit_app` in framework code
- All imports resolve correctly
- Path utilities work standalone

---

### 1.4 Fix Makefile Paths

**Problem**: Makefile references `../scripts/agent_tools/` but should be `../agent_tools/`.

**Solution**: Update all path references.

**Actions**:
- [ ] Replace all `../scripts/agent_tools/` with `../agent_tools/` in Makefile
- [ ] Update `agent/workflows/*.sh` scripts
- [ ] Test all Makefile targets
- [ ] Update help text in `agent_tools/core/discover.py`

**Success Criteria**:
- All `make` commands execute successfully
- No "file not found" errors
- Help text shows correct paths

---

## Phase 2: Project-Specific Cleanup

**Timeline**: After Phase 1  
**Priority**: 🟡 High  
**Goal**: Make framework reusable

### 2.1 Remove Project-Specific Content

**Problem**: 125+ references to "Korean Grammar Correction", "Upstage", etc.

**Solution**: Template-based approach with placeholders.

**Actions**:
- [ ] Create template versions of project-specific files:
  - `ai_handbook/index.md.template`
  - `ai_handbook/01_onboarding/01_project_overview.md.template`
  - `scripts/adapt_project.py` (already exists, enhance it)
- [ ] Replace hardcoded project names with `{{PROJECT_NAME}}` placeholders
- [ ] Update `adapt_project.py` to replace placeholders during setup
- [ ] Remove or template project-specific utility files:
  - `scripts/utilities/process_manager.py` (project-specific, remove or template)
  - `scripts/utilities/path_utils.py` (update description)

**Success Criteria**:
- Zero hardcoded project names in framework code
- Templates work with `adapt_project.py`
- New projects can be set up without manual edits

---

### 2.2 Fix Hardcoded Paths

**Problem**: Absolute paths like `/workspaces/upstage-prompt-hack-a-thon-dev` in configs.

**Solution**: Use relative paths and environment variables.

**Actions**:
- [ ] Update `agent_interface/tools/puppeteer/README.md` to use relative paths
- [ ] Update `agent_interface/tools/audio/README.md` to use relative paths
- [ ] Update `scripts/utilities/play_audio.sh` to use environment variables
- [ ] Replace hardcoded paths in artifact examples with placeholders
- [ ] Update all README examples

**Success Criteria**:
- No absolute paths in framework code
- Examples work in any project
- Documentation shows correct patterns

---

## Phase 3: Structural Improvements

**Timeline**: After Phase 2  
**Priority**: 🟠 Medium  
**Goal**: Improve maintainability and scalability

### 3.1 Consolidate Makefile

**Problem**: 371 lines, duplicate targets, verbose help.

**Solution**: Simplify and consolidate.

**Actions**:
- [ ] Remove duplicate `context-list` target (keep one)
- [ ] Extract common path variables:
  ```makefile
  AGENT_TOOLS := ../agent_tools
  FRAMEWORK := ../quality_management_framework
  ```
- [ ] Consolidate similar targets
- [ ] Simplify help text (remove emojis, be concise)
- [ ] Add prerequisite validation

**Success Criteria**:
- Makefile < 200 lines
- No duplicate targets
- Clear, concise help
- All targets work

---

### 3.2 Split Monolithic Validator

**Problem**: 560-line validator with mixed concerns.

**Solution**: Modular design.

**Actions**:
- [ ] Create `agent_tools/compliance/naming.py`:
  ```python
  class NamingValidator:
      def validate_prefix(self, filename: str) -> bool:
          ...
      def validate_format(self, filename: str) -> bool:
          ...
  ```
- [ ] Create `agent_tools/compliance/frontmatter.py`:
  ```python
  class FrontmatterValidator:
      def validate_schema(self, frontmatter: dict) -> bool:
          ...
      def validate_required_fields(self, frontmatter: dict) -> bool:
          ...
  ```
- [ ] Create `agent_tools/compliance/bundles.py`:
  ```python
  class BundleValidator:
      def validate_bundle(self, bundle_name: str) -> bool:
          ...
  ```
- [ ] Create `agent_tools/compliance/config.py`:
  ```python
  def load_validation_config() -> dict:
      """Load validation rules from YAML."""
      ...
  ```
- [ ] Refactor `validate_artifacts.py` to use modules

**Success Criteria**:
- Each module < 200 lines
- Clear separation of concerns
- Easy to test individually
- Same functionality as before

---

### 3.3 Extract Schema Configuration

**Problem**: Schema hardcoded in generator, duplicated in docs.

**Solution**: Centralized schema files.

**Actions**:
- [ ] Create `quality_management_framework/config/` directory
- [ ] Create `artifact_schema.yaml`:
  ```yaml
  artifact_types:
    implementation_plan:
      prefix: "implementation_plan_"
      directory: "implementation_plans/"
      required_fields: [title, date, status, version]
    assessment:
      prefix: "assessment-"
      directory: "assessments/"
      required_fields: [title, date, status]
  ```
- [ ] Create `directory_structure.yaml`:
  ```yaml
  handbook_structure:
    - onboarding/
    - protocols/
    - references/
    - changelog/
  ```
- [ ] Update `auto_generate_index.py` to read from YAML
- [ ] Update documentation to reference schema files

**Success Criteria**:
- Schema in YAML, not code
- Single source of truth
- Generator reads from config
- Docs reference config files

---

### 3.4 Create Dependency Manifest

**Problem**: No `requirements.txt` or `pyproject.toml`.

**Solution**: Minimal dependency declaration.

**Actions**:
- [ ] Create `requirements.txt`:
  ```
  pyyaml>=6.0
  jinja2>=3.1.0
  jsonschema>=4.17.0
  ```
- [ ] Or create `pyproject.toml`:
  ```toml
  [project]
  name = "agent-qms"
  version = "0.1.0"
  dependencies = [
      "pyyaml>=6.0",
      "jinja2>=3.1.0",
      "jsonschema>=4.17.0",
  ]
  ```
- [ ] Document installation in README

**Success Criteria**:
- Dependencies clearly declared
- Installation works with `pip install -r requirements.txt`
- Version constraints specified

---

## Phase 4: Optimization & Enhancement

**Timeline**: After Phase 3  
**Priority**: 🟢 Low  
**Goal**: Improve efficiency and user experience

### 4.1 Streamline Documentation

**Problem**: Verbose protocols, redundant examples.

**Solution**: Concise, action-oriented documentation.

**Actions**:
- [ ] Review `ai_handbook/02_protocols/` for verbosity
- [ ] Remove redundant examples
- [ ] Use bullet points instead of paragraphs where possible
- [ ] Focus on "what to do" not "why" (move why to separate docs)
- [ ] Reduce `docs/export_guide.md` from 800+ lines to < 400

**Success Criteria**:
- Protocols < 200 lines each
- Clear, scannable format
- Essential information only

---

### 4.2 Optimize Index Generation

**Problem**: Regenerates everything, slow for large projects.

**Solution**: Incremental updates with caching.

**Actions**:
- [ ] Add metadata cache (JSON file with file hashes)
- [ ] Only regenerate changed files
- [ ] Parallel processing for large directories
- [ ] Progress indicators

**Success Criteria**:
- 10x faster for large projects
- Only updates changed files
- Clear progress feedback

---

### 4.3 Create Unified CLI

**Problem**: Makefile complexity, multiple entry points.

**Solution**: Single Python CLI tool.

**Actions**:
- [ ] Create `agent/qms.py`:
  ```python
  #!/usr/bin/env python3
  """Unified QMS CLI."""
  import click
  
  @click.group()
  def cli():
      """Quality Management Framework CLI."""
      pass
  
  @cli.command()
  def create(type, name, title):
      """Create artifact."""
      ...
  
  @cli.command()
  def validate(target):
      """Validate artifacts."""
      ...
  ```
- [ ] Make executable: `chmod +x agent/qms.py`
- [ ] Update documentation to use `python agent/qms.py` instead of `make`
- [ ] Keep Makefile as convenience wrapper

**Success Criteria**:
- Single entry point
- Clear help system
- Works without Make
- Backward compatible (Makefile still works)

---

## Implementation Priority Matrix

| Phase | Tasks | Effort | Impact | Dependencies |
|-------|-------|--------|--------|--------------|
| 1.1 | Fix Path Resolution | Medium | Critical | None |
| 1.2 | Eliminate Bootstrap | Low | Critical | 1.1 |
| 1.3 | Extract Path Utils | Medium | Critical | 1.1 |
| 1.4 | Fix Makefile Paths | Low | Critical | 1.1 |
| 2.1 | Remove Project Content | Medium | High | 1.x |
| 2.2 | Fix Hardcoded Paths | Low | High | 1.x |
| 3.1 | Consolidate Makefile | Low | Medium | 1.x |
| 3.2 | Split Validator | High | Medium | 1.x |
| 3.3 | Extract Schema | Medium | Medium | 1.x |
| 3.4 | Dependency Manifest | Low | Medium | None |
| 4.1 | Streamline Docs | Medium | Low | 2.x |
| 4.2 | Optimize Indexing | High | Low | 3.x |
| 4.3 | Unified CLI | Medium | Low | 1.x |

---

## Success Metrics

### Phase 1 Success Criteria
- ✅ All `make` commands execute without errors
- ✅ Artifact creation workflow completes end-to-end
- ✅ Zero missing dependency errors
- ✅ Works in fresh project setup

### Phase 2 Success Criteria
- ✅ Framework installs in new project without manual edits
- ✅ Zero hardcoded project names
- ✅ `adapt_project.py` successfully configures framework

### Phase 3 Success Criteria
- ✅ Makefile < 200 lines
- ✅ Validator split into < 200 line modules
- ✅ Schema in YAML config files
- ✅ Dependencies declared in `requirements.txt`

### Phase 4 Success Criteria
- ✅ Documentation 50% more concise
- ✅ Index generation 10x faster
- ✅ Unified CLI available
- ✅ User satisfaction improved

---

## Risk Mitigation

### Risk 1: Breaking Existing Workflows
**Mitigation**: 
- Keep Makefile as wrapper during transition
- Maintain backward compatibility
- Gradual migration path

### Risk 2: Path Resolution Edge Cases
**Mitigation**:
- Comprehensive testing in various directory contexts
- Clear error messages
- Fallback mechanisms

### Risk 3: Schema Migration Complexity
**Mitigation**:
- Version schema files
- Migration scripts if needed
- Clear documentation

---

## Next Steps

1. **Immediate**: Start Phase 1.1 (Path Resolution)
2. **Week 1**: Complete Phase 1 (Critical Fixes)
3. **Week 2**: Complete Phase 2 (Project Cleanup)
4. **Week 3**: Complete Phase 3 (Structural Improvements)
5. **Week 4**: Complete Phase 4 (Optimization)

See `04_standards_specification.md` for detailed standards and `05_automation_recommendations.md` for maintenance automation.

