# Bug Fix Protocol

**Document ID**: `PROTO-GOV-004`
**Status**: ACTIVE
**Created**: 2025-10-25
**Last Updated**: 2025-10-25
**Type**: Governance Protocol

## Rules

### Scope
- Applies to: code changes, UI/UX regressions, performance issues, data processing errors
- Does not apply to: pure documentation updates, feature requests

### Trigger Conditions
- Activate when: functional bugs identified, root causes found, fixes implemented and tested

### Required Documentation
- Summary reports in `docs/artifacts/bug_reports/`
- Changelog updates in `docs/CHANGELOG.md`
- Bug reports for serious issues

## AI Agent Guidelines

### When Fixing Bugs
1. **Reproduce issue** in controlled environment
2. **Identify root cause** through code analysis
3. **Implement minimal fix** addressing root cause
4. **Add error handling** and validation
5. **Test comprehensively** to prevent regressions
6. **Document fix** with summary report
7. **Update changelog** under [Unreleased] section

### Documentation Standards
- **Bug Report**: `YYYY-MM-DD_BUG_REPORT_[DESCRIPTION]_V1.md`
- **Changelog**: Add entry with bug description and fix summary
- **Summary**: Include root cause, fix details, and testing performed

### Quality Checklist
- [ ] Root cause identified and documented
- [ ] Fix addresses root cause without regressions
- [ ] Comprehensive testing completed
- [ ] Code follows project standards
- [ ] Error handling added
- [ ] Documentation updated
- [ ] Changelog entry created

## File Locations
- Bug reports: `docs/artifacts/bug_reports/`
- Changelog: `docs/CHANGELOG.md`
- Templates: `docs/artifacts/templates/bug_report_template.md`

## Related Documents
- `docs/ai_handbook/02_protocols/governance/01_artifact_management_protocol.md`
- `docs/artifacts/MASTER_INDEX.md`
