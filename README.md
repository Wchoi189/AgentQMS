# AgentQMS Framework

AgentQMS is a reusable Quality Management Framework that standardizes
artifact creation, documentation workflows, and automation for collaborative
AI coding. The framework is **containerized** so it can travel between projects
as a pair of directories: `.agentqms/` + `AgentQMS/`.

## Framework Contents

### AgentQMS/ (Framework Container)

- `interface/` – Agent-only interface layer (Makefile, CLI wrappers, workflows).
- `agent_tools/` – Canonical implementation layer (automation, validators, docs tooling).
- `conventions/` – Artifact types, schemas, templates, and audit framework.
- `knowledge/` – Self-contained knowledge surface for agents and maintainers:
  - `agent/` – system SST, quick references, tool catalog.
  - `protocols/` – governance/development/testing protocols.
  - `references/` – technical and architecture references.
  - `meta/` – maintainer-facing docs (e.g., `MAINTAINERS.md`, framework design).

> Note: `AgentQMS/toolkit/` still exists as a **legacy compatibility layer**
> but all new code and docs should target `AgentQMS/agent_tools/`.

### Project-Level Directories

- `.agentqms/` – Hidden framework state and configuration:
  - `settings.yaml` – project configuration (if present).
  - `effective.yaml` – resolved configuration snapshot.
  - `state/architecture.yaml` – component and capability map.
- `docs/` – **project history** and host-project artifacts:
  - `docs/artifacts/` – implementation plans, assessments, bug reports, etc.
  - `docs/audit/` – audit outputs (including `2025-11-24_audit/` for this refactor).
  - `docs/ai_handbook/` – legacy handbook; kept for history, not exported.

## Using AgentQMS in a Project

1. **Copy the container into your project**

   ```bash
   cp -r AgentQMS/ your_project/
   cp -r .agentqms your_project/
   ```

   (You usually do **not** copy `docs/` when exporting the framework; those are
   project-specific history for this repo.)

2. **Configure paths and behavior (optional)**

   - Preferred: create or edit `your_project/.agentqms/settings.yaml`.
   - Alternative for consuming projects: use `your_project/config/` with
     `framework.yaml`, `interface.yaml`, and `paths.yaml`.

3. **Run basic checks via the interface**

   ```bash
   cd your_project/AgentQMS/interface
   make discover
   make status
   make validate
   make compliance
   ```

4. **(Optional) Run project adaptation helpers**

   ```bash
   python AgentQMS/agent_tools/utilities/adapt_project.py --help
   ```

## High-Level Layout

```text
project_root/
├── AgentQMS/
│   ├── interface/
│   ├── agent_tools/
│   ├── conventions/
│   └── knowledge/
├── .agentqms/
├── docs/
│   ├── artifacts/
│   ├── audit/
│   └── ai_handbook/        # legacy handbook for this project only
└── README.md
```

## Key Capabilities

- **Artifact workflows** – `AgentQMS/agent_tools/core/artifact_workflow.py` creates,
  validates, and maintains QMS artifacts.
- **Validation & compliance** – `AgentQMS/agent_tools/compliance/*` enforces naming,
  structure, and boundary rules; integrates with CI and optional pre-commit hooks.
- **Audit framework** – tools and templates under
  `AgentQMS/conventions/audit_framework/` and `AgentQMS/agent_tools/audit/`.
- **Knowledge surface** – `AgentQMS/knowledge/*` provides agent-first protocols and
  references, with `.agentqms/state/architecture.yaml` acting as a compact index.

## License

This project is licensed under the MIT License – see [LICENSE](LICENSE).

