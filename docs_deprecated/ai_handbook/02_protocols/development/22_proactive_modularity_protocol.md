# Proactive Modularity Protocol

**Document ID**: `PROTO-DEV-022`
**Status**: ACTIVE
**Last Updated**: 2025-11-20
**Type**: Development Protocol

## 🎯 Purpose

This protocol describes **framework-specific modularity patterns** and how to structure code when working with the AgentQMS framework. For general coding standards, see [Coding Standards V2](01_coding_standards_v2.md).

---

## 🏗️ Framework Modularity Principles

The AgentQMS framework follows specific modularity patterns that projects using the framework should understand:

### **Framework Structure**

```
AgentQMS/
├── agent_tools/           # Implementation layer - functional modules
│   ├── core/              # Core framework functionality
│   ├── compliance/        # Validation and compliance
│   ├── utilities/         # Helper utilities
│   └── utils/             # Framework utilities
├── agent_interface/       # Interface layer - wrappers and CLIs
└── config_defaults/       # Configuration defaults
```

### **Framework Design Principles**

- **Separation of Interface and Implementation**: Interface layer (`agent_interface/`) provides thin wrappers around implementation (`agent_tools/`)
- **Single Responsibility**: Each module has one clear purpose
- **Composability**: Modules can be combined to create workflows
- **Configuration-Driven**: Behavior controlled by configuration, not hardcoded

---

## 📏 General Modularity Guidelines

### Function Size
- Primary functions: <20-30 lines (target)
- Helper functions: <20 lines (target)
- Class methods: <30 lines (target)
- Single responsibility principle

### File Size
- Files: <400 lines max (recommended)
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

## 🔧 Framework-Specific Patterns

### **When Working with Framework Tools**

- **Use framework utilities** - Don't reimplement framework functionality
- **Extend, don't modify** - Extend framework modules rather than modifying them
- **Configuration over code** - Use configuration to customize behavior
- **Compose workflows** - Build on framework tools to create project workflows

### **When Creating Project Modules**

Follow framework patterns:
- **Core logic** → Similar to `agent_tools/core/` structure
- **Utilities** → Similar to `agent_tools/utilities/` structure
- **Interfaces** → Similar to `agent_interface/` wrapper pattern
- **Configuration** → Use `config/` directory at project root

---

## 📋 Modularity Triggers

### **Signs You Need to Refactor**

- Function names with "and" (multiple responsibilities)
- File purposes requiring "and" to describe (multiple concepts)
- Repeated code patterns (3+ similar blocks)
- Multiple data transformations (should be separate functions)
- Different error handling strategies (centralize)
- Separate configuration needs (extract to config)
- Independent testing requirements (separate concerns)

---

## 🔄 Refactoring Strategy

### **Priority Order**

1. **Extract repeated code** → utility functions
2. **Separate data operations** → data modules
3. **Isolate business logic** → processing modules
4. **Centralize configuration** → config modules (use framework config system)
5. **Standardize error handling** → error utilities

### **Development Workflow**

- Plan single primary objective first
- Identify distinct reusable steps
- Create mental module map
- Extract modules during development
- Keep main script <100 lines
- **Data operations** → `data/` or `loaders/`
- **Business logic** → `processors/` or `services/`
- **Output operations** → `output/` or `generators/`
- **Common utilities** → `utils/`

---

## ✅ Validation Checklist

- [ ] Main script is under 100 lines
- [ ] Each module has a single responsibility
- [ ] No repeated code patterns
- [ ] Clear separation between data, processing, and output
- [ ] Configuration uses framework config system
- [ ] Error handling is consistent
- [ ] Module names are descriptive
- [ ] Dependencies are minimal
- [ ] Code is testable
- [ ] Framework utilities used where applicable

---

## 🔗 Related

- **Coding Standards**: [01_coding_standards_v2.md](01_coding_standards_v2.md) - General Python standards
- **Import Handling**: [23_import_handling_protocol.md](23_import_handling_protocol.md) - Framework import patterns
- **Module Schema Reference**: [../../03_references/development/module_schema_reference.md](../../03_references/development/module_schema_reference.md) - Standard module structures

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
