import streamlit as st
import json
import os
from signal_processing.main import run_pipeline

st.set_page_config(
    page_title="EVE-Node-AI: Forest Bioacoustic Intelligence",
    page_icon="🌲",
    layout="wide"
)

st.title("🌲 EVE-Node-AI: Closed-Loop Energy-Aware Bioacoustic Sensing")
st.markdown("**Ingénieux IEEE Hackathon | Track: Forests & Wildlife Intelligent Sensing**")

# Sidebar configurations for interactive demo
st.sidebar.header("🎛️ Pipeline Configuration")
lowcut = st.sidebar.slider("Bandpass Low Cutoff (Hz)", 100.0, 400.0, 250.0)
highcut = st.sidebar.slider("Bandpass High Cutoff (Hz)", 2000.0, 4000.0, 3500.0)
gate_mult = st.sidebar.slider("Spectral Noise Gate Multiplier", 1.0, 3.0, 1.6)
mode = st.sidebar.selectbox("Initial Agent Mode", ["STANDARD", "ADAPTIVE_DEEP_CLEAN"])

if st.button("🚀 Run Closed-Loop Audio Analysis & Agent Trigger", type="primary"):
    with st.spinner("Running Signal Processing pipeline & Agent reasoning loop..."):
        # Executes your signal processing code and outputs JSON/plots
        run_pipeline(lowcut=lowcut, highcut=highcut, gate_mult=gate_mult, mode=mode)
        
    st.success("Pipeline executed successfully and Agent evaluated the audio frame!")

# Load and display latest payload if available
payload_path = "signal_processing/outputs/agent_payload.json"
plot_path = "signal_processing/outputs/pipeline_results.png"

if os.path.exists(payload_path):
    with open(payload_path, "r") as f:
        payload = json.load(f)
        
    st.markdown("---")
    st.subheader("📊 Real-Time Edge Processing Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Baseline SNR", f"{payload['metrics']['snr_before_db']} dB")
    col2.metric("Cleaned SNR", f"{payload['metrics']['snr_after_db']} dB")
    col3.metric("SNR Gain", f"+{payload['metrics']['snr_gain_db']} dB")
    col4.metric("Battery/Frames Saved", f"{payload['metrics']['data_reduction_pct']}%")

    st.markdown("---")
    st.subheader("🤖 Autonomous Agent Decision & Reasoning")
    agent_eval = payload["agent_evaluation"]
    
    decision = agent_eval["agent_decision"]
    if "ALERT" in decision:
        st.error(f"🚨 **Decision: {decision}**")
    else:
        st.info(f"💤 **Decision: {decision}**")
        
    st.write(f"**Agent Reasoning:** {agent_eval['reasoning']}")

    st.markdown("---")
    st.subheader("📈 Signal Processing & Energy Gating Evidence")
    if os.path.exists(plot_path):
        st.image(plot_path, caption="Multi-stage pipeline outputs: Raw noisy stream vs. Cleaned harmonic signal vs. RMS energy gating.", use_container_width=True)
        
    with st.expander("🔍 View Raw JSON Payload"):
        st.json(payload)
else:
    st.info("Click the button above to execute the pipeline and generate real-time metrics and plots.")
