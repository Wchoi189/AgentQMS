# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial experimental POC structure
- AgentQMS framework with modular architecture
- Quality management tools and protocols
- Documentation and handbook for agents

### Changed
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
- Duplicate `docs/audit_snapshots/v001_b/` directory (redundant copy of audit documents)

## [0.1.0] - 2025-11-09

### Added
- Project initialization
- Basic framework export functionality</content>
<parameter name="filePath">/workspaces/agent_qms/CHANGELOG.md