.PHONY: help sync sync-dev dev prod test cov cov-html lint format reset clean

# Default target: show help
help:
	@echo ""
	@echo "Task Manager — Makefile Commands"
	@echo "--------------------------------"
	@echo "make dev         Run Flask development server"
	@echo "make prod        Run Gunicorn production server"
	@echo "make test        Run tests"
	@echo "make clean       Remove caches and artifacts"
	@echo "make reset       Rebuild environment"
	@echo ""

# Install all project dependencies
sync:
	uv sync

# Install dev dependencies (pytest, coverage, etc.)
sync-dev:
	uv sync --group dev

# Ensure uv.lock matches pyproject.toml
lockcheck:
	@echo "Checking lockfile consistency..."
	@uv lock --check || (echo "❌ uv.lock is out of date. Run: uv lock"; exit 1)
	@echo "✔ uv.lock is up to date."

# Development server (debug + auto-reload)
dev: lockcheck
	uv run flask --app task_manager.app run --debug --reload

# Production server (gunicorn)
prod: lockcheck
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
