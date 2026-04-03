# AI-Powered Threat Intelligence Dashboard

A complete system for detecting security anomalies in log data using machine learning.

## 🎯 Project Overview

**Detects threats by:**
- Analyzing log data patterns
- Using Isolation Forest ML model to identify anomalies
- Displaying results in an interactive Streamlit dashboard
- Providing REST API for integrations

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit Dashboard                      │
│            (Real-time visualization & analytics)            │
└────────────────────┬─────────────────────────────────────────┘
                     │ HTTP Requests
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                     FastAPI Backend                         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ REST API Endpoints (Routes)                          │  │
│  │ - POST /api/analyze (Log analysis)                   │  │
│  │ - GET /api/results (Fetch predictions)               │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ ML Engine (Isolation Forest)                         │  │
│  │ - Anomaly detection                                  │  │
│  │ - Model inference                                    │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                     │
                     ▼
        ┌────────────────────────────┐
        │   ML Models & Data         │
        │ - Trained models           │
        │ - Sample log datasets      │
        └────────────────────────────┘
```

## 📁 Project Structure

```
ai-threat-intelligence-dashboard/
├── backend/                          # FastAPI Backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                  # FastAPI entry point
│   │   ├── config.py                # Configuration management
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── routes.py            # API endpoints
│   │   ├── ml/
│   │   │   ├── __init__.py
│   │   │   └── anomaly_detector.py  # Isolation Forest model
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── schemas.py           # Pydantic data models
│   │   └── utils/
│   │       ├── __init__.py
│   │       └── logger.py            # Logging utility
│   ├── tests/                       # Unit tests
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .dockerignore
│
├── frontend/                        # Streamlit Frontend
│   ├── app.py                       # Streamlit main app
│   ├── requirements.txt
│   ├── pages/                       # Multi-page components
│   ├── components/                  # Reusable UI components
│   ├── Dockerfile
│   └── .dockerignore
│
├── ml/                              # ML Models & Data
│   ├── models/                      # Trained model files
│   └── data/
│       └── sample_logs.csv          # Sample dataset
│
├── docker-compose.yml               # Docker orchestration
├── .env                             # Environment variables
├── .gitignore
└── README.md                        # This file
```

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose (recommended)
- Python 3.11+ (for local development)

### Option 1: Docker (Recommended)

```bash
# Clone the repository
cd ai-threat-intelligence-dashboard

# Start services
docker-compose up --build

# Access the application
# Frontend: http://localhost:8501
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Option 2: Local Development

#### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

#### Frontend Setup
```bash
cd frontend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## 📊 Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Backend** | FastAPI | RESTful API framework |
| **Frontend** | Streamlit | Interactive dashboard |
| **ML** | Scikit-learn | Anomaly detection (Isolation Forest) |
| **Data Processing** | Pandas, NumPy | Log data manipulation |
| **Containerization** | Docker | Deployment |
| **Testing** | pytest | Unit tests |

## 🔄 Development Phases

### Phase 1: Architecture ✅ (COMPLETED)
- [x] Folder structure
- [x] Configuration files
- [x] Docker setup
- [x] Documentation

### Phase 2: Backend APIs ✅ (COMPLETED)
- [x] FastAPI main app (`app/main.py`)
- [x] API routes for log analysis (`api/routes.py`)
- [x] Request/response schemas (`models/schemas.py`)
- [x] Isolation Forest anomaly detector (`ml/anomaly_detector.py`)
- [x] Error handling and validation
- [x] Unit tests (`tests/test_backend.py`)
- [x] API documentation (Swagger/ReDoc)
- **See:** [Phase 2 Complete Guide](PHASE2_COMPLETE.md) | [Quick Reference](PHASE2_QUICKREF.md)

### Phase 3: Streamlit Dashboard ✅ (COMPLETED)
- [x] Multi-tab Streamlit application
- [x] Data upload (CSV, Sample, Manual)
- [x] Real-time anomaly visualization
- [x] Interactive Plotly charts
- [x] Advanced filtering & sorting
- [x] CSV & JSON export
- [x] Backend API integration
- **See:** [Phase 3 Complete Guide](PHASE3_COMPLETE.md) | [Quick Reference](PHASE3_QUICKREF.md)

### Phase 4: Advanced Features (Next)
- [ ] Isolation Forest implementation
- [ ] Model training
- [ ] Inference logic
- [ ] Model persistence

### Phase 4: Integration (Next)
- [ ] Connect API to ML model
- [ ] Request processing pipeline
- [ ] Result formatting

### Phase 5: Streamlit Dashboard (Next)
- [ ] Main dashboard page
- [ ] Data upload component
- [ ] Results visualization
- [ ] Metrics display

### Phase 6: Deployment (Next)
- [ ] Docker image optimization
- [ ] Production configuration
- [ ] CI/CD setup
- [ ] Documentation

## 🧪 Testing

```bash
cd backend
pytest tests/
```

## 📖 API Documentation

Once backend is running, visit `http://localhost:8000/docs` for interactive API documentation (Swagger UI).

## 🤝 Contributing

1. Create a feature branch
2. Make your changes
3. Write tests
4. Submit a pull request

## 📝 License

MIT License

## 📞 Support

For issues or questions, please open an issue on GitHub.

---

**Status**: Phase 1 Complete - Ready for Phase 2 Backend Development
