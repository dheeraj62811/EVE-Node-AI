"""
EVE-Node: Event-Vigilant Edge Sensing Platform
File: app.py
Module: Interactive Streamlit Dashboard for Live Demonstrations
"""

import os
import json
import streamlit as st
import numpy as np

# Page configuration"""
EVE-Node: Event-Vigilant Edge Sensing Platform
File: app.py
Module: Interactive Streamlit Dashboard for Live Demonstrations
"""

import os
import json
import streamlit as st
import soundfile as sf
import numpy as np

st.set_page_config(
    page_title="EVE-Node | Intelligent Sensing Dashboard",
    page_icon="🌲",
    layout="wide"
)

st.title("🌲 EVE-Node: Event-Vigilant Edge Sensing Platform")
st.caption("IEEE Ingénieux Hackathon | Track 2: Forests & Wildlife Intelligent Sensing | Team Ciphera")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PAYLOAD_PATH = os.path.join(BASE_DIR, "signal_processing", "outputs", "agent_payload.json")
RESULTS_IMG_PATH = os.path.join(BASE_DIR, "signal_processing", "outputs", "pipeline_results.png")
FALLBACK_IMG_PATH = os.path.join(BASE_DIR, "outputs", "pipeline_results.png")
DISPATCH_PATH = os.path.join(BASE_DIR, "outputs", "ranger_incident_dispatch.json")
CLEANED_WAV_PATH = os.path.join(BASE_DIR, "signal_processing", "processed", "cleaned_forest_signal.wav")

# Sidebar Controls
st.sidebar.header("🕹️ Edge Sensor Simulation Controls")
battery_slider = st.sidebar.slider("Edge Node Battery Level (%)", min_value=5.0, max_value=100.0, value=17.5, step=0.5)
weather_select = st.sidebar.selectbox("Ambient Weather Condition", ["HEAVY_MONSOON", "HIGH_WIND", "CALM_RAIN", "CLEAR_NIGHT"])

st.sidebar.markdown("---")
st.sidebar.header("🎙️ Audio Ingestion Source")
uploaded_file = st.sidebar.file_uploader("Upload Any Audio Recording (.wav, .mp3)", type=["wav", "mp3"])

if uploaded_file is not None:
    st.sidebar.audio(uploaded_file, format='audio/wav')
    st.sidebar.success("Custom recording loaded!")

st.sidebar.markdown("---")
run_btn = st.sidebar.button("⚡ Trigger EVE-Node Wake Cycle", use_container_width=True)

# Main Dashboard
tab1, tab2, tab3 = st.tabs(["📊 Edge DSP & Spectral Evidence", "🤖 Agentic Reasoning Trace", "🚨 Ranger Interdiction Console"])

with tab1:
    col1, col2, col3, col4 = st.columns(4)
    
    payload_data = {}
    if os.path.exists(PAYLOAD_PATH):
        with open(PAYLOAD_PATH, "r") as f:
            payload_data = json.load(f)

    metrics = payload_data.get("metrics", {})
    features = payload_data.get("extracted_features", {})

    col1.metric("Input Raw SNR", f"{metrics.get('snr_before_db', -4.12):.2f} dB")
    col2.metric("Cleaned Output SNR", f"{metrics.get('snr_after_db', 6.85):.2f} dB", delta=f"+{metrics.get('snr_gain_db', 10.97):.2f} dB")
    col3.metric("Ambient Frames Dropped", f"{metrics.get('data_reduction_pct', 60.0):.1f}%", help="Energy saved by RMS frame gating before waking AI")
    
    centroid_val = features.get('spectral_centroid_hz', 815.42)
    col4.metric("Spectral Centroid", f"{centroid_val:.1f} Hz", delta="Motor Range" if 350 <= centroid_val <= 1600 else "Biophony / Wind")

    st.markdown("### 🔬 Multi-Stage DSP Evidence (Denoising & Harmonic Extraction)")
    target_img = RESULTS_IMG_PATH if os.path.exists(RESULTS_IMG_PATH) else FALLBACK_IMG_PATH
    if os.path.exists(target_img):
        st.image(target_img, caption="Stage 1: Raw Ingested Signal | Stage 2: IIR Cicada Notch & Broad Filter | Stage 3: Adaptive Agent Pass + STFT Rain Gating", use_container_width=True)

    if os.path.exists(CLEANED_WAV_PATH):
        st.markdown("#### 🎧 Cleaned Audio Output")
        st.audio(CLEANED_WAV_PATH, format="audio/wav")

with tab2:
    st.markdown("### 🧠 Observe $\\rightarrow$ Reason $\\rightarrow$ Adapt $\\rightarrow$ Act Trace")
    
    if run_btn:
        from signal_processing.main import run_pipeline
        from agent_controller import EvenodeAgenticController

        with st.spinner("Processing audio through DSP pipeline and running Agentic loop..."):
            # Step 1: Run DSP with uploaded audio if present
            if uploaded_file is not None:
                audio_bytes, sr = sf.read(uploaded_file)
                run_pipeline(audio_source=(audio_bytes, sr))
            else:
                run_pipeline()

            # Step 2: Trigger Agentic Controller
            controller = EvenodeAgenticController(node_id="EVE_Node_01", gps_coords="17.5449° N, 78.5718° E")
            result = controller.run_cycle(simulated_battery=battery_slider, weather=weather_select)
        
        st.success("Reasoning Cycle Complete!")
        st.code(result["logs"], language="text")
        st.rerun()
    else:
        st.info("Upload an audio file in the sidebar (or leave blank for the synthetic stream) and click **'Trigger EVE-Node Wake Cycle'**.")

with tab3:
    st.markdown("### 📡 Tactical Dispatch Packet for Park Rangers")
    if os.path.exists(DISPATCH_PATH):
        with open(DISPATCH_PATH, "r") as f:
            dispatch_info = json.load(f)
        
        c1, c2 = st.columns([1, 2])
        with c1:
            st.warning(f"**Classification:** {dispatch_info.get('incident_classification')}")
            st.metric("Detection Confidence", f"{dispatch_info.get('confidence_score', 0.95)*100:.1f}%")
            st.write(f"**Node ID:** {dispatch_info.get('sensor_node')}")
            st.write(f"**Location:** `{dispatch_info.get('geo_coordinates')}`")
        with c2:
            st.markdown(f"**Evidence Summary:**\n> {dispatch_info.get('evidence_summary')}")
            st.markdown(f"**Recommended Action:**\n> `{dispatch_info.get('recommended_tactical_action')}`")
            st.json(dispatch_info)
    else:
        st.info("No active dispatch packets. The node is in dormant monitoring mode.")
st.set_page_config(
    page_title="EVE-Node | Intelligent Sensing Dashboard",
    page_icon="🌲",
    layout="wide"
)

st.title("🌲 EVE-Node: Event-Vigilant Edge Sensing Platform")
st.caption("IEEE Ingénieux Hackathon | Track 2: Forests & Wildlife Intelligent Sensing | Team Ciphera")

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PAYLOAD_PATH = os.path.join(BASE_DIR, "signal_processing", "outputs", "agent_payload.json")
RESULTS_IMG_PATH = os.path.join(BASE_DIR, "signal_processing", "outputs", "pipeline_results.png")
FALLBACK_IMG_PATH = os.path.join(BASE_DIR, "outputs", "pipeline_results.png")
DISPATCH_PATH = os.path.join(BASE_DIR, "outputs", "ranger_incident_dispatch.json")

# Sidebar Controls
st.sidebar.header("🕹️ Edge Sensor Simulation Controls")
battery_slider = st.sidebar.slider("Edge Node Battery Level (%)", min_value=5.0, max_value=100.0, value=17.5, step=0.5)
weather_select = st.sidebar.selectbox("Ambient Weather Condition", ["HEAVY_MONSOON", "HIGH_WIND", "CALM_RAIN", "CLEAR_NIGHT"])
scenario_select = st.sidebar.selectbox("Acoustic Audio Source", ["Illegal Chainsaw (Logging)", "Gunshot Transient (Poaching)", "Ambient Rain & Insects"])

st.sidebar.markdown("---")
run_btn = st.sidebar.button("⚡ Trigger EVE-Node Wake Cycle", use_container_width=True)

# Main Display Tabs
tab1, tab2, tab3 = st.tabs(["📊 Edge DSP & Spectral Evidence", "🤖 Agentic Reasoning Trace", "🚨 Ranger Interdiction Console"])

with tab1:
    col1, col2, col3, col4 = st.columns(4)
    
    # Read current payload
    payload_data = {}
    if os.path.exists(PAYLOAD_PATH):
        with open(PAYLOAD_PATH, "r") as f:
            payload_data = json.load(f)
    elif os.path.exists(os.path.join(BASE_DIR, "outputs", "agent_payload.json")):
        with open(os.path.join(BASE_DIR, "outputs", "agent_payload.json"), "r") as f:
            payload_data = json.load(f)

    metrics = payload_data.get("metrics", {})
    features = payload_data.get("extracted_features", {})

    col1.metric("Input Raw SNR", f"{metrics.get('snr_before_db', -4.12):.2f} dB")
    col2.metric("Output Clean SNR", f"{metrics.get('snr_after_db', 6.85):.2f} dB", delta=f"+{metrics.get('snr_gain_db', 10.97):.2f} dB")
    col3.metric("Ambient Frames Dropped", f"{metrics.get('data_reduction_pct', 60.0):.1f}%", help="Energy saved by RMS frame gating before waking the AI")
    col4.metric("Spectral Centroid", f"{features.get('spectral_centroid_hz', 815.42):.1f} Hz", delta="Motor Range" if 350 <= features.get('spectral_centroid_hz', 815.42) <= 1600 else "Biophony")

    st.markdown("### 🔬 Multi-Stage DSP Evidence (Denoising & Harmonic Extraction)")
    target_img = RESULTS_IMG_PATH if os.path.exists(RESULTS_IMG_PATH) else FALLBACK_IMG_PATH
    if os.path.exists(target_img):
        st.image(target_img, caption="Stage 1: Raw Ingested Signal | Stage 2: IIR Cicada Notch & Broad Filter | Stage 3: Adaptive Agent Pass + STFT Rain Gating", use_container_width=True)
    else:
        st.info("Run main.py or benchmark.py to generate pipeline_results.png")

with tab2:
    st.markdown("### 🧠 Observe $\\rightarrow$ Reason $\\rightarrow$ Adapt $\\rightarrow$ Act Trace")
    
    if run_btn:
        from agent_controller import EvenodeAgenticController
        controller = EvenodeAgenticController(node_id="EVE_Node_01", gps_coords="17.5449° N, 78.5718° E")
        
        with st.spinner("Executing Closed-Loop Agentic Cycle..."):
            result = controller.run_cycle(simulated_battery=battery_slider, weather=weather_select)
        
        st.success("Reasoning Cycle Complete!")
        st.code(result["logs"], language="text")
    else:
        st.write("Click **'Trigger EVE-Node Wake Cycle'** in the sidebar to simulate live agent reasoning.")

with tab3:
    st.markdown("### 📡 Tactical Dispatch Packet for Park Rangers")
    if os.path.exists(DISPATCH_PATH):
        with open(DISPATCH_PATH, "r") as f:
            dispatch_info = json.load(f)
        
        c1, c2 = st.columns([1, 2])
        with c1:
            st.warning(f"**Classification:** {dispatch_info.get('incident_classification')}")
            st.metric("Detection Confidence", f"{dispatch_info.get('confidence_score', 0.95)*100:.1f}%")
            st.write(f"**Node ID:** {dispatch_info.get('sensor_node')}")
            st.write(f"**Location:** `{dispatch_info.get('geo_coordinates')}`")
        with c2:
            st.markdown(f"**Evidence Summary:**\n> {dispatch_info.get('evidence_summary')}")
            st.markdown(f"**Recommended Action:**\n> `{dispatch_info.get('recommended_tactical_action')}`")
            st.json(dispatch_info)
    else:
        st.info("No active dispatch packets. The system remains in low-power dormant listening mode.")
