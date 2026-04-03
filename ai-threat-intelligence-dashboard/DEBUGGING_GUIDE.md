# Debugging Guide: "No logs to analyze" Error

## Current Status
✅ Backend running on port 8000  
✅ Frontend running on port 8503  
✅ Sample data file exists at `ml/data/sample_logs.csv`

## Step-by-Step Debugging

### Step 1: Access the Dashboard

Open your browser and navigate to:
```
http://localhost:8503
```

You should see the Streamlit dashboard with:
- File upload area at top
- Two tabs below: "Data Upload" and "Dashboard"

### Step 2: Test "Use Sample Data"

1. Click the **"Use Sample Data"** button
2. **Monitor the terminal where frontend is running** - you should see detailed logs
3. Click the **"Analyze Logs"** button
4. **Monitor both terminals** for error messages

### Step 3: Check Frontend Terminal Output

You're looking for this sequence:

```
LOADING SAMPLE DATA
  File path: ../ml/data/sample_logs.csv
  Absolute path: [full path shown]
  File exists: True
  Loaded CSV: [X] rows x [Y] columns
  Columns: [list of columns]
  Parsing CSV to logs...
  Parse result keys: ['logs', 'errors']
  Logs parsed: [X]
```

### Step 4: Check Data Processing Logs

After clicking analyze, you should see:

```
DATA PROCESSING PIPELINE START
  Input DataFrame shape: (X, Y)
  Input columns: [...]
  After validation: [pass/fail]
  After cleaning: X → Y rows (dropped Z)
  Parsed N valid rows, skipped M rows
  First log keys: [list of keys]
```

### Step 5: Check Backend Logs

In the backend terminal, you should see:

```
BACKEND PIPELINE START: Received X logs
  -> Converted to dict format: X logs
  -> Extracting features from X logs
  -> ML prediction started...
```

### Step 6: Interpret Results

#### ✅ If You See All Logs Flowing Through
1. Check if analysis completes
2. Results should display in "Dashboard" tab
3. Everything works - no issue

#### ❌ If Logs Stop at Frontend
Look for error messages about:
- CSV file not found
- Column missing
- Validation failed
- Dtype mismatch
- **Action**: Check `frontend/components/data_processing.py` for the specific error

#### ❌ If Logs Stop at Data Parsing
Look for error messages about:
- Cleaned rows: "X → 0 rows" (all dropped)
- Parse errors listed
- Field validation failed
- **Action**: Check which fields are being rejected

#### ❌ If Logs Stop Before Backend
Look for error messages about:
- API connection failed
- Invalid data format
- **Action**: Check backend is running, try manual API test below

#### ❌ If Backend Receives Empty Batch
Log message: "CRITICAL: Empty logs batch received"
- **Action**: Go back to Step 4 and see why frontend sent empty logs

---

## Manual API Test (If Frontend Has Issues)

Use Python to test the backend directly:

```python
import requests
import pandas as pd
import json
from pathlib import Path

# Load sample data
csv_path = Path("ml/data/sample_logs.csv")
df = pd.read_csv(csv_path)
print(f"Loaded {len(df)} rows from CSV")

# Convert to logs format
logs = df.to_dict('records')
print(f"Converted to {len(logs)} logs")

# Send to backend
response = requests.post(
    "http://localhost:8000/api/analyze",
    json={"logs": logs},
    timeout=10
)

print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")
```

Run this to confirm backend works independently of frontend.

---

## Detailed Log Reference

### CSV Loading Logs
```
LOADING SAMPLE DATA
├─ File path shown
├─ Absolute path shown
├─ File exists confirmed
├─ CSV shape (rows, columns)
└─ Column names listed
```

### Data Parsing Logs
```
DATA PROCESSING PIPELINE START
├─ Input shape and columns
├─ Validation: PASS/FAIL
├─ Before/after cleaning row counts
├─ Parse success/skip counts
└─ First log structure verified
```

### Backend Logs
```
BACKEND PIPELINE START: Received X logs
├─ Batch size verified
├─ Required fields checked
├─ Feature extraction started
├─ Model prediction running
└─ Results returned with anomaly counts
```

### Error Logs to Watch For
```
CRITICAL: Empty logs batch received
├─ Means: Frontend sent 0 logs to backend
├─ Check: Data parsing succeeded but result empty

MISSING required fields: [list]
├─ Means: Logs don't have all required columns
├─ Check: CSV has all needed columns

Parse errors: X
├─ Means: Some rows failed validation
├─ Check: Which specific fields are invalid
```

---

## Quick Checks

**Problem**: "No logs to analyze" message in dashboard
```
→ Check frontendterm: "LOADING SAMPLE DATA" appears?
→ Check: "DATA PROCESSING PIPELINE START" appears?
→ Check: How many logs parsed?
→ Check backend term: "BACKEND PIPELINE START" appears?
```

**Problem**: Sample data doesn't load
```
→ File exists: ml/data/sample_logs.csv?
→ Check: CSV has columns: timestamp, source_ip, destination_ip, port, protocol, bytes_sent, bytes_received, duration?
→ Check: At least 1 row of data?
```

**Problem**: CSV loads but 0 rows parse
```
→ Check: "After cleaning: X → 0 rows"?
→ Check: Which validation rule rejects rows?
→ Check: Data types match expectations? (port should be int, bytes should be numeric)
```

---

## Terminal Log Locations

**Frontend Terminal**: Logs from Streamlit app.py (port 8503)
```
LOADING SAMPLE DATA
DATA PROCESSING PIPELINE START
```

**Backend Terminal**: Logs from FastAPI (port 8000)
```
BACKEND PIPELINE START
```

Both logs together tell you the complete story of where data goes.

---

## Next Steps After Debugging

Once you identify where logs stop flowing:

1. **If frontend issue**: Update `frontend/components/data_processing.py`
2. **If backend issue**: Update `backend/app/api/routes.py`
3. **If validation issue**: Update `backend/app/models/schemas.py`

The detailed logs will show exactly which field or validation rule is causing the problem.
