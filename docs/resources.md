---
title: "Useful Resources for Exporting AI Agent Framework"
date: "2025-11-01 00:00 (KST)"
status: "active"
version: "1.0"
category: "user_guide"
tags: ["export", "framework", "resources", "ai_agent"]
---

# Useful Resources for Exporting AI Agent Framework

This document lists all useful resources for exporting and reusing the AI agent framework.

> **Containerized Framework (v002_b)**  
> Always copy the full `AgentQMS/` directory **and** the hidden `.agentqms/`
> metadata folder when exporting the framework. The metadata directory contains
> version/config/state that the tooling now expects.

## 📁 Core Framework Components

### 1. `AgentQMS/agent_tools/` - Implementation Layer

**Status**: ✅ **95% Ready for Export** (Minimal changes needed)

**What's Included**:
- `core/` - Artifact creation, discovery, templates
- `compliance/` - Validation and monitoring tools
- `documentation/` - Index generation, link validation
- `utilities/` - Context tools, feedback system
- `maintenance/` - One-time fix scripts

**Key Files**:
- `core/artifact_workflow.py` - Main artifact creation tool
- `core/discover.py` - Tool discovery system
- `core/artifact_templates.py` - Generic artifact templates
- `compliance/validate_artifacts.py` - Validation system
- `utilities/adapt_project.py` - **NEW**: Project adaptation script

**Export Readiness**: ✅ Ready - Only path verification needed

---

### 2. `agent/` - Interface Layer

**Status**: ✅ **90% Ready for Export** (Config template needed)

**What's Included**:
- `Makefile` - Command interface (uses relative paths)
- `config/` - Configuration files
- `tools/` - Thin wrapper scripts
- `workflows/` - Workflow scripts

**Key Files**:
- `Makefile` - Complete command interface
- `config/agent_config.yaml` - Agent configuration
- `config/tool_mappings.json` - Tool path mappings
- `README.md` - Usage guide

**Export Readiness**: ✅ Ready - Only config template creation needed

---

### 3. `docs/ai_handbook/` - Documentation

**Status**: ⚠️ **60% Ready for Export** (Needs abstraction)

**What's Included**:
- `02_protocols/` - ✅ **Generic protocols** (Keep as-is)
- `03_references/` - ⚠️ **Mixed** (Some generic, some project-specific)
- `01_onboarding/` - ❌ **Project-specific** (Needs templates)

**Key Generic Files** (Keep as-is):
- `02_protocols/governance/01_artifact_management_protocol.md` ✅
- `02_protocols/governance/02_implementation_plan_protocol.md` ✅
- `02_protocols/development/01_coding_standards_v2.md` ✅
- `02_protocols/development/22_proactive_modularity_protocol.md` ✅
- `02_protocols/development/23_import_handling_protocol.md` ✅

**Files Needing Abstraction**:
- `index.md` - Project name and structure
- `01_onboarding/01_project_overview.md` - Entire file
- `01_onboarding/03_data_overview.md` - Project-specific data
- `03_references/development/ai_agent_context.md` - Project-specific patterns

**Export Readiness**: ⚠️ Needs template creation for project-specific sections

---

## 🛠️ Tools and Scripts

### Adaptation Tools

1. **`AgentQMS/agent_tools/utilities/adapt_project.py`** ✅ **NEW**
   - Automated project adaptation
   - Interactive setup wizard
   - Config file generation
   - Dry-run mode for testing

2. **`docs/ai_handbook/config/project_config.yaml.template`** ✅ **NEW**
   - Template for project configuration
   - Includes all necessary fields
   - Well-documented

### Discovery Tools

1. **`AgentQMS/agent_tools/core/discover.py`**
   - Lists all available tools
   - Shows tool descriptions
   - Provides usage examples

2. **`agent/Makefile`** - `make discover`
   - Convenient wrapper for discovery
   - Shows tool organization

### Validation Tools

1. **`AgentQMS/agent_tools/compliance/validate_artifacts.py`**
   - Validates naming conventions
   - Checks frontmatter
   - Ensures compliance

2. **`AgentQMS/agent_tools/compliance/monitor_artifacts.py`**
   - Compliance monitoring
   - Issue detection
   - Status reporting

---

## 📚 Documentation Resources

### Export Documentation

1. **`docs/export_guide.md`** ✅ **NEW**
   - Comprehensive export guide
   - Step-by-step instructions
   - Abstraction strategies
   - Complete checklist

2. **`docs/quick_start_export.md`** ✅ **NEW**
   - Quick-start guide
   - Fast installation steps
   - Common issues and solutions

### Framework Documentation

1. **`docs/ai_handbook/04_agent_system/system.md`**
   - Single source of truth for agents
   - Core rules and guidelines
   - Quick reference

2. **`AgentQMS/agent_tools/README.md`**
   - Tool implementation guide
   - Usage examples
   - Architecture overview

3. **`agent/README.md`**
   - Agent interface guide
   - Usage instructions
   - Quick start

---

## 🎯 What to Export

### ✅ **Export As-Is** (No Changes Needed)

These are already generic and ready:

```
AgentQMS/agent_tools/
├── core/
│   ├── artifact_workflow.py       ✅ Generic
│   ├── discover.py                 ✅ Generic
│   └── artifact_templates.py       ✅ Generic templates
├── compliance/
│   ├── validate_artifacts.py       ✅ Generic
│   └── monitor_artifacts.py        ✅ Generic
├── documentation/
│   ├── auto_generate_index.py      ✅ Generic
│   └── validate_links.py           ✅ Generic
└── utilities/
    ├── adapt_project.py            ✅ NEW - Generic
    └── get_context.py               ✅ Generic

agent/
├── Makefile                         ✅ Generic (relative paths)
├── tools/                           ✅ Generic wrappers
└── workflows/                       ✅ Generic scripts

docs/ai_handbook/
└── 02_protocols/                   ✅ Generic protocols
    ├── governance/                  ✅ Generic
    └── development/                 ✅ Generic
```

### ⚠️ **Export with Templates** (Need Abstraction)

Create templates for:

```
docs/ai_handbook/
├── index.md                         ⚠️ Create template
├── 01_onboarding/
│   ├── 01_project_overview.md       ⚠️ Create template
│   └── 03_data_overview.md           ⚠️ Create template
└── 03_references/development/
    └── ai_agent_context.md           ⚠️ Create template
```

### 📝 **Create New** (For Export Package)

1. **`project_config.yaml.template`** ✅ Created
2. **`adapt_project.py`** ✅ Created
3. **`export_guide.md`** ✅ Created
4. **`quick_start_export.md`** ✅ Created

---

## 🔍 Finding Project-Specific Content

### Search Commands

```bash
# Find project name references
grep -ri "upstage\|prompt.*hack\|korean.*grammar" docs/ai_handbook/

# Find specific file references
grep -ri "prompts\.py\|grammar_correction\|streamlit_app" docs/ai_handbook/

# Find project structure references
grep -ri "upstage-prompt\|project.*structure" docs/ai_handbook/

# Find API references
grep -ri "Solar Pro\|solar.*pro" docs/ai_handbook/
```

### Key Files to Review

1. **`docs/ai_handbook/index.md`**
   - Lines 2-5: Project name and purpose
   - Lines 11-17: Project components
   - Lines 45-60: Project structure
   - Lines 116-128: Project-specific tasks

2. **`docs/ai_handbook/01_onboarding/01_project_overview.md`**
   - Entire file: Project-specific overview

3. **`docs/ai_handbook/03_references/development/ai_agent_context.md`**
   - Lines 12-56: Project-specific patterns

---

## 📋 Export Checklist

### Preparation
- [ ] Backup current project
- [ ] Identify project-specific content
- [ ] Document dependencies

### Create Templates
- [ ] Create `project_config.yaml.template` ✅ Done
- [ ] Create template for `index.md`
- [ ] Create template for `01_project_overview.md`
- [ ] Create template for `ai_agent_context.md`

### Create Tools
- [ ] Create `adapt_project.py` ✅ Done
- [ ] Create export documentation ✅ Done
- [ ] Test adaptation script

### Package Export
- [ ] Copy generic files
- [ ] Copy templates
- [ ] Include adaptation script
- [ ] Include documentation
- [ ] Create README

### Test Export
- [ ] Test in new project
- [ ] Verify all tools work
- [ ] Check documentation links
- [ ] Validate paths

---

## 🚀 Quick Export Command

```bash
# Quick export script (save as export_framework.sh)
#!/bin/bash

mkdir -p ai_agent_framework_export
cd ai_agent_framework_export

# Copy framework
cp -r ../docs/ai_handbook/ .
cp -r ../agent/ .
cp -r ../AgentQMS/agent_tools/ scripts/

# Copy utilities
cp ../AgentQMS/agent_tools/utilities/adapt_project.py scripts/
cp ../docs/ai_handbook/config/project_config.yaml.template config/

# Copy documentation
cp ../docs/export_guide.md .
cp ../docs/quick_start_export.md .

echo "✅ Export complete!"
echo "📦 Package location: $(pwd)"
```

---

## 📊 Export Readiness Summary

| Component | Readiness | Action Needed |
|-----------|-----------|---------------|
| `AgentQMS/agent_tools/` | 95% | ✅ Path verification only |
| `agent/` | 90% | ✅ Config template created |
| `docs/ai_handbook/` | 60% | ⚠️ Create templates for 4 files |
| **Overall** | **80%** | ⚠️ Template creation needed |

---

## 🎯 Next Steps

1. ✅ **DONE**: Created adaptation script
2. ✅ **DONE**: Created config template
3. ✅ **DONE**: Created export documentation
4. ⚠️ **TODO**: Create templates for project-specific handbook sections
5. ⚠️ **TODO**: Test export in a new project
6. ⚠️ **TODO**: Package for distribution

---

**Last Updated**: 2025-11-01
**Version**: 1.0
