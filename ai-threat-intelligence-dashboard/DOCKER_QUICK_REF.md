# Docker Quick Reference

## 🚀 Quick Start (30 seconds)

```bash
# Clone & enter project
git clone https://github.com/Sashwath2006/AI-Powered-Threat-Intelligence-Dashboard
cd AI-Powered-Threat-Intelligence-Dashboard

# Start services
docker compose up --build

# Access dashboard
# Backend API: http://localhost:8000/docs
# Frontend: http://localhost:8501
```

---

## 📋 Essential Commands

| Task | Command |
|------|---------|
| **Build images** | `docker compose build` |
| **Start services** | `docker compose up -d` |
| **Stop services** | `docker compose down` |
| **View logs** | `docker compose logs -f` |
| **Backend shell** | `docker compose exec backend bash` |
| **Frontend shell** | `docker compose exec frontend bash` |
| **Run tests** | `docker compose exec backend pytest` |
| **Clean everything** | `docker compose down -v` |

---

## 🖥️ Windows Users

**Option 1: Batch Script**
```batch
docker-dev.bat up          # Start
docker-dev.bat logs        # View logs
docker-dev.bat shell-backend  # Shell
docker-dev.bat clean       # Stop & cleanup
```

**Option 2: PowerShell (Direct Docker)**
```powershell
docker compose up -d
docker compose logs -f
```

---

## 🐧 Linux/macOS Users

**Option 1: Bash Script**
```bash
chmod +x docker-dev.sh     # Make executable (first time only)
./docker-dev.sh up         # Start
./docker-dev.sh logs       # View logs
./docker-dev.sh shell-backend  # Shell
```

**Option 2: Make Commands**
```bash
make up                    # Start
make logs                  # View logs
make shell-backend         # Shell
make clean                 # Stop & cleanup
```

---

## 🔍 Verify Services Running

```bash
# Check container status
docker compose ps

# Expected:
# NAME                 STATUS        PORTS
# threat-intel-backend     Up       8000/tcp
# threat-intel-frontend    Up       8501/tcp
```

---

## 🧪 Testing

```bash
# Run all tests
docker compose exec backend pytest

# Run specific test
docker compose exec backend pytest tests/test_backend.py::TestAnomalyDetector

# Integration test
docker compose exec backend python test_e2e_pipeline.py

# With coverage
docker compose exec backend pytest --cov=app
```

---

## 🐛 Debugging

| Issue | Solution |
|-------|----------|
| **Port 8000 in use** | `docker-dev.bat down` or change port in docker-compose.yml |
| **Can't connect to backend** | `docker compose logs backend` to check errors |
| **Services not starting** | `docker compose down -v && docker compose up --build` |
| **High memory usage** | `docker stats` to monitor, reduce container limits |

---

## 📦 Production Deployment

```bash
# Use production compose override (no hot reload)
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# Or use helper script
docker-dev.bat prod-up     # Windows
./docker-dev.sh prod-up    # Linux/macOS
```

---

## 📊 Container Stats

```bash
# Real-time resource usage
docker compose stats

# Example output:
# CONTAINER                CPU %     MEM USAGE / LIMIT
# threat-intel-backend     0.05%     250MiB / 1GiB
# threat-intel-frontend    0.02%     180MiB / 512MiB
```

---

## 🔐 Security Notes

✅ Non-root user (`appuser:1000`) running both services  
✅ Health checks auto-restart failed containers  
✅ Network isolation between services  
✅ Python buffers disabled for security logging  

---

## 📁 Key Files

```
.dockerignore               - Files to exclude from build
docker-compose.yml         - Main orchestration (development)
docker-compose.prod.yml    - Production overrides
backend/Dockerfile         - Backend image definition
frontend/Dockerfile        - Frontend image definition
Makefile                   - Linux/macOS commands
docker-dev.bat            - Windows commands
docker-dev.sh             - Bash script for Linux/macOS
```

---

## 🌐 Service URLs

| Service | URL | Purpose |
|---------|-----|---------|
| Backend API | `http://localhost:8000` | REST API |
| Backend Docs | `http://localhost:8000/docs` | Swagger UI |
| Backend Health | `http://localhost:8000/health` | Health check |
| Frontend | `http://localhost:8501` | Streamlit dashboard |

---

## 📚 More Information

See [DOCKER_SETUP.md](DOCKER_SETUP.md) for comprehensive guide:
- Architecture details
- Network configuration
- Volume management
- Logging & monitoring
- Performance optimization
- Troubleshooting guide
