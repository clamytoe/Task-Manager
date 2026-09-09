# Updated Task Priority Feature: Micro Context & Guardrails (Corrected & Current)

> *All untouched portions remain conceptually the same; only outdated parts are updated.*

This PR enhances the Task‑Manager application by expanding task metadata handling and improving user interaction flows. It introduces full due‑date support, overdue detection, inline editing for due dates, and UI refinements that improve clarity and usability. Priority assignment remains a creation‑time attribute and is displayed consistently, though not editable after creation. Sorting behavior is unchanged. The PR also strengthens API validation, improves consistency across routes, and maintains full compatibility with existing project and task workflows.

---

## ✔ What stayed the same

These elements from the original micro‑context remain accurate and unchanged:

- The PR improves metadata handling for tasks.  
- It enhances user interaction flows.  
- It maintains compatibility with existing project/task workflows.  
- It improves consistency across routes and validation.  

## ✔ What was updated

These elements were corrected to match the current implementation:

- Priority is **not** editable after creation.  
- Tasks are **not** sorted by priority.  
- Due‑date support is now fully implemented (including overdue logic and inline editing).  
- UI improvements now include “Unassigned” display and proper overdue highlighting.  

---

## 1. Role Delineation of Harness Artifacts

- **`AGENTS.md`**: Standing project knowledge, environment conventions, and permanent agent directives.
- **`harness_learning/exploration_report.md`**: Grounded repository evidence, structural dependencies, and execution flow.
- **`harness_learning/implementation_plan.md`**: Task intent, minimal design choices, and behavioral acceptance criteria.
- **`harness_learning/micro_context.md`**: Targeted code symbols, inspection vs modification boundaries, and quantitative debugging protocols.

---

## 2. Symbol-Level Target Mapping

| Target Symbol / Function | File Location | Purpose & Action |
| :--- | :--- | :--- |
| `class Tasks(db.Model)` | `task_manager/models.py` | Add `priority` Column definition and update `__init__` constructor signature with default `priority="Medium"`. |
| `def add_task()` | `task_manager/routes.py` | Extract `request.form.get("priority", "Medium")` and pass to `Tasks`. |
| `def api_get_tasks()` & `api_get_task()` | `task_manager/routes.py` | Add `"priority": t.priority` to JSON serialization dict. |
| `def api_create_task()` | `task_manager/routes.py` | Extract `data.get("priority", "Medium")` from JSON body when creating task. |
| `def api_update_task()` | `task_manager/routes.py` | Update `task.priority = data.get("priority", task.priority)` from JSON body. |
| Form & Table HTML snippets | `task_manager/templates/index.html` | Add `<select name="priority">` in task input form; display priority badge in task table. |

---

## 3. Inspection vs Modification Boundaries

### A. Direct Modification Scope

- `task_manager/models.py` (specifically `Tasks` class)
- `task_manager/routes.py` (specifically `/add` and `/api/tasks*` endpoints)
- `task_manager/templates/index.html` (specifically task form and task row rendering)

### B. Conditional Modification Scope

- `conftest.py`: **Modification is NOT required initially**. Because `Tasks.__init__` will provide `priority="Medium"` as a default parameter, existing `create_task` calls will continue working seamlessly without changing `conftest.py`. Modifying `conftest.py` should only be done if explicit priority overrides are needed in new tests.

### C. Inspection-Allowed / Non-Modification Scope

- `task_manager/app.py` & `task_manager/__init__.py`: May be inspected for DB initialization context, but **MUST NOT be modified**.
- `tests/test_routes.py` & `tests/test_rest.py`: May be inspected for test patterns, but **existing test assertions MUST NOT be modified or deleted** (only new tests appended).

---

## 4. Quantitative Debugging Protocol & Stagnation Rules

When encountering an unexpected test failure or bug during development, follow this strict quantitative protocol:

### A. Read-Only Diagnosis Rule

- **Mandatory**: All diagnostic investigation MUST remain strictly read-only (`read_file`, `uv run pytest`, `git diff`). **DO NOT edit code during diagnosis**. Formulate a root-cause hypothesis first, verify it against inspected files, and only edit when a clear fix is identified.

### B. Local-to-Global Escalation Steps

1. **Local Unit Verification**: Run only the specific failing test file (e.g., `uv run pytest tests/test_models.py`).
2. **Structural Dependency Check**: Trace broken references through the dependency map (`Models` -> `Routes` -> `Templates`/`API`).
3. **Alternative Safe Route Application**: An "Alternative Safe Route" is defined as applying an existing, verified repository pattern from another working module (e.g., copying the `status` handling pattern from `api_update_task`) rather than inventing custom mechanisms.
   - *STRICT PROHIBITION*: NEVER use temporary patch placeholders, mock overrides, dummy fallbacks, or `# type: ignore` hacks to bypass failures.

### C. Quantitative Limits & Stagnation Thresholds

- **Maximum Retries**: A maximum of **3 modification attempts** is permitted for any single test failure.
- **Stagnation Rule**: If **2 consecutive modification attempts** result in the exact same error message or produce no new diagnostic information, the agent is considered **stagnated**.
- **Escalation Trigger**: Upon reaching the stagnation threshold or 3-retry limit, the agent MUST immediately stop, revert changes using `git checkout` / `restore_file`, and request user input with diagnostic findings.
