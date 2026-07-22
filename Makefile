.DEFAULT_GOAL := help

.PHONY: help bootstrap format format-check lint typecheck unit integration check dev dev-infra dev-api dev-web dev-apps dev-down

help:
	@echo "bootstrap     Install locked Python and Node development dependencies"
	@echo "format        Format Python and TypeScript workspace files"
	@echo "format-check  Verify formatting without changing files"
	@echo "lint          Run Python and TypeScript linters"
	@echo "typecheck     Run Python and TypeScript type checking"
	@echo "unit          Run fixture-only unit tests"
	@echo "integration   Run fixture-only integration tests"
	@echo "check         Run all offline verification targets"
	@echo "dev           Start Postgres, Redis, API, and web development servers"
	@echo "dev-infra     Start local Postgres and Redis in the background"
	@echo "dev-api       Start the API development server"
	@echo "dev-web       Start the web development server"
	@echo "dev-apps      Start the API and web development servers"
	@echo "dev-down      Stop local Postgres and Redis"

bootstrap:
	uv sync --frozen
	npm ci

format:
	uv run --frozen ruff format services packages tests scripts/dev.py
	npm run format

format-check:
	uv run --frozen ruff format --check services packages tests scripts/dev.py
	npm run format:check

lint:
	uv run --frozen ruff check services packages tests scripts/dev.py
	npm run lint

typecheck:
	uv run --frozen mypy
	npm run typecheck

unit:
	uv run --frozen pytest -m "not integration"
	npm run test:unit

integration:
	uv run --frozen pytest -m integration
	npm run test:integration

check: format-check lint typecheck unit integration

dev:
	$(MAKE) dev-infra
	uv run --frozen python scripts/dev.py

dev-infra:
	docker compose --env-file .env.example -f infra/compose.yaml up -d --wait

dev-api:
	uv run --frozen uvicorn services.api.main:app --host "$${API_HOST:-127.0.0.1}" --port "$${API_PORT:-8000}" $${API_RELOAD:+--reload}

dev-web:
	npm run dev --workspace @tendy-spider/web

dev-apps:
	uv run --frozen python scripts/dev.py

dev-down:
	docker compose --env-file .env.example -f infra/compose.yaml down
