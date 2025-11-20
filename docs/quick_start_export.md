---
title: "Quick Start: Exporting AI Agent Framework"
date: "2025-11-01 00:00 (KST)"
status: "active"
version: "1.0"
category: "user_guide"
tags: ["export", "framework", "quick_start", "ai_agent"]
---

# Quick Start: Exporting AI Agent Framework

This guide provides a quick-start approach to exporting and reusing the AI agent framework in other projects.

## 🚀 Quick Export Steps

### Step 1: Copy Framework Directories

```bash
# From your current project
cp -r AgentQMS/ export/AgentQMS/
# Note: .agentqms/ contains project-specific config - handle separately
# Framework defaults are in AgentQMS/config_defaults/
cp -r docs/ai_handbook/ export/ai_handbook/
```

### Step 2: Create Export Package

```bash
mkdir -p ai_agent_framework_export
cd ai_agent_framework_export

# Copy framework (containerized structure)
cp -r ../export/AgentQMS/ .
cp -r ../export/ai_handbook/ docs/

# Copy utilities
cp ../AgentQMS/agent_tools/utilities/adapt_project.py AgentQMS/agent_scripts/

# Copy documentation
cp ../docs/export_guide.md .
cp ../docs/quick_start_export.md .
```

### Step 3: Initialize Project Configuration

Create project-specific configuration:

```bash
# In new project root, create config/ directory
mkdir -p config

# Copy framework defaults as starting point (optional)
cp -r AgentQMS/config_defaults/* config/  # If you want to override defaults

# Or create minimal config files
touch config/framework.yaml config/interface.yaml config/paths.yaml
```

## 📦 Installing in a New Project

### Method 1: Manual Installation

```bash
# 1. Copy framework directory (containerized structure)
cp -r AgentQMS/ new_project/AgentQMS/
cp -r ai_handbook/ new_project/docs/

# 2. Create project config (optional - framework works with defaults)
cd new_project/
mkdir -p config
# Create config/framework.yaml, config/interface.yaml, config/paths.yaml if needed
# Framework defaults are in AgentQMS/config_defaults/

# 3. Verify installation
cd AgentQMS/agent_interface/
make discover
make status
```

### Method 2: Using Framework Tools

```bash
# 1. Copy framework (containerized structure)
cp -r AgentQMS/ new_project/AgentQMS/
cp -r ai_handbook/ new_project/docs/

# 2. Initialize project (if needed)
cd new_project/
# Create config/ directory for project overrides if needed
mkdir -p config

# 3. Verify installation
cd AgentQMS/agent_interface/
make discover
```

## ✅ Verification Checklist

After installation, verify:

- [ ] `cd AgentQMS/agent_interface/ && make discover` works
- [ ] `make status` shows correct paths
- [ ] `make create-plan NAME=test TITLE="Test"` creates artifact
- [ ] Documentation links work
- [ ] Project name appears correctly in handbook
- [ ] Configuration hierarchy works (defaults → project overrides → effective.yaml)

## 🔧 Common Issues

### Issue: "Tool not found" errors

**Solution**: Check configuration:
- Framework defaults are in `AgentQMS/config_defaults/`
- Project overrides in `config/` (if created)
- Effective merged config in `.agentqms/effective.yaml`
- Tool mappings are in `AgentQMS/config_defaults/tool_mappings.json`

### Issue: Project name not replaced

**Solution**: Manually update:
- `docs/ai_handbook/index.md`
- `docs/ai_handbook/01_onboarding/01_project_overview.md`

### Issue: Broken documentation links

**Solution**: Update relative paths in handbook files to match your project structure.

## 📚 Next Steps

1. Read `export_guide.md` for detailed information
2. Review `AgentQMS/config_defaults/` for available configuration options
3. Create `config/` directory for project-specific overrides (optional)
4. Customize `docs/ai_handbook/01_onboarding/01_project_overview.md` for your project
5. Test all tools: `cd AgentQMS/agent_interface/ && make help`

## 🆘 Need Help?

- See `export_guide.md` for comprehensive documentation
- Check `AgentQMS/config_defaults/` for configuration options
- Review `.agentqms/effective.yaml` for merged configuration
- Check `AgentQMS/agent_tools/README.md` for tool documentation
- Review `docs/ai_handbook/index.md` for handbook structure
