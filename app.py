# app.py
import streamlit as st
from backend import process_runtime_traffic, evaluate_traffic_anomaly

st.title("🛡️ Network Intrusion Detection System")
st.write("Mock UI for testing backend operations.")

# 1. Collect arbitrary network inputs from input components
proto = st.selectbox("Protocol (proto):", ['tcp', 'udp', 'unas', 'arp', 'ospf', 'other'])
service = st.selectbox("Service:", ['-', 'dns', 'http', 'ftp', 'ftp-data', 'smtp'])
state = st.selectbox("State:", ['FIN', 'CON', 'INT', 'REQ', 'RST'])

dur = st.number_input("Duration (dur):", min_value=0.0, value=0.11)
sbytes = st.number_input("Source Bytes (sbytes):", min_value=0, value=500)
dbytes = st.number_input("Destination Bytes (dbytes):", min_value=0, value=200)
spkts = st.number_input("Source Packets (spkts):", min_value=0, value=10)
dpkts = st.number_input("Destination Packets (dpkts):", min_value=0, value=8)

if st.button("Run Traffic Threat Analysis"):
    # Pack up the UI inputs into a simple dictionary structure
    user_payload = {
        "proto": proto, "service": service, "state": state,
        "dur": dur, "sbytes": sbytes, "dbytes": dbytes,
        "spkts": spkts, "dpkts": dpkts
    }
    
    # Pass input payload dictionary safely through the backend engine functions
    clean_row = process_runtime_traffic(user_payload)
    is_anomaly, confidence = evaluate_traffic_anomaly(clean_row)
    
    # Display Output Results
    st.subheader("Analysis Breakdown")
    if is_anomaly == 1:
        st.error(f"🚨 threat alert: Network Anomaly Detected! (Confidence: {confidence[0]*100:.2f}%)")
    else:
        st.success(f"✅ Safe Traffic: Pattern aligns with normal network behavior.")
