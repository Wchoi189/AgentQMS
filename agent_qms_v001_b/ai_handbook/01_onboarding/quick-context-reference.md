# Quick Context Reference for AI Agents

**Last Updated**: 2025-01-27
**Purpose**: Single-page context summary for rapid agent onboarding

## 🎯 **Project Essence**
- **Goal**: Korean grammar correction using prompt engineering (no model fine-tuning)
- **API**: Upstage Solar Pro
- **Architecture**: Modular Streamlit app with service layer
- **Data**: 254 training samples, 110 test samples

## 🏗️ **Core Architecture (5 Components)**
1. **Data Layer**: `streamlit_app/services/data_service.py` - Data loading & caching
2. **Inference Layer**: `streamlit_app/services/inference_service/` - API calls & prompt formatting
3. **Analysis Layer**: `streamlit_app/services/analysis_service.py` - Metrics & evaluation
4. **UI Layer**: `streamlit_app/pages/` - 3 main pages (Data, Inference, Analysis)
5. **Utils Layer**: `streamlit_app/utils/` - Shared utilities

## 📁 **Critical Files (Read in Order)**
1. `streamlit_app/main.py` - App entry point
2. `streamlit_app/services/inference_service/service.py` - Main orchestration
3. `streamlit_app/models/` - Pydantic models
4. `prompts.py` - Core prompt templates
5. `metrics.py` - Evaluation metrics

## 🔧 **Current Status**
- **Phase**: Streamlit app development (Phase 1 complete)
- **Active**: Visualization module implementation
- **Next**: Performance optimization and testing

## ⚡ **Quick Commands**
```bash
# Run app
cd streamlit_app && streamlit run main.py

# Run linting
make lint

# Run tests
pytest
```

## 🚫 **Common Mistakes to Avoid**
- Don't create files in project root
- Don't duplicate existing documentation
- Don't modify core prompt templates without testing
- Don't ignore the service layer architecture

## 📞 **When Stuck**
1. Check this file first
2. Read `streamlit_app/README.md`
3. Consult `docs/ai_agent/system.md` (single source of truth)
4. Ask for clarification on architecture decisions
