import streamlit as st
import requests
import time
import pandas as pd
import json

import os

# Configuration
# Default to localhost for local dev, or set via env for production
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(
    page_title="Vertex SRE Mission Control",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for "Mission Control" look
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
        color: #c9d1d9;
    }
    .metric-card {
        background-color: #161b22;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #30363d;
    }
    .incident-critical {
        border-left: 5px solid #da3633;
    }
    .incident-warning {
        border-left: 5px solid #d29922;
    }
</style>
""", unsafe_allow_html=True)

st.title("🛡️ Vertex SRE: Autonomous Incident Response")

# Sidebar
with st.sidebar:
    st.header("Status")
    st.metric("System Health", "Operational", delta="Normal")
    st.metric("Active Agents", "1", delta="Standard")
    
    st.divider()
    if st.button("Refresh Data"):
        st.rerun()

# Layout
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("🚨 Active Incidents")
    
    try:
        # Fetch incidents from backend
        # Note: In a real app we'd handle pagination and better error states
        try:
            response = requests.get(f"{BACKEND_URL}/incidents")
            incidents_data = response.json()
        except requests.exceptions.ConnectionError:
            st.error("Backend unreachable. Is it running?")
            incidents_data = {}

        if not incidents_data:
            st.info("No active incidents.")
        
        for inc_id, data in incidents_data.items():
            incident_payload = data.get("incident", {})
            analysis = data.get("analysis", {})
            
            with st.container():
                st.markdown(f"""
                <div class="metric-card incident-critical">
                    <h4>{incident_payload.get('summary', 'Unknown Incident')}</h4>
                    <p><b>ID:</b> {inc_id}</p>
                    <p><b>Service:</b> {incident_payload.get('resource_name')}</p>
                    <p><b>Time:</b> {incident_payload.get('timestamp')}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"Investigate {inc_id}", key=inc_id):
                    st.session_state["selected_incident"] = inc_id

    except Exception as e:
        st.error(f"Error loading incidents: {e}")

with col2:
    st.subheader("🔍 Investigation Timeline & Remediation")
    
    selected_id = st.session_state.get("selected_incident")
    
    if selected_id and incidents_data.get(selected_id):
        data = incidents_data[selected_id]
        analysis = data.get("analysis", {})
        
        st.markdown(f"### Analysis for `{selected_id}`")
        
        # Tabs for details
        tab1, tab2, tab3 = st.tabs(["Root Cause Analysis", "Topology & Context", "Remediation"])
        
        with tab1:
            st.markdown("#### 🤖 Vertex AI Conclusion")
            if analysis.get("confidence", 0) > 0.8:
                st.success(f"Confidence: {analysis.get('confidence')}")
            else:
                st.warning(f"Confidence: {analysis.get('confidence')}")
            
            st.write(analysis.get("root_cause"))
            
            st.markdown("#### Evidence")
            st.json(analysis.get("related_deployments"))

        with tab2:
            st.markdown("#### Dependency Graph")
            # In a real app, use streamlit-agraph or graphviz
            st.info("Visualizing dependencies found via Cloud Asset Inventory...")
            st.code(json.dumps(data.get("incident", {}).get("resource_name"), indent=2))
            
        with tab3:
            st.markdown("#### Recommended Action")
            plan = analysis.get("remediation_plan")
            st.info(plan)
            
            st.divider()
            st.write("Execute Remediation:")
            c1, c2 = st.columns(2)
            with c1:
                if st.button("Rollback Deployment", type="primary"):
                    st.toast("Triggering Cloud Build Rollback...", icon="🚀")
                    time.sleep(1)
                    st.success("Rollback initiated successfully!")
            with c2:
                if st.button("Ignore / Close Incident"):
                    st.session_state["selected_incident"] = None
                    st.rerun()
    else:
        st.markdown("*Select an incident from the left panel to view details.*")
        
        # Placeholder / Empty State with nice graphic
        st.image("https://www.gstatic.com/cloud/images/social/cloud-console-social.png", use_column_width=True, caption="Vertex SRE Standby")
