test-integration:
	uv run pytest tests/integration -m integration -v

test:
	uv run pytest

lint:
	uv run ruff check src/ tests/
	uv run ruff format --check src/ tests/

typecheck:
	uv run mypy src/

check: lint typecheck test