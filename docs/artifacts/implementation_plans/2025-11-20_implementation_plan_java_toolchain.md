---
type: "implementation_plan"
category: "java-migration"
status: "archived"
version: "0.2"
tags: ["java", "cli", "validators", "automation"]
title: "Implementation Plan: Java Toolchain Migration"
date: "2025-11-20 00:00 (KST)"
last_updated: "2025-11-21 04:15 (KST)"
author: "Agent Maintainers"
note: "Java toolchain implementation has been moved to separate 'java-toolchain' branch. This plan documents the original implementation strategy."
---

# Implementation Plan: Java Toolchain Migration

## 1. Objective
- Rebuild the AgentQMS automation surface in Java after pruning Python/Node tooling.
- Deliver JVM-based CLIs (Maven modules and runnable JARs) that keep artifact workflows, compliance validation, documentation upkeep, and audit generation operational.
- Preserve existing documentation/artifact layouts (`docs/artifacts/**`, `docs/ai_handbook/**`) so downstream teams experience minimal disruption.

## 2. In-Scope vs Out-of-Scope
**In Scope**
- Java packaging (Maven multi-module project) inside `AgentQMS/java-tools`.
- CLI commands for artifact creation, validation, index updates, and audit generation.
- Shared utility layer replacing `AgentQMS.agent_tools.utils.runtime`.
- Adapter scripts in `agent_interface/` pointing to Java binaries.

**Out of Scope**
- Reintroducing Python/Node tooling archived under `AgentQMS/_archive`.
- UI/dashboard rewrites (Streamlit replacement).
- Documentation refresh beyond command references (handled after GA).

## 3. Deliverables
1. **Java Project Skeleton**
   - Maven parent `pom.xml`, module-specific POMs, baseline module layout (`core`, `validation`, `docs`, `audit`, `cli`).
   - Shared configuration loader that reads `.agentqms/config.yaml` + environment overrides.
2. **Artifact Workflow CLI**
   - Commands: `artifact create`, `artifact validate`, `artifact indexes`.
   - Template rendering using existing Markdown blueprints (read from `docs/artifacts/templates`).
3. **Compliance + Boundary Validators**
   - Rule engine mirroring `validate_artifacts.py` (filename, frontmatter, placement).
   - Boundary checks ensuring artifacts remain within approved directories.
   - JSON/Markdown report output.
4. **Documentation Maintenance Suite**
   - Link validator, index generator, manifest updater compatible with handbook paths.
5. **Audit Tooling**
   - Java implementation of `audit_generator.py` + `checklist_tool.py` with CLI parity.
6. **Agent Interface Integration**
   - Updated `agent_interface/Makefile` (or Maven wrapper script) invoking Java CLIs.
   - README updates describing new commands and prerequisites (JDK 21+, Maven).

## 4. Work Plan & Milestones

| Phase | Target | Key Tasks | Status |
|-------|--------|-----------|--------|
| Phase 1 – Foundation (Day 1-2) | Java workspace ready | Create `AgentQMS/java-tools` Maven project, configure code style, set up shared config loader, add smoke-test CLI (`mvn -f AgentQMS/java-tools/pom.xml -pl cli -am exec:java -Dexec.mainClass=com.agentqms.cli.AgentQmsCli -Dexec.args=\"status\"`). | ✅ **COMPLETE** |
| Phase 2 – Artifact Workflow (Day 3-5) | Artifact CLI parity | Implement template loader + renderer, port artifact creation logic, integrate validation hooks, add tests covering template selection and index trigger stubs. | ✅ **COMPLETE** (Core functionality working; validation hooks pending Phase 3) |
| Phase 3 – Compliance Engine (Day 6-8) | Validator parity | Port naming/frontmatter rules, implement boundary scanning, emit structured reports, add CLI commands `validate artifacts`, `validate boundary`. | ✅ **COMPLETE** |
| Phase 4 – Documentation Automation (Day 9-11) | Docs maintenance commands | Port index generator, manifest validator, and link checker; ensure outputs match current Markdown layouts. | ✅ **COMPLETE** |
| Phase 5 – Audit Suite (Day 12-13) | Audit CLI parity | Recreate audit generator + checklist workflows with templating + date utilities. |
| Phase 6 – Integration & Onboarding (Day 14) | Agent workflow ready | Recreate `agent_interface/Makefile` targets (or shell/Maven wrapper scripts) pointing to Java binaries, document prerequisites, smoke test end-to-end flow (`artifact create` → `validate` → `docs update`). |

## 5. Risks & Mitigations
- **Config Divergence** – Java CLI might read different paths than archived Python tools. *Mitigation*: centralize path resolution in a `PathResolver` service with tests referencing actual repo layout.
- **Template Drift** – Markdown templates may rely on Jinja-style placeholders. *Mitigation*: implement a minimal placeholder engine or reuse Java templating (e.g., Mustache) configured to respect existing tokens.
- **Maven Complexity** – Contributors unfamiliar with Maven may struggle. *Mitigation*: add wrapper scripts (`./agent-java artifact create ...`) plus concise onboarding docs.
- **Performance Regression** – Java validators must handle hundreds of files quickly. *Mitigation*: add benchmarks and ensure streaming I/O; parallelize when safe.

## 6. Dependencies
- JDK 21+ installed in agent environment.
- Existing Markdown templates and docs remain available (not removed during pruning).
- Access to `.agentqms` configs for runtime metadata.

## 7. Acceptance Criteria

### ✅ Completed
- `mvn -f AgentQMS/java-tools/pom.xml -pl cli -am exec:java -Dexec.mainClass=com.agentqms.cli.AgentQmsCli -Dexec.args="status"` succeeds from repo root.
- Running artifact creation produces compliant Markdown with proper frontmatter and content structure.
- Artifact templates (implementation_plan, assessment, design, research) are functional.
- CLI commands `artifact create` and `artifact list-templates` work correctly.

### 🔄 In Progress
- Agent Make targets or wrapper scripts successfully call into the Java CLIs with zero Python dependencies. (Phase 6)

## 8. Progress Summary

**Phase 1 (Foundation)**: ✅ Complete
- Maven multi-module project structure created
- PathResolver utility implemented
- CLI skeleton with status command working
- JDK 21 and Maven installed and configured

**Phase 2 (Artifact Workflow)**: ✅ Complete
- ArtifactTemplate and ArtifactTemplateRegistry implemented
- ArtifactWorkflowService with create functionality
- Template rendering with placeholder substitution
- Frontmatter generation with proper YAML format
- CLI commands: `artifact create`, `artifact list-templates`
- Templates available: implementation_plan, assessment, design, research
- Date formatting and filename generation working correctly

**Phase 3 (Compliance Engine)**: ✅ Complete
- ArtifactValidator with naming convention validation
- Frontmatter validation (required fields, valid types/categories/statuses)
- Directory placement validation
- BoundaryValidator for framework/project boundaries
- ValidationResult and reporting system
- CLI commands: `validate artifacts`, `validate boundary`, `validate all`

**Phase 4 (Documentation Automation)**: ✅ Complete
- ArtifactIndexUpdater for generating INDEX.md files in artifact directories
- LinkValidator for validating internal and external documentation links
- Frontmatter parsing and artifact metadata extraction
- CLI commands: `docs update-indexes`, `docs validate-links`
- Successfully generates indexes grouped by status with proper formatting

**Phase 5 (Audit Tools)**: ✅ Complete
- AuditGenerator for template-based document generation
- ChecklistTool for phase-specific checklist generation and tracking
- Support for placeholder replacement in templates ({{PLACEHOLDER_NAME}})
- CLI commands: `audit init`, `audit generate`, `audit checklist [generate|track]`, `audit report`, `audit list-templates`
- Successfully generates all 6 audit documents from templates
- Checklist generation from protocol/checklists.md
- Progress reporting for audit checklists

**Next Steps**: Begin Phase 6 (Integration & Onboarding) - create wrapper scripts and update Makefiles.

