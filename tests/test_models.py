from datetime import date

from task_manager import db
from task_manager.models import Tasks


def test_project_model_repr(app, create_project):
    project = create_project(name="Alchemy", active=True)
    with app.app_context():
        assert repr(project) == f"<Project {project.project_name}>"


def test_task_model_repr(app, create_task):
    task = create_task(task_desc="Test Task")
    with app.app_context():
        assert repr(task) == f"<Task {task.task}>"


def test_task_model_priority_default(app, create_task):
    task = create_task(task_desc="Default Priority Task")
    with app.app_context():
        assert task.priority == "Medium"


def test_task_model_priority_explicit(app, create_project, create_task):
    project = create_project(name="Priority Project")
    task = create_task(task_desc="Urgent Task", project=project, priority="High")

    with app.app_context():
        assert task.priority == "High"


def test_task_model_priority_invalid_fallback(app, create_project, create_task):
    project = create_project(name="Invalid Priority Project")
    task = create_task(task_desc="Invalid Task", project=project, priority="Urgent")

    with app.app_context():
        assert task.priority == "Medium"


def test_task_due_date_iso_parsing(app, create_project, create_task):
    project = create_project(name="ISO Test")
    task = create_task(task_desc="Test", project=project, due_date="2026-09-10")

    with app.app_context():
        assert task.due_date.isoformat() == "2026-09-10"


def test_task_due_date_none(app, create_project, create_task):
    project = create_project(name="None Test")
    task = create_task(task_desc="Test", project=project, due_date=None)

    with app.app_context():
        assert task.due_date is None
        assert task.is_overdue is False


def test_task_is_overdue(app, create_project, create_task):
    project = create_project(name="Overdue Test")
    past_date = (date.today().replace(year=date.today().year - 1)).isoformat()
    task = create_task(task_desc="Test", project=project, due_date=past_date)

    with app.app_context():
        assert task.is_overdue is True


def test_task_due_date_display(app, create_project, create_task):
    project = create_project(name="Display Test")
    task = create_task(task_desc="Test", project=project, due_date="2026-09-10")

    with app.app_context():
        assert task.due_date_display == "10/09"


def test_task_due_date_display_unassigned(app, create_project, create_task):
    project = create_project(name="Unassigned Display Test")
    task = create_task(task_desc="Test", project=project, due_date=None)

    db.session.commit()

    with app.app_context():
        assert task.due_date_display == "Unassigned"


def test_task_due_date_date_object(app, create_project, create_task):
    project = create_project(name="Date Object Test")
    d = date(2026, 9, 10)
    task = create_task(task_desc="Test", project=project, due_date=d)

    with app.app_context():
        assert task.due_date == d
