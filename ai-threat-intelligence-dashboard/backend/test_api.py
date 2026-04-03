"""Quick test script for the backend API"""
import requests
from datetime import datetime
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("\n=== Testing Health Check ===")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_stats():
    """Test stats endpoint"""
    print("\n=== Testing Stats Endpoint ===")
    response = requests.get(f"{BASE_URL}/api/stats")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_analysis():
    """Test analysis endpoint"""
    print("\n=== Testing Log Analysis ===")
    
    payload = {
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
                "source_ip": "192.168.1.101",
                "destination_ip": "1.1.1.1",
                "port": 80,
                "protocol": "TCP",
                "bytes_sent": 512,
                "bytes_received": 1024,
                "duration": 3.2
            },
            {
                "timestamp": "2024-01-01T12:02:00",
                "source_ip": "10.0.0.50",
                "destination_ip": "8.8.8.8",
                "port": 9999,
                "protocol": "TCP",
                "bytes_sent": 50000,
                "bytes_received": 100000,
                "duration": 60.0
            }
        ]
    }
    
    response = requests.post(f"{BASE_URL}/api/analyze", json=payload)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\nAnalysis Results:")
        print(f"  Total Logs: {data['total_logs']}")
        print(f"  Anomalies Detected: {data['anomalies_detected']}")
        print(f"  Anomaly Percentage: {data['anomaly_percentage']:.2f}%")
        print(f"\n  Detailed Results:")
        for result in data['results']:
            print(f"    Log {result['log_index']}:")
            print(f"      Is Anomaly: {result['is_anomaly']}")
            print(f"      Anomaly Score: {result['anomaly_score']:.4f}")
            print(f"      Severity: {result['severity']}")
    else:
        print(f"Error: {response.text}")


def main():
    """Run all tests"""
    print("Starting API Tests...")
    print(f"Base URL: {BASE_URL}")
    
    try:
        test_health()
        test_stats()
        test_analysis()
        print("\n=== All Tests Complete ===\n")
    except requests.exceptions.ConnectionError:
        print(f"ERROR: Could not connect to {BASE_URL}")
        print("Make sure the backend is running: python -m uvicorn app.main:app --reload")
    except Exception as e:
        print(f"ERROR: {str(e)}")


if __name__ == "__main__":
    main()
