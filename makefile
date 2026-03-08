.PHONY: lint format test ci

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

publish:
	@echo "Publishing to PyPI..."
	@poetry publish --build --username __token__ --password $PYPI_TOKEN