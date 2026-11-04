import os
import json
import streamlit as st
import soundfile as sf
import numpy as np
import streamlit.components.v1 as components

st.set_page_config(
    page_title="EVE-Node | Intelligent Sensing Hub",
    page_icon="🌲",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Inter:wght@300;400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .hero-title { font-size: 2.1rem; font-weight: 700; color: #f0f6fc; margin-bottom: 2px; }
    .hero-sub { color: #8b949e; font-size: 0.95rem; margin-bottom: 16px; }
    .metric-card {
        background: linear-gradient(135deg, rgba(22, 27, 34, 0.95), rgba(13, 17, 23, 0.95));
        border: 1px solid rgba(48, 54, 61, 0.9);
        border-radius: 12px;
        padding: 16px 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
        margin-bottom: 12px;
    }
    .metric-label { font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.08em; color: #8b949e; font-weight: 600; }
    .metric-val { font-family: 'JetBrains Mono', monospace; font-size: 1.85rem; font-weight: 700; margin-top: 4px; }
    .metric-sub { font-size: 0.8rem; font-family: 'JetBrains Mono', monospace; margin-top: 2px; }
    
    .threat-banner-red {
        background: rgba(248, 81, 73, 0.15); border: 1px solid #f85149;
        color: #ff7b72; padding: 14px 18px; border-radius: 10px; font-weight: 600; margin-bottom: 15px;
    }
    .threat-banner-green {
        background: rgba(63, 185, 80, 0.15); border: 1px solid #3fb950;
        color: #56d364; padding: 14px 18px; border-radius: 10px; font-weight: 600; margin-bottom: 15px;
    }

    .trace-card {
        background: rgba(13, 17, 23, 0.85);
        border: 1px solid #30363d;
        border-radius: 10px;
        padding: 18px 22px;
        margin-bottom: 14px;
    }
    .trace-badge {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.78rem;
        padding: 3px 8px;
        border-radius: 6px;
        font-weight: 700;
        display: inline-block;
        margin-bottom: 8px;
    }
</style>
""", unsafe_allow_html=True)

def render_3d_scanner(active=False, threat_detected=False):
    theme_color = "#f85149" if threat_detected else ("#3fb950" if active else "#58a6ff")
    active_flag = "true" if active else "false"
    threat_flag = "true" if threat_detected else "false"
    badge_text = "THREAT CONFIRMED" if threat_detected else ("ACOUSTIC STREAM LIVE" if active else "SYSTEM DORMANT")

    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ margin: 0; overflow: hidden; background: transparent; }}
            #canvas-container {{ width: 100%; height: 240px; position: relative; }}
            #badge {{
                position: absolute; top: 10px; left: 14px; font-family: monospace; font-size: 11px;
                color: {theme_color}; background: rgba(13, 17, 23, 0.8); padding: 4px 10px;
                border-radius: 6px; border: 1px solid {theme_color}44; pointer-events: none;
            }}
        </style>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    </head>
    <body>
        <div id="canvas-container"><div id="badge">EVE-NODE 3D SENSING ARRAY: {badge_text}</div></div>
        <script>
            const container = document.getElementById('canvas-container');
            const scene = new THREE.Scene();
            const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 1000);
            const renderer = new THREE.WebGLRenderer({{ alpha: true, antialias: true }});
            renderer.setSize(container.clientWidth, container.clientHeight);
            container.appendChild(renderer.domElement);

            const geom = new THREE.IcosahedronGeometry(2.1, 2);
            const mat = new THREE.MeshBasicMaterial({{
                color: '{theme_color}',
                wireframe: true,
                transparent: true,
                opacity: {0.9 if active else 0.4}
            }});
            const sphere = new THREE.Mesh(geom, mat);
            scene.add(sphere);

            const ringGeom = new THREE.RingGeometry(2.7, 2.75, 64);
            const ringMat = new THREE.MeshBasicMaterial({{ color: '{theme_color}', side: THREE.DoubleSide, transparent: true, opacity: 0.35 }});
            const ring = new THREE.Mesh(ringGeom, ringMat);
            ring.rotation.x = Math.PI / 2;
            scene.add(ring);

            const pCount = {260 if active else 110};
            const pGeom = new THREE.BufferGeometry();
            const pPos = new Float32Array(pCount * 3);
            for(let i = 0; i < pCount * 3; i += 3) {{
                pPos[i] = (Math.random() - 0.5) * 12;
                pPos[i+1] = (Math.random() - 0.5) * 6;
                pPos[i+2] = (Math.random() - 0.5) * 12;
            }}
            pGeom.setAttribute('position', new THREE.BufferAttribute(pPos, 3));
            const pMat = new THREE.PointsMaterial({{ color: '{theme_color}', size: {0.14 if active else 0.08}, transparent: true, opacity: 0.65 }});
            const particles = new THREE.Points(pGeom, pMat);
            scene.add(particles);

            camera.position.z = 7;
            camera.position.y = 2.1;
            camera.lookAt(0, 0, 0);

            let clock = new THREE.Clock();
            function animate() {{
                requestAnimationFrame(animate);
                const t = clock.getElapsedTime();
                const rotSpeed = {0.025 if active else 0.006};
                sphere.rotation.y += rotSpeed;
                sphere.rotation.x += rotSpeed * 0.5;
                ring.rotation.z += rotSpeed * 0.7;

                if ({active_flag}) {{
                    const s = 1.0 + Math.sin(t * 3.5) * {0.08 if threat_flag else 0.03};
                    sphere.scale.set(s, s, s);
                }}
                particles.rotation.y -= 0.003;
                renderer.render(scene, camera);
            }}
            animate();
        </script>
    </body>
    </html>
    """
    components.html(html_code, height=250)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PAYLOAD_PATH = os.path.join(BASE_DIR, "signal_processing", "outputs", "agent_payload.json")
RESULTS_IMG_PATH = os.path.join(BASE_DIR, "signal_processing", "outputs", "pipeline_results.png")
FALLBACK_IMG_PATH = os.path.join(BASE_DIR, "outputs", "pipeline_results.png")
DISPATCH_PATH = os.path.join(BASE_DIR, "outputs", "ranger_incident_dispatch.json")
CLEANED_WAV_PATH = os.path.join(BASE_DIR, "signal_processing", "processed", "cleaned_forest_signal.wav")
TRACE_JSON_PATH = os.path.join(BASE_DIR, "evidence", "agent_reasoning_trace.json")

if "executed" not in st.session_state:
    st.session_state.executed = False
if "metrics_data" not in st.session_state:
    st.session_state.metrics_data = None
if "features_data" not in st.session_state:
    st.session_state.features_data = None
if "trace_obj" not in st.session_state:
    st.session_state.trace_obj = None
if "dispatch_data" not in st.session_state:
    st.session_state.dispatch_data = None

st.markdown('<div class="hero-title">🌲 EVE-Node: Intelligent Forest Sensing & Interdiction</div>', unsafe_allow_html=True)
st.caption("IEEE Ingénieux Hackathon | Track 2: Forests & Wildlife Intelligent Sensing | Team Ciphera")

is_threat = False
if st.session_state.executed and st.session_state.dispatch_data:
    is_threat = st.session_state.dispatch_data.get("threat_detected", False)

render_3d_scanner(active=st.session_state.executed, threat_detected=is_threat)
st.markdown("---")

st.sidebar.markdown("### 🎛️ Sensor Hardware Status")
battery_slider = st.sidebar.slider("Edge Node Battery Level (%)", min_value=5.0, max_value=100.0, value=82.0, step=1.0)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🎙️ Audio Transmission Ingestion")
uploaded_file = st.sidebar.file_uploader("Upload Audio Sample (.wav, .mp3)", type=["wav", "mp3"])

if uploaded_file is not None:
    st.sidebar.audio(uploaded_file, format="audio/wav")
    st.sidebar.caption(f"Loaded: `{uploaded_file.name}`")

st.sidebar.markdown("---")
c_run, c_reset = st.sidebar.columns([3, 1])
with c_run:
    run_btn = st.button("⚡ Trigger Wake Cycle", use_container_width=True)
with c_reset:
    reset_btn = st.button("🔄 Reset", use_container_width=True)

if reset_btn:
    st.session_state.executed = False
    st.session_state.metrics_data = None
    st.session_state.features_data = None
    st.session_state.trace_obj = None
    st.session_state.dispatch_data = None
    st.rerun()

if run_btn:
    from signal_processing.main import run_pipeline
    from agent_controller import EvenodeAgenticController

    with st.spinner("Decoding telemetry and running tactical acoustic classifier..."):
        audio_in = None
        if uploaded_file is not None:
            uploaded_file.seek(0)
            raw_array, sr = sf.read(uploaded_file)
            if len(raw_array.shape) > 1:
                raw_array = np.mean(raw_array, axis=1)
            audio_in = (raw_array, sr)

        metrics, features = run_pipeline(
            audio_source=audio_in,
            lowcut=60.0 if battery_slider >= 20.0 else 180.0,
            highcut=4200.0 if battery_slider >= 20.0 else 2400.0,
            gate_mult=1.4,
            mode="STANDARD" if battery_slider >= 20.0 else "LOW_POWER"
        )

        controller = EvenodeAgenticController(node_id="EVE_Node_01", gps_coords="17.5449 N, 78.5718 E")
        controller.run_cycle(simulated_battery=battery_slider, weather=features.get("detected_weather", "CLEAR_CALM"))

        if os.path.exists(PAYLOAD_PATH):
            with open(PAYLOAD_PATH, "r") as f:
                p = json.load(f)
                st.session_state.metrics_data = p.get("metrics", {})
                st.session_state.features_data = p.get("extracted_features", {})

        if os.path.exists(TRACE_JSON_PATH):
            with open(TRACE_JSON_PATH, "r") as f:
                st.session_state.trace_obj = json.load(f)

        if os.path.exists(DISPATCH_PATH):
            with open(DISPATCH_PATH, "r") as f:
                st.session_state.dispatch_data = json.load(f)

        st.session_state.executed = True

    st.sidebar.success("Transmission evaluated!")
    st.rerun()

tab1, tab2, tab3 = st.tabs([
    "📊 Edge DSP & Spectral Evidence",
    "🤖 Agentic Reasoning Trace",
    "🚨 Ranger Interdiction Console"
])

if not st.session_state.executed:
    for tab in [tab1, tab2, tab3]:
        with tab:
            st.markdown(
                """
                <div style="text-align: center; padding: 60px 20px; border: 1px dashed rgba(48, 54, 61, 0.8); border-radius: 12px; margin-top: 15px; background: rgba(13, 17, 23, 0.5);">
                    <div style="font-size: 2.8rem; margin-bottom: 12px;">🛰️</div>
                    <h3 style="color: #f0f6fc; margin-bottom: 6px;">Sensor In Dormant Sleep State</h3>
                    <p style="color: #8b949e; max-width: 500px; margin: 0 auto; font-size: 0.92rem;">
                        No metrics or outputs are active. Upload an audio recording in the sidebar and click 
                        <strong style="color: #58a6ff;">⚡ Trigger Wake Cycle</strong> to transmit and classify acoustic telemetry.
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
else:
    dispatch = st.session_state.dispatch_data or {}
    metrics = st.session_state.metrics_data or {}
    features = st.session_state.features_data or {}
    trace = st.session_state.trace_obj or {}
    classification = dispatch.get("incident_classification", "UNKNOWN")
    threat_status = dispatch.get("threat_detected", False)

    if threat_status:
        st.markdown(f'<div class="threat-banner-red">🚨 ALERT DISPATCHED: <strong>{classification}</strong> (Confidence: {int(dispatch.get("confidence_score", 0.9)*100)}%)</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="threat-banner-green">✅ NOMINAL FOREST STATE: <strong>{classification}</strong> — No threat detected.</div>', unsafe_allow_html=True)

    with tab1:
        c1, c2, c3, c4 = st.columns(4)
        c1.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Auto-Detected Weather</div>
            <div class="metric-val" style="color: #58a6ff; font-size: 1.4rem;">{features.get("detected_weather", "CLEAR_CALM")}</div>
            <div class="metric-sub" style="color: #8b949e;">Acoustic Floor Analysis</div>
        </div>
        """, unsafe_allow_html=True)

        c2.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Cleaned SNR</div>
            <div class="metric-val" style="color: #3fb950;">{metrics.get("snr_after_db", 0.0):.2f} dB</div>
            <div class="metric-sub" style="color: #3fb950;">+{metrics.get("snr_gain_db", 0.0):.2f} dB Gain</div>
        </div>
        """, unsafe_allow_html=True)

        c3.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Frame Energy Gating</div>
            <div class="metric-val" style="color: #58a6ff;">{metrics.get("data_reduction_pct", 0.0):.1f}%</div>
            <div class="metric-sub" style="color: #a371f7;">Dormant Power Saved</div>
        </div>
        """, unsafe_allow_html=True)

        centroid_val = features.get("spectral_centroid_hz", 0.0)
        c4.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Event Centroid</div>
            <div class="metric-val" style="color: {'#e3b341' if threat_status else '#58a6ff'};">{centroid_val:.1f} Hz</div>
            <div class="metric-sub" style="color: {'#e3b341' if threat_status else '#3fb950'};">{'Threat Profile' if threat_status else 'Natural Biophony'}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### 🔬 Multi-Stage Signal Transformation Spectrogram")
        target_img = RESULTS_IMG_PATH if os.path.exists(RESULTS_IMG_PATH) else FALLBACK_IMG_PATH
        if os.path.exists(target_img):
            st.image(target_img, caption="Stage 1: Raw Ingested Signal | Stage 2: Adaptive Bandpass | Stage 3: Dynamic STFT Denoising", use_container_width=True)

        if os.path.exists(CLEANED_WAV_PATH):
            st.markdown("#### 🎧 Cleaned Audio Stream")
            st.audio(CLEANED_WAV_PATH, format="audio/wav")

    with tab2:
        st.markdown("### 🧠 Autonomous Agent Cognitive Trace")
        st.markdown("#### 🎯 Multi-Class Threat Probability Meter")
        scores = trace.get("scores", dispatch.get("class_probabilities", {}))
        
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            felling_val = float(scores.get("ILLEGAL_LOGGING_TREE_FELLING", 0.0))
            st.write(f"🪓 **Tree Felling & Axe Impacts**: `{int(felling_val * 100)}%`")
            st.progress(min(1.0, felling_val))

            chainsaw_val = float(scores.get("ILLEGAL_LOGGING_CHAINSAW", 0.0))
            st.write(f"⚙️ **Chainsaw Combustion Whine**: `{int(chainsaw_val * 100)}%`")
            st.progress(min(1.0, chainsaw_val))

        with col_m2:
            poaching_val = float(scores.get("POACHING_BALLISTIC_DISCHARGE", 0.0))
            st.write(f"💥 **Ballistic Gunshot Discharge**: `{int(poaching_val * 100)}%`")
            st.progress(min(1.0, poaching_val))

            biophony_val = float(scores.get("BENIGN_FOREST_BIOPHONY", 0.0))
            st.write(f"🌿 **Natural Canopy Biophony**: `{int(biophony_val * 100)}%`")
            st.progress(min(1.0, biophony_val))

        st.markdown("---")

        c_step1, c_step2 = st.columns(2)
        with c_step1:
            step1_html = (
                '<div class="trace-card">'
                '<span class="trace-badge" style="background: rgba(88, 166, 255, 0.2); color: #58a6ff;">STEP 1: OBSERVE</span>'
                '<p style="margin: 0; color: #c9d1d9; font-size: 0.88rem;">'
                f'<strong>Node Telemetry:</strong> ID <code>{trace.get("node_id", "EVE_Node_01")}</code> | '
                f'Battery: <strong>{trace.get("battery", 80)}%</strong> | Inferred Weather: <strong>{trace.get("weather", "CLEAR_CALM")}</strong><br>'
                f'<strong>Acoustic Floor:</strong> Raw SNR <code>{trace.get("snr_raw", 0.0):.2f} dB</code> ➔ '
                f'Cleaned SNR <code>{trace.get("snr_cleaned", 0.0):.2f} dB</code> (<strong>+{trace.get("snr_gain", 0.0):.2f} dB Net Gain</strong>)<br>'
                f'<strong>Transient Dynamics:</strong> Event Centroid <code>{trace.get("centroid", 0.0):.1f} Hz</code> | '
                f'Kurtosis <code>{trace.get("kurtosis", 0.0):.2f}</code> | Crest Factor <code>{trace.get("crest", 0.0):.2f}</code>'
                '</p></div>'
            )
            st.markdown(step1_html, unsafe_allow_html=True)

            step2_html = (
                '<div class="trace-card">'
                '<span class="trace-badge" style="background: rgba(227, 179, 65, 0.2); color: #e3b341;">STEP 2: REASON</span>'
                '<p style="margin: 0; color: #c9d1d9; font-size: 0.88rem;">'
                'Isolated foreground event frames from ambient background noise.<br>'
                f'• <strong>Motor Harmonic Concentration:</strong> <code>{int(trace.get("motor_ratio", 0.0) * 100)}%</code> in 250–2200 Hz band.<br>'
                f'• <strong>Percussive Timber Impact Energy:</strong> <code>{int(trace.get("impact_ratio", 0.0) * 100)}%</code> in 50–900 Hz band.<br>'
                f'• <strong>Acoustic Kurtosis:</strong> <code>{trace.get("kurtosis", 0.0):.2f}</code> (Sharp transient impact threshold: &gt; 2.5).'
                '</p></div>'
            )
            st.markdown(step2_html, unsafe_allow_html=True)

        with c_step2:
            pol_name = "LOW_POWER_RESTRICTED" if trace.get("battery", 80) < 20 else "STANDARD_FULL_CYCLE"
            step3_html = (
                '<div class="trace-card">'
                '<span class="trace-badge" style="background: rgba(163, 113, 247, 0.2); color: #a371f7;">STEP 3: ADAPT</span>'
                '<p style="margin: 0; color: #c9d1d9; font-size: 0.88rem;">'
                'Evaluated Edge Hardware Power Envelope:<br>'
                f'• <strong>Battery State:</strong> {trace.get("battery", 80)}% remaining.<br>'
                f'• <strong>Policy Applied:</strong> <code>{pol_name}</code>.<br>'
                '• <strong>Telemetry Mode:</strong> Full broadband tactical dispatch packet transmission enabled.'
                '</p></div>'
            )
            st.markdown(step3_html, unsafe_allow_html=True)

            badge_col = "rgba(248, 81, 73, 0.2)" if trace.get("threat", False) else "rgba(63, 185, 80, 0.2)"
            txt_col = "#f85149" if trace.get("threat", False) else "#3fb950"
            step4_html = (
                '<div class="trace-card">'
                f'<span class="trace-badge" style="background: {badge_col}; color: {txt_col};">STEP 4: ACT</span>'
                '<p style="margin: 0; color: #c9d1d9; font-size: 0.88rem;">'
                f'<strong>Verdict:</strong> <code>{trace.get("classification", "UNKNOWN")}</code> '
                f'(<strong>{int(trace.get("confidence", 0.0) * 100)}% Confidence</strong>)<br>'
                f'<strong>Action:</strong> {trace.get("action", "Standby")}'
                '</p></div>'
            )
            st.markdown(step4_html, unsafe_allow_html=True)

    with tab3:
        st.markdown("#### 📡 Tactical Dispatch Packet for Park Rangers")
        if dispatch:
            col_l, col_r = st.columns([1, 2])
            with col_l:
                if threat_status:
                    st.error(f"**Classification:** {classification}")
                else:
                    st.success(f"**Classification:** {classification}")
                st.metric("Confidence Score", f"{dispatch.get('confidence_score', 0.9)*100:.1f}%")
                st.write(f"**Node ID:** `{dispatch.get('sensor_node', 'EVE_Node_01')}`")
                st.write(f"**Coordinates:** `{dispatch.get('geo_coordinates', 'N/A')}`")
            with col_r:
                ev_summary = dispatch.get("evidence_summary", "N/A")
                act_summary = dispatch.get("recommended_tactical_action", "N/A")
                st.markdown(f"**Evidence Summary:**\n\n> {ev_summary}")
                st.markdown(f"**Recommended Tactical Action:**\n\n> `{act_summary}`")
                st.json(dispatch)
