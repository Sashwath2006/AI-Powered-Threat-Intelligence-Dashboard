"""Anomaly Detection using Isolation Forest"""
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from typing import List, Tuple, Dict, Any
import pickle
import joblib
from pathlib import Path
from app.utils.logger import get_logger

logger = get_logger(__name__)


class AnomalyDetector:
    """Isolation Forest-based anomaly detector"""
    
    def __init__(self, contamination: float = 0.1):
        """
        Initialize anomaly detector
        
        Args:
            contamination: Expected proportion of anomalies (0.0 - 0.5)
        """
        self.contamination = contamination
        self.model = IsolationForest(
            contamination=contamination,
            random_state=42,
            n_estimators=100
        )
        self.scaler = StandardScaler()
        self.is_trained = False
        self.feature_names = None
        
    def train(self, X: np.ndarray) -> None:
        """
        Train the Isolation Forest model
        
        Args:
            X: Training data (n_samples, n_features)
        """
        try:
            # Normalize features
            X_scaled = self.scaler.fit_transform(X)
            
            # Train model
            self.model.fit(X_scaled)
            self.is_trained = True
            logger.info(f"Model trained on {X.shape[0]} samples with {X.shape[1]} features")
        except Exception as e:
            logger.error(f"Error during model training: {str(e)}")
            raise
    
    def predict(self, X: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Predict anomalies
        
        Args:
            X: Data to predict (n_samples, n_features)
            
        Returns:
            Tuple of (predictions, scores)
            - predictions: -1 for anomaly, 1 for normal
            - scores: Anomaly scores (0.0 - 1.0)
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before prediction")
        
        try:
            # Normalize using training data's scaler
            X_scaled = self.scaler.transform(X)
            
            # Get predictions and scores
            predictions = self.model.predict(X_scaled)
            scores = -self.model.score_samples(X_scaled)  # Negate for positive anomaly scores
            
            # Normalize scores to 0-1 range
            scores_normalized = (scores - scores.min()) / (scores.max() - scores.min() + 1e-10)
            
            logger.info(f"Predicted {np.sum(predictions == -1)} anomalies out of {len(predictions)} samples")
            return predictions, scores_normalized
        except Exception as e:
            logger.error(f"Error during prediction: {str(e)}")
            raise
    
    def save_model(self, path: str) -> None:
        """
        Save trained model to disk
        
        Args:
            path: Path to save model (e.g., 'model.pkl')
        """
        if not self.is_trained:
            raise ValueError("Cannot save untrained model")
        
        try:
            Path(path).parent.mkdir(parents=True, exist_ok=True)
            with open(path, 'wb') as f:
                pickle.dump({'model': self.model, 'scaler': self.scaler}, f)
            logger.info(f"Model saved to {path}")
        except Exception as e:
            logger.error(f"Error saving model: {str(e)}")
            raise
    
    def load_model(self, path: str) -> None:
        """
        Load trained model from disk
        
        Args:
            path: Path to model file
        """
        try:
            with open(path, 'rb') as f:
                data = pickle.load(f)
            self.model = data['model']
            self.scaler = data['scaler']
            self.is_trained = True
            logger.info(f"Model loaded from {path}")
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise


def extract_features(logs: List[Dict[str, Any]]) -> np.ndarray:
    """
    Extract numerical features from logs with flexible schema support
    
    Core features (4):
    - port (from port, source_port, or destination_port)
    - bytes_sent
    - bytes_received
    - duration
    
    Args:
        logs: List of log dictionaries
        
    Returns:
        Feature matrix as numpy array (n_rows, 4)
    """
    df = pd.DataFrame(logs)
    logger.info(f"🔍 Extracting features from {len(df)} logs")
    logger.info(f"   Available columns: {list(df.columns)}")
    
    features = []
    
    # Try to get port data - support multiple formats
    if 'port' in df.columns:
        port_feature = df['port'].fillna(0).astype(float).values
        logger.info("   Using 'port' column")
    elif 'source_port' in df.columns:
        port_feature = df['source_port'].fillna(0).astype(float).values
        logger.info("   Using 'source_port' column")
    elif 'destination_port' in df.columns:
        port_feature = df['destination_port'].fillna(0).astype(float).values
        logger.info("   Using 'destination_port' column")
    else:
        logger.warning("   No port columns found, using zeros")
        port_feature = np.zeros(len(df))
    
    features.append(port_feature)
    
    # Bytes sent - required for ML
    if 'bytes_sent' in df.columns:
        features.append(df['bytes_sent'].fillna(0).astype(float).values)
    else:
        logger.warning("   Missing 'bytes_sent', using zeros")
        features.append(np.zeros(len(df)))
    
    # Bytes received - required for ML
    if 'bytes_received' in df.columns:
        features.append(df['bytes_received'].fillna(0).astype(float).values)
    else:
        logger.warning("   Missing 'bytes_received', using zeros")
        features.append(np.zeros(len(df)))
    
    # Duration - required for ML
    if 'duration' in df.columns:
        features.append(df['duration'].fillna(0).astype(float).values)
    else:
        logger.warning("   Missing 'duration', using zeros")
        features.append(np.zeros(len(df)))
    
    # Stack features as columns (always 4 core features)
    X = np.column_stack(features)
    logger.info(f"   Created feature matrix: {X.shape}")
    
    return X


def score_severity(anomaly_score: float) -> str:
    """
    Determine severity level based on anomaly score
    
    Args:
        anomaly_score: Score from 0.0 to 1.0
        
    Returns:
        Severity level string
    """
    if anomaly_score >= 0.90:
        return "CRITICAL"
    elif anomaly_score >= 0.75:
        return "HIGH"
    elif anomaly_score >= 0.50:
        return "MEDIUM"
    else:
        return "LOW"
