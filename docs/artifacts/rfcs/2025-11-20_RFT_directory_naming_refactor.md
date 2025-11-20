---
type: "rfc"
category: "framework-structure"
status: "draft"
version: "0.1"
tags: ["rfc", "naming", "structure"]
title: "RFT: Directory Naming & Documentation Consolidation"
date: "2025-11-20 00:00 (KST)"
author: "Framework Maintainers"
---

# RFT: Directory Naming & Documentation Consolidation

## 1. Summary

We propose to realign several top-level directories to better reflect their responsibilities:

- `AgentQMS/agent_interface_interface/` → `AgentQMS/agent_interface_interface/`
- `AgentQMS/project_conventions/` → `AgentQMS/project_conventions/`
- Merge `docs/ai_handbook/04_agent_system/` into `docs/ai_handbook/` under a new “Agent System” section
- Clarify the relationship between `agent_scripts/` and `agent_tools/`, ensuring only interface wrappers remain in the former

This RFT describes the motivation, scope, and migration considerations prior to implementation.

## 2. Background & Motivation

Recent audit work surfaced overlapping directory names (`agent`, `agent_tools`, `conventions`, `ai_agent`) that cause onboarding friction and path errors. The audit assessment (see `2025-11-20_assessment_framework_structure.md`) and implementation plan (`2025-11-20_IMPLEMENTATION_PLAN_framework_structure_refactor.md`) recommend resolving these conflicts before documentation updates.

## 3. Problem Statement

- `AgentQMS/agent_interface_interface/` currently contains configs, Makefiles, wrapper scripts, and docs—its name implies the entire agent implementation, which actually resides in `agent_tools/`.
- `AgentQMS/project_conventions/` houses project-level standards/templates but sounds optional.
- `docs/ai_handbook/04_agent_system/` duplicates content from `docs/ai_handbook/` and conflicts with other “agent” directories.
- `agent_scripts/` vs `agent_tools/` have overlapping logic; contributors are unsure where to modify behavior.

## 4. Proposed Changes

1. **Rename `AgentQMS/agent_interface_interface/` to `AgentQMS/agent_interface_interface/`**
   - Keep only CLI wrappers, Makefile, workflows, and documentation relevant to the interface.
   - Move configuration files elsewhere per the configuration RFC.

2. **Rename `AgentQMS/project_conventions/` to `AgentQMS/project_conventions/`**
   - Update template loaders, path helpers, and documentation references.
   - Provide shims (e.g., symlinks or warning scripts) during transition.

3. **Merge `docs/ai_handbook/04_agent_system/` into `docs/ai_handbook/`**
   - Create a dedicated “Agent System” section.
   - Leave a stub README in the old directory pointing to the new location until references are updated.

4. **Clarify `agent_scripts/` Role**
   - Audit scripts currently under `agent_scripts/`.
   - Move any implementation logic into `agent_tools/`.
   - Document the distinction (interface wrappers vs implementation).

## 5. Alternatives Considered

- Keep existing names and rely on documentation → rejected; confusion persists.
- Merge `agent_tools/` into `agent/` → rejected; breaks separation of interface vs implementation.
- Delete `docs/ai_handbook/04_agent_system/` without consolidation → rejected; loses content without giving it a home.

## 6. Impact & Migration

| Area | Impact | Mitigation |
|------|--------|------------|
| Tooling / imports | Update path helpers, Makefile, scripts, template loaders | Provide compatibility shims and lints |
| Documentation | Numerous references to old names | Defer final documentation updates until structure stabilized |
| Integrations | Export scripts referencing `project_conventions/` | Provide migration script to rename directories |
| Contributors | Local checkouts may need manual `git mv` | Document steps in migration guide |

## 7. Open Questions

1. Should we maintain short-lived symlinks from old names to new names during migration?  
2. Do we enforce the new naming via CI (e.g., forbid committing to `AgentQMS/agent_interface_interface/`)?  
3. How long should the `docs/ai_handbook/04_agent_system/` stub remain before removal?

## 8. Timeline (aligned with implementation plan)

- **Week 1:** Approve RFT, finalize naming decisions.
- **Weeks 2–3:** Execute renames + script migrations, keeping shims in place.
- **Week 4:** Update documentation/handbook references and remove shims.

## 9. Request for Feedback

- Are the proposed names (`agent_interface/`, `project_conventions/`) acceptable?
- Any concerns with merging `docs/ai_handbook/04_agent_system/` into the handbook?
- Additional dependencies or tooling that must be considered before renames?

Please provide feedback by **2025-11-25** so we can start Phase 1 of the implementation plan.

