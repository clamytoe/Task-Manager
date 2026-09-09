# Exploration Report: Task Priority Feature

## 1. Boundary & Exploration Scope Constraint

- **Boundary Rule**: Source code (`task_manager/`, `tests/`) was strictly preserved without modification during exploration.
- **Artifact Scope**: This document in `harness_learning/` is generated specifically to capture exploration findings and structural dependencies as requested.

---

## 2. Observed Repository Facts vs Inferences vs Proposed Assumptions

### A. Observed Repository Facts (Grounded in Code Inspection)

1. **`task_manager/models.py`**:
   - `Tasks` table schema originally had columns: `task_id`, `project_id`, `task`, `status`.
  (Note: The current implementation now includes `priority` and `due_date`, added after this exploration phase.)
2. **`task_manager/routes.py`**:
   - `/add` (`POST`) retrieves `task = request.form.get("task")`, `project = request.form.get("project")`, `status = bool(int(request.form.get("status")))`.
   - `/api/tasks` (`GET`) serializes tasks into dictionaries with keys `id`, `project_id`, `task`, `status`.
   - `/api/tasks` (`POST`) accepts `project_id`, `task`, `status` from JSON payload.
   - `/api/tasks/<id>` (`PUT`) updates `task` and `status` from JSON payload.
3. **`conftest.py`**:
   - `create_task` fixture calls `Tasks(project_id=project.project_id, task=task_desc, status=status, priority=priority, due_date=due_date)`.

### B. Inferences (Derived Architectural Relationships)

1. Adding a new attribute to `Tasks` requires synchronized updates across ORM model attributes, form parsing, JSON serialization/deserialization, and test fixtures.
2. Form handlers use `request.form.get()` which defaults to `None` if a form parameter is missing; API endpoints use `request.get_json()` which requires dict key checking.

### C. Proposed Implementation Assumptions (Updated Outcome)

1. Task priority is stored as a string field (`"Low"`, `"Medium"`, `"High"`) with a default value of `"Medium"`.
2. Existing tasks and legacy API requests without explicit priority correctly default to `"Medium"`.
3. Priority is assigned at creation time and is not editable afterward in the current implementation.
4. Priority does not currently affect sorting order.

---

## 3. Structural Dependency Relationships vs Runtime Execution Flow

### A. Structural Dependency Relationships

- **`task_manager/models.py:Tasks`**
  └── Dependent on: `db.Model` (SQLAlchemy)
- **`task_manager/routes.py`**
  ├── Dependent on: `task_manager/models.py:Tasks`
  ├── Dependent on: `task_manager/models.py:Projects`
  └── Dependent on: `task_manager/templates/index.html`
- **`tests/conftest.py`**
  └── Dependent on: `task_manager/models.py:Tasks`
- **`tests/test_routes.py`, `tests/test_api.py`, `tests/test_rest.py`**
  └── Dependent on: `conftest.py` fixtures and `routes.py` endpoints

### B. Runtime Execution Flow for Task Operations

```
[ Web UI Form Submission ]                      [ REST API JSON Request ]
  POST /add                                        POST /api/tasks
     │                                                │
     ▼                                                ▼
Extract form fields                             Extract JSON fields
  (task, project, status)                          (project_id, task, status)
     │                                                │
     └───────────────────────┬────────────────────────┘
                             │
                             ▼
                 Instantiate Tasks Model
                 Tasks(project_id, task, status)
                             │
                             ▼
                 SQLAlchemy DB Session Commit
                 db.session.add() & db.session.commit()
                             │
     ┌───────────────────────┴────────────────────────┐
     │                                                │
     ▼                                                ▼
Redirect to / (Render index.html)             Return 201 Created JSON Payload
```

---

## 4. Grounding Verification Matrix

| Claim in Exploration Report | Inspected File & Line Evidence | Verification Status |
| :--- | :--- | :--- |
| `Tasks` model has `task_id`, `project_id`, `task`, `status` | `task_manager/models.py` (lines 28-34) | **Grounded** |
| `/add` route handles task creation via form data | `task_manager/routes.py` (lines 43-85) | **Grounded** |
| `/api/tasks` GET endpoint serializes task fields | `task_manager/routes.py` (lines 191-213) | **Grounded** |
| `create_task` test fixture instantiates `Tasks` | `conftest.py` (lines 38-46) | **Grounded** |
| Working tree is clean and 55 pytest tests pass | Terminal command `uv run pytest` output | **Grounded** |
