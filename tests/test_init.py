import pytest
from task_manager import create_app


def test_runtime_error_when_testing_uses_production_db():
    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///ctm.db",
    }

    with pytest.raises(RuntimeError) as excinfo:
        create_app(test_config)

    assert "Refusing to run tests against production database" in str(excinfo.value)


def test_runtime_error_when_testing_uses_dev_db():
    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///dev.db",
    }

    with pytest.raises(RuntimeError):
        create_app(test_config)
