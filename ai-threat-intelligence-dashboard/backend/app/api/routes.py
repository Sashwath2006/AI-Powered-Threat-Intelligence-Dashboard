"""API Routes and Endpoints"""
from fastapi import APIRouter, HTTPException, status
from typing import List
from datetime import datetime
import numpy as np

from app.models.schemas import (
    LogBatch,
    AnalysisResponse,
    AnomalyResult,
    SeverityLevel,
    ErrorResponse
)
from app.ml.anomaly_detector import (
    AnomalyDetector,
    extract_features,
    score_severity
)
from app.utils.logger import get_logger
from typing import Optional
from app.config import get_settings

logger = get_logger(__name__)
settings = get_settings()
router = APIRouter()

# Global detector instance (loaded on startup)
detector: Optional[AnomalyDetector] = None


def set_detector(anomaly_detector: AnomalyDetector) -> None:
    """Set the anomaly detector instance"""
    global detector
    detector = anomaly_detector


@router.post(
    "/analyze",
    response_model=AnalysisResponse,
    summary="Analyze logs for anomalies",
    tags=["Analysis"]
)
async def analyze_logs(log_batch: LogBatch) -> AnalysisResponse:
    """
    Analyze a batch of logs for anomalies
    
    **Request:**
    - logs: List of log entries with timestamp, IPs, port, protocol, bytes, duration
    
    **Response:**
    - total_logs: Number of logs analyzed
    - anomalies_detected: Count of detected anomalies
    - anomaly_percentage: Percentage of total logs
    - results: Detailed anomaly results for each log
    
    **Example:**
    ```json
    {
      "logs": [
        {
          "timestamp": "2024-01-01T12:00:00Z",
          "source_ip": "192.168.1.100",
          "destination_ip": "8.8.8.8",
          "port": 443,
          "protocol": "TCP",
          "bytes_sent": 1024,
          "bytes_received": 2048,
          "duration": 5.5
        }
      ]
    }
    ```
    """
    try:
        # Validate detector is initialized
        if detector is None:
            logger.error("CRITICAL: ML detector not initialized")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="ML model not initialized"
            )
        
        # Validate we have logs
        if not log_batch.logs or len(log_batch.logs) == 0:
            logger.error("CRITICAL: Empty logs batch received")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No logs provided for analysis"
            )
        
        logger.info(f"BACKEND PIPELINE START: Received {len(log_batch.logs)} logs")
        
        # Prepare logs as dictionaries for feature extraction
        logs_list = [log.model_dump() for log in log_batch.logs]
        logger.info(f"  -> Converted to dict format: {len(logs_list)} logs")
        
        # Verify first log has CORE required fields
        if logs_list:
            first_log = logs_list[0]
            # CORE required: these should always be present from frontend validation
            core_required = ['bytes_sent', 'bytes_received', 'duration']
            missing_core = [f for f in core_required if f not in first_log or first_log.get(f) is None]
            if missing_core:
                logger.error(f"  CRITICAL MISSING fields: {missing_core}")
                logger.error(f"  Available fields: {list(first_log.keys())}")
                raise ValueError(f"Missing CRITICAL fields in logs: {missing_core}")
            
            # PORT is flexible - comes from port, source_port, or destination_port
            has_port = any(f in first_log for f in ['port', 'source_port', 'destination_port'])
            if not has_port:
                logger.warning(f"  WARNING: No port data available, using zeros for ML features")
        
        # Extract features
        logger.info(f"  -> Extracting features from {len(logs_list)} logs")
        X = extract_features(logs_list)
        
        # Predict anomalies
        predictions, scores = detector.predict(X)
        
        # Build results
        results = []
        anomaly_count = 0
        
        for idx, (log, pred, score) in enumerate(zip(log_batch.logs, predictions, scores)):
            is_anomaly = pred == -1
            if is_anomaly:
                anomaly_count += 1
            
            severity = SeverityLevel(score_severity(float(score)))
            
            # Build result with flexible port handling
            result_data = {
                "log_index": idx,
                "timestamp": log.timestamp,
                "source_ip": log.source_ip,
                "destination_ip": log.destination_ip,
                "protocol": log.protocol,
                "bytes_sent": log.bytes_sent,
                "bytes_received": log.bytes_received,
                "duration": log.duration,
                "is_anomaly": is_anomaly,
                "anomaly_score": float(score),
                "severity": severity
            }
            
            # Add port information (support multiple formats)
            if log.source_port is not None:
                result_data["source_port"] = log.source_port
            if log.destination_port is not None:
                result_data["destination_port"] = log.destination_port
            if log.port is not None:
                result_data["port"] = log.port
            
            # Add optional extended fields
            if log.event_type is not None:
                result_data["event_type"] = log.event_type
            if log.failed_login_attempts is not None:
                result_data["failed_login_attempts"] = log.failed_login_attempts
            if log.country is not None:
                result_data["country"] = log.country
            
            result = AnomalyResult(**result_data)
            results.append(result)
        
        anomaly_percentage = (anomaly_count / len(log_batch.logs)) * 100
        
        logger.info(
            f"Analysis complete: {len(log_batch.logs)} logs, "
            f"{anomaly_count} anomalies ({anomaly_percentage:.2f}%)"
        )
        
        return AnalysisResponse(
            status="success",
            total_logs=len(log_batch.logs),
            anomalies_detected=anomaly_count,
            anomaly_percentage=anomaly_percentage,
            results=results
        )
        
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        # Re-raise HTTP exceptions without catching them
        raise
    except Exception as e:
        import traceback
        logger.error(f"Unexpected error during analysis: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during analysis"
        )


@router.get(
    "/stats",
    summary="Get detector statistics",
    tags=["Status"]
)
async def get_stats() -> dict:
    """
    Get statistics about the detector
    
    **Response:**
    - model_trained: Whether model has been trained
    - contamination: Contamination parameter
    """
    try:
        if detector is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="ML model not initialized"
            )
        
        return {
            "status": "operational",
            "model_trained": detector.is_trained,
            "contamination": detector.contamination,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        import traceback
        logger.error(f"Error getting stats: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving statistics"
        )


__all__ = ["router", "set_detector"]
