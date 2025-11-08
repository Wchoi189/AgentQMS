# **filename: docs/ai_handbook/03_references/development/utility_functions.md**
<!-- ai_cue:priority=high -->
<!-- ai_cue:use_when=utility_adoption,code_reuse,refactoring -->

# **Reference: Utility Functions & Scripts**

**Note for AI Agents**: This reference provides concise hints. No tutorials needed - minimal examples are sufficient.

## **Overview**
Catalog of approved utility functions. Use these for consistency and code reuse.

## **Core Utility Modules**

### **Path Utilities** (`streamlit_app/utils/path_utils.py`)
Centralized path resolution for the Korean Grammar Correction project.

**🚨 MANDATORY**: Always use `setup_project_paths()` instead of manual `sys.path` manipulation.

**Key Functions:**
```python
from streamlit_app.utils.path_utils import setup_project_paths, get_path_resolver

# Setup paths (call at script start)
setup_project_paths()

# Get resolver instance
resolver = get_path_resolver()

# Access common paths
data_dir = resolver.config.data_dir
output_dir = resolver.config.output_dir
experiments_dir = resolver.config.experiments_dir
```

**Available Methods:**
- `get_path_resolver()` - Get global path resolver instance
- `setup_project_paths()` - Initialize project paths and sys.path
- `get_project_root()` - Get project root directory
- `get_data_dir()` - Get data directory (contains train.csv, test.csv)
- `get_config_dir()` - Get config directory (YAML configs)
- `get_output_dir()` - Get output directory
- `get_experiments_dir()` - Get experiments directory
- `get_results_dir()` - Get results directory
- `get_logs_dir()` - Get logs directory

**Usage Pattern (REQUIRED):**
```python
# ✅ CORRECT - At the top of any script/page
from streamlit_app.utils.path_utils import setup_project_paths
setup_project_paths()

# Now you can safely import from any project module
from streamlit_app.services.inference_service import InferenceService
from visualizations import ComparativeAnalysisVisualizer  # Root-level packages
```

**❌ WRONG (Deprecated Pattern):**
```python
# Never do this - use path_utils instead
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
```

## **Scripts**

### **Process Manager** (`scripts/process_manager.py`)
Manages the Korean Grammar Correction Streamlit application processes with proper lifecycle handling.

**Usage:**
```bash
# Start the app
python scripts/process_manager.py start --port 8501

# Stop the app
python scripts/process_manager.py stop --port 8501

# Check status
python scripts/process_manager.py status --port 8501

# View logs
python scripts/process_manager.py logs --port 8501 --lines 100

# Clear logs
python scripts/process_manager.py clear-logs --port 8501
```

**Features:**
- Process lifecycle management (start/stop/status)
- Log file management and viewing
- Port availability checking
- PID file tracking for process monitoring
- Background and foreground execution modes

**Command Line Options:**
- `--port`: Port number (default: 8501)
- `--foreground`: Run in foreground mode
- `--no-logging`: Disable logging to files
- `--restart`: Restart if already running
- `--lines`: Number of log lines to show (default: 50)
- `--follow`: Follow log files in real-time

## **Service Utilities**

### **Inference Service** (`streamlit_app/services/inference_service.py`)
Handles grammar correction inference using Upstage Solar API.

### **Data Service** (`streamlit_app/services/data_service.py`)
Manages data loading and preprocessing for training/test datasets.

### **Analysis Service** (`streamlit_app/services/analysis_service.py`)
Provides analysis and evaluation functionality for experiments.

### **LLM Service** (`streamlit_app/services/llm_service.py`)
Manages interactions with the Upstage Solar API.

## **Validation & Configuration**

### **Pydantic Models** (`streamlit_app/models/`)
Type-safe data validation using Pydantic V2.

**Key Models:**
- `ExperimentMetadata` - Experiment tracking and metadata
- `CorrectionResult` - Grammar correction results
- `DatasetInfo` - Dataset information and statistics

### **Configuration Management** (`streamlit_app/utils/config.py`)
YAML-based configuration loading with validation.

## **Best Practices**

### **Path Resolution**
Always use the path utilities instead of hardcoded paths:
```python
# ✅ Good
from streamlit_app.utils.path_utils import get_path_resolver
data_path = get_path_resolver().get_data_file("train.csv")

# ❌ Bad
data_path = "data/train.csv"  # Not portable
```

### **Process Management**
Use the process manager script for all Streamlit app operations:
```bash
# ✅ Good
python scripts/process_manager.py start

# ❌ Bad
streamlit run streamlit_app/main.py  # No process tracking
```

### **Import Order**
Follow consistent import patterns:
```python
# Standard library
import os
import sys

# Third-party
import pandas as pd
import streamlit as st

# Project utilities (always first)
from streamlit_app.utils.path_utils import setup_project_paths
setup_project_paths()

# Project modules
from streamlit_app.services.inference_service import InferenceService
```

## **Contributing New Utilities**

When adding new utility functions:

1. **Check for existing solutions first** - Avoid duplication
2. **Add to appropriate module** - Extend existing utilities rather than creating new files
3. **Include comprehensive docstrings** - Document parameters, return values, and examples
4. **Add type hints** - Use modern Python typing
5. **Update this reference** - Keep documentation current
6. **Add tests** - Ensure reliability

## **Related Documents**
- [Coding Standards](../02_protocols/development/01_coding_standards_v2.md) - Development best practices
- [Project Architecture](../03_references/architecture/01_architecture.md) - System design
- [AI Agent System](../../../../ai_agent/system.md) - Single source of truth for AI agents
