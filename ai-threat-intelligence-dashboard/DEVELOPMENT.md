# Development Guide

## Getting Started with Phase 1

### Local Environment Setup

#### 1. Clone/Navigate to Project
```bash
cd ai-threat-intelligence-dashboard
```

#### 2. Virtual Environment (Optional but Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies (Both)
```bash
# Backend
cd backend
pip install -r requirements.txt
cd ..

# Frontend
cd frontend
pip install -r requirements.txt
cd ..
```

### Running Without Docker

#### Terminal 1 - Backend
```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
- API will be available at: http://localhost:8000
- Swagger docs at: http://localhost:8000/docs

#### Terminal 2 - Frontend
```bash
cd frontend
streamlit run app.py
```
- Dashboard will be available at: http://localhost:8501

### Environment Configuration

The `.env` file contains key settings:

```env
BACKEND_HOST=0.0.0.0           # Backend server address
BACKEND_PORT=8000              # Backend server port
DEBUG=True                      # Debug mode
ANOMALY_THRESHOLD=0.7           # ML anomaly threshold
MODEL_PATH=ml/models/...        # Path to ML model
LOG_LEVEL=INFO                  # Logging level
```

**For development**: Leave defaults in `.env`
**For production**: Update values and set `DEBUG=False`

### File Organization

**Backend (app/):**
- `main.py` - FastAPI application factory
- `config.py` - Configuration & settings
- `api/routes.py` - API endpoint definitions
- `ml/anomaly_detector.py` - ML model logic
- `models/schemas.py` - Pydantic request/response models

**Frontend:**
- `app.py` - Main Streamlit app
- `components/` - Reusable UI components
- `pages/` - Multi-page views

**ML:**
- `models/` - Trained model files (saved as .pkl or .joblib)
- `data/` - Sample datasets (sample_logs.csv)

## Development Workflow

### Adding a New API Endpoint

1. Define schema in `backend/app/models/schemas.py`
2. Add route in `backend/app/api/routes.py`
3. Implement logic in appropriate module
4. Test with: `curl -X POST http://localhost:8000/api/endpoint`
5. Verify in Swagger UI: http://localhost:8000/docs

### Adding a Streamlit Page

1. Create file in `frontend/pages/page_name.py`
2. Import and use in `frontend/app.py`
3. Restart Streamlit to see changes

### Testing

```bash
cd backend
pytest tests/ -v                    # Run all tests
pytest tests/test_file.py -v        # Run specific test file
pytest tests/ --cov                 # With coverage report
```

## Docker Development

### Build Images
```bash
docker-compose build
```

### Start Services
```bash
docker-compose up
```

### Stop Services
```bash
docker-compose down
```

### View Logs
```bash
docker-compose logs backend      # Backend logs
docker-compose logs frontend     # Frontend logs
docker-compose logs              # All logs
```

### Rebuild After Changes
```bash
docker-compose up --build
```

## Debugging

### Backend Debugging
Add to `backend/app/main.py`:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
```

### Frontend Debugging
```python
# In Streamlit components
st.write("Debug info:", variable)
```

### Docker Debugging
```bash
# Execute command in running container
docker-compose exec backend bash
docker-compose exec frontend bash
```

## Common Issues

### Port Already in Use
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:8000 | xargs kill -9
```

### Module Not Found
```bash
# Ensure proper installation
pip install -r requirements.txt

# Or reinstall
pip install -r requirements.txt --force-reinstall
```

### CORS Issues
Check `backend/app/main.py` for CORS configuration.

## Next Steps (Phase 2)

Once Phase 1 is set up correctly:
1. Implement `backend/app/main.py` - FastAPI app
2. Create API routes in `backend/app/api/routes.py`
3. Define data schemas in `backend/app/models/schemas.py`
4. Test endpoints with Swagger UI
