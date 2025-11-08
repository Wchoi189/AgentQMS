# Modularity Quick Reference

**Purpose**: Quick reference for maintaining concise, modular code during development.

## **🚨 Immediate Triggers**

**Refactor immediately when:**
- Function name contains "and" (e.g., `load_and_clean_data`)
- File purpose requires "and" to describe (e.g., "loads data and handles UI")
- **3+ similar code blocks** exist
- **Multiple responsibilities** in one file
- Script exceeds **200-300 lines** (warning bell)

## **📏 Size Guidelines**

### **For Functions: The "One Screen" Rule**
- **Guideline:** Aim for **under 20-30 lines**
- **Principle:** **Single Responsibility Principle (SRP)** - One thing, done well
- **Why:** Should fit on one screen without scrolling for easy reading, testing, and debugging
- **Better Litmus Test:** Can you give the function a clear, simple name without "and"s?
  - ❌ **Bad:** `def load_and_clean_data(file):` (doing two things)
  - ✅ **Good:** `def load_data(file):` and `def clean_data(df):`

### **For Scripts/Modules: The "High Cohesion" Rule**
- **Guideline:** Aim for **under 200-300 lines**
- **Principle:** **High Cohesion** - Everything closely related to one central concept
- **Why:** 200-300 lines is a warning bell. If `data_utils.py` is 500 lines, it's probably doing more than just "data utilities"
- **Better Litmus Test:** Can you describe the file's purpose in one short sentence without "and"?
  - ❌ **Bad:** "This file loads data *and* handles the Streamlit UI for the data viewer page"
  - ✅ **Good:** "This file contains all functions for loading and caching data from disk"

### **Principle Over Pylint**
- **Use line counts as signals, not hard failures**
- **40-line function** doing one complex transformation? That's fine.
- **15-line function** doing three different things? Split it.

## **🏗️ Quick Modularization Pattern**

### **Step 1: Identify Responsibilities**
```python
# Before: Monolithic script (150+ lines)
def process_data():
    # Data loading (30 lines)
    # Data cleaning (40 lines)
    # Data transformation (50 lines)
    # Data validation (30 lines)
    # Data saving (20 lines)
```

### **Step 2: Extract Modules**
```python
# After: Modular approach
from modules.data_loader import DataLoader
from modules.data_cleaner import DataCleaner
from modules.data_transformer import DataTransformer
from modules.data_validator import DataValidator
from modules.data_saver import DataSaver

def process_data():
    """Main processing pipeline (20 lines)."""
    data = DataLoader.load()
    cleaned = DataCleaner.clean(data)
    transformed = DataTransformer.transform(cleaned)
    validated = DataValidator.validate(transformed)
    DataSaver.save(validated)
```

## **📁 Directory Structure**

```
project/
├── scripts/           # Main execution (50-100 lines each)
├── modules/           # Reusable components
│   ├── data/         # Data operations
│   ├── processing/   # Business logic
│   └── output/       # Output generation
├── utils/            # Shared utilities
└── config/           # Configuration
```

## **🎯 Naming Conventions**

| Type | Pattern | Example |
|------|---------|---------|
| Scripts | `action_object.py` | `process_data.py` |
| Modules | `noun_verb.py` | `data_loader.py` |
| Utilities | `noun.py` | `error_handler.py` |

## **⚡ Development Workflow**

### **Phase 1: Rapid Prototype (1-2 hours)**
- Write everything in one file
- Keep under 200 lines total
- Focus on proving concept works

### **Phase 2: Immediate Modularization (30-60 min)**
- Extract clear modules
- Each module under 100 lines
- Split by responsibility

### **Phase 3: Iterative Refinement (Ongoing)**
- Optimize and reuse
- Maintain modularity
- Refactor as needed

## **🔍 Common Patterns**

### **Data Processing**
```python
# Extract: data_loader.py, data_cleaner.py, data_transformer.py
def process_data():
    data = DataLoader.load()
    cleaned = DataCleaner.clean(data)
    transformed = DataTransformer.transform(cleaned)
    return transformed
```

### **API Integration**
```python
# Extract: api_client.py, auth_manager.py, response_parser.py
def api_workflow():
    client = APIClient(AuthManager.get_credentials())
    response = client.make_request()
    return ResponseParser.parse(response)
```

### **Analysis Pipeline**
```python
# Extract: results_loader.py, metrics_calculator.py, report_generator.py
def analyze_results():
    results = ResultsLoader.load()
    metrics = MetricsCalculator.calculate(results)
    return ReportGenerator.generate(metrics)
```

## **✅ Quick Checklist**

Before considering any script complete:
- [ ] Function names don't contain "and" (single responsibility)
- [ ] File purpose can be described without "and"
- [ ] Main script under 200-300 lines (warning bell)
- [ ] Each module has high cohesion (closely related concepts)
- [ ] No repeated code patterns
- [ ] Clear separation: data/processing/output
- [ ] Configuration centralized
- [ ] Error handling consistent
- [ ] Module names descriptive
- [ ] Dependencies minimal
- [ ] Code testable

## **🚫 Common Pitfalls**

**❌ Over-modularization:**
- Don't create modules for single-use functions
- Don't split every function into its own file

**❌ Under-modularization:**
- Don't keep everything in one file
- Don't ignore repeated code patterns

**❌ Poor naming:**
- Don't use generic names like `utils.py`
- Don't use unclear abbreviations

---

**Reference**: [Full Proactive Modularity Protocol](../02_protocols/development/22_proactive_modularity_protocol.md)
