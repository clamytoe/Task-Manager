from task_manager import db
from task_manager.models import Projects, Tasks


# Test /
def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200


def test_index_single_project_auto_activate(client, create_project, app):
    project = create_project(active=False)
    response = client.get("/")
    assert response.status_code == 200

    with app.app_context():
        updated = db.session.get(Projects, project.project_id)
        assert updated.active is True


def test_index_multiple_projects_with_one_active(client, create_project, app):
    p1 = create_project("Inactive", active=False)
    p2 = create_project("Active", active=True)

    response = client.get("/")
    assert response.status_code == 200
    # Confirm the active project remains active
    with app.app_context():
        assert p2.active is True
        assert p1.active is False


def test_index_multiple_projects_none_active(client, create_project, app):
    create_project("One", active=False)
    create_project("Two", active=False)

    response = client.get("/")
    assert response.status_code == 200

    with app.app_context():
        all_projects = Projects.query.all()
        actives = [p for p in all_projects if p.active]
        assert len(actives) == 1


def test_index_no_projects(client):
    response = client.get("/")
    assert response.status_code == 200


# Test /projects


def test_add_task_no_task_field(client):
    response = client.post("/add", data={"project": "Something"})
    # Missing 'task' should trigger redirect
    assert response.status_code == 302
    assert response.location.endswith("/")


def test_add_task_blank_task(client):
    response = client.post("/add", data={"task": "", "project": "Something"})
    assert response.status_code == 302  # Redirect on blank task
    assert response.location.endswith("/")


def test_add_task_default_project(client, app):
    response = client.post(
        "/add", data={"task": "Do this", "project": "", "status": "1"}
    )
    assert response.status_code == 302

    with app.app_context():
        task = Tasks.query.first()
        project = db.session.get(Projects, task.project_id)
        assert task.task == "Do this"
        assert project.project_name == "Tasks"


def test_add_task_new_project_created(client, app):
    response = client.post(
        "/add", data={"task": "Task A", "project": "Alpha", "status": "1"}
    )
    assert response.status_code == 302

    with app.app_context():
        proj = Projects.query.filter_by(project_name="Alpha").first()
        assert proj is not None
        assert proj.active is True
        task = Tasks.query.first()
        assert task.task == "Task A"
        assert task.project_id == proj.project_id


def test_add_task_existing_project_used(client, app):
    # Pre-create a project with active=False
    proj = Projects(project_name="Repeat", active=False)
    db.session.add(proj)
    db.session.commit()

    response = client.post(
        "/add", data={"task": "Task X", "project": "Repeat", "status": "0"}
    )
    assert response.status_code == 302

    with app.app_context():
        refreshed = db.session.get(Projects, proj.project_id)
        task = Tasks.query.first()
        assert refreshed.active is True
        assert task.status is False
        assert task.task == "Task X"


# Test /close


def test_close_task_valid_toggle(client, create_task, app):
    task = create_task("Toggle me", status=True)
    response = client.get(f"/close/{task.task_id}")
    assert response.status_code == 302
    assert response.location.endswith("/")

    with app.app_context():
        updated = db.session.get(Tasks, task.task_id)
        assert updated.status is False  # Confirm toggle worked


def test_close_task_invalid_redirects(client):
    response = client.get("/close/9999")  # Non-existent task
    assert response.status_code == 302
    assert response.location.endswith("/")


def test_close_task_from_closed_to_open(client, create_task, app):
    task = create_task("Toggle back", status=False)  # Start closed
    response = client.get(f"/close/{task.task_id}")
    assert response.status_code == 302

    with app.app_context():
        refreshed = db.session.get(Tasks, task.task_id)
        assert refreshed.status is True


# Test /delete


def test_delete_task_invalid_id_redirects(client):
    response = client.get("/delete/9999")  # Should not exist
    assert response.status_code == 302
    assert response.location.endswith("/")


# Test /clear


def test_clear_all_removes_tasks_and_project(client, create_task, app):
    task = create_task("Clean me", status=True)
    project_id = task.project_id

    response = client.get(f"/clear/{project_id}")
    assert response.status_code == 302
    assert response.location.endswith("/")

    with app.app_context():
        assert Tasks.query.filter_by(project_id=project_id).count() == 0
        assert db.session.get(Projects, project_id) is None


def test_clear_all_on_nonexistent_project(client, app):
    response = client.get("/clear/9999")  # ID doesn't exist
    assert response.status_code == 302

    # Confirm nothing blows up and no rows were mistakenly touched
    with app.app_context():
        assert Tasks.query.count() == 0
        assert Projects.query.count() == 0


# Test /remove


def test_remove_all_deletes_tasks(client, create_task, app):
    task = create_task("Poof me", status=True)
    project_id = task.project_id

    response = client.get(f"/remove/{project_id}")
    assert response.status_code == 302
    assert response.location.endswith("/")

    with app.app_context():
        remaining = Tasks.query.filter_by(project_id=project_id).all()
        assert len(remaining) == 0


def test_remove_all_on_empty_project(client, create_project, app):
    project = create_project("Lonely", active=True)

    response = client.get(f"/remove/{project.project_id}")
    assert response.status_code == 302

    with app.app_context():
        assert Tasks.query.filter_by(project_id=project.project_id).count() == 0


# Test tab nav


def test_tab_nav_switches_active_project(client, create_project, app):
    # Create two projects, both initially inactive
    p1 = create_project("Alpha", active=False)
    p2 = create_project("Beta", active=False)

    response = client.get(f"/project/{p2.url_slug}")
    assert response.status_code == 302
    assert response.location.endswith("/")

    with app.app_context():
        refreshed_p1 = db.session.get(Projects, p1.project_id)
        refreshed_p2 = db.session.get(Projects, p2.project_id)

        assert refreshed_p1.active is False
        assert refreshed_p2.active is True


def test_tab_nav_with_nonexistent_tab(client, create_project, app):
    create_project("Gamma", active=True)  # existing active project

    response = client.get("/project/NoSuchTab")
    assert response.status_code == 302

    with app.app_context():
        active_count = Projects.query.filter_by(active=True).count()
        # All projects should now be inactive since nothing matched
        assert active_count == 0


# Test /rename_project


def test_rename_project_success(client, create_project, app):
    project = create_project("OldName", active=True)
    response = client.post(
        f"/rename_project/{project.project_id}", json={"new_name": "NewName"}
    )
    assert response.status_code == 204

    with app.app_context():
        refreshed = db.session.get(Projects, project.project_id)
        assert refreshed.project_name == "NewName"


def test_rename_project_missing_project(client):
    response = client.post("/rename_project/9999", json={"new_name": "Ghost"})
    assert response.status_code == 404
    assert b"Project not found" in response.data


def test_rename_project_blank_name(client, create_project):
    project = create_project("Name", active=True)
    response = client.post(
        f"/rename_project/{project.project_id}", json={"new_name": ""}
    )
    assert response.status_code == 400
    assert b"Invalid name" in response.data


# Test /rename_task_desc


def test_rename_task_desc_success(client, create_task, app):
    task = create_task("Old Desc", status=True)
    response = client.post(
        f"/rename_task_desc/{task.task_id}", json={"new_desc": "New Desc"}
    )
    assert response.status_code == 204

    with app.app_context():
        refreshed = db.session.get(Tasks, task.task_id)
        assert refreshed.task == "New Desc"


def test_rename_task_desc_not_found(client):
    response = client.post("/rename_task_desc/9999", json={"new_desc": "Ghost task"})
    assert response.status_code == 404
    assert b"Task not found" in response.data


def test_rename_task_desc_invalid_desc(client, create_task):
    task = create_task("Old", status=True)
    response = client.post(f"/rename_task_desc/{task.task_id}", json={"new_desc": ""})
    assert response.status_code == 400
    assert b"Invalid description" in response.data
