# Agent Tools

This directory contains all AgentQMS tooling with clear separation of concerns.

## Ultra-Concise CLI

**Simple Python CLI for all tools:**

```bash
# Discover available tools
python -m agent_tools.cli discover

# Create artifacts
python -m agent_tools.cli create-plan --name my-plan --title "My Plan"
python -m agent_tools.cli create-assessment --name my-assessment --title "My Assessment"

# Validate and compliance
python -m agent_tools.cli validate
python -m agent_tools.cli compliance

# Feedback and quality
python -m agent_tools.cli feedback
python -m agent_tools.cli quality

# Help
python -m agent_tools.cli help
```

## Directory Structure

```
agent_tools/
├── cli.py              # Ultra-concise CLI entry point
├── core/               # Core tools (discover, artifact_workflow, context_bundle)
├── compliance/         # Compliance and validation tools
├── audit/              # Audit tools
├── documentation/      # Documentation tools
├── maintenance/        # Maintenance tools
├── migration/          # Migration tools
├── integrations/       # External integrations
│   ├── mcp/            # MCP servers (audio, puppeteer)
│   └── semantic_search/ # Semantic search integration
├── utilities/          # Helper utilities
├── workflows/          # Workflow scripts
└── utils/              # Framework utilities (config, paths, state)
```

## Separation of Concerns

- **core/** - Essential automation tools
- **compliance/**, **audit/**, **documentation/** - Domain-specific tools
- **integrations/** - External service integrations (MCP servers, semantic search)
- **utilities/** - Shared helper functions
- **workflows/** - Workflow orchestration
- **utils/** - Framework-level utilities

## Direct Tool Access

You can also call tools directly:

```bash
# Discover tools
python -m agent_tools.core.discover

# Create artifact
python -m agent_tools.core.artifact_workflow create --type implementation_plan --name my-plan

# Validate
python -m agent_tools.compliance.validate_artifacts

# Compliance
python -m agent_tools.compliance.monitor_artifacts
```

## Benefits

- ✅ **Clear separation** - Core, domain, integrations, utilities
- ✅ **Single directory** - No confusion about where tools are
- ✅ **Simple CLI** - `python -m agent_tools.cli <command>`
- ✅ **No wrappers** - CLI calls implementations directly
- ✅ **No inappropriate `tools/`** - Proper categorization
- ✅ **Easy to discover** - `python -m agent_tools.cli help`
