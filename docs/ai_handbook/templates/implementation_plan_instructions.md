# Implementation Plan Instructions

## 🚨 Critical Quality Rules

**Before implementing any code, follow these rules to prevent 80% of linting errors:**

### 1. Import Management
- **ALWAYS** use absolute imports from project root
- **NEVER** use relative imports (`..` or `.`)
- **CHECK** existing files for import patterns before coding

```python
# ✅ Correct
from streamlit_app.models import PromptInfo
from streamlit_app.utils.api_client import APIClient

# ❌ Wrong - Will cause import-not-found errors
from ..models import PromptInfo
from .api_client import APIClient
```

### 2. Type Safety for Dynamic Imports
- **ADD** `# type: ignore[no-any-return]` when delegating to dynamically loaded modules
- **CONVERT** objects to expected types before method calls

```python
# For dynamic module delegation
return self.prompt_manager.get_available_prompts()  # type: ignore[no-any-return]

# For method calls expecting specific types
result_dict = {"results": getattr(result, "results", [])}
analysis_service.analyze_experiment_performance(result_dict)
```

### 3. Method Signature Compliance
- **VERIFY** exact parameter names from method signatures
- **CHECK** expected argument types before calling methods
- **CONVERT** objects to match expected types

### 4. Variable Naming
- **USE** exact parameter names from method signatures
- **AVOID** generic names like `format` when method expects `export_format`

## Pre-Implementation Checklist

- [ ] Reviewed existing similar files for patterns
- [ ] Verified all import paths use absolute imports
- [ ] Checked method signatures for correct parameter names/types
- [ ] Planned type conversions for method calls
- [ ] Added type ignores for dynamic imports

## Post-Implementation Verification

- [ ] `make lint` passes without errors
- [ ] All imports resolve correctly
- [ ] Method calls use correct signatures
- [ ] Type annotations are complete

---

**Reference**: [Code Generation Quality Protocol](../02_protocols/development/code_generation_quality_protocol.md)
