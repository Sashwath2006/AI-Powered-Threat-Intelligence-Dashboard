# Architecture & Design Document

## System Design

### 1. Frontend Layer (Streamlit)
**Responsibilities:**
- Display threat intelligence dashboard
- Handle user input for log uploads
- Visualize anomaly detection results
- Show real-time metrics and alerts

**Key Components:**
- `app.py` - Main entry point
- `pages/` - Multi-page navigation
- `components/` - Reusable UI elements

### 2. API Layer (FastAPI)
**Responsibilities:**
- Expose REST endpoints for log analysis
- Validate incoming requests
- Orchestrate ML predictions
- Return formatted results

**Key Endpoints:**
- `POST /api/analyze` - Analyze logs
- `GET /api/results` - Retrieve results
- `GET /api/stats` - System statistics
- `GET /health` - Health check

### 3. ML Layer (Scikit-learn)
**Responsibilities:**
- Detect anomalies in log data
- Use Isolation Forest algorithm
- Generate anomaly scores
- Predict threat severity

**Key Components:**
- `AnomalyDetector` - Main ML class
- Model training pipeline
- Inference engine

### 4. Data Processing
**Input Format:**
```
timestamp, source_ip, destination_ip, port, protocol, bytes_sent, bytes_received, duration
```

**Output Format:**
```json
{
  "log_id": "unique_id",
  "is_anomaly": true/false,
  "anomaly_score": 0.85,
  "severity": "HIGH",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

## Data Flow

```
1. User uploads logs (CSV)
   ↓
2. Streamlit sends to FastAPI backend
   ↓
3. Backend validates and preprocesses data
   ↓
4. ML model analyzes logs
   ↓
5. Results returned to frontend
   ↓
6. Dashboard displays anomalies
```

## Scalability Considerations

- **Horizontal Scaling**: Backend can be scaled behind a load balancer
- **Caching**: Results can be cached for repeated queries
- **Batch Processing**: ML inference can be batched for efficiency
- **Async Operations**: FastAPI supports async endpoints for I/O operations

## Security

- Input validation on all endpoints
- Rate limiting (to be added)
- CORS configuration
- Environment variable for sensitive data
- Docker isolation between services

## Performance

- ML model optimization: Isolation Forest is fast for anomaly detection
- Vectorized operations using NumPy/Pandas
- Efficient data preprocessing
- Model caching to avoid reloading
