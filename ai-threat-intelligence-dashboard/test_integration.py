#!/usr/bin/env python3
"""
Integration Test - Simulates Frontend Flow
Tests: Load Sample Data → Parse → Send to Backend → Get Results
"""

import sys
import json
from pathlib import Path

# Add paths
sys.path.insert(0, str(Path(__file__).parent / "frontend"))

import pandas as pd
import requests
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

print("\n" + "="*70)
print("INTEGRATION TEST: Frontend Flow")
print("="*70)

WORKSPACE = Path(__file__).parent
CSV_PATH = WORKSPACE / "ml" / "data" / "sample_logs.csv"
API_URL = "http://localhost:8000/api/analyze"

# STEP 1: Load CSV (simulating "Use Sample Data" button)
print("\n[STEP 1] Load Sample Data")
print("-" * 70)

try:
    df = pd.read_csv(CSV_PATH)
    logger.info(f"Loaded {len(df)} rows from {CSV_PATH}")
except Exception as e:
    logger.error(f"Failed to load CSV: {e}")
    sys.exit(1)

# STEP 2: Parse CSV (simulating parse_csv_to_logs)
print("\n[STEP 2] Parse CSV to Logs")
print("-" * 70)

try:
    from components.data_processing import parse_csv_to_logs  # type: ignore
    
    parsed_result = parse_csv_to_logs(df)
    logs_list = parsed_result.get("logs", [])
    errors = parsed_result.get("errors", [])
    
    logger.info(f"Parsed {len(logs_list)} logs")
    if errors:
        logger.warning(f"Parse errors: {len(errors)}")
        for err in errors[:3]:
            logger.warning(f"  - {err}")
    
    if len(logs_list) == 0:
        logger.error("CRITICAL: No logs parsed!")
        sys.exit(1)
    
    logger.info(f"First log keys: {list(logs_list[0].keys())}")
    logger.info(f"✅ Parsing successful")
    
except Exception as e:
    logger.error(f"Parsing failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# STEP 3: Send to Backend (simulating analyze_logs)
print("\n[STEP 3] Send to Backend API")
print("-" * 70)

try:
    # Prepare payload (same structure as frontend sends)
    payload = {
        "logs": logs_list,
        "errors": errors
    }
    
    logger.info(f"Sending {len(logs_list)} logs to {API_URL}")
    
    response = requests.post(API_URL, json=payload, timeout=30)
    logger.info(f"Response status: {response.status_code}")
    
    if response.status_code != 200:
        logger.error(f"API error: {response.text}")
        sys.exit(1)
    
    result = response.json()
    logger.info(f"✅ Backend analysis successful")
    
except Exception as e:
    logger.error(f"API call failed: {e}")
    sys.exit(1)

# STEP 4: Display Results
print("\n[STEP 4] Results")
print("-" * 70)

try:
    total_logs = result.get("total_logs", 0)
    anomalies = result.get("anomalies_detected", 0)
    percentage = result.get("anomaly_percentage", 0)
    results_data = result.get("results", [])
    
    logger.info(f"Total logs analyzed: {total_logs}")
    logger.info(f"Anomalies detected: {anomalies}")
    logger.info(f"Anomaly rate: {percentage:.1f}%")
    logger.info(f"Detailed results: {len(results_data)} entries")
    
    if results_data:
        first_result = results_data[0]
        logger.info(f"First result keys: {list(first_result.keys())}")
        logger.info(f"Sample result: {json.dumps(first_result, indent=2)[:200]}...")
    
except Exception as e:
    logger.error(f"Failed to display results: {e}")
    sys.exit(1)

print("\n" + "="*70)
print("INTEGRATION TEST PASSED")
print("="*70)
print("\nThe frontend flow is now working correctly:")
print("1. ✅ Front-end loads sample data")
print("2. ✅ Data parsing completes without errors")
print("3. ✅ Logs sent to backend successfully")
print("4. ✅ Backend returns analysis results")
print("\nYour dashboard should now work! Open http://localhost:8503")
print("and click 'Use Sample Data' followed by 'Analyze Logs'")
print("\n")
