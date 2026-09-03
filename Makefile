.PHONY: help sync sync-dev dev prod test cov cov-html lint format reset clean

# Default target: show help
help:
	@echo ""
	@echo "Task Manager — Makefile Commands"
	@echo "--------------------------------"
	@echo "make sync        Install all project dependencies using uv"
	@echo "make sync-dev    Install dev dependencies (pytest, coverage)"
	@echo "make dev         Start Flask in development mode (debug + reload)"
	@echo "make prod        Start production server using gunicorn"
	@echo "make test        Run tests"
	@echo "make cov         Run tests with coverage (terminal report)"
	@echo "make cov-html    Run tests with coverage (HTML report)"
	@echo "make lint        Run black, isort, and mypy checks"
	@echo "make format      Auto-format code with black and isort"
	@echo "make reset       Clean environment and reinstall everything"
	@echo "make clean       Remove caches and artifacts"
	@echo ""

# Install all project dependencies
sync:
	uv sync

# Install dev dependencies (pytest, coverage, etc.)
sync-dev:
	uv sync --group dev

# Development server (debug + auto-reload)
dev:
	uv run flask --app task_manager.app run --debug --reload

# Production server (gunicorn)
prod:
	uv run gunicorn "task_manager.wsgi:app" --config gunicorn.conf.py

# Run tests
test:
	uv run pytest -x

# Coverage in terminal
cov:
	uv run pytest --cov=task_manager --cov-report=term-missing

# Coverage with HTML output
cov-html:
	uv run pytest --cov=task_manager --cov-report=html
	@echo "Open htmlcov/index.html in your browser to view the report."

# Linting: black, isort, mypy
lint:
	uv run black --check .
	uv run isort --check-only .
	uv run mypy .

# Auto-format code
format:
	uv run isort .
	uv run black .

# Reset environment completely
reset:
	rm -rf .venv
	uv sync
	uv sync --group dev

# Clean caches and artifacts
clean:
	find . -type d -name "__pycache__" -exec rm -r {} + || true
	find . -type f -name "*.pdf" -exec rm {} +
	rm -rf .pytest_cache .coverage htmlcov
	clear
