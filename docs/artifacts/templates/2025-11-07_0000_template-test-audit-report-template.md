# Test Audit Report Template

**Document ID**: `TEMPLATE-AUDIT-001`
**Status**: ACTIVE
**Created**: 2025-11-07
**Last Updated**: 2025-11-07
**Type**: Audit Template

## When to Use
- ✅ Periodic test suite health assessments
- ✅ Pre-release quality validation
- ✅ Test debt identification and cleanup
- ✅ CI/CD pipeline quality gate audits
- ✅ Post-refactoring validation

## When NOT to Use
- ❌ Individual test debugging
- ❌ Performance profiling
- ❌ Code coverage analysis only
- ❌ Manual test execution

## Template Structure
```markdown
# Master Prompt
You are an autonomous AI agent, my Chief Test Auditor for conducting comprehensive test suite audits. Your primary responsibility is to execute the "Living Test Audit Blueprint" systematically, identify test debt, and provide actionable remediation plans. Do not ask for clarification on what to do next; your next task is always explicitly defined.

---

**Your Core Workflow is an Assess-Analyze-Remediate Loop:**
1. **Assess:** A clear `🎯 Audit Scope` will be provided for you to evaluate.
2. **Analyze:** You will systematically analyze test files, identify issues, and categorize findings.
3. **Remediate:** Based on analysis results, you will follow the specified remediation plan. Your response must be in two parts:
   * **Part 1: Audit Findings Report:** Provide a comprehensive analysis of test suite health with categorized issues and impact assessment.
   * **Part 2: Blueprint Update Confirmation:** Confirm that the living audit blueprint has been updated with findings and next remediation steps. The updated blueprint is available in the workspace file.

---

# Living Test Audit Blueprint: [Audit Name]

## Progress Tracker
- **STATUS:** Not Started / In Progress / Completed
- **CURRENT PHASE:** [Assessment / Analysis / Remediation / Validation]
- **LAST COMPLETED TASK:** [Description of last completed audit task]
- **NEXT TASK:** [Description of the immediate next audit task]

### Audit Implementation Outline (Checklist)

#### **Phase 1: Assessment & Discovery (Week 1)**
1. [ ] **Task 1.1: Test Suite Inventory**
   - [ ] Catalog all test files by type (unit, integration, performance, manual)
   - [ ] Count total test files and lines of code
   - [ ] Identify test file locations and organization structure

2. [ ] **Task 1.2: Quality Metrics Baseline**
   - [ ] Run linting checks across entire test suite
   - [ ] Execute test coverage analysis
   - [ ] Measure test execution time and reliability

3. [ ] **Task 1.3: Structural Analysis**
   - [ ] Analyze test file sizes and complexity
   - [ ] Check for TODO comments and incomplete implementations
   - [ ] Review test naming conventions and organization

#### **Phase 2: Deep Analysis & Categorization (Week 2)**
4. [ ] **Task 2.1: Code Quality Assessment**
   - [ ] Identify linting errors and code quality issues
   - [ ] Check type annotation coverage in test files
   - [ ] Analyze test utility and helper function quality

5. [ ] **Task 2.2: Test Effectiveness Evaluation**
   - [ ] Assess test coverage adequacy and gaps
   - [ ] Review test isolation and independence
   - [ ] Evaluate test maintainability and readability

6. [ ] **Task 2.3: Technical Debt Quantification**
   - [ ] Calculate test debt metrics (obsolete tests, duplication, complexity)
   - [ ] Identify maintenance burden and technical debt hotspots
   - [ ] Prioritize issues by impact and remediation effort

#### **Phase 3: Remediation Planning (Week 3)**
7. [ ] **Task 3.1: Issue Prioritization**
   - [ ] Categorize findings by severity (Critical, High, Medium, Low)
   - [ ] Create remediation roadmap with timelines
   - [ ] Identify quick wins vs. major refactoring needs

8. [ ] **Task 3.2: Solution Design**
   - [ ] Design consolidation strategies for duplicate tests
   - [ ] Plan removal procedures for obsolete test artifacts
   - [ ] Define quality gate implementations

9. [ ] **Task 3.3: Impact Assessment**
   - [ ] Estimate remediation effort and resource requirements
   - [ ] Assess risk of breaking changes during cleanup
   - [ ] Define success metrics for remediation completion

#### **Phase 4: Implementation & Validation (Week 4)**
10. [ ] **Task 4.1: Immediate Cleanup**
    - [ ] Remove identified obsolete test files
    - [ ] Fix critical linting errors and quality issues
    - [ ] Implement basic quality gates

11. [ ] **Task 4.2: Structural Improvements**
    - [ ] Reorganize test files according to standards
    - [ ] Consolidate duplicate test patterns
    - [ ] Update test utilities and helpers

12. [ ] **Task 4.3: Prevention Strategy**
    - [ ] Implement automated quality checks
    - [ ] Establish test maintenance protocols
    - [ ] Create monitoring and alerting systems

---

## 📋 **Technical Audit Requirements Checklist**

### **Test Suite Structure**
- [ ] Organized by type (unit/, integration/, performance/, manual/)
- [ ] Consistent naming conventions followed
- [ ] No test files in project root (except shared utilities)
- [ ] Proper separation of concerns maintained

### **Code Quality Standards**
- [ ] Zero linting errors in test suite
- [ ] Type annotations required for all test functions
- [ ] No TODO/FIXME comments in test code
- [ ] Test files under 300 lines maximum

### **Test Effectiveness**
- [ ] Test coverage > 80% maintained
- [ ] Tests execute reliably without flakiness
- [ ] Test isolation and independence verified
- [ ] Performance tests properly benchmarked

### **Maintenance & Documentation**
- [ ] Test documentation current and accurate
- [ ] CI/CD integration working properly
- [ ] Automated quality gates active
- [ ] Regular maintenance schedule established

---

## 🎯 **Audit Success Criteria Validation**

### **Discovery Objectives**
- [ ] All test files inventoried and categorized
- [ ] Quality metrics baseline established
- [ ] Technical debt hotspots identified
- [ ] Impact assessment completed

### **Analysis Objectives**
- [ ] Issues categorized by severity and type
- [ ] Root cause analysis completed
- [ ] Remediation effort estimated
- [ ] Risk assessment documented

### **Remediation Objectives**
- [ ] Critical issues resolved immediately
- [ ] Remediation roadmap created
- [ ] Quality gates implemented
- [ ] Prevention strategies established

### **Validation Objectives**
- [ ] Test suite health improved measurably
- [ ] Quality standards enforced automatically
- [ ] Maintenance burden reduced
- [ ] Team productivity increased

---

## 📊 **Risk Mitigation & Fallbacks**

### **Current Risk Level**: LOW / MEDIUM / HIGH
### **Active Mitigation Strategies**:
1. [Incremental Analysis - Process test files in batches to avoid overwhelming findings]
2. [Conservative Remediation - Start with safe, reversible changes]
3. [Comprehensive Testing - Validate all changes before committing]
4. [Stakeholder Communication - Regular updates on audit progress and findings]

### **Fallback Options**:
1. [Scoped Audit - If full audit is too large, focus on critical directories only]
2. [Phased Approach - Break remediation into smaller, manageable chunks]
3. [Revert Strategy - Maintain ability to rollback changes if issues arise]
4. [Documentation Focus - If code changes risky, prioritize documentation improvements]

---

## 🔄 **Blueprint Update Protocol**

**Update Triggers:**
- Phase completion (move to next phase)
- Significant findings discovered (update analysis)
- Remediation blocker encountered (adjust approach)
- Quality gate implementation (validate effectiveness)
- Stakeholder feedback received (incorporate changes)

**Update Format:**
1. Update Progress Tracker (STATUS, CURRENT PHASE, LAST COMPLETED TASK, NEXT TASK)
2. Mark completed checklist items with [x]
3. Add quantitative findings and metrics
4. Update risk assessment based on discoveries
5. Adjust remediation plan as needed

---

## 🚀 **Immediate Next Action**

**TASK:** [Description of the immediate next audit task]

**OBJECTIVE:** [Clear, concise goal of the audit task]

**APPROACH:**
1. [Step 1 to execute the audit task]
2. [Step 2 to execute the audit task]
3. [Step 3 to execute the audit task]

**SUCCESS CRITERIA:**
- [Measurable outcome 1 that defines task completion]
- [Measurable outcome 2 that defines task completion]
- [Measurable outcome 3 that defines task completion]
```

## Usage Guidelines

### **For AI Auditors**
1. **Assess Scope**: Determine if full audit or targeted assessment needed
2. **Customize Template**: Replace placeholders with audit-specific information
3. **Maintain Structure**: Keep all required sections and systematic approach
4. **Update Progress**: Regularly update progress tracker as audit proceeds
5. **Document Findings**: Use standardized categorization for all issues

### **For Development Teams**
1. **Review Scope**: Ensure audit covers necessary test aspects
2. **Validate Phases**: Check that phases and tasks are realistic for timeline
3. **Assess Resources**: Confirm team has capacity for remediation work
4. **Monitor Progress**: Use progress tracker for status updates and reporting
5. **Implement Changes**: Execute remediation plan systematically

## Quality Checklist

### **Required Elements**
- [ ] Master prompt with autonomous auditor definition
- [ ] Progress tracker with all required fields
- [ ] Audit implementation outline with phases and tasks
- [ ] Technical audit requirements checklist
- [ ] Success criteria validation
- [ ] Risk mitigation and fallbacks
- [ ] Blueprint update protocol
- [ ] Immediate next action defined

### **Content Quality**
- [ ] Clear, actionable audit tasks
- [ ] Realistic timelines and phases
- [ ] Comprehensive risk assessment
- [ ] Measurable success criteria
- [ ] Proper categorization of findings
- [ ] Consistent formatting and structure

## Related Documents

- [Blueprint Protocol Template](../governance/03_blueprint_protocol_template.md)
- [Test Audit Report 2025-11-07](../test_reports/2025-11-07_test_audit_report.md)
- [Artifact Management Protocol](../governance/01_artifact_management_protocol.md)
- [Master Artifact Registry](../../MASTER_INDEX.md)

---

*This template enables systematic, autonomous execution of comprehensive test audits with clear progress tracking, standardized findings categorization, and actionable remediation planning.*
