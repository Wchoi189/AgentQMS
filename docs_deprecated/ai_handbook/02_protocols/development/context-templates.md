# Context Templates

**Document ID**: `PROTO-DEV-026`
**Status**: ACTIVE
**Created**: 2025-10-25
**Last Updated**: 2025-10-25
**Type**: Development Protocol

## Component Overview Template
```markdown
# [Component Name] - Quick Context

## Purpose
- What it does in 1 sentence
- Why it exists
- When to use it

## Key Files (Max 3)
1. `file1.py` - Primary responsibility
2. `file2.py` - Secondary responsibility
3. `file3.py` - Supporting functionality

## Dependencies
- Requires: [list]
- Provides: [list]
- Conflicts with: [list]

## Common Tasks
- Task 1: [command/action]
- Task 2: [command/action]
- Task 3: [command/action]

## Troubleshooting
- Problem 1: [solution]
- Problem 2: [solution]
```

## Task Context Template
```markdown
# [Task Name] - Execution Context

## Prerequisites
- [ ] Check 1
- [ ] Check 2
- [ ] Check 3

## Required Context (Max 5 files)
1. `file1.py` - [reason]
2. `file2.py` - [reason]
3. `file3.py` - [reason]

## Execution Steps
1. Step 1: [action]
2. Step 2: [action]
3. Step 3: [action]

## Success Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Common Pitfalls
- Pitfall 1: [avoidance strategy]
- Pitfall 2: [avoidance strategy]
```

## 🎯 **Template 3: Architecture Context**

```markdown
# [System Name] - Architecture Context

## Overview
- High-level purpose
- Key responsibilities
- Integration points

## Component Map
```
[Visual diagram or ASCII art]
```

## Data Flow
1. Input → [component] → [component] → Output
2. [specific flow for common use case]

## Key Interfaces
- Interface 1: [purpose]
- Interface 2: [purpose]
- Interface 3: [purpose]

## Configuration
- Config file: [location]
- Key settings: [list]
- Environment variables: [list]
```

## 🎯 **Template 4: Problem-Solving Context**

```markdown
# [Problem Domain] - Problem-Solving Context

## Common Problems
1. **Problem 1**: [description]
   - Symptoms: [list]
   - Causes: [list]
   - Solutions: [list]

2. **Problem 2**: [description]
   - Symptoms: [list]
   - Causes: [list]
   - Solutions: [list]

## Diagnostic Steps
1. Check [location] for [indicator]
2. Verify [condition] in [file]
3. Test [functionality] with [method]

## Quick Fixes
- Fix 1: [command/action]
- Fix 2: [command/action]
- Fix 3: [command/action]

## When to Escalate
- [condition] → [action]
- [condition] → [action]
```

## 🎯 **Template 5: Development Context**

```markdown
# [Feature/Module] - Development Context

## Current Status
- Phase: [current phase]
- Progress: [percentage]
- Blockers: [list]

## Development Environment
- Setup: [commands]
- Dependencies: [list]
- Configuration: [files]

## Testing Strategy
- Unit tests: [location]
- Integration tests: [location]
- Manual testing: [steps]

## Deployment
- Build: [commands]
- Deploy: [commands]
- Verify: [commands]

## Related Work
- Depends on: [list]
- Blocks: [list]
- Related to: [list]
```

## 📋 **Usage Guidelines**

### **For AI Agents**
1. **Always use templates** for new documentation
2. **Fill in all sections** - don't leave blanks
3. **Keep it concise** - maximum 1 page per template
4. **Update regularly** - review monthly

### **For Humans**
1. **Create templates first** before detailed docs
2. **Use templates as checklists** for completeness
3. **Share templates** with team members
4. **Iterate on templates** based on usage feedback

## 🔄 **Template Maintenance**

### **Monthly Review**
- [ ] Check template usage statistics
- [ ] Update based on common patterns
- [ ] Remove unused sections
- [ ] Add missing sections

### **Quarterly Update**
- [ ] Full template revision
- [ ] User feedback integration
- [ ] Best practices incorporation
- [ ] Version control update
