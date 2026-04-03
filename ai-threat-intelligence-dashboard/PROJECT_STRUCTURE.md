# Project Structure Reference

## Complete File Tree

```
ai-threat-intelligence-dashboard/
│
├── 📄 README.md                          ← Start here!
├── 📄 ARCHITECTURE.md                    ← System design
├── 📄 DEVELOPMENT.md                     ← Development guide
├── 📄 docker-compose.yml                 ← Docker orchestration
├── 📄 .env                               ← Environment variables
├── 📄 .gitignore                         ← Git ignore rules
│
├── 📁 backend/                           ← FastAPI Backend
│   ├── 📁 app/                           ← Main application
│   │   ├── 📄 __init__.py
│   │   ├── 📄 main.py                   ← PHASE 2: FastAPI factory
│   │   ├── 📄 config.py                 ← Settings & config ✅
│   │   │
│   │   ├── 📁 api/
│   │   │   ├── 📄 __init__.py
│   │   │   └── 📄 routes.py             ← PHASE 2: API endpoints
│   │   │
│   │   ├── 📁 ml/
│   │   │   ├── 📄 __init__.py
│   │   │   └── 📄 anomaly_detector.py   ← PHASE 3: ML model
│   │   │
│   │   ├── 📁 models/
│   │   │   ├── 📄 __init__.py
│   │   │   └── 📄 schemas.py            ← PHASE 2: Pydantic models
│   │   │
│   │   └── 📁 utils/
│   │       ├── 📄 __init__.py
│   │       └── 📄 logger.py             ← Logging utility
│   │
│   ├── 📁 tests/                        ← Unit tests
│   ├── 📄 requirements.txt               ← Dependencies ✅
│   ├── 📄 Dockerfile                    ← Docker image ✅
│   └── 📄 .dockerignore
│
├── 📁 frontend/                         ← Streamlit Frontend
│   ├── 📄 app.py                        ← PHASE 5: Main dashboard
│   ├── 📄 requirements.txt               ← Dependencies ✅
│   ├── 📁 pages/                        ← PHASE 5: Multi-page views
│   ├── 📁 components/                   ← PHASE 5: Reusable UI
│   ├── 📄 Dockerfile                    ← Docker image ✅
│   └── 📄 .dockerignore
│
└── 📁 ml/                               ← ML Models & Data
    ├── 📁 models/                       ← PHASE 3-4: Trained models
    └── 📁 data/                         ← PHASE 3: Training data
        └── 📄 sample_logs.csv           ← PHASE 3: Sample dataset
```

## Phase Completion Status

### ✅ Phase 1: COMPLETE
- [x] Directory structure created
- [x] Configuration files set up
- [x] Docker configuration ready
- [x] Documentation prepared
- [x] .env template created
- [x] Requirements files prepared

### ✅ Phase 2: COMPLETE
- [x] FastAPI application factory (`app/main.py`)
- [x] API route handlers (`api/routes.py`)
- [x] Request/response validation (`models/schemas.py`)
- [x] Error handling and logging
- [x] Isolation Forest anomaly detector
- [x] Unit tests with pytest
- [x] API documentation (Swagger/ReDoc)
- **Documentation:** [Phase 2 Summary](PHASE2_COMPLETE.md) | [Quick Reference](PHASE2_QUICKREF.md)

### ✅ Phase 3: COMPLETE
- [x] Streamlit main application (`app.py`)
- [x] Multi-tab dashboard interface
- [x] CSV file upload with validation
- [x] Real-time anomaly visualization
- [x] Interactive Plotly charts
- [x] Advanced filtering and sorting
- [x] CSV & JSON export capability
- [x] Reusable UI components
- [x] Backend API integration
- **Documentation:** [Phase 3 Summary](PHASE3_COMPLETE.md) | [Quick Reference](PHASE3_QUICKREF.md)

### ⏳ Phase 4: Advanced Features (Next)
- [ ] Metrics display
- [ ] Isolation Forest implementation
- [ ] Model training pipeline
- [ ] Sample data generation
- [ ] Model persistence

### ⏳ Phase 4: Integration
- [ ] API → ML connection
- [ ] Data pipeline
- [ ] Result formatting

### ⏳ Phase 5: Streamlit Dashboard
- [ ] Main page layout
- [ ] File upload component
- [ ] Results visualization
- [ ] Metrics display

### ⏳ Phase 6: Deployment
- [ ] Production configuration
- [ ] Docker optimization
- [ ] Deployment testing

## Key Files to Modify by Phase

| Phase | Key Files |
|-------|-----------|
| 2 | `backend/app/main.py` <br> `backend/app/api/routes.py` <br> `backend/app/models/schemas.py` |
| 3 | `backend/app/ml/anomaly_detector.py` <br> `ml/data/sample_logs.csv` |
| 4 | `backend/app/api/routes.py` (update) <br> `backend/app/ml/anomaly_detector.py` (update) |
| 5 | `frontend/app.py` <br> `frontend/pages/*.py` <br> `frontend/components/*.py` |
| 6 | `docker-compose.yml` (update) <br> `.env` (update) |

## Development Commands Quick Reference

```bash
# Setup
docker-compose up --build       # Start all services with Docker

# Backend only
cd backend && python -m uvicorn app.main:app --reload

# Frontend only
cd frontend && streamlit run app.py

# Testing
cd backend && pytest tests/

# Check health
curl http://localhost:8000/health
curl http://localhost:8000/docs       # API docs
```

## Data Flow Example

```
User Input (CSV) 
    ↓
Streamlit Upload Component
    ↓  
HTTP POST /api/analyze
    ↓
FastAPI Route Handler
    ↓
Data Validation (Pydantic)
    ↓
ML Model Inference
    ↓
Response JSON
    ↓
Streamlit Visualization
```

---

**Current Status**: Phase 1 Architecture Ready ✅  
**Next Action**: Start Phase 2 - Backend APIs
