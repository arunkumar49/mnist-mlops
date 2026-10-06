.RECIPEPREFIX = >
.DEFAULT_GOAL := help
.PHONY: help install format lint typecheck contracts test check pre-commit

help: ## Show available commands
> @grep -E '^[a-z-]+:.*## ' Makefile | awk -F':.*## ' '{printf "  %-11s %s\n", $$1, $$2}'

install: ## Create .venv from uv.lock and install git hooks
> uv sync --locked
> uv run pre-commit install

format: ## Auto-format code and auto-fix lint issues
> uv run ruff format .
> uv run ruff check --fix .

lint: ## Check style and likely bugs (changes nothing)
> uv run ruff check .
> uv run ruff format --check .

typecheck: ## Strict type checking
> uv run mypy

contracts: ## Check the clean-architecture layer rules
> uv run lint-imports

test: ## Run tests with coverage (fails under 90%)
> uv run pytest

check: lint typecheck contracts test ## Run everything CI runs on Python code

pre-commit: ## Run every pre-commit hook on all files
> uv run pre-commit run --all-files
