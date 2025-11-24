# AgentQMS Framework - Deployment Recommendations

## Overview

This document provides recommendations for deploying and maintaining the AgentQMS framework based on the comprehensive audit conducted on 2025-11-24. The framework is designed as a containerized Quality Management System for AI coding agents that can be imported into other projects.

## Critical Deployment Considerations

### 1. Python Module Import Strategy

**Current State**: The framework uses a custom import approach where:
- The project root must be added to `sys.path` for imports to work
- Scripts use `ensure_project_root_on_sys_path()` from `AgentQMS.agent_tools.utils.runtime`

**Recommendations**:

#### Option A: Add setup.py or pyproject.toml (Recommended for Production)
```python
# setup.py
from setuptools import setup, find_packages

setup(
    name="agentqms",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "pyyaml>=6.0.3",
    ],
    python_requires=">=3.11",
)
```

**Benefits**:
- Standard Python package installation: `pip install -e .`
- Cleaner imports without manual sys.path manipulation
- Better compatibility with virtual environments and deployment tools

#### Option B: Keep Current Approach (Current Implementation)
- Always set `PYTHONPATH=.` when running scripts
- Document this requirement clearly in all usage guides
- Ensure CI/CD workflows include `PYTHONPATH=.` in environment

**Current CI/CD Implementation**: All workflow steps now include `PYTHONPATH=.` prefix:
```yaml
run: |
  PYTHONPATH=. python AgentQMS/agent_tools/compliance/validate_artifacts.py --all
```

### 2. Framework Structure and Import Targets

**Export Configuration**: When importing into another project, copy only:
- `.agentqms/` - Hidden framework state and configuration
- `AgentQMS/` - Framework container with all components

**Do NOT export**:
- `docs/` - Project-specific history and artifacts
- Root-level project files (README.md specific to this repo)

### 3. Implementation Layer Naming

**Current State**: Dual naming exists:
- `AgentQMS/agent_tools/` - Canonical implementation layer
- `AgentQMS/toolkit/` - Legacy compatibility layer

**Recommendation**: 
- Always reference `agent_tools` in new code and documentation
- Keep `toolkit` as a thin wrapper for backward compatibility
- Add deprecation notices to `toolkit` documentation

### 4. CI/CD Best Practices

#### Required Validations

Create a GitHub Actions workflow that runs:
```yaml
- name: Validate artifacts
  run: PYTHONPATH=. python AgentQMS/agent_tools/compliance/validate_artifacts.py --all

- name: Validate boundaries
  run: PYTHONPATH=. python AgentQMS/agent_tools/compliance/validate_boundaries.py --json

- name: Validate documentation
  run: |
    PYTHONPATH=. python AgentQMS/agent_tools/documentation/auto_generate_index.py --validate
    PYTHONPATH=. python AgentQMS/agent_tools/documentation/validate_manifest.py docs/ai_handbook/index.json

- name: Validate links
  run: PYTHONPATH=. python AgentQMS/agent_tools/documentation/validate_links.py docs
```

#### Pre-commit Hooks

Configure `.pre-commit-config.yaml`:
```yaml
repos:
  - repo: local
    hooks:
      - id: agentqms-validate-artifacts
        name: AgentQMS - Validate Artifacts
        entry: bash -c 'PYTHONPATH=. python AgentQMS/agent_tools/compliance/validate_artifacts.py --staged'
        language: system
        pass_filenames: false
        
      - id: agentqms-validate-docs
        name: AgentQMS - Validate Documentation
        entry: bash -c 'PYTHONPATH=. python AgentQMS/agent_tools/documentation/auto_generate_index.py --validate'
        language: system
        pass_filenames: false
```

### 5. Documentation Migration

**Current State**: Documentation is split between:
- `docs/ai_handbook/` - Legacy handbook (project history)
- `AgentQMS/knowledge/` - New containerized knowledge base

**Recommendations**:
- Complete migration of active protocols to `AgentQMS/knowledge/protocols/`
- Complete migration of references to `AgentQMS/knowledge/references/`
- Keep `docs/ai_handbook/` as project history (not exported)
- Update all internal references to use `AgentQMS/knowledge/*` paths

### 6. Path References and Legacy Code

**Resolved Issues**:
- ✅ Fixed interface workflows to use correct paths
- ✅ Updated auto_generate_index.py to use containerized paths
- ✅ Fixed CI/CD PYTHONPATH configuration

**Remaining Considerations**:
- Some monitoring/maintenance scripts contain comments referencing old `scripts/agent_tools` structure
- These are informational only and don't affect functionality
- Consider updating comments in future refactoring passes

## Deployment Checklist for New Projects

### Initial Setup
- [ ] Copy `.agentqms/` and `AgentQMS/` to project root
- [ ] Configure `PROJECT_ROOT/.agentqms/settings.yaml` if needed
- [ ] Verify PYTHONPATH is set correctly for script execution
- [ ] Run initial validation: `make discover && make status`

### CI/CD Integration
- [ ] Add `.github/workflows/agentqms-validation.yml`
- [ ] Configure all Python invocations with `PYTHONPATH=.`
- [ ] Test workflow in a feature branch before merging
- [ ] Set up badge in README showing validation status

### Pre-commit Setup (Optional but Recommended)
- [ ] Install pre-commit: `pip install pre-commit`
- [ ] Add `.pre-commit-config.yaml` with AgentQMS hooks
- [ ] Run `pre-commit install`
- [ ] Test with `pre-commit run --all-files`

### Development Workflow
- [ ] Use Makefile targets from `AgentQMS/interface/` for common tasks
- [ ] Create artifacts via: `make create-plan NAME=... TITLE="..."`
- [ ] Validate regularly: `make validate && make compliance`
- [ ] Generate docs: `make docs-refresh`

## Best Practices for Maintainers

### 1. Artifact Management
- Use templates from `AgentQMS/conventions/templates/`
- Follow naming convention: `YYYY-MM-DD_HHMM_[TYPE]_descriptive-name.md`
- Include proper frontmatter with required fields
- Run validation before committing

### 2. Interface Layer Usage
- Agents should use Makefile targets or workflows from `AgentQMS/interface/`
- Human developers can use either Makefile or direct Python script invocation
- Always run from `AgentQMS/interface/` directory for relative paths to work

### 3. Code Organization
- New implementation code goes in `AgentQMS/agent_tools/`
- Conventions and templates go in `AgentQMS/conventions/`
- Agent-facing docs go in `AgentQMS/knowledge/`
- Project-specific artifacts stay in `PROJECT_ROOT/docs/artifacts/`

### 4. Configuration Management
- Primary config: `.agentqms/settings.yaml`
- Runtime state: `.agentqms/state/architecture.yaml`
- Effective config snapshot: `.agentqms/effective.yaml`
- Use config loader utilities from `AgentQMS.agent_tools.utils.config`

## Future Improvements

### Short Term (1-3 months)
1. Add setup.py/pyproject.toml for proper package installation
2. Complete documentation migration to `AgentQMS/knowledge/`
3. Add more comprehensive integration tests
4. Create example project showing framework integration

### Medium Term (3-6 months)
1. Add support for multiple artifact storage backends
2. Implement smart context loading as described in references
3. Create web UI for artifact management (optional)
4. Add metrics and analytics for framework usage

### Long Term (6-12 months)
1. Consider plugin architecture for custom validators
2. Add support for multiple project types/languages
3. Create marketplace for shared conventions and templates
4. Build integration with popular CI/CD platforms

## Support and Resources

### Key Documentation Files
- Framework Overview: `README.md`
- Interface Guide: `AgentQMS/interface/README.md`
- Audit Reports: `docs/audit/2025-11-24_audit/`
- Maintainer Guide: `AgentQMS/knowledge/meta/MAINTAINERS.md`

### Getting Help
- Check `AgentQMS/knowledge/agent/system.md` for agent instructions
- Review protocols in `AgentQMS/knowledge/protocols/`
- Run `make help` from `AgentQMS/interface/` for available commands

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'AgentQMS'`
**Solution**: Ensure PYTHONPATH includes project root: `PYTHONPATH=. python script.py`

**Issue**: Workflow scripts fail with "file not found"
**Solution**: Run from `AgentQMS/interface/` directory, not from workflow subdirectory

**Issue**: Validation fails for legacy artifacts
**Solution**: Legacy artifacts in `docs/` are not required to follow new conventions. Focus on artifacts created after framework adoption.

## Version History

- **2025-11-24**: Initial deployment recommendations based on comprehensive audit
  - Fixed CI/CD failures
  - Updated workflow scripts
  - Documented current state and best practices

---

For questions or contributions, please refer to the project's issue tracker or contact the maintainers.
