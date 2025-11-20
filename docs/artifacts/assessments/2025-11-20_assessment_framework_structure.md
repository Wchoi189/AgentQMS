---
type: "assessment"
category: "framework-structure"
status: "draft"
version: "0.1"
tags: ["structure", "naming", "configuration", "audit"]
title: "Assessment: Framework Directory Structure & Naming Conflicts"
date: "2025-11-20 00:00 (KST)"
author: "Framework Maintainers"
---

# Assessment: Framework Directory Structure & Naming Conflicts

## 1. Overview

Multiple framework directories use overlapping names (`agent`, `config`, `conventions`, `ai_agent`) that are no longer self-explanatory after the audit framework additions. This assessment captures the current pain points and outlines candidate restructuring approaches before we change documentation or automate migrations.

## 2. Observed Issues

| # | Area | Symptom | Consequence |
|---|------|---------|-------------|
| 1 | `AgentQMS/agent_interface_interface/` | Directory name implies “full agent implementation,” but it only contains configs, thin wrappers, and workflows. | New contributors confuse it with `agent_tools/`; unclear where to edit configs. |
| 2 | Configuration files | `AgentQMS/config/framework.yaml` stores global config, while `AgentQMS/agent_interface_interface/config/` holds agent-specific YAML/JSON. | Scattered configuration hierarchy, hard to explain in docs; no clear rule for new config files. |
| 3 | `project_conventions/` directory | Name does not communicate its scope (project-level standards, templates, schemas). | Repeated need to clarify whether it is framework-specific or project-specific. |
| 4 | `agent_interface/tools/` vs `agent_tools/` | Nearly identical names; one holds wrappers, the other implementation. | Frequent path mistakes (`../agent_tools` vs `agent_interface/tools`), onboarding friction. |
| 5 | `docs/ai_handbook/04_agent_system/` | Directory overlaps semantically with `agent/`, `agent_tools/`, and `ai_handbook/`. | Hard to reason about which docs live where; fosters duplicate content. |

## 3. Detailed Findings & Options

### 3.1 `AgentQMS/agent_interface_interface/` Naming

- **Current Contents:** `config/`, `tools/` (wrappers), `workflows/`, `docs/`, `Makefile`.
- **Pain Point:** Name suggests core agent implementation, yet actual automation lives in `agent_tools/`.
- **Updated Direction:**
  - Wrapper/CLI code should **stay together** as an interface surface.
  - Configuration blobs should **move elsewhere** so they are not conflated with the interface.
- **Preferred Rename:** `agent_interface/`
  - Highlights its purpose: entry points, Makefile, workflows.
  - Avoids the “under-represented” feel of `agent_configs/`.
- **Structural Plan:**
  1. Relocate `agent/config/` contents into the future configuration hierarchy (see §3.2).
  2. Rename the remaining directory to `agent_interface/` and update tooling references.
  3. Keep user-facing commands accessible from repository root (symlink or short path), but maintain physical separation between interface and configs.

### 3.2 Configuration Hierarchy

- **Current State:**  
  - `AgentQMS/config/framework.yaml` – global defaults.  
  - `AgentQMS/agent_interface_interface/config/*` – agent-wrapper settings.  
  - Additional config fragments live in templates and documentation.
- **Problems:** No single “source of truth” directory; unclear where future YAML should live.
- **Candidate Structures:**
  1. **`AgentQMS/config/` as root hub** with subfolders (`framework/`, `agent/`, `project_defaults/`), referenced via path helpers.
  2. **`config/` at repo root** (peer to `AgentQMS/`) containing both framework and project overrides to emphasize separation from code.
  3. **Adopt `.agentqms/` entirely** for runtime config, keeping `AgentQMS/config/` strictly for defaults shipped with framework.
- **Needs:** Decision matrix on how CLI discovers precedence (framework defaults → agent interface overrides → project-specific `.agentqms/`).

### 3.3 `project_conventions/` Renaming

- **Feedback:** “Conventions” sounds optional; directory actually contains project-level standards, schemas, tooling.
- **Proposal:** Rename to `project_conventions/` to clarify intent (project scaffolding + reusable standards).
- **Considerations:**  
  - Update imports, documentation, and tool references (`tool_architecture.md`, template loaders).  
  - Provide migration script to move directory when exporting framework.

### 3.4 `agent_interface/tools/` vs `agent_tools/`

- **Observations:**
  - `agent_interface/tools/` = thin Python wrappers (entry points for agents/humans).  
  - `agent_tools/` = core automation packages.
- **Risks:** Similar names; mistake leads to executing wrong script (or import errors).
- **Options:**
  1. Rename `agent_interface/tools/` → `agent_wrappers/` (or `agent_cli/`).
  2. Restructure so wrappers live inside `agent/Makefile` or `agent_scripts/`.
  3. Consolidate wrappers into `agent_scripts/` and deprecate `agent_interface/tools/`.
- **Dependencies to Audit:** Makefile targets, `tool_mappings.json`, docs referencing `agent_interface/tools`.

### 3.5 `docs/ai_handbook/04_agent_system/`

- **Issue:** Directory name overlaps with `agent`, `agent_tools`, and `ai_handbook`.
- **Symptoms:** Hard to know whether guidance belongs in `docs/ai_handbook/04_agent_system/` vs `docs/ai_handbook/`.
- **Decision:** Adopt idea 1 – merge `docs/ai_handbook/04_agent_system/` into `docs/ai_handbook/` under a dedicated “Agent System” section.
- **Migration Notes:**
  - Create a new subsection within the handbook to house the existing `ai_agent` content.
  - Leave a stub/redirect file temporarily so existing links do not break.

## 4. Cross-Cutting Concerns

- **Migration Effort:** Renaming top-level directories (`agent/`, `project_conventions/`) impacts imports, tooling paths, make targets, documentation.
- **Backward Compatibility:** Need shims or helpful errors for existing scripts referencing old paths.
- **Documentation Debt:** Once structure stabilizes, documentation + diagrams must be regenerated; delaying docs right now avoids churn.
- **Tooling Support:** Path helpers (`agent_tools/utils/runtime.py`, CLI wrappers) should expose canonical getters so future renames require minimal code changes.

## 5. Next Steps (Proposal)

1. **Finalize Naming Decisions (Week 1)**
   - Confirm `agent_interface/` rename scope (files, imports, symlinks).
   - Approve `project_conventions/` rename and identify tooling impacts.
   - Sign off on merging `docs/ai_handbook/04_agent_system/` into `docs/ai_handbook/`.

2. **Design Config Hierarchy (Week 1-2)**
   - Draft RFC describing layers: framework defaults, interface overrides, project overrides (`.agentqms/`).
   - Decide physical location (`AgentQMS/config/` vs repo root `config/` vs `.agentqms/`).
   - Define precedence/merge rules used by CLI and tooling.

3. **Implement Directory Renames (Week 2)**
   - Scripted rename of `agent/` → `agent_interface/` after configs extracted.
   - Scripted rename of `project_conventions/` → `project_conventions/`.
   - Provide compatibility shims/logging to catch old paths.

4. **Configuration Migration (Week 2-3)**
   - Move `AgentQMS/agent_interface_interface/config/` contents into new hierarchy.
   - Update Makefile/tool references (`tool_mappings.json`, path helpers).
   - Add automated checks ensuring configs live only in approved directories.

5. **Docs Folder Consolidation (Week 3)**
   - Move `docs/ai_handbook/04_agent_system/` into `docs/ai_handbook/03_agent_system/`.
   - Leave redirect README to warn about new location until references updated.

6. **Tooling Updates (Week 3-4)**
   - Expand `agent_tools/utils/runtime.py` with getters (`get_agent_interface_dir()`, `get_project_conventions_dir()`, etc.).
   - Update CLI wrappers to rely on getters rather than hard-coded paths.
   - Enhance validation scripts to detect stale paths/directories.

7. **Documentation Sprint (After Structural Changes)**
   - Refresh READMEs, diagrams, and onboarding materials once structure is stable.
   - Document config hierarchy, migration steps, and new directory map.

> **Note:** Documentation updates are intentionally deferred per request until we finalize the structural plan.

---

**Pending Decisions:**  
- Preferred new names for `agent/` and `project_conventions/`.  
- Single location for shipped configs vs runtime configs.  
- Whether to consolidate documentation directories (`docs/ai_handbook/04_agent_system/`, `ai_handbook/`).

**Prepared By:** Framework Maintainers  
**Review Needed:** Core team alignment on naming + config strategy.

