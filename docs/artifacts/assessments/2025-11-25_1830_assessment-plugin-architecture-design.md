---
title: "Plugin Architecture Design Assessment"
date: "2025-11-25 18:30 (KST)"
type: "assessment"
category: "architecture"
status: "active"
version: "1.0"
tags: ["assessment", "architecture", "plugin-system", "extensibility"]
---

# Plugin Architecture Design Assessment

## Purpose

This assessment evaluates extension point candidates in AgentQMS, analyzes plugin architecture patterns, and proposes a minimal viable plugin system that enables multi-project extensibility while preserving the framework's clean containerization.

## Scope

- **Subject**: AgentQMS extensibility and plugin architecture
- **Assessment Date**: 2025-11-25
- **Assessor**: AI Agent
- **Methodology**: Codebase analysis, pattern evaluation, requirements mapping

---

## Executive Summary

AgentQMS is **structurally well-positioned** for plugin architecture. The existing configuration system, component registry (`architecture.yaml`), and YAML-driven conventions provide a solid foundation. However, current extensibility is **implicit and hardcoded**, requiring direct code modification to add artifact types, validators, or context bundles.

**Key Recommendation**: Implement a **registry-based plugin system** starting with 3 high-value extension points (artifact types, validators, context bundles) using YAML-driven discovery and Python interfaces.

---

## Part 1: Current State Analysis

### 1.1 Strengths (Ready for Extension)

| Aspect | Status | Evidence | Plugin Relevance |
|--------|--------|----------|------------------|
| Configuration System | ✅ Ready | `ConfigLoader` with merge chain | Plugin config loading |
| Component Registry | ✅ Ready | `architecture.yaml` | Plugin discovery index |
| Tool Manifest | ✅ Ready | `q-manifest.yaml` | Tool/type registration |
| YAML Conventions | ✅ Ready | Context bundles, schemas | Declarative plugins |
| Layer Separation | ✅ Ready | `interface/` → `agent_tools/` → `conventions/` | Clean plugin boundaries |
| Path Resolution | ✅ Ready | `paths.py`, `get_artifacts_dir()` | Plugin-aware paths |

### 1.2 Current Extension Mechanisms

```
┌─────────────────────────────────────────────────────────────────┐
│                    CURRENT ARCHITECTURE                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐       │
│  │ settings.yaml│───▶│ConfigLoader  │───▶│effective.yaml│       │
│  └──────────────┘    └──────────────┘    └──────────────┘       │
│         │                   │                                    │
│         ▼                   ▼                                    │
│  ┌──────────────┐    ┌──────────────┐                           │
│  │ q-manifest   │◀───│ArtifactTypes │  (hardcoded in Python)    │
│  │   .yaml      │    │  Templates   │                           │
│  └──────────────┘    └──────────────┘                           │
│         │                   │                                    │
│         ▼                   ▼                                    │
│  ┌──────────────┐    ┌──────────────┐                           │
│  │ Validators   │    │Context       │  (hardcoded prefixes,     │
│  │ (hardcoded)  │    │ Bundles      │   types, categories)      │
│  └──────────────┘    └──────────────┘                           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 1.3 Identified Gaps

| Gap | Location | Impact | Remediation Complexity |
|-----|----------|--------|------------------------|
| Hardcoded artifact types | `ArtifactTemplates.__init__` | Cannot add types without code | Medium |
| Hardcoded validators | `ArtifactValidator.__init__` | `valid_prefixes`, `valid_types`, `valid_categories` | Medium |
| No plugin discovery | `discover.py` scans fixed categories | No external tools | Low |
| No hook system | Only `update_bundles_on_artifact_change` | Limited extension points | High |
| Coupled templates | Templates embedded in Python | Cannot override from config | Medium |

### 1.4 Existing Patterns Worth Preserving

1. **Configuration Merge Chain**: `defaults → framework → project → environment`
2. **YAML-First Declarations**: Context bundles, architecture.yaml
3. **Runtime Snapshot**: `effective.yaml` audit trail
4. **Component Registry**: Structured capability mapping
5. **Shim Layer Pattern**: `agent_tools/` → `toolkit/` compatibility

---

## Part 2: Extension Point Analysis

### 2.1 Extension Point Candidates

| Extension Point | Value | Complexity | Use Cases |
|-----------------|-------|------------|-----------|
| **Artifact Types** | 🔴 Critical | Medium | Custom document types, industry-specific artifacts |
| **Validators** | 🟡 High | Medium | Custom naming rules, domain validation |
| **Context Bundles** | 🟡 High | Low | Project-specific context sets |
| **Audit Phases** | 🟠 Medium | High | Custom audit methodologies |
| **Tool Registry** | 🟠 Medium | Medium | Custom CLI tools |
| **Template Overrides** | 🟢 Low | Low | Project-specific templates |

### 2.2 Detailed Analysis: High-Priority Extension Points

#### 2.2.1 Artifact Types (Critical)

**Current Implementation:**
```python
# AgentQMS/toolkit/core/artifact_templates.py (hardcoded)
self.templates = {
    "implementation_plan": {...},
    "assessment": {...},
    "bug_report": {...},
    # Cannot add without code modification
}
```

**Extension Requirements:**
- Register new artifact types via YAML
- Define custom templates, schemas, validation rules
- Specify output directories and filename patterns
- Support type inheritance (base templates)

**Proposed Plugin Interface:**
```yaml
# .agentqms/plugins/artifact_types/custom_type.yaml
name: change_request
version: 1.0
extends: implementation_plan  # Optional inheritance

metadata:
  filename_pattern: "CR_{date}_{name}.md"
  directory: change_requests/
  frontmatter:
    type: change_request
    category: governance
    status: pending_approval

validation:
  required_fields: [title, date, type, approver]
  custom_validators:
    - name: require_approver_section
      module: myproject.validators.cr_validator

template: |
  # Change Request: {title}
  
  ## Approval Section
  - **Requested By**: {author}
  - **Approver**: [Pending]
  ...
```

#### 2.2.2 Validators (High)

**Current Implementation:**
```python
# AgentQMS/agent_tools/compliance/validate_artifacts.py
self.valid_prefixes = {
    "implementation_plan_": "implementation_plans/",
    "assessment-": "assessments/",
    # Hardcoded, cannot extend
}
self.valid_types = ["implementation_plan", "assessment", ...]
self.valid_categories = ["development", "architecture", ...]
```

**Extension Requirements:**
- Register custom prefixes and directories
- Add/override valid types and categories
- Custom validation functions (Python callables)
- Validation rule enable/disable per project

**Proposed Plugin Interface:**
```yaml
# .agentqms/plugins/validators.yaml
prefixes:
  change_request_: change_requests/
  spec_: specifications/

types:
  - change_request
  - specification
  - decision_record

categories:
  - governance
  - compliance
  - security

custom_validators:
  - name: security_classification_check
    module: myproject.validators.security
    function: validate_classification
    applies_to: [specification, change_request]
```

#### 2.2.3 Context Bundles (High)

**Current Implementation:**
Already YAML-driven under `AgentQMS/knowledge/context_bundles/`. This is the **closest to plugin-ready**.

**Gap:** No mechanism for project-level bundle additions.

**Proposed Enhancement:**
```yaml
# .agentqms/context_bundles/myproject-security.yaml
name: security-review
title: Security Review Context
description: Context for security-focused code reviews

tiers:
  tier1:
    name: Security Standards
    files:
      - path: myproject/security/policies.md
        priority: critical
      - path: myproject/security/threat-model.md
        priority: high
```

**Discovery Path:** Merge bundles from:
1. `AgentQMS/knowledge/context_bundles/*.yaml` (framework)
2. `.agentqms/context_bundles/*.yaml` (project plugins)

---

## Part 3: Architecture Pattern Evaluation

### 3.1 Pattern Comparison

| Pattern | Pros | Cons | Fit for AgentQMS |
|---------|------|------|------------------|
| **Registry-Based** | Simple, declarative, YAML-friendly | Less dynamic | ✅ Excellent |
| **Hook-Based** | Fine-grained control, event-driven | Complex, harder to test | ⚠️ Partial |
| **Entry Points** | Python standard, pip-friendly | Requires packaging | 🔄 Future |
| **File Discovery** | No code changes, hot-reload | Path management, conflicts | ✅ Good |

### 3.2 Recommended Architecture: Hybrid Registry + Discovery

```
┌─────────────────────────────────────────────────────────────────┐
│                    PROPOSED ARCHITECTURE                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    Plugin Loader                          │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐       │   │
│  │  │ Framework   │  │ Project     │  │ Entry       │       │   │
│  │  │ Plugins     │  │ Plugins     │  │ Points      │       │   │
│  │  │ (builtin)   │  │ (.agentqms) │  │ (pip pkgs)  │       │   │
│  │  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘       │   │
│  │         │                │                │               │   │
│  │         └────────────────┼────────────────┘               │   │
│  │                          ▼                                │   │
│  │                 ┌─────────────────┐                       │   │
│  │                 │ Plugin Registry │                       │   │
│  │                 │ (merged config) │                       │   │
│  │                 └────────┬────────┘                       │   │
│  └──────────────────────────┼───────────────────────────────┘   │
│                             │                                    │
│         ┌───────────────────┼───────────────────┐               │
│         ▼                   ▼                   ▼               │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐         │
│  │ Artifact    │    │ Validators  │    │ Context     │         │
│  │ Type Plugin │    │ Plugin API  │    │ Bundle API  │         │
│  └─────────────┘    └─────────────┘    └─────────────┘         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 3.3 Plugin Discovery Flow

```
1. Framework Load
   └─▶ Load AgentQMS/conventions/plugins/*.yaml (builtin)
   
2. Project Load  
   └─▶ Load .agentqms/plugins/*.yaml (project-specific)
   
3. Entry Points (Phase 2)
   └─▶ Load from installed packages with `agentqms.plugins` group
   
4. Merge & Validate
   └─▶ Merge registries with conflict detection
   └─▶ Validate plugin schemas
   └─▶ Write to .agentqms/state/plugins.yaml (runtime snapshot)
   
5. Inject into Components
   └─▶ ArtifactTemplates loads from registry
   └─▶ ArtifactValidator loads from registry
   └─▶ context_bundle.py loads from registry
```

---

## Part 4: Minimal Viable Plugin System (MVP)

### 4.1 MVP Scope

| Feature | MVP | Phase 2 | Phase 3 |
|---------|-----|---------|---------|
| YAML artifact type registration | ✅ | | |
| Config-driven validator extension | ✅ | | |
| Project-level context bundles | ✅ | | |
| Plugin schema validation | ✅ | | |
| Python callable validators | | ✅ | |
| Entry point discovery | | ✅ | |
| Plugin dependency management | | | ✅ |
| Plugin versioning/updates | | | ✅ |

### 4.2 MVP File Structure

```
.agentqms/
├── settings.yaml              # Existing config
├── effective.yaml             # Runtime snapshot
├── plugins/                   # NEW: Plugin definitions
│   ├── artifact_types/        # Custom artifact types
│   │   └── change_request.yaml
│   ├── validators.yaml        # Validator extensions
│   └── context_bundles/       # Custom context bundles
│       └── security-review.yaml
└── state/
    ├── architecture.yaml      # Existing component map
    └── plugins.yaml           # NEW: Merged plugin registry
```

### 4.3 MVP Implementation Plan

#### Phase 1: Plugin Infrastructure (Week 1-2)

1. **Create Plugin Loader Module**
   - `AgentQMS/agent_tools/core/plugin_loader.py`
   - YAML discovery from framework + project paths
   - Schema validation using JSON Schema
   - Merge logic with conflict detection

2. **Define Plugin Schemas**
   - `AgentQMS/conventions/schemas/plugin_artifact_type.json`
   - `AgentQMS/conventions/schemas/plugin_validators.json`
   - `AgentQMS/conventions/schemas/plugin_context_bundle.json`

3. **Update ConfigLoader**
   - Add `load_plugins()` method
   - Generate `plugins.yaml` runtime snapshot

#### Phase 2: Component Integration (Week 3-4)

4. **Refactor ArtifactTemplates**
   - Load types from plugin registry (merge with builtins)
   - Support template inheritance (`extends:` key)

5. **Refactor ArtifactValidator**
   - Load `valid_prefixes`, `valid_types`, `valid_categories` from registry
   - Keep hardcoded values as defaults

6. **Enhance Context Bundle Loading**
   - Discover bundles from `.agentqms/plugins/context_bundles/`
   - Merge with framework bundles

#### Phase 3: Testing & Documentation (Week 5)

7. **Add Plugin Tests**
   - Discovery tests
   - Schema validation tests
   - Integration tests with sample plugins

8. **Update Documentation**
   - Plugin authoring guide
   - API reference for plugin interfaces
   - Migration guide for existing extensions

### 4.4 MVP API Contracts

#### 4.4.1 Artifact Type Plugin Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["name", "version", "metadata", "template"],
  "properties": {
    "name": {"type": "string", "pattern": "^[a-z_]+$"},
    "version": {"type": "string"},
    "extends": {"type": "string"},
    "metadata": {
      "type": "object",
      "required": ["filename_pattern", "directory"],
      "properties": {
        "filename_pattern": {"type": "string"},
        "directory": {"type": "string"},
        "frontmatter": {"type": "object"}
      }
    },
    "validation": {
      "type": "object",
      "properties": {
        "required_fields": {"type": "array", "items": {"type": "string"}},
        "custom_validators": {"type": "array"}
      }
    },
    "template": {"type": "string"}
  }
}
```

#### 4.4.2 Plugin Loader Interface

```python
# AgentQMS/agent_tools/core/plugin_loader.py

class PluginLoader:
    """Loads and merges plugins from framework and project sources."""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.framework_root = project_root / "AgentQMS"
    
    def discover_plugins(self) -> Dict[str, List[Plugin]]:
        """Discover all plugins from registered sources."""
        ...
    
    def load_artifact_types(self) -> Dict[str, ArtifactTypePlugin]:
        """Load and merge artifact type plugins."""
        ...
    
    def load_validators(self) -> ValidatorConfig:
        """Load and merge validator configuration."""
        ...
    
    def load_context_bundles(self) -> Dict[str, ContextBundlePlugin]:
        """Load and merge context bundle plugins."""
        ...
    
    def write_runtime_snapshot(self) -> Path:
        """Write merged plugin state to .agentqms/state/plugins.yaml."""
        ...
```

---

## Part 5: Multi-Project Considerations

### 5.1 Plugin Sharing Strategies

| Strategy | Mechanism | Use Case |
|----------|-----------|----------|
| **Copy** | Copy plugin YAML to `.agentqms/plugins/` | Simple, one-off |
| **Git Submodule** | Submodule in `plugins/shared/` | Versioned sharing |
| **Pip Package** | `agentqms.plugins` entry point | Organization-wide |
| **Monorepo** | Shared plugin directory | Related projects |

### 5.2 Namespace Collision Prevention

```yaml
# Plugin naming convention
# Format: {scope}_{name}
# Scopes: org_, project_, builtin_

# Example: org_acme_change_request.yaml
name: org_acme_change_request
version: 1.0
scope: org_acme  # Namespace for conflict detection
```

### 5.3 Override Precedence

```
1. Project plugins override framework plugins (same name)
2. Environment-specific plugins override project plugins
3. Explicit disable in settings.yaml removes plugins

# .agentqms/settings.yaml
plugins:
  disabled:
    - builtin_research  # Disable builtin research type
  overrides:
    implementation_plan:
      metadata:
        directory: plans/  # Override output directory
```

---

## Recommendations

### High Priority (MVP)

1. **Implement Plugin Loader** - Central registry with YAML discovery
2. **Externalize Artifact Types** - Move hardcoded templates to YAML plugins
3. **Config-Driven Validators** - Load prefixes/types/categories from config
4. **Project Context Bundles** - Enable `.agentqms/plugins/context_bundles/`

### Medium Priority (Phase 2)

5. **Python Callable Validators** - Support custom validation functions
6. **Entry Point Discovery** - Enable pip-installable plugins
7. **Plugin CLI** - `make plugin-list`, `make plugin-validate`

### Low Priority (Phase 3)

8. **Plugin Marketplace** - Central registry of community plugins
9. **Plugin Versioning** - Semantic versioning and compatibility checks
10. **Hot Reload** - Reload plugins without restart

---

## Implementation Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Breaking existing workflows | Medium | High | Feature flag for plugin system |
| Performance overhead | Low | Medium | Lazy loading, caching |
| Configuration complexity | Medium | Medium | Sensible defaults, good docs |
| Plugin conflicts | Medium | Low | Namespace conventions, validation |

---

## Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Plugin adoption | 3+ projects using custom plugins | Usage tracking |
| Type extensibility | 0 code changes to add artifact types | Developer survey |
| Time to extend | <30 min to create new artifact type | Onboarding test |
| Backwards compatibility | 100% existing workflows work | CI regression tests |

---

## Conclusion

AgentQMS has a strong foundation for plugin architecture. The recommended approach:

1. **Start with Registry-Based MVP** - YAML-driven, minimal code changes
2. **Focus on 3 Extension Points** - Artifact types, validators, context bundles
3. **Preserve Existing Patterns** - Extend ConfigLoader, maintain merge chains
4. **Plan for Growth** - Design API contracts that support Phase 2/3 features

The proposed MVP can be implemented in **5 weeks** with minimal disruption to existing users, providing immediate value for multi-project scenarios.

---

## Next Steps

1. ☐ Review and approve this assessment
2. ☐ Create Implementation Plan artifact based on MVP scope
3. ☐ Define detailed plugin schemas (JSON Schema)
4. ☐ Prototype plugin loader with artifact types
5. ☐ Document plugin authoring guide

---

*This assessment follows the AgentQMS standardized format for evaluation and analysis.*

