.PHONY: lint format test ci precommit-install precommit-run

typecheck:
	@echo "Typechecking"
	@uv run ty check .

lint:
	@echo "Linting with Ruff..."
	@uv run ruff check .

format:
	@echo "Formatting with Ruff..."
	@uv run ruff format .

test:
	@echo "Running tests..."
	@uv run pytest .

ci: lint format typecheck test

precommit-install:
	@echo "Installing pre-commit hooks..."
	@uv run pre-commit install

precommit-run:
	@echo "Running pre-commit..."
	@uv run pre-commit run --all-files

publish:
	@echo "Publishing to PyPI..."
	@poetry publish --build --username __token__ --password $PYPI_TOKEN
