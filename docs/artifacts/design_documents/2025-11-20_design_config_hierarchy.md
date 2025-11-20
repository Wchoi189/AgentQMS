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

## 2. Proposed Hierarchy

```
workspace_root/
├── AgentQMS/
│   ├── config_defaults/            # Replaces current AgentQMS/config/
│   │   ├── framework.yaml          # Framework-level defaults
│   │   ├── interface.yaml          # Defaults for agent interface
│   │   └── paths.yaml              # Shipped canonical paths
│   ├── agent_interface/            # (future rename of agent/) - no configs inside
│   ├── agent_tools/
│   └── project_conventions/        # (future rename of project_conventions/)
├── config/                         # Project-level overrides (new, optional)
│   ├── framework.yaml              # Project tweaks to defaults
│   └── interface.yaml              # Project-specific interface settings
└── .agentqms/                      # Runtime state + generated config
    ├── config.yaml                 # Effective merged config (generated)
    └── state/...
```

### Layers & Precedence

1. **Defaults (`AgentQMS/config_defaults/`)**  
   - Version-controlled with the framework.  
   - Provide baseline values used when no overrides exist.

2. **Project Overrides (`config/` at repo root)**  
   - Optional directory maintained by the consuming project.  
   - Overrides defaults to reflect project-specific paths, naming, or policies.  
   - Safe to commit to the project repo.

3. **Runtime (`.agentqms/`)**  
   - Generated/managed files (install metadata, last-run state).  
   - Writing final merged config + state used by tooling.  
   - Should not be manually edited; typically gitignored.

The effective configuration used by tooling is:  
`merged_config = defaults ⊕ project_overrides ⊕ runtime_state`

---

## 3. File Breakdown

| Layer | File | Purpose | Managed By |
|-------|------|---------|------------|
| Defaults | `AgentQMS/config_defaults/framework.yaml` | Canonical framework metadata, path names | Framework maintainers |
| Defaults | `AgentQMS/config_defaults/interface.yaml` | Interface-specific defaults (e.g., workflows auto-run) | Framework maintainers |
| Defaults | `AgentQMS/config_defaults/paths.yaml` | Canonical directory names used by tooling | Framework maintainers |
| Project | `config/framework.yaml` | Adjust framework-level defaults for a project | Project team |
| Project | `config/interface.yaml` | Turn interface features on/off per project | Project team |
| Runtime | `.agentqms/config.yaml` | Generated merged config (read-mostly) | Tooling |
| Runtime | `.agentqms/state/*` | Execution metadata, migration logs | Tooling |

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

## 5. Agent Scripts vs Agent Tools Overlap

- **Observation:** `AgentQMS/agent_scripts/` currently mixes orchestration glue and partial business logic, often mirroring code in `agent_tools/`.
- **Problems:**
  - Duplicate scripts (e.g., validation or documentation helpers) live in both directories with different relative paths.
  - Config references in `agent_scripts/` drift from the canonical implementation, creating path mismatches.
  - Contributors struggle to know whether to patch `agent_scripts/` or `agent_tools/`.
- **Design Principles:**
  1. **Interface Layer Only:** `agent_interface/` (future rename of `agent/`) plus `agent_scripts/` should contain wrappers, CLI entry points, and install automation—not core logic.
  2. **Implementation Layer:** All functional logic (validation, generation, automation) must live in `agent_tools/` and be consumed via APIs/helpers.
- **Action Plan:**
  - During migration, inventory scripts inside `agent_scripts/` and categorize them as:
    - **Wrappers:** Keep in interface layer but refactor to call `agent_tools` functions.
    - **Logic:** Relocate into `agent_tools/` modules and leave a thin wrapper (or remove the script if redundant).
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

