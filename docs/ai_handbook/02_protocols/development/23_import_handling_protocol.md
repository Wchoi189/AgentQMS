# Import Handling Protocol

**Document ID**: `PROTO-DEV-023`
**Status**: ACTIVE
**Created**: 2025-10-25
**Last Updated**: 2025-10-25
**Type**: Development Protocol

**For AI Agents**: Concise protocol - hints only, no tutorials.

## Rules

### Always Use Path Utils (REQUIRED)
- ALWAYS use `setup_project_paths()` from `streamlit_app.utils.path_utils`
- NEVER manually manipulate `sys.path`
- This ensures consistency, error handling, and environment variable support

```python
# ✅ CORRECT
from streamlit_app.utils.path_utils import setup_project_paths
setup_project_paths()
from visualizations import ComparativeAnalysisVisualizer

# ❌ WRONG (deprecated)
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
```

### Never Change Working Imports
- If import works, don't change it
- Don't convert absolute to relative imports
- Test in live browser app, not terminal

### Component Imports
```python
# Same package: from .component import Component
# Parent package: from ..component import Component
```

### Service Imports
```python
from streamlit_app.services.data_service import DataService
from streamlit_app.utils.data_loader import DataLoader
```

## Debugging
- Start live app: `streamlit run streamlit_app/main.py --server.port 8503`
- Test in browser at `http://localhost:8503`
- Never rely on test scripts for import validation

## Loader Registry Path Resolution

For loader registry import path issues:
- See [Loader Path Resolution Reference](../../03_references/development/loader_path_resolution.md)
- Uses `LOADER_BASE_PATH` environment variable for flexible path resolution
- Multiple import strategies with fallback logic
- Requires `setup_project_paths()` to be called first
