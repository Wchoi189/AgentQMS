# Project Overview

**Document ID**: `ONBOARD-001`
**Status**: ACTIVE
**Created**: 2025-10-27
**Last Updated**: 2025-10-27
**Type**: Onboarding Guide

---

## Project Purpose

The Korean Grammar Correction project is a "Prompt-a-thon" focused on developing optimal prompts for Korean grammar error correction using the Solar Pro API. The goal is to create a system that can take sentences with grammar errors as input and output grammatically correct sentences through prompt engineering alone, without any model fine-tuning.

## Core Objectives

### **Primary Goal**
Develop and optimize prompts that achieve high accuracy in Korean grammar correction using the Solar Pro API.

### **Secondary Goals**
- Create an interactive Streamlit application for testing and analysis
- Build a comprehensive evaluation framework
- Develop reusable prompt templates and utilities
- Document best practices for Korean grammar correction

## Project Scope

### **In Scope**
- Prompt engineering for Korean grammar correction
- Interactive web interface development
- Data processing and evaluation pipelines
- Performance analysis and optimization
- Documentation and knowledge sharing

### **Out of Scope**
- Model fine-tuning or training
- Multi-language support (Korean only)
- Real-time production deployment
- Advanced NLP research beyond prompt engineering

## Key Components

### **1. Grammar Correction Engine**
- **Location**: `prompts.py`, `grammar_correction_utils.py`
- **Purpose**: Core prompt templates and utility functions
- **Status**: Active development

### **2. Streamlit Application**
- **Location**: `streamlit_app/` directory
- **Purpose**: Interactive interface for testing and analysis
- **Data Validation**: Pydantic V2 models in `streamlit_app/models/`
- **Status**: Active development (see [plan-2-streamlit-app.md](../../artifacts/completed_plans/implementation_plans/plan-2-streamlit-app.md))

### **3. Evaluation Framework**
- **Location**: `evaluate.py`, `metrics.py`
- **Purpose**: Performance measurement and comparison
- **Status**: Active development

### **4. Data Pipeline**
- **Location**: `data/` directory
- **Purpose**: Training and test data management
- **Status**: Active

## Technology Stack

### **Core Technologies**
- **Python 3.x**: Primary development language
- **Solar Pro API**: LLM for grammar correction
- **Streamlit**: Web application framework
- **Pydantic V2**: Type-safe data validation and serialization
- **Pandas**: Data processing and analysis
- **Pytest**: Testing framework

### **Development Tools**
- **UV**: Package management
- **Git**: Version control
- **Markdown**: Documentation
- **YAML**: Configuration management

## Project Structure

```
upstage-prompt-a-thon-project/
├── docs/                              # Documentation
│   ├── ai_handbook/                   # AI agent handbook
│   ├── artifacts/                     # Generated artifacts
│   └── [other docs]
├── data/                              # Training and test data
├── prompts.py                         # Core prompt templates
├── grammar_correction_utils.py        # Utility functions
├── evaluate.py                        # Evaluation scripts
├── metrics.py                         # Performance metrics
├── plan-1-implementation.md          # Implementation strategy
├── plan-2-streamlit-app.md           # Streamlit app design
├── README.md                          # Project overview
└── CLAUDE.md                          # Code protocol
```

## Success Metrics

### **Primary Metrics**
- **Accuracy**: Percentage of correctly corrected sentences
- **Precision**: Correct corrections / Total corrections
- **Recall**: Correct corrections / Total errors in input

### **Secondary Metrics**
- **Response Time**: API call latency
- **Cost Efficiency**: API usage optimization
- **User Experience**: Streamlit app usability

## Current Status

### **Completed**
- Basic project structure
- Initial prompt templates
- Evaluation framework foundation
- Documentation system

### **In Progress**
- Prompt optimization
- Streamlit app design
- Data processing pipeline
- Performance analysis

### **Planned**
- Streamlit app implementation
- Advanced evaluation metrics
- User interface optimization
- Documentation completion

## Key Documents

### **Implementation Plans**
- [Streamlit App Strategic Plan](../../artifacts/implementation_plans/2025-01-27_IMPLEMENTATION_PLAN_STREAMLIT_APP_V1.md)
- [Original Implementation Plan](../../../PLAN_1_IMPLEMENTATION.md)

### **Design Documents**
- [Streamlit App Design](../../artifacts/completed_plans/implementation_plans/plan-2-streamlit-app.md)
- [Project Architecture](../03_references/architecture/01_project_architecture.md)

### **Protocols**
- [Artifact Management Protocol](../02_protocols/governance/01_artifact_management_protocol.md)
- [Coding Standards](../02_protocols/development/01_coding_standards_v2.md)

## Getting Started

### **For New Contributors**
1. Read this overview
2. Review [Environment Setup](02_environment_setup.md)
3. Check [Data Overview](03_data_overview.md)
4. Follow [Coding Standards](../02_protocols/development/01_coding_standards_v2.md)

### **For AI Agents**
1. Understand project goals and scope
2. Review [Artifact Management Protocol](../02_protocols/governance/01_artifact_management_protocol.md)
3. Check existing [artifacts](../../artifacts/) before creating new ones
4. Follow established protocols and standards

## Related Documents

- [Environment Setup](02_environment_setup.md)
- [Data Overview](03_data_overview.md)
- [Project Architecture](../03_references/architecture/01_project_architecture.md)
- [Implementation Plan](../../artifacts/completed_plans/implementation_plans/plan-1-implementation.md)
- [Streamlit App Design](../../artifacts/completed_plans/implementation_plans/plan-2-streamlit-app.md)
