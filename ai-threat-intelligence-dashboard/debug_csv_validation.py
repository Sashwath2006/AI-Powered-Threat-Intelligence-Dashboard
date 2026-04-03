#!/usr/bin/env python3
"""
CSV Validation and Debugging Utility

Use this script to validate and debug your CSV files before uploading them
to the threat intelligence system.

Usage:
    python debug_csv_validation.py path/to/your/file.csv
    
Example:
    python debug_csv_validation.py ml/data/advanced_logs.csv
"""

import sys
import pandas as pd
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)-8s | %(message)s')
logger = logging.getLogger(__name__)


def print_header(title):
    """Print formatted header"""
    print(f"\n{'='*70}\n  {title}\n{'='*70}\n")


def analyze_csv(filepath):
    """Comprehensive CSV analysis"""
    
    path = Path(filepath)
    if not path.exists():
        logger.error(f"File not found: {filepath}")
        return False
    
    if not path.suffix.lower() == '.csv':
        logger.error(f"Not a CSV file: {filepath}")
        return False
    
    print_header("CSV VALIDATION REPORT")
    
    try:
        # Read CSV
        logger.info(f"Reading file: {filepath}")
        df = pd.read_csv(filepath)
        
        # 1. Dataset Overview
        print_header("[1] DATASET OVERVIEW")
        logger.info(f"File loaded successfully")
        logger.info(f"Shape: {len(df)} rows x {len(df.columns)} columns")
        logger.info(f"Memory: {df.memory_usage(deep=True).sum() / 1024:.2f} KB")
        
        # 2. Column Information
        print_header("[2] COLUMN INFORMATION")
        logger.info(f"Found {len(df.columns)} columns:")
        for i, col in enumerate(df.columns, 1):
            dtype = df[col].dtype
            non_null = df[col].notna().sum()
            null_count = df[col].isna().sum()
            logger.info(f"  {i:2}. {col:25} | {str(dtype):10} | Non-null: {non_null:4} | Null: {null_count:4}")
        
        # 3. Core Required Columns
        print_header("[3] CORE REQUIRED COLUMNS")
        core_required = [
            "timestamp", "source_ip", "destination_ip", "protocol",
            "bytes_sent", "bytes_received", "duration"
        ]
        
        missing_core = []
        for col in core_required:
            if col in df.columns:
                logger.info(f"  [OK] {col}")
            else:
                logger.error(f"  [MISSING] {col}")
                missing_core.append(col)
        
        if missing_core:
            logger.error(f"\nMissing {len(missing_core)} core columns: {', '.join(missing_core)}")
            return False
        else:
            logger.info(f"\nAll core columns present!")
        
        # 4. Port Column Detection
        print_header("[4] PORT COLUMN DETECTION")
        
        if 'source_port' in df.columns and 'destination_port' in df.columns:
            logger.info(f"Found source_port and destination_port (source/dest format)")
        elif 'port' in df.columns:
            logger.info(f"Found port (single port format)")
        else:
            logger.warning(f"No port columns found (port, source_port, or destination_port)")
        
        # 5. Sample Data Preview
        print_header("[5] SAMPLE DATA PREVIEW")
        logger.info(f"First 3 rows:")
        print(df.head(3).to_string())
        
        # 6. Data Type Validation
        print_header("[6] DATA TYPE VALIDATION")
        
        numeric_check = {
            'bytes_sent': 'int/float',
            'bytes_received': 'int/float',
            'duration': 'float',
        }
        
        if 'source_port' in df.columns:
            numeric_check['source_port'] = 'int (0-65535)'
        if 'destination_port' in df.columns:
            numeric_check['destination_port'] = 'int (0-65535)'
        if 'port' in df.columns:
            numeric_check['port'] = 'int (0-65535)'
        
        for col, expected_type in numeric_check.items():
            if col in df.columns:
                try:
                    numeric_vals = pd.to_numeric(df[col], errors='coerce')
                    invalid_count = numeric_vals.isna().sum()
                    if invalid_count == 0:
                        logger.info(f"  [OK] {col:25} | {expected_type:15} | All valid")
                    else:
                        logger.warning(f"  [WARN] {col:25} | {expected_type:15} | {invalid_count} invalid")
                except Exception as e:
                    logger.error(f"  [ERROR] {col:25} | {expected_type:15} | {str(e)}")
        
        # 7. Missing Values Analysis
        print_header("[7] MISSING VALUES ANALYSIS")
        missing_data = df.isnull().sum()
        has_missing = (missing_data > 0).any()
        
        if has_missing:
            logger.warning(f"Found missing values:")
            for col, count in missing_data[missing_data > 0].items():
                pct = (count / len(df)) * 100
                logger.warning(f"  [WARN] {col:25} | {count:4} rows ({pct:5.1f}%)")
        else:
            logger.info(f"No missing values found")
        
        # 8. Data Quality Metrics
        print_header("[8] DATA QUALITY METRICS")
        
        if 'timestamp' in df.columns:
            try:
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                logger.info(f"  [OK] Timestamps: Valid datetime format")
                logger.info(f"       Range: {df['timestamp'].min()} to {df['timestamp'].max()}")
            except:
                logger.error(f"  [ERROR] Timestamps: Invalid format")
        
        for ip_col in ['source_ip', 'destination_ip']:
            if ip_col in df.columns:
                valid_ips = df[ip_col].str.match(r'^(\d{1,3}\.){3}\d{1,3}$').sum()
                logger.info(f"  [OK] {ip_col:20} | {valid_ips}/{len(df)} valid IPs")
        
        for port_col in ['port', 'source_port', 'destination_port']:
            if port_col in df.columns:
                df_temp = df.copy()
                df_temp[port_col] = pd.to_numeric(df_temp[port_col], errors='coerce')
                valid_ports = ((df_temp[port_col] >= 0) & (df_temp[port_col] <= 65535)).sum()
                invalid_ports = df_temp[port_col].isna().sum()
                logger.info(f"  [OK] {port_col:20} | {valid_ports} valid (0-65535), {invalid_ports} invalid")
        
        # 9. Optional Fields Detection
        print_header("[9] OPTIONAL FIELDS (EXTENDED SCHEMA)")
        optional_fields = [
            'event_type', 'failed_login_attempts', 'country', 'severity', 'is_anomaly'
        ]
        
        found_optional = []
        for field in optional_fields:
            if field in df.columns:
                logger.info(f"  [OK] {field}")
                found_optional.append(field)
        
        if found_optional:
            logger.info(f"\nFound {len(found_optional)} optional fields (will enhance ML model)")
        else:
            logger.info(f"No optional fields found (that's OK, using core fields only)")
        
        # 10. ML Feature Readiness
        print_header("[10] ML FEATURE READINESS")
        
        ml_features = {
            'port (source/dest)': ['port', 'source_port', 'destination_port'],
            'bytes_sent': ['bytes_sent'],
            'bytes_received': ['bytes_received'],
            'duration': ['duration'],
            'failed_login_attempts': ['failed_login_attempts']
        }
        
        ready_count = 0
        for feature_name, cols in ml_features.items():
            has_feature = any(col in df.columns for col in cols)
            if has_feature:
                logger.info(f"  [OK] {feature_name}")
                ready_count += 1
            else:
                logger.warning(f"  [WARN] {feature_name} - NOT FOUND")
        
        logger.info(f"\nML Readiness: {ready_count}/{len(ml_features)} features available")
        
        # 11. Final Verdict
        print_header("FINAL VERDICT")
        
        all_valid = (not missing_core and not has_missing)
        
        if all_valid:
            logger.info("CSV IS PRODUCTION-READY")
            logger.info("This file can be uploaded and analyzed immediately!")
            return True
        else:
            logger.warning("CSV HAS ISSUES - REVIEW ERROR MESSAGES ABOVE")
            logger.warning("Fix the issues before uploading to the system")
            return False
            
    except Exception as e:
        logger.error(f"Error reading CSV: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main entry point"""
    
    if len(sys.argv) < 2:
        print_header("CSV VALIDATION TOOL - USAGE")
        logger.info("Validates CSV files for the threat intelligence system")
        logger.info("\nUsage:")
        logger.info("  python debug_csv_validation.py /path/to/your/file.csv")
        logger.info("\nExample:")
        logger.info("  python debug_csv_validation.py ml/data/sample_logs.csv")
        logger.info("  python debug_csv_validation.py ml/data/advanced_logs.csv")
        logger.info("\n" + "="*70)
        sys.exit(1)
    
    csv_file = sys.argv[1]
    success = analyze_csv(csv_file)
    
    print_header("END OF REPORT")
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
