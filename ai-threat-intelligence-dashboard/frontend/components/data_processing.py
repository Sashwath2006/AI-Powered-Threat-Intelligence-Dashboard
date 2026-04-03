"""
Data Processing Utilities
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from datetime import datetime


"""Data processing and validation utilities for logs"""
import pandas as pd
import logging
from typing import Tuple, Dict, List, Any, Optional, Union

logger = logging.getLogger(__name__)


def get_dataset_columns(df: pd.DataFrame) -> List[str]:
    """Get list of all columns in dataset"""
    return list(df.columns)


def detect_column_schema(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Detect which port columns are available in the dataset
    Returns: {'port_type': 'source_dest'|'single', 'source_col': str, 'dest_col': str, 'single_col': str, 'has_source_dest': bool}
    """
    columns = set(df.columns)
    
    # Check for source/destination port format
    if 'source_port' in columns and 'destination_port' in columns:
        logger.info("✅ Detected source_port/destination_port format")
        return {
            'port_type': 'source_dest',
            'source_col': 'source_port',
            'dest_col': 'destination_port',
            'has_source_dest': True
        }
    
    # Check for single port format
    elif 'port' in columns:
        logger.info("✅ Detected single port format")
        return {
            'port_type': 'single',
            'single_col': 'port',
            'source_col': None,
            'dest_col': None,
            'has_source_dest': False
        }
    
    else:
        logger.warning("⚠️ No port columns detected (source_port, destination_port, or port)")
        return {
            'port_type': 'unknown',
            'source_col': None,
            'dest_col': None,
            'has_source_dest': False
        }


def validate_log_csv(df: pd.DataFrame) -> Tuple[bool, str, Dict[str, Any]]:
    """
    Validate CSV has required columns with detailed debugging
    
    Returns:
        (is_valid: bool, message: str, debug_info: dict)
    """
    debug_info = {
        'rows': len(df),
        'columns': get_dataset_columns(df),
        'schema': None,
        'missing': []
    }
    
    # Log dataset info
    logger.info(f"📊 Dataset shape: {len(df)} rows, {len(df.columns)} columns")
    logger.info(f"📋 Columns: {', '.join(df.columns)}")
    
    # CORE required columns (must exist)
    core_required = [
        "timestamp",
        "source_ip",
        "destination_ip",
        "protocol",
        "bytes_sent",
        "bytes_received"
    ]
    
    # OPTIONAL columns (nice to have, won't fail if missing)
    optional_cols = [
        "duration",
        "port",
        "source_port",
        "destination_port",
        "event_type",
        "failed_login_attempts",
        "country",
        "severity",
        "is_anomaly"
    ]
    
    # Check CORE columns - strict validation
    missing_core = [col for col in core_required if col not in df.columns]
    if missing_core:
        msg = f"❌ FATAL: Missing CORE columns: {missing_core}"
        logger.error(msg)
        debug_info['missing'] = missing_core
        return False, msg, debug_info
    
    # Check OPTIONAL columns - log warnings only
    missing_optional = [col for col in optional_cols if col not in df.columns]
    if missing_optional:
        logger.info(f"⚠️ Optional columns not found: {missing_optional}")
        logger.info(f"   These will be engineered or set to defaults")
    
    # Detect port schema
    schema = detect_column_schema(df)
    debug_info['schema'] = schema
    
    if schema['port_type'] == 'unknown':
        msg = "⚠️ WARNING: No port columns found. ML model needs port data."
        logger.warning(msg)
        # Don't fail validation - port might be optional
    
    logger.info(f"✅ CSV validation passed")
    return True, "✅ CSV is valid", debug_info


def clean_log_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and prepare log data with intelligent preprocessing:
    - Removes duplicates and empty rows
    - Converts numeric columns to proper types
    - Engineers missing duration from available features
    - Handles optional columns gracefully
    """
    df = df.copy()
    original_len = len(df)
    
    logger.info(f"🧹 Starting data cleaning on {original_len} rows")
    
    # Remove duplicates
    df = df.drop_duplicates()
    logger.info(f"   - After removing duplicates: {len(df)} rows")
    
    # Remove rows with all NaN values
    df = df.dropna(how='all')
    logger.info(f"   - After removing empty rows: {len(df)} rows")
    
    # CRITICAL: Convert core numeric columns
    core_numeric = ['bytes_sent', 'bytes_received']
    for col in core_numeric:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Handle port columns - multiple formats supported
    for port_col in ['source_port', 'destination_port', 'port']:
        if port_col in df.columns:
            df[port_col] = pd.to_numeric(df[port_col], errors='coerce')
    
    # Handle optional numeric fields
    optional_numeric = ['failed_login_attempts']
    for col in optional_numeric:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # ENGINEER DURATION if missing
    if 'duration' not in df.columns:
        logger.info(f"   - Duration column missing, engineering from available features...")
        
        # Strategy: Estimate duration based on data volume and failed login attempts
        # duration ~ (bytes_sent + bytes_received) / bandwidth + failed_attempts_penalty
        base_duration = (df['bytes_sent'] + df['bytes_received']) / 1000.0  # Rough estimate
        base_duration = base_duration.clip(lower=0.1, upper=300)  # Realistic bounds: 0.1 to 300 seconds
        
        # Add penalty for failed login attempts if available
        if 'failed_login_attempts' in df.columns:
            penalty = df['failed_login_attempts'].fillna(0) * 0.5  # 0.5 sec per failed attempt
            df['duration'] = base_duration + penalty
            logger.info(f"   - Duration engineered with failed_login_attempts penalty")
        else:
            df['duration'] = base_duration
            logger.info(f"   - Duration engineered from bytes_sent + bytes_received")
        
        logger.info(f"   - Duration range: {df['duration'].min():.2f}s to {df['duration'].max():.2f}s")
    else:
        # Convert existing duration to float
        df['duration'] = pd.to_numeric(df['duration'], errors='coerce')
        logger.info(f"   - Duration column exists: {df['duration'].min():.2f}s to {df['duration'].max():.2f}s")
    
    # REMOVE rows with NaN in CORE numeric columns only
    core_required_numeric = ['bytes_sent', 'bytes_received', 'duration']
    df = df.dropna(subset=core_required_numeric, how='any')
    logger.info(f"   - After cleaning numeric values: {len(df)} rows")
    
    cleaned_len = len(df)
    removed = original_len - cleaned_len
    pct = (removed / original_len * 100) if original_len > 0 else 0
    logger.info(f"✅ Data cleaning complete: {removed} rows removed ({pct:.1f}%)")
    logger.info(f"   - Final dataset: {len(df)} rows ready for analysis")
    
    return df


def safe_get_port(row: Union[Dict[str, Any], pd.Series]) -> Optional[int]:
    """
    Safely get port value from row, supporting multiple formats
    
    Try in order: source_port, destination_port, port
    
    Args:
        row: Either a dictionary (from direct access) or pandas Series (from iterrows)
        
    Returns:
        Port number (0-65535) or None if not found/invalid
    """
    for port_col in ['source_port', 'destination_port', 'port']:
        if port_col in row and row[port_col] is not None:
            try:
                val = int(row[port_col])
                if 0 <= val <= 65535:
                    return val
            except (ValueError, TypeError):
                continue
    
    return None


def parse_csv_to_logs(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Convert CSV DataFrame to API format with comprehensive error handling and debugging
    """
    logs = []
    errors = []
    
    logger.info(f"\nDATA PROCESSING PIPELINE START")
    logger.info(f"  Input DataFrame shape: {df.shape}")
    logger.info(f"  Input columns: {list(df.columns)}")
    
    # First validate dataset
    is_valid, msg, debug_info = validate_log_csv(df)
    if not is_valid:
        logger.error(f"  VALIDATION FAILED: {msg}")
        logger.error(f"  Returning empty logs")
        return {"logs": [], "errors": [msg], "debug": debug_info}
    
    logger.info(f"  Validation passed")
    
    # Clean data
    df_before_clean = len(df)
    df = clean_log_data(df)
    df_after_clean = len(df)
    logger.info(f"  After cleaning: {df_before_clean} → {df_after_clean} rows (dropped {df_before_clean - df_after_clean})")
    
    if df_after_clean == 0:
        logger.error(f"  CRITICAL: All rows dropped during cleaning!")
        return {"logs": [], "errors": ["All rows were dropped during data cleaning"], "debug": debug_info}
    
    logger.info(f"  Parsing {df_after_clean} rows...")
    
    row_count = 0
    skip_count = 0
    
    for idx, row in df.iterrows():
        try:
            # Core fields (required) - these MUST exist
            log = {
                "timestamp": str(row["timestamp"]),
                "source_ip": str(row["source_ip"]),
                "destination_ip": str(row["destination_ip"]),
                "protocol": str(row["protocol"]),
                "bytes_sent": int(row["bytes_sent"]),
                "bytes_received": int(row["bytes_received"]),
                "duration": float(row["duration"])  # NOW ALWAYS EXISTS (engineered if missing)
            }
            
            # Handle ports - support multiple formats
            port = safe_get_port(row)
            if port is not None:
                if 'source_port' in row and row['source_port'] is not None:
                    log["source_port"] = int(row["source_port"])
                
                if 'destination_port' in row and row['destination_port'] is not None:
                    log["destination_port"] = int(row["destination_port"])
                
                # Single port format (backward compatibility)
                if 'port' in row and row['port'] is not None:
                    log["port"] = int(row["port"])
                elif 'source_port' in row and row['source_port'] is not None:
                    log["port"] = int(row["source_port"])  # Use source_port as fallback
            
            # Optional extended fields (safe access with .get())
            if "event_type" in row and pd.notna(row["event_type"]):
                log["event_type"] = str(row["event_type"])
            
            if "failed_login_attempts" in row and pd.notna(row["failed_login_attempts"]):
                log["failed_login_attempts"] = int(row["failed_login_attempts"])
            
            if "country" in row and pd.notna(row["country"]):
                log["country"] = str(row["country"])
            
            if "severity" in row and pd.notna(row["severity"]):
                log["severity"] = str(row["severity"])
            
            if "is_anomaly" in row and pd.notna(row["is_anomaly"]):
                log["is_anomaly"] = bool(row["is_anomaly"])
            
            logs.append(log)
            row_count += 1
            
        except Exception as e:
            error_msg = f"Row {idx}: {str(e)}"
            logger.debug(f"    Row {idx} error: {str(e)}")
            errors.append(error_msg)
            skip_count += 1
            continue
    
    logger.info(f"  Parsed {row_count} valid rows, skipped {skip_count} rows")
    
    if not logs:
        logger.error(f"  CRITICAL: No valid logs parsed!")
        logger.error(f"  Parse errors: {errors}")
        return {"logs": [], "errors": errors, "debug": debug_info}
    
    logger.info(f"SUCCESS: Parsed {len(logs)} logs")
    logger.info(f"  First log keys: {list(logs[0].keys())}")
    
    return {
        "logs": logs,
        "errors": errors,
        "debug": {
            "total_rows": df_after_clean,
            "valid_logs": len(logs),
            "skipped": skip_count,
            "schema": debug_info['schema']
        }
    }


def summarize_results(results: Dict) -> Dict:
    """Summarize analysis results"""
    results_df = pd.DataFrame(results["results"])
    
    summary = {
        "total_logs": results["total_logs"],
        "anomalies_detected": results["anomalies_detected"],
        "anomaly_percentage": results["anomaly_percentage"],
        "severity_breakdown": {
            "CRITICAL": len(results_df[results_df["severity"] == "CRITICAL"]),
            "HIGH": len(results_df[results_df["severity"] == "HIGH"]),
            "MEDIUM": len(results_df[results_df["severity"] == "MEDIUM"]),
            "LOW": len(results_df[results_df["severity"] == "LOW"]),
        },
        "average_anomaly_score": float(results_df["anomaly_score"].mean()),
        "max_anomaly_score": float(results_df["anomaly_score"].max()),
        "min_anomaly_score": float(results_df["anomaly_score"].min()),
    }
    
    return summary


def get_top_anomalies(results: Dict, top_n: int = 10) -> List[Dict]:
    """Get top N anomalies by score"""
    results_df = pd.DataFrame(results["results"])
    top_anomalies = results_df.nlargest(top_n, "anomaly_score")
    return top_anomalies.to_dict("records")


def get_anomalies_by_severity(results: Dict) -> Dict[str, List[Dict]]:
    """Group anomalies by severity"""
    results_df = pd.DataFrame(results["results"])
    anomalies = results_df[results_df["is_anomaly"]]
    
    grouped = {}
    for severity in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
        severity_data = anomalies[anomalies["severity"] == severity]
        grouped[severity] = severity_data.to_dict("records")
    
    return grouped


def generate_timestamp_series(results: Dict) -> pd.Series:
    """Generate time series of anomalies"""
    results_df = pd.DataFrame(results["results"])
    results_df["timestamp"] = pd.to_datetime(results_df["timestamp"])
    
    # Count anomalies per hour
    time_series = results_df[results_df["is_anomaly"]].set_index("timestamp").resample("H").size()
    
    return time_series
