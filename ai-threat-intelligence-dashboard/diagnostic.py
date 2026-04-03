#!/usr/bin/env python3
"""
Simple End-to-End Diagnostic
Tests each layer independently without complex imports
"""

import sys
import json
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

WORKSPACE = Path(__file__).parent

print("\n" + "="*70)
print("DIAGNOSTIC: End-to-End Pipeline Test")
print("="*70)

# TEST 1: CSV File Check
print("\n[TEST 1] CSV FILE CHECK")
print("-" * 70)

csv_file = WORKSPACE / "ml" / "data" / "sample_logs.csv"
logger.info(f"Looking for: {csv_file}")

if not csv_file.exists():
    logger.error(f"FAILED: File not found at {csv_file}")
    sys.exit(1)

logger.info(f"SUCCESS: File found")

# Read first few lines
with open(csv_file, 'r') as f:
    lines = [f.readline() for _ in range(5)]

header = lines[0].strip().split(',')
logger.info(f"Columns: {header}")
logger.info(f"First row: {lines[1].strip()}")

required_cols = ['timestamp', 'source_ip', 'destination_ip', 'port', 'bytes_sent', 'bytes_received', 'duration']
missing = [c for c in required_cols if c not in header]

if missing:
    logger.error(f"FAILED: Missing columns: {missing}")
    sys.exit(1)

logger.info(f"SUCCESS: All required columns present")

# TEST 2: CSV Parsing with Pandas
print("\n[TEST 2] CSV PARSING")
print("-" * 70)

try:
    import pandas as pd
    df = pd.read_csv(csv_file)
    logger.info(f"Loaded {len(df)} rows x {len(df.columns)} columns")
    logger.info(f"Data types:\n{df.dtypes}")
except Exception as e:
    logger.error(f"FAILED: {e}")
    sys.exit(1)

logger.info(f"SUCCESS: CSV parsed successfully")

# TEST 3: Backend API Test
print("\n[TEST 3] BACKEND API TEST")
print("-" * 70)

try:
    import requests
    
    # Check health
    response = requests.get("http://localhost:8000/health", timeout=2)
    logger.info(f"Backend health: {response.status_code} {response.text}")
    
    if response.status_code != 200:
        logger.warning("Backend not ready")
    else:
        logger.info("SUCCESS: Backend is responding")
        
except Exception as e:
    logger.error(f"FAILED: Backend not responding - {e}")
    logger.info("Make sure backend is running: python backend/main.py")

# TEST 4: Send Sample Data to API
print("\n[TEST 4] SEND DATA TO API")
print("-" * 70)

try:
    import requests
    
    # Get first 5 rows as logs
    df_sample = df.head(5)
    logs = df_sample.to_dict('records')
    
    logger.info(f"Sending {len(logs)} sample logs to backend...")
    logger.info(f"First log keys: {list(logs[0].keys())}")
    logger.info(f"First log sample: port={logs[0].get('port')}, bytes_sent={logs[0].get('bytes_sent')}")
    
    response = requests.post(
        "http://localhost:8000/api/analyze",
        json={"logs": logs},
        timeout=10
    )
    
    logger.info(f"Response status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        logger.info(f"SUCCESS: Analysis completed")
        logger.info(f"Response keys: {list(result.keys())}")
        logger.info(f"Anomalies found: {len(result.get('anomalies', []))}")
        
        if result.get('anomalies'):
            logger.info(f"First anomaly: {result['anomalies'][0]}")
    else:
        logger.error(f"FAILED: API returned {response.status_code}")
        logger.error(f"Response: {response.text}")
        
except Exception as e:
    logger.error(f"FAILED: {e}")
    import traceback
    traceback.print_exc()

# TEST 5: Feature Extraction Test
print("\n[TEST 5] FEATURE EXTRACTION TEST")
print("-" * 70)

try:
    sys.path.insert(0, str(WORKSPACE / "backend"))
    from app.ml.anomaly_detector import AnomalyDetector  # type: ignore
    
    detector = AnomalyDetector()
    df_sample = df.head(5)
    logs = df_sample.to_dict('records')
    
    logger.info(f"Extracting features from {len(logs)} logs...")
    
    detector.predict(logs)
    logger.info(f"SUCCESS: Model predictions work")
    
except Exception as e:
    logger.error(f"FAILED: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*70)
print("DIAGNOSTIC COMPLETE")
print("="*70)
print("\nIf all tests passed:")
print("1. Open http://localhost:8503 in browser")
print("2. Click 'Use Sample Data'")
print("3. Click 'Analyze Logs'")
print("4. Check both terminal windows for status")
print("\n")
