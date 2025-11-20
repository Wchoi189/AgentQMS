# Proactive Modularity Protocol

**Document ID**: `PROTO-DEV-022`
**Status**: ACTIVE
**Created**: 2025-10-25
**Last Updated**: 2025-10-25
**Type**: Development Protocol

## Rules

### Function Size
- Primary functions: <20-30 lines
- Helper functions: <20 lines
- Class methods: <30 lines
- Single responsibility principle

### File Size
- Files: <400 lines max
- High cohesion principle
- One central concept per file

### Modularity Triggers
- Function names with "and"
- File purposes requiring "and" to describe
- Repeated code patterns (3+ similar blocks)
- Multiple data transformations
- Different error handling strategies
- Separate configuration needs
- Independent testing requirements

### Development Strategy
- Plan single primary objective first
- Identify distinct reusable steps
- Create mental module map
- Extract modules during development
- Keep main script <100 lines
- **Data operations** → `data_loader.py`
- **Business logic** → `processor.py`
- **Output operations** → `output_generator.py`
- **Common utilities** → `utils/`

## Refactoring Priority
1. Extract repeated code → utility functions
2. Separate data operations → data modules
3. Isolate business logic → processing modules
4. Centralize configuration → config modules
5. Standardize error handling → error utilities

## AI Agent Guidelines

### When Writing Code
- Start modular - Extract modules from the beginning
- Keep scripts short - Main logic under 100 lines
- Use clear names - Module names should be self-explanatory
- Separate concerns - Data, processing, output, utilities
- Plan for reuse - Design modules to be reusable

### When Refactoring
- Identify patterns - Look for repeated code
- Extract utilities - Common functions go to utils/
- Separate data ops - Data operations go to data/
- Isolate business logic - Processing goes to processing/
- Centralize config - Configuration goes to config/

### When Reviewing Code
- Check line counts - Flag scripts over 100 lines
- Verify single responsibility - Each module has one purpose
- Look for reuse opportunities - Can this be extracted?
- Validate naming - Are names clear and consistent?
- Test modularity - Can modules be tested independently?

## Validation Checklist
- [ ] Main script is under 100 lines
- [ ] Each module has a single responsibility
- [ ] No repeated code patterns
- [ ] Clear separation between data, processing, and output
- [ ] Configuration is centralized
- [ ] Error handling is consistent
- [ ] Module names are descriptive
- [ ] Dependencies are minimal
- [ ] Code is testable
- [ ] Documentation is clear
