# AgentQMS Framework (Version: v002_b)

AgentQMS is a reusable Quality Management Framework that standardizes
artifact creation, documentation workflows, and automation for collaborative
AI coding. The v002_b release introduces the containerized layout so the
entire framework can travel as a single directory.

## Framework Contents

### AgentQMS/ (Framework Container)
- `agent/` – Interface layer (Makefile, wrappers, workflows)
- `agent_tools/` – Implementation layer (automation, validators, docs tooling)
- `conventions/` – Templates, schemas, and QMS conventions (formerly quality_management_framework)
- `agent_scripts/` – Framework scripts and utilities
- `config/` – Default framework configuration (`framework.yaml`)
- `templates/` – Bootstrap templates for exporting/adapting

### Project-Level Directories
- `artifacts/` – Generated artifacts (configurable via `.agentqms/config.yaml`)
- `docs/` – Project documentation (handbook + local docs)
- `ai_handbook/`, `ai_agent/`, `agent_templates/` – Documentation and template packs
- `.agentqms/` – Hidden metadata directory (version, config, state)

## Installation

1. **Copy the framework container**
   ```bash
   cp -r AgentQMS/ your_project/
   cp -r ai_handbook/ your_project/docs/
   cp -r ai_agent/ your_project/docs/
   cp -r agent_templates/ your_project/
   cp -r artifacts/ your_project/
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
   cd AgentQMS/agent
   make discover
   make status
   make validate
   ```

## Framework Structure

```
project_root/
├── AgentQMS/
│   ├── agent/
│   ├── agent_tools/
│   ├── conventions/
│   ├── agent_scripts/
│   ├── config/
│   └── templates/
├── .agentqms/
├── artifacts/
├── docs/
├── ai_handbook/
├── ai_agent/
├── agent_templates/
└── README.md
```

## Key Features
- **Containerized Distribution** – All framework code lives inside `AgentQMS/`.
- **Metadata Directory** – `.agentqms/` tracks version, configuration, and future state.
- **Path & Config Loader** – Centralized resolver ensures consistent CLI behavior.
- **Boundary Validation** – Automated guardrails prevent framework/project drift.
- **State Hooks** – JSON-backed placeholder ready for future SQLite/external stores.

## Documentation
- `docs/audit/` – Current audit, containerization design, and migration guides.
- `ai_handbook/` – AI agent handbook (protocols, onboarding, references).
- `ai_agent/` – System documentation for agents and automation tooling.

## License
This project is licensed under the MIT License – see [LICENSE](LICENSE).
