# Implementation Plan Protocol

**Document ID**: `PROTO-GOV-002`
**Status**: ACTIVE
**Last Updated**: 2025-11-20
**Type**: Governance Protocol

---

## 🎯 Purpose

This protocol describes **when** and **how** to create implementation plans using the framework tools. The framework provides templates that automatically include required structure.

---

## 🛠️ Framework Tool

**Use the framework artifact workflow tool**:
```bash
python -m AgentQMS.agent_tools.core.artifact_workflow create \
  --type implementation_plan \
  --name "feature-name" \
  --title "Feature Name Implementation Plan"
```

The framework template automatically includes:
- ✅ Progress tracker structure
- ✅ Blueprint protocol format
- ✅ Required frontmatter
- ✅ Standard sections
- ✅ Compliance validation

**See tool help**:
```bash
python -m AgentQMS.agent_tools.core.artifact_workflow create --help
```

---

## 📋 When to Create Implementation Plans

### **Create Implementation Plans For:**

- ✅ Major feature development (multi-phase, multi-session)
- ✅ Significant refactoring work
- ✅ Architecture changes
- ✅ Multi-file, multi-component changes
- ✅ Work requiring systematic execution

### **Don't Create Implementation Plans For:**

- ❌ Simple bug fixes
- ❌ Single-file changes
- ❌ Trivial modifications
- ❌ One-off scripts

---

## 🔄 Workflow

### **Step 1: Create Plan**

```bash
python -m AgentQMS.agent_tools.core.artifact_workflow create \
  --type implementation_plan \
  --name "my-feature" \
  --title "My Feature Implementation"
```

The framework creates the plan with:
- Correct naming convention
- Proper directory placement
- Template structure
- Required fields pre-filled

### **Step 2: Customize Plan**

Edit the generated plan to add:
- **Progress Tracker**: Current status, current step, last completed, next task
- **Agent Prompt** (if using autonomous execution): Chief of Staff role definition
- **Phases and Tasks**: Break down work into manageable phases
- **Success Criteria**: How to know work is complete
- **Source Attribution**: Reference original requirements/documents

### **Step 3: Validate Plan**

```bash
python -m AgentQMS.agent_tools.core.artifact_workflow validate \
  --file docs/artifacts/implementation_plans/YYYY-MM-DD_IMPLEMENTATION_PLAN_my-feature.md
```

### **Step 4: Update Progress**

As work progresses:
- Update progress tracker (status, current step, last completed, next task)
- Mark completed tasks
- Update phases
- Document decisions and changes

---

## 📝 Plan Structure

The framework template provides the structure. Key elements:

### **Required Elements**

1. **Progress Tracker** (framework template includes this)
   - STATUS: Not Started, In Progress, Completed
   - CURRENT STEP: Current phase and task
   - LAST COMPLETED TASK: Description
   - NEXT TASK: Description

2. **Agent Prompt** (optional, for autonomous execution)
   - Define agent role (e.g., "Chief of Staff")
   - Set execution authority
   - Provide context and constraints

3. **Phases and Tasks**
   - Clear phase breakdown
   - Actionable task lists
   - Dependencies identified

4. **Success Criteria**
   - How to validate completion
   - Testing requirements
   - Acceptance criteria

5. **Source Attribution**
   - Reference original requirements
   - Link to related documents
   - Maintain traceability

---

## ✅ Validation Checklist

Use the framework validation tool - it checks:

- ✅ Proper naming convention
- ✅ Required frontmatter fields
- ✅ Directory placement
- ✅ Structure compliance
- ✅ Cross-references

**Manual checklist** (in addition to framework validation):

- [ ] Progress tracker present and current
- [ ] Phases and tasks clearly defined
- [ ] Success criteria measurable
- [ ] Source documents referenced
- [ ] Related artifacts cross-referenced

---

## 🔗 Related

- **Framework Tool**: `AgentQMS/agent_tools/core/artifact_workflow.py`
- **Template**: `AgentQMS/agent_tools/core/artifact_templates.py` (implementation_plan template)
- **Blueprint Protocol**: [03_blueprint_protocol_template.md](03_blueprint_protocol_template.md)
- **Artifact Management Protocol**: [01_artifact_management_protocol.md](01_artifact_management_protocol.md)

---

## ❓ Troubleshooting

**Q: What if the template doesn't fit my needs?**
- The template is a starting point - customize as needed
- Framework validation checks structure, not content
- For major deviations, document rationale

**Q: How do I track progress?**
- Update the progress tracker regularly
- Use checkboxes in task lists
- Document decisions in the plan

**Q: Can I use blueprint protocol format?**
- Yes - see [Blueprint Protocol Template](03_blueprint_protocol_template.md)
- Framework supports blueprint format in templates

---

*This protocol focuses on **workflow** and **tool usage**. The framework template provides the structure - customize as needed while maintaining compliance.*
