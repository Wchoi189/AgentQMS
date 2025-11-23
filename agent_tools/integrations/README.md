# Integrations

This directory contains external integrations and specialized tools that connect AgentQMS with external services or provide specialized functionality.

## Structure

```
integrations/
├── mcp/                  # Model Context Protocol servers
│   ├── audio/            # Audio MCP server
│   └── puppeteer/        # Puppeteer MCP server
└── semantic_search.py    # Semantic search integration
```

## MCP Servers

MCP (Model Context Protocol) servers provide specialized functionality for AI agents:

- **audio/** - Audio message generation and management
- **puppeteer/** - Browser automation via Puppeteer

## Usage

These integrations are typically used by MCP clients or called directly from agent workflows. They are not part of the main CLI but can be imported and used programmatically.

