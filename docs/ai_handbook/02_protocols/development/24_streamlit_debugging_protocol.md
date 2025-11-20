# Streamlit Debugging Protocol

**Document ID**: `PROTO-DEV-024`
**Status**: ACTIVE
**Created**: 2025-10-25
**Last Updated**: 2025-10-25
**Type**: Development Protocol

## Rules

### Debugging Environment
- Always test in live browser app
- Never rely on test scripts or terminal debugging
- Start app with: `streamlit run streamlit_app/main.py --server.port 8503 --server.headless true`

### Schema Page Debugging
- Schema pages require live app testing
- Configuration errors only appear in browser
- Session state issues need real environment

### Error Types
- **Import Errors**: Check import patterns in browser console
- **Schema Configuration**: Implement missing functions/variables referenced in YAML
- **Session State**: Initialize missing session state variables
- **Component Rendering**: Check component configuration and services

## AI Agent Guidelines

### When Debugging Imports
- Start live app first
- Navigate to problematic page
- Check browser console for ModuleNotFoundError/ImportError
- Fix import pattern
- Refresh browser to test

### When Debugging Schema Issues
- Start live app
- Navigate to schema page
- Look for red error boxes
- Identify missing functions/variables from YAML
- Implement required code
- Test in browser

### When Debugging Session State
- Start live app
- Navigate to page with session state issues
- Look for "Cannot access 'variable' on SessionStateProxy"
- Initialize missing session state variables
- Test functionality

## Validation Checklist
- [ ] Live app starts without errors
- [ ] All pages load in browser
- [ ] No red error boxes in UI
- [ ] Components render correctly
- [ ] Data displays properly
- [ ] User interactions work
- [ ] Schema pages function correctly

## Related Documents
- `docs/ai_handbook/02_protocols/development/23_import_handling_protocol.md`
- `docs/ai_handbook/02_protocols/development/code_generation_quality_protocol.md`
- `docs/ai_handbook/03_references/development/schema_configuration_fix.md`
- `docs/ai_handbook/03_references/development/import_handling_reference.md`
