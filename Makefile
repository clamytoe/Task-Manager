.PHONY: test cov cov-html clean

test:
	pytest -x

cov:
	pytest --cov=task_manager --cov-report=term-missing

cov-html:
	pytest --cov=task_manager --cov-report=html
	@echo "Open htmlcov/index.html in your browser to view the report."

clean:
	find . -type d -name "__pycache__" -exec rm -r {} + || true
	rm -rf .pytest_cache .coverage htmlcov
