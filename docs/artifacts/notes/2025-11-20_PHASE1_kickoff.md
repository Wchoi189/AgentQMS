---
type: "note"
category: "framework-structure"
status: "draft"
tags: ["phase1", "kickoff", "structure-refactor"]
title: "Phase 1 Kickoff Notes: Framework Structure Refactor"
date: "2025-11-20"
author: "Framework Maintainers"
---

# Phase 1 Kickoff Notes

## Objectives
- Secure approval for the directory naming refactor (`agent_interface/`, `project_conventions/`, docs merge).
- Secure approval for the unified configuration hierarchy (three-layer model).
- Capture outstanding questions and assign owners prior to migrations.

## Inputs
- [`2025-11-20_RFT_directory_naming_refactor.md`](../rfcs/2025-11-20_RFT_directory_naming_refactor.md)
- [`2025-11-20_RFT_configuration_hierarchy.md`](../rfcs/2025-11-20_RFT_configuration_hierarchy.md)
- [`2025-11-20_design_config_hierarchy.md`](../design_documents/2025-11-20_design_config_hierarchy.md)
- Implementation plan: [`2025-11-20_IMPLEMENTATION_PLAN_framework_structure_refactor.md`](../implementation_plans/2025-11-20_IMPLEMENTATION_PLAN_framework_structure_refactor.md)

## Decision Checklist
| Decision | RFT Reference | Owner | Status | Notes |
|----------|---------------|-------|--------|-------|
| Rename `agent/` → `agent_interface/` | Directory Naming RFT §4.1 | Framework Leads | ✅ Completed | Approved 2025-11-20 (see kickoff log) |
| Rename `conventions/` → `project_conventions/` | Directory Naming RFT §4.2 | Framework Leads | ✅ Completed | Included in rename rollout plan |
| Merge `docs/ai_agent/` into handbook | Directory Naming RFT §4.3 | Docs Team | ✅ Completed | Redirect + changelog staged for Phase 4 |
| Adopt three-layer config hierarchy | Config Hierarchy RFT | Platform WG | ✅ Completed | RFC accepted; helper scope defined |
| JSON Schema as canonical validation | Config Hierarchy RFT §6 | Platform WG | ✅ Completed | Validation work queued for Phase 3 |
| Relative paths in `paths.yaml` | Config Hierarchy RFT §6 | Tooling WG | ✅ Completed | Enforced through new path helpers |

## Open Questions
1. Do we maintain short-lived symlinks for renamed directories? **Decision:** No symlinks needed (solo prototype, minimal consumers). Owner: Infra ✅
2. How do we communicate doc merge to downstream partners? **Decision:** No migration note; a concise CHANGELOG entry is sufficient. Owner: Docs Team ✅
3. Any repos consuming `agent_scripts/` directly? **Decision:** None—this branch is standalone and incompatible with other repos. Owner: Tooling WG ✅

## Action Items
| ID | Description | Owner | Due | Status |
|----|-------------|-------|-----|--------|
| AI-001 | Circulate RFTs with request for comments (deadline 2025-11-25) | Framework Leads | 2025-11-21 | ✅ Completed |
| AI-002 | Compile list of repos referencing `AgentQMS/agent_interface/` directly | Tooling WG | 2025-11-22 | ✅ Completed |
| AI-003 | Draft stub README for `docs/ai_agent/` redirect | Docs Team | 2025-11-24 | ✅ Completed |
| AI-004 | Prototype config loader merge logic (defaults + overrides) | Platform WG | 2025-11-28 | ✅ Completed |

## Next Checkpoint
- **Date:** 2025-11-25
- **Agenda:** Review RFT feedback, finalize naming/config decisions, decide go/no-go for Phase 2 preparations.

