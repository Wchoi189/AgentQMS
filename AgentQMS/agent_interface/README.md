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

This directory is the **Agent-Only Interface Layer** that provides convenience commands for AI agents. All actual tool implementations live in `AgentQMS/agent_tools/`.

**Relationship**:
- `agent/` = Thin wrapper layer (Makefile, wrappers, config)
- `AgentQMS/agent_tools/` = Implementation layer (actual Python scripts)

**See**: `index.md` for detailed architecture documentation.

### **🚫 Human Access Restrictions**

- **DO NOT** run commands from this directory
- **DO NOT** modify files in this directory
- **DO NOT** use the agent Makefile
- **USE** the main project Makefile instead
- **USE** `AgentQMS/agent_tools/` directly for tool implementations

### **🤖 Agent Usage**

**Migration Notice (Java Toolchain):** the legacy Python Makefile and wrapper scripts
have been archived while we stand up the new Maven-based CLI. Use the steps below
to exercise the placeholder Java tooling until the interface is fully restored.

1. **Install prerequisites (one time)**  
   ```bash
   sudo apt-get update
   sudo apt-get install -y maven openjdk-21-jdk-headless
   ```
2. **Build the Maven workspace**  
   ```bash
   mvn -f AgentQMS/java-tools/pom.xml install -DskipTests
   ```
3. **Run the Java CLI**  
   From repo root:
   ```bash
   mvn -f AgentQMS/java-tools/pom.xml -pl cli -am exec:java \
     -Dexec.mainClass=com.agentqms.cli.AgentQmsCli -Dexec.args="status"
   ```
   or from the module directory:
   ```bash
   cd AgentQMS/java-tools/cli
   mvn exec:java -Dexec.mainClass=com.agentqms.cli.AgentQmsCli -Dexec.args="status"
   ```
4. **Command routing (temporary)**  
   The placeholder CLI understands `status`, `artifact`, `validate`, `docs`, and
   `audit` subcommands (currently stubs that confirm wiring). Future updates will
   reintroduce full workflows and new agent-facing wrappers.

Until the new CLI exposes feature parity, defer to documentation updates in
`docs/artifacts/implementation_plans/2025-11-20_implementation_plan_java_toolchain.md`.

### **📁 Directory Structure**

```
agent/
├── index.md             # Architecture documentation
├── README.md            # This file
├── Makefile             # Agent-only Makefile (main entry point)
├── tools/               # Thin wrapper scripts
│   ├── ast_analysis.py  # Wraps streamlit_app/services/ast_service/ and scripts/ast_analysis_cli.py
│   ├── discover.py      # Wraps AgentQMS/agent_tools/core/discover.py
│   ├── feedback.py      # Wraps AgentQMS/agent_tools/utilities/agent_feedback.py
│   └── quality.py       # Wraps AgentQMS/agent_tools/compliance/documentation_quality_monitor.py
├── workflows/           # Agent workflow scripts
│   ├── create-artifact.sh
│   ├── validate.sh
│   └── compliance.sh
├── config/              # Agent configuration
│   ├── agent_config.yaml
│   └── tool_mappings.json
└── logs/                # Agent activity logs
    ├── feedback/
    └── quality/
```

**Note**: All actual implementations are in `AgentQMS/agent_tools/`. This directory provides convenience wrappers.

### **🎯 Quick Start for Agents**

Legacy Make targets are unavailable during the migration. Use the Maven commands
outlined above to exercise the Java CLI until replacement wrappers land. Updated
quick-start instructions will return once the new interface is stabilized.

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
