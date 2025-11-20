# Artifact Management Protocol

**Document ID**: `PROTO-GOV-001`
**Status**: ACTIVE
**Last Updated**: 2025-11-20
**Type**: Governance Protocol

---

## 🎯 Purpose

This protocol describes **when** and **why** to create artifacts, and **how** to use the framework tools to manage them. The framework tools handle all naming conventions, validation, and structure automatically.

---

## 🛠️ Framework Tool

**Use the framework artifact workflow tool**:
```bash
python -m AgentQMS.agent_tools.core.artifact_workflow create --type <type> --name <name> --title "<title>"
```

The framework tool automatically:
- ✅ Applies correct naming conventions (`YYYY-MM-DD_[CATEGORY]_[NAME].md`)
- ✅ Places artifacts in correct directories
- ✅ Validates structure and required fields
- ✅ Updates indexes
- ✅ Checks compliance

**See tool help for details**:
```bash
python -m AgentQMS.agent_tools.core.artifact_workflow --help
python -m AgentQMS.agent_tools.core.artifact_workflow create --help
```

---

## 📋 When to Create Artifacts

### **Artifact Types**

1. **Implementation Plans** - Major feature development or refactoring work
2. **Assessments** - System audits, gap analyses, evaluations
3. **Design Documents** - Architecture decisions, system designs
4. **Bug Reports** - Issue documentation and resolution tracking
5. **Research** - Investigation findings, technical research
6. **Templates** - Reusable templates for artifacts

### **Guidelines**

- ✅ **Create artifacts** for significant work (multi-session, multi-file, multi-phase)
- ✅ **Create artifacts** for documentation that needs traceability
- ✅ **Create artifacts** for design decisions that impact architecture
- ❌ **Don't create artifacts** for trivial changes or one-off fixes
- ❌ **Don't create artifacts** in project root - use framework tool

---

## 🔄 Workflow

### **Step 1: Create Artifact**

Use the framework tool:
```bash
python -m AgentQMS.agent_tools.core.artifact_workflow create \
  --type implementation_plan \
  --name "feature-name" \
  --title "Feature Name Implementation Plan"
```

The tool will:
- Create the artifact in the correct directory
- Apply proper naming conventions
- Populate with template content
- Validate structure

### **Step 2: Validate Artifact**

```bash
# Validate a specific artifact
python -m AgentQMS.agent_tools.core.artifact_workflow validate --file path/to/artifact.md

# Validate all artifacts
python -m AgentQMS.agent_tools.core.artifact_workflow validate --all
```

### **Step 3: Update Indexes**

After creating or modifying artifacts:
```bash
python -m AgentQMS.agent_tools.core.artifact_workflow update-indexes
```

### **Step 4: Check Compliance**

Regular compliance checking:
```bash
python -m AgentQMS.agent_tools.core.artifact_workflow check-compliance
```

---

## 📁 Directory Structure

The framework automatically organizes artifacts in `docs/artifacts/`:

```
docs/artifacts/
├── implementation_plans/    # Implementation plans and blueprints
├── assessments/             # Audits, gap analyses, evaluations
├── design_documents/        # Architecture and design decisions
├── bug_reports/            # Bug documentation
├── research/               # Technical research
└── templates/              # Reusable templates
```

**The framework tool handles directory placement automatically** - you don't need to know the structure.

---

## ✅ Compliance

The framework enforces compliance automatically through validation:

- ✅ **Naming conventions** - Validated by `validate_artifacts.py`
- ✅ **Directory structure** - Enforced by artifact workflow
- ✅ **Required fields** - Validated against templates
- ✅ **Frontmatter format** - Validated by framework
- ✅ **Boundary compliance** - Artifacts must be in `docs/artifacts/`

**Check compliance**:
```bash
python -m AgentQMS.agent_tools.compliance.validate_artifacts --all
```

---

## 🎓 Best Practices

1. **Always use the framework tool** - Don't create artifacts manually
2. **Validate before committing** - Run validation checks
3. **Update indexes regularly** - Keep indexes current
4. **Reference source documents** - Include attribution in artifacts
5. **Cross-reference related artifacts** - Link to related work

---

## 🔗 Related

- **Framework Tool**: `AgentQMS/agent_tools/core/artifact_workflow.py`
- **Validation Tool**: `AgentQMS/agent_tools/compliance/validate_artifacts.py`
- **Templates**: `AgentQMS/agent_tools/core/artifact_templates.py`
- **Implementation Plan Protocol**: [02_implementation_plan_protocol.md](02_implementation_plan_protocol.md)
- **Blueprint Protocol**: [03_blueprint_protocol_template.md](03_blueprint_protocol_template.md)

---

## ❓ Troubleshooting

**Q: What if I need a custom artifact type?**
- Check available types: `python -m AgentQMS.agent_tools.core.artifact_workflow create --help`
- Framework templates are extensible - see `artifact_templates.py`

**Q: How do I update an existing artifact?**
- Edit the artifact file directly
- Run validation: `python -m AgentQMS.agent_tools.core.artifact_workflow validate --file path/to/artifact.md`
- Update indexes if structure changed

**Q: Validation failed - what do I do?**
- Check error messages from validation tool
- Framework validation will point to specific issues
- Fix issues and re-validate

---

*This protocol focuses on **workflow** and **tool usage**. For detailed naming conventions and structure rules, see the framework validation tool - it's the source of truth.*
