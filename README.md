# AgentQMS - Quality Management System for Coding Agents

## ⚠️ Experimental POC

**Warning**: This project is an experimental Proof of Concept (POC) and is not ready for production use. It is under active development and may contain bugs, incomplete features, or breaking changes. Use at your own risk.

AgentQMS is a reusable Quality Management System designed to enhance AI coding agents' effectiveness. It enforces project conventions, automates quality checks, and improves context delivery to ensure consistent, high-quality code generation across development workflows.

## Features

- **Convention Enforcement**: Automated rules and protocols to maintain coding standards.
- **Context Enhancement**: Rich documentation and tooling for better agent understanding.
- **Modular Architecture**: Easily adaptable to various projects via scripts and templates.
- **Agent Collaboration**: Frameworks for multi-agent handoffs and workflows.
- **Quality Assurance**: Built-in tracking, compliance checks, and debugging tools.

## Benefits

- Reduce manual oversight in AI-assisted coding.
- Ensure scalable, reliable outputs across teams.
- Streamline onboarding for new agents and projects.
- Integrate seamlessly with existing development pipelines.

## Architecture

- `agent_tools/` - Core Python automation scripts for quality checks and tooling.
- `agent/` - Interface layer with Makefiles, wrappers, and configuration.
- `ai_handbook/` - Comprehensive protocols and guidelines for agents.
- `ai_agent/` - Domain-specific documentation and system rules.
- `scripts/` - Adaptation utilities for project integration.
- `docs/` - Guides, quick starts, and export documentation.

## Installation

See `docs/export_guide.md` for detailed installation instructions.

## Quick Start

1. Copy framework directories to your project:
   ```bash
   cp -r agent_tools/ your_project/scripts/
   cp -r agent/ your_project/
   cp -r ai_handbook/ your_project/docs/
   cp -r ai_agent/ your_project/docs/
   ```

2. Run adaptation script:
   ```bash
   python scripts/adapt_project.py --interactive
   ```

3. Verify installation:
   ```bash
   cd agent/
   make discover
   make status
   ```

## Excluded Components

The following project-specific components are excluded from this export:
- Streamlit UI dashboard features
- Project-specific data and outputs
- Project-specific configuration files
- Development artifacts (logs, caches, etc.)

## Contributing

[Add contribution guidelines here]

## License

[Add your license information here]