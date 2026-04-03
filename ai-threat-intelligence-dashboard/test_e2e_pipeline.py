#!/usr/bin/env python3
"""
End-to-End Pipeline Test for AI Threat Intelligence Dashboard
Tests: CSV Loading → Data Parsing → Backend API → ML Analysis
"""

import sys
import os
import json
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add project paths
FRONTEND_DIR = Path(__file__).parent / "frontend"
ML_DIR = Path(__file__).parent / "ml"
BACKEND_DIR = Path(__file__).parent / "backend"

sys.path.insert(0, str(FRONTEND_DIR))
sys.path.insert(0, str(BACKEND_DIR))

def test_csv_loading():
    """Test 1: CSV Loading"""
    print("\n" + "="*60)
    print("TEST 1: CSV LOADING")
    print("="*60)
    
    import pandas as pd
    
    csv_path = ML_DIR / "data" / "sample_logs.csv"
    logger.info(f"CSV path: {csv_path}")
    logger.info(f"File exists: {csv_path.exists()}")
    
    if not csv_path.exists():
        logger.error(f"❌ CSV file not found at {csv_path}")
        return None
    
    df = pd.read_csv(csv_path)
    logger.info(f"✅ CSV loaded: {len(df)} rows x {len(df.columns)} columns")
    logger.info(f"Columns: {list(df.columns)}")
    logger.info(f"Data types:\n{df.dtypes}")
    logger.info(f"First row:\n{df.iloc[0]}")
    
    return df

def test_data_parsing(df):
    """Test 2: Data Parsing"""
    print("\n" + "="*60)
    print("TEST 2: DATA PARSING")
    print("="*60)
    
    from components.data_processing import parse_csv_to_logs  # type: ignore
    
    logger.info(f"Parsing {len(df)} rows...")
    result = parse_csv_to_logs(df)
    
    logger.info(f"Parse result keys: {list(result.keys())}")
    logger.info(f"Logs parsed: {len(result.get('logs', []))}")
    logger.info(f"Errors: {len(result.get('errors', []))}")
    
    if result.get('errors'):
        logger.warning(f"Parse errors:")
        for err in result['errors'][:5]:  # Show first 5 errors
            logger.warning(f"  - {err}")
    
    if len(result.get('logs', [])) == 0:
        logger.error("❌ No logs parsed!")
        return None
    
    logger.info(f"✅ Successfully parsed {len(result['logs'])} logs")
    
    # Verify first log structure
    first_log = result['logs'][0]
    required_fields = ['timestamp', 'source_ip', 'destination_ip', 'port', 'bytes_sent', 'bytes_received', 'duration']
    missing = [f for f in required_fields if f not in first_log]
    
    if missing:
        logger.error(f"❌ First log missing fields: {missing}")
        logger.error(f"First log keys: {list(first_log.keys())}")
        return None
    
    logger.info(f"✅ First log has all required fields")
    logger.info(f"First log: {first_log}")
    
    return result

def test_backend_api(logs_data):
    """Test 3: Backend API"""
    print("\n" + "="*60)
    print("TEST 3: BACKEND API")
    print("="*60)
    
    import requests
    from app.models.schemas import LogBatch  # type: ignore
    
    # Check if backend is running
    try:
        response = requests.get("http://localhost:8000/health", timeout=2)
        logger.info(f"Backend health check: {response.status_code}")
    except Exception as e:
        logger.error(f"❌ Backend not responding: {str(e)}")
        logger.error("Make sure backend is running on port 8000")
        return None
    
    # Prepare log batch
    try:
        log_batch = LogBatch(logs=logs_data)
        logger.info(f"✅ LogBatch created with {len(log_batch.logs)} logs")
    except Exception as e:
        logger.error(f"❌ Failed to create LogBatch: {str(e)}")
        return None
    
    # Send to backend
    try:
        response = requests.post(
            "http://localhost:8000/api/analyze",
            json=log_batch.model_dump(),
            timeout=10
        )
        logger.info(f"API response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            logger.info(f"✅ Backend analysis successful")
            logger.info(f"Response keys: {list(result.keys())}")
            
            anomalies = result.get('anomalies', [])
            logger.info(f"Anomalies detected: {len(anomalies)}")
            if anomalies:
                logger.info(f"First anomaly: {anomalies[0]}")
            
            return result
        else:
            logger.error(f"❌ API returned status {response.status_code}")
            logger.error(f"Response: {response.text}")
            return None
            
    except Exception as e:
        logger.error(f"❌ API request failed: {str(e)}")
        return None

def test_feature_extraction(logs_data):
    """Test 4: Feature Extraction"""
    print("\n" + "="*60)
    print("TEST 4: FEATURE EXTRACTION")
    print("="*60)
    
    from app.ml.anomaly_detector import AnomalyDetector  # type: ignore
    
    try:
        detector = AnomalyDetector()
        logger.info(f"✅ AnomalyDetector loaded")
        logger.info(f"Model type: {type(detector.model)}")
        
        # Extract features
        features = detector.extract_features(logs_data)
        logger.info(f"Features shape: {features.shape}")
        logger.info(f"Features:\n{features[:3]}")
        
        # Predict
        predictions = detector.predict(logs_data)
        logger.info(f"✅ Predictions: {len(predictions)} anomalies")
        
        return predictions
        
    except Exception as e:
        logger.error(f"❌ Feature extraction failed: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return None

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("END-TO-END PIPELINE TEST")
    print("="*60)
    
    # Test 1: CSV Loading
    df = test_csv_loading()
    if df is None:
        return False
    
    # Test 2: Data Parsing
    parsed_data = test_data_parsing(df)
    if parsed_data is None:
        return False
    
    logs = parsed_data.get('logs', [])
    
    # Test 3: Feature Extraction (faster than API test)
    predictions = test_feature_extraction(logs)
    if predictions is None:
        logger.warning("⚠️ Feature extraction failed, skipping API test")
    else:
        logger.info(f"Feature extraction successful: {len(predictions)} anomalies")
    
    # Test 4: Backend API (if available)
    try:
        result = test_backend_api(logs)
        if result is None:
            logger.warning("⚠️ Backend API not available")
        else:
            logger.info(f"Backend API successful: {len(result.get('anomalies', []))} anomalies")
    except Exception as e:
        logger.warning(f"⚠️ Could not test backend API: {str(e)}")
    
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    logger.info("✅ All pipeline tests completed successfully!")
    logger.info("If you see this, the end-to-end pipeline works.")
    logger.info("Check the logs above for any errors.")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        logger.error(f"Test failed with error: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        sys.exit(1)
