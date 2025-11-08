# Architecture Summary for AI Agents

**Purpose**: High-level system understanding without deep code diving

## 🏗️ **System Overview**

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Streamlit UI  │    │   Service Layer  │    │   Data Layer    │
│                 │    │                  │    │                 │
│ • Data Explorer │◄──►│ • Data Service   │◄──►│ • CSV Files     │
│ • Inference     │    │ • Inference Svc  │    │ • Cache System  │
│ • Analysis      │    │ • Analysis Svc   │    │ • Config Files  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌──────────────────┐
                    │   External APIs  │
                    │                  │
                    │ • Upstage Solar  │
                    │ • Seroost Search │
                    └──────────────────┘
```

## 🔄 **Data Flow**

1. **User Input** → Streamlit UI
2. **UI** → Service Layer (business logic)
3. **Service** → Data Layer (loading/caching)
4. **Service** → External APIs (inference)
5. **Response** → UI (display results)

## 🧩 **Key Components**

### **Inference Service** (Most Complex)
- **Purpose**: Orchestrates all inference operations
- **Key Files**:
  - `service.py` - Main coordinator
  - `model_manager.py` - Model configuration
  - `prompt_formatter.py` - Template processing
  - `api_client_manager.py` - API lifecycle
- **Pattern**: Composition over inheritance

### **Data Service**
- **Purpose**: Centralized data management
- **Features**: Caching, validation, loading
- **Key Files**: `data_service.py`, `data_loader.py`

### **Analysis Service**
- **Purpose**: Metrics calculation and evaluation
- **Key Files**: `analysis_service.py`, `metrics.py`

## 🔧 **Configuration System**
- **Environment**: `.env.local` → `.streamlit/secrets.toml`
- **App Config**: `streamlit_app/config/*.yaml`
- **Models**: Pydantic V2 models in `streamlit_app/models/`

## 🚀 **Performance Considerations**
- **Caching**: Aggressive caching in data service
- **Async**: API calls are async where possible
- **Memory**: Large datasets loaded on-demand
- **UI**: Pagination for large tables

## 🔍 **Debugging Points**
- **API Issues**: Check `api_client_manager.py`
- **Data Issues**: Check `data_service.py`
- **UI Issues**: Check individual page files
- **Config Issues**: Check `config.py` and YAML files
