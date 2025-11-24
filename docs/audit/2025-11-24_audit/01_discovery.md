### Discovery Audit – Removal Candidate List (Discovery Phase Output)

#### **Executive Summary**

- **Scope**: Discovery audit of AgentQMS containerized framework (code + conventions + knowledge + interface), with focus on broken paths, legacy references, and reusability blockers.
- **Result**:
  - **🔴 Critical**: 1 confirmed blocking issue (broken interface workflows).
  - **🟡 High**: 3 major reusability/consistency issues (doc roots, legacy path references, dual implementation naming).
  - **🟠 Medium / 🟢 Low**: Several design and documentation alignment issues to resolve in later phases.

---

### 🔴 Critical Issues (Blocking)

#### 🔴 Path mismatch: agent interface workflows call non-existent `scripts/agent_tools` paths

- **Location**:
  - `AgentQMS/interface/workflows/create-artifact.sh`
  - `AgentQMS/interface/workflows/validate.sh`
  - `AgentQMS/interface/workflows/compliance.sh`
- **Issue**:
  - Each wrapper calls `python ../scripts/agent_tools/...`:
    - `../scripts/agent_tools/core/artifact_workflow.py`
    - `../scripts/agent_tools/compliance/validate_artifacts.py`
    - `../scripts/agent_tools/compliance/monitor_artifacts.py`
  - In this repo layout there is **no** `scripts/agent_tools/` tree above `AgentQMS/interface`; instead the canonical implementations are under:
    - `AgentQMS/toolkit/core/artifact_workflow.py`
    - `AgentQMS/toolkit/compliance/validate_artifacts.py`
    - `AgentQMS/toolkit/compliance/monitor_artifacts.py`
- **Impact**:
  - Agent-only shell workflows for artifact creation, validation, and compliance **do not function**.
  - Agents must currently use **Makefile targets** (which correctly call `../toolkit/...`) instead of these scripts.
- **Action**:
  - Update wrapper paths to align with `toolkit` (or remove wrappers entirely in favor of Make targets).
  - Optionally, add a quick runtime guard that prints “DEPRECATED – use Makefile” if you decide to retire them.

---

### 🟡 High Priority Issues (Reusability)

#### 🟡 Legacy `project_conventions/audit_framework` path references

- **Location** (non-exhaustive):
  - `AgentQMS/conventions/audit_framework/usage_guide.md`
  - `AgentQMS/conventions/audit_framework/tools/tool_architecture.md`
  - `AgentQMS/conventions/audit_framework/README.md`
  - Some audit-related artifacts under `docs/artifacts/...`
- **Issue**:
- Docs and usage guides repeatedly referenced `project_conventions/audit_framework/...` paths (old layout) instead of the actual containerized location `AgentQMS/conventions/audit_framework/...`.
- **Impact**:
  - Misleads maintainers/agents about where protocols, templates, and tools live.
  - Blocks straightforward reuse of the audit framework in new projects.
- **Action**:
  - Normalize all references to `AgentQMS/conventions/audit_framework/...`.
  - Optionally keep a brief “legacy layout” note in a single meta doc, not spread across usage text.

#### 🟡 Docs root mismatch: `docs/ai_handbook` vs `AgentQMS/knowledge`

- **Location**:
  - `AgentQMS/knowledge/agent/system.md` (multiple `docs/ai_handbook/...` references).
  - `AgentQMS/knowledge/references/context_optimization/smart-context-loading.md` (numerous `docs/ai_handbook/...` paths).
  - Root `README.md` and export docs refer to `docs/ai_handbook/` as the primary handbook.
  - `.agentqms/state/architecture.yaml` sets `docs_root: AgentQMS/knowledge`.
- **Issue**:
  - The architecture state and long-term design assume **knowledge** is under `AgentQMS/knowledge/`, but key instructions and context-optimization logic still hardcode `docs/ai_handbook/...`.
- **Impact**:
  - For reuse, consumers of the framework will see two competing doc roots.
  - Once docs are physically moved into `AgentQMS/knowledge/`, these references will become broken unless updated.
- **Action**:
  - As part of the docs migration, rewrite all `docs/ai_handbook/...` references to their `AgentQMS/knowledge/...` equivalents (or via a central “knowledge index”).
  - Keep a single, clear description of the old location only in a migration note if needed.

#### 🟡 Dual naming and messaging: `AgentQMS/toolkit` vs `AgentQMS/agent_tools`

- **Location**:
  - `AgentQMS/interface/README.md` and `docs/export_guide.md` emphasize `AgentQMS/toolkit/` as the implementation layer.
  - `.agentqms/state/architecture.yaml` and new design docs describe `AgentQMS/agent_tools/` as the implementation layer.
- **Issue**:
  - The framework now has **two parallel names** for the implementation layer, and both directories exist (`toolkit/` and `agent_tools/`) with overlapping responsibilities.
- **Impact**:
  - Confusion for maintainers and agents about which is canonical.
  - Makes export and path-based tooling more fragile.
- **Action**:
  - Choose a **single canonical name** for the implementation layer (e.g. `agent_tools` or `toolkit`) and align:
    - Interface Makefile paths,
    - Export docs,
    - Architecture state,
    - New knowledge docs.
  - Mark the other path as legacy and, where possible, add shims or clear deprecation notes.

---

### 🟠 Medium Priority Issues (Maintainability / Design)

#### 🟠 Smart context loading still tied to old doc layout

- **Location**:
  - `AgentQMS/knowledge/references/context_optimization/smart-context-loading.md`
- **Issue**:
  - Strategy and code examples reference `docs/ai_handbook/*.md` and `docs/artifacts/*` paths, not the new `AgentQMS/knowledge` design or containerized artifact layout.
- **Impact**:
  - When/if smart context loading is activated as a protocol, it will need substantial path and structure updates.
- **Action**:
  - Leave as-is for now (explicitly marked `status: experimental`), but during Design Phase:
    - Redesign context bundles against `architecture.yaml` + `AgentQMS/knowledge`.
    - Remove hard-coded `docs/ai_handbook` references in favor of capability-based lookups.

#### 🟠 Incomplete migration of protocols/references into `AgentQMS/knowledge`

- **Location**:
  - Many protocol and reference docs still live under `docs/ai_handbook/02_protocols` and `03_references`.
- **Issue**:
  - We’ve begun the migration (SST, tracking CLI, tool catalog, artifact rules, smart context loading), but the rest of the protocols and references are still in the old location and format.
- **Impact**:
  - Agents and maintainers see a split knowledge surface.
  - Rules are duplicated across old and new docs, risking drift.
- **Action**:
  - Complete the migration:
    - Move remaining protocols to `AgentQMS/knowledge/protocols/` and prune to agent-style rules.
    - Move references to `AgentQMS/knowledge/references/`, adding TL;DR sections.
    - Decommission or archive `docs/ai_handbook` once everything is represented in `AgentQMS/knowledge`.

---

### 🟢 Low Priority Issues (Optimization / Cleanup)

#### 🟢 Legacy export and project-specific docs still in `docs/`

- **Location**:
  - `docs/export_guide.md`, `docs/quick_start_export.md`, `docs/resources.md`.
  - Some assessment/RFC artifacts describing earlier directory refactors.
- **Issue**:
  - These documents are verbose, partially project-specific, and not aligned with the new `AgentQMS/knowledge` design.
- **Impact**:
  - They don’t break the framework but add noise and can confuse readers about the current canonical layout.
- **Action**:
  - Keep them outside the containerized knowledge surface:
    - Either archive in a separate “project history” area or compress essentials into a short `MAINTAINERS.md` under `knowledge/meta/` and retire the originals.

---

### Discovery Phase Status vs Protocol

- **Issue Identification**:
  - ✅ Broken agent interface wrappers (real path mismatches).
  - ✅ Legacy path references (`project_conventions/...`, `docs/ai_handbook/...`).
  - ✅ Dual implementation naming (`toolkit` vs `agent_tools`).
- **Categorization & Impact**:
  - ✅ Issues classified into Critical / High / Medium / Low with concise impact descriptions.
- **Removal Candidates**:
  - ✅ Clear candidates identified for removal/refactor:
    - Broken wrappers or their paths.
    - Legacy references to `project_conventions/...` and `docs/ai_handbook/...`.
    - One of the duplicate implementation-layer names once a canonical choice is made.

---


