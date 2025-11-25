# AI Agent Configuration Guidelines

**Date**: 2025-10-25
**Status**: CRITICAL - Must Follow
**Priority**: HIGH - Prevents Multi-Hour Debugging Sessions

## 🚨 **CRITICAL: YAML-ONLY Configuration**

### **❌ NEVER DO THIS:**
- Use hardcoded defaults in Pydantic models
- Use `load_legacy_config()` function
- Modify `models/config.py` for configuration values
- Create new hardcoded configuration dictionaries
- Use `AppConfig()` without loading from YAML

### **✅ ALWAYS DO THIS:**
- Use YAML files in `config/` directory
- Use `load_app_config()` for main configuration
- Use `PydanticConfigLoader` for validation
- Update YAML files for configuration changes
- Load configuration from YAML before using

## 📁 **Configuration Files (SINGLE SOURCE OF TRUTH):**

### **Primary Configuration Files:**
- `config/app_config.yaml` - Main application configuration
- `config/model_config.yaml` - Model and prompt configurations
- `config/ui_config.yaml` - UI theme and layout settings

### **Additional Configuration Files:**
- `config/hybrid_recall_precision.yaml` - Hybrid prompt template
- `config/improved_grammar_correction_prompt.yaml` - Improved prompt template
- `config/recall_focused_grammar_correction.yaml` - Recall-focused prompt template

## 🔧 **Loading Configuration (CORRECT METHODS):**

### **✅ CORRECT - Use YAML Configuration:**
```python
# Method 1: Load main app configuration
from utils.pydantic_config import load_app_config
app_config = load_app_config()

# Method 2: Load specific configuration
from utils.pydantic_config import PydanticConfigLoader
loader = PydanticConfigLoader()
app_config = loader.load_app_config()

# Method 3: Load legacy config (with deprecation warning)
from utils.pydantic_config import load_legacy_config
config_dict = load_legacy_config("model_config")  # Will show deprecation warning
```

### **❌ WRONG - Don't Use Hardcoded Defaults:**
```python
# WRONG - This uses hardcoded defaults that override YAML!
from models.config import AppConfig
app_config = AppConfig()  # This will use hardcoded defaults!

# WRONG - This bypasses YAML configuration
from models.config import UIConfig
ui_config = UIConfig()  # This will use hardcoded defaults!
```

## ⚠️ **If You See Hardcoded Defaults in models/config.py:**

1. **They are SCHEMA-ONLY** for Pydantic validation
2. **They will be removed** in future versions
3. **YAML configuration is the authoritative source**
4. **Changes to hardcoded defaults have NO EFFECT**
5. **Always use YAML configuration instead**

## 🎯 **Configuration Structure:**

### **app_config.yaml Structure:**
```yaml
app:
  name: "Korean Grammar Correction Lab"
  version: "1.0.0"
  description: "Streamlit app for Korean grammar error correction using prompt engineering"

data:
  training_data_path: "${GRAMMAR_CORRECTION_DATA_DIR}/train.csv"
  test_data_path: "${GRAMMAR_CORRECTION_DATA_DIR}/test.csv"
  output_dir: "${GRAMMAR_CORRECTION_OUTPUT_DIR}"
  cache_dir: "${GRAMMAR_CORRECTION_CACHE_DIR}"

api:
  base_url: "https://api.upstage.ai/v1/solar"
  default_model: "solar-pro2"
  timeout: 30
  max_retries: 3
  retry_delay: 1

models:
  solar-pro2:
    name: "Solar Pro 2"
    description: "Latest Solar Pro model - optimized for Korean grammar correction"
    max_tokens: 2048
  # ... more models

ui:
  theme:
    primary_color: "#FF6B6B"
    background_color: "#FFFFFF"
    # ... more theme settings
  layout:
    sidebar_state: "expanded"
    initial_page: "Data Explorer"
  # ... more UI settings

performance:
  max_rows_display: 1000
  pagination_size: 50
  cache_ttl: 3600
```

### **ui_config.yaml Structure:**
```yaml
theme:
  primary_color: "#FF6B6B"
  background_color: "#FFFFFF"
  secondary_background_color: "#F0F2F6"
  text_color: "#262730"
  font: "sans-serif"

layout:
  sidebar_state: "expanded"
  initial_page: "Data Explorer"

display:
  max_text_length: 1000
  show_confidence_scores: true
  show_processing_times: true
  diff_view: true

notifications:
  position: "top-right"
  auto_dismiss: true
  duration: 5000
```

## 🔍 **Common Configuration Patterns:**

### **1. Loading App Configuration:**
```python
# In page files (e.g., pages/3_📈_Analysis.py)
from utils.pydantic_config import load_app_config
app_config = load_app_config()
inference_service = InferenceService(app_config=app_config)
```

### **2. Loading Model Configuration:**
```python
# For model-specific configuration
from utils.pydantic_config import PydanticConfigLoader
loader = PydanticConfigLoader()
model_config = loader.load_model_config()
```

### **3. Loading UI Configuration:**
```python
# For UI-specific configuration
from utils.pydantic_config import PydanticConfigLoader
loader = PydanticConfigLoader()
ui_config = loader.load_ui_config()
```

## 🚨 **Error Handling:**

### **If YAML Configuration is Missing:**
```python
# The system will raise clear error messages:
ValueError: app configuration MUST be defined in app_config.yaml - hardcoded defaults have been removed to prevent confusion
ValueError: models configuration MUST be defined in app_config.yaml - hardcoded defaults have been removed to prevent confusion
```

### **If Using Deprecated Functions:**
```python
# You'll see deprecation warnings:
DeprecationWarning: load_legacy_config() is deprecated. Use YAML configuration with load_app_config() or PydanticConfigLoader instead.
```

## 🎯 **Best Practices:**

1. **Always load from YAML first** before using any configuration
2. **Use environment variables** in YAML for sensitive data
3. **Validate configuration** using Pydantic models
4. **Update YAML files** for configuration changes
5. **Never modify hardcoded defaults** in Python files
6. **Use type hints** for configuration objects
7. **Test configuration loading** in your code

## 🔧 **Environment Variables:**

YAML files support environment variable substitution:
```yaml
data:
  training_data_path: "${GRAMMAR_CORRECTION_DATA_DIR}/train.csv"
  output_dir: "${GRAMMAR_CORRECTION_OUTPUT_DIR}"
```

## 📝 **Configuration Updates:**

### **To Update Configuration:**
1. **Edit YAML files** in `config/` directory
2. **Restart the application** (if needed)
3. **Test the changes** immediately
4. **No cache clearing required**

### **To Add New Configuration:**
1. **Add to YAML file** first
2. **Update Pydantic model** if needed
3. **Add validation** if required
4. **Test loading** the new configuration

## 🎯 **Troubleshooting:**

### **Configuration Not Loading:**
1. Check YAML file exists in `config/` directory
2. Verify YAML syntax is correct
3. Ensure all required fields are present
4. Check environment variables are set

### **Hardcoded Defaults Overriding YAML:**
1. **This should not happen** - hardcoded defaults have been removed
2. If it does happen, check you're using `load_app_config()` not `AppConfig()`
3. Verify YAML file has all required fields
4. Check for validation errors

### **Deprecation Warnings:**
1. Replace `load_legacy_config()` with `load_app_config()`
2. Use `PydanticConfigLoader` for specific configurations
3. Update any code using deprecated functions

## 🎯 **Summary:**

- **YAML is the SINGLE SOURCE OF TRUTH**
- **Hardcoded defaults have been REMOVED**
- **Always use `load_app_config()` or `PydanticConfigLoader`**
- **Never use `AppConfig()` or `UIConfig()` directly**
- **Configuration changes take effect immediately**
- **No cache clearing required**
- **Clear error messages for missing configuration**
