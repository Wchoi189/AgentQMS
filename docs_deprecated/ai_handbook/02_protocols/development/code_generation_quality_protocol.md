# Code Generation Quality Protocol

**Document ID**: `PROTO-DEV-025`
**Status**: ACTIVE
**Created**: 2025-10-25
**Last Updated**: 2025-10-25
**Type**: Development Protocol

## Critical Rules

1. **Imports**: Always use absolute imports from project root
   ```python
   # ✅ Correct
   from streamlit_app.models import PromptInfo
   from streamlit_app.utils.api_client import APIClient

   # ❌ Wrong
   from ..models import PromptInfo
   from .api_client import APIClient
   ```

2. **Type Annotations**: Add `# type: ignore[no-any-return]` for dynamic imports
   ```python
   # When delegating to dynamically loaded modules
   return self.prompt_manager.get_available_prompts()  # type: ignore[no-any-return]
   ```

3. **Method Calls**: Convert objects to expected types
   ```python
   # Convert ExperimentResult to dict for analysis methods
   result_dict = {
       "results": getattr(result, "results", []),
       "metadata": getattr(result, "metadata", {}),
   }
   analysis_service.analyze_experiment_performance(result_dict)
   ```

4. **Variable Names**: Use exact parameter names from method signatures
   ```python
   # Check method signature first, use exact parameter names
   export_analysis(data, output_path, export_format="json")  # not "format"
   ```

### 🔧 Pre-Generation Checklist

- [ ] Check existing similar files for import patterns
- [ ] Verify method signatures before calling
- [ ] Use absolute imports only
- [ ] Add type ignores for dynamic modules
- [ ] Convert objects to expected types

### 📋 Implementation Plan Template

```markdown
# Implementation Plan: [Feature Name]

## Files to Create/Modify
- `streamlit_app/services/[service].py` - [Description]
- `streamlit_app/models/[model].py` - [Description]

## Import Strategy
- Use absolute imports: `from streamlit_app.models import ModelName`
- Check existing files for patterns

## Type Safety
- Add return type annotations
- Use `# type: ignore[no-any-return]` for dynamic imports
- Convert objects to expected types for method calls

## Testing
- [ ] `make lint` passes
- [ ] All imports resolve
- [ ] Method signatures match
```

---

*For comprehensive guidelines, see: [Full Protocol](link-to-comprehensive-version)*
