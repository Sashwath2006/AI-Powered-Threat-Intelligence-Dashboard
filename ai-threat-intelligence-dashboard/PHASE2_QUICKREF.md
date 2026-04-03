# Phase 2: Quick Reference Guide

## Start Backend

```bash
# Terminal 1
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

### Health Check
```bash
curl http://localhost:8000/health
```

### Get Statistics
```bash
curl http://localhost:8000/api/stats
```

### Analyze Logs
```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "logs": [
      {
        "timestamp": "2024-01-01T12:00:00",
        "source_ip": "192.168.1.100",
        "destination_ip": "8.8.8.8",
        "port": 443,
        "protocol": "TCP",
        "bytes_sent": 1024,
        "bytes_received": 2048,
        "duration": 5.5
      },
      {
        "timestamp": "2024-01-01T12:01:00",
        "source_ip": "10.0.0.50",
        "destination_ip": "172.217.1.1",
        "port": 9999,
        "protocol": "TCP",
        "bytes_sent": 50000,
        "bytes_received": 100000,
        "duration": 60.0
      }
    ]
  }'
```

## Documentation

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **OpenAPI JSON:** http://localhost:8000/openapi.json

## Testing

```bash
# Run all tests
cd backend
pytest tests/ -v

# Run with coverage
pytest tests/ --cov

# Quick API test script
python test_api.py
```

## Key Files

| File | Purpose |
|------|---------|
| `app/main.py` | FastAPI application |
| `app/api/routes.py` | API endpoints |
| `app/ml/anomaly_detector.py` | Isolation Forest model |
| `app/models/schemas.py` | Pydantic Data models |
| `app/config.py` | Configuration management |
| `tests/test_backend.py` | Unit tests |

## Environment Variables

Set in `.env`:
```
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
DEBUG=True
ANOMALY_THRESHOLD=0.7
LOG_LEVEL=INFO
```

## How Anomaly Detection Works

1. **Receive Logs** - POST request with log batch
2. **Extract Features** - Values: port, bytes_sent, bytes_received, duration
3. **Normalize** - StandardScaler normalizes features
4. **Predict** - Isolation Forest generates predictions
5. **Score** - Anomaly scores mapped to 0.0-1.0 range
6. **Severity** - Scores converted to severity levels:
   - 0.9-1.0: CRITICAL
   - 0.75-0.9: HIGH
   - 0.5-0.75: MEDIUM
   - 0.0-0.5: LOW

## Integration Example (Python)

```python
import requests
from datetime import datetime

# Prepare logs
logs = {
    "logs": [
        {
            "timestamp": datetime.now().isoformat(),
            "source_ip": "192.168.1.1",
            "destination_ip": "8.8.8.8",
            "port": 443,
            "protocol": "TCP",
            "bytes_sent": 1024,
            "bytes_received": 2048,
            "duration": 5.0
        }
    ]
}

# Call API
response = requests.post("http://localhost:8000/api/analyze", json=logs)
result = response.json()

# Use results
print(f"Analyzed {result['total_logs']} logs")
print(f"Found {result['anomalies_detected']} anomalies")

for anomaly in result['results']:
    if anomaly['is_anomaly']:
        print(f"Anomaly: {anomaly['source_ip']} -> {anomaly['destination_ip']} "
              f"(Score: {anomaly['anomaly_score']:.2f}, Severity: {anomaly['severity']})")
```

## Logs Available

Sample logs in `ml/data/sample_logs.csv`:
- Normal traffic: ports 53 (DNS), 80 (HTTP), 443 (HTTPS)
- Anomalous traffic: ports 7777-9999 with unusual byte patterns

Features:
- 1024-2560 bytes sent (normal) vs 50,000-80,000 (anomalous)
- 2-5 seconds duration (normal) vs 60-120 seconds (anomalous)
