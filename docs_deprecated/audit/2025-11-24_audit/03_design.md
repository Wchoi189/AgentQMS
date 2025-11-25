### 03 Design Phase – Restructure Proposal & Standards (Draft)

**Date**: 2025-11-24  
**Scope**: Containerized AgentQMS framework (`.agentqms/`, `AgentQMS/`, `docs/`) – design responses to discovery/analysis findings.  
**Status**: Draft (Design Phase)

---

## 1. Critical Fixes (Blocking)

### 🔴 Fix 1 – Align agent workflows with canonical implementation layer (remove `scripts/agent_tools`)

**Problem**  
Agent interface shell workflows under `AgentQMS/interface/workflows/*.sh` invoke `../scripts/agent_tools/...`, but the containerized framework does not provide `scripts/agent_tools`; canonical tools live under `AgentQMS/toolkit/` / `AgentQMS/agent_tools/` and the Makefile is already wired correctly.

**Solution**  
- Treat the **Makefile** as the canonical agent entrypoint for artifacts, validation, and compliance.  
- Either:
  - (A) Update shell workflows to delegate to the Makefile (e.g. `make create-plan`, `make validate`, `make compliance`), or  
  - (B) Mark shell workflows as deprecated and keep only Make targets.

**Implementation (Option A – delegate to Make)**  
Example pattern for `create-artifact.sh`:

```bash
cd "$(dirname "$0")/.."  # ensure we are in AgentQMS/interface/
make create-$(TYPE) NAME="$NAME" TITLE="$TITLE"
```

**Actions**
- [ ] Decide between **A: delegate** vs **B: deprecate** shell workflows.  
- [ ] If delegating, update `create-artifact.sh`, `validate.sh`, and `compliance.sh` to call Make targets only.  
- [ ] If deprecating, change their bodies to print a clear message: “Use `make <target>`; this script is deprecated.”

**Success Criteria**
- [ ] No remaining references to `../scripts/agent_tools` in interface workflows.  
- [ ] Running any supported workflow from `AgentQMS/interface/` works out-of-the-box for agents.  
- [ ] Documentation and SST reference **only one** recommended path per capability (Make or direct Python, but not both).

---

## 2. High-Priority Design Decisions (Reusability)

### 🟡 Design 1 – Single canonical implementation layer: `AgentQMS/agent_tools/`

**Problem**  
Documentation and tooling currently refer to both `AgentQMS/toolkit/` and `AgentQMS/agent_tools/` as the implementation layer. This dual naming increases cognitive load and complicates exports.

**Solution**  
- Choose `AgentQMS/agent_tools/` as the canonical implementation layer name (aligned with Python package imports like `AgentQMS.agent_tools.*`).  
- Gradually deprecate or repurpose `AgentQMS/toolkit/` as:
  - A thin compatibility layer, or
  - A legacy directory containing only shims and transitional scripts.

**Implementation**
- Update:
  - `AgentQMS/interface/README.md` to state: “Implementation layer: `AgentQMS/agent_tools/`.”  
  - Export docs (or their successors in `AgentQMS/knowledge/meta`) to reference `AgentQMS/agent_tools/` only.  
  - Any remaining paths in tooling that hardcode `AgentQMS/toolkit/` when they should refer to the main implementation package.
- Where `toolkit` is required for backwards compatibility:
  - Keep `AgentQMS/toolkit/` as a **thin wrapper** that imports from `AgentQMS.agent_tools` and exposes the same CLI entrypoints.

**Actions**
- [ ] Inventory all references to `AgentQMS/toolkit/` and classify as:
  - [ ] Core (should move to `agent_tools`)  
  - [ ] Legacy (keep as shims or mark deprecated)
- [ ] Update interface Makefile comments and README to emphasize `agent_tools` as canonical.  
- [ ] Add a brief note in `toolkit/README.md` explaining its legacy/shim status.

**Success Criteria**
- [ ] New consumers see only one implementation-layer name in primary docs.  
- [ ] All new tools and protocols reference `AgentQMS/agent_tools/` exclusively.  
- [ ] `toolkit/` is either:
  - a documented legacy layer, or  
  - fully merged into `agent_tools/` and no longer needed.

---

### 🟡 Design 2 – Containerized doc root: `AgentQMS/knowledge/` as the single source of truth

**Problem**  
Knowledge is split across `docs/ai_handbook/` and `AgentQMS/knowledge/`; both are referenced from SST, references, and export docs. This conflicts with the architecture state (`docs_root: AgentQMS/knowledge`) and complicates reuse.

**Solution**  
- Treat `AgentQMS/knowledge/` as the **only** authoritative docs root.  
- Migrate all relevant protocols, references, and agent instructions from `docs/ai_handbook` into appropriate subfolders in `AgentQMS/knowledge/`.  
- Update SST and references to use `AgentQMS/knowledge/...` paths (or capability-based references via `.agentqms/state/architecture.yaml`).

**Implementation**
- Mapping approach:
  - `docs/ai_handbook/02_protocols/...` → `AgentQMS/knowledge/protocols/...`  
  - `docs/ai_handbook/03_references/...` → `AgentQMS/knowledge/references/...`  
  - `04_agent_system` agent-facing docs → `AgentQMS/knowledge/agent/`  
  - Templates → `AgentQMS/knowledge/templates/` or `AgentQMS/conventions/templates/`.
- After migration:
  - Replace `docs/ai_handbook/...` references in:
    - `AgentQMS/knowledge/agent/system.md`  
    - `smart-context-loading.md`  
    - Any meta/export docs still inside the container.
  - Optionally keep `docs/ai_handbook` only as **project history** outside the exported container.

**Actions**
- [ ] Finalize and execute a file-level migration plan from `docs/ai_handbook` to `AgentQMS/knowledge`.  
- [ ] Update all internal references to use `AgentQMS/knowledge` paths or logical capability references (e.g., “see import-handling protocol”).  
- [ ] Mark any remaining `docs/ai_handbook` references as legacy in a single migration note, not in SST.

**Success Criteria**
- [ ] `.agentqms/state/architecture.yaml` correctly points to all active knowledge locations.  
- [ ] No agent-facing doc references `docs/ai_handbook` as a primary location.  
- [ ] New projects can copy `.agentqms/` + `AgentQMS/` and have a self-contained knowledge surface.

---

### 🟡 Design 3 – Normalize audit framework paths to `AgentQMS/conventions/audit_framework/`

**Problem**  
Audit usage guides and tool-architecture docs still refer to `project_conventions/audit_framework/...`, while the actual containerized location is `AgentQMS/conventions/audit_framework/...`.

**Solution**  
- Update all documentation references to point to `AgentQMS/conventions/audit_framework/...`.  
- Clearly describe the **containerized audit bundle**:
  - Protocols: `AgentQMS/conventions/audit_framework/protocol/`  
  - Templates: `AgentQMS/conventions/audit_framework/templates/`  
  - Tools: `AgentQMS/toolkit/audit/` or `AgentQMS/agent_tools/audit/` (once naming is unified).

**Implementation**
- Edit:
  - `AgentQMS/conventions/audit_framework/usage_guide.md`  
  - `AgentQMS/conventions/audit_framework/tools/tool_architecture.md`  
  - `AgentQMS/conventions/audit_framework/README.md`
- Ensure Make targets under `AgentQMS/interface/` reference this containerized layout consistently.

**Actions**
- [x] Replace `project_conventions/audit_framework/...` with `AgentQMS/conventions/audit_framework/...` in all audit docs.  
- [ ] Add a short “Legacy Layout” subsection in the audit README, explaining previous locations for historical context only.

**Success Criteria**
- [ ] Running audit workflows in a new project requires no knowledge of `project_conventions/...`.  
- [ ] All audit-related docs inside the container reference the containerized paths only.

---

## 3. Medium-Priority Design (Maintainability)

### 🟠 Design 4 – Canonical artifact rules protocol + schema alignment

**Problem**  
Artifact rules (naming, placement, frontmatter) are scattered across multiple docs (prompts-artifact-guidelines, governance protocols, SST), increasing drift risk.

**Solution**  
- Use `AgentQMS/knowledge/protocols/governance/artifact_rules.md` as the **single canonical ruleset** for artifacts.  
- Ensure:
  - `q-manifest.yaml` + JSON schemas (including `bug_report.json`) align with these rules.  
  - SST and other protocols **reference** this file instead of redefining rules.

**Implementation**
- Update SST (`system.md`) artifact-related bullets to say “see Artifact Rules protocol” for details.  
- Review and adjust schemas/templates to ensure:
  - Required frontmatter fields match `artifact_rules.md`.  
  - Naming and directory structures match `q-manifest.yaml`.

**Actions**
- [ ] Cross-check `artifact_rules.md`, `q-manifest.yaml`, and all schemas/templates.  
- [ ] Replace any duplicated rule text in governance protocols with references to `artifact_rules.md`.

**Success Criteria**
- [ ] No conflicting artifact rules in different docs.  
- [ ] All validators and templates enforce the same ruleset.

---

## 4. Low-Priority Design (Optimization & Cleanup)

### 🟢 Design 5 – Archive verbose export/history docs outside the framework container

**Problem**  
Long-form export guides and historical assessments live under `docs/` and partially contradict or predate the containerized design.

**Solution**  
- Move or reclassify:
  - `docs/export_guide.md`, `docs/quick_start_export.md`, `docs/resources.md`, and historical assessment/RFC artifacts as **project-history material**, not part of the exported AgentQMS container.  
- Extract any still-relevant, framework-agnostic content into a compact `AgentQMS/knowledge/meta/MAINTAINERS.md`.

**Implementation**
- Create `AgentQMS/knowledge/meta/MAINTAINERS.md` with:
  - Short export overview.  
  - Pointers to architecture state, audit framework, and key protocols.  
- Move verbose and project-specific docs to a non-exported area or archive repo.

**Actions**
- [x] Draft `MAINTAINERS.md` with the minimum necessary guidance.  
- [ ] Tag legacy export/history docs as archived and exclude them from any packaged export.

**Success Criteria**
- [ ] Exported framework is lean: `.agentqms/` + `AgentQMS/` without project-specific history.  
- [ ] Maintainers still have a concise, up-to-date view of how to adapt/export the framework.

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