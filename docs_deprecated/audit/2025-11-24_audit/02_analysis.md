### 02 Workflow Analysis – AgentQMS Containerized Framework

**Date**: 2025-11-24  
**Audit Scope**: Containerized AgentQMS framework (`.agentqms/`, `AgentQMS/`, `docs/`) – workflows related to artifacts, docs, audit, and context.  
**Status**: Draft (Analysis Phase)

---

## Executive Summary

- The **core implementation and conventions** (under `AgentQMS/agent_tools`, `AgentQMS/conventions`, `.agentqms`) are structurally sound and ready for reuse.
- The **biggest pain points** are:
  - Broken agent-interface shell workflows pointing at non-existent `scripts/agent_tools` paths.
  - Split and partially migrated **documentation workflows** (`docs/ai_handbook` vs `AgentQMS/knowledge`).
  - Mixed **implementation-layer naming** (`toolkit` vs `agent_tools`) that complicates mental models and export.
- The **audit framework** itself is well-structured, but its usage docs still reference the **legacy `project_conventions/...` layout**, which conflicts with the new containerized `AgentQMS/conventions/...` design.

---

## 1. Current High-Level Workflows

### 1.1 Artifact Lifecycle Workflow

**Actors**: AI Agents (primary), maintainers (secondary).

**Main paths**:

- **Makefile-based** (working):

  ```bash
  cd AgentQMS/interface/
  make create-plan NAME=... TITLE="..."
  make validate
  make compliance
  ```

  - Invokes: `AgentQMS/toolkit/core/artifact_workflow.py`, `AgentQMS/toolkit/compliance/*`.

- **Shell-wrapper-based** (broken):

  ```bash
  cd AgentQMS/interface/
  workflows/create-artifact.sh ...
  workflows/validate.sh ...
  workflows/compliance.sh ...
  ```

  - All call `../scripts/agent_tools/...` which **does not exist** in this layout.

**Pain points / bottlenecks**

- **Single critical break**: any agent using the documented `workflows/*.sh` will hit immediate `FileNotFound` errors.
- **Dual entrypoints** (Make vs shell scripts) cause confusion and drift:
  - Makefile targets are aligned with `toolkit`.
  - Shell wrappers still encode legacy `scripts/agent_tools` paths and lack the brevity reminders recently added to Make-based flows.

**Implications**

- For reuse, **only Makefile workflows are safe**; shell scripts must be fixed or clearly deprecated.
- Documentation (including SST and tool catalog) currently references **both** direct Python invocations and Make; this needs tightening to one canonical pattern per capability.

---

### 1.2 Documentation & Knowledge Workflow

**Intended design (new)**:

- **Docs root**: `AgentQMS/knowledge/` (per `.agentqms/state/architecture.yaml`).
- **Structure**:
  - `knowledge/agent/` – SST (`system.md`), tracking CLI, tool catalog.
  - `knowledge/protocols/` – governance/development/testing rules (e.g. `artifact_rules.md`).
  - `knowledge/references/` – architecture, import handling, smart context loading (experimental).
  - `knowledge/meta/` – maintainer docs (e.g. `framework_maintenance_design.md`).

**Actual usage (mixed)**:

- Many existing references (in SST, smart-context-loading, export docs, RFCS, assessments) still point to **`docs/ai_handbook/...`**, including:
  - `docs/ai_handbook/04_agent_system/system.md`
  - `docs/ai_handbook/02_protocols/...`
  - `docs/ai_handbook/03_references/...`
- The **new knowledge files** are in place but **not yet the sole source of truth**:
  - Rules are duplicated between `docs/ai_handbook/...` and `AgentQMS/knowledge/...`.
  - Some paths in new references still mention `docs/ai_handbook`.

**Pain points / bottlenecks**

- Agents and tools must navigate **two parallel documentation hierarchies**; it’s unclear which is authoritative.
- Migration is incomplete, so any future change risks being applied in one tree but not the other.
- Smart-context-loading design is tightly coupled to the old `docs/ai_handbook` layout, making it hard to adopt for the new containerized design.

**Implications**

- Until migration is finished and old references are removed or pointed at `AgentQMS/knowledge`, **documentation-based workflows are fragile**.
- Context-based tooling (future smart context loading) cannot be reliably implemented yet.

---

### 1.3 Audit Framework Workflow

**Intended flow** (per `usage_guide.md` and protocols):

- Use `AgentQMS/agent_interface/` + Make targets:

  ```bash
  cd AgentQMS/interface/
  make audit-init FRAMEWORK="..." DATE="..." SCOPE="..."
  make audit-validate
  make audit-checklist-generate PHASE="discovery"
  make audit-checklist-report
  ```

- Work with templates and protocols under:

  - `AgentQMS/conventions/audit_framework/templates/`
  - `AgentQMS/conventions/audit_framework/protocol/`

**Legacy references still present**:

- Multiple docs originally referred to:

  - `project_conventions/audit_framework/protocol/`
  - `project_conventions/audit_framework/templates/`
  - `AgentQMS/project_conventions/audit_framework/`

**Pain points / bottlenecks**

- New users following the **usage guide literally** may look for `project_conventions/...` which doesn’t exist in the containerized layout.
- The **tools themselves** point at the right places (under `AgentQMS/toolkit/audit`), but the written references are misleading.
- This adds friction whenever someone tries to **re-run or adapt** the audit framework in a new host project.

**Implications**

- Audit workflows are **operationally sound** via Make and toolkit, but documentation must be updated to reflect the containerized path structure.
- For export/reuse, keeping any reference to `project_conventions` is a reusability red flag.

---

### 1.4 Context & Discovery Tooling Workflow

**Core components**:

- `AgentQMS/toolkit/utilities/get_context.py` (used via `make context*` targets).
- `AgentQMS/toolkit/utilities/tracking/cli.py` + `tracking_cli.md`.
- `smart-context-loading.md` reference.

**Actual usage patterns**:

- Makefile provides **context bundle commands**:

  ```bash
  make context TASK="..."
  make context-development
  make context-docs
  make context-debug
  make context-list
  ```

- `get_context.py` examples still refer to `scripts/agent_tools/get_context.py` in usage comments.
- `smart-context-loading.md` describes advanced strategies and bundles that presuppose the **older doc layout** and a more mature context system than currently implemented.

**Pain points / bottlenecks**

- There is a **gap between design and implementation**:
  - Smart context loading is architected but not wired into Make targets or `.agentqms/state/architecture.yaml` as an active feature.
- References to `scripts/agent_tools/...` in usage strings conflict with the containerized `AgentQMS/toolkit/...` reality.
- Without aligning these, maintainers may hesitate to rely on context tools beyond straightforward `get_context.py` usage.

**Implications**

- Context workflows function in a **basic** way (via `get_context.py`), but advanced, automated context loading remains aspirational.
- Before pushing any “auto-activated protocol” for context, design must be reconciled with current paths and architecture state.

---

## 2. Pain Points & Bottlenecks by Category

### 2.1 Path & Layout Inconsistencies

- **Broken paths**: `../scripts/agent_tools/*` from interface workflows.
- **Legacy doc paths**: `docs/ai_handbook/...` scattered across new knowledge files and meta docs.
- **Legacy audit paths**: `project_conventions/audit_framework/...` in usage and tool-architecture docs.

**Bottleneck**: Any new consumer of the framework must mentally model **both old and new layouts**, increasing onboarding time and risk of misconfiguration.

### 2.2 Duplication of Rules & Knowledge

- Artifact rules currently live in:
  - `prompts-artifact-guidelines.md`,
  - Governance protocols,
  - SST (`system.md`),
  - New `artifact_rules.md`.
- Documentation architecture and import/loader behavior are explained in:
  - `architecture-summary.md`,
  - Multiple development references,
  - New meta design doc.

**Bottleneck**: It’s easy for one copy of the rules to drift; agents and maintainers may not know where the canonical version is.

### 2.3 Incomplete Migration to Containerized Knowledge Surface

- `AgentQMS/knowledge` is **partially populated** and referenced by `.agentqms/state/architecture.yaml`, but:
  - Old `docs/ai_handbook` tree remains heavily referenced.
  - Export/quick-start docs still assume `docs/ai_handbook` as the primary docs root.

**Bottleneck**: Tools, agents, and humans alike don’t have a single, clearly blessed doc hierarchy to rely on.

---

## 3. Workflow Impact of Identified Issues

For each key workflow:

- **Artifact creation/validation**:
  - Broken shell workflows risk runtime failures if any automation or docs recommend them.
  - Make-based commands work; they should be elevated as the **only recommended entrypoints** for agents.

- **Documentation & learning**:
  - Agents are told to “read this file only” (`system.md`), but that file itself still references the **old doc layout**, which is in the process of being replaced.
  - Human maintainers may need to consult both `docs/ai_handbook` and `AgentQMS/knowledge`, creating inefficiency and confusion.

- **Audit framework execution**:
  - The Make + toolkit path is viable, but usage/docs point to legacy directories, adding friction.
  - For reuse in other projects, those references are a clear reusability hazard.

- **Context loading**:
  - Basic `get_context.py` usage is fine; advanced strategies and metrics are still conceptual.
  - Smart context loading cannot yet be treated as a dependable mechanism, which is correctly reflected in its `experimental` status.

---

## 4. Summary – Inputs for Design Phase

The Analysis Phase shows that:

- The **most urgent design work** is **not** in core Python logic but in:
  - **Path normalization** (interface workflows, docs, audit references).
  - **Knowledge consolidation** (migrating to `AgentQMS/knowledge` and turning rules into single canonical protocols).
- The **current architecture state file** (`.agentqms/state/architecture.yaml`) is a solid base for:
  - Future knowledge lookup by capability.
  - Future context-loading design.
- The **Design Phase** should focus on:
  - Proposing a **single canonical implementation-layer name** and directory (`agent_tools` vs `toolkit`) and adjusting all references.
  - Finalizing the **docs migration plan** (mapping `docs/ai_handbook/...` to `AgentQMS/knowledge/...`) and updating SST + references accordingly.
  - Deciding the fate of **interface shell workflows**:
    - Either aligned with `toolkit`/`agent_tools` or officially deprecated in favor of Make.

This completes the **Analysis Phase** per `02_analysis_protocol.md`: workflows have been mapped, pain points identified, and specific design questions isolated for the next phase.

---


