"""
Reusable UI Components
"""
import streamlit as st
import plotly.graph_objects as go
from datetime import datetime


def render_metric_card(title, value, delta=None, icon="📊"):
    """Render a metric card"""
    with st.container():
        col1, col2 = st.columns([1, 3])
        with col1:
            st.write(icon)
        with col2:
            st.metric(title, value, delta=delta)


def render_severity_badge(severity, score):
    """Render severity badge with color"""
    colors = {
        "CRITICAL": "#ff0000",
        "HIGH": "#ff6600",
        "MEDIUM": "#ffaa00",
        "LOW": "#00aa00"
    }
    emojis = {
        "CRITICAL": "🔴",
        "HIGH": "🟠",
        "MEDIUM": "🟡",
        "LOW": "🟢"
    }
    
    color = colors.get(severity, "#cccccc")
    emoji = emojis.get(severity, "⚪")
    
    return f"{emoji} **{severity}** ({score:.2f})"


def render_alert(alert_type, title, message):
    """Render an alert"""
    if alert_type == "critical":
        st.error(f"🔴 {title}: {message}")
    elif alert_type == "warning":
        st.warning(f"⚠️ {title}: {message}")
    elif alert_type == "info":
        st.info(f"ℹ️ {title}: {message}")
    else:
        st.success(f"✅ {title}: {message}")


def create_anomaly_gauge(score):
    """Create a gauge chart for anomaly score"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score * 100,
        title={'text': "Anomaly Score (%)"},
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 50], 'color': "#00aa00"},
                {'range': [50, 75], 'color': "#ffaa00"},
                {'range': [75, 90], 'color': "#ff6600"},
                {'range': [90, 100], 'color': "#ff0000"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    fig.update_layout(height=300, template="plotly_dark")
    return fig


def format_log_entry(log_data):
    """Format log entry for display"""
    return f"""
    **Source:** {log_data.get('source_ip', 'N/A')}  
    **Destination:** {log_data.get('destination_ip', 'N/A')}:{log_data.get('port', 'N/A')}  
    **Protocol:** {log_data.get('protocol', 'N/A')}  
    **Bytes Sent/Received:** {log_data.get('bytes_sent', 0)} / {log_data.get('bytes_received', 0)}  
    **Duration:** {log_data.get('duration', 0):.2f}s
    """


def export_results_summary(results_df):
    """Generate a summary for export"""
    summary = {
        "generated_at": datetime.now().isoformat(),
        "total_logs": len(results_df),
        "anomalies_detected": len(results_df[results_df["is_anomaly"]]),
        "average_anomaly_score": float(results_df["anomaly_score"].mean()),
        "critical_count": len(results_df[results_df["severity"] == "CRITICAL"]),
        "high_count": len(results_df[results_df["severity"] == "HIGH"]),
        "medium_count": len(results_df[results_df["severity"] == "MEDIUM"]),
        "low_count": len(results_df[results_df["severity"] == "LOW"]),
    }
    return summary
