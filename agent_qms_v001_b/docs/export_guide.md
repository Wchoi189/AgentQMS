---
title: "AI Handbook & Agent Tools Export Guide"
date: "2025-11-01"
status: "active"
version: "1.0"
category: "user_guide"
tags: ["export", "framework", "ai_agent", "documentation"]
---

# AI Handbook & Agent Tools Export Guide

**Version**: 1.0
**Date**: 2025-11-01
**Purpose**: Complete guide for exporting and reusing `docs/ai_handbook/`, `agent/`, and `scripts/agent_tools/` in other projects

---

## Table of Contents

1. [Overview](#overview)
2. [What to Export](#what-to-export)
3. [Project-Specific Content Identification](#project-specific-content-identification)
4. [Abstraction Strategy](#abstraction-strategy)
5. [Export Checklist](#export-checklist)
6. [Adaptation Guide for New Projects](#adaptation-guide-for-new-projects)
7. [Useful Resources](#useful-resources)

---

## Overview

This guide enables you to export and reuse the AI agent framework components:

1. **`docs/ai_handbook/`** - AI agent documentation and protocols
2. **`docs/ai_agent/`** - AI agent domain documentation (system.md, tracking, automation, etc.)
3. **`agent/`** - Agent-only interface layer (Makefile, wrappers, config)
4. **`scripts/agent_tools/`** - Implementation layer (Python automation scripts)
5. **Templates** - Artifact and blueprint templates

### Why Export?

- **Reusable AI Agent Framework**: Standardized workflows and tools for AI-assisted development
- **Documentation System**: Structured protocols and guidelines
- **Automation Tools**: Artifact creation, validation, compliance checking
- **Best Practices**: Established patterns for AI agent collaboration

### Automated Export Utility ✅

**NEW**: An automated export utility is now available! Use the export tool to create project-agnostic packages:

```bash
# From agent/ directory (recommended)
cd agent/
make export OUTPUT=../export_package/

# Or directly with Python
python scripts/agent_tools/utilities/export_framework.py --output export_package/
```

**Features**:
- ✅ Automated copying of all framework components
- ✅ Excludes Streamlit UI dashboard features
- ✅ Excludes project-specific content (data, outputs, logs, configs)
- ✅ Includes all new agent tools and documentation
- ✅ Export validation
- ✅ Dry-run mode for testing

**See [Automated Export](#automated-export) section below for details.**

### What Makes It Project-Agnostic?

Most of the code is already generic! The automated export utility handles:
- Removing project-specific references from documentation
- Excluding project-specific files and directories
- Creating configuration templates
- Providing adaptation instructions

---

## What to Export

### ✅ **Fully Exportable (Minimal Changes)**

#### `scripts/agent_tools/` - 95% Ready
```
scripts/agent_tools/
├── core/                    # ✅ Generic - artifact creation, discovery
├── compliance/              # ✅ Generic - validation, monitoring
├── documentation/           # ✅ Generic - index generation, link validation
├── utilities/               # ✅ Generic - context tools, feedback
└── maintenance/             # ✅ Generic - one-time fixes
```

**Why**: Python scripts are mostly generic. Only paths might need adjustment.

#### `agent/` - 90% Ready
```
agent/
├── Makefile                 # ✅ Generic - command wrappers
├── config/                  # ⚠️ Needs template - paths are project-specific
│   ├── agent_config.yaml    # ✅ Generic structure
│   └── tool_mappings.json   # ⚠️ Paths need abstraction
├── tools/                   # ✅ Generic - thin wrappers
└── workflows/               # ✅ Generic - shell scripts
```

**Why**: Wrapper layer is generic, but config files reference project paths.

### ⚠️ **Needs Abstraction (Project-Specific Content)**

#### `docs/ai_handbook/` - 60% Ready

**Project-Specific Sections**:
- `01_onboarding/01_project_overview.md` - Entire file is project-specific
- `01_onboarding/03_data_overview.md` - Project-specific data structure
- `index.md` - Contains project name, purpose, structure
- `03_references/development/ai_agent_context.md` - Project-specific import patterns
- Various protocol files referencing specific project files

**Generic Sections** (Keep as-is):
- `02_protocols/governance/01_artifact_management_protocol.md` - Generic artifact management
- `02_protocols/development/01_coding_standards_v2.md` - Generic coding standards
- `02_protocols/development/22_proactive_modularity_protocol.md` - Generic modularity
- Most protocol templates

---

## Project-Specific Content Identification

### 🔍 **Search Patterns to Find Project-Specific Content**

Use these patterns to identify what needs abstraction:

```bash
# Project name references
grep -ri "upstage\|prompt.*hack\|korean.*grammar" docs/ai_handbook/

# Specific file references
grep -ri "prompts\.py\|grammar_correction\|streamlit_app\|evaluate\.py" docs/ai_handbook/

# Project structure references
grep -ri "upstage-prompt\|project.*structure" docs/ai_handbook/

# Specific API/service references
grep -ri "Solar Pro\|solar.*pro" docs/ai_handbook/
```

### 📋 **Known Project-Specific References**

#### In `docs/ai_handbook/index.md`:
- Line 2: Project name "Korean Grammar Correction Project"
- Line 5: Project purpose description
- Lines 11-17: Project-specific components
- Lines 45-60: Project structure diagram
- Lines 116-128: Project-specific file references

#### In `docs/ai_handbook/01_onboarding/01_project_overview.md`:
- Entire file is project-specific
- Technology stack references specific APIs
- Project structure is project-specific

#### In `docs/ai_handbook/03_references/development/ai_agent_context.md`:
- Lines 12-26: Project-specific architecture
- Lines 28-42: Project-specific import patterns
- Lines 44-56: Project-specific debugging methods

#### In Configuration Files:
- `agent/config/tool_mappings.json`: Path references (`../scripts/agent_tools/`)
- `agent/config/agent_config.yaml`: Generic but may have project-specific settings

---

## Abstraction Strategy

### 🎯 **Three-Level Abstraction Approach**

#### **Level 1: Variable Substitution**
Replace hardcoded values with placeholders:
- Project name → `{{PROJECT_NAME}}`
- Project purpose → `{{PROJECT_PURPOSE}}`
- Specific files → `{{PROJECT_ROOT}}/path/to/file`

#### **Level 2: Template Files**
Create template versions that can be filled in:
- `docs/ai_handbook/index.md.template`
- `docs/ai_handbook/01_onboarding/01_project_overview.md.template`

#### **Level 3: Configuration-Driven**
Move project-specific content to config files:
- `docs/ai_handbook/config/project_config.yaml`
- Read config and generate project-specific docs

### 📝 **Abstraction Examples**

#### Before (Project-Specific):
```markdown
# AI Agent Handbook: Korean Grammar Correction Project

**Project**: Korean Grammar Error Correction using Prompt Engineering

This project focuses on developing optimal prompts for Korean grammar correction using the Solar Pro API.

## Project Structure
```
upstage-prompt-a-thon-project/
├── prompts.py
├── grammar_correction_utils.py
```
```

#### After (Project-Agnostic):
```markdown
# AI Agent Handbook: {{PROJECT_NAME}}

**Project**: {{PROJECT_PURPOSE}}

{{PROJECT_DESCRIPTION}}

## Project Structure
```
{{PROJECT_ROOT}}/
{{PROJECT_STRUCTURE}}
```
```

Or use configuration:

```yaml
# docs/ai_handbook/config/project_config.yaml
project:
  name: "{{PROJECT_NAME}}"
  purpose: "{{PROJECT_PURPOSE}}"
  description: "{{PROJECT_DESCRIPTION}}"
  structure:
    root: "{{PROJECT_ROOT}}"
    key_files:
      - prompts.py
      - grammar_correction_utils.py
```

---

## Automated Export

### 🚀 **Quick Export**

The automated export utility makes exporting the framework simple:

```bash
# From agent/ directory (recommended)
cd agent/
make export OUTPUT=../export_package/

# Or directly with Python
python scripts/agent_tools/utilities/export_framework.py --output export_package/
```

### 📋 **Export Commands**

#### Using Makefile (Recommended)

```bash
# Export framework
make export OUTPUT=../export_package/

# Dry run (see what would be exported)
make export-dry-run OUTPUT=../export_package/

# Export with validation
make export-validate OUTPUT=../export_package/
```

#### Using Python Directly

```bash
# Export framework
python scripts/agent_tools/utilities/export_framework.py --output export_package/

# Dry run (see what would be exported)
python scripts/agent_tools/utilities/export_framework.py --output export_package/ --dry-run

# Export with validation
python scripts/agent_tools/utilities/export_framework.py --output export_package/ --validate
```

### 📦 **What Gets Exported**

The export utility automatically includes:

✅ **Agent Tools** (`agent_tools/`):
- All core tools (artifact_workflow, discover, templates)
- All compliance tools (validation, monitoring, alerts)
- All documentation tools (index generation, link validation)
- All utilities (context, feedback, tracking)
- All maintenance scripts

✅ **Agent Interface** (`agent/`):
- Makefile and configuration
- Tool wrappers and workflows
- Blueprint templates

✅ **AI Handbook** (`ai_handbook/`):
- All protocols and guidelines
- Onboarding documentation
- Reference materials
- Templates

✅ **AI Agent Documentation** (`ai_agent/`):
- System documentation (system.md)
- Tracking domain documentation
- Automation domain documentation
- Coding protocols

✅ **Templates**:
- Artifact templates
- Blueprint templates
- Handbook templates

✅ **Adaptation Tools**:
- `scripts/adapt_project.py` - Project adaptation script
- Export documentation

### 🚫 **What Gets Excluded**

The export utility automatically excludes:

❌ **Streamlit UI Dashboard Features**:
- `compliance_dashboard.py` - Streamlit UI dashboard
- `validate_coordinate_consistency.py` - Streamlit UI validation

❌ **Project-Specific Content**:
- Data directories (`data/`, `outputs/`, `logs/`, `results/`)
- Project-specific configuration files
- Development artifacts (caches, build files)
- Node modules and dependencies

### ✅ **Export Validation**

The export utility includes validation to ensure completeness:

```bash
# Export with validation
make export-validate OUTPUT=../export_package/
```

Validation checks:
- ✅ All required directories are present
- ✅ All required files are present
- ✅ Excluded files are not present
- ✅ Export structure is correct

### 📊 **Export Summary**

After export, you'll see a summary:

```
📊 Export Summary
============================================================
   Files copied: 163
   Files excluded: 14
   Directories created: 25
```

### 📝 **Export Package Structure**

The exported package has this structure:

```
export_package/
├── README.md                    # Export package README
├── agent_tools/                  # Implementation layer
│   ├── core/
│   ├── compliance/
│   ├── documentation/
│   ├── utilities/
│   └── maintenance/
├── agent/                        # Interface layer
│   ├── Makefile
│   ├── config/
│   └── tools/
├── ai_handbook/                  # AI handbook
│   ├── 01_onboarding/
│   ├── 02_protocols/
│   ├── 03_references/
│   └── templates/
├── ai_agent/                     # AI agent documentation
│   ├── system.md
│   ├── tracking/
│   └── automation/
├── scripts/                      # Adaptation scripts
│   └── adapt_project.py
└── docs/                         # Export documentation
    ├── export_guide.md
    ├── quick_start_export.md
    └── resources.md
```

---

## Export Checklist

### Phase 1: Automated Export (Recommended) ✅

- [ ] **Run Automated Export**
  ```bash
  cd agent/
  make export OUTPUT=../export_package/
  ```

- [ ] **Validate Export**
  ```bash
  make export-validate OUTPUT=../export_package/
  ```

- [ ] **Review Export Summary**
  - Check files copied count
  - Verify excluded files are correct
  - Review any warnings

### Phase 2: Manual Export (Alternative)

If you need manual control:

- [ ] **Backup Current Project**
  ```bash
  cp -r docs/ai_handbook/ docs/ai_handbook.backup/
  cp -r agent/ agent.backup/
  cp -r scripts/agent_tools/ scripts/agent_tools.backup/
  ```

- [ ] **Identify Project-Specific Content**
  ```bash
  # Run search patterns
  grep -ri "PROJECT_SPECIFIC_TERM" docs/ai_handbook/ agent/ scripts/agent_tools/
  ```

- [ ] **Document Dependencies**
  - Python version requirements
  - Required packages (check `requirements.txt` or `pyproject.toml`)
  - File structure assumptions

### Phase 3: Create Template Versions (Manual Only)

- [ ] **Create Template Directory**
  ```bash
  mkdir -p export_templates/ai_handbook
  mkdir -p export_templates/agent
  mkdir -p export_templates/agent_tools
  ```

- [ ] **Create Project Config Template**
  ```yaml
  # export_templates/project_config.yaml.template
  project:
    name: "Your Project Name"
    purpose: "Brief project purpose"
    description: "Detailed project description"
    structure:
      root: "project-root-directory"
      docs_path: "docs"
      artifacts_path: "docs/artifacts"
      scripts_path: "scripts"
  ```

- [ ] **Create Abstraction Script**
  - Python script to replace placeholders
  - Copy templates to new project
  - Fill in project-specific values

### Phase 3: Abstract Documentation

- [ ] **Update `docs/ai_handbook/index.md`**
  - Replace project name with `{{PROJECT_NAME}}`
  - Replace project structure with template
  - Remove project-specific file references

- [ ] **Create Template for `01_project_overview.md`**
  - Template structure with placeholders
  - Example content as comments

- [ ] **Abstract `03_references/development/ai_agent_context.md`**
  - Remove project-specific import patterns
  - Keep generic debugging guidance
  - Add template for project-specific patterns

- [ ] **Review All Protocol Files**
  - Mark generic vs. project-specific sections
  - Create template versions where needed

### Phase 4: Abstract Configuration

- [ ] **Update `agent/config/tool_mappings.json`**
  - Use relative paths (already done)
  - Document path assumptions

- [ ] **Create `agent/config/project_config.yaml.template`**
  - Project-specific settings
  - Path configurations

- [ ] **Review `agent/Makefile`**
  - Verify paths are relative
  - Document any assumptions

### Phase 5: Test Export

- [ ] **Create Test Project**
  ```bash
  mkdir test_export_project
  # Copy exported templates
  # Run adaptation script
  # Verify functionality
  ```

- [ ] **Verify Tools Work**
  ```bash
  cd test_export_project/agent/
  make discover
  make create-plan NAME=test TITLE="Test Plan"
  ```

- [ ] **Verify Documentation**
  - Check all links work
  - Verify placeholders are filled
  - Ensure no broken references

### Phase 6: Package Export

- [ ] **Create Export Package**
  ```bash
  mkdir ai_agent_framework_export
  # Copy abstracted versions
  # Include adaptation scripts
  # Include README
  ```

- [ ] **Create README for Export**
  - Installation instructions
  - Adaptation guide
  - Quick start

- [ ] **Create Adaptation Script**
  - Interactive setup
  - Config file generation
  - Template filling

---

## Adaptation Guide for New Projects

### 🚀 **Quick Start (5 Steps)**

#### Step 1: Copy Framework
```bash
# Copy three directories
cp -r docs/ai_handbook/ new_project/docs/
cp -r agent/ new_project/
cp -r scripts/agent_tools/ new_project/scripts/
```

#### Step 2: Create Project Configuration
```bash
cd new_project/
# Create project config file
cat > docs/ai_handbook/config/project_config.yaml << EOF
project:
  name: "My New Project"
  purpose: "Brief purpose description"
  description: "Detailed project description"
  structure:
    root: "."
    docs_path: "docs"
    artifacts_path: "docs/artifacts"
    scripts_path: "scripts"
EOF
```

#### Step 3: Run Adaptation Script
```bash
# If you created an adaptation script
python scripts/agent_tools/utilities/adapt_project.py \
  --config docs/ai_handbook/config/project_config.yaml \
  --project-root .
```

#### Step 4: Update Project-Specific Files
Manually update:
- `docs/ai_handbook/index.md` - Project name and structure
- `docs/ai_handbook/01_onboarding/01_project_overview.md` - Project overview
- `docs/ai_handbook/03_references/development/ai_agent_context.md` - Project-specific patterns

#### Step 5: Verify Installation
```bash
cd agent/
make discover
make status
make create-plan NAME=test TITLE="Test Plan"
```

### 📝 **Manual Adaptation Checklist**

If automated script isn't available:

- [ ] **Update Project Name**
  - Search/replace: `docs/ai_handbook/index.md`
  - Search/replace: All references in handbook

- [ ] **Update Project Structure**
  - Modify structure diagrams
  - Update file references
  - Adjust paths in examples

- [ ] **Create Project Overview**
  - Copy template from `01_project_overview.md.template`
  - Fill in project-specific details
  - Update technology stack

- [ ] **Update Agent Context**
  - Document project-specific import patterns
  - Update debugging methods
  - Add project-specific guidelines

- [ ] **Verify Paths**
  - Check `agent/config/tool_mappings.json`
  - Verify `agent/Makefile` paths
  - Test all tool commands

- [ ] **Update Examples**
  - Replace example file names
  - Update example commands
  - Fix example paths

---

## Useful Resources

### 📚 **Files to Reference**

#### Core Documentation
- `docs/ai_agent/system.md` - Single source of truth for agents
- `docs/ai_handbook/index.md` - Handbook index
- `docs/ai_handbook/02_protocols/governance/01_artifact_management_protocol.md` - Artifact system

#### Tool Documentation
- `scripts/agent_tools/README.md` - Tool implementation guide
- `scripts/agent_tools/core/discover.py` - Tool discovery script
- `scripts/agent_tools/core/artifact_workflow.py` - Artifact creation tool

#### Configuration
- `agent/config/agent_config.yaml` - Agent configuration template
- `agent/config/tool_mappings.json` - Tool path mappings
- `agent/Makefile` - Command interface

#### Templates
- `scripts/agent_tools/core/artifact_templates.py` - Artifact templates (generic)
- `docs/ai_handbook/templates/` - Documentation templates

### 🔧 **Utility Scripts**

#### Discovery Tools
```bash
# List all available tools
python scripts/agent_tools/core/discover.py

# Check system status
cd agent/ && make status
```

#### Validation Tools
```bash
# Validate all artifacts
python scripts/agent_tools/compliance/validate_artifacts.py --all

# Check compliance
python scripts/agent_tools/compliance/monitor_artifacts.py --check
```

#### Documentation Tools
```bash
# Generate documentation index
python scripts/agent_tools/documentation/auto_generate_index.py --validate

# Validate links
python scripts/agent_tools/documentation/validate_links.py
```

### 📋 **What's Already Generic**

✅ **Fully Generic (No Changes Needed)**:
- `scripts/agent_tools/core/artifact_templates.py` - Pure templates
- `scripts/agent_tools/compliance/` - Generic validation
- `scripts/agent_tools/documentation/` - Generic doc tools
- `scripts/agent_tools/utilities/` - Generic utilities
- Most protocol files in `docs/ai_handbook/02_protocols/`

⚠️ **Mostly Generic (Minor Path Updates)**:
- `agent/Makefile` - Uses relative paths
- `agent/config/agent_config.yaml` - Mostly generic
- `agent/tools/` - Thin wrappers, generic

❌ **Needs Abstraction**:
- `docs/ai_handbook/index.md` - Project name/structure
- `docs/ai_handbook/01_onboarding/01_project_overview.md` - Entire file
- `docs/ai_handbook/01_onboarding/03_data_overview.md` - Project-specific
- `docs/ai_handbook/03_references/development/ai_agent_context.md` - Project-specific patterns

---

## Creating the Export Package

### 📦 **Package Structure**

```
ai_agent_framework/
├── README.md                    # Export package README
├── INSTALLATION.md              # Installation guide
├── ADAPTATION.md                # Adaptation instructions
├── LICENSE                      # License file
│
├── ai_handbook/                 # Abstracted handbook
│   ├── templates/               # Template files
│   ├── config/                  # Configuration templates
│   └── [rest of handbook]
│
├── agent/                       # Agent interface layer
│   ├── config/                  # Configuration templates
│   └── [rest of agent directory]
│
├── agent_tools/                 # Implementation layer
│   └── [all Python scripts]
│
└── scripts/                     # Adaptation scripts
    ├── adapt_project.py         # Main adaptation script
    ├── extract_project_config.py # Extract config from project
    └── validate_export.py       # Validate export completeness
```

### 🛠️ **Adaptation Script Template**

```python
#!/usr/bin/env python3
"""
Project Adaptation Script
Automates the process of adapting the AI agent framework to a new project.
"""

import yaml
import re
from pathlib import Path
from typing import Dict

def load_project_config(config_path: Path) -> Dict:
    """Load project configuration."""
    with open(config_path) as f:
        return yaml.safe_load(f)

def replace_placeholders(content: str, config: Dict) -> str:
    """Replace placeholders in content with config values."""
    replacements = {
        '{{PROJECT_NAME}}': config['project']['name'],
        '{{PROJECT_PURPOSE}}': config['project']['purpose'],
        '{{PROJECT_DESCRIPTION}}': config['project']['description'],
        '{{PROJECT_ROOT}}': config['project']['structure']['root'],
    }

    for placeholder, value in replacements.items():
        content = content.replace(placeholder, value)

    return content

def adapt_file(file_path: Path, config: Dict) -> None:
    """Adapt a single file by replacing placeholders."""
    content = file_path.read_text()
    adapted = replace_placeholders(content, config)
    file_path.write_text(adapted)

def adapt_project(project_root: Path, config_path: Path) -> None:
    """Main adaptation function."""
    config = load_project_config(config_path)

    # List of files to adapt
    files_to_adapt = [
        project_root / 'docs' / 'ai_handbook' / 'index.md',
        project_root / 'docs' / 'ai_handbook' / '01_onboarding' / '01_project_overview.md',
        # Add more files as needed
    ]

    for file_path in files_to_adapt:
        if file_path.exists():
            adapt_file(file_path, config)
            print(f"✅ Adapted: {file_path}")
        else:
            print(f"⚠️  Not found: {file_path}")

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', required=True, help='Path to project config')
    parser.add_argument('--project-root', default='.', help='Project root directory')
    args = parser.parse_args()

    adapt_project(Path(args.project_root), Path(args.config))
```

---

## Summary

### ✅ **Export Readiness**

| Component | Readiness | Changes Needed |
|-----------|-----------|----------------|
| `scripts/agent_tools/` | 95% | Minimal path checks |
| `agent/` | 90% | Config template creation |
| `docs/ai_handbook/` | 60% | Abstract project-specific content |

### 🎯 **Quick Wins**

1. **Export `scripts/agent_tools/`** - Already mostly generic
2. **Export `agent/`** - Only needs config template
3. **Create templates** - For project-specific handbook sections
4. **Write adaptation script** - Automate the process

### 📝 **Next Steps**

1. Run through the export checklist
2. Create template versions of project-specific files
3. Test export in a new project
4. Document any edge cases
5. Package for distribution

---

**Last Updated**: 2025-11-01
**Version**: 1.0
**Maintainer**: AI Agent Framework Team
