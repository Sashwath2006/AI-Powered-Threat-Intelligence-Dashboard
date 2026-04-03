@echo off
REM Docker commands for Windows - Threat Intelligence Dashboard
REM Usage: docker-dev.bat [command]

setlocal enabledelayedexpansion

if "%1"=="" (
    cls
    echo.
    echo   AI Threat Intelligence Dashboard - Docker Manager for Windows
    echo   ============================================================
    echo.
    echo   Usage: docker-dev.bat [command]
    echo.
    echo   Development:
    echo     build              Build Docker images
    echo     up                 Start containers (with hot reload^)
    echo     down               Stop containers
    echo     restart            Restart all containers
    echo     logs               View all logs
    echo     logs-backend       View backend logs only
    echo     logs-frontend      View frontend logs only
    echo.
    echo   Debugging:
    echo     shell-backend      Open PowerShell in backend container
    echo     shell-frontend     Open PowerShell in frontend container
    echo     ps                 Show running containers
    echo     stats              Show container resource usage
    echo.
    echo   Testing:
    echo     test               Run backend tests
    echo     test-integration   Run integration tests
    echo.
    echo   Production:
    echo     prod-build         Build production images
    echo     prod-up            Start production containers (no hot reload^)
    echo     prod-down          Stop production containers
    echo.
    echo   Cleanup:
    echo     clean              Remove containers and volumes
    echo     prune              Remove all unused Docker resources
    echo.
    goto end
)

if "%1"=="build" (
    docker compose build
    echo.
    echo [OK] Docker images built
    goto end
)

if "%1"=="up" (
    docker compose up -d
    echo.
    echo [OK] Services started
    echo Backend: http://localhost:8000/docs
    echo Frontend: http://localhost:8501
    goto end
)

if "%1"=="down" (
    docker compose down
    echo [OK] Services stopped
    goto end
)

if "%1"=="restart" (
    docker compose down
    docker compose up -d
    echo [OK] Services restarted
    echo Backend: http://localhost:8000/docs
    echo Frontend: http://localhost:8501
    goto end
)

if "%1"=="logs" (
    docker compose logs -f
    goto end
)

if "%1"=="logs-backend" (
    docker compose logs -f backend
    goto end
)

if "%1"=="logs-frontend" (
    docker compose logs -f frontend
    goto end
)

if "%1"=="shell-backend" (
    docker compose exec backend powershell
    goto end
)

if "%1"=="shell-frontend" (
    docker compose exec frontend powershell
    goto end
)

if "%1"=="ps" (
    docker compose ps
    goto end
)

if "%1"=="stats" (
    docker compose stats
    goto end
)

if "%1"=="test" (
    docker compose exec backend pytest tests/
    goto end
)

if "%1"=="test-integration" (
    docker compose exec backend python test_e2e_pipeline.py
    goto end
)

if "%1"=="prod-build" (
    docker compose -f docker-compose.yml -f docker-compose.prod.yml build
    echo [OK] Production images built
    goto end
)

if "%1"=="prod-up" (
    docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
    echo [OK] Production services started
    goto end
)

if "%1"=="prod-down" (
    docker compose -f docker-compose.yml -f docker-compose.prod.yml down
    echo [OK] Production services stopped
    goto end
)

if "%1"=="clean" (
    docker compose down -v --remove-orphans
    echo [OK] Containers and volumes removed
    goto end
)

if "%1"=="prune" (
    docker system prune -a --volumes --force
    echo [OK] All unused Docker resources removed
    goto end
)

echo Unknown command: %1
goto end

:end
endlocal
