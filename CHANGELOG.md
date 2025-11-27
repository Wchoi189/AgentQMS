# Changelog

## 📋 Guidelines

This changelog should stay **scannable and brief**; use it as an index, not a narrative.

- **One line per change** – Use bullet points, avoid paragraphs.
- **Reference extended summaries** – Link to audits, PRs, issues, or docs for full context.
- **Group by type** – Prefer standard categories: Added, Changed, Fixed, Removed, Security.
- **Datestamps** – When needed, use `YYYY-MM-DD HH:MM (KST)` (Asia/Seoul time).
- **Version format** – Follow [Semantic Versioning](https://semver.org/): `MAJOR.MINOR.PATCH`.
- **Historical entries** – Older entries may be more verbose; new entries should follow these rules.

---

## [Unreleased]

### Added
- Initial experimental POC structure
- AgentQMS framework with modular architecture
- Quality management tools and protocols
- Documentation and handbook for agents
- Cursor IDE instructions template (`.cursor/plans/instructions.md`) plus README guidance on multi-IDE auto-discovery workflows

### Changed
- **2025-11-20**: Refactored configuration hierarchy and removed legacy support
  - Moved root-level `config/` to `.agentqms/project_config/` to avoid conflicts with consuming projects
  - Renamed runtime config from `.agentqms/config.yaml` to `.agentqms/effective.yaml` for clarity
  - Framework defaults are now in `AgentQMS/config_defaults/`
  - Project-specific configuration should be in `config/` at project root (not inside AgentQMS/)
  - Configuration hierarchy: `defaults → project overrides → effective.yaml`
  - Removed all legacy configuration paths and scattered layout support
  - Simplified codebase - only containerized structure supported
  - Updated all documentation to reflect new configuration structure

- **2025-11-09**: Restructured documentation framework for better organization
  - Moved `artifacts/` directory into `docs/artifacts/` to consolidate all documentation
  - Moved `ai_handbook/` into `docs/ai_handbook/` and retired the legacy `docs/ai_agent/` tree (now `docs/ai_handbook/04_agent_system/`)
  - Enforced frontmatter `date` timestamps using the `YYYY-MM-DD HH:MM (KST)` format across docs and validators
  - Relocated `agent_templates/` to `docs/artifacts/templates/agent_workflows/`
  - Removed duplicate `docs/audit_snapshots/` directory
  - Updated all code references and default paths to reflect new structure
  - All documentation now organized under `docs/` for clearer separation of concerns

### Fixed
- N/A

### Removed
- **2025-11-20**: Removed all legacy support to prevent chaos
  - Removed legacy fallback for `.agentqms/config.yaml`
  - Removed legacy scattered layout support
  - Removed legacy configuration warning functions
  - Removed `detect_structure()` function - only containerized layout supported
  - Framework now fails fast if structure is incorrect instead of trying legacy paths
- Duplicate `docs/audit_snapshots/v001_b/` directory (redundant copy of audit documents)

### 2025-11-26 – CI fixes and documentation improvements

#### Fixed
- **Bundle validation paths**: Fixed `validate_bundles()` in `validate_artifacts.py` to use correct paths (`AgentQMS/knowledge/context_bundles/` and `.agentqms/plugins/context_bundles/`) instead of hardcoded `docs/context_bundles/`.
- **Project root calculation**: Fixed incorrect `project_root` calculation in bundle validation (was 3 levels up from file, now uses `get_project_root()` utility).
- **Optional file handling**: Bundle files marked `optional: true` now produce warnings instead of validation errors.
- **Missing dependencies**: Added `requests>=2.28.0` and `jsonschema>=4.17.0` to `requirements.txt` for CI.

#### Added
- **AI Agent onboarding guide**: Enhanced README.md with comprehensive agent orientation:
  - Entry points table (priority-ordered files for agents to read)
  - Copy-paste ready onboarding prompt
  - Instructions for encouraging proactive QMS use in system prompts
  - Complete agent interface command reference
  - Plugin system documentation section
- **Maintainer references**: Added links to maintainer guide and framework design docs in README.

### 2025-11-25 – Plugin architecture for extensibility (Task 4.3)
- Added plugin system enabling project-level extensions without modifying framework code.
- **New schemas**: `plugin_artifact_type.json`, `plugin_validators.json`, `plugin_context_bundle.json` for validating plugin definitions.
- **New module**: `AgentQMS/agent_tools/core/plugins/` with modular architecture (discovery, validation, registry, loader, snapshot, cli).
- **Plugin discovery**: Scans `AgentQMS/conventions/plugins/` (framework) and `.agentqms/plugins/` (project).
- **Component integration**: `ArtifactTemplates`, `ArtifactValidator`, and `context_bundle.py` now load extensions from plugin registry.
- **Sample plugins**: `change_request` artifact type, validator extensions (CR_, DR_, SPEC_ prefixes), `security-review` context bundle.
- **CLI**: `python -m AgentQMS.agent_tools.core.plugins --list` to inspect registered plugins.
- **65 unit tests** covering all plugin modules.
- See `docs_deprecated/artifacts/assessments/2025-11-25_assessment_plugin_architecture_design.md` for design details.

### 2025-11-25 – Post-audit implementation plan complete
- Completed all critical, high, and medium priority tasks from the post-audit implementation plan.
- Framework is now fully functional with working CI/CD, standard packaging, and clear documentation.
- Deferred smart context loading (Task 4.2) and extensibility/multi-project support (Task 4.3) as future work requiring in-depth research.
- See `docs_deprecated/artifacts/implementation_plans/2025-11-24-IMPLEMENTATION_PLAN_post_audit_fixes.md` for full details.

### 2025-11-25 – Packaging: pyproject.toml and standard installation
- Added `pyproject.toml` for standard Python packaging (`pip install -e .`).
- Created `AgentQMS/__init__.py` with `__version__ = "0.3.0"`.
- Added shim `AgentQMS/agent_tools/core/artifact_templates.py` to expose templates via canonical import path.
- Updated deployment recommendations with package installation guidance.

### 2025-11-25 – Post-audit fixes: deprecate docs/ and align artifacts path
- Renamed `docs/` → `docs_deprecated/` to clearly mark project-history content as non-exported.
- Updated `.agentqms/settings.yaml` to use `artifacts: artifacts` (project-root-relative) and `implementation: agent_tools`.
- Removed hardcoded `docs/artifacts` defaults from `validate_artifacts.py`; validator now defaults to `artifacts/`.
- Updated CI workflow (`.github/workflows/agentqms-validation.yml`) to remove `docs/**` path triggers and point link validation at `AgentQMS/knowledge`.
- Updated `auto_generate_index.py` defaults to `AgentQMS/knowledge` instead of `docs/ai_handbook`.
- Created empty `artifacts/` directory at project root for host-project artifacts.
- Cleaned up host-specific content from agent SST (`system.md`) to align with the reusable framework model.
- Migrated key development/testing protocols to `AgentQMS/knowledge/protocols/` (coding_standards, import_handling, test_organization).
- Updated `.agentqms/state/architecture.yaml` with full knowledge domain inventory (version 2).
- Added legacy layout notes to audit framework README and tool_architecture.md.

### 2025-11-24 – Containerized framework audit and knowledge refactor
- Performed full five-phase audit (`docs_deprecated/audit/2025-11-24_audit.md`) over the containerized AgentQMS framework.
- Fixed broken agent interface workflows by aligning them with the containerized implementation layer and removing legacy `scripts/agent_tools` paths.
- Normalized audit framework docs to `AgentQMS/conventions/audit_framework/...` and updated agent-facing docs to use `AgentQMS/knowledge/...` as the primary docs root.
- Introduced `AgentQMS/knowledge/agent/*`, canonical artifact rules, bug-report schema/template, and a concise maintainer guide in `AgentQMS/knowledge/meta/MAINTAINERS.md`.
- Made `AgentQMS/agent_tools/` the canonical implementation layer (with `AgentQMS/toolkit/` as a legacy shim), migrated key governance protocols and references into `AgentQMS/knowledge/*`, and added pre-commit + CI validation flows wired to the new `agent_tools` entrypoints.

## [0.1.0] - 2025-11-09

### Added
- Project initialization
- Basic framework export functionality