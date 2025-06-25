from task_manager import db
from task_manager.models import Tasks


def test_add_task(client, create_project):
    project = create_project(name="Urgent Stuff")
    response = client.post(
        "/add",
        data={
            "project": project.project_id,
            "task": "Finish tests",
            "status": 1,
        },
    )
    assert response.status_code == 302


def test_rename_task_desc(app, client, create_task):
    task = create_task(task_desc="Old Task")

    response = client.post(
        f"/rename_task_desc/{task.task_id}",
        json={"new_desc": "Updated Task"},
    )

    assert response.status_code == 204

    with app.app_context():
        updated = db.session.get(Tasks, task.task_id)
        assert updated.task == "Updated Task"  # type: ignore


def test_delete_task(app, client, create_task):
    task = create_task(task_desc="Vanishing Task")
    tid = task.task_id

    response = client.get(f"/delete/{tid}")
    assert response.status_code == 302  # Redirect after deletion

    with app.app_context():
        deleted = db.session.get(Tasks, tid)
        assert deleted is None
