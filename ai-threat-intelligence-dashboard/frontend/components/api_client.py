"""
API Client for Backend Communication
"""
import requests
import pandas as pd
from typing import Dict, List, Optional, Tuple
import logging

logger = logging.getLogger(__name__)


class BackendClient:
    """Client for communicating with FastAPI backend"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.timeout = 30
    
    def check_health(self) -> bool:
        """Check if backend is online"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=2)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False
    
    def get_stats(self) -> Optional[Dict]:
        """Get detector statistics"""
        try:
            response = requests.get(
                f"{self.base_url}/api/stats",
                timeout=self.timeout
            )
            return response.json() if response.status_code == 200 else None
        except Exception as e:
            logger.error(f"Failed to get stats: {e}")
            return None
    
    def analyze_logs(self, logs_data: Dict) -> Optional[Dict]:
        """Analyze logs for anomalies"""
        try:
            response = requests.post(
                f"{self.base_url}/api/analyze",
                json=logs_data,
                timeout=self.timeout
            )
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"API error: {response.status_code}")
                return None
        except Exception as e:
            logger.error(f"Failed to analyze logs: {e}")
            return None
    
    def analyze_csv(self, df: pd.DataFrame) -> Optional[Dict]:
        """
        Analyze logs from DataFrame with flexible schema support
        """
        from components.data_processing import parse_csv_to_logs
        
        try:
            # Use the comprehensive parsing function
            parse_result = parse_csv_to_logs(df)
            
            if not parse_result.get('logs'):
                logger.error(f"No valid logs to analyze. Errors: {parse_result.get('errors', [])}")
                return None
            
            # Call API with parsed logs
            return self.analyze_logs({"logs": parse_result['logs']})
            
        except Exception as e:
            logger.error(f"Failed to analyze CSV: {e}")
            return None
            return None


# Global client instance
_client: Optional[BackendClient] = None


def get_client(base_url: str = "http://localhost:8000") -> BackendClient:
    """Get or create backend client"""
    global _client
    if _client is None:
        _client = BackendClient(base_url)
    elif _client.base_url != base_url:
        _client = BackendClient(base_url)
    return _client
