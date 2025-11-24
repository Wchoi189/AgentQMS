### 04 Implementation Phase – Phased Plan

**Date**: 2025-11-24  
**Scope**: Implement design decisions for paths, docs, and conventions in the containerized AgentQMS framework.  
**Status**: Draft (Implementation Phase)

---

## Phase 1: Critical Fixes – Make Framework Functional

**Timeline**: 1 week  
**Priority**: 🔴 Critical  
**Goal**: Ensure all agent workflows for artifact creation, validation, and compliance function reliably in the containerized layout.

### Tasks
1. Decide on the fate of `AgentQMS/interface/workflows/*.sh`:
   - Delegate to Make targets or deprecate in favor of Make-only usage.
2. Remove all `../scripts/agent_tools/...` references from interface workflows and any remaining docs.  
3. Verify that all Makefile targets (`create-*`, `validate`, `compliance`) work end-to-end in a clean checkout.

### Success Criteria
- [x] No references to `../scripts/agent_tools` remain in executable workflows.  
- [ ] Running `make create-plan`, `make validate`, and `make compliance` from `AgentQMS/interface/` succeeds without manual path tweaks.  
- [ ] SST and quick references show only the working workflows (no broken examples).

### Risks
- **Risk**: Agents or scripts relying on the old shell wrappers may break.  
  **Mitigation**: Keep wrappers but make them thin delegators to Make, or print a clear deprecation message.

---

## Phase 2: High-Priority Changes – Make Framework Reusable

**Timeline**: 1 week  
**Priority**: 🟡 High  
**Goal**: Clean up path and naming inconsistencies so the framework can be dropped into new projects without confusion.

### Tasks
1. **Implementation layer naming**:
   - Choose `AgentQMS/agent_tools/` as canonical implementation layer in design docs.  
   - Mark `AgentQMS/toolkit/` as legacy/shim in its README and update references in interface/knowledge/meta docs.
2. **Doc root consolidation**:
   - Finalize mapping from `docs/ai_handbook/...` to `AgentQMS/knowledge/...`.  
   - Update SST, smart-context-loading, and any in-container docs to use `AgentQMS/knowledge` paths.  
   - Mark `docs/ai_handbook` as project history/not exported.
3. **Audit path normalization**:
   - Replace `project_conventions/audit_framework/...` with `AgentQMS/conventions/audit_framework/...` across audit docs.

### Success Criteria
- [ ] A new maintainer sees only `AgentQMS/agent_tools/` as the implementation layer in all primary docs.  
- [ ] All agent-facing docs and protocols reference `AgentQMS/knowledge` as the docs root.  
- [ ] Audit usage and tool-architecture docs reference only `AgentQMS/conventions/audit_framework/...`.

### Risks
- **Risk**: Over-aggressive refactors break existing tool paths.  
  **Mitigation**: Apply changes incrementally; use search/grep to verify all references and run validation tools after each batch.

---

## Phase 3: Medium-Priority Changes – Improve Maintainability

**Timeline**: 1 week  
**Priority**: 🟠 Medium  
**Goal**: Consolidate rules and references to reduce drift and make the framework easier to extend.

### Tasks
1. Complete migration of protocols/references into `AgentQMS/knowledge/`:
   - Move remaining `docs/ai_handbook/02_protocols` and `03_references` docs to the new structure.  
   - Prune and compress them into strict agent-oriented formats (rules + TL;DR).
2. Canonicalize artifact rules:
   - Make `artifact_rules.md` the only full artifact-rules definition.  
   - Ensure schemas, templates, and validators all align with it.
3. Align smart-context-loading design with containerized layout:
   - Add placeholders or notes in `smart-context-loading.md` for future adjustments to `AgentQMS/knowledge` and `.agentqms/state/architecture.yaml`.

### Success Criteria
- [ ] Protocols and references exist only under `AgentQMS/knowledge`, not as competing copies elsewhere.  
- [ ] Artifact rules are consistent across docs, schemas, and validators.  
- [ ] Smart-context-loading reference clearly marks what is design-only vs. implemented today.

### Risks
- **Risk**: Moving docs introduces broken links or missing references.  
  **Mitigation**: Run documentation link validation tooling after migration; add redirects or migration notes where needed.

---

## Phase 4: Low-Priority Changes – Optimize & Clean Up

**Timeline**: 1 week  
**Priority**: 🟢 Low  
**Goal**: Reduce noise, archive legacy materials, and smooth maintainer experience.

### Tasks
1. Archive verbose export/history docs outside the framework container.  
2. Create `AgentQMS/knowledge/meta/MAINTAINERS.md` as a concise onboarding + export guide for maintainers.  
3. Tag or move historical artifacts (old assessments/RFCs) to a clear “project history” location.

### Success Criteria
- [ ] Exported AgentQMS bundle is lean and free of project-specific history.  
- [ ] Maintainers have a single, short maintainer guide for export/adaptation.  
- [ ] Historical docs remain accessible but clearly separated from the reusable framework.

---

{
  "cells": [],
  "metadata": {
    "language_info": {
      "name": "python"
    }
  },
  "nbformat": 4,
  "nbformat_minor": 2
}