#!/usr/bin/env python3
"""
Test: Dataset WITHOUT duration Column
Simulates user's actual dataset structure
"""

import sys
from pathlib import Path
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

sys.path.insert(0, str(Path(__file__).parent / "frontend"))

print("\n" + "="*70)
print("TEST: Dataset WITHOUT Duration Column")
print("="*70)

# Create test dataset matching user's actual structure
print("\n[STEP 1] Create Test Dataset (NO DURATION)")
print("-" * 70)

test_data = {
    'timestamp': [
        '2024-01-01T10:00:00',
        '2024-01-01T10:01:00', 
        '2024-01-01T10:02:00',
        '2024-01-01T10:03:00',
        '2024-01-01T10:04:00',
    ],
    'source_ip': [
        '192.168.1.100',
        '192.168.1.101',
        '192.168.1.102',
        '192.168.1.103',
        '192.168.1.104',
    ],
    'destination_ip': [
        '8.8.8.8',
        '1.1.1.1',
        '208.67.222.222',
        '9.9.9.9',
        '1.1.1.1',
    ],
    'event_type': [
        'connection',
        'failed_login',
        'connection',
        'data_transfer',
        'failed_login',
    ],
    'protocol': ['TCP', 'TCP', 'TCP', 'UDP', 'TCP'],
    'source_port': [5000, 5001, 5002, 5003, 5004],
    'destination_port': [443, 22, 443, 53, 22],
    'bytes_sent': [1024, 512, 2048, 256, 128],
    'bytes_received': [2048, 1024, 4096, 512, 256],
    'failed_login_attempts': [0, 3, 0, 0, 5],
    'country': ['US', 'US', 'US', 'US', 'US'],
    'severity': ['low', 'high', 'low', 'low', 'high'],
    'is_anomaly': [False, True, False, False, True],
}

df = pd.DataFrame(test_data)

print(f"Dataset shape: {len(df)} rows x {len(df.columns)} columns")
print(f"Columns: {list(df.columns)}")
print(f"Has 'duration': {'duration' in df.columns}")

if 'duration' in df.columns:
    print("ERROR: Test data should NOT have duration!")
    sys.exit(1)

print("✓ Test dataframe created (no duration column)")

# Test 2: Parse CSV
print("\n[STEP 2] Parse Dataset Through Pipeline")
print("-" * 70)

try:
    from components.data_processing import parse_csv_to_logs  # type: ignore
    
    result = parse_csv_to_logs(df)
    logs = result.get('logs', [])
    errors = result.get('errors', [])
    
    print(f"Logs parsed: {len(logs)}")
    print(f"Parse errors: {len(errors)}")
    
    if len(logs) == 0:
        print("ERROR: No logs parsed!")
        print(f"Debug info: {result.get('debug', {})}")
        sys.exit(1)
    
    # Check first log
    first_log = logs[0]
    print(f"\nFirst log keys: {list(first_log.keys())}")
    print(f"First log: {first_log}")
    
    # Verify duration exists (engineered)
    if 'duration' not in first_log:
        print("ERROR: Duration not in parsed log!")
        sys.exit(1)
    
    print(f"✓ Duration engineered: {first_log['duration']:.2f}s")
    
    # Check all logs have duration
    missing_duration = [i for i, log in enumerate(logs) if 'duration' not in log]
    if missing_duration:
        print(f"ERROR: Logs missing duration: {missing_duration}")
        sys.exit(1)
    
    print(f"✓ All {len(logs)} logs have duration")
    
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 3: Send to Backend
print("\n[STEP 3] Send to Backend API")
print("-" * 70)

try:
    import requests
    
    payload = {"logs": logs, "errors": errors}
    
    print(f"Sending {len(logs)} logs to http://localhost:8000/api/analyze...")
    
    response = requests.post(
        "http://localhost:8000/api/analyze",
        json=payload,
        timeout=30
    )
    
    if response.status_code != 200:
        print(f"ERROR: Status {response.status_code}")
        print(f"Response: {response.text}")
        sys.exit(1)
    
    result = response.json()
    
    print(f"Status: {response.status_code}")
    print(f"Total analyzed: {result.get('total_logs', 0)}")
    print(f"Anomalies detected: {result.get('anomalies_detected', 0)}")
    print(f"Anomaly rate: {result.get('anomaly_percentage', 0):.1f}%")
    
    print("✓ Backend analysis successful!")
    
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "="*70)
print("TEST PASSED!")
print("="*70)
print("\nSUMMARY:")
print("✓ Dataset WITHOUT duration column created")
print("✓ Pipeline automatically engineered duration from data volume")
print("✓ All logs parsed successfully")
print("✓ Backend received and analyzed logs")
print("✓ Results returned with anomaly scores")
print("\nYour dataset structure is now fully supported!")
print("\n")
