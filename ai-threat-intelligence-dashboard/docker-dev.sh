#!/bin/bash

# Docker commands for Linux/macOS - Threat Intelligence Dashboard
# Usage: ./docker-dev.sh [command]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

show_help() {
    clear
    echo ""
    echo "  AI Threat Intelligence Dashboard - Docker Manager"
    echo "  =================================================="
    echo ""
    echo "  Usage: ./docker-dev.sh [command]"
    echo ""
    echo "  Development:"
    echo "    build              Build Docker images"
    echo "    up                 Start containers (with hot reload)"
    echo "    down               Stop containers"
    echo "    restart            Restart all containers"
    echo "    logs               View all logs"
    echo "    logs-backend       View backend logs only"
    echo "    logs-frontend      View frontend logs only"
    echo ""
    echo "  Debugging:"
    echo "    shell-backend      Open bash shell in backend container"
    echo "    shell-frontend     Open bash shell in frontend container"
    echo "    ps                 Show running containers"
    echo "    stats              Show container resource usage"
    echo ""
    echo "  Testing:"
    echo "    test               Run backend tests"
    echo "    test-integration   Run integration tests"
    echo ""
    echo "  Production:"
    echo "    prod-build         Build production images"
    echo "    prod-up            Start production containers (no hot reload)"
    echo "    prod-down          Stop production containers"
    echo ""
    echo "  Cleanup:"
    echo "    clean              Remove containers and volumes"
    echo "    prune              Remove all unused Docker resources"
    echo ""
}

success() {
    echo -e "${GREEN}✓ $1${NC}"
}

error() {
    echo -e "${RED}✗ $1${NC}"
}

info() {
    echo -e "${YELLOW}ℹ $1${NC}"
}

case "${1:-}" in
    build)
        docker compose build
        success "Docker images built"
        ;;
    up)
        docker compose up -d
        success "Services started"
        info "Backend: http://localhost:8000/docs"
        info "Frontend: http://localhost:8501"
        ;;
    down)
        docker compose down
        success "Services stopped"
        ;;
    restart)
        docker compose down
        docker compose up -d
        success "Services restarted"
        info "Backend: http://localhost:8000/docs"
        info "Frontend: http://localhost:8501"
        ;;
    logs)
        docker compose logs -f
        ;;
    logs-backend)
        docker compose logs -f backend
        ;;
    logs-frontend)
        docker compose logs -f frontend
        ;;
    shell-backend)
        docker compose exec backend /bin/bash
        ;;
    shell-frontend)
        docker compose exec frontend /bin/bash
        ;;
    ps)
        docker compose ps
        ;;
    stats)
        docker compose stats
        ;;
    test)
        docker compose exec backend pytest tests/
        ;;
    test-integration)
        docker compose exec backend python test_e2e_pipeline.py
        ;;
    prod-build)
        docker compose -f docker-compose.yml -f docker-compose.prod.yml build
        success "Production images built"
        ;;
    prod-up)
        docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
        success "Production services started"
        ;;
    prod-down)
        docker compose -f docker-compose.yml -f docker-compose.prod.yml down
        success "Production services stopped"
        ;;
    clean)
        docker compose down -v --remove-orphans
        success "Containers and volumes removed"
        ;;
    prune)
        docker system prune -a --volumes --force
        success "All unused Docker resources removed"
        ;;
    "")
        show_help
        ;;
    *)
        error "Unknown command: $1"
        echo ""
        show_help
        exit 1
        ;;
esac
