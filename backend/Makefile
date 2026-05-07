SHELL := /usr/bin/env bash

COMPOSE := docker compose --env-file ../.env
BACKEND_COMPOSE := $(COMPOSE) -f ../compose.backend.yml
FRONTEND_COMPOSE := $(COMPOSE) -f ../compose.frontend.yml
STACK_COMPOSE := $(COMPOSE) -f ../compose.backend.yml -f ../compose.frontend.yml
PYTEST_ARGS ?=

.PHONY: help
help:
	@printf "Targets:\n"
	@printf "  make up                 Start backend + frontend with build in detached mode\n"
	@printf "  make up-backend         Start backend stack only\n"
	@printf "  make up-frontend        Start frontend only\n"
	@printf "  make down               Stop stack and remove volumes\n"
	@printf "  make build              Build backend + frontend images\n"
	@printf "  make logs               Follow stack logs\n"
	@printf "  make logs-backend       Follow backend logs\n"
	@printf "  make shell              Open bash in backend container\n"
	@printf "  make test               Run backend tests in the backend container\n"
	@printf "  make test-fresh         Recreate backend stack, then run tests\n"
	@printf "  make db-clean           Drop DB schema, migrate, and seed initial data\n"
	@printf "  make db-reset           Recreate backend stack and DB volume\n"
	@printf "  make prune              Run docker system prune -a\n"
	@printf "  make prune-volumes      Run docker volume prune\n"
	@printf "  make prune-images       Run docker image prune -a\n"
	@printf "  make prune-all          Run docker system prune -a --volumes\n"

.PHONY: up
up:
	$(STACK_COMPOSE) up --build -d

.PHONY: up-backend
up-backend:
	$(BACKEND_COMPOSE) up --build -d

.PHONY: up-frontend
up-frontend:
	$(FRONTEND_COMPOSE) up --build -d

.PHONY: build
build:
	$(STACK_COMPOSE) build

.PHONY: down
down:
	$(STACK_COMPOSE) down -v --remove-orphans

.PHONY: logs
logs:
	$(STACK_COMPOSE) logs -f

.PHONY: logs-backend
logs-backend:
	$(BACKEND_COMPOSE) logs -f backend

.PHONY: shell
shell:
	$(BACKEND_COMPOSE) exec backend bash

.PHONY: test
test:
	$(BACKEND_COMPOSE) exec -T backend bash scripts/tests-start.sh $(PYTEST_ARGS)

.PHONY: test-fresh
test-fresh:
	$(BACKEND_COMPOSE) down -v --remove-orphans
	$(BACKEND_COMPOSE) up --build -d
	$(BACKEND_COMPOSE) exec -T backend bash scripts/tests-start.sh $(PYTEST_ARGS)

.PHONY: db-clean
db-clean:
	$(BACKEND_COMPOSE) exec -T db sh -c 'psql -U "$$POSTGRES_USER" -d "$$POSTGRES_DB" -c "DROP SCHEMA IF EXISTS public CASCADE; CREATE SCHEMA public;"'
	$(BACKEND_COMPOSE) exec -T backend alembic upgrade head
	$(BACKEND_COMPOSE) exec -T backend python app/initial_data.py

.PHONY: db-reset
db-reset:
	$(BACKEND_COMPOSE) down -v --remove-orphans
	$(BACKEND_COMPOSE) up --build -d

.PHONY: db-migrate
db-migrate:
	$(BACKEND_COMPOSE) exec -T backend alembic upgrade head

.PHONY: db-seed
db-seed:
	$(BACKEND_COMPOSE) exec -T backend python app/initial_data.py

.PHONY: db-shell
db-shell:
	$(BACKEND_COMPOSE) exec db sh -c 'psql -U "$$POSTGRES_USER" -d "$$POSTGRES_DB"'

.PHONY: prune
prune:
	docker system prune -a

.PHONY: prune-volumes
prune-volumes:
	docker volume prune

.PHONY: prune-images
prune-images:
	docker image prune -a

.PHONY: prune-all
prune-all:
	docker system prune -a --volumes
