# AgentQMS Framework (Version: v002_b)

AgentQMS is a reusable Quality Management Framework that standardizes
artifact creation, documentation workflows, and automation for collaborative
AI coding. The v002_b release introduces the containerized layout so the
entire framework can travel as a single directory.

## Framework Contents

### AgentQMS/ (Framework Container)
- `agent_interface/` – Interface layer (Makefile, wrappers, workflows)
- `agent_tools/` – Implementation layer (automation, validators, docs tooling)
- `project_conventions/` – Templates, schemas, and QMS conventions
- `agent_scripts/` – Framework scripts and utilities
- `config_defaults/` – Canonical framework defaults (framework/interface/paths)
- `templates/` – Bootstrap templates for exporting/adapting

### Project-Level Directories
- `docs/` – Project documentation and artifacts
  - `docs/artifacts/` – Generated artifacts (implementation plans, assessments, templates, etc.)
  - `docs/ai_handbook/` – AI agent handbook (protocols, onboarding, references) including the `04_agent_system/` section for agent-only operations.
  - `docs/audit/` – Framework audit and design documents
- `.agentqms/` – Hidden metadata directory (version, config, state)

## Installation

1. **Copy the framework container and documentation**
   ```bash
   cp -r AgentQMS/ your_project/
   cp -r docs/ your_project/          # Includes artifacts, ai_handbook (agent system), audit
   cp -r .agentqms your_project/
   ```

2. **Configure the project**
   ```bash
   cd your_project
   python AgentQMS/agent_scripts/adapt_project.py --interactive
   ```
   or edit `.agentqms/config.yaml` to specify custom artifact/doc paths.

3. **Verify installation**
   ```bash
   cd AgentQMS/agent_interface
   make discover
   make status
   make validate
   ```

## Framework Structure

```
project_root/
├── AgentQMS/
│   ├── agent_interface/
│   ├── agent_tools/
│   ├── project_conventions/
│   ├── agent_scripts/
│   ├── config_defaults/
│   └── templates/
├── .agentqms/
├── docs/
│   ├── artifacts/
│   ├── ai_handbook/
│   │   └── 04_agent_system/
│   └── audit/
└── README.md
```

## Key Features
- **Containerized Distribution** – All framework code lives inside `AgentQMS/`.
- **Metadata Directory** – `.agentqms/` tracks version, configuration, and future state.
- **Path & Config Loader** – Centralized resolver ensures consistent CLI behavior.
- **Boundary Validation** – Automated guardrails prevent framework/project drift.
- **State Hooks** – JSON-backed placeholder ready for future SQLite/external stores.

## Documentation
- `docs/artifacts/` – Generated project artifacts (implementation plans, assessments, design documents, templates)
- `docs/ai_handbook/` – AI agent handbook (protocols, onboarding, references) with the `04_agent_system/` subsection for agent tooling docs
- `docs/audit/` – Framework audit, containerization design, and migration guides

## License
This project is licensed under the MIT License – see [LICENSE](LICENSE).
