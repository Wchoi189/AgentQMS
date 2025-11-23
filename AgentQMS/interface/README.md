---
title: "Agent Directory Usage Guide"
date: "2025-11-01T18:00:00Z"
type: "documentation"
category: "usage"
status: "active"
version: "1.0"
tags: ["agent", "usage", "documentation"]
---

# Agent-Only Directory

## ⚠️ **IMPORTANT: AGENT-ONLY ACCESS**

This directory contains tools and workflows **exclusively for AI agents**. Humans should **NOT** use these tools directly.

## 🏗️ **Architecture**

This directory is the **Agent-Only Interface Layer** that provides convenience commands for AI agents. All actual tool implementations live in `AgentQMS/toolkit/`.

**Relationship**:
- `interface/` = Thin wrapper layer (Makefile, CLI wrappers, workflows)
- `AgentQMS/toolkit/` = Implementation layer (actual Python packages and scripts)

**See**: `index.md` for detailed architecture documentation.

### **🚫 Human Access Restrictions**

- **DO NOT** run commands from this directory
- **DO NOT** modify files in this directory
- **DO NOT** use the agent Makefile
- **USE** the main project Makefile instead
- **USE** `AgentQMS/toolkit/` directly for tool implementations

### **🤖 Agent Usage**

AI agents should:

1. **Navigate to this directory**: `cd AgentQMS/interface/`
2. **Use the agent Makefile**: `make help`
3. **Follow agent-specific workflows**: `make workflow-create`
4. **Report issues**: `make feedback-issue`

### **📁 Directory Structure**

```text
interface/
├── index.md             # Architecture documentation
├── README.md            # This file
├── Makefile             # Agent-only Makefile (main entry point)
├── cli_tools/           # Thin wrapper scripts
│   ├── ast_analysis.py  # Wraps scripts/ast_analysis_cli.py
│   ├── discover.py      # Wraps AgentQMS/toolkit/core/discover.py
│   ├── feedback.py      # Wraps AgentQMS/toolkit/utilities/agent_feedback.py
│   └── quality.py       # Wraps AgentQMS/toolkit/compliance/documentation_quality_monitor.py
├── workflows/           # Agent workflow scripts
│   ├── create-artifact.sh
│   ├── validate.sh
│   └── compliance.sh
└── logs/                # Agent activity logs
    ├── feedback/
    └── quality/
```

**Note**: All actual implementations are in `AgentQMS/toolkit/`. This directory provides convenience wrappers.

### **🎯 Quick Start for Agents**

```bash
# Navigate to agent interface directory
cd AgentQMS/interface/

# Show available commands
make help

# Discover tools
make discover

# Check system status
make status

# Create artifacts
make create-plan NAME=my-plan TITLE="My Plan"

# Validate work
make validate
make compliance

# Get context bundles for tasks
make context TASK="implement new feature"
make context-development
make context-docs
make context-debug
make context-plan
make context-list

# Report issues
make feedback-issue ISSUE="Description" FILE="path/to/file"

# AST Code Analysis (NEW)
make ast-analyze                       # Analyze codebase structure
make ast-analyze TARGET=streamlit_app/ # Analyze specific path
make ast-check-quality                 # Check code quality
make ast-generate-tests TARGET=file.py # Generate test scaffolds
make ast-extract-docs TARGET=file.py   # Extract documentation
```

### **🔒 Security Notes**

- All tools in this directory are **agent-only**
- Human access is **restricted** by design
- Agent tools have **limited scope** and **controlled access**
- All agent activity is **logged** for monitoring

### **📞 Support**

**For Human Developers**:
- Use the main project Makefile
- Use tools in `AgentQMS/agent_tools/` directly
- Do NOT use this agent directory
- See `AgentQMS/agent_tools/README.md` for tool usage

**For AI Agents**:
- Use this directory for all automation tasks (`cd AgentQMS/agent_interface/` then `make help`)
- Follow the agent workflows
- Report any issues using the feedback system
- See `index.md` for architecture details

**Related Documentation**:
- `index.md` - Architecture and design principles
- `AgentQMS/agent_tools/index.md` - Implementation layer architecture
- `AgentQMS/agent_tools/README.md` - Tool implementation guide
