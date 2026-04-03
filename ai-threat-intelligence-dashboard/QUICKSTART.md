# ⚡ Phase 2: ULTRA-QUICK START

## 🏃 Get Running in 30 Seconds

### Step 1: Navigate to Project
```bash
cd "f:\Intern Project\ai-threat-intelligence-dashboard"
```

### Step 2: Start Backend
```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Wait for:**
```
Uvicorn running on http://0.0.0.0:8000
Application startup complete
```

### Step 3: Open Documentation
Open in browser: **http://localhost:8000/docs**

## ✅ That's It!

Now you can:
- 📖 Read the API docs (Swagger UI)
- 🧪 Test endpoints interactively
- 💡 See request/response examples

## 🎮 Try It Now!

In Swagger UI, click **POST /api/analyze** then:

1. Click **"Try it out"**
2. Paste this in the request body:
```json
{
  "logs": [
    {
      "timestamp": "2024-01-01T12:00:00",
      "source_ip": "192.168.1.1",
      "destination_ip": "8.8.8.8",
      "port": 443,
      "protocol": "TCP",
      "bytes_sent": 1024,
      "bytes_received": 2048,
      "duration": 5.0
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
}
```

3. Click **"Execute"**

**Result:** Should show 1 anomaly detected! ✨

## 🔗 Key URLs

| What | URL |
|------|-----|
| API Docs | http://localhost:8000/docs |
| Alternative Docs | http://localhost:8000/redoc |
| Health Check | http://localhost:8000/health |
| OpenAPI JSON | http://localhost:8000/openapi.json |

## 📝 Other Options

### Run Tests
```bash
cd backend
pytest tests/ -v
```

### Run Quick API Test
```bash
cd backend
python test_api.py
```

### Using curl
```bash
# Health check
curl http://localhost:8000/health

# Analyze logs (with sample data)
curl -X POST http://localhost:8000/api/analyze ^
  -H "Content-Type: application/json" ^
  -d "{\"logs\":[{\"timestamp\":\"2024-01-01T12:00:00\",\"source_ip\":\"192.168.1.1\",\"destination_ip\":\"8.8.8.8\",\"port\":443,\"protocol\":\"TCP\",\"bytes_sent\":1024,\"bytes_received\":2048,\"duration\":5.0}]}"
```

## 🛠️ If Something Goes Wrong

**Error: "ModuleNotFoundError: No module named 'fastapi'"**
```bash
pip install -r requirements.txt
```

**Error: "Port 8000 already in use"**
```bash
# Kill process (Windows PowerShell)
$process = Get-Process | Where-Object {$_.ProcessName -eq "python"} | Select-Object -First 1
Stop-Process $process -Force

# OR edit .env and change BACKEND_PORT=8001
```

**Error: "Connection refused"**
- Make sure backend is running (check terminal)
- Make sure you didn't stop it

## 📚 Learn More

After 30-second quickstart, read these:

1. **[PHASE2_COMPLETE.md](PHASE2_COMPLETE.md)** - Full details
2. **[PHASE2_QUICKREF.md](PHASE2_QUICKREF.md)** - Commands reference
3. **[Architecture](ARCHITECTURE.md)** - How it works

## 🎯 What Happens

1. You send logs (JSON format)
2. Backend validates with strict type checking
3. ML model extracts 4 features per log:
   - Port number
   - Bytes sent
   - Bytes received
   - Duration
4. Isolation Forest predicts anomalies
5. Scores converted to severity levels:
   - CRITICAL: 0.9-1.0
   - HIGH: 0.75-0.9
   - MEDIUM: 0.5-0.75
   - LOW: 0.0-0.5

**Example Result:**
- Normal traffic (port 443, 1KB sent): LOW severity
- Suspicious traffic (port 9999, 50KB sent): HIGH severity

## 🚀 Next: Phase 3

Ready to build the dashboard? Run:
```
Ready to proceed with Phase 3: Streamlit Dashboard?
```

---

**That's literally it!** 🎉

Backend is running and ready for the frontend.
