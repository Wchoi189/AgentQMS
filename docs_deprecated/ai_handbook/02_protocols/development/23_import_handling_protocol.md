# Import Handling Protocol

**Document ID**: `PROTO-DEV-023`
**Status**: ACTIVE
**Last Updated**: 2025-11-20
**Type**: Development Protocol

**For AI Agents**: Concise protocol - framework-agnostic import patterns.

---

## 🎯 Purpose

This protocol describes import handling patterns when working with the AgentQMS framework. Use framework-provided path utilities to ensure consistent path resolution across projects.

---

## 🛠️ Framework Path Utilities

**Use framework path utilities** for consistent path resolution:

```python
from AgentQMS.agent_tools.utils.paths import (
    get_framework_root,
    get_project_root,
    get_container_path,
)
from AgentQMS.agent_tools.utils.runtime import ensure_project_root_on_sys_path

# Ensure project root is on sys.path (for framework-aware scripts)
ensure_project_root_on_sys_path()
```

---

## 📋 Import Patterns

### **Framework Imports**

Always use absolute imports for framework components:

```python
# ✅ CORRECT - Framework imports
from AgentQMS.agent_tools.core.artifact_workflow import ArtifactWorkflow
from AgentQMS.agent_tools.compliance.validate_artifacts import ArtifactValidator
from AgentQMS.agent_tools.utils.config import load_config
```

### **Project-Specific Imports**

For project-specific code, use clear import patterns:

```python
# ✅ CORRECT - Project imports (absolute or relative as appropriate)
from project_module import ProjectClass
from .local_module import LocalClass
from ..parent_module import ParentClass
```

### **Never Change Working Imports**

- ✅ If an import works, don't change it
- ✅ Don't convert absolute to relative imports unnecessarily
- ✅ Don't convert relative to absolute imports unnecessarily
- ✅ Test imports in the actual runtime environment

---

## 🔧 Path Resolution

### **Framework Root Detection**

The framework automatically detects its location:

```python
from AgentQMS.agent_tools.utils.paths import get_framework_root

framework_root = get_framework_root()
# Returns: Path to AgentQMS/ directory
```

### **Project Root Detection**

```python
from AgentQMS.agent_tools.utils.paths import get_project_root

project_root = get_project_root()
# Returns: Path to project root (parent of AgentQMS/)
```

### **Component Path Resolution**

Use framework helper to get component paths:

```python
from AgentQMS.agent_tools.utils.paths import get_container_path

config_defaults = get_container_path("config_defaults")
# Returns: Path to AgentQMS/config_defaults/
```

---

## 🚨 Common Pitfalls

### **❌ Don't Manually Manipulate sys.path**

```python
# ❌ WRONG - Don't do this
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# ✅ CORRECT - Use framework utility
from AgentQMS.agent_tools.utils.runtime import ensure_project_root_on_sys_path
ensure_project_root_on_sys_path()
```

### **❌ Don't Use Relative Imports for Framework**

```python
# ❌ WRONG - Framework is in different package
from ...agent_tools.core import artifact_workflow

# ✅ CORRECT - Use absolute import
from AgentQMS.agent_tools.core import artifact_workflow
```

### **❌ Don't Hardcode Paths**

```python
# ❌ WRONG - Hardcoded path
framework_path = "/workspaces/project/AgentQMS"

# ✅ CORRECT - Use framework detection
from AgentQMS.agent_tools.utils.paths import get_framework_root
framework_path = get_framework_root()
```

---

## 🔍 Debugging Import Issues

### **Framework Scripts**

For scripts using the framework:

```python
from AgentQMS.agent_tools.utils.runtime import ensure_project_root_on_sys_path

# This ensures the project root is on sys.path
ensure_project_root_on_sys_path()

# Now you can import project modules
from project_module import ProjectClass
```

### **Import Errors**

If you see import errors:

1. **Check framework installation** - Is `AgentQMS/` in the project?
2. **Use framework path utilities** - Don't manipulate sys.path manually
3. **Verify project structure** - Framework expects containerized layout
4. **Check configuration** - Ensure framework root detection works

---

## 📚 Related

- **Framework Path Utilities**: `AgentQMS/agent_tools/utils/paths.py`
- **Runtime Utilities**: `AgentQMS/agent_tools/utils/runtime.py`
- **Loader Path Resolution**: [Loader Path Resolution Reference](../../03_references/development/loader_path_resolution.md)
- **Configuration System**: `AgentQMS/agent_tools/utils/config.py`

---

## ✅ Best Practices

1. **Use framework path utilities** - Don't manipulate paths manually
2. **Use absolute imports for framework** - `from AgentQMS...`
3. **Use framework detection** - Don't hardcode paths
4. **Test in actual environment** - Don't rely on test scripts alone
5. **Keep imports clear** - Use explicit imports, avoid wildcards

---

*This protocol focuses on **framework-agnostic** import patterns. For project-specific import patterns, see project documentation.*
