# AI Agent Framework Export

This package contains the AI collaboration and documentation management framework.

## Contents

- `agent_tools/` - Implementation layer (Python automation scripts)
- `agent/` - Interface layer (Makefile, wrappers, config)
- `ai_handbook/` - AI agent documentation and protocols
- `ai_agent/` - AI agent domain documentation
- `scripts/` - Adaptation scripts
- `docs/` - Export documentation

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

## License

[Add your license information here]
