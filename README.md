# AI Collaboration Framework

A reusable framework for facilitating AI-to-human collaboration through standardized artifact generation, directory scaffolding, and project conventions.

## Overview

This framework provides:

- **AgentQMS (Quality Management System)**: Python toolbelt for programmatic artifact creation
- **Standardized Artifacts**: Templates and schemas for assessments, implementation plans, bug reports, and data contracts
- **Documentation Structure**: AI agent instructions and protocols
- **Automation Scripts**: Core tools for artifact management and validation
- **Cursor IDE Integration**: Rules and guidelines for AI agents

## Quick Start

### 1. Installation

Copy this framework to your project root:

```bash
cp -r ai-collaboration-framework/* /path/to/your/project/
```

### 2. Setup

1. **Install Python dependencies:**
   ```bash
   pip install pyyaml jinja2 jsonschema
   ```

2. **Configure Cursor IDE (optional):**
   - The `.cursor/rules/` directory contains rules for Cursor IDE
   - Cursor will automatically pick up these rules

3. **Verify installation:**
   ```python
   from agent_qms.toolbelt import AgentQMSToolbelt

   toolbelt = AgentQMSToolbelt()
   print(toolbelt.list_artifact_types())
   # Should output: ['implementation_plan', 'assessment', 'bug_report', 'data_contract']
   ```

### 3. Create Your First Artifact

```python
from agent_qms.toolbelt import AgentQMSToolbelt

toolbelt = AgentQMSToolbelt()
artifact_path = toolbelt.create_artifact(
    artifact_type="assessment",
    title="My First Assessment",
    content="## Summary\nThis is my assessment.",
    author="ai-agent",
    tags=["example"]
)

print(f"Created: {artifact_path}")
```

## Framework Components

### AgentQMS

The core framework package located in `agent_qms/`:

- `q-manifest.yaml` - Central configuration defining artifact types, templates, and schemas
- `templates/` - Markdown templates for each artifact type
- `schemas/` - JSON schemas for frontmatter validation
- `toolbelt/` - Python toolbelt for programmatic artifact creation

### Artifact Types

1. **Assessment** - Evaluation of a specific aspect of the system
2. **Implementation Plan** - Detailed plan for implementing features or changes
3. **Bug Report** - Bug documentation with root cause analysis
4. **Data Contract** - Data structure definitions with validation rules

### Standardized Frontmatter

All artifacts use a standardized frontmatter format:

```yaml
---
title: "Artifact Title"
author: "ai-agent"
timestamp: "2025-01-01 12:00 KST"  # KST format with hour and minute
branch: "main"  # Git branch name
status: "draft"  # draft | in-progress | completed
tags: []
---
```

### Documentation

- `docs/agents/` - AI agent instructions and protocols
  - `system.md` - Single source of truth for AI agent behavior
  - `protocols/` - Development, governance, and component protocols

### Automation Scripts

- `scripts/agent_tools/core/` - Core automation (artifact creation, discovery)
- `scripts/agent_tools/compliance/` - Validation and monitoring
- `scripts/agent_tools/documentation/` - Documentation management
- `scripts/agent_tools/utilities/` - Helper functions

## Usage Examples

### Creating an Assessment

```python
from agent_qms.toolbelt import AgentQMSToolbelt

toolbelt = AgentQMSToolbelt()
artifact_path = toolbelt.create_artifact(
    artifact_type="assessment",
    title="Performance Analysis",
    content="## Summary\n...",
    author="ai-agent",
    tags=["performance", "analysis"]
)
```

### Creating a Data Contract

```python
toolbelt = AgentQMSToolbelt()
artifact_path = toolbelt.create_artifact(
    artifact_type="data_contract",
    title="API Data Contract",
    content="## Overview\n...",
    author="ai-agent",
    tags=["api", "contract"]
)
```

### Validating an Artifact

```python
toolbelt = AgentQMSToolbelt()
is_valid = toolbelt.validate_artifact("artifacts/assessments/my-assessment.md")
```

## Customization

### Adding New Artifact Types

1. Add entry to `agent_qms/q-manifest.yaml`
2. Create template in `agent_qms/templates/`
3. Create schema in `agent_qms/schemas/`
4. Update toolbelt if needed (usually not required)

### Modifying Templates

Templates use Jinja2 syntax. Modify templates in `agent_qms/templates/` as needed.

## Migration Guide

If you have existing artifacts with the old frontmatter format:

1. **Old format** (deprecated):
   ```yaml
   ---
   title: "..."
   date: "2025-01-01"
   timestamp: "2025-01-01 12:00 KST"
   ---
   ```

2. **New format** (current):
   ```yaml
   ---
   title: "..."
   timestamp: "2025-01-01 12:00 KST"
   branch: "main"
   ---
   ```

**Changes:**
- Removed `date` field (redundant, date is in timestamp)
- Added `branch` field (required, git branch name)
- `timestamp` format unchanged (YYYY-MM-DD HH:MM KST)

## License

[Add your license here]

## Contributing

[Add contribution guidelines if applicable]

## Support

For issues or questions, see `docs/agents/system.md` for detailed documentation.
