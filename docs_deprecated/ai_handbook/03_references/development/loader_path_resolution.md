---
title: "Loader Path Resolution - Environment Variables"
date: "2025-11-07 00:00 (KST)"
type: "reference"
category: "development"
status: "active"
version: "1.0"
tags: ['reference', 'development', 'environment-variables', 'loader-registry', 'path-resolution']
---

# Loader Path Resolution - Environment Variables

**For AI Agents**: Concise reference for loader path resolution using environment variables.

## 🎯 **Purpose**

The loader registry uses environment variables to resolve module import paths flexibly, supporting different execution contexts and deployment scenarios.

## 🔧 **Environment Variable: `LOADER_BASE_PATH`**

### **Description**

`LOADER_BASE_PATH` is an optional environment variable that defines the base module path prefix for loader imports. This allows the loader registry to resolve module paths correctly in different execution contexts.

### **Usage**

Add to `.env.local` in the project root:

```bash
# Loader path resolution
LOADER_BASE_PATH=streamlit_app
```

### **How It Works**

The loader registry tries multiple import strategies in order:

1. **Strategy 1**: Use path as-is from config (e.g., `streamlit_app.schema_engine.utils.data_loaders`)
2. **Strategy 2**: If `LOADER_BASE_PATH` is set, try with base path prefix
3. **Strategy 3**: Try without first part (e.g., remove `streamlit_app.` prefix)
4. **Strategy 4**: If `LOADER_BASE_PATH` is set, try with base path but without first part

### **Example**

If `config.yaml` has:
```yaml
loader_path: streamlit_app.schema_engine.utils.data_loaders.get_available_prompts
```

And `LOADER_BASE_PATH=streamlit_app` is set, the registry will try:
1. `streamlit_app.schema_engine.utils.data_loaders` (as-is)
2. `streamlit_app.streamlit_app.schema_engine.utils.data_loaders` (with base path)
3. `schema_engine.utils.data_loaders` (without first part)
4. `streamlit_app.schema_engine.utils.data_loaders` (with base path, without first part)

### **When to Use**

- **Default**: Not required if `sys.path` is configured correctly via `setup_project_paths()`
- **Override**: Use when standard path resolution fails in specific execution contexts
- **Debugging**: Use to test different import strategies when troubleshooting loader import errors

### **Dependencies**

⚠️ **CRITICAL**: This solution depends on the **Path Utils Migration** being completed first.

The loader registry requires `sys.path` to be configured correctly via `setup_project_paths()` from `streamlit_app.utils.path_utils`. Without proper `sys.path` setup, even the flexible import strategies won't work.

**Priority Order**:
1. ✅ Complete Path Utils Migration (ensures `sys.path` is configured)
2. ✅ Test loader imports (verify they work with standard paths)
3. ✅ Use `LOADER_BASE_PATH` only if needed (for edge cases or debugging)

## 📝 **Implementation Details**

### **Registry Implementation**

The loader registry automatically:
- Reads `LOADER_BASE_PATH` from environment variables
- Tries multiple import strategies in order
- Logs which strategy succeeded (for debugging)
- Provides clear error messages if all strategies fail

### **Code Location**

- **Registry**: `streamlit_app/schema_engine/core/data_binding/registry.py`
- **Method**: `LoaderRegistry._load_single_loader()`
- **Environment Loader**: `streamlit_app/utils/env_loader.py`

### **Error Messages**

If all import strategies fail, the registry provides detailed error messages:

```
Cannot import module 'streamlit_app.schema_engine.utils.data_loaders' for loader 'get_available_prompts'.
Tried strategies: 'streamlit_app.schema_engine.utils.data_loaders', 'schema_engine.utils.data_loaders'.
Last error: ModuleNotFoundError: No module named 'streamlit_app.schema_engine.utils.data_loaders'.
Set LOADER_BASE_PATH env var to override base path (current: not set)
```

## 🚨 **Troubleshooting**

### **Loader Import Errors**

1. **Check `sys.path` setup**: Ensure `setup_project_paths()` is called before loader registry initialization
2. **Verify environment variable**: Check if `LOADER_BASE_PATH` is set correctly in `.env.local`
3. **Check logs**: Look for "Trying import strategy" messages to see which strategies are being attempted
4. **Test manually**: Try importing the module directly in Python REPL to verify path resolution

### **Common Issues**

- **"Module not found"**: Usually means `sys.path` isn't configured correctly
- **"Attempted relative import beyond top-level package"**: Usually means path prefix is incorrect
- **"All strategies failed"**: Usually means `sys.path` setup is missing or incorrect

## ✅ **Best Practices**

1. **Complete Path Utils Migration First**: Ensure `sys.path` is configured correctly
2. **Use Standard Paths**: Don't set `LOADER_BASE_PATH` unless necessary
3. **Test After Changes**: Verify loader imports work after path configuration changes
4. **Check Logs**: Review loader registry logs to see which import strategies succeeded

## 📚 **Related Documentation**

- **Path Utils Migration**: `docs/artifacts/implementation_plans/2025-11-07_0241_implementation_plan_path-utils-migration-blueprint.md`
- **Import Handling Protocol**: `docs/ai_handbook/02_protocols/development/23_import_handling_protocol.md`
- **Path Utils Reference**: `docs/ai_handbook/03_references/development/utility_functions.md`
- **Error Log Assessment**: `docs/artifacts/assessments/2025-11-07_1603_assessment-error-log-debugging-session-handover.md`

## 🔗 **Related Documentation**

- **Import Handling**: [Import Handling Reference](import_handling_reference.md) - General import patterns
- **Import Protocol**: [Import Handling Protocol](../../02_protocols/development/23_import_handling_protocol.md) - Import handling rules
- **Path Utils**: [Utility Functions](utility_functions.md) - Path utilities reference
- **Path Utils Migration**: [Path Utils Migration Blueprint](../../../../artifacts/implementation_plans/2025-11-07_0241_implementation_plan_path-utils-migration-blueprint.md) - Migration plan
- **Error Assessment**: [Error Log Assessment](../../../../artifacts/assessments/2025-11-07_1603_assessment-error-log-debugging-session-handover.md) - Original error analysis

---

*This reference provides concise hints for AI agents working with loader path resolution. For detailed implementation, see the registry code and path utils migration blueprint.*
