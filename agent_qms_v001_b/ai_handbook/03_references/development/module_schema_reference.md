# Module Schema Reference

**Version**: 1.0
**Date**: 2025-10-25
**Status**: ACTIVE
**Category**: Development Reference

---

## 🎯 **Purpose**

This reference defines standardized schemas for common module types in the Korean GEC project. By following these schemas, agents can predict and plan file/folder structures in advance, ensuring consistent organization and reducing refactoring overhead.

## 📁 **Module Type Schemas**

### **1. Data Processing Module**
**Purpose**: Handle data loading, validation, transformation, and persistence.

**Standard Structure**:
```
data_processing/
├── __init__.py
├── loaders/
│   ├── __init__.py
│   ├── csv_loader.py
│   ├── json_loader.py
│   └── api_loader.py
├── validators/
│   ├── __init__.py
│   ├── schema_validator.py
│   └── data_validator.py
├── transformers/
│   ├── __init__.py
│   ├── text_transformer.py
│   ├── feature_extractor.py
│   └── normalizer.py
├── savers/
│   ├── __init__.py
│   ├── csv_saver.py
│   ├── json_saver.py
│   └── database_saver.py
├── utils/
│   ├── __init__.py
│   ├── data_utils.py
│   └── file_utils.py
└── config/
    ├── __init__.py
    └── data_config.py
```

**Key Files**:
- `loaders/csv_loader.py`: CSV file loading functions
- `validators/data_validator.py`: Data integrity checks
- `transformers/text_transformer.py`: Text preprocessing
- `savers/json_saver.py`: Result persistence

### **2. API Service Module**
**Purpose**: Handle external API interactions, authentication, and response processing.

**Standard Structure**:
```
api_service/
├── __init__.py
├── clients/
│   ├── __init__.py
│   ├── upstage_client.py
│   ├── openai_client.py
│   └── anthropic_client.py
├── auth/
│   ├── __init__.py
│   ├── token_manager.py
│   └── credentials.py
├── requests/
│   ├── __init__.py
│   ├── prompt_request.py
│   ├── batch_request.py
│   └── async_request.py
├── responses/
│   ├── __init__.py
│   ├── response_parser.py
│   ├── error_handler.py
│   └── rate_limiter.py
├── utils/
│   ├── __init__.py
│   ├── retry_utils.py
│   └── logging_utils.py
└── config/
    ├── __init__.py
    └── api_config.py
```

**Key Files**:
- `clients/upstage_client.py`: Upstage API client
- `requests/prompt_request.py`: Prompt submission logic
- `responses/response_parser.py`: API response processing
- `auth/token_manager.py`: Authentication handling

### **3. Evaluation Module**
**Purpose**: Metrics calculation, result analysis, and performance reporting.

**Standard Structure**:
```
evaluation/
├── __init__.py
├── metrics/
│   ├── __init__.py
│   ├── accuracy_metrics.py
│   ├── grammatical_metrics.py
│   ├── semantic_metrics.py
│   └── custom_metrics.py
├── analyzers/
│   ├── __init__.py
│   ├── error_analyzer.py
│   ├── pattern_analyzer.py
│   └── trend_analyzer.py
├── reporters/
│   ├── __init__.py
│   ├── console_reporter.py
│   ├── file_reporter.py
│   └── dashboard_reporter.py
├── comparers/
│   ├── __init__.py
│   ├── baseline_comparer.py
│   └── experiment_comparer.py
├── utils/
│   ├── __init__.py
│   ├── stat_utils.py
│   └── visualization_utils.py
└── config/
    ├── __init__.py
    └── eval_config.py
```

**Key Files**:
- `metrics/accuracy_metrics.py`: Accuracy calculations
- `analyzers/error_analyzer.py`: Error pattern analysis
- `reporters/file_reporter.py`: Result file generation
- `comparers/baseline_comparer.py`: Baseline vs experiment comparison

### **4. Streamlit Page Module**
**Purpose**: Individual Streamlit application pages with schema-driven components.

**Standard Structure**:
```
streamlit_page/
├── __init__.py
├── page.py                    # Main page logic
├── components/
│   ├── __init__.py
│   ├── data_display.py
│   ├── input_form.py
│   └── results_view.py
├── services/
│   ├── __init__.py
│   ├── data_service.py
│   ├── api_service.py
│   └── validation_service.py
├── schemas/
│   ├── __init__.py
│   ├── page_schema.yaml
│   └── component_schemas.yaml
├── utils/
│   ├── __init__.py
│   ├── session_utils.py
│   └── ui_utils.py
└── config/
    ├── __init__.py
    └── page_config.py
```

**Key Files**:
- `page.py`: Main Streamlit page function
- `components/data_display.py`: Data visualization components
- `services/api_service.py`: Page-specific API calls
- `schemas/page_schema.yaml`: Page configuration schema

### **5. Core Script Module**
**Purpose**: Main execution scripts that orchestrate the application flow.

**Standard Structure**:
```
core_script/
├── __init__.py
├── main.py                    # Entry point
├── config/
│   ├── __init__.py
│   ├── app_config.py
│   └── logging_config.py
├── runners/
│   ├── __init__.py
│   ├── baseline_runner.py
│   ├── evaluation_runner.py
│   └── experiment_runner.py
├── orchestrators/
│   ├── __init__.py
│   ├── data_orchestrator.py
│   ├── api_orchestrator.py
│   └── result_orchestrator.py
├── utils/
│   ├── __init__.py
│   ├── arg_parser.py
│   └── output_utils.py
└── exceptions/
    ├── __init__.py
    └── custom_exceptions.py
```

**Key Files**:
- `main.py`: Script entry point with CLI
- `runners/baseline_runner.py`: Baseline execution logic
- `orchestrators/api_orchestrator.py`: API call coordination
- `config/app_config.py`: Application configuration

## 🏗️ **Implementation Guidelines**

### **Planning Phase**
1. **Identify Module Type**: Match your feature to one of the schemas above
2. **Predict Structure**: Create the folder structure before writing code
3. **Define Interfaces**: Plan class/function signatures in advance
4. **Estimate Complexity**: Ensure each file stays under 400 lines

### **Development Phase**
1. **Start with Skeletons**: Create empty files with basic imports
2. **Implement Core Logic**: Fill in main functionality
3. **Extract Utilities**: Move shared code to utils/
4. **Add Configuration**: Separate config from logic

### **Refactoring Triggers**
- **File exceeds 400 lines**: Split into submodules
- **Multiple responsibilities**: Extract to separate folders
- **Repeated patterns**: Create utility modules
- **Complex dependencies**: Add orchestration layer

## 📋 **Checklist for New Modules**

- [ ] Module type identified from schemas above
- [ ] Folder structure created in advance
- [ ] `__init__.py` files added to all directories
- [ ] Core interfaces defined before implementation
- [ ] Configuration separated from logic
- [ ] Utility functions extracted
- [ ] Tests planned in corresponding test structure
- [ ] Documentation updated with new module

## 🔗 **Related References**

- [Proactive Modularity Protocol](../02_protocols/development/22_proactive_modularity_protocol.md)
- [Test Organization Guidelines](../02_protocols/testing/test_organization_protocol.md)
- [Import Handling Reference](./import_handling_reference.md)
