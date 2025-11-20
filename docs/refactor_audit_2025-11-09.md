# AgentQMS v001_b Refactor Audit (2025-11-09)

## Scope & Approach
- Reviewed automation layer under `agent_qms_v001_b/agent_tools`, agent interface in `agent_qms_v001_b/agent`, and supporting documentation/templates.
- Focused on runtime viability of tooling, structural duplication, and maintainability risks that block or slow agent-driven workflows.

## High-Priority Findings

- **Interface/implementation path drift breaks every agent command**
  - Evidence: `agent_qms_v001_b/agent/Makefile` and `agent_qms_v001_b/agent_interface/tools/*.py` still call `../scripts/agent_tools/...`, while the implementation now lives in `agent_qms_v001_b/agent_tools/` (`agent_tools/core/discover.py` even prints the outdated path).
  - Impact: `make` targets (e.g. `make discover`, `make validate`) and direct CLI invocations raise `python: can't open file '.../scripts/agent_tools/...': [Errno 2] No such file or directory`. The agent interface is effectively unusable.
  - Refactor: decide on one canonical package path—either restore a `scripts/agent_tools` package shim or update every entrypoint (Makefile, wrappers, docs, generated help text) to the new `agent_tools` location. Add integration tests that run high-traffic targets to prevent regressions.

- **Bootstrap dependency removed but still required by most tools**
  - Evidence: `agent_tools/core/artifact_workflow.py`, `agent_tools/compliance/validate_artifacts.py`, and `agent_tools/utilities/get_context.py` call `_load_bootstrap()` expecting `scripts/_bootstrap.py`, yet no such file exists in the repo.
  - Impact: Any script launched directly fails immediately with `RuntimeError("Could not locate scripts/_bootstrap.py")`, so artifact creation, validation, and context bundling are dead paths.
  - Refactor: either reintroduce a maintained bootstrap module (containing `setup_project_paths`, `get_path_resolver`, etc.) or strip the bootstrap loader and replace with explicit relative imports + a small `sys.path` helper.

- **Agent wrappers depend on missing `streamlit_app` module**
  - Evidence: `agent_interface/tools/discover.py`, `agent_interface/tools/quality.py`, `agent_interface/tools/feedback.py`, and MCP adapters import `streamlit_app.utils.path_utils`, which never ships in this export. The Makefile even instructs `pip install -r ../streamlit_app/requirements.txt` though `streamlit_app/` is absent.
  - Impact: Every wrapper raises `ModuleNotFoundError: No module named 'streamlit_app'`; AST/feedback/compliance flows cannot start.
  - Refactor: decouple wrappers from the Streamlit project. Lift the tiny path utilities into this repo (or into the restored bootstrap) and drop the hard dependency on a UI package the release no longer includes.

- **Doc/tooling references point at non-existent scripts**
  - Evidence: `agent_tools/documentation/auto_generate_index.py` shells out to `python scripts/agent_tools/validate_manifest.py`, and documentation throughout `ai_agent/` & `agent_tools/index.md` instructs identical paths.
  - Impact: Even after fixing imports, doc-generation workflows still fail because they dispatch to dead entrypoints.
  - Refactor: sweep the repo for `scripts/agent_tools` references, update to the new layout, and regenerate helper docs so the instructions match reality.

- **Duplicate targets & stale outputs hide breakages**
  - Evidence: `agent_qms_v001_b/agent/Makefile` defines `context-list` twice (lines 147 & 210), masking failures when one path changes. Generated indexes like `agent_templates/INDEX.md` include truncated metadata, signalling the generator may also be stale.
  - Impact: Drift accumulates silently; automation that depends on these outputs may misbehave without failing fast.
  - Refactor: deduplicate Makefile targets, add CI smoke tests that run `make help` and fast doc-generation commands, and re-run generators once the import path issues are solved.

## Medium-Priority Findings

- **Monolithic artifact validator (`agent_tools/compliance/validate_artifacts.py`) is ~560 lines with hand-rolled YAML parsing and duplicated config**
  - Maintenance cost is high; logic (prefix lists, status enums, bundle hooks) is sprinkled across validation, workflow, and docs. Consider splitting into modules (`naming`, `frontmatter`, `bundles`), load config from a shared YAML, and rely on a mature YAML parser.

- **Hard-coded handbook schema duplicated in code and docs**
  - `agent_tools/documentation/auto_generate_index.py` bakes the full directory taxonomy. Similar tables appear in the handbook. Drifts must be updated in several places. Extract shared schema (e.g. `docs/config/handbook.yaml`) and have the generator read it.

- **Quality management toolbelt uses mutable defaults and weak templating guarantees**
  - `quality_management_framework/toolbelt/core.py` defines `tags: list = []`, writes frontmatter+body without guarding delimiter placement, and silently overwrites files. Refactor to immutable defaults, central template validation, and idempotent writes (fail if file exists unless `--force`).

- **Deprecated scripts left in production tree**
  - `_deprecated/` still exposes runnable Python modules without safeguards. Agents might call them accidentally. Either delete, archive elsewhere, or add a guard that refuses to run.

## Low-Priority / Nice-to-Have

- Ensure `agent_tools/index.md` and template indexes include frontmatter and consistent summaries so they can be validated alongside other docs.
- Add unit/integration coverage around critical CLIs (artifact creation, bundle lookups) once bootstrap/import problems are resolved.
- Track versions of third-party deps (`jinja2`, `yaml`, `jsonschema`) in a `requirements.txt` or `pyproject.toml`; the current export omits dependency declarations.

## Suggested Next Steps
1. Restore runtime parity: reintroduce (or replace) bootstrap/path utils, fix import paths, and run a full suite of CLI smoke tests.
2. Once automation works end-to-end, refactor the large validator into smaller modules backed by shared config data.
3. Prune or quarantine deprecated utilities and regenerate public indexes/documentation so they reflect the new structure.f
