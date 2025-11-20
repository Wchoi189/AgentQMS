---
type: "implementation_plan"
category: "framework-structure"
status: "draft"
version: "0.1"
tags: ["structure", "naming", "configuration"]
title: "Implementation Plan: Framework Structure & Configuration Refactor"
date: "2025-11-20 00:00 (KST)"
author: "Framework Maintainers"
---

# Implementation Plan: Framework Structure & Configuration Refactor

## Master Prompt

> You are an infrastructure-focused AI engineer responsible for removing naming ambiguity and configuration sprawl in the AgentQMS framework. Deliver a phased plan that realigns directory names, introduces a layered configuration hierarchy, and preserves reliability for downstream teams during migration.

## Overview

- **Problem Summary:** Directory names (`agent/`, `project_conventions/`, `docs/ai_handbook/04_agent_system/`) and configuration locations are ambiguous, leading to onboarding friction and fragile tooling. We must realign naming, centralize configuration, and prepare for migrations before updating documentation.
- **Scope:** Rename interface directories, introduce the new configuration hierarchy, consolidate documentation, and provide helper tooling.
- **Out of Scope:** Final documentation rewrite (deferred until structure stabilizes), feature work unrelated to path/config organization.
- **Timebox:** ~4 weeks (phased).
- **Dependencies:** Approval of RFTs (directory naming, configuration hierarchy), availability of migration tooling, alignment with documentation team.

---

## Autonomous Execution Model

- **Coordination Channel:** `#agentqms-refactor` (primary), fallback to kickoff notes for async updates.
- **State Artifacts:** Implementation plan (this doc), Phase 1 kickoff note, RFTs, design doc. Autonomous agents must update status tables + action items after each meaningful change.
- **Worker Roles:**
  - **Coordinator Agent:** Ensures prerequisites/approvals, updates progress tracker, escalates blockers.
  - **Infra Agent:** Executes filesystem changes, config migrations, shims, backups.
  - **Tooling Agent:** Builds helper APIs, migration CLI, validation/lint rules.
  - **Docs Agent:** Handles handbook merges, redirects, changelog messaging.
- **Execution Protocol:**
  1. Read relevant RFTs + kickoff note before acting.
  2. Claim task by adding comment in action item table; include planned command/script.
  3. Perform work in isolated branch; run associated tests listed in phase matrix.
  4. Log results + telemetry links in kickoff note and update this plan’s trackers.
  5. If automation detects failures, roll back via documented backup procedure and notify coordinator.
- **Guardrails:** No direct edits to partner repos without dry run + approval; all migrations must support `--discover`, `--dry-run`, `--apply` sequencing; backups stored in `.agentqms/backups`.

---

## Context & Constraints

- Legacy exports and partner projects still assume the old directory layout; migrations must remain backward compatible for at least one release.
- Tooling currently relies on hard-coded relative paths; refactors must ship alongside helper APIs to avoid regressions.
- Documentation updates are intentionally deferred until after structural changes stabilize to prevent churn.
- Any downtime in `make` workflows or CLI wrappers blocks downstream work; plan prioritizes reliability and staged rollout.

---

## Related Artifacts & References

- **Phase 1 Kickoff Notes:** `docs/artifacts/notes/2025-11-20_PHASE1_kickoff.md` (decision checklist, action items, open questions log)
- **Directory Naming RFT:** `docs/artifacts/rfcs/2025-11-20_RFT_directory_naming_refactor.md`
- **Configuration Hierarchy RFT:** `docs/artifacts/rfcs/2025-11-20_RFT_configuration_hierarchy.md`
- **Design Doc – Config Hierarchy:** `docs/artifacts/design_documents/2025-11-20_design_config_hierarchy.md`

Use this plan alongside the kickoff notes for day-to-day execution tracking; RFTs and design doc remain the canonical decision artifacts.

---

## Goal-Execute-Update Loop

### 🎯 Goal: Phase 1 – Decisions & RFCs
**Next Task:** Ratify naming + directory plan and finalize config hierarchy RFC.
- **Pass:** Proceed to Phase 2.
- **Fail:** Revisit assessment findings and gather additional input.

### 🎯 Goal: Phase 2 – Directory & Config Restructure
**Next Task:** Implement directory renames and migrate configuration files.
- **Pass:** Proceed to Phase 3.
- **Fail:** Roll back changes, refine migration scripts, retry.

### 🎯 Goal: Phase 3 – Tooling & Validation
**Next Task:** Update helpers, CLIs, and validators to rely on the new hierarchy.
- **Pass:** Proceed to Phase 4.
- **Fail:** Fix regressions, add tests, retry.

### 🎯 Goal: Phase 4 – Documentation & Cleanup
**Next Task:** Update README/handbooks and remove deprecated shims.
- **Pass:** Mark plan complete.
- **Fail:** Capture gaps, re-open tasks.

---

## Progress Tracker

| Phase | Task ID | Description | Owner | Status | Notes |
|-------|---------|-------------|-------|--------|-------|
| 1 | P1-T1 | Ratify naming plan (`agent_interface/`, `project_conventions/`, docs merge) | Framework Leads | ✅ Completed | Decision log updated in `2025-11-20_PHASE1_kickoff` |
| 1 | P1-T2 | Approve configuration hierarchy RFC | Platform WG | ✅ Completed | RFC signed; helper scope confirmed |
| 1 | P1-T3 | Inventory `agent_scripts/` overlap | Tooling WG | ✅ Completed | Documented in `2025-11-20_PHASE1_kickoff` (no external consumers) |
| 2 | P2-T1 | Create `config_defaults/` and move framework defaults | Infra | ✅ Completed | Defaults moved to `AgentQMS/config_defaults/` |
| 2 | P2-T2 | Introduce root `config/` & refresh `.agentqms/config.yaml` | Infra | ✅ Completed | New `config/` tree + runtime snapshot writer |
| 2 | P2-T3 | Rename directories + install shims/logging | Infra + Docs | ✅ Completed | `agent/`→`agent_interface/`, `conventions/`→`project_conventions/`, migration warnings added |
| 2 | P2-T4 | Migrate config files + generator | Infra | ✅ Completed | ConfigLoader rewired to new hierarchy |
| 3 | P3-T1 | Implement config/path helper APIs | Tooling WG | ✅ Completed | New getters in `agent_tools.utils.paths` |
| 3 | P3-T2 | Enhance validation + deprecation checks | QA | ✅ Completed | Config loader + boundary validator log legacy usage |
| 3 | P3-T3 | Build migration script + logging | Infra | ✅ Completed | `agent_tools/migration/migrate.py` with discover/dry-run/apply |
| 4 | P4-T1 | Update handbooks/READMEs | Docs Team | ✅ Completed | Handbook + README now reference `04_agent_system/` |
| 4 | P4-T2 | Remove shims & archive legacy docs | Infra + Docs | ✅ Completed | Legacy `docs/ai_agent/` removed; all tooling/docs point to `docs/ai_handbook/04_agent_system/` |

---

## Autonomous Task Graph & Assignments

| Task ID | Worker Agent | Trigger Condition | Key Commands / Scripts | Acceptance Criteria |
|---------|--------------|-------------------|------------------------|---------------------|
| P1-T1 | Coordinator Agent | RFT feedback window closes | `scripts/rft/collect_feedback.py --rft directory_naming` | Decision checklist rows updated, approvals logged in kickoff note |
| P1-T2 | Coordinator + Tooling Agent | Config RFC draft ready | `scripts/rft/collect_feedback.py --rft config_hierarchy` | Signed RFC PDF, schema questions resolved |
| P2-T1 | Infra Agent | Phase 1 complete | `make config_defaults.init` | `config_defaults/` committed, tests `pytest tests/config_defaults` green |
| P2-T2 | Infra Agent | After P2-T1 | `make agentqms-init-config` | Root `config/` scaffolded, `.agentqms/config.yaml` regen diff attached |
| P2-T3 | Infra Agent | After P2-T2 | `scripts/migrate/rename_dirs.py --apply --telemetry` | Directory rename logs stored, shims emitting telemetry |
| P2-T4 | Infra Agent | After shims verified | `scripts/migrate/config_files.py --dry-run/--apply` | Legacy configs relocated, generator snapshot attached |
| P3-T1 | Tooling Agent | Helper API spec approved | `scripts/helpers/generate_paths.py` + `make lint-helpers` | Helper package published, CLIs import helpers |
| P3-T2 | QA Agent | After helpers integrated | `make validate-config` | Deprecated dirs detected, schema lint gating CI |
| P3-T3 | Tooling + Infra | After P2 tasks | `agentqms migrate --discover/dry-run/apply` | Migration logs archived, telemetry dashboards linked |
| P4-T1 | Docs Agent | Tooling adoption complete | `scripts/docs/update_handbook.py` | Handbook PR merged, redirect stub verified |
| P4-T2 | Infra + Docs | Shim fallback <5% | `scripts/migrate/remove_shims.py` | Shims removed, monitoring alarms green 72h |

- **Execution Notes:** Autonomous workers must record command output hashes in kickoff note action items; failed commands must halt automation and escalate.

---

## Phase Outline & Tasks

### **Phase 1: Decision & RFC (Week 1)**
1. [ ] **Task 1.1: Ratify Naming Plan**
   - [ ] Approve `agent_interface/` rename scope *(see RFT: directory naming refactor)*
   - [ ] Approve `project_conventions/` rename *(see RFT: directory naming refactor)*
   - [ ] Approve merging `docs/ai_handbook/04_agent_system/` into handbook *(see RFT: directory naming refactor)*
2. [ ] **Task 1.2: Configuration RFC**
   - [ ] Review `config_defaults/` + root `config/` proposal *(see RFT: configuration hierarchy)*
   - [ ] Finalize precedence rules and helper APIs
   - [ ] Document open questions and answers
3. [ ] **Task 1.3: Agent Scripts Inventory**
   - [ ] Catalog `agent_scripts/` vs `agent_tools/` overlap
   - [ ] Tag scripts for wrapper vs implementation migration (feeds Phase 2)

### **Phase 2: Directory & Config Restructure (Weeks 2–3)**
1. [ ] **Task 2.1: Create `config_defaults/`**
   - [ ] Move `AgentQMS/config/framework.yaml` into defaults tree
   - [ ] Extract interface defaults from `agent/config/`
2. [ ] **Task 2.2: Introduce Root `config/` & `.agentqms/` Updates**
   - [ ] Scaffold directory with sample overrides
   - [ ] Update installer/export instructions (internal notes only)
   - [ ] Ensure `.agentqms/config.yaml` generation reflects new layers
3. [ ] **Task 2.3: Rename Directories**
   - [ ] `agent/` → `agent_interface/`
   - [ ] `conventions/` → `project_conventions/`
   - [ ] Provide compatibility shims/logging
4. [ ] **Task 2.4: Migrate Config Files**
   - [ ] Move contents of `agent/config/` into new hierarchy
   - [ ] Update `.agentqms/config.yaml` generator

### **Phase 3: Tooling & Validation (Week 3–4)**
1. [ ] **Task 3.1: Update Path Helpers**
   - [ ] Add getters (`get_agent_interface_dir()`, `get_config_defaults_dir()`, etc.)
   - [ ] Refactor CLIs to use helpers
2. [ ] **Task 3.2: Enhance Validation**
   - [ ] Add checks for deprecated directories
   - [ ] Validate config schema + precedence
3. [ ] **Task 3.3: Migration Scripts**
   - [ ] Provide automation for existing installs
   - [ ] Log migration status to `.agentqms/migration.log`

### **Phase 4: Documentation & Cleanup (Week 4)**
1. [ ] **Task 4.1: Update Handbooks/READMEs**
   - [ ] Incorporate new directory names and config hierarchy
   - [ ] Merge `docs/ai_handbook/04_agent_system/` content into `docs/ai_handbook/` section
2. [ ] **Task 4.2: Remove Shims & Deprecations**
   - [ ] Delete old directories after warnings
   - [ ] Archive legacy docs & close out migration notices

---

## Phase Execution Details

### Phase 1 – Decisions & RFCs
- **Inputs:** Directory Naming RFT, Config Hierarchy RFT, kickoff notes, config design doc.
- **Execution Steps:**
  - Run async + live review sessions; record approvals/dissent in kickoff note.
  - Lock final naming matrix (directories + doc merge) and share with partners.
  - Complete `agent_scripts/` inventory (done) and capture consumers.
- **Exit Criteria:** Decision checklist rows in kickoff note marked ✅; outstanding questions closed or assigned.

### Phase 2 – Directory & Config Restructure
- **Task 2.1 `config_defaults/`:** Create tree containing `framework.yaml`, `interface.yaml`, and schema-driven defaults; update loaders and add merge tests.
- **Task 2.2 Root `config/`:** Scaffold overrides (`config/environments/<env>.yaml`, `config/overrides/local.yaml`, `config/paths.yaml`), update installer + `.agentqms/config.yaml` generator.
- **Task 2.3 Renames:** Rename `agent/`→`agent_interface/` and `conventions/`→`project_conventions/`; add shim module with warnings + telemetry.
- **Task 2.4 Config Migration:** Move legacy `agent/config/` contents into new hierarchy, update generators + CI to consume helpers.
- **Exit Criteria:** New layout merged to default branch, shims logging, migration script dry-run success on seed repo.

### Phase 3 – Tooling & Validation
- Implement `path_helpers` (or equivalent) with getters surfaced to CLIs + Make targets; enforce usage via lint.
- Extend validation suite to detect deprecated directories and enforce config precedence.
- Build migration CLI with discover/dry-run/apply modes, writing to `.agentqms/migration.log`.
- **Exit Criteria:** Tooling WG + QA sign-off, CI green with new lint, migration script validated on partner repo clone.

### Phase 4 – Documentation & Cleanup
- Docs merge `docs/ai_handbook/04_agent_system/` content into `docs/ai_handbook/` with redirects + changelog entry.
- Infra removes shims after one release cycle, archives legacy directories, and confirms zero references remain.
- Publish completion report linking to updated handbook + telemetry summary.

---

## Phase 1 Kickoff (Week 1)

- **Start Date:** 2025-11-20  
- **Focus:** Finalize naming approvals, lock configuration hierarchy, inventory agent scripts.
- **Planned Outputs:** Signed RFCs (naming + config), documented overlap analysis for `agent_scripts/`.
- **Coordination:** Framework Leads hosting daily 15-min standup this week; Platform WG and Tooling WG representation required.
- **Blockers:** None; dependencies cleared by RFT approvals.
- **Cross-Reference:** See `docs/artifacts/notes/2025-11-20_PHASE1_kickoff.md` for the detailed decision checklist, action items AI-001..004, and resolved questions backing this phase.

---

## Phase 2 Kickoff & Execution (Weeks 2–3)

- **Prereqs:** Phase 1 decision log completed, helper API surface approved, migration tooling ready for dry-run.
- **Readiness Checklist (due 2025-11-27):**
  - [ ] Config schemas frozen and published in `config_defaults/schema/`.
  - [ ] Partner comms sent with rename timeline + rollback steps.
  - [ ] Infra staffing + pair rotation confirmed for rename + migration windows.
  - [ ] Migration script `--discover/--dry-run` modes demoed.
- **Execution Cadence:**
  - **Week 2 (Days 1–2):** Create `config_defaults/`, scaffold root `config/`, add precedence tests.
  - **Week 2 (Days 3–4):** Commit directory renames with shims + telemetry; run smoke/regression tests.
  - **Week 3 (Days 1–3):** Migrate configs/generator, regenerate `.agentqms/config.yaml`, capture dry-run logs.
  - **Week 3 (Day 4):** Consolidate findings, prep helper adoption plan for Phase 3.
- **Checkpoints:** Mid-week rename go/no-go, end-of-week readiness review (sign-off recorded in kickoff note).
- **Outputs:** Updated tree on default branch, migration script dry-run artifacts, release note draft, telemetry dashboard URL.

---

## Phase 3 Execution Plan (Week 3–4 overlap)

- **Entry Criteria:** Phase 2 exit review signed; helper API ready for adoption; migration dry-runs green.
- **Focus Areas:**
  - Adopt helper getters across CLIs/Make targets via tracked PR set.
  - Enhance validation + telemetry (deprecation detection, schema enforcement).
  - Harden migration tooling with partner repo rehearsals (discover → dry-run → apply).
- **Milestones:**
  - **M3.1:** Helper library published + version pinned (Week 3 Day 4).
  - **M3.2:** CLI regression suite green with lint enforcing helper usage (Week 4 Day 1).
  - **M3.3:** Migration script validated on ≥2 partner repos with logs archived (Week 4 Day 2).
- **Risk Controls:** Feature freeze for high-risk CLIs during adoption; telemetry dashboards live before helper release; rollback instructions tied to helper version tags.

---

## Phase 4 Closeout & Go-Live (Week 4)

- **Entry Criteria:** Helper adoption complete, telemetry shows <5% shim fallback, migration tooling GA-ready.
- **Activities:**
  - Docs Team merges handbook updates, onboarding guides, and changelog entries (includes redirect stubs).
  - Infra removes compatibility shims via feature-flagged rollout; monitors telemetry for regressions.
  - Final validation sweep (link checker + schema + helper enforcement) prior to tagging release.
- **Go-Live Checklist:**
  - [ ] `docs/ai_handbook/` reflects new structure with redirects tested end-to-end.
  - [ ] Shim removal PR merged + telemetry alarm configured for legacy path touches.
  - [ ] Release/retro report posted to `#agentqms-refactor` with migration stats + rollback plan archived.
- **Completion Signal:** Post-migration audit confirms zero deprecated directories referenced; handbook feedback loop closed; plan status updated to `Complete`.

---

## Success Criteria

### Phase 1
- ✅ Naming decisions documented and approved
- ✅ Config hierarchy RFC signed off

### Phase 2
- ✅ `config_defaults/` + root `config/` structure in place
- ✅ Directories renamed with minimal breakage
- ✅ Migration script prepared

### Phase 3
- ✅ Tooling uses helper getters (no raw relative paths)
- ✅ Validators detect deprecated paths/configs
- ✅ Migration script validated on sample repo

### Phase 4
- ✅ Documentation updated
- ✅ Shims removed, legacy config directories retired
- ✅ Handbook reflects merged content

---

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Hard-coded paths missed | Breaks CLIs/scripts | Comprehensive search + regression tests |
| Config overrides conflict | Runtime breakage | Schema validation + precedence logging |
| Large doc update churn | Confusion | Defer docs until structure stable; coordinate sprint |
| Migration script errors | Users stuck mid-upgrade | Dry-run mode + backups before changes |

---

## Next Steps

1. Socialize decision + RFC plan with maintainers.  
2. Begin Phase 1 tasks (naming approval, RFC finalization).  
3. Schedule implementation weeks and assign owners.  
4. After Phase 2/3 complete, re-open audit framework documentation tasks.

---

## Timeline & Milestones

| Week | Focus | Checkpoint |
|------|-------|------------|
| 1 | Phase 1 – Decisions & RFCs | Naming + config RFC approvals signed |
| 2 | Phase 2 kickoff – config defaults + root config | `config_defaults/` scaffolded, root `config/` in repo |
| 3 | Phase 2 completion + Phase 3 start | Directory rename PR merged with shims, migration script draft ready |
| 4 | Phase 3 wrap + Phase 4 docs/cleanup | Helper APIs released, docs PR ready, shim removal plan confirmed |

- **Release Gates:** Each week ends with a go/no-go review; blockers escalate to Framework SteerCo within 24h.
- **Contingency:** If any checkpoint slips by >3 days, swap Week 4 documentation tasks to Docs team while Infra focuses on outstanding migrations.

---

## Resource & Communication Plan

- **Owners:** Framework Leads (overall), Infra (directory/config), Tooling WG (helpers), Docs (handbooks).
- **Standups:** 2× weekly cross-team sync covering blockers + readiness to advance phases.
- **Status Reporting:** Publish summary to `#agentqms-refactor` every Thursday; include KPIs (number of paths migrated, config validation pass rate).
- **Change Management:** Migration scripts ship with dry-run instructions and rollback steps pushed to the internal handbook before general availability.

---

## Migration Workflow & Tooling

1. **Discovery:** `agentqms migrate --discover` inventories current directories/configs and writes `.agentqms/migration-report.json`.
2. **Dry Run:** `agentqms migrate --dry-run` previews file moves, config merges, and shim activations; fails fast on schema drift.
3. **Backup:** Script snapshots touched paths to `.agentqms/backups/<timestamp>/` before mutations.
4. **Apply:** `agentqms migrate --apply` performs renames, scaffolds `config_defaults/` + root `config/`, regenerates `.agentqms/config.yaml`, and updates helpers.
5. **Telemetry:** Structured events (phase, repo, outcome) emitted to central logging and `.agentqms/migration.log` for traceability.
6. **Validation:** Post-apply validation suite runs helper-based integration tests; failures provide rollback commands referencing latest backup.

---

## Test & Verification Matrix

| Phase | Primary Tests | Owner | Tooling |
|-------|---------------|-------|---------|
| 1 | RFC lint + decision checklist review | Framework Leads | Markdown lint, kickoff note |
| 2 | File layout + config precedence integration tests | Infra | `pytest` integration suite, filesystem snapshot diff |
| 3 | CLI regression + schema validation + migration dry runs | Tooling WG / QA | CLI harness, JSON Schema validator, migration simulator |
| 4 | Docs link checker + shim removal validation | Docs + Infra | Link checker, CI job enforcing zero legacy refs |

---

## Open Questions

1. Do partner repositories require staggered rollout windows, or can we coordinate a single migration weekend?  
   **Answer:** Proceed with a single migration weekend coordinated across partner repos; plan includes dry-run + rollback steps beforehand.
2. Should compatibility shims emit structured telemetry to central logging, or is local logging sufficient for the first release?  
   **Answer:** Emit structured telemetry to the central logging pipeline from Day 1 to accelerate deprecation tracking.
3. Are there additional directories (e.g., `samples/`) that need renaming for parity with the new conventions?  
   **Answer:** No additional directories require renaming right now; revisit after conventions stabilize.

---

## Validation & Reliability Strategy

- **Automated Tests:** Expand integration tests for `make` targets and config loaders to ensure new helper APIs behave consistently across environments.
- **Migration Dry Runs:** Execute migration scripts on cloned repositories (including partner projects) with a dry-run flag; capture logs in `.agentqms/migration.log`.
- **Schema Enforcement:** Introduce CI checks that validate merged configs against JSON Schema and flag legacy directories.
- **Observability:** Emit structured logs whenever tooling falls back to compatibility shims; after one release, convert these into hard failures.
- **Rollback Plan:** Tag repository prior to each phase, maintain shims for at least one release cycle, and document rollback commands in the migration guide.

---

**Status:** Plan complete – Phase 4 documentation + cleanup landed (ready for release).

