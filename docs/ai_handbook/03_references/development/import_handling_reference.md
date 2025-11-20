# Import Handling Reference

**Version**: 1.0
**Date**: 2025-10-24
**Status**: ACTIVE
**Category**: Development Reference

**For AI Agents**: Concise hints only - no tutorials needed.

---

## 🎯 **Purpose**

Quick reference for import patterns. Minimal examples suffice.

## 🚨 **Critical Rules**

1. **ALWAYS use path_utils** - Never manually manipulate sys.path
2. **NEVER change working imports** - Test in browser first
3. **ALWAYS use browser debugging** - Not test scripts
4. **UNDERSTAND package structure** - Root packages need path setup

## 🔧 **Import Patterns**

### **Root-Level Package Imports (REQUIRED PATTERN)**
```python
# ✅ CORRECT - Use path_utils
from streamlit_app.utils.path_utils import setup_project_paths
setup_project_paths()
from visualizations import ComparativeAnalysisVisualizer

# ❌ WRONG - Manual sys.path manipulation (deprecated)
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
```

### **Component Imports**
```python
# Same package components
from .visualization_utils import VisualizationUtils

# Parent package components
from ..data_tables import DataTableManager
```

### **Service Imports**
```python
# Services and utilities
from streamlit_app.services.data_service import DataService
from streamlit_app.utils.data_loader import DataLoader
```

### **Standalone Scripts / CLI Helpers**
```python
import importlib.util
import sys
from pathlib import Path


def _load_bootstrap():
    current_dir = Path(__file__).resolve().parent
    for directory in (current_dir,) + tuple(current_dir.parents):
        candidate = directory / "_bootstrap.py"
        if candidate.exists():
            spec = importlib.util.spec_from_file_location("scripts._bootstrap", candidate)
            module = importlib.util.module_from_spec(spec)
            sys.modules[spec.name] = module
            spec.loader.exec_module(module)
            return module
    raise RuntimeError("scripts/_bootstrap.py not found")


_BOOTSTRAP = _load_bootstrap()
setup_project_paths = _BOOTSTRAP.setup_project_paths

setup_project_paths()
```

## 📁 **File-Specific Templates**

### **Schema Engine Components**
Files: `streamlit_app/components/visualizations/*_visualization_manager.py`

```python
from __future__ import annotations

from typing import TYPE_CHECKING

import streamlit as st

# Setup project paths using path_utils
from streamlit_app.utils.path_utils import setup_project_paths
setup_project_paths()

# Import root-level packages
from visualizations import SomeVisualizer

# Import same-package components
from .visualization_utils import VisualizationUtils

if TYPE_CHECKING:
    import pandas as pd
```

### **Schema Pages**
Files: `streamlit_app/pages/schema_*.py`

```python
from __future__ import annotations

import streamlit as st

# Setup project paths using path_utils
from streamlit_app.utils.path_utils import setup_project_paths
setup_project_paths()

from streamlit_app.schema_engine.schema_processor import SchemaProcessor
```

### **Imperative Pages**
Files: `streamlit_app/pages/1_📊_Data_Explorer.py`

```python
from __future__ import annotations

import streamlit as st

# Setup project paths using path_utils
from streamlit_app.utils.path_utils import setup_project_paths
setup_project_paths()

from components.enhanced_data_tables import EnhancedDataTableManager
```

## ❌ **Common Mistakes**

### **Mistake 1: Manual sys.path Manipulation (CRITICAL)**
```python
# ❌ WRONG: Manual sys.path manipulation is deprecated
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

# ✅ CORRECT: Always use path_utils
from streamlit_app.utils.path_utils import setup_project_paths
setup_project_paths()
```

### **Mistake 2: Overwriting Working Imports**
```python
# WRONG: Changing working import
from visualizations import X  # WORKS
# Changed to:
from ...visualizations import X  # BREAKS
```

### **Mistake 3: Wrong Path for Root Packages**
```python
# WRONG: visualizations is at root, not in streamlit_app
from streamlit_app.visualizations import X
```

### **Mistake 4: Using Test Scripts**
```bash
# WRONG: Testing in isolation
python -c "from streamlit_app.components.visualizations import something"
```

## ✅ **Quick Fix Commands**

### **Start Live App**
```bash
cd /home/vscode/workspace/upstage-prompt-a-thon-project
streamlit run streamlit_app/main.py --server.port 8503 --server.headless true
```

### **Test in Browser**
Navigate to: `http://localhost:8503`

### **Emergency Import Fix**
```python
# Add to top of file with import errors:
from streamlit_app.utils.path_utils import setup_project_paths
setup_project_paths()
```

## 🎯 **Problem Files**

These files need sys.path modification for `visualizations/` imports:
- `streamlit_app/components/visualizations/comparative_analysis_visualization_manager.py`
- `streamlit_app/components/visualizations/statistical_metrics_visualization_manager.py`
- `streamlit_app/components/visualizations/network_graphs_visualization_manager.py`
- `streamlit_app/components/visualizations/linguistic_features_visualization_manager.py`
- `streamlit_app/components/visualizations/error_patterns_visualization_manager.py`
- `streamlit_app/components/visualizations/text_complexity_visualization_manager.py`

## 🚨 **Warning Signs**

- `ModuleNotFoundError: No module named 'visualizations'`
- `ImportError: attempted relative import beyond top-level package`
- AI agent suggesting to change working imports

## 📊 **Success Criteria**

- All pages load without import errors in browser
- No new errors introduced
- Working imports remain unchanged

## 🔧 **Loader Registry Path Resolution**

For loader registry import path issues, see:
- [Loader Path Resolution](loader_path_resolution.md) - Environment variables for loader registry path resolution

---

**Related**:
- [Import Handling Protocol](../../02_protocols/development/23_import_handling_protocol.md)
- [Loader Path Resolution](loader_path_resolution.md) - Environment variables and import strategies for loader registry
