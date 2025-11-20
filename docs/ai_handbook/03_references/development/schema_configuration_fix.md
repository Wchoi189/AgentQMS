# Schema Configuration Fix Reference

**Version**: 1.0
**Date**: 2025-10-24
**Status**: ACTIVE
**Category**: Development Reference

---

## 🎯 **Purpose**

Reference for fixing schema configuration errors in Streamlit schema-driven pages.

## 🐛 **Common Schema Errors**

### **Missing Function Errors**
```
Failed to resolve content_source 'get_about_content'
Failed to apply format function 'format_prompt_option'
Failed to resolve options from 'get_sample_indices'
```

### **Missing Session State Errors**
```
Cannot access 'selected_prompt' on SessionStateProxy
Cannot access 'df' on SessionStateProxy
Cannot access 'experiment_result' on SessionStateProxy
```

### **Missing Calculation Errors**
```
Failed to resolve metric value from 'calculate_success_rate'
Failed to resolve metric value from 'count_text_columns'
```

## 🔧 **Function Implementations**

### **Data Source Functions**
```python
def get_available_prompts() -> list[dict[str, Any]]:
    """Get available prompt templates for inference."""
    return [
        {
            "id": "baseline",
            "name": "Competition Baseline",
            "description": "Official competition baseline prompt",
            "category": "competition",
            "complexity": "medium",
            "system_prompt": "당신은 한국어 문장 교정 전문가입니다...",
            "template": "# 지시\\n- 다음 규칙에 따라 원문을 교정하세요...",
            "placeholders": ["text"],
            "estimated_tokens": None,
            "success_rate": None
        }
    ]

def get_available_experiments() -> list[str]:
    """Get list of available experiments for analysis."""
    import os
    from pathlib import Path

    outputs_dir = Path(__file__).parent.parent.parent.parent / "outputs"
    if not outputs_dir.exists():
        return []

    experiments = []
    for file in outputs_dir.glob("*.json"):
        experiments.append(file.stem)

    return experiments

def get_sample_indices() -> list[int]:
    """Get available sample indices from loaded data."""
    if 'df' in st.session_state and st.session_state.df is not None:
        return st.session_state.df.index.tolist()
    return []

def get_error_types() -> list[str]:
    """Get available error types from loaded data."""
    if 'df' in st.session_state and st.session_state.df is not None:
        if 'type' in st.session_state.df.columns:
            return st.session_state.df['type'].unique().tolist()
    return []
```

### **Format Functions**
```python
def format_prompt_option(prompt: dict[str, Any]) -> str:
    """Format prompt option for display in selectbox."""
    return f"{prompt['name']} ({prompt['category']})"

def format_common_patterns(patterns: list[dict[str, Any]]) -> str:
    """Format common error patterns for display."""
    if not patterns:
        return "No patterns found"

    formatted = []
    for pattern in patterns[:5]:  # Show top 5
        formatted.append(f"• {pattern['pattern']} ({pattern['count']} occurrences)")

    return "\\n".join(formatted)

def format_pagination_info(current_page: int, total_pages: int, total_items: int) -> str:
    """Format pagination information for display."""
    return f"Page {current_page} of {total_pages} ({total_items} total items)"

def get_about_content() -> str:
    """Get about content for sidebar."""
    return """
    ## About This App

    This is the Korean Grammar Correction Lab, a comprehensive tool for:
    - Exploring Korean grammar correction datasets
    - Testing different prompt engineering approaches
    - Analyzing correction performance and patterns
    - Comparing experiment results

    Built with Streamlit and powered by advanced NLP models.
    """
```

### **Calculation Functions**
```python
def calculate_success_rate(experiment_data: dict[str, Any]) -> float:
    """Calculate success rate from experiment data."""
    if not experiment_data or 'results' not in experiment_data:
        return 0.0

    results = experiment_data['results']
    if not results:
        return 0.0

    successful = sum(1 for r in results if r.get('success', False))
    return (successful / len(results)) * 100

def count_text_columns(df) -> int:
    """Count text columns in dataframe."""
    if df is None:
        return 0

    text_columns = 0
    for col in df.columns:
        if df[col].dtype == 'object' or 'str' in str(df[col].dtype):
            text_columns += 1

    return text_columns

def count_numeric_columns(df) -> int:
    """Count numeric columns in dataframe."""
    if df is None:
        return 0

    numeric_columns = 0
    for col in df.columns:
        if df[col].dtype in ['int64', 'float64', 'int32', 'float32']:
            numeric_columns += 1

    return numeric_columns

def calculate_missing_percentage(df) -> float:
    """Calculate percentage of missing data in dataframe."""
    if df is None or df.empty:
        return 0.0

    total_cells = df.size
    missing_cells = df.isnull().sum().sum()

    return (missing_cells / total_cells) * 100 if total_cells > 0 else 0.0
```

## 🔄 **Session State Initialization**

```python
def initialize_session_state():
    """Initialize required session state variables."""
    # Data variables
    if 'df' not in st.session_state:
        st.session_state.df = None

    if 'loaded_dataframe' not in st.session_state:
        st.session_state.loaded_dataframe = None

    if 'filtered_dataframe' not in st.session_state:
        st.session_state.filtered_dataframe = None

    if 'analysis_dataframe' not in st.session_state:
        st.session_state.analysis_dataframe = None

    # Selection variables
    if 'selected_prompt' not in st.session_state:
        st.session_state.selected_prompt = None

    if 'selected_sample' not in st.session_state:
        st.session_state.selected_sample = None

    # Experiment variables
    if 'experiment_result' not in st.session_state:
        st.session_state.experiment_result = None

    if 'quality_metrics' not in st.session_state:
        st.session_state.quality_metrics = None
```

## 🔧 **Function Registration**

```python
def register_schema_functions(data_binder: DataBinder):
    """Register all schema functions with data binder."""

    # Data source functions
    data_binder.register_loader("get_available_prompts", get_available_prompts)
    data_binder.register_loader("get_available_experiments", get_available_experiments)
    data_binder.register_loader("get_sample_indices", get_sample_indices)
    data_binder.register_loader("get_error_types", get_error_types)

    # Format functions
    data_binder.register_loader("format_prompt_option", format_prompt_option)
    data_binder.register_loader("format_common_patterns", format_common_patterns)
    data_binder.register_loader("format_pagination_info", format_pagination_info)
    data_binder.register_loader("get_about_content", get_about_content)

    # Calculation functions
    data_binder.register_loader("calculate_success_rate", calculate_success_rate)
    data_binder.register_loader("count_text_columns", count_text_columns)
    data_binder.register_loader("count_numeric_columns", count_numeric_columns)
    data_binder.register_loader("calculate_missing_percentage", calculate_missing_percentage)
```

## 🧪 **Testing Workflow**

### **Step 1: Start Live App**
```bash
streamlit run streamlit_app/main.py --server.port 8503
```

### **Step 2: Test Schema Pages**
1. Navigate to `http://localhost:8503`
2. Click on schema inference page
3. Look for red error boxes
4. Note specific error messages

### **Step 3: Implement Fixes**
1. Implement missing functions
2. Initialize session state
3. Register functions with data binder
4. Test in browser

### **Step 4: Validate**
- [ ] No red error boxes in UI
- [ ] Components render correctly
- [ ] Data displays properly
- [ ] Interactions work as expected

## 📊 **Error Resolution Checklist**

### **Function Errors**
- [ ] Implement missing function
- [ ] Register function with data binder
- [ ] Test function in browser

### **Session State Errors**
- [ ] Initialize missing variable
- [ ] Load data if needed
- [ ] Test variable access

### **Calculation Errors**
- [ ] Implement calculation function
- [ ] Handle edge cases (None, empty data)
- [ ] Test with real data

## 🎯 **Success Criteria**

- [ ] All schema pages load without configuration errors
- [ ] Data source functions return valid data
- [ ] Format functions display data correctly
- [ ] Session state variables are properly initialized
- [ ] Calculation functions work with real data

---

**Related**: [Streamlit Debugging Protocol](../../02_protocols/development/24_streamlit_debugging_protocol.md)
