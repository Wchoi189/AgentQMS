# AI Agent Context Reference

**Version**: 1.0
**Date**: 2025-10-24
**Status**: ACTIVE
**Category**: Development Reference

---

## 🎯 **Purpose**

Essential context for AI agents working on the Korean Grammar Correction Streamlit project.

## 📋 **Project Context**

### **Project Type**
- **Streamlit Application** with complex import structure
- **Dual UI System**: Both imperative Python pages and schema-driven YAML pages
- **Root-level packages** imported by deeply nested components

### **Key Architecture Points**
- **Import Complexity**: Root-level packages (`visualizations/`) imported by nested components
- **Live Debugging**: Browser-based debugging is essential (not terminal-based)
- **Test Isolation**: Test scripts run in isolation, separate from live app
- **Schema System**: YAML-driven UI with complex configuration requirements

## 🚨 **Critical Import Issue**

```python
# This project has root-level packages (like visualizations/) that are imported
# by components in streamlit_app/components/visualizations/
# AI agents frequently break these imports by changing them to relative imports

# CORRECT (working):
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from visualizations import ComparativeAnalysisVisualizer

# WRONG (breaks):
from ...visualizations import ComparativeAnalysisVisualizer
```

## 🐛 **Debugging Method**

- **MUST use browser debugging** - Terminal/test scripts don't show real errors
- **Start app**: `streamlit run streamlit_app/main.py --server.port 8503`
- **Test in browser**: Navigate to `http://localhost:8503`
- **Fix imports**: Use sys.path modification for root-level packages

## ❌ **Common AI Mistakes**

1. **Overwriting working imports** - AI changes working imports to broken ones
2. **Using test scripts** - Test scripts run in isolation, don't reflect live app
3. **Not understanding package structure** - Root packages need special handling
4. **Changing working code** - If imports work, don't change them

## 📁 **Files That Need Special Import Handling**

- `streamlit_app/components/visualizations/*_visualization_manager.py`
- Any file importing from root-level `visualizations/` package

## 🔧 **Quick Fix Template**

```python
# Add to top of files with import errors:
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
```

## 🧪 **Testing Strategy**

1. Start live Streamlit app
2. Navigate to all pages in browser
3. Note any import errors
4. Fix using template above
5. Test immediately in browser
6. Don't change working imports

## 🚨 **Warning Signs**

- `ModuleNotFoundError: No module named 'visualizations'`
- `ImportError: attempted relative import beyond top-level package`
- AI agent suggesting to change working imports

## ✅ **Success Criteria**

- All pages load without import errors in browser
- No new errors introduced
- Working imports remain unchanged

## 📊 **Schema Configuration Context**

### **Schema Pages**
- `schema_inference` - Inference page with prompt selection
- `schema_analysis` - Analysis page with experiment results
- `schema_advanced_analysis` - Advanced analysis with visualizations

### **Common Schema Errors**
- Missing functions: `get_about_content`, `format_prompt_option`
- Missing session state: `selected_prompt`, `df`, `experiment_result`
- Missing calculations: `calculate_success_rate`, `count_text_columns`

### **Schema Fix Strategy**
1. Implement missing functions
2. Initialize session state variables
3. Register functions with data binder
4. Test in live browser app

## 🎯 **Development Workflow**

### **Before Starting Work**
- [ ] Start live Streamlit app
- [ ] Navigate to all pages and document current errors
- [ ] Understand which imports are working vs broken
- [ ] Read this context completely

### **During Development**
- [ ] Test changes in live browser app, not test scripts
- [ ] Don't change working imports
- [ ] Use correct import patterns for each file type
- [ ] Make minimal changes to fix specific issues

### **After Completing Work**
- [ ] Test all pages in browser
- [ ] Verify no new errors introduced
- [ ] Document what was fixed and why
- [ ] Update this context if new patterns discovered

## 🔄 **Project Structure**

```
upstage-prompt-a-thon-project/
├── streamlit_app/                    # Main Streamlit application
│   ├── pages/                        # Streamlit pages (both imperative and schema-driven)
│   ├── components/                   # Reusable UI components
│   ├── schema_engine/                # Schema-driven UI system
│   ├── services/                     # Business logic services
│   └── utils/                        # Utility functions
├── visualizations/                   # Root-level visualization package
├── data/                            # Dataset files
├── outputs/                         # Experiment results
└── tests/                           # Test suites
```

## 📚 **Related Documentation**

- [Import Handling Protocol](../../02_protocols/development/23_import_handling_protocol.md)
- [Streamlit Debugging Protocol](../../02_protocols/development/24_streamlit_debugging_protocol.md)
- [Import Handling Reference](import_handling_reference.md)
- [Schema Configuration Fix](schema_configuration_fix.md)

## 🚨 **Critical Warnings**

1. **NEVER** change working imports without testing in browser first
2. **ALWAYS** use browser debugging for Streamlit-specific issues
3. **UNDERSTAND** the package structure before making import changes
4. **TEST** in live app after making changes

---

**Key Rule**: If imports work, don't change them. Test in browser, not test scripts.
