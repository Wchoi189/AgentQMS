# Standards Specification

**Date**: 2025-11-09  
**Audit Scope**: Mandatory Standards Definition  
**Status**: Framework Standards

## Executive Summary

This document defines mandatory standards for the Quality Management Framework, including output directory structure, file naming conventions, frontmatter schemas, and artifact templates. These standards are designed to be self-enforcing through automated validation.

---

## 1. Output Directory Structure

### 1.1 Standard Directory Layout

```
project_root/
├── agent/                          # Agent interface layer
│   ├── Makefile                   # Agent commands
│   ├── config/                    # Agent configuration
│   ├── tools/                     # Agent tool wrappers
│   └── workflows/                 # Workflow scripts
├── agent_tools/                   # Implementation layer
│   ├── core/                      # Core automation
│   ├── compliance/                # Validation tools
│   ├── documentation/             # Doc management
│   ├── utilities/                 # Helper functions
│   └── utils/                     # Framework utilities (NEW)
├── quality_management_framework/  # QMS framework
│   ├── templates/                 # Artifact templates
│   ├── schemas/                   # JSON schemas
│   ├── config/                    # Configuration (NEW)
│   └── toolbelt/                  # Python toolbelt
├── artifacts/                     # Generated artifacts
│   ├── implementation_plans/
│   ├── assessments/
│   ├── design_documents/
│   ├── research/
│   ├── templates/
│   ├── bug_reports/
│   └── user-guides/
├── docs/                          # Documentation
│   ├── ai_handbook/               # AI agent docs
│   └── audit/                     # Audit reports
└── scripts/                       # Utility scripts
```

### 1.2 Directory Naming Rules

**Mandatory**:
- Use lowercase with underscores: `implementation_plans/`
- No spaces or special characters
- Plural form for collections: `assessments/`, `templates/`
- Singular for single-purpose: `config/`, `utils/`

**Forbidden**:
- ❌ `Implementation Plans/` (spaces, capitals)
- ❌ `implementation-plans/` (hyphens)
- ❌ `impl_plans/` (abbreviations)

**Validation**: Automated check in `agent_tools/compliance/validate_structure.py`

---

## 2. File Naming Conventions

### 2.1 Artifact File Naming

**Format**: `YYYY-MM-DD_HHMM_<type>_<name>.md`

**Components**:
- `YYYY-MM-DD`: Date (ISO 8601)
- `HHMM`: Time (24-hour, no colon)
- `<type>`: Artifact type prefix (see 2.2)
- `<name>`: Descriptive name (lowercase, underscores)

**Examples**:
- ✅ `2025-11-09_1430_implementation_plan_feature-x.md`
- ✅ `2025-11-09_1430_assessment-api-design.md`
- ✅ `2025-11-09_1430_BUG_crash-on-startup.md`
- ❌ `implementation_plan.md` (missing date/time)
- ❌ `2025-11-09 implementation plan.md` (spaces, no time)
- ❌ `IMPLEMENTATION_PLAN.md` (wrong prefix format)

### 2.2 Artifact Type Prefixes

| Type | Prefix | Directory | Example |
|------|--------|-----------|---------|
| Implementation Plan | `implementation_plan_` | `implementation_plans/` | `2025-11-09_1430_implementation_plan_feature-x.md` |
| Assessment | `assessment-` | `assessments/` | `2025-11-09_1430_assessment-api-design.md` |
| Design Document | `design-` | `design_documents/` | `2025-11-09_1430_design-auth-system.md` |
| Research | `research-` | `research/` | `2025-11-09_1430_research-llm-options.md` |
| Template | `template-` | `templates/` | `2025-11-09_1430_template-api-spec.md` |
| Bug Report | `BUG_` | `bug_reports/` | `2025-11-09_1430_BUG_crash-on-startup.md` |
| User Guide | `user-guide_` | `user-guides/` | `2025-11-09_1430_user-guide_setup.md` |

**Validation**: Automated prefix check in `agent_tools/compliance/naming.py`

### 2.3 Configuration File Naming

**Format**: `<name>.yaml` or `<name>.json`

**Examples**:
- ✅ `artifact_schema.yaml`
- ✅ `directory_structure.yaml`
- ✅ `project_config.yaml`
- ❌ `artifact-schema.yaml` (hyphens not allowed)
- ❌ `ArtifactSchema.yaml` (camelCase not allowed)

### 2.4 Script File Naming

**Format**: `<name>.py` (lowercase, underscores)

**Examples**:
- ✅ `validate_artifacts.py`
- ✅ `artifact_workflow.py`
- ❌ `ValidateArtifacts.py` (PascalCase not allowed)
- ❌ `validate-artifacts.py` (hyphens not allowed)

---

## 3. Frontmatter Schemas

### 3.1 Standard Frontmatter Structure

All artifacts must include YAML frontmatter with required fields. The `date` field must always include the hour/minute timestamp and regional marker: `YYYY-MM-DD HH:MM (KST)`.

```yaml
---
title: "Artifact Title"
date: "YYYY-MM-DD HH:MM (KST)"
status: "active" | "draft" | "deprecated" | "archived"
version: "1.0"
category: "implementation_plan" | "assessment" | "design" | "research" | "template" | "bug_report" | "user_guide"
tags: ["tag1", "tag2", "tag3"]
---
```

### 3.2 Required Fields by Type

#### Implementation Plan
```yaml
---
title: "Implementation Plan: Feature Name"
date: "2025-11-09 09:00 (KST)"
status: "active" | "draft" | "completed"
version: "1.0"
category: "implementation_plan"
tags: ["feature", "backend", "api"]
owner: "agent-name"  # Optional
priority: "high" | "medium" | "low"  # Optional
---
```

#### Assessment
```yaml
---
title: "Assessment: Topic Name"
date: "2025-11-09 09:00 (KST)"
status: "active" | "draft" | "completed"
version: "1.0"
category: "assessment"
tags: ["evaluation", "analysis"]
scope: "brief description"  # Optional
---
```

#### Design Document
```yaml
---
title: "Design: Component Name"
date: "2025-11-09 09:00 (KST)"
status: "active" | "draft" | "approved" | "deprecated"
version: "1.0"
category: "design"
tags: ["architecture", "component"]
---
```

#### Bug Report
```yaml
---
title: "BUG: Issue Description"
date: "2025-11-09 09:00 (KST)"
status: "open" | "in_progress" | "resolved" | "closed"
version: "1.0"
category: "bug_report"
tags: ["bug", "critical" | "high" | "medium" | "low"]
severity: "critical" | "high" | "medium" | "low"  # Required
reproducible: true | false  # Required
---
```

### 3.3 Field Validation Rules

**Title**:
- Required: Yes
- Type: String
- Length: 5-200 characters
- Format: Sentence case, descriptive

**Date**:
- Required: Yes
- Type: String (`YYYY-MM-DD HH:MM (KST)`)
- Validation: Must be valid 24-hour timestamp in KST, not in the future

**Status**:
- Required: Yes
- Type: Enum (type-specific values)
- Default: "draft"

**Version**:
- Required: Yes
- Type: String (semantic versioning: X.Y or X.Y.Z)
- Default: "1.0"

**Category**:
- Required: Yes
- Type: Enum (must match file prefix)
- Validation: Must match artifact type

**Tags**:
- Required: Yes
- Type: Array of strings
- Min: 1 tag
- Max: 10 tags
- Format: lowercase, hyphens allowed

**Validation**: Automated in `agent_tools/compliance/frontmatter.py`

---

## 4. Artifact Templates

### 4.1 Template Location

All templates in: `quality_management_framework/templates/`

**Naming**: `<type>_template.md`

**Examples**:
- `implementation_plan_template.md`
- `assessment_template.md`
- `bug_report_template.md`

### 4.2 Template Structure

Templates must include:
1. Frontmatter with placeholders
2. Section structure
3. Example content (commented or in examples section)
4. Usage instructions

**Example Template**:
```markdown
---
title: "{{TITLE}}"
date: "{{DATE}}"
status: "draft"
version: "1.0"
category: "{{CATEGORY}}"
tags: ["{{TAG1}}", "{{TAG2}}"]
---

# {{TITLE}}

## Overview
[Brief description of the artifact]

## Objectives
- [Objective 1]
- [Objective 2]

## Details
[Main content]

## Next Steps
- [ ] Action item 1
- [ ] Action item 2

## References
- [Link or reference]
```

### 4.3 Template Variables

**Standard Variables**:
- `{{TITLE}}`: Artifact title
- `{{DATE}}`: Creation date (YYYY-MM-DD)
- `{{CATEGORY}}`: Artifact category
- `{{TAG1}}`, `{{TAG2}}`, etc.: Tags

**Type-Specific Variables**:
- Implementation Plan: `{{OWNER}}`, `{{PRIORITY}}`
- Bug Report: `{{SEVERITY}}`, `{{REPRODUCIBLE}}`

**Validation**: Template validation in `agent_tools/core/template_validator.py`

---

## 5. Code Standards

### 5.1 Python Code Style

**Mandatory**:
- PEP 8 compliance
- Type hints for function signatures
- Docstrings for all public functions/classes
- Maximum line length: 100 characters

**Example**:
```python
def validate_artifact(filename: str, artifact_type: str) -> bool:
    """
    Validate artifact against naming and frontmatter standards.
    
    Args:
        filename: Path to artifact file
        artifact_type: Type of artifact (implementation_plan, etc.)
    
    Returns:
        True if valid, False otherwise
    """
    ...
```

### 5.2 Import Organization

**Order**:
1. Standard library imports
2. Third-party imports
3. Local framework imports

**Example**:
```python
import sys
from pathlib import Path
from typing import Optional

import yaml
import jsonschema

from agent_tools.utils.paths import get_project_root
from agent_tools.compliance.naming import validate_prefix
```

### 5.3 Error Handling

**Mandatory**:
- Specific exception types
- Clear error messages
- Actionable guidance

**Example**:
```python
try:
    artifact = load_artifact(path)
except FileNotFoundError:
    raise RuntimeError(
        f"Artifact not found: {path}\n"
        f"Expected location: {expected_path}\n"
        f"Run 'make create-plan NAME=...' to create artifact."
    )
```

---

## 6. Configuration Standards

### 6.1 YAML Configuration Files

**Location**: `quality_management_framework/config/`

**Format**:
- UTF-8 encoding
- 2-space indentation
- No tabs
- Comments allowed with `#`

**Example**:
```yaml
# Artifact type definitions
artifact_types:
  implementation_plan:
    prefix: "implementation_plan_"
    directory: "implementation_plans/"
    required_fields:
      - title
      - date
      - status
      - version
      - category
    optional_fields:
      - owner
      - priority
```

### 6.2 JSON Schema Files

**Location**: `quality_management_framework/schemas/`

**Format**:
- JSON Schema Draft 7
- Descriptive `$schema` reference
- Clear error messages in `description` fields

**Example**:
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Artifact Frontmatter Schema",
  "type": "object",
  "required": ["title", "date", "status", "version", "category", "tags"],
  "properties": {
    "title": {
      "type": "string",
      "minLength": 5,
      "maxLength": 200,
      "description": "Artifact title in sentence case"
    }
  }
}
```

---

## 7. Documentation Standards

### 7.1 Markdown Format

**Mandatory**:
- Markdown format (`.md` extension)
- Frontmatter for all docs (see 3.1)
- Headers: `#` for title, `##` for sections, `###` for subsections
- Lists: Use `-` for unordered, `1.` for ordered
- Code blocks: Specify language: ` ```python `

### 7.2 Documentation Structure

**Required Sections**:
1. Title (H1)
2. Overview/Introduction
3. Main content (organized with H2/H3)
4. Examples (if applicable)
5. References/Links

**Optional Sections**:
- Prerequisites
- Troubleshooting
- FAQ

### 7.3 Link Standards

**Internal Links**:
- Use relative paths: `[Link Text](../path/to/file.md)`
- No absolute paths
- Validate links exist

**External Links**:
- Use full URLs: `[Link Text](https://example.com)`
- Mark as external if needed

**Validation**: Automated link validation in `agent_tools/documentation/validate_links.py`

---

## 8. Validation & Enforcement

### 8.1 Automated Validation

**Tools**:
- `agent_tools/compliance/validate_artifacts.py`: Comprehensive validation
- `agent_tools/compliance/naming.py`: Naming convention checks
- `agent_tools/compliance/frontmatter.py`: Frontmatter schema validation
- `agent_tools/documentation/validate_links.py`: Link validation

**When to Run**:
- Pre-commit hooks (recommended)
- CI/CD pipeline
- Manual: `make validate`

### 8.2 Validation Rules

**Naming**:
- ✅ Pass: Correct prefix, date/time format, valid characters
- ❌ Fail: Missing prefix, wrong format, invalid characters

**Frontmatter**:
- ✅ Pass: All required fields present, valid values, correct types
- ❌ Fail: Missing fields, invalid values, type mismatches

**Structure**:
- ✅ Pass: File in correct directory, matches prefix
- ❌ Fail: Wrong directory, prefix mismatch

**Links**:
- ✅ Pass: All internal links resolve, external links accessible
- ❌ Fail: Broken internal links, unreachable external links

### 8.3 Self-Enforcing Mechanisms

**Pre-commit Hooks** (Recommended):
```bash
#!/bin/bash
# .git/hooks/pre-commit
python agent_tools/compliance/validate_artifacts.py --staged
```

**CI Integration**:
```yaml
# .github/workflows/validate.yml
- name: Validate Artifacts
  run: |
    cd agent
    make validate
```

**Template Enforcement**:
- Artifact creation tools use templates
- Validation runs automatically on creation
- Cannot create invalid artifacts through framework

---

## 9. Extension Standards

### 9.1 Adding New Artifact Types

**Steps**:
1. Add type definition to `quality_management_framework/config/artifact_schema.yaml`
2. Create template in `quality_management_framework/templates/`
3. Update validator to recognize new type
4. Document in framework docs

**Example**:
```yaml
# config/artifact_schema.yaml
new_type:
  prefix: "new_type-"
  directory: "new_types/"
  required_fields: [title, date, status, version, category, tags]
```

### 9.2 Adding New Validators

**Location**: `agent_tools/compliance/`

**Structure**:
```python
# agent_tools/compliance/new_validator.py
class NewValidator:
    def validate(self, artifact_path: Path) -> ValidationResult:
        """Validate artifact against new rules."""
        ...
```

**Integration**: Add to `validate_artifacts.py` main validator

---

## 10. Compliance Checklist

### For Artifact Creation
- [ ] File name follows naming convention
- [ ] File in correct directory
- [ ] Frontmatter includes all required fields
- [ ] Frontmatter values are valid
- [ ] Content follows template structure
- [ ] Links are valid (if any)

### For Code Contributions
- [ ] Code follows PEP 8
- [ ] Type hints included
- [ ] Docstrings present
- [ ] Error handling with clear messages
- [ ] Tests added (if applicable)

### For Documentation
- [ ] Frontmatter included
- [ ] Structure follows standards
- [ ] Links validated
- [ ] Examples work
- [ ] No hardcoded project names

---

## Summary

These standards ensure:
- **Consistency**: All artifacts follow same structure
- **Discoverability**: Clear naming and organization
- **Validation**: Automated checks prevent violations
- **Extensibility**: Clear process for adding new types
- **Maintainability**: Standards are documented and enforced

**Next Steps**: See `05_automation_recommendations.md` for implementation of self-enforcing mechanisms.

