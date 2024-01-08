.PHONY: build run lint test format check clean

build:
	@echo "Building the project with Poetry"
	@poetry install

run:
	@echo "Running the FastAPI app with Uvicorn"
	@poetry run uvicorn apps.app:app --host 0.0.0.0 --port 8000 --workers 4 --timeout-keep-alive 600

test:
	@echo "Running tests with Coverage - Pytest"
	@poetry run coverage run -m pytest && poetry run coverage report -m
	@poetry run coverage xml -o coverage.xml

format:
	@echo "Formatting code with Black"
	@poetry run black .
	@poetry run isort .

check:
	@echo "Running code formatting check with Black"
	@poetry run mypy .
	@poetry run black --check .

clean:
	@echo "Cleaning up generated files"
	@poetry run rm -rf __pycache__ .pytest_cache .coverage
