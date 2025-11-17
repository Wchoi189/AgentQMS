# Artifact Management Protocol

**Document ID**: `PROTO-GOV-001`
**Status**: ACTIVE
**Created**: 2025-10-25
**Last Updated**: 2025-10-25
**Type**: Governance Protocol

## Rules

### Separation of Concerns
- Project root: Only active code, config, essential files
- Documentation: All artifacts in dedicated folders outside project root
- No mixing implementation artifacts with source code

### Naming Conventions
- Timestamped: All artifacts include creation date in filename
- HHMM Required: Session-generated artifacts (handovers, quick references) include hours/minutes
- Categorized: Clear prefixes indicate artifact type
- Versioned: Sequential numbering for related artifacts
- Descriptive: Names clearly indicate content and purpose

### Traceability
- Source attribution: Every artifact references source documents
- Cross-references: Clear links between related artifacts
- Index system: Central registry of all artifacts

## Directory Structure
```
docs/artifacts/
├── MASTER_INDEX.md
├── implementation_plans/
│   ├── 2025-10-23_IMPLEMENTATION_PLAN_schema_engine_phase_5_continuation.md
│   ├── 2025-10-25_1200_SESSION_HANDOVER_documentation_framework_audit.md
│   ├── 2025-10-24_IMPLEMENTATION_PLAN_schema_engine_refactoring.md
│   └── 2025-10-27_IMPLEMENTATION_PLAN_component_renderer_refactoring.md
├── assessments/
│   ├── 2025-10-23_schema_architecture_gap_analysis.md
│   ├── 2025-10-24_schema_engine_audit.md
│   └── 2025-10-27_documentation_framework_audit.md
├── bug_reports/
│   ├── 2025-10-25_BUG_REPORT_streamlit_import_error.md
│   ├── 2025-10-26_BUG_REPORT_schema_validation_failure.md
│   └── 2025-10-27_BUG_REPORT_component_rendering_issue.md
├── design_documents/
│   ├── 2025-10-23_file_based_schema_architecture.md
│   ├── 2025-10-24_page_migration_guide.md
│   └── 2025-10-25_prompt_versioning_evaluation_storage_brainstorm.md
├── research/
├── templates/
└── INDEX.md
```

## File Naming
```
YYYY-MM-DD_[CATEGORY]_[DESCRIPTIVE_NAME]_[VERSION].md
```

### Session-Generated Artifacts (HHMM Required)
Session handovers, quick references, and other session artifacts must include HHMM timestamps:
```
YYYY-MM-DD_HHMM_[CATEGORY]_[DESCRIPTIVE_NAME]_[VERSION].md
```

### Category-Specific Examples
- **Implementation Plans**: `2025-10-23_IMPLEMENTATION_PLAN_schema_engine_refactoring.md`
- **Session Handovers**: `2025-10-25_1200_SESSION_HANDOVER_dynamic_few_shot_implementation.md`
- **Assessments**: `2025-10-24_schema_engine_audit.md`
- **Bug Reports**: `2025-10-25_BUG_REPORT_streamlit_import_error.md`
- **Design Documents**: `2025-10-23_file_based_schema_architecture.md`

## Required Actions
- Check existing artifacts before creating
- Use correct directory (never project root)
- Include document header with ID, status, dates
- Reference source documents
- Update INDEX.md files
- Cross-reference related artifacts

## Compliance
- Never create artifacts in project root
- Always use timestamped filenames
- Include HHMM timestamps for session-generated artifacts
- Include source document references
- Update index files immediately
- Follow naming conventions exactly
- Use approved templates only
