# Docker Setup & Deployment Guide

## Overview

This project is fully containerized with Docker and Docker Compose. Both the FastAPI backend and Streamlit frontend run in separate containers, communicating over a custom bridge network.

**Stack:**
- Backend: Python 3.12 + FastAPI + scikit-learn (Port 8000)
- Frontend: Python 3.12 + Streamlit (Port 8501)
- Orchestration: Docker Compose 3.8
- Network: Custom bridge network `ai-threat-intelligence-network`

---

## Prerequisites

### System Requirements
- Docker 20.10+ ([Install](https://docs.docker.com/get-docker/))
- Docker Compose 2.0+ (included with Docker Desktop)
- 4GB RAM minimum
- 2GB disk space

### Verify Installation
```bash
docker --version
docker compose version
```

---

## Project Structure

```
ai-threat-intelligence-dashboard/
├── docker-compose.yml          # Container orchestration
├── .dockerignore                # Files to exclude from build context
├── backend/
│   ├── Dockerfile              # Backend image definition
│   ├── requirements.txt         # Python dependencies
│   └── app/
│       ├── main.py            # FastAPI entry point
│       └── ... (ML, API routes, etc.)
├── frontend/
│   ├── Dockerfile              # Frontend image definition
│   ├── requirements.txt         # Python dependencies
│   └── app.py                  # Streamlit entry point
└── ml/                          # Shared ML models
```

---

## Quick Start

### 1. Build & Start Containers

```bash
# Navigate to project root
cd ai-threat-intelligence-dashboard

# Build and start services
docker compose up --build

# (Omit --build if images already exist)
docker compose up
```

### 2. Verify Services Running

```bash
# Check running containers
docker compose ps

# Expected output:
# NAME                      STATUS      PORTS
# threat-intel-backend      Up 30s      0.0.0.0:8000->8000/tcp
# threat-intel-frontend     Up 25s      0.0.0.0:8501->8501/tcp
```

### 3. Access Applications

- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs (Swagger UI)
- **Frontend Dashboard:** http://localhost:8501

### 4. Stop Services

```bash
# Stop containers (persists volumes)
docker compose down

# Stop and remove volumes
docker compose down -v

# Stop and remove all (containers, volumes, networks)
docker compose down -v --remove-orphans
```

---

## Common Commands

### View Logs

```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f backend
docker compose logs -f frontend

# Last 100 lines
docker compose logs --tail 100 backend
```

### Execute Commands in Containers

```bash
# Backend: Run Python command
docker compose exec backend python -c "import pandas; print(pandas.__version__)"

# Frontend: Check Streamlit config
docker compose exec frontend streamlit config show

# Backend: Run tests
docker compose exec backend pytest tests/
```

### Access Container Shell

```bash
# Backend shell
docker compose exec backend /bin/bash

# Frontend shell
docker compose exec frontend /bin/bash

# Exit shell
exit
```

### Rebuild Images

```bash
# Rebuild all images (after code changes)
docker compose build

# Rebuild specific service
docker compose build backend
docker compose build frontend

# Force full rebuild (no cache)
docker compose build --no-cache
```

### View Image Details

```bash
# List local images
docker images | grep threat-intel

# Image size
docker images --format "table {{.Repository}}\t{{.Size}}" | grep threat-intel
```

---

## Docker Architecture

### Dockerfiles

#### Backend (`backend/Dockerfile`)
- **Base:** Python 3.12-slim (optimized for size)
- **Multi-stage:** Builder stage compiles deps, runtime stage stays minimal
- **User:** Non-root user `appuser` (security best practice)
- **Health Check:** Curl to `/docs` endpoint every 30 seconds
- **Startup:** Uvicorn server binding to 0.0.0.0:8000

#### Frontend (`frontend/Dockerfile`)
- **Base:** Python 3.12-slim
- **User:** Non-root user `appuser`
- **Health Check:** Curl to root endpoint every 30 seconds
- **Startup:** Streamlit server binding to 0.0.0.0:8501

### docker-compose.yml

**Key Features:**
1. **Named Containers:** `threat-intel-backend`, `threat-intel-frontend`
2. **Custom Network:** `ai-threat-intelligence-network` (bridge)
3. **Service Dependencies:** Frontend waits for backend's health check
4. **Volume Mounts:** Live code reloading for development
5. **Health Checks:** Automated container restart if unhealthy
6. **Restart Policy:** `unless-stopped` (auto-restart on failure)
7. **Environment Variables:** Backend URL for inter-service communication

### Network Communication

```
Frontend Container (8501)
        ↓
  ai-threat-intelligence-network
        ↓
Backend Container (8000)
        ↓
    ML Models (sklearn)
```

Services communicate via container name (`backend`, `frontend`) not localhost:
- Frontend calls: `http://backend:8000/api/analyze` (not `localhost:8000`)
- Backend serves on: `0.0.0.0:8000` (all interfaces)

---

## Environment Variables

### Backend (Automatic)
```env
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
PYTHONUNBUFFERED=1          # Real-time log output
PYTHONDONTWRITEBYTECODE=1   # No .pyc files (smaller images)
```

### Frontend (Automatic)
```env
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
BACKEND_URL=http://backend:8000
PYTHONUNBUFFERED=1
PYTHONDONTWRITEBYTECODE=1
```

### Custom .env File (Optional)

Create `.env` in project root (not committed):
```env
# Override docker-compose variables
COMPOSE_PROJECT_NAME=threat-intel
LOG_LEVEL=info
```

---

## Development Workflow

### Local Development (Without Docker)

```bash
# Terminal 1: Backend
cd backend
python -m uvicorn app.main:app --reload

# Terminal 2: Frontend
cd frontend
streamlit run app.py --server.port 8501
```

### Development with Docker (Live Reload)

```bash
# Start with build
docker compose up --build

# Edit files locally, containers auto-reload:
# - Backend: Uvicorn hot-reloads on code change
# - Frontend: Streamlit reruns on file change
```

### Production Build (No Reload)

For deployment, remove `volumes` and use `--detach`:
```bash
docker compose up -d
```

---

## Image Size Optimization

### Current Sizes (Estimated)
- Backend: ~800 MB (Python 3.12 + FastAPI + scikit-learn)
- Frontend: ~600 MB (Python 3.12 + Streamlit)
- **Total:** ~1.4 GB on disk

### Optimization Techniques Used
1. **Multi-stage Build (Backend):** Dev dependencies only in builder stage
2. **Slim Base Image:** `python:3.12-slim` instead of full `ubuntu`
3. **Prebuilt Wheels:** All packages have binary wheels (no C compilation)
4. `.dockerignore:** Excludes unnecessary files from build context

### Further Optimization (Optional)
```dockerfile
# For even smaller images, use distroless (no shell):
FROM gcr.io/distroless/python3.12
```

---

## Troubleshooting

### Issue: Port Already in Use

```bash
# Find what's running on port 8000
lsof -i :8000  # macOS/Linux
Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess  # Windows

# Change ports in docker-compose.yml
# Change "8000:8000" to "8001:8000" for backend
# Change "8501:8501" to "8502:8501" for frontend
```

### Issue: Backend Unhealthy (Health Check Fails)

```bash
# Check logs
docker compose logs backend

# Common fixes:
# 1. App crashed - check logs for errors
# 2. Slow startup - increase start_period in docker-compose.yml
# 3. Port binding failed - change port mapping

# Manual health check
docker compose exec backend curl http://localhost:8000/docs
```

### Issue: Frontend Can't Connect to Backend

```bash
# Verify network connectivity
docker compose exec frontend curl http://backend:8000/docs

# Common fixes:
# 1. Backend not healthy - check backend logs
# 2. BACKEND_URL wrong - should be http://backend:8000
# 3. Firewall blocking - check Docker CE network settings

# Debug address resolution
docker compose exec frontend nslookup backend
```

### Issue: High Memory Usage

```bash
# Check container resource usage
docker compose stats

# Limit resources in docker-compose.yml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 512M
```

### Issue: No Space Left on Device

```bash
# Clean up dangling images/containers
docker system prune -a

# Remove all containers and rebuild
docker compose down -v
docker compose build --no-cache
```

---

## Production Deployment

### Docker Hub Registry

1. **Tag Image:**
```bash
docker tag threat-intel-backend:latest yourusername/threat-intel-backend:1.0.0
docker tag threat-intel-frontend:latest yourusername/threat-intel-frontend:1.0.0
```

2. **Push to Registry:**
```bash
docker login
docker push yourusername/threat-intel-backend:1.0.0
docker push yourusername/threat-intel-frontend:1.0.0
```

3. **Pull on Deployment Server:**
```bash
docker pull yourusername/threat-intel-backend:1.0.0
docker pull yourusername/threat-intel-frontend:1.0.0
```

### Kubernetes Deployment

See `kubernetes-deployment.yml` (optional) for Kubernetes setup.

### SSL/HTTPS

Add reverse proxy (nginx) in docker-compose.yml:
```yaml
nginx:
  image: nginx:1.25-alpine
  ports:
    - "443:443"
  volumes:
    - ./nginx.conf:/etc/nginx/nginx.conf
    - ./certs:/etc/nginx/certs
```

---

## Testing

### Unit Tests (Backend)

```bash
# Run all tests
docker compose exec backend pytest

# Run specific test file
docker compose exec backend pytest tests/test_backend.py

# With coverage
docker compose exec backend pytest --cov=app tests/
```

### Integration Tests

```bash
# Test end-to-end pipeline
docker compose exec backend python test_e2e_pipeline.py
```

### Load Testing

```bash
# Using Apache Bench
docker compose exec backend ab -n 100 -c 10 http://localhost:8000/docs

# Using wrk
docker run --rm --network ai-threat-intelligence-network \
  -v /path/to/script.lua:/script.lua \
  williamyeh/wrk -c 100 -d 30s http://backend:8000
```

---

## Monitoring & Logging

### View Logs

```bash
# Real-time logs all services
docker compose logs -f

# Format: container-name | timestamp | message
# Colors: different for each service
```

### Log File Extraction

```bash
# Export backend logs
docker compose logs backend > backend.log

# Export all logs
docker compose logs > all-services.log

# Export JSON format
docker compose logs --no-color > logs.json
```

### Persistent Logging

For production, configure log drivers in docker-compose.yml:
```yaml
services:
  backend:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

---

## Performance Tips

1. **Resource Allocation:** Assign sufficient RAM to Docker daemon (4GB+)
2. **Network:** Direct container-to-container via docker network is fast
3. **Volume Performance:** Use named volumes instead of bind mounts for large datasets
4. **Caching:** Leverage Docker layer caching - keep stable dependencies early
5. **Monitoring:** Use `docker compose stats` to profile resource usage

---

## Security Best Practices

✅ **Already Implemented:**
- Non-root user (`appuser:1000`) in containers
- Health checks to auto-recover failed services
- Python buffers disabled for real-time logs
- No compilation in runtime image (supply-chain security)

✅ **Additional Recommendations:**
- Use `.env` for secrets, never commit to Git
- Scan images: `docker scan threat-intel-backend`
- Keep base images updated: `python:3.12-slim`
- Use networks to isolate services
- Enable Docker Content Trust for image verification

---

## Useful References

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Specification](https://compose-spec.io/)
- [Python Docker Best Practices](https://docs.docker.com/language/python/)
- [FastAPI in Containers](https://fastapi.tiangolo.com/deployment/docker/)
- [Streamlit with Docker](https://docs.streamlit.io/knowledge-base/tutorials/deploy/docker)

---

## Next Steps

1. **Test Locally:** `docker compose up --build`
2. **Verify Access:**
   - Backend: http://localhost:8000/docs
   - Frontend: http://localhost:8501
3. **Test Sample Data:** Use "Use Sample Data" button in dashboard
4. **Deploy:** Follow production deployment section above

