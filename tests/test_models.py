def test_project_model_repr(app, make_project):
    project = make_project(name="Alchemy", active=True)
    with app.app_context():
        assert repr(project) == f"<Project {project.project_name}>"


def test_task_model_repr(app, make_task):
    task = make_task(task_desc="Test Task")
    with app.app_context():
        assert repr(task) == f"<Task {task.task}>"
