# AI Agent Handbook: Korean Grammar Correction Project

**Version**: 2.3 (2025-11-01)
**Status**: ACTIVE - Single source of truth for AI agents
**Project**: Korean Grammar Error Correction using Prompt Engineering

---

## Project Overview

This project focuses on developing optimal prompts for Korean grammar correction using the Solar Pro API. The goal is to create a system that takes sentences with grammar errors as input and outputs grammatically correct sentences through prompt engineering, without model tuning.

### Key Components
- **Grammar Correction Engine**: Core prompt engineering system
- **Streamlit Application**: Interactive web interface for testing and analysis
- **Data Processing Pipeline**: Training and test data management
- **Evaluation Framework**: Performance measurement and comparison

---

## Quick Navigation

### 🚀 **For New AI Agents**
1. **Start Here**: [Project Overview](01_onboarding/01_project_overview.md)
2. **Setup**: [Environment Setup](01_onboarding/02_environment_setup.md)
3. **Data**: [Data Overview](01_onboarding/03_data_overview.md)

### 🛠️ **For Development Tasks**
1. **Standards**: [Coding Standards V2](02_protocols/development/01_coding_standards_v2.md)
2. **Modularity**: [Proactive Modularity Protocol](02_protocols/development/22_proactive_modularity_protocol.md)
3. **Import Handling**: [Import Handling Protocol](02_protocols/development/23_import_handling_protocol.md)
4. **Streamlit Debugging**: [Streamlit Debugging Protocol](02_protocols/development/24_streamlit_debugging_protocol.md)
5. **Code Generation**: [Code Generation Quality Protocol](02_protocols/development/code_generation_quality_protocol.md)
6. **Context Templates**: [Context Templates](02_protocols/development/context-templates.md)

### 🤖 **For Agent-Only Operations**
1. **System Rules**: [AI Agent System – Single Source of Truth](04_agent_system/system.md)
2. **Automation Overview**: [Automation Tooling](04_agent_system/automation/tooling_overview.md)
3. **Tracking CLI**: [Tracking CLI Reference](04_agent_system/tracking/cli_reference.md)
4. **Tool Catalog**: [Automation Tool Catalog](04_agent_system/automation/tool_catalog.md)

### 📋 **For Project Management**
1. **Artifacts**: [Artifact Management Protocol](02_protocols/governance/01_artifact_management_protocol.md)
2. **Implementation Plans**: [Implementation Plan Protocol](02_protocols/governance/02_implementation_plan_protocol.md)
3. **Blueprint Template**: [Blueprint Protocol Template](02_protocols/governance/03_blueprint_protocol_template.md)
4. **Bug Fixes**: [Bug Fix Protocol](02_protocols/governance/04_bug_fix_protocol.md)
5. **Current Implementation**: [Streamlit App Plan](../../artifacts/implementation_plans/2025-01-27_IMPLEMENTATION_PLAN_STREAMLIT_APP_V1.md)

---

## Project Structure

```
upstage-prompt-a-thon-project/
├── docs/
│   ├── ai_handbook/                   # This handbook
│   ├── artifacts/                     # All AI-generated artifacts
│   └── [other documentation]
├── data/                              # Training and test data
├── prompts.py                         # Core prompt templates
├── grammar_correction_utils.py        # Utility functions
├── evaluate.py                        # Evaluation scripts
├── PLAN_1_IMPLEMENTATION.md          # Implementation strategy
├── PLAN_2_STREAMLIT_APP.md           # Streamlit app design
└── [other project files]
```

---

## Key Documents

### **Implementation Plans**
- [Streamlit App Strategic Plan](../../artifacts/implementation_plans/2025-01-27_IMPLEMENTATION_PLAN_STREAMLIT_APP_V1.md)
- [Original Implementation Plan](../../planning/PLAN_1_IMPLEMENTATION.md)

### **Design Documents**
- [Streamlit App Design](../../planning/PLAN_2_STREAMLIT_APP.md)
- [Project Architecture](03_references/architecture/01_project_architecture.md)

### **Reference Documentation**
- [AI Agent Context](03_references/development/ai_agent_context.md)
- [Import Handling Reference](03_references/development/import_handling_reference.md)
- [Loader Path Resolution](03_references/development/loader_path_resolution.md) - Environment variables for loader registry path resolution
- [Schema Configuration Fix](03_references/development/schema_configuration_fix.md)
- [Modularity Quick Reference](03_references/development/modularity_quick_reference.md)
- [Utility Functions](03_references/development/utility_functions.md)
- [Elasticsearch Integration Guide](../../artifacts/research/2025-11-01_elasticsearch_integration_guide.md)

### **Protocols**
- [Artifact Management Protocol](02_protocols/governance/01_artifact_management_protocol.md)
- [Implementation Plan Protocol](02_protocols/governance/02_implementation_plan_protocol.md)
- [Blueprint Protocol Template](02_protocols/governance/03_blueprint_protocol_template.md)
- [Bug Fix Protocol](02_protocols/governance/04_bug_fix_protocol.md)
- [Coding Standards](02_protocols/development/01_coding_standards.md)
- [Import Handling Protocol](02_protocols/development/23_import_handling_protocol.md)
- [Streamlit Debugging Protocol](02_protocols/development/24_streamlit_debugging_protocol.md)

---

## AI Agent Guidelines

### **Before Making Changes**
1. **Read this handbook** - Understand project structure and goals
2. **Check existing artifacts** - Avoid duplicating work
3. **Follow protocols** - Use established procedures
4. **Update documentation** - Keep everything current

### **File Creation Rules**
- **Never create files in project root** - Use appropriate directories
- **Follow artifact management protocol** - Use timestamped names
- **Reference source documents** - Always attribute sources
- **Update indexes** - Keep navigation current

### **Quality Standards**
- **Consistent formatting** - Follow established patterns
- **Clear documentation** - Explain decisions and approaches
- **Proper references** - Link to related documents
- **Regular updates** - Keep information current

---

## Common Tasks

### **Adding New Prompts**
1. Review [prompts.py](../../prompts.py) for existing patterns
2. Follow [coding standards](02_protocols/development/01_coding_standards.md)
3. Test with [evaluation framework](../../evaluate.py)
4. Document in [data overview](01_onboarding/03_data_overview.md)

### **Developing Streamlit Features**
1. Follow [Streamlit development protocol](02_protocols/development/03_streamlit_development.md)
2. Reference [app design document](../../planning/PLAN_2_STREAMLIT_APP.md)
3. Use [implementation plan](../../artifacts/implementation_plans/2025-01-27_IMPLEMENTATION_PLAN_STREAMLIT_APP_V1.md)
4. Test thoroughly before deployment

### **Creating Documentation**
1. Use [artifact management protocol](02_protocols/governance/01_artifact_management_protocol.md)
2. Follow [templates](02_protocols/templates/) for consistency
3. Update relevant indexes
4. Cross-reference related documents

### **Creating Implementation Plans**
1. **Use Blueprint Template**: [Blueprint Protocol Template](02_protocols/governance/03_blueprint_protocol_template.md)
2. **Follow Plan Protocol**: [Implementation Plan Protocol](02_protocols/governance/02_implementation_plan_protocol.md)
3. **Include Progress Tracker**: Status, current step, completed tasks, next task
4. **Add Autonomous Agent Prompt**: Chief of Staff prompt at the top
5. **Reference Source Documents**: Always attribute original requirements
6. **Ask for Confirmation**: If blueprint format might not be appropriate

---

## Getting Help

### **Documentation Issues**
- Check [artifact management protocol](02_protocols/governance/01_artifact_management_protocol.md)
- Review [templates](02_protocols/templates/) for examples
- Consult [project architecture](03_references/architecture/01_project_architecture.md)

### **Technical Issues**
- Review [coding standards](02_protocols/development/01_coding_standards.md)
- Check [data overview](01_onboarding/03_data_overview.md)
- Consult existing code examples

### **Project Questions**
- Read [project overview](01_onboarding/01_project_overview.md)
- Review [implementation plans](../../artifacts/implementation_plans/)
- Check [design documents](../../PLAN_2_STREAMLIT_APP.md)

---

## Archive

Previous versions of this handbook are preserved in [ARCHIVE/](ARCHIVE/) for reference. The current version (2.0) is aligned with the actual project structure and artifact management system.

---

*This handbook is the single source of truth for AI agents working on the Korean Grammar Correction project. Keep it updated and follow its guidance for consistent, high-quality work.*
