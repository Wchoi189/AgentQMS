# AgentQMS Framework

AgentQMS is a reusable Quality Management Framework that standardizes
artifact creation, documentation workflows, and automation for collaborative
AI coding. The framework is **containerized** so it can travel between projects
as a pair of directories: `.agentqms/` + `AgentQMS/`.

---

## 🤖 For AI Agents: Getting Started

### Auto-Discovery (GitHub Copilot Spaces)

**AgentQMS is automatically discoverable in GitHub Copilot Spaces!** No manual instructions needed.

The framework provides auto-discovery files that Copilot automatically reads:
- **`.github/copilot-instructions.md`** – Primary entry point directing Copilot to framework
- **`.copilot/context/`** – Auto-scanned context files:
  - `agentqms-overview.md` – Framework overview
  - `tool-registry.json` – Machine-readable tool registry
  - `tool-catalog.md` – Human-readable tool catalog
  - `workflow-triggers.yaml` – Task → workflow mapping
  - `context-bundles-index.md` – Available context bundles

**Features**:
- ✅ **Auto-discovery**: Tools and workflows automatically registered
- ✅ **Context-aware suggestions**: Detects task type and suggests relevant tools/context
- ✅ **Workflow automation**: Auto-executes validation after artifact creation
- ✅ **Proactive guidance**: Suggests next steps based on current task

### Cursor AI Instructions

Cursor doesn't automatically read `.copilot/context/`, so a dedicated ultra-short instruction file is provided for Cursor agents:

- File: `.cursor/plans/instructions.md`
- Usage: pin or paste into Cursor's Custom Instructions so every session knows to follow the AgentQMS SST, use automation, run validation, and load context via `make context`.

This keeps Cursor aligned with the same rules Copilot uses while staying within Cursor's tighter instruction window.

### First Contact: What to Read

When an AI agent encounters a project using AgentQMS, these are the **entry points** in priority order:

| Priority | File | Purpose |
|----------|------|---------|
| 1️⃣ | `AgentQMS/knowledge/agent/system.md` | **Single Source of Truth** – Core rules, do/don't, artifact creation |
| 2️⃣ | `.agentqms/state/architecture.yaml` | Component map, capabilities, tool locations |
| 3️⃣ | `.copilot/context/tool-catalog.md` | Available automation tools (auto-generated) |
| 4️⃣ | `AgentQMS/knowledge/agent/tool_catalog.md` | Legacy tool catalog |
| 5️⃣ | This README | Framework overview and installation |

### Quick Onboarding Prompt

Copy this prompt to quickly orient an AI agent to this framework:

```
You are working in a project that uses AgentQMS for quality management.

FIRST: Read these files to understand the framework:
1. AgentQMS/knowledge/agent/system.md (core rules - REQUIRED)
2. .agentqms/state/architecture.yaml (component map)

KEY RULES:
- Use automation tools; never create artifacts manually
- Run `cd AgentQMS/interface && make help` to see available commands
- Artifacts go in artifacts/ with proper naming: YYYY-MM-DD_HHMM_[type]_name.md
- Validate changes: `make validate` and `make compliance`

When creating implementation plans, assessments, or bug reports, use:
  cd AgentQMS/interface && make create-plan NAME=my-plan TITLE="My Title"
```

### Encouraging Proactive Use

To make the AI agent **proactively** use AgentQMS, include these instructions in your system prompt or project rules:

```
QUALITY MANAGEMENT RULES:
1. Before starting any significant task, check if an implementation plan exists
2. For multi-step work, create an implementation plan first:
   cd AgentQMS/interface && make create-plan NAME=feature-name TITLE="Feature Title"
3. After completing work, run validation:
   cd AgentQMS/interface && make validate && make compliance
4. Document bugs using the bug report workflow, not ad-hoc notes
5. When stuck, run `make discover` to see available tools
```

### Agent Interface Commands

All agent commands are run from `AgentQMS/interface/`:

```bash
cd AgentQMS/interface

# Discovery & Status
make help              # Show all available commands
make discover          # List available tools
make status            # Framework status check

# Artifact Creation
make create-plan NAME=my-plan TITLE="My Plan"
make create-assessment NAME=my-assessment TITLE="My Assessment"
make create-bug-report NAME=my-bug TITLE="Bug Description"

# Validation
make validate          # Validate all artifacts
make compliance        # Full compliance check
make boundary          # Boundary validation

# Context Loading (for focused work)
make context TYPE=development    # Load development context
make context TYPE=debugging      # Load debugging context
make context TYPE=planning       # Load planning context

# Plugin Management
make plugin-list       # List registered plugins (if available)

# Registry Generation (for auto-discovery)
make generate-registry  # Regenerate tool registries and context files
```

---

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
  - `plugins/` – project-specific plugin extensions.
- `artifacts/` – QMS artifacts (implementation plans, assessments, bug reports).
- `.copilot/context/` – Auto-discovery context files (for GitHub Copilot Spaces):
  - `agentqms-overview.md` – Framework overview
  - `tool-registry.json` – Machine-readable tool registry
  - `tool-catalog.md` – Human-readable tool catalog
  - `workflow-triggers.yaml` – Task → workflow mapping
  - `context-bundles-index.md` – Context bundles reference
- `.cursor/` – Cursor-specific instructions and plans (`.cursor/plans/instructions.md`) for pinning concise SST reminders inside Cursor IDE.

---

## Installation

### Option A: Install as a Python Package (Recommended)

```bash
# Clone and install in editable mode
git clone https://github.com/your-org/agent_qms.git
cd agent_qms
pip install -e .

# Verify installation
python -c "import AgentQMS; print(AgentQMS.__version__)"
```

### Option B: Copy into Your Project

```bash
cp -r AgentQMS/ your_project/
cp -r .agentqms your_project/
mkdir -p your_project/artifacts
```

---

## Plugin System (Extensibility)

AgentQMS supports project-level extensions via plugins. Define custom:

- **Artifact Types** – New document types with custom templates
- **Validators** – Additional validation rules and prefixes
- **Context Bundles** – Task-specific context file collections

### Plugin Directory Structure

```
.agentqms/plugins/
├── artifact_types/           # Custom artifact type definitions
│   └── change_request.yaml   # Example: Change request type
├── validators.yaml           # Validator extensions (prefixes, types, categories)
└── context_bundles/          # Custom context bundles
    └── security-review.yaml  # Example: Security review bundle
```

### Using Plugins

```bash
# List registered plugins
python -m AgentQMS.agent_tools.core.plugins --list

# Validate plugin definitions
python -m AgentQMS.agent_tools.core.plugins --validate

# View specific plugin
python -m AgentQMS.agent_tools.core.plugins --show change_request
```

See `AgentQMS/conventions/schemas/plugin_*.json` for plugin schema documentation.

---

## High-Level Layout

```text
project_root/
├── AgentQMS/                  # Framework container
│   ├── interface/             # Agent commands (Makefile)
│   ├── agent_tools/           # Implementation layer
│   ├── conventions/           # Schemas, templates, audit framework
│   └── knowledge/             # Documentation surface
│       ├── agent/             # AI agent instructions (SST)
│       ├── protocols/         # Governance, development protocols
│       └── references/        # Technical references
├── .agentqms/                 # Framework state
│   ├── settings.yaml          # Project configuration
│   ├── state/architecture.yaml
│   └── plugins/               # Project extensions
├── artifacts/                 # QMS artifacts
└── README.md
```

---

## Key Capabilities

- **Artifact workflows** – `AgentQMS/agent_tools/core/artifact_workflow.py` creates,
  validates, and maintains QMS artifacts.
- **Validation & compliance** – `AgentQMS/agent_tools/compliance/*` enforces naming,
  structure, and boundary rules; integrates with CI and optional pre-commit hooks.
- **Audit framework** – tools and templates under
  `AgentQMS/conventions/audit_framework/` and `AgentQMS/agent_tools/audit/`.
- **Knowledge surface** – `AgentQMS/knowledge/*` provides agent-first protocols and
  references, with `.agentqms/state/architecture.yaml` acting as a compact index.
- **Plugin extensibility** – Define custom artifact types, validators, and context
  bundles in `.agentqms/plugins/`.
- **Auto-discovery** – Automatic tool registration, workflow suggestions, and context
  loading for GitHub Copilot Spaces and compatible AI agents.

---

## For Maintainers

- **Maintainer Guide**: `AgentQMS/knowledge/meta/MAINTAINERS.md`
- **Framework Design**: `AgentQMS/knowledge/meta/framework_maintenance_design.md`
- **Audit Framework**: `AgentQMS/conventions/audit_framework/README.md`

---

## License

This project is licensed under the MIT License – see [LICENSE](LICENSE).
