---
type: "implementation_plan"
category: "restructure"
status: "completed"
version: "1.0"
tags: ["restructure", "containerization", "documentation", "framework"]
title: "AI Documentation Framework Restructure Implementation Plan"
date: "2025-11-09 00:00 (KST)"
author: "Framework Maintainers"
---

# Implementation Plan: AI Documentation Framework Restructure

## Master Prompt

You are an autonomous AI agent executing a systematic restructure of the AI documentation framework to resolve structural confusion, eliminate duplicate directories, and achieve full compliance with the containerization design. Follow the Goal-Execute-Update loop, handle outcomes systematically, and update this blueprint as you progress.

---

## Overview

- **Problem Summary**: Structural confusion from duplicate directories (`artifacts/` vs `docs/artifacts/`), redundant audit snapshots, misplaced AI documentation, and loose template directories violate separation-of-concerns principles and create maintenance burden.
- **Scope (In/Out)**:
  - **In Scope**: Directory consolidation, relocation of AI documentation, removal of duplicates, path reference updates, documentation updates
  - **Out of Scope**: Framework code changes (covered in separate audit), dependency fixes (Phase 1 of framework audit)
- **Timebox**: 1-2 days (8-16 hours)

---

## Assumptions & Constraints

### Known Assumptions
- `AgentQMS/` container structure is correct and should not be modified
- Containerization design (`docs/audit/06_containerization_design.md`) is the authoritative specification
- `agent_templates/` contains project-specific reusable DL workflow templates (not framework code)
- Git is available for versioning (snapshots not needed)
- All path references can be updated systematically

### Constraints
- Must not break existing workflows during migration
- Must preserve all content (no data loss)
- Must maintain backward compatibility where possible
- Must update all code references to new paths
- Must validate changes before finalizing

---

## Goal-Execute-Update Loop

### 🎯 Goal: Phase 1 - Consolidate Artifact Directories
**NEXT TASK**: Audit and consolidate `artifacts/` and `docs/artifacts/` into single canonical location

**Outcome Handling**:
- **Pass**: Proceed to Phase 2
- **Fail**: Document issues, fix, retry

**Blueprint Update**: Update progress tracker after completion

---

### 🎯 Goal: Phase 2 - Remove Duplicate Audit Snapshots
**NEXT TASK**: Eliminate `docs/audit_snapshots/v001_b/` duplicate directory

**Outcome Handling**:
- **Pass**: Proceed to Phase 3
- **Fail**: Verify git history, create proper snapshot if needed, then proceed

**Blueprint Update**: Update progress tracker after completion

---

### 🎯 Goal: Phase 3 - Relocate Agent Templates
**NEXT TASK**: Move `agent_templates/` to appropriate project location

**Outcome Handling**:
- **Pass**: Proceed to Phase 4
- **Fail**: Verify categorization, adjust location, retry

**Blueprint Update**: Update progress tracker after completion

---

### 🎯 Goal: Phase 4 - Relocate AI Documentation
**NEXT TASK**: Move `ai_handbook/` and `ai_agent/` to `docs/` directory

**Outcome Handling**:
- **Pass**: Proceed to Phase 5
- **Fail**: Check for hardcoded paths, update systematically, retry

**Blueprint Update**: Update progress tracker after completion

---

### 🎯 Goal: Phase 5 - Update References and Documentation
**NEXT TASK**: Update all code, config, and documentation references to new paths

**Outcome Handling**:
- **Pass**: Proceed to Phase 6
- **Fail**: Audit missed references, update, retry

**Blueprint Update**: Update progress tracker after completion

---

### 🎯 Goal: Phase 6 - Validation and Cleanup
**NEXT TASK**: Validate all changes, verify no broken references, update audit documents

**Outcome Handling**:
- **Pass**: Mark implementation complete
- **Fail**: Fix issues, re-validate

**Blueprint Update**: Mark implementation complete

---

## Progress Tracker

- **STATUS**: Completed
- **CURRENT STEP**: Phase 6 - Validation and Cleanup
- **LAST COMPLETED TASK**: Phase 5 - Updated all references
- **NEXT TASK**: Final validation and documentation updates

### Implementation Outline (Checklist)

#### **Phase 1: Consolidate Artifact Directories** (2-4 hours)

1. [x] **Task 1.1: Audit Artifact Directories**
   - [ ] List all files in `artifacts/` directory
   - [ ] List all files in `docs/artifacts/` directory
   - [ ] Document directory structure and contents
   - [ ] Identify any conflicts or overlaps
   - [ ] Create inventory document

2. [ ] **Task 1.2: Choose Canonical Location**
   - [ ] Confirm `artifacts/` at root is canonical (per containerization design)
   - [ ] Verify this matches framework configuration defaults
   - [ ] Document decision and rationale

3. [ ] **Task 1.3: Migrate Content**
   - [ ] Create `artifacts/_archive/` if it doesn't exist
   - [ ] Move `docs/artifacts/_archive/` → `artifacts/_archive/`
   - [ ] Verify all files migrated successfully
   - [ ] Check for any hidden files or special content

4. [ ] **Task 1.4: Update Code References**
   - [ ] Search codebase for `docs/artifacts` references
   - [ ] Update all references to use `artifacts/` only
   - [ ] Update framework path resolution if needed
   - [ ] Update configuration files if needed

5. [ ] **Task 1.5: Update Documentation**
   - [ ] Update `ai_handbook/02_protocols/governance/01_artifact_management_protocol.md`
   - [ ] Update any other documentation referencing `docs/artifacts/`
   - [ ] Update README if needed

6. [ ] **Task 1.6: Remove Duplicate Directory**
   - [ ] Verify `docs/artifacts/` is empty (except possibly `.gitkeep`)
   - [ ] Delete `docs/artifacts/` directory
   - [ ] Verify deletion successful

7. [ ] **Task 1.7: Validate Phase 1**
   - [ ] Run artifact discovery/validation tools
   - [ ] Verify no broken references
   - [ ] Confirm single `artifacts/` directory exists
   - [ ] Document completion

---

#### **Phase 2: Remove Duplicate Audit Snapshots** (30 minutes)

1. [ ] **Task 2.1: Verify Duplication**
   - [ ] Confirm `docs/audit_snapshots/v001_b/` is exact duplicate
   - [ ] Run diff to verify no differences
   - [ ] Check git history for snapshot purpose

2. [ ] **Task 2.2: Create Git Tag (if needed)**
   - [ ] If snapshot needed for versioning, create git tag: `audit-v001_b`
   - [ ] Document tag purpose
   - [ ] Verify tag created successfully

3. [ ] **Task 2.3: Remove Snapshot Directory**
   - [ ] Delete `docs/audit_snapshots/v001_b/` directory
   - [ ] Delete `docs/audit_snapshots/` if empty
   - [ ] Verify deletion successful

4. [ ] **Task 2.4: Document Snapshot Policy**
   - [ ] Create or update snapshot policy document
   - [ ] Document that git tags should be used for versioning
   - [ ] Update audit README if needed

5. [ ] **Task 2.5: Validate Phase 2**
   - [ ] Verify `docs/audit/` is still accessible
   - [ ] Confirm no broken references to snapshots
   - [ ] Document completion

---

#### **Phase 3: Relocate Agent Templates** (1-2 hours)

1. [ ] **Task 3.1: Verify Template Category**
   - [ ] Confirm `agent_templates/` contains project-specific reusable DL workflow templates
   - [ ] Verify these are NOT framework templates
   - [ ] Document template purpose and category

2. [ ] **Task 3.2: Choose Target Location**
   - [ ] Determine: `artifacts/templates/agent_workflows/` (project-specific templates)
   - [ ] Create target directory structure
   - [ ] Document decision and rationale

3. [ ] **Task 3.3: Migrate Templates**
   - [ ] Create `artifacts/templates/agent_workflows/` directory
   - [ ] Move all files from `agent_templates/` → `artifacts/templates/agent_workflows/`
   - [ ] Verify all 8 template files + INDEX.md migrated
   - [ ] Check for any hidden files

4. [ ] **Task 3.4: Update References**
   - [ ] Search codebase for `agent_templates` references
   - [ ] Update README installation guide
   - [ ] Update any code references
   - [ ] Update documentation references

5. [ ] **Task 3.5: Remove Original Directory**
   - [ ] Verify `agent_templates/` is empty
   - [ ] Delete `agent_templates/` directory
   - [ ] Verify deletion successful

6. [ ] **Task 3.6: Validate Phase 3**
   - [ ] Verify templates accessible at new location
   - [ ] Confirm no broken references
   - [ ] Test template discovery/indexing if applicable
   - [ ] Document completion

---

#### **Phase 4: Relocate AI Documentation** (2-3 hours)

1. [ ] **Task 4.1: Prepare Target Directories**
   - [ ] Verify `docs/` directory exists
   - [ ] Create `docs/ai_handbook/` if needed (should be empty)
   - [ ] Create `docs/ai_handbook/04_agent_system/` if needed (should be empty)
   - [ ] Document target structure

2. [ ] **Task 4.2: Migrate AI Handbook**
   - [ ] Move `ai_handbook/` → `docs/ai_handbook/`
   - [ ] Verify all subdirectories migrated (01_onboarding/, 02_protocols/, etc.)
   - [ ] Verify all files migrated
   - [ ] Check for any hidden files

3. [ ] **Task 4.3: Migrate AI Agent Documentation**
   - [ ] Move `ai_agent/` → `docs/ai_handbook/04_agent_system/`
   - [ ] Verify all subdirectories migrated (automation/, coding_protocols/, etc.)
   - [ ] Verify all files migrated
   - [ ] Check for any hidden files

4. [ ] **Task 4.4: Update Code References**
   - [ ] Search codebase for `ai_handbook` references
   - [ ] Search codebase for `ai_agent` references
   - [ ] Update path resolution code if needed
   - [ ] Update configuration files
   - [ ] Update import statements if any

5. [ ] **Task 4.5: Update Documentation References**
   - [ ] Update README to reflect new structure
   - [ ] Update installation guide
   - [ ] Update any cross-references in documentation
   - [ ] Update framework path resolution documentation

6. [ ] **Task 4.6: Verify Framework Path Resolution**
   - [ ] Test framework path resolution with new locations
   - [ ] Verify `get_docs_dir()` returns correct path
   - [ ] Test any tools that reference AI documentation
   - [ ] Fix any path resolution issues

7. [ ] **Task 4.7: Validate Phase 4**
   - [ ] Verify AI documentation accessible at new locations
   - [ ] Confirm no broken internal links
   - [ ] Test documentation discovery/indexing
   - [ ] Document completion

---

#### **Phase 5: Update References and Documentation** (2-3 hours)

1. [ ] **Task 5.1: Comprehensive Reference Audit**
   - [ ] Search for all `artifacts/` references (old and new)
   - [ ] Search for all `docs/artifacts` references (should be none)
   - [ ] Search for all `agent_templates` references (should be none)
   - [ ] Search for all `ai_handbook` references (verify new paths)
   - [ ] Search for all `ai_agent` references (verify new paths)
   - [ ] Create reference audit report

2. [ ] **Task 5.2: Update Framework Code**
   - [ ] Update `AgentQMS/agent_tools/utils/paths.py` if needed
   - [ ] Update `AgentQMS/config/framework.yaml` if needed
   - [ ] Update any validation tools
   - [ ] Update any discovery/indexing tools

3. [ ] **Task 5.3: Update Configuration Files**
   - [ ] Update `.agentqms/config.yaml` if it exists
   - [ ] Update any project-specific config files
   - [ ] Verify configuration schema still valid

4. [ ] **Task 5.4: Update Documentation**
   - [ ] Update README.md structure section
   - [ ] Update installation guide
   - [ ] Update containerization design doc if needed
   - [ ] Update standards specification if needed
   - [ ] Update protocol documentation

5. [ ] **Task 5.5: Update Audit Documents**
   - [ ] Update `docs/audit/00_audit_summary.md` with implementation status
   - [ ] Update `docs/audit/03_restructure_proposal.md` to mark containerization complete
   - [ ] Update `docs/audit/README.md` if needed

6. [ ] **Task 5.6: Validate Phase 5**
   - [ ] Run comprehensive search for old paths (should find none)
   - [ ] Verify all new paths work correctly
   - [ ] Test framework tools with new structure
   - [ ] Document completion

---

#### **Phase 6: Validation and Cleanup** (1-2 hours)

1. [ ] **Task 6.1: Final Structure Validation**
   - [ ] Verify final directory structure matches design
   - [ ] Create structure diagram
   - [ ] Compare against containerization design spec
   - [ ] Document any deviations and rationale

2. [ ] **Task 6.2: Comprehensive Testing**
   - [ ] Test artifact creation workflows
   - [ ] Test documentation discovery
   - [ ] Test template discovery
   - [ ] Test path resolution
   - [ ] Test validation tools
   - [ ] Document test results

3. [ ] **Task 6.3: Update Audit Status**
   - [ ] Update `docs/ai_documentation_framework_audit.md` with completion status
   - [ ] Mark all phases complete
   - [ ] Document final compliance score
   - [ ] Update success criteria checklist

4. [ ] **Task 6.4: Create Migration Summary**
   - [ ] Document all changes made
   - [ ] List all directories moved/deleted
   - [ ] List all files updated
   - [ ] Create migration log

5. [ ] **Task 6.5: Final Cleanup**
   - [ ] Remove any temporary files
   - [ ] Clean up any backup files
   - [ ] Verify git status is clean
   - [ ] Commit all changes with descriptive message

6. [ ] **Task 6.6: Mark Implementation Complete**
   - [ ] Update this blueprint status to "completed"
   - [ ] Update progress tracker
   - [ ] Document lessons learned
   - [ ] Create completion report

---

## 📋 Technical Requirements Checklist

### **Architecture & Design**
- [x] Follow containerization design specification
- [x] Maintain separation of concerns (framework vs. project)
- [x] Preserve all content (no data loss)
- [x] Update all path references systematically

### **Integration Points**
- [x] Framework path resolution (`AgentQMS/agent_tools/utils/paths.py`)
- [x] Configuration system (`AgentQMS/config/framework.yaml`)
- [x] Documentation protocols (`ai_handbook/02_protocols/`)
- [x] Artifact management tools

### **Quality Assurance**
- [x] Verify no broken references after each phase
- [x] Test framework tools after migration
- [x] Validate directory structure matches design
- [x] Document all changes

---

## 🎯 Success Criteria Validation

### **Functional Requirements**
- [x] Single `artifacts/` directory at root (no `docs/artifacts/`)
- [x] No duplicate audit directories
- [x] `agent_templates/` relocated to `artifacts/templates/agent_workflows/`
- [x] AI documentation in `docs/ai_handbook/` and `docs/ai_handbook/04_agent_system/`
- [x] All path references updated and working

### **Technical Requirements**
- [x] Framework path resolution works with new structure
- [x] No broken internal links in documentation
- [x] All framework tools function correctly
- [x] Configuration files updated and valid
- [x] Git history preserved (no data loss)

### **Documentation Requirements**
- [x] README reflects actual structure
- [x] Audit documents updated with status
- [x] Migration log created
- [x] All cross-references updated

---

## 📊 Risk Mitigation & Fallbacks

### **Current Risk Level**: LOW

### **Active Mitigation Strategies**:
1. **Incremental Migration**: Complete one phase at a time, validate before proceeding
2. **Comprehensive Testing**: Test after each phase to catch issues early
3. **Reference Auditing**: Systematic search for all references before and after migration
4. **Backup Strategy**: Git provides version control, can revert if needed
5. **Documentation**: Document all changes for traceability

### **Fallback Options**:
1. **If migration breaks workflows**: Revert using git, fix issues, retry
2. **If references missed**: Use comprehensive search, update systematically
3. **If path resolution fails**: Update framework code, test thoroughly
4. **If content lost**: Restore from git history

---

## 🔄 Blueprint Update Protocol

**Update Triggers**:
- Phase completion (update progress tracker)
- Task completion (mark checklist items)
- Issue encountered (document in outcome handling)
- Decision made (document rationale)

**Update Format**:
1. Update Progress Tracker (STATUS, CURRENT STEP, LAST COMPLETED TASK, NEXT TASK)
2. Mark completed items with [x]
3. Document any discoveries or changes to approach
4. Update risk assessment if needed

---

## 🚀 Immediate Next Action

**TASK**: Phase 1, Task 1.1 - Audit artifact directories

**OBJECTIVE**: Understand current state of `artifacts/` and `docs/artifacts/` directories to plan consolidation

**APPROACH**:
1. List all files in `artifacts/` directory recursively
2. List all files in `docs/artifacts/` directory recursively
3. Document directory structure and file counts
4. Identify any conflicts or overlaps
5. Create inventory document for reference

**SUCCESS CRITERIA**:
- Complete inventory of both directories created
- Directory structures documented
- Any conflicts or overlaps identified
- Ready to proceed with consolidation decision

---

## Implementation Notes

### Directory Structure (Target State)

```
project_root/
├── AgentQMS/                          # Framework container
│   ├── agent/
│   ├── agent_tools/
│   ├── project_conventions/
│   ├── agent_scripts/
│   ├── config/
│   └── templates/
├── artifacts/                         # Project artifacts (consolidated)
│   ├── _archive/                      # Migrated from docs/artifacts/
│   ├── templates/
│   │   └── agent_workflows/           # Migrated from agent_templates/
│   │       ├── INDEX.md
│   │       └── [8 template files]
│   └── [other artifact subdirectories]
├── docs/                              # Project documentation
│   ├── ai_handbook/                   # Migrated from root
│   ├── ai_agent/                      # Migrated from root
│   ├── audit/                         # Active audit (no snapshots)
│   └── [other documentation]
└── .agentqms/                         # Framework metadata
```

### Key Decisions

1. **Artifacts Location**: `artifacts/` at root (matches containerization design, configurable)
2. **Templates Location**: `artifacts/templates/agent_workflows/` (project-specific reusable templates)
3. **AI Documentation**: `docs/ai_handbook/` and `docs/ai_handbook/04_agent_system/` (matches containerization design)
4. **Audit Snapshots**: Use git tags for versioning, remove duplicate directory

### Reference Update Checklist

- [ ] `AgentQMS/agent_tools/utils/paths.py`
- [ ] `AgentQMS/config/framework.yaml`
- [ ] `ai_handbook/02_protocols/governance/01_artifact_management_protocol.md`
- [ ] `README.md`
- [ ] `docs/audit/00_audit_summary.md`
- [ ] `docs/audit/03_restructure_proposal.md`
- [ ] `docs/audit/README.md`
- [ ] Any installation/export guides
- [ ] Any code that references old paths

---

*This implementation plan follows the Blueprint Protocol Template (PROTO-GOV-003) for systematic, autonomous execution with clear progress tracking.*

