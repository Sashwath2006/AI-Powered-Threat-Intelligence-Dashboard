"""Unit Tests for Backend"""
import pytest
from fastapi.testclient import TestClient
from datetime import datetime
import numpy as np

from app.main import app, create_app
from app.models.schemas import LogEntry, LogBatch
from app.ml.anomaly_detector import AnomalyDetector, extract_features, score_severity


@pytest.fixture
def client():
    """Create test client with proper lifespan context"""
    test_app = create_app()
    with TestClient(test_app) as test_client:
        yield test_client


@pytest.fixture
def sample_logs():
    """Create sample logs for testing"""
    return LogBatch(
        logs=[
            LogEntry(
                timestamp=datetime(2024, 1, 1, 12, 0, 0),
                source_ip="192.168.1.100",
                destination_ip="8.8.8.8",
                port=443,
                protocol="TCP",
                bytes_sent=1024,
                bytes_received=2048,
                duration=5.5,
                source_port=None,
                destination_port=None,
                event_type=None,
                failed_login_attempts=None,
                country=None,
                severity=None,
                is_anomaly=None
            ),
            LogEntry(
                timestamp=datetime(2024, 1, 1, 12, 1, 0),
                source_ip="192.168.1.101",
                destination_ip="1.1.1.1",
                port=80,
                protocol="TCP",
                bytes_sent=512,
                bytes_received=1024,
                duration=3.2,
                source_port=None,
                destination_port=None,
                event_type=None,
                failed_login_attempts=None,
                country=None,
                severity=None,
                is_anomaly=None
            ),
            LogEntry(
                timestamp=datetime(2024, 1, 1, 12, 2, 0),
                source_ip="192.168.1.102",
                destination_ip="8.8.8.8",
                port=9999,
                protocol="UDP",
                bytes_sent=50000,
                bytes_received=100000,
                duration=60.0,
                source_port=None,
                destination_port=None,
                event_type=None,
                failed_login_attempts=None,
                country=None,
                severity=None,
                is_anomaly=None
            )
        ]
    )


class TestAnomalyDetector:
    """Test Isolation Forest anomaly detector"""
    
    def test_detector_initialization(self):
        """Test detector can be initialized"""
        detector = AnomalyDetector(contamination=0.1)
        assert detector.is_trained is False
        assert detector.contamination == 0.1
    
    def test_model_training(self):
        """Test model can be trained"""
        detector = AnomalyDetector()
        
        # Generate sample data
        X = np.random.randn(100, 4)
        detector.train(X)
        
        assert detector.is_trained is True
    
    def test_prediction_before_training(self):
        """Test prediction fails before training"""
        detector = AnomalyDetector()
        X = np.random.randn(10, 4)
        
        with pytest.raises(ValueError):
            detector.predict(X)
    
    def test_prediction_after_training(self):
        """Test prediction works after training"""
        detector = AnomalyDetector()
        
        # Train on normal data
        X_train = np.random.normal(0, 1, (100, 4))
        detector.train(X_train)
        
        # Predict on new data
        X_test = np.random.normal(0, 1, (10, 4))
        predictions, scores = detector.predict(X_test)
        
        assert len(predictions) == 10
        assert len(scores) == 10
        assert np.all((scores >= 0) & (scores <= 1))
    
    def test_feature_extraction(self):
        """Test feature extraction from logs"""
        logs = [
            {
                'port': 443,
                'bytes_sent': 1024,
                'bytes_received': 2048,
                'duration': 5.5
            },
            {
                'port': 80,
                'bytes_sent': 512,
                'bytes_received': 1024,
                'duration': 3.2
            }
        ]
        
        X = extract_features(logs)
        assert X.shape == (2, 4)
    
    def test_severity_scoring(self):
        """Test severity scoring"""
        assert score_severity(0.95) == "CRITICAL"
        assert score_severity(0.80) == "HIGH"
        assert score_severity(0.60) == "MEDIUM"
        assert score_severity(0.30) == "LOW"


class TestAPIEndpoints:
    """Test API endpoints"""
    
    def test_health_check(self, client):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
    
    def test_root_endpoint(self, client):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        assert "service" in response.json()
    
    def test_analyze_logs_success(self, client, sample_logs):
        """Test log analysis endpoint"""
        response = client.post("/api/analyze", json=sample_logs.model_dump(mode='json'))
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "success"
        assert data["total_logs"] == 3
        assert "results" in data
        assert len(data["results"]) == 3
    
    def test_analyze_logs_invalid_input(self, client):
        """Test analysis with invalid input"""
        response = client.post(
            "/api/analyze",
            json={"logs": []}
        )
        assert response.status_code == 422  # Validation error
    
    def test_get_stats(self, client):
        """Test stats endpoint"""
        response = client.get("/api/stats")
        assert response.status_code == 200
        assert "model_trained" in response.json()


class TestDataSchemas:
    """Test Pydantic data models"""
    
    def test_log_entry_validation(self):
        """Test LogEntry validation"""
        valid_log = LogEntry(
            timestamp=datetime.now(),
            source_ip="192.168.1.1",
            destination_ip="8.8.8.8",
            port=443,
            protocol="TCP",
            bytes_sent=1024,
            bytes_received=2048,
            duration=5.0,
            source_port=None,
            destination_port=None,
            event_type=None,
            failed_login_attempts=None,
            country=None,
            severity=None,
            is_anomaly=None
        )
        assert valid_log.port == 443
    
    def test_log_entry_invalid_port(self):
        """Test LogEntry with invalid port"""
        with pytest.raises(ValueError):
            LogEntry(
                timestamp=datetime.now(),
                source_ip="192.168.1.1",
                destination_ip="8.8.8.8",
                port=70000,  # Invalid: > 65535
                protocol="TCP",
                bytes_sent=1024,
                bytes_received=2048,
                duration=5.0,
                source_port=None,
                destination_port=None,
                event_type=None,
                failed_login_attempts=None,
                country=None,
                severity=None,
                is_anomaly=None
            )
    
    def test_log_batch(self):
        """Test LogBatch creation"""
        logs = LogBatch(
            logs=[
                LogEntry(
                    timestamp=datetime.now(),
                    source_ip="192.168.1.1",
                    destination_ip="8.8.8.8",
                    port=443,
                    protocol="TCP",
                    bytes_sent=1024,
                    bytes_received=2048,
                    duration=5.0,
                    source_port=None,
                    destination_port=None,
                    event_type=None,
                    failed_login_attempts=None,
                    country=None,
                    severity=None,
                    is_anomaly=None
                )
            ]
        )
        assert len(logs.logs) == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
