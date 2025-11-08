---
title: "Quick Start: Exporting AI Agent Framework"
date: "2025-11-01"
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
cp -r docs/ai_handbook/ export/ai_handbook/
cp -r agent/ export/agent/
cp -r scripts/agent_tools/ export/agent_tools/
```

### Step 2: Create Export Package

```bash
mkdir -p ai_agent_framework_export
cd ai_agent_framework_export

# Copy framework
cp -r ../export/ai_handbook/ .
cp -r ../export/agent/ .
cp -r ../export/agent_tools/ scripts/

# Copy utilities
cp ../scripts/agent_tools/utilities/adapt_project.py scripts/
cp ../docs/ai_handbook/config/project_config.yaml.template config/

# Copy documentation
cp ../docs/export_guide.md .
cp ../docs/QUICK_START.md .  # This file
```

### Step 3: Abstract Project-Specific Content

Run the adaptation script in dry-run mode first:

```bash
python scripts/adapt_project.py --create-config
# Edit project_config.yaml.template with your project details
python scripts/adapt_project.py --config config/project_config.yaml.template --dry-run
```

## 📦 Installing in a New Project

### Method 1: Manual Installation

```bash
# 1. Copy directories
cp -r ai_handbook/ new_project/docs/
cp -r agent/ new_project/
cp -r scripts/agent_tools/ new_project/scripts/

# 2. Create project config
cd new_project/
cp docs/ai_handbook/config/project_config.yaml.template docs/ai_handbook/config/project_config.yaml
# Edit project_config.yaml with your project details

# 3. Run adaptation
python scripts/agent_tools/utilities/adapt_project.py --config docs/ai_handbook/config/project_config.yaml

# 4. Verify installation
cd agent/
make discover
make status
```

### Method 2: Using Adaptation Script

```bash
# 1. Copy framework
cp -r ai_handbook/ new_project/docs/
cp -r agent/ new_project/
cp -r scripts/agent_tools/ new_project/scripts/

# 2. Run interactive setup
cd new_project/
python scripts/agent_tools/utilities/adapt_project.py --interactive

# 3. Verify installation
cd agent/
make discover
```

## ✅ Verification Checklist

After installation, verify:

- [ ] `cd agent/ && make discover` works
- [ ] `make status` shows correct paths
- [ ] `make create-plan NAME=test TITLE="Test"` creates artifact
- [ ] Documentation links work
- [ ] Project name appears correctly in handbook
- [ ] Tool paths are correct

## 🔧 Common Issues

### Issue: "Tool not found" errors

**Solution**: Check paths in `agent/config/tool_mappings.json`:
```json
{
  "tool_mappings": {
    "artifact_workflow": {
      "path": "../scripts/agent_tools/core/artifact_workflow.py"
    }
  }
}
```

### Issue: Project name not replaced

**Solution**: Manually update:
- `docs/ai_handbook/index.md`
- `docs/ai_handbook/01_onboarding/01_project_overview.md`

### Issue: Broken documentation links

**Solution**: Update relative paths in handbook files to match your project structure.

## 📚 Next Steps

1. Read `export_guide.md` for detailed information
2. Customize `docs/ai_handbook/01_onboarding/01_project_overview.md` for your project
3. Update `docs/ai_handbook/03_references/development/ai_agent_context.md` with project-specific patterns
4. Test all tools: `cd agent/ && make help`

## 🆘 Need Help?

- See `export_guide.md` for comprehensive documentation
- Check `scripts/agent_tools/README.md` for tool documentation
- Review `docs/ai_handbook/index.md` for handbook structure
