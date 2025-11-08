# Test Organization Protocol

**Version**: 1.0
**Date**: 2025-10-25
**Status**: ACTIVE
**Category**: Testing Protocol

---

## 🎯 **Purpose**

This protocol establishes strict guidelines for test file organization to prevent the common problem of test scripts becoming scattered across the project root and losing maintainability. All tests must follow a structured hierarchy within the `tests/` directory.

## 🚨 **Critical Rules**

### **❌ Never Place Tests In:**
- Project root directory (`/`)
- `scripts/` folder
- `src/` or module folders (except for specific integration tests)
- Any location outside `tests/`

### **✅ Always Place Tests In:**
- `tests/unit/` - Unit tests for individual functions/classes
- `tests/integration/` - Integration tests across modules
- `tests/components/` - Component-specific tests (e.g., Streamlit components)
- `tests/data/` - Data processing and validation tests
- `tests/schema_engine/` - Schema engine tests
- `tests/manual/` - Manual/ exploratory tests (can be temporary)

## 📁 **Test Directory Structure**

```
tests/
├── __init__.py
├── conftest.py                 # Shared pytest fixtures
├── test_utils.py              # Test utility functions
├── unit/                      # Unit tests
│   ├── __init__.py
│   ├── test_data_loaders.py
│   ├── test_api_clients.py
│   ├── test_metrics.py
│   └── test_validators.py
├── integration/               # Integration tests
│   ├── __init__.py
│   ├── test_full_pipeline.py
│   ├── test_api_integration.py
│   └── test_data_flow.py
├── components/                # Component tests
│   ├── __init__.py
│   ├── test_streamlit_components.py
│   └── test_ui_elements.py
├── data/                      # Data tests
│   ├── __init__.py
│   ├── test_data_validation.py
│   └── test_sample_data.py
├── schema_engine/             # Schema tests
│   ├── __init__.py
│   ├── test_schema_validation.py
│   └── test_page_schemas.py
├── manual/                    # Manual tests
│   ├── __init__.py
│   ├── test_debug_session.py
│   └── test_exploratory.py
└── debug/                     # Debug helpers
    ├── __init__.py
    └── debug_utils.py
```

## 🏷️ **Test Naming Conventions**

### **File Naming**
- **Unit tests**: `test_<module_name>.py`
- **Integration tests**: `test_<feature>_integration.py`
- **Component tests**: `test_<component_name>.py`
- **Data tests**: `test_<data_type>_validation.py`

### **Function Naming**
- **Unit tests**: `test_<function_name>_<scenario>`
- **Integration tests**: `test_<feature>_<outcome>`
- **Fixtures**: Use descriptive names in `conftest.py`

### **Examples**
```python
# tests/unit/test_data_loaders.py
def test_load_csv_file_success():
def test_load_csv_file_invalid_path():

# tests/integration/test_api_integration.py
def test_full_prompt_submission_flow():
def test_error_handling_with_invalid_api_key():

# tests/components/test_streamlit_components.py
def test_data_display_component_renders():
def test_input_form_validation():
```

## 🔧 **Test Organization Workflow**

### **When Creating New Tests**

1. **Identify Test Type**:
   - Unit: Single function/class testing
   - Integration: Multi-module interaction
   - Component: UI/component behavior
   - Data: Data validation and processing

2. **Choose Correct Directory**:
   - Unit → `tests/unit/`
   - Integration → `tests/integration/`
   - Component → `tests/components/`
   - Data → `tests/data/`

3. **Create or Update File**:
   - Check if file already exists
   - Add to existing file if appropriate
   - Create new file following naming convention

4. **Add Proper Imports**:
   - Import from correct module paths
   - Use relative imports where appropriate
   - Include necessary fixtures

### **Refactoring Existing Tests**

1. **Audit Current Tests**:
   - Find all test files in root and subdirectories
   - Identify misplaced tests

2. **Move to Correct Location**:
   - Move files to appropriate `tests/` subdirectories
   - Update import paths if necessary
   - Update any hardcoded paths

3. **Update References**:
   - Update CI/CD configurations
   - Update documentation references
   - Update any scripts that reference old paths

## 📋 **Checklist for Test Creation**

- [ ] Test type identified (unit/integration/component/data)
- [ ] Correct directory chosen within `tests/`
- [ ] File named according to convention
- [ ] Proper imports and fixtures used
- [ ] Test follows AAA pattern (Arrange-Act-Assert)
- [ ] Test is isolated and doesn't depend on external state
- [ ] Test added to appropriate `__init__.py` if needed

## 🚫 **Common Violations to Avoid**

### **❌ Root Directory Tests**
```bash
# BAD - Don't do this
/project/
├── test_api_client.py
├── test_data_loader.py
└── test_metrics.py
```

### **✅ Proper Organization**
```bash
# GOOD - Do this
/project/
└── tests/
    ├── unit/
    │   ├── test_api_client.py
    │   └── test_data_loader.py
    └── unit/
        └── test_metrics.py
```

### **❌ Mixed Responsibilities**
```python
# BAD - Single file testing multiple concerns
# tests/test_everything.py
def test_load_data():
def test_process_data():
def test_display_data():
def test_api_call():
```

### **✅ Separated Concerns**
```python
# GOOD - Separate files for different concerns
# tests/unit/test_data_loader.py
def test_load_data():

# tests/unit/test_data_processor.py
def test_process_data():

# tests/components/test_data_display.py
def test_display_data():

# tests/integration/test_api_flow.py
def test_api_call():
```

## 🔗 **Related References**

- [Proactive Modularity Protocol](../development/22_proactive_modularity_protocol.md)
- [Module Schema Reference](../../03_references/development/module_schema_reference.md)
- [pytest.ini](../../../pytest.ini) - Test configuration
