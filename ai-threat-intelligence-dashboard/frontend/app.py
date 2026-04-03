"""
Main Streamlit Application - Threat Intelligence Dashboard
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from typing import cast
import requests
import json
from io import StringIO
import time
import logging

# Setup logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Page config
st.set_page_config(
    page_title="Threat Intelligence Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown(
    """
    <style>
    body {
        font-family: 'IBM Plex Mono', monospace;
    }
    .main {
        padding: 2rem 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ff0051;
    }
    .anomaly-high {
        color: #ff4444;
        font-weight: bold;
    }
    .anomaly-medium {
        color: #ffaa00;
        font-weight: bold;
    }
    .anomaly-low {
        color: #44aa44;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Constants
import os
BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")
DEMO_LOG_FILE = "../ml/data/sample_logs.csv"  # Correct path from frontend directory

# Initialize session state
if "analysis_results" not in st.session_state:
    st.session_state.analysis_results = None
if "backend_status" not in st.session_state:
    st.session_state.backend_status = None
if "uploaded_logs" not in st.session_state:
    st.session_state.uploaded_logs = None
if "logs_data" not in st.session_state:
    st.session_state.logs_data = None


# Utility Functions
@st.cache_data
def check_backend_health():
    """Check if backend is running"""
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=2)
        return response.status_code == 200
    except:
        return False


def analyze_logs(logs_data):
    """Send logs to backend for analysis with comprehensive debugging"""
    logger.info("FRONTEND PIPELINE START: analyze_logs called")
    
    try:
        # DEBUG: Log what we received
        logger.debug(f"  -> logs_data type: {type(logs_data)}")
        logger.debug(f"  -> logs_data keys: {list(logs_data.keys()) if logs_data else 'None'}")
        
        # Validate logs are not empty
        if not logs_data:
            st.error("❌ No logs data received from parser")
            logger.error("  CRITICAL: logs_data is None")
            return None
        
        if "logs" not in logs_data:
            st.error(f"❌ Invalid data format: missing 'logs' key. Got keys: {list(logs_data.keys())}")
            logger.error(f"  CRITICAL: missing 'logs' key in parsed data. Keys: {list(logs_data.keys())}")
            return None
        
        logs_list = logs_data.get("logs", [])
        errors = logs_data.get("errors", [])
        
        logger.info(f"  -> Parsed logs count: {len(logs_list)}")
        logger.info(f"  -> Parse errors count: {len(errors)}")
        
        if len(logs_list) == 0:
            error_msg = f"No valid logs to analyze. Errors: {errors}" if errors else "No logs parsed"
            st.error(f"❌ {error_msg}")
            logger.error(f"  CRITICAL: Empty logs list. Parse errors: {errors}")
            return None
        
        # Verify first log has required fields
        if logs_list:
            first_log = logs_list[0]
            required_fields = ['timestamp', 'source_ip', 'destination_ip', 'bytes_sent', 'bytes_received', 'duration']
            missing = [f for f in required_fields if f not in first_log]
            if missing:
                st.error(f"❌ Missing required fields in parsed logs: {missing}")
                logger.error(f"  CRITICAL: Missing fields {missing}. First log keys: {list(first_log.keys())}")
                return None
        
        log_count = len(logs_list)
        logger.info(f"  -> Sending {log_count} logs to backend")
        st.info(f"📤 Sending {log_count} logs to backend for analysis...")
        
        # Send to backend
        response = requests.post(
            f"{BACKEND_URL}/api/analyze",
            json=logs_data,
            timeout=30
        )
        
        logger.info(f"  -> Backend response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            results_count = len(result.get('results', []))
            logger.info(f"  -> SUCCESS: Got {results_count} results")
            return result
        else:
            error_detail = response.text
            try:
                error_json = response.json()
                error_detail = error_json.get("detail", error_detail)
            except:
                pass
            st.error(f"❌ Backend error {response.status_code}: {error_detail}")
            logger.error(f"  BACKEND ERROR {response.status_code}: {error_detail}")
            return None
            
    except Exception as e:
        st.error(f"❌ Error calling backend: {str(e)}")
        logger.exception(f"analyze_logs: Exception occurred: {str(e)}")
        return None


def parse_csv_to_logs(df):
    """Convert CSV DataFrame to API format - now in data_processing"""
    from components.data_processing import parse_csv_to_logs as parse_logs
    result = parse_logs(df)
    return result


def get_severity_color(severity):
    """Get color for severity level"""
    colors = {
        "CRITICAL": "#ff0000",
        "HIGH": "#ff6600",
        "MEDIUM": "#ffaa00",
        "LOW": "#00aa00"
    }
    return colors.get(severity, "#cccccc")


def get_severity_emoji(severity):
    """Get emoji for severity level"""
    emojis = {
        "CRITICAL": "🔴",
        "HIGH": "🟠",
        "MEDIUM": "🟡",
        "LOW": "🟢"
    }
    return emojis.get(severity, "⚪")


# Main Application
def main():
    # Header
    col1, col2, col3 = st.columns([1, 3, 1])
    with col1:
        st.write("")
    with col2:
        st.title("🛡️ Threat Intelligence Dashboard")
        st.markdown("### AI-Powered Anomaly Detection System")
    with col3:
        # Backend status indicator
        backend_available = check_backend_health()
        if backend_available:
            st.success("🟢 Backend Online", icon="✅")
        else:
            st.error("🔴 Backend Offline", icon="❌")
            st.info("Make sure backend is running on http://localhost:8000")

    st.divider()

    # Sidebar Configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        api_url = st.text_input(
            "Backend URL",
            value=BACKEND_URL,
            help="URL of the backend API server"
        )
        
        st.divider()
        
        # Upload mode - track previous mode to detect changes
        if "prev_upload_mode" not in st.session_state:
            st.session_state.prev_upload_mode = None
        
        upload_mode = st.radio(
            "Data Source",
            ["Upload CSV", "Use Sample Data", "Manual Entry"],
            help="Choose how to provide log data"
        )
        
        # Reset logs if mode changed
        if upload_mode != st.session_state.prev_upload_mode:
            st.session_state.logs_data = None
            st.session_state.prev_upload_mode = upload_mode
        
        st.divider()
        st.markdown("### 📊 Dashboard Info")
        st.markdown("""
        **How it works:**
        1. Upload log data (CSV format)
        2. Backend analyzes logs with ML
        3. View anomalies and statistics
        4. Export results for further analysis
        
        **Expected CSV columns:**
        - timestamp
        - source_ip
        - destination_ip
        - port
        - protocol
        - bytes_sent
        - bytes_received
        - duration
        """)

    # Main Content Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Analysis",
        "📈 Visualizations",
        "🔍 Details",
        "ℹ️ About"
    ])

    # TAB 1: Analysis
    with tab1:
        st.header("Log Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📤 Data Input")
            
            if upload_mode == "Upload CSV":
                uploaded_file = st.file_uploader(
                    "Upload CSV file",
                    type=["csv"],
                    help="CSV with columns: timestamp, source_ip, destination_ip, port, protocol, bytes_sent, bytes_received, duration"
                )
                
                if uploaded_file:
                    try:
                        df = pd.read_csv(uploaded_file)
                        st.success(f"Loaded {len(df)} logs")
                        st.dataframe(df.head(), use_container_width=True)
                        st.session_state.logs_data = parse_csv_to_logs(df)
                        st.session_state.uploaded_logs = df
                    except Exception as e:
                        st.error(f"Error reading file: {str(e)}")
                        logger.error(f"CSV upload error: {str(e)}")
                        
            elif upload_mode == "Use Sample Data":
                try:
                    logger.info(f"\nLOADING SAMPLE DATA")
                    logger.info(f"  File path: {DEMO_LOG_FILE}")
                    
                    # Check if file exists
                    import os
                    abs_path = os.path.abspath(DEMO_LOG_FILE)
                    logger.info(f"  Absolute path: {abs_path}")
                    logger.info(f"  File exists: {os.path.exists(abs_path)}")
                    
                    df = pd.read_csv(DEMO_LOG_FILE)
                    logger.info(f"  Loaded CSV: {len(df)} rows x {len(df.columns)} columns")
                    logger.info(f"  Columns: {list(df.columns)}")
                    
                    st.info(f"✅ Using {len(df)} sample logs from dataset")
                    st.dataframe(df.head(), use_container_width=True)
                    
                    logger.info(f"  Parsing CSV to logs...")
                    parsed_result = parse_csv_to_logs(df)
                    
                    logger.info(f"  Parse result keys: {list(parsed_result.keys())}")
                    logger.info(f"  Logs parsed: {len(parsed_result.get('logs', []))}")
                    
                    if parsed_result.get('errors'):
                        logger.warning(f"  Parse errors: {parsed_result['errors']}")
                        st.warning(f"⚠️ {len(parsed_result['errors'])} rows failed to parse")
                    
                    st.session_state.logs_data = parsed_result
                    st.session_state.uploaded_logs = df
                    
                    logger.info(f"  Stored in session_state: {len(st.session_state.logs_data.get('logs', []))} logs")
                    
                except Exception as e:
                    st.error(f"❌ Error loading sample data: {str(e)}")
                    logger.exception(f"Sample data loading error: {str(e)}")
                    import traceback
                    logger.error(f"Traceback: {traceback.format_exc()}")
                    
            else:  # Manual Entry
                st.write("**Add logs manually:**")
                num_logs = st.number_input("Number of logs", 1, 10, 1)
                
                logs_list = []
                for i in range(int(num_logs)):
                    with st.expander(f"Log {i+1}"):
                        col_a, col_b = st.columns(2)
                        with col_a:
                            ts = st.text_input(f"Timestamp {i}", "2024-01-01T12:00:00", key=f"ts_{i}")
                            src_ip = st.text_input(f"Source IP {i}", "192.168.1.1", key=f"src_{i}")
                            dst_ip = st.text_input(f"Dest IP {i}", "8.8.8.8", key=f"dst_{i}")
                            port = st.number_input(f"Port {i}", 0, 65535, 443, key=f"port_{i}")
                        with col_b:
                            protocol = st.selectbox(f"Protocol {i}", ["TCP", "UDP"], key=f"proto_{i}")
                            bytes_sent = st.number_input(f"Bytes Sent {i}", 0, key=f"bs_{i}", value=1024)
                            bytes_recv = st.number_input(f"Bytes Received {i}", 0, key=f"br_{i}", value=2048)
                            duration = st.number_input(f"Duration {i}", 0.0, key=f"dur_{i}", value=5.0)
                        
                        logs_list.append({
                            "timestamp": ts,
                            "source_ip": src_ip,
                            "destination_ip": dst_ip,
                            "port": port,
                            "protocol": protocol,
                            "bytes_sent": bytes_sent,
                            "bytes_received": bytes_recv,
                            "duration": duration
                        })
                
                if logs_list:
                    st.session_state.logs_data = {"logs": logs_list}
                    st.session_state.uploaded_logs = pd.DataFrame(logs_list)
        
        with col2:
            st.subheader("🔍 Analysis Results")
            
            # Show status
            if st.session_state.logs_data:
                log_count = len(st.session_state.logs_data.get("logs", []))
                st.success(f"✅ Data loaded: {log_count} logs ready")
                logger.debug(f"Session state has {log_count} logs")
            else:
                st.warning("⏳ Waiting for log data...")
                logger.debug("Session state logs_data is None")
            
            st.divider()
            
            if st.button("🚀 Analyze Logs", type="primary", use_container_width=True):
                logger.info("Analyze button clicked")
                if st.session_state.logs_data:
                    logger.info(f"Analyzing {len(st.session_state.logs_data.get('logs', []))} logs")
                    if not backend_available:
                        st.error("Backend is not available! Start backend first.")
                        logger.error("Backend not available")
                    else:
                        with st.spinner("Analyzing logs..."):
                            results = analyze_logs(st.session_state.logs_data)
                        
                        if results:
                            st.session_state.analysis_results = results
                            st.success("Analysis complete!")
                            
                            # Display key metrics
                            col_m1, col_m2, col_m3 = st.columns(3)
                            
                            with col_m1:
                                st.metric(
                                    "Total Logs",
                                    results.get("total_logs", 0),
                                    delta=None
                                )
                            
                            with col_m2:
                                anomalies = results.get("anomalies_detected", 0)
                                st.metric(
                                    "🚨 Anomalies",
                                    anomalies,
                                    delta_color="inverse"
                                )
                            
                            with col_m3:
                                pct = results.get("anomaly_percentage", 0)
                                st.metric(
                                    "Anomaly Rate",
                                    f"{pct:.1f}%",
                                    delta=None
                                )
                        else:
                            st.error("Failed to analyze logs")
                else:
                    st.warning("Please provide log data first")
        
        # Display results if available
        if st.session_state.analysis_results:
            st.divider()
            st.subheader("📋 Detailed Results")
            
            results = st.session_state.analysis_results
            
            # Create results dataframe
            if results.get("results"):
                results_df = pd.DataFrame(results["results"])
            else:
                st.error("No results data in response")
                results_df = None
            
            # Display with formatting
            def style_severity(val):
                if val == "CRITICAL":
                    return 'color: #ff0000; font-weight: bold;'
                elif val == "HIGH":
                    return 'color: #ff6600; font-weight: bold;'
                elif val == "MEDIUM":
                    return 'color: #ffaa00; font-weight: bold;'
                else:
                    return 'color: #00aa00;'
            
            if results_df is not None:
                styled_df = results_df.style.map(style_severity, subset=['severity'])
                st.dataframe(styled_df, use_container_width=True)
                
                # Export results
                col_exp1, col_exp2 = st.columns(2)
                with col_exp1:
                    csv = results_df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download Results CSV",
                        data=csv,
                        file_name=f"threat_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
                
                with col_exp2:
                    json_data = json.dumps(results, indent=2)
                st.download_button(
                    label="📥 Download Results JSON",
                    data=json_data,
                    file_name=f"threat_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )

    # TAB 2: Visualizations
    with tab2:
        if st.session_state.analysis_results:
            st.header("📈 Threat Visualizations")
            
            results = st.session_state.analysis_results
            if results.get("results"):
                results_df = pd.DataFrame(results["results"])
            else:
                st.error("No results data in response")
                st.stop()
            
            # Cast to DataFrame for type checker (st.stop() terminates if results_df is None)
            results_df = cast(pd.DataFrame, results_df)
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Severity Distribution
                severity_counts = results_df["severity"].value_counts()
                fig_severity = go.Figure(data=[
                    go.Bar(
                        x=severity_counts.index,
                        y=severity_counts.values,
                        marker=dict(
                            color=["#ff0000", "#ff6600", "#ffaa00", "#00aa00"],
                        ),
                        text=severity_counts.values,
                        textposition='auto',
                    )
                ])
                fig_severity.update_layout(
                    title="Threat Severity Distribution",
                    xaxis_title="Severity Level",
                    yaxis_title="Count",
                    height=400,
                    template="plotly_dark",
                    showlegend=False
                )
                st.plotly_chart(fig_severity, use_container_width=True)
            
            with col2:
                # Anomaly Score Distribution
                fig_scores = go.Figure(data=[
                    go.Histogram(
                        x=results_df["anomaly_score"],
                        nbinsx=20,
                        marker=dict(color="rgba(255, 0, 81, 0.7)"),
                    )
                ])
                fig_scores.update_layout(
                    title="Anomaly Score Distribution",
                    xaxis_title="Anomaly Score",
                    yaxis_title="Frequency",
                    height=400,
                    template="plotly_dark",
                    showlegend=False
                )
                st.plotly_chart(fig_scores, use_container_width=True)
            
            col3, col4 = st.columns(2)
            
            with col3:
                # Anomaly Status Pie Chart
                anomaly_counts = results_df["is_anomaly"].value_counts()
                labels = ["Normal", "Anomaly"]
                values = [anomaly_counts.get(False, 0), anomaly_counts.get(True, 0)]
                
                fig_pie = go.Figure(data=[
                    go.Pie(labels=labels, values=values, marker=dict(colors=["#00aa00", "#ff0000"]))
                ])
                fig_pie.update_layout(
                    title="Normal vs Anomalous Logs",
                    height=400,
                    template="plotly_dark"
                )
                st.plotly_chart(fig_pie, use_container_width=True)
            
            with col4:
                # Timeline of Anomalies
                results_df["timestamp"] = pd.to_datetime(results_df["timestamp"])
                results_df = results_df.sort_values("timestamp")
                
                fig_timeline = go.Figure()
                fig_timeline.add_trace(go.Scatter(
                    x=results_df["timestamp"],
                    y=results_df["anomaly_score"],
                    mode='markers',
                    marker=dict(
                        size=8,
                        color=results_df["anomaly_score"],
                        colorscale="Reds",
                        showscale=True,
                        colorbar=dict(title="Anomaly Score")
                    ),
                    text=[f"Score: {s:.2f}<br>Severity: {sev}" 
                          for s, sev in zip(results_df["anomaly_score"], results_df["severity"])],
                    hoverinfo="text"
                ))
                fig_timeline.update_layout(
                    title="Anomaly Scores Over Time",
                    xaxis_title="Timestamp",
                    yaxis_title="Anomaly Score",
                    height=400,
                    template="plotly_dark",
                    hovermode="closest"
                )
                st.plotly_chart(fig_timeline, use_container_width=True)
        else:
            st.info("📊 Run analysis first to see visualizations")

    # TAB 3: Details
    with tab3:
        st.header("🔍 Detailed Analysis")
        
        if st.session_state.analysis_results:
            results = st.session_state.analysis_results
            
            if not results.get("results"):
                st.error("No results data in response")
                st.stop()
            
            results_df = pd.DataFrame(results["results"])
            
            # Filter options
            col1, col2, col3 = st.columns(3)
            
            with col1:
                severity_filter = st.multiselect(
                    "Filter by Severity",
                    ["CRITICAL", "HIGH", "MEDIUM", "LOW"],
                    default=["CRITICAL", "HIGH", "MEDIUM", "LOW"]
                )
            
            with col2:
                anomaly_filter = st.radio(
                    "Show",
                    ["All", "Anomalies Only", "Normal Only"]
                )
            
            with col3:
                sort_by = st.selectbox(
                    "Sort By",
                    ["Anomaly Score (Desc)", "Timestamp", "Port"]
                )
            
            # Apply filters
            filtered_df = results_df.copy()
            
            if severity_filter:
                filtered_df = filtered_df[filtered_df["severity"].isin(severity_filter)]
            
            if anomaly_filter == "Anomalies Only":
                filtered_df = filtered_df[filtered_df["is_anomaly"] == True]
            elif anomaly_filter == "Normal Only":
                filtered_df = filtered_df[filtered_df["is_anomaly"] == False]
            
            # Sort
            if sort_by == "Anomaly Score (Desc)":
                filtered_df = filtered_df.sort_values("anomaly_score", ascending=False)
            elif sort_by == "Timestamp":
                filtered_df = filtered_df.sort_values("timestamp")
            elif sort_by == "Port":
                filtered_df = filtered_df.sort_values("port")
            
            st.info(f"Showing {len(filtered_df)} of {len(results_df)} logs")
            
            # Display detailed table
            st.dataframe(
                filtered_df,
                use_container_width=True,
                hide_index=True
            )
            
            # Top anomalies
            st.subheader("🔴 Top Anomalies")
            top_anomalies = results_df[results_df["is_anomaly"]].nlargest(5, "anomaly_score")
            
            if len(top_anomalies) > 0:
                for idx, row in top_anomalies.iterrows():
                    with st.container():
                        col_a, col_b, col_c = st.columns([1, 4, 1])
                        
                        with col_a:
                            severity = row["severity"]
                            st.write(f"{get_severity_emoji(severity)} **{severity}**")
                        
                        with col_b:
                            st.write(f"""
                            **{row['source_ip']}** → **{row['destination_ip']}**:{row['port']}  
                            Score: {row['anomaly_score']:.4f} | {row['protocol']} | Bytes: {row['bytes_sent']}/{row['bytes_received']}
                            """)
                        
                        with col_c:
                            st.metric("Anomaly", f"{row['anomaly_score']:.2f}")
                        
                        st.divider()
            else:
                st.success("No anomalies detected!")
        else:
            st.info("🔍 Run analysis first to see details")

    # TAB 4: About
    with tab4:
        st.header("ℹ️ About This Dashboard")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🎯 Purpose")
            st.markdown("""
            This dashboard provides real-time threat detection using machine learning.
            
            **Key Features:**
            - 📊 Upload log data (CSV format)
            - 🤖 AI-powered anomaly detection
            - 📈 Real-time visualizations
            - 💾 Export results (CSV, JSON)
            - 🔍 Detailed threat analysis
            """)
            
            st.subheader("🔧 Technology Stack")
            st.markdown("""
            - **Frontend:** Streamlit
            - **Backend:** FastAPI
            - **ML Model:** Scikit-learn (Isolation Forest)
            - **Data Processing:** Pandas, NumPy
            - **Visualization:** Plotly
            """)
        
        with col2:
            st.subheader("📋 Expected CSV Format")
            st.markdown("""
            Your CSV file should contain these columns:
            - `timestamp` - ISO 8601 format (YYYY-MM-DDTHH:MM:SS)
            - `source_ip` - Source IP address
            - `destination_ip` - Destination IP address
            - `port` - Port number (0-65535)
            - `protocol` - TCP or UDP
            - `bytes_sent` - Bytes sent (integer)
            - `bytes_received` - Bytes received (integer)
            - `duration` - Connection duration in seconds (float)
            """)
            
            st.subheader("🚨 Severity Levels")
            severity_info = {
                "CRITICAL": "0.9-1.0 | Highly anomalous",
                "HIGH": "0.75-0.9 | Unusual activity",
                "MEDIUM": "0.5-0.75 | Suspicious",
                "LOW": "0.0-0.5 | Normal traffic"
            }
            
            for severity, description in severity_info.items():
                color = get_severity_color(severity)
                emoji = get_severity_emoji(severity)
                st.markdown(f"{emoji} **{severity}** - {description}")
        
        st.divider()
        
        st.subheader("📚 Documentation")
        st.markdown("""
        For more information, visit:
        - [Main README](https://github.com/project/README.md)
        - [Architecture](https://github.com/project/ARCHITECTURE.md)
        - [Phase 2 Backend](https://github.com/project/PHASE2_COMPLETE.md)
        """)
        
        st.subheader("⚙️ System Status")
        col_status1, col_status2, col_status3 = st.columns(3)
        
        with col_status1:
            backend_ok = check_backend_health()
            status_text = "✅ Online" if backend_ok else "❌ Offline"
            st.info(f"**Backend:** {status_text}")
        
        with col_status2:
            st.info(f"**Dashboard:** ✅ Online")
        
        with col_status3:
            st.info(f"**Last Update:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    main()
