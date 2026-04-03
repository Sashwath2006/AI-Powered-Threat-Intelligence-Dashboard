.PHONY: help build up down logs clean restart test shell-backend shell-frontend

help:
	@echo "AI Threat Intelligence Dashboard - Docker Commands"
	@echo ""
	@echo "Development Commands:"
	@echo "  make build              Build Docker images"
	@echo "  make up                 Start containers (with live reload)"
	@echo "  make down               Stop containers"
	@echo "  make restart            Restart containers"
	@echo "  make logs               View logs from all services"
	@echo "  make logs-backend       View backend logs only"
	@echo "  make logs-frontend      View frontend logs only"
	@echo ""
	@echo "Debugging Commands:"
	@echo "  make shell-backend      Open bash shell in backend container"
	@echo "  make shell-frontend     Open bash shell in frontend container"
	@echo "  make ps                 Show running containers"
	@echo "  make stats              Show container resource usage"
	@echo ""
	@echo "Testing Commands:"
	@echo "  make test               Run backend tests"
	@echo "  make test-integration   Run integration tests"
	@echo ""
	@echo "Production Commands:"
	@echo "  make prod-build         Build production images"
	@echo "  make prod-up            Start production containers (no reload)"
	@echo "  make prod-down          Stop production containers"
	@echo ""
	@echo "Cleanup Commands:"
	@echo "  make clean              Remove containers and volumes"
	@echo "  make prune              Remove all unused Docker resources"
	@echo ""

# Development builds and runs
build:
	docker compose build

up:
	docker compose up -d
	@echo "✓ Services started"
	@echo "  Backend: http://localhost:8000/docs"
	@echo "  Frontend: http://localhost:8501"

down:
	docker compose down

restart: down up
	@echo "✓ Services restarted"

logs:
	docker compose logs -f

logs-backend:
	docker compose logs -f backend

logs-frontend:
	docker compose logs -f frontend

# Debugging
shell-backend:
	docker compose exec backend /bin/bash

shell-frontend:
	docker compose exec frontend /bin/bash

ps:
	docker compose ps

stats:
	docker compose stats

# Testing
test:
	docker compose exec backend pytest tests/

test-integration:
	docker compose exec backend python test_e2e_pipeline.py

# Production
prod-build:
	docker compose -f docker-compose.yml -f docker-compose.prod.yml build

prod-up:
	docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
	@echo "✓ Production services started (no hot reload)"

prod-down:
	docker compose -f docker-compose.yml -f docker-compose.prod.yml down

# Cleanup
clean:
	docker compose down -v --remove-orphans
	@echo "✓ Containers and volumes removed"

prune:
	docker system prune -a --volumes
	@echo "✓ All unused Docker resources removed"

# Quick checks
check-health:
	@echo "Backend health: " && \
	docker compose exec -T backend curl -s http://localhost:8000/docs > /dev/null && echo "✓ Healthy" || echo "✗ Unhealthy"
	@echo "Frontend health: " && \
	docker compose exec -T frontend curl -s http://localhost:8501 > /dev/null && echo "✓ Healthy" || echo "✗ Unhealthy"

# Build info
info:
	@echo "=== Backend Image ===" && \
	docker images | grep threat-intel-backend || echo "Not built" && \
	echo "" && \
	echo "=== Frontend Image ===" && \
	docker images | grep threat-intel-frontend || echo "Not built"
