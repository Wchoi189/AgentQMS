# Path Utils Migration Quickstart

**Version**: 1.0
**Date**: 2025-11-07
**Status**: ACTIVE
**Category**: Development Reference

---

## 🎯 Purpose
- Provide lightning-fast reminders for migrating legacy `sys.path` blocks to `path_utils`
- Highlight the canonical snippets for unit tests, CLI scripts, and ad-hoc harnesses

## ✅ Mandatory Pattern (Most Files)
```python
from streamlit_app.utils.path_utils import setup_project_paths

setup_project_paths()
```

## ⚠️ Streamlit Pages Pattern (Special Case)
Streamlit pages need minimal bootstrap because `streamlit_app` isn't on the path yet:
```python
# Minimal path setup to import path_utils (Streamlit pages need this)
import sys
from pathlib import Path

_minimal_path = Path(__file__).parent.parent.parent
if str(_minimal_path) not in sys.path:
    sys.path.insert(0, str(_minimal_path))

# Now use path_utils for full setup
from streamlit_app.utils.path_utils import setup_project_paths

setup_project_paths()
```

## 🛠️ Standalone Scripts & CLI Tools
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

## 🧪 Pytest Harnesses
```python
import importlib.util
import sys
import types
from pathlib import Path


def _load_path_utils():
    repo_root = next(
        directory
        for directory in (Path(__file__).resolve().parent,) + tuple(Path(__file__).resolve().parents)
        if (directory / "pyproject.toml").exists()
    )
    module_path = repo_root / "streamlit_app" / "utils" / "path_utils.py"
    spec = importlib.util.spec_from_file_location("streamlit_app.utils.path_utils", module_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules.setdefault("streamlit_app", types.ModuleType("streamlit_app"))
    sys.modules.setdefault("streamlit_app.utils", types.ModuleType("streamlit_app.utils"))
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


_PATH_UTILS = _load_path_utils()
setup_project_paths = _PATH_UTILS.setup_project_paths

setup_project_paths()
```

## 📝 Checklist
- [x] `setup_project_paths()` invoked exactly once per module
- [x] No residual `sys.path.insert` or `append`
- [x] Tests/scripts call bootstrap helper before importing project modules
- [ ] Full pytest run (requires environment dependencies installed)
- [ ] Browser smoke-test for Streamlit pages (post-migration)

## 🚨 Troubleshooting
- **`ModuleNotFoundError: streamlit_app`** → Verify bootstrap snippet runs before imports
- **`pandas` missing during tests** → Install dev dependencies or skip dataset-heavy suites
- **Circular import** → Use minimal bootstrap (see Edge Cases section below)

## ⚠️ Edge Cases & Circularity Protection

### When to Use Minimal Bootstrap

**Rare Case**: If `path_utils` import fails without basic path setup (e.g., in deeply nested scripts or unusual execution contexts), use minimal bootstrap:

```python
# Only needed if path_utils import fails without basic path setup
import sys
from pathlib import Path

# Minimal path setup to import path_utils
_minimal_path = Path(__file__).parent.parent.parent
if str(_minimal_path) not in sys.path:
    sys.path.insert(0, str(_minimal_path))

# Now use path_utils for full setup
from streamlit_app.utils.path_utils import setup_project_paths
setup_project_paths()
```

**When This Is Needed:**
- Scripts executed from non-standard locations (e.g., via `python -m` from wrong directory)
- Deeply nested module structures where `path_utils` itself can't be found
- Custom execution environments that don't follow standard Python path resolution

**When This Is NOT Needed:**
- Regular scripts in `scripts/` directory (use bootstrap helper)
- Test files (use pytest harness pattern)
- Any file where `streamlit_app.utils.path_utils` can be imported normally

**Note**: Streamlit pages (`streamlit_app/pages/*.py` and `streamlit_app/main.py`) **DO need** minimal bootstrap because `streamlit_app` isn't on the path when the page is first loaded. Use the Streamlit Pages Pattern shown above.

### Idempotent Behavior

`setup_project_paths()` is **idempotent** - safe to call multiple times:

```python
# This is safe - won't duplicate paths
from streamlit_app.utils.path_utils import setup_project_paths
setup_project_paths()
setup_project_paths()  # No-op, safe
setup_project_paths()  # No-op, safe
```

### Environment Variable Override

Project root can be overridden via `PROJECT_ROOT` environment variable:

```bash
# Override project root for testing or special execution contexts
export PROJECT_ROOT=/custom/path/to/project
python your_script.py
```

### Multiple Execution Contexts

**Streamlit Pages**: Use mandatory pattern (already in `streamlit_app/` package context)

**Standalone Scripts**: Use bootstrap helper (loads `scripts/_bootstrap.py`)

**Test Files**: Use pytest harness pattern (loads `path_utils` directly)

**CLI Tools**: Use bootstrap helper or mandatory pattern depending on location

### Common Pitfalls

1. **Forgetting to call `setup_project_paths()`**: Always call it before importing project modules
2. **Calling after imports**: Must be called **before** any project imports
3. **Mixing patterns**: Don't combine manual `sys.path` manipulation with `path_utils`
4. **Circular imports**: If you encounter circular import issues, use minimal bootstrap pattern

### Verification Checklist

After migration, verify:
- [ ] No `sys.path.insert` or `sys.path.append` calls remain
- [ ] `setup_project_paths()` called exactly once per module
- [ ] Called **before** any project imports
- [ ] All imports work correctly
- [ ] Tests pass with new path setup

### Linting & Enforcement

**Pre-commit Hook**: A pre-commit hook automatically checks for manual `sys.path` usage:
```bash
# Install pre-commit hooks (if not already installed)
pre-commit install

# Run manually (using uv)
uv run pre-commit run check-sys-path-usage --all-files

# Or run all hooks
uv run pre-commit run --all-files
```

**Manual Check**: Run the linting script directly:
```bash
# Using uv (recommended)
uv run python scripts/maintenance/check_sys_path_usage.py

# Or directly
python scripts/maintenance/check_sys_path_usage.py
```

**CI/CD Integration**: The pre-commit hook runs automatically on commit. For CI/CD, add:
```yaml
- name: Check sys.path usage
  run: uv run python scripts/maintenance/check_sys_path_usage.py
```

---

**See also:** `docs/ai_handbook/03_references/development/import_handling_reference.md`
