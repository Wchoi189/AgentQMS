---
type: "design_document"
category: "configuration"
status: "draft"
version: "0.1"
tags: ["configuration", "hierarchy", "paths", "refactor"]
title: "Design: Unified Configuration Hierarchy for AgentQMS"
date: "2025-11-20 00:00 (KST)"
author: "Framework Maintainers"
---

# Design: Unified Configuration Hierarchy for AgentQMS

## 1. Goals & Constraints

**Goals**
- Provide a clear configuration hierarchy that separates shipped defaults, interface-specific settings, and project/runtime overrides.
- Remove ambiguity between `AgentQMS/config/`, `AgentQMS/agent_interface_interface/config/`, and `.agentqms/config.yaml`.
- Enable tooling to discover paths/config without hard-coded relative references.

**Constraints**
- Preserve backwards compatibility through shims until migrations are complete.
- Keep user-facing commands simple (`make ...` should still work from repo root).
- Support export/install flows (copying `AgentQMS/` into another project must include the right config defaults).

---

## 2. Actual Hierarchy (Current)

```
workspace_root/
├── AgentQMS/
│   ├── interface/                  # Agent-only interface (Makefile, CLI wrappers, workflows)
│   ├── toolkit/                    # Implementation layer (Python packages, tools)
│   ├── conventions/                # QMS templates, schemas, manifests
│   ├── scripts/                    # Framework scripts and maintenance utilities
│   └── templates/                  # Bootstrap/export templates (if any)
├── config/                         # (Optional) Project-level overrides in consuming projects
│   ├── framework.yaml              # Project tweaks to defaults
│   └── interface.yaml              # Project-specific interface settings
└── .agentqms/                      # Runtime + primary configuration
    ├── settings.yaml               # Authoritative project/framework config
    ├── effective.yaml              # Generated merged config (read-mostly)
    └── state/...
```

### Layers & Precedence

1. **Project Configuration (`.agentqms/settings.yaml`)**  
   - Version-controlled with the framework in this repo.  
   - Acts as the single source of truth for paths, framework metadata, interface settings, and tool mappings.

2. **Optional Project Overrides (`config/` at repo root)**  
   - Only present in consuming projects that import AgentQMS as a framework.  
   - Overrides defaults from `settings.yaml` to reflect project-specific paths, naming, or policies.  
   - Safe to commit to the consuming project repo.

3. **Runtime Snapshot (`.agentqms/effective.yaml`)**  
   - Generated/managed file (install metadata, last-run state).  
   - Captures the resolved configuration used by tooling (after environment overrides).  
   - Should not be manually edited; typically gitignored.

The effective configuration used by tooling is:  
`merged_config = settings.yaml ⊕ (optional project config/) ⊕ environment_overrides`

---

## 3. File Breakdown

| Layer   | File                          | Purpose                                       | Managed By          |
|---------|-------------------------------|-----------------------------------------------|---------------------|
| Project | `.agentqms/settings.yaml`     | Canonical framework + interface + paths config| Framework maintainers |
| Project | `config/framework.yaml`       | Adjust framework-level defaults for a project | Project team        |
| Project | `config/interface.yaml`       | Turn interface features on/off per project    | Project team        |
| Runtime | `.agentqms/effective.yaml`    | Generated merged config (read-mostly)         | Tooling             |
| Runtime | `.agentqms/state/*`           | Execution metadata, migration logs            | Tooling             |

---

## 4. Access Patterns

Introduce helper functions in `agent_tools/utils/runtime.py` (or new `config.py`) to avoid ad-hoc path math:

```python
from AgentQMS.agent_tools.utils.config import get_config_defaults_dir, load_effective_config

defaults = load_yaml(get_config_defaults_dir() / "framework.yaml")
effective = load_effective_config()
```

**Helper Responsibilities**
- Discover workspace root (existing logic).
- Locate `AgentQMS/config_defaults/`.
- Detect project overrides (`workspace_root/config/`).
- Merge YAML with clear precedence and schema validation.
- Cache merged config (write to `.agentqms/config.yaml`).

---

## 5. Scripts vs Toolkit Overlap

- **Observation:** `AgentQMS/scripts/` currently mixes orchestration glue and partial business logic, often mirroring code in the toolkit.
- **Problems:**
  - Duplicate scripts (e.g., validation or documentation helpers) live in both directories with different relative paths.
  - Config references in `scripts/` drift from the canonical implementation, creating path mismatches.
  - Contributors struggle to know whether to patch `scripts/` or the toolkit.
- **Design Principles:**
  1. **Interface Layer Only:** `interface/` plus `scripts/` should contain wrappers, CLI entry points, and install automation—not core logic.
  2. **Implementation Layer:** All functional logic (validation, generation, automation) must live in `toolkit/` and be consumed via APIs/helpers.
- **Action Plan:**
  - During migration, inventory scripts inside `scripts/` and categorize them as:
    - **Wrappers:** Keep in interface layer but refactor to call `toolkit` functions.
    - **Logic:** Relocate into `toolkit/` modules and leave a thin wrapper (or remove the script if redundant).
  - Update config hierarchy RFC to document the responsibility split and ensure future tooling additions follow this pattern.

---

## 6. Migration Strategy (High-Level)

1. **Create `config_defaults/`** inside `AgentQMS/` and move `AgentQMS/config/framework.yaml` there.  
2. **Extract interface defaults** from `AgentQMS/agent_interface_interface/config/agent_config.yaml` into `config_defaults/interface.yaml`.  
3. **Introduce root-level `config/` directory** (empty by default) to encourage project overrides.  
4. **Update tooling** to read from helper functions and stop referencing `agent/config`.  
5. **Write migration script** that:
   - Copies existing `AgentQMS/agent_interface_interface/config/*` into either `config_defaults/` (framework-managed) or `config/` (project-managed) depending on file type.
   - Updates `.agentqms/config.yaml` structure.
6. **Deprecate `AgentQMS/agent_interface_interface/config/`** with a clear error message directing users to the new hierarchy.

---

## 7. Open Questions (with preliminary answers)

1. **Where should project overrides live?**  
   - **Decision:** Store project overrides under a dedicated `config/` directory at the workspace root for clarity.  
   - `.agentqms/overrides/` remains runtime-only.  
   - **Implication:** `AgentQMS/agent_interface_interface/config/agent_config.yaml` no longer holds long-term overrides—its contents will be redistributed: interface defaults to `config_defaults/interface.yaml`, project customization to `config/interface.yaml`, and runtime state to `.agentqms/config.yaml`.

2. **Schema validation approach (JSON Schema vs YAML schema tooling)?**  
   - Historically we mixed ad-hoc YAML parsing with JSON Schema fragments, leading to “dual architecture.”  
   - **Decision:** Normalize on JSON Schema definitions stored alongside the defaults (e.g., `config_defaults/schemas/*.json`) and validate all merged YAML against these schemas. This deprecates bespoke YAML validation helpers.

3. **Environment-specific overrides (`config/dev/framework.yaml` etc.)?**  
   - Recognized need, but implementing now would double file count and slow the migration.  
   - **Decision:** Defer; note requirement in RFC for future extension (e.g., allow optional `config/<env>/` directories resolved via env var).

4. **Should `paths.yaml` use relative or absolute paths?**  
   - **Decision:** Keep relative paths; tooling will resolve them relative to workspace root at runtime.  
   - **Trade-offs:** Relative paths avoid embedding machine-specific locations and keep repos portable; tooling must ensure resolution happens after merges to avoid ambiguity.

---

## 8. Next Actions

1. Write formal RFC capturing this hierarchy + open questions.  
2. Prototype config loader/merger in `agent_tools/utils/config.py`.  
3. Draft migration script that moves existing files into the new structure.  
4. Update assessment & implementation plan once hierarchy is approved.  
5. Schedule documentation update after migration.

---

**Status:** Draft for review. Requesting comments on directory names, override precedence, and helper API before implementation.

