import os
import tempfile

import pytest

from task_manager import create_app, db
from task_manager.models import Projects, Tasks


@pytest.fixture(scope="session")
def app():
    db_fd, db_path = tempfile.mkstemp(suffix=".sqlite3")
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": f"sqlite:///{db_path}",
        }
    )

    with app.app_context():
        db.create_all()
        yield app

        db.session.remove()
        db.drop_all()
        engine = db.engine
        engine.dispose()

        # Explicitly close all connections in the pool
        if hasattr(engine.pool, "dispose"):
            engine.pool.dispose()

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def create_project():
    def _create_project(name="Test Project", active=True):
        project = Projects(project=name, active=active)
        db.session.add(project)
        db.session.commit()
        return project

    return _create_project


@pytest.fixture
def create_task(create_project):
    def _create_task(task_desc="Sample Task", status=True, project=None):
        if not project:
            project = create_project()
        task = Tasks(project_id=project.project_id, task=task_desc, status=status)
        db.session.add(task)
        db.session.commit()
        return task

    return _create_task
