---
type: "rfc"
category: "configuration"
status: "draft"
version: "0.1"
tags: ["rfc", "configuration", "hierarchy"]
title: "RFT: Unified Configuration Hierarchy"
date: "2025-11-20 00:00 (KST)"
author: "Framework Maintainers"
---

# RFT: Unified Configuration Hierarchy

## 1. Summary

This RFT proposes a three-layer configuration hierarchy for AgentQMS:

1. **Framework defaults** shipped with the framework (`AgentQMS/config_defaults/`)
2. **Project overrides** stored at the workspace root (`config/`)
3. **Runtime state** (`.agentqms/`) housing merged effective config and metadata

It also recommends standardizing schema validation and clarifies the responsibilities of existing config files (e.g., `AgentQMS/agent_interface_interface/config/agent_config.yaml`).

## 2. Motivation

- Current configuration is scattered across `AgentQMS/config/`, `AgentQMS/agent_interface_interface/config/`, template files, and `.agentqms/`.  
- Tooling relies on hard-coded relative paths, making renames and exports fragile.  
- Lack of schema validation leads to subtle errors when projects customize settings.

Design background: `docs/artifacts/design_documents/2025-11-20_design_config_hierarchy.md`.

## 3. Proposal

### Directory Structure

```
workspace_root/
├── AgentQMS/
│   ├── config_defaults/
│   │   ├── framework.yaml
│   │   ├── interface.yaml
│   │   ├── paths.yaml
│   │   └── schemas/*.json
│   └── ...
├── config/
│   ├── framework.yaml
│   └── interface.yaml
└── .agentqms/
    ├── config.yaml
    └── state/
```

### Key Points

- `AgentQMS/agent_interface_interface/config/agent_config.yaml` is decomposed: defaults move to `config_defaults/`, project-specific values go to `config/` (or `.agentqms/project_config/` for framework project), runtime values to `.agentqms/effective.yaml`.
- Merged configuration logic handles precedence: `defaults ⊕ project overrides ⊕ runtime`.
- JSON Schemas stored alongside defaults validate merged outputs.

## 4. Tooling Requirements

- Add helper APIs (e.g., `get_config_defaults_dir()`, `load_effective_config()`) in `agent_tools/utils/config.py`.
- CLI and scripts must read settings via these helpers rather than relative paths.
- Provide lint/check to ensure no new configs appear outside the sanctioned directories.

## 5. Migration Plan

1. Create `config_defaults/` and move `AgentQMS/config/framework.yaml` there.
2. Extract interface defaults from `AgentQMS/agent_interface_interface/config/agent_config.yaml`.
3. Scaffold root `config/` with sample overrides.
4. Update tooling to read from helper APIs.
5. Provide migration script that:
   - Copies existing files into new layers.
   - Regenerates `.agentqms/effective.yaml`.
   - Logs operations to `.agentqms/migration.log`.
6. Deprecate `AgentQMS/agent_interface_interface/config/` (warnings, then removal).

## 6. Open Issues & Responses

1. **Project overrides location?** → Use root-level `config/` for clarity; `.agentqms/` remains runtime-only.  
2. **Schema validation?** → Normalize on JSON Schema stored in `config_defaults/schemas/`.  
3. **Environment-specific overrides?** → Deferred; note requirement in RFC for future extension.  
4. **Relative vs absolute paths?** → Keep relative paths in `paths.yaml`, resolve at runtime to preserve portability.

## 7. Impact

| Area | Impact | Mitigation |
|------|--------|------------|
| Build/CLI scripts | Need to adopt helper APIs | Provide shared utilities + lints |
| Existing installations | Require migration script | Offer dry-run + backups |
| Documentation | Needs update post-migration | Coordinate with implementation plan Phase 4 |

## 8. Timeline

- Week 1: Approve RFC, finalize helper API design.  
- Weeks 2–3: Build helpers, migrate configs, run scripts on sample repos.  
- Week 4: Enforce new structure, remove deprecated config paths.

## 9. Request for Feedback

- Are the three layers sufficient for foreseeable use cases?  
- Any objections to JSON Schema as the canonical validation mechanism?  
- Additional considerations for migration tooling?

Please comment by **2025-11-25** so we can proceed with Phase 1 of the implementation plan.

