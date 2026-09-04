.PHONY: help dev test lint format clean

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

dev: ## Start development servers
	docker compose up

dev-build: ## Build and start development servers
	docker compose up --build

prod: ## Start production servers
	docker compose -f docker-compose.prod.yml up -d

test: test-backend test-frontend ## Run all tests

test-backend: ## Run backend tests
	cd backend && pytest --cov=app

test-frontend: ## Run frontend tests
	cd frontend && npm run test:coverage

lint: lint-backend lint-frontend ## Run all linters

lint-backend: ## Lint backend code
	cd backend && ruff check . && mypy app/

lint-frontend: ## Lint frontend code
	cd frontend && npm run lint

format: format-backend format-frontend ## Format all code

format-backend: ## Format backend code
	cd backend && black . && ruff check --fix .

format-frontend: ## Format frontend code
	cd frontend && npm run lint -- --fix

clean: ## Clean up
	docker compose down -v
	rm -rf backend/__pycache__ frontend/.next frontend/node_modules

db-migrate: ## Run database migrations
	cd backend && alembic upgrade head

db-downgrade: ## Downgrade database
	cd backend && alembic downgrade -1
