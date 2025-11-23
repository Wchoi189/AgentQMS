---
type: "assessment"
category: "java-migration"
status: "draft"
version: "0.1"
tags: ["java", "tooling", "cleanup", "migration"]
title: "Assessment: Java Migration Pruning Plan"
date: "2025-11-20 00:00 (KST)"
author: "Agent Maintainers"
---

# Assessment: Java Migration Pruning Plan

## 1. Objective & Method
- Branch `agent_java` must drop Python- and Node-focused helpers so the framework can be reimplemented around a Java toolchain.
- Surveyed `AgentQMS/agent_interface`, `AgentQMS/agent_scripts`, and `AgentQMS/agent_tools` to classify every executable surface (Python, Node, shell).
- Kept focus on **scripted automation**; documentation, templates, and Markdown artifacts remain language-agnostic and are outside this pruning pass.

## 2. Removal Candidates (Language-Incompatible / Low ROI)

| # | Component | Location | Runtime & Coupling | Why Removal Is Recommended |
|---|-----------|----------|--------------------|----------------------------|
| 1 | Agent-only Make targets | `AgentQMS/agent_interface/Makefile` | GNU Make shelling out to Python entrypoints (`python ../agent_tools/...`) for every action | Targets assume Python CLI availability and reference module paths that will disappear once Java replaces the runtime. Rebuilding the command surface in Gradle/Maven is cleaner than shimming every target. |
| 2 | Adaptation wizard | `AgentQMS/agent_scripts/adapt_project.py` | Python + PyYAML interactive CLI | Script injects YAML-driven placeholder replacements for docs (`docs/ai_handbook/**`) and agent configs, but every helper (`ProjectAdapter`, `interactive_setup`) is Python-specific. Converting projects for Java will require a new scaffolder anyway, so drop this file. |
| 3 | Legacy browser automation | `AgentQMS/agent_scripts/browser-automation/*.js` | Node + Puppeteer targeting Streamlit (`verify_analysis_page_fix.js` hits `http://localhost:8501`) | These scripts automate a Python Streamlit UI, not the Java stack we plan to support. Keeping them would force Node tooling plus the old Streamlit service just to run tests. |
| 4 | Audio/TTS helpers | `AgentQMS/agent_scripts/utilities/{elevenlabs_tts.py,play_audio.py,play_audio.sh}` | Python subprocesses, ElevenLabs REST API, PulseAudio/ffplay integration | Features are unrelated to Java migration and add brittle multimedia dependencies. No strong value proposition for Java automation; remove until a JVM-native notification layer exists. |
| 5 | Process/Env wrappers | `AgentQMS/agent_scripts/utilities/{env_loader.py,process_manager.py,path_utils.py}` | Python-only shims around `subprocess`, `psutil`, and POSIX paths | Java runtime will introduce different process control primitives; keeping these risks conflicting abstractions. Replace with JVM-native helpers later if needed. |
| 6 | Tracking CLI + SQLite tooling | `AgentQMS/agent_tools/utilities/tracking/cli.py` (invoked via `make plan-new`, `exp-export`) | Python Click CLI, SQLite file, YAML config loaders | Java migration should lean on JPA/H2 or another JVM-friendly persistence layer. Rewriting this CLI in Java is a larger effort than starting from requirements; archive the Python version. |
| 7 | AST wrappers | `AgentQMS/agent_interface/tools/ast_analysis.py` & `make ast-*` targets | Python AST inspection, imports `AgentQMS.agent_scripts.ast_analysis_cli` | Tightly bound to Python syntax trees, so they cannot analyze Java code. Drop them to avoid confusion once the repo becomes Java-first. |
| 8 | Automated compliance shell | `AgentQMS/agent_tools/automated_compliance_fix.sh` and related maintenance scripts | bash calling Python modules (`validate_artifacts.py`, `documentation_quality_monitor.py`) | These scripts merely orchestrate the Python validators slated for removal. Keeping stale shell wrappers creates dead commands and onboarding friction. |

## 3. High-Utility Capabilities to Port to Java
Only the following toolsets showed repeatable value for QMS operations; they should be **rewritten** (not shimmed) inside the emerging Java framework.

| Capability | Source Files | Why It Matters | Java Porting Notes |
|------------|--------------|----------------|--------------------|
| Artifact lifecycle orchestration | `AgentQMS/agent_tools/core/artifact_workflow.py` | Centralizes create/validate/index/update flows for implementation plans and assessments; enforces boundary checks before emitting artifacts. | Recreate as a Java service (Spring CLI or Gradle plugin) that reads the same Markdown templates and manifests. Preserve hooks for validation + index refresh. |
| Compliance & boundary validators | `AgentQMS/agent_tools/compliance/{validate_artifacts.py,validate_boundaries.py}` | Enforces naming/frontmatter rules and ensures docs stay within approved directories. | Implement validators as Java CLI commands using existing schemas; results should still integrate with docs under `docs/artifacts`. |
| Documentation index + manifest upkeep | `AgentQMS/agent_tools/documentation/{auto_generate_index.py,update_artifact_indexes.py,validate_links.py}` | Keeps handbook/artifact indexes synchronized; prevents link rot. | Port logic into Java to regenerate Markdown indices (possibly via FreeMarker/VTL). These are the only documentation scripts with cross-cutting utility. |
| Audit workbook generators | `AgentQMS/agent_tools/audit/{audit_generator.py,checklist_tool.py}` | Automates audit package creation and status reporting, directly supporting compliance workflows. | Convert to Java templating so teams retain automated audit scaffolds without depending on Python. |

Everything else (feedback reporters, ElevenLabs integration, experimental tracking CLI, Puppeteer harnesses) either duplicates IDE capabilities or depends on runtimes we no longer intend to ship. Pruning them now reduces noise before the Java toolchain lands.

## 4. Evidence Highlights
- **Agent command surface**: every Make target shells out to `python ../agent_tools/...` from `AgentQMS/agent_interface/Makefile`, so none of the commands run without Python available.
- **Browser automation**: scripts such as `AgentQMS/agent_scripts/browser-automation/verify_analysis_page_fix.js` import `puppeteer`, open `http://localhost:8501`, and inspect Streamlit selectors—tightly coupling them to the deprecated Python dashboard.
- **Artifact workflow**: `AgentQMS/agent_tools/core/artifact_workflow.py` imports validators and templates from the Python package and orchestrates subprocess calls to documentation scripts, underscoring why it is the single most valuable component to port rather than delete.
- **Compliance validator**: `AgentQMS/agent_tools/compliance/validate_artifacts.py` codifies naming/frontmatter rules that protect the documentation tree, making it a prime candidate for a Java rewrite.
- **Audio helpers**: `AgentQMS/agent_scripts/utilities/elevenlabs_tts.py` wraps the ElevenLabs REST API and drives playback through `ffplay`, which has no role in the lean Java framework.

## 5. Next Steps
1. **Archive the removal set** listed in §2 (delete directories or move into `_archive/python_legacy/` so they stop appearing in discovery commands).
2. **Capture requirements** for the four high-utility capabilities and decide on the Java packaging surface (Gradle plugin vs. CLI jar).
3. **Stub new Java modules** that recreate artifact lifecycle + validator flows, pointing at the existing `docs/` tree to keep outputs compatible.
4. **Update onboarding docs** once the new CLI shape is known so agents understand the reduced surface area.

