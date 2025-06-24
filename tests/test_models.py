def test_task_model_repr(app, make_task):
    task = make_task(task_desc="Test Task")
    with app.app_context():
        assert repr(task) == f"<Task {task.task}>"
