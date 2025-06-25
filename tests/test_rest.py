import json

from task_manager import db
from task_manager.models import Projects, Tasks


def test_get_projects_empty(client):
    response = client.get("/api/projects")
    assert response.status_code == 200
    assert json.loads(response.data) == []


def test_get_projects(client, create_project):
    project = create_project("Project1", True)
    response = client.get("/api/projects")
    data = json.loads(response.data)
    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]["id"] == project.project_id
    assert data[0]["name"] == "Project1"
    assert data[0]["active"] is True


def test_get_project_valid(client, create_project):
    project = create_project("Project1", True)
    response = client.get(f"/api/projects/{project.project_id}")
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data["id"] == project.project_id
    assert data["name"] == "Project1"


def test_get_project_invalid(client):
    response = client.get("/api/projects/9999")
    assert response.status_code == 404
    assert "error" in json.loads(response.data)


def test_get_tasks_empty(client):
    response = client.get("/api/tasks")
    assert response.status_code == 200
    assert json.loads(response.data) == []


def test_get_tasks(client, create_task):
    task = create_task("Task1", True)
    response = client.get("/api/tasks")
    data = json.loads(response.data)
    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]["id"] == task.task_id
    assert data[0]["task"] == "Task1"


def test_get_task_valid(client, create_task):
    task = create_task("Task1", True)
    response = client.get(f"/api/tasks/{task.task_id}")
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data["id"] == task.task_id
    assert data["task"] == "Task1"


def test_get_task_invalid(client):
    response = client.get("/api/tasks/9999")
    assert response.status_code == 404
    assert "error" in json.loads(response.data)


def test_create_project_success(client):
    response = client.post("/api/projects", json={"name": "NewProj", "active": True})
    data = json.loads(response.data)
    assert response.status_code == 201
    assert "id" in data
    assert data["message"] == "Project created"


def test_create_project_fail(client):
    response = client.post("/api/projects", json={})
    data = json.loads(response.data)
    assert response.status_code == 400
    assert "error" in data


def test_create_task_success(client, create_project):
    project = create_project("P", True)
    payload = {"project_id": project.project_id, "task": "New Task", "status": False}
    response = client.post("/api/tasks", json=payload)
    data = json.loads(response.data)
    assert response.status_code == 201
    assert "id" in data
    assert data["message"] == "Task created"


def test_create_task_fail(client):
    response = client.post("/api/tasks", json={"task": "No project"})
    data = json.loads(response.data)
    assert response.status_code == 400
    assert "error" in data


def test_update_project_success(client, create_project, app):
    project = create_project("OldName", False)
    payload = {"name": "UpdatedName", "active": True}
    response = client.put(f"/api/projects/{project.project_id}", json=payload)
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data["message"] == "Project updated"

    with app.app_context():
        updated = db.session.get(Projects, project.project_id)
        assert updated.project_name == "UpdatedName"
        assert updated.active is True


def test_update_project_fail(client):
    response = client.put("/api/projects/9999", json={"name": "Name"})
    data = json.loads(response.data)
    assert response.status_code == 404
    assert "error" in data


def test_update_task_success(client, create_task, app):
    task = create_task("OldTask", True)
    payload = {"task": "NewTask", "status": False}
    response = client.put(f"/api/tasks/{task.task_id}", json=payload)
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data["message"] == "Task updated"

    with app.app_context():
        updated = db.session.get(Tasks, task.task_id)
        assert updated.task == "NewTask"
        assert updated.status is False


def test_update_task_fail(client):
    response = client.put("/api/tasks/9999", json={"task": "Name"})
    data = json.loads(response.data)
    assert response.status_code == 404
    assert "error" in data


def test_delete_project_success(client, create_project, app):
    project = create_project("ToDelete", True)
    response = client.delete(f"/api/projects/{project.project_id}")
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data["message"] == "Project deleted"

    with app.app_context():
        assert db.session.get(Projects, project.project_id) is None


def test_delete_project_fail(client):
    response = client.delete("/api/projects/9999")
    data = json.loads(response.data)
    assert response.status_code == 404
    assert "error" in data


def test_delete_task_success(client, create_task, app):
    task = create_task("TaskToDelete", True)
    response = client.delete(f"/api/tasks/{task.task_id}")
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data["message"] == "Task deleted"

    with app.app_context():
        assert db.session.get(Tasks, task.task_id) is None


def test_delete_task_fail(client):
    response = client.delete("/api/tasks/9999")
    data = json.loads(response.data)
    assert response.status_code == 404
    assert "error" in data


def test_delete_all_success(client, app):
    response = client.delete("/api/delete_all")
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data["message"] == "All projects and tasks deleted"

    with app.app_context():
        assert Projects.query.count() == 0
        assert Tasks.query.count() == 0
