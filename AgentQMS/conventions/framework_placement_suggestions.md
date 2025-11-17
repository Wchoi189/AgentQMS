# Suggestions for Quality Management Framework Placement

The current location of the Quality Management Framework (QMF) at `.claude/export_package/quality_management_framework` was temporary. A permanent, well-considered location is crucial for maintainability, discoverability, and clarity for both human developers and AI agents.

Here are three potential placement strategies, with a final recommendation.

---

### Suggestion 1: Top-Level `quality_framework` Directory (Recommended)

**Proposed Location:** `/quality_framework`

This is the most straightforward and recommended approach.

```
/
├── quality_framework/
│   ├── q-manifest.yaml
│   ├── schemas/
│   ├── templates/
│   └── toolbelt/
├── streamlit_app/
├── agent/
└── ... (other project directories)
```

**Pros:**

*   **High Visibility:** Placing the framework at the root of the project makes it immediately visible and signals its importance as a core component of the development process.
*   **Clear Separation:** It is distinctly separate from application-specific code (like `streamlit_app`) and agent-specific logic (`agent`), enforcing a clean architecture.
*   **Unambiguous Naming:** The name `quality_framework` is explicit and leaves no doubt as to its purpose. It avoids generic names like `utils` or `common` which can become a dumping ground for unrelated code.
*   **Agent-Friendly:** An AI agent can be easily instructed to look for the `/quality_framework` directory as its starting point for all quality-related tasks.

**Cons:**

*   Adds another directory to the project root, which some developers prefer to keep minimal. However, for a component of this importance, the visibility is a net benefit.

---

### Suggestion 2: Under a `shared` or `common` Directory

**Proposed Location:** `/shared/quality_framework`

This option is ideal if you anticipate having other shared libraries or components that are used across different parts of your application.

```
/
├── shared/
│   ├── quality_framework/
│   └── ... (other future shared libraries)
├── streamlit_app/
├── agent/
└── ...
```

**Pros:**

*   **Good for Scalability:** If you plan to introduce other cross-cutting concerns like a design system, a data access library, or other frameworks, this structure keeps them neatly organized.
*   **Reduces Root Clutter:** It helps keep the top-level directory cleaner by grouping shared components.

**Cons:**

*   **Potential for Over-Engineering:** If the QMF is the *only* shared component, creating a `shared` directory might be unnecessary abstraction.
*   **Slightly Less Discoverable:** It requires one extra level of navigation, making it slightly less obvious than a top-level directory.

---

### Suggestion 3: As a Sub-Package of the `agent` Directory

**Proposed Location:** `/agent/frameworks/quality`

This approach treats the QMF as a tool that is exclusively owned and used by the AI agent.

```
/
├── agent/
│   ├── frameworks/
│   │   └── quality/
│   ├── tools/
│   └── ...
├── streamlit_app/
└── ...
```

**Pros:**

*   **Agent-Centric:** Co-locates the framework with other agent-specific code, reinforcing the idea that it's part of the agent's core capabilities.

**Cons:**

*   **Reduces Visibility for Humans:** Human developers might not think to look inside the `agent` directory for a project-wide quality framework.
*   **Limits Scope:** This placement implies that only the agent should use the framework. In reality, you might want human developers to use the `toolbelt` for their own tasks as well.
*   **Potentially Confusing:** It could be mistaken for a framework *for building agents*, rather than a framework *used by agents*.

---

## Final Recommendation

**The recommended approach is Suggestion 1: a top-level `/quality_framework` directory.**

This option provides the best balance of visibility, clarity, and architectural cleanliness. It establishes the QMF as a first-class citizen of the project, making it easy for both current and future developers (human or AI) to understand its role and how to use it.
