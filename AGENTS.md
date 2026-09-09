# AGENTS.md — Standing Knowledge & Instructions

## 1. Project Purpose & Scope

**Task-Manager** is a task and project management web application built with Python and Flask. It allows users to organize tasks under project tabs, manage open/closed task statuses, rename projects and tasks, and interact through either a web browser interface or a RESTful JSON API documented via Swagger.

---

## 2. Verified Technology Stack

*(Source of truth: `pyproject.toml`, `task_manager/__init__.py`, `task_manager/app.py`)*

- **Language**: Python (`>=3.13` as declared in `pyproject.toml`)
- **Web Framework**: Flask 3.1.3
- **Database & ORM**: SQLite (`ctm.db`), Flask-SQLAlchemy 3.1.1, SQLAlchemy 2.0.41
- **API Documentation**: Flasgger 0.9.7.1 (Swagger UI at `/apidocs/`)
- **Frontend**: HTML5, Jinja2 3.1.6, Bootstrap 3.3.7 (CDN), jQuery 1.12.4 (CDN), custom UX script (`ux.js`)
- **Test Suite**: `pytest` 9.0.3, `pytest-cov` 6.2.1

---

## 3. Project Entry Points & Running

- **Development Server**: `python task_manager/app.py` or `make dev` (Runs Flask dev server on `http://localhost:5000`)
- **Production Server**: `make prod` (Runs Gunicorn server on `http://localhost:8000`)
- **Interactive API Documentation**: `http://localhost:5000/apidocs/`
- **Application Factory**: `task_manager/__init__.py:create_app()`

---

## 4. Test Execution & Quality Assurance

The project supports standard Python environment runners. When using `uv` in this sandbox environment:

- **Run All Tests**: `uv run pytest`
- **Run with Coverage**: `uv run pytest --cov=task_manager --cov-report=term-missing`
- **Code Formatting / Type Checks** (configured in `pyproject.toml`):

  ```bash
  uv run black --check task_manager tests
  uv run isort --check task_manager tests
  uv run mypy task_manager
  ```

---

## 5. Architecture & Execution Flow

```
                      ┌─────────────────────────┐
                      │    USER / HTTP CLIENT   │
                      └────────────┬────────────┘
                                   │
                 ┌─────────────────┴─────────────────┐
                 │                                   │
                 ▼                                   ▼
      [ WEB UI REQUESTS ]                  [ REST API REQUESTS ]
    e.g., GET /, POST /add                e.g., GET /api/tasks,
    GET /project/<slug>                   POST /api/tasks, PUT /api/...
                 │                                   │
                 └─────────────────┬─────────────────┘
                                   │
                                   ▼
                       [ Flask Blueprint Routes ]
                         (task_manager/routes.py)
                                   │
       ┌───────────────────────────┴───────────────────────────┐
       │                                                       │
       ▼                                                       ▼
[ Jinja2 View Renderer ]                              [ JSON Response ]
(task_manager/templates/index.html)                  (Flask jsonify)
       │                                                       │
       └───────────────────────────┬───────────────────────────┘
                                   │
                                   ▼
                      [ SQLAlchemy ORM Models ]
                        (task_manager/models.py)
                       ├── Projects (project_id, project_name, active, url_slug)
                       └── Tasks (task_id, project_id, task, status, priority, due_date)
                                   │
                                   ▼
                        [ SQLite Database ]
                         (instance/ctm.db)
```

>> Note: Tasks also expose computed properties such as `is_overdue` and `due_date_display` in the current implementation.

---

## 6. Repository Map

```
task-manager/
├── task_manager/
│   ├── __init__.py         # Application factory (create_app) & DB initialization
│   ├── app.py              # Main entrypoint with Flasgger Swagger initialization
│   ├── models.py           # Database models (Projects, Tasks)
│   ├── routes.py           # Web UI routes & REST API endpoints
│   ├── templates/
│   │   └── index.html      # Jinja2 template for web interface
│   └── static/
│       └── js/
│           └── ux.js       # Client-side JavaScript interactions
├── tests/
│   ├── conftest.py         # Pytest fixtures (app, client, create_project, create_task)
│   ├── test_models.py      # ORM Model unit tests
│   ├── test_routes.py      # Web route integration tests
│   ├── test_api.py         # Web API integration tests
│   └── test_rest.py        # REST API unit tests
├── harness_learning/       # Exploration reports, implementation plans, and micro-contexts
├── pyproject.toml          # Project metadata, dependencies, and tool settings
├── Makefile                # Target commands (dev, prod, test, clean)
└── REST_README.md          # REST API usage documentation
```

---

## 7. Development Conventions

1. **Preserve Existing Signatures**: Ensure function and model parameter lists retain backwards compatibility to prevent breaking callers and test fixtures.
2. **Explicit Form & JSON Fallbacks**: Route handlers processing `request.form` or `request.get_json()` must handle missing keys gracefully using fallbacks.
3. **ORM Model Methods**: Domain logic and slug generation belong directly on model classes in `models.py`.
4. **Clean Commits**: Commit messages should follow standard Git conventions (short subject line under 50 characters, blank line, clear body detailing reasoning).

---

## 8. What NOT To Do (Negative Constraints)

- **DO NOT** modify codebase files during exploration phases when only research or planning is requested.
- **DO NOT** write code without progressive exploration and context gathering first.
- **DO NOT** introduce heavy external dependencies (e.g. migration frameworks or custom enum libraries) when simple Python standard types suffice.
- **DO NOT** state claims as verified truth without citing inspected files or test output.

---

## 9. Verification Instructions

Before declaring any task complete, perform three levels of verification:

1. **Behavioral Verification**: Confirm that the implemented requirement actually works end-to-end as intended in runtime execution, not merely that automated tests exist.
2. **Regression & Test Verification**: Execute `uv run pytest` to verify that relevant unit and integration tests pass and no regressions were introduced.
3. **Repository State Verification**: Run `git status` to confirm that only intended files were modified or created.
