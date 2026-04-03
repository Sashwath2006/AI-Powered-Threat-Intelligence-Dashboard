"""Pydantic Data Models for API"""
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from datetime import datetime
from enum import Enum
import pandas as pd


class SeverityLevel(str, Enum):
    """Threat severity levels"""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class LogEntry(BaseModel):
    """Single log entry - supports both port formats"""
    timestamp: datetime
    source_ip: str
    destination_ip: str
    source_port: Optional[int] = Field(None, ge=0, le=65535)  # For source_port format
    destination_port: Optional[int] = Field(None, ge=0, le=65535)  # For destination_port format
    port: Optional[int] = Field(None, ge=0, le=65535)  # For backward compatibility
    protocol: str
    bytes_sent: int = Field(..., ge=0)
    bytes_received: int = Field(..., ge=0)
    duration: float = Field(..., ge=0)
    # Optional fields from extended schema
    event_type: Optional[str] = None
    failed_login_attempts: Optional[int] = Field(None, ge=0)
    country: Optional[str] = None
    severity: Optional[str] = None
    is_anomaly: Optional[bool] = None
    
    @field_validator('source_port', 'destination_port', 'port', mode='before')
    @classmethod
    def validate_ports(cls, v):
        """Ensure port is valid integer or None"""
        if v is None or v == '' or pd.isna(v):
            return None
        try:
            return int(v)
        except (ValueError, TypeError):
            return None


class LogBatch(BaseModel):
    """Batch of logs for analysis"""
    logs: List[LogEntry] = Field(..., min_length=1)


class AnomalyResult(BaseModel):
    """Single anomaly detection result - supports both port formats"""
    log_index: int
    timestamp: datetime
    source_ip: str
    destination_ip: str
    source_port: Optional[int] = None  # For source_port format
    destination_port: Optional[int] = None  # For destination_port format
    port: Optional[int] = None  # For backward compatibility
    protocol: str
    bytes_sent: int
    bytes_received: int
    duration: float
    # Optional extended fields
    event_type: Optional[str] = None
    failed_login_attempts: Optional[int] = None
    country: Optional[str] = None
    
    is_anomaly: bool
    anomaly_score: float = Field(..., ge=0.0, le=1.0)
    severity: SeverityLevel


class AnalysisResponse(BaseModel):
    """Response from analysis endpoint"""
    status: str = "success"
    total_logs: int
    anomalies_detected: int
    anomaly_percentage: float
    results: List[AnomalyResult]
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class HealthCheck(BaseModel):
    """Health check response"""
    status: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    service: str = "Threat Intelligence API"


class ErrorResponse(BaseModel):
    """Error response"""
    status: str = "error"
    message: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
