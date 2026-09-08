# Specification: Task Due Dates Feature

## 1. Overview & Purpose

This specification defines the requirement for adding an **optional Due Date** field to tasks in the Task-Manager application. When specified, the due date is displayed directly in front of the task description in `DD/MM` format. If the due date has passed, the due date label turns **red**. Tasks created without a due date (and all pre-existing tasks in the database) default to showing `"Unassigned"`.

---

## 2. Core Requirements & Scope Boundaries

### Included Features

1. **Optional Due Date Input**: User can optionally select or enter a due date during task creation via Web UI or REST API.
2. **Display Format**: Rendered in `DD/MM` format (e.g. `25/12`) directly in front of the status checkbox / task action icons.
3. **Unassigned Fallback**: Tasks without a due date display `"Unassigned"`. All existing records in the database inherit `"Unassigned"`.
4. **Overdue Highlighting**: If the current date exceeds the task's due date, the due date text/badge renders in **red** (e.g., Bootstrap CSS `text-danger` or `label-danger`).
5. **REST API & Swagger Integration**: `due_date` field exposed in GET, POST, and PUT API responses/payloads.

### Explicit Negative Constraints (Out of Scope)

* **NO Reminders**: Do NOT build email, push, or popup reminder functionality.
* **NO Notifications**: Do NOT send background notifications or queue system messages.
* **NO Recurring Schedules**: Do NOT build recurring due date logic or calendar sync integrations.

---

## 3. Interfaces & Data Contracts

### A. Database Schema (`task_manager/models.py`)

* **New Column**: `due_date = db.Column(db.String(10), default="Unassigned")`
* **Model Constructor**:

  ```python
  def __init__(self, project_id, task, status=True, priority="Medium", due_date="Unassigned"):
      self.project_id = project_id
      self.task = task
      self.status = status
      self.priority = priority
      self.due_date = due_date if due_date else "Unassigned"
  ```

### B. Web Interface (`task_manager/templates/index.html` & `routes.py`)

1. **Creation Form**:
   * Add optional date input field in task form:
     `<input type="date" id="due_date" name="due_date" class="form-control" placeholder="Due Date (DD/MM)">`
2. **Task Table Display**:
   * Position: Rendered just before the status check icon / column in `index.html`.
   * Template Logic:

     ```jinja2
     {% if task.due_date and task.due_date != "Unassigned" and is_overdue(task.due_date) %}
       <span class="text-danger font-weight-bold">{{ task.due_date }}</span>
     {% else %}
       <span>{{ task.due_date }}</span>
     {% endif %}
     ```

### C. REST API Contracts (`task_manager/routes.py`)

1. **`GET /api/tasks` & `GET /api/tasks/<id>`**:
   * Response payload key: `"due_date": "25/12"` or `"due_date": "Unassigned"`.
2. **`POST /api/tasks`**:
   * Optional JSON property: `"due_date": "25/12"`. If omitted or null, defaults to `"Unassigned"`.
3. **`PUT /api/tasks/<id>`**:
   * Optional JSON property: `"due_date": "25/12"`. Updates task due date if provided.

---

## 4. Blast Radius Analysis & Risk Mitigation

| Component | Blast Radius Risk | Mitigation Strategy |
| :--- | :--- | :--- |
| **`Tasks.__init__` Constructor** | **High**: Adding `due_date` as a required parameter breaks all existing model instantiations in routes and unit test fixtures. | Make `due_date="Unassigned"` an optional keyword argument with default value. |
| **Database Backward Compatibility** | **High**: Existing rows in `ctm.db` will have `NULL` or missing `due_date` values. | Python property getter / helper method treats `None` or missing value as `"Unassigned"`. |
| **Date Parsing Mismatch** | **Medium**: Users or API clients submitting dates in `YYYY-MM-DD` vs `DD/MM` formats. | Standardize formatting logic helper `format_due_date()` in Python to format valid dates to `DD/MM` and fall back safely to `"Unassigned"`. |
| **Overdue Comparison** | **Medium**: Date comparison logic failing across month boundaries or leap years. | Parse `DD/MM` with current year context using Python `datetime` for overdue comparison (`task_date < today`). |

---

## 5. Verification & Test Strategy

To verify feature correctness without regressions:

1. **Model Tests (`tests/test_models.py`)**:
   * Verify default `due_date` is `"Unassigned"`.
   * Verify explicit `due_date` storing (e.g. `"15/08"`).
2. **Web Route & Overdue Styling Tests (`tests/test_routes.py`)**:
   * Verify task creation with and without `due_date`.
   * **Mandatory Test**: Verify that if a due date has passed (e.g., yesterday's date formatted as `DD/MM`), the rendered HTML contains the `text-danger` class or red styling indicator.
3. **REST API Tests (`tests/test_rest.py`)**:
   * Verify `GET /api/tasks` returns `"due_date"` field for all records.
   * Verify `POST /api/tasks` accepts `"due_date"`.
   * Verify `PUT /api/tasks/<id>` updates `"due_date"`.

---

## 6. Acceptance Criteria (Definition of Done)

* **AC 1**: Tasks created without a due date show `"Unassigned"`.
* **AC 2**: Pre-existing tasks in the database display `"Unassigned"`.
* **AC 3**: Due dates display in `DD/MM` format positioned before the status check icon.
* **AC 4**: When a task due date is in the past, it renders in **red** text/style on the UI.
* **AC 5**: REST API GET, POST, and PUT endpoints support `"due_date"`.
* **AC 6**: Automated test asserts that overdue tasks render with red styling indicator.
* **AC 7**: Zero reminders, notifications, or extraneous features are added.
