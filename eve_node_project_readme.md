# 🌲 EVE-Node: Energy-Aware Adaptive Bioacoustic Sentry
**IEEE Ingénieux Hackathon | Track 2: Forests & Wildlife Intelligent Sensing**  
*Team Ciphera*

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)
[![GitHub Repository](https://img.shields.io/badge/GitHub-Repository-181717?logo=github)](https://github.com/dheeraj62811/EVE-Node-AI)

---

## 📌 Problem & Motivation
Remote acoustic sensor nodes deployed in wildlife sanctuaries and protected forests operate under severe edge constraints:
1. **Bandwidth & Power Penalties:** Continuously transmitting raw audio streams over satellite or cellular links rapidly exhausts battery reserves.
2. **False Threat Alarms:** Conventional amplitude-threshold detectors frequently trigger false alarms from harmless avian vocalizations and rain bursts.
3. **Black-Box Classification:** Standard deep neural networks consume significant compute cycles without providing transparent evidence trails to guide ranger response teams.

---

## 💡 The EVE-Node Solution
**EVE-Node** is an autonomous, energy-aware edge computing pipeline designed for real-time forest protection:
- **Autonomous Denoising & Gating:** Executes adaptive bandpass filtering and dynamic STFT spectral subtraction to eliminate stationary environmental noise, coupled with frame-energy gating to achieve **up to 70%+ compute savings**.
- **Physics-Guided Feature Discrimination:** Extracts Crest Factor, Kurtosis, Zero-Crossing Rate, and Motor/Impact sub-band ratios to cleanly distinguish timber cuts and firearm discharges from natural canopy biophony.
- **Explainable Agent Controller:** Generates an auditable four-stage reasoning trace (`OBSERVE` ➔ `REASON` ➔ `ADAPT` ➔ `ACT`) and outputs a low-latency JSON dispatch packet for field rangers.
- **Spatial 3D Command Console:** Visualizes real-time sensor node telemetry through an interactive Three.js holographic radar and a dedicated three-tier mission console.

---

## 🏗️ Architecture & Processing Pipeline

```
[ Ambient Microphone Audio Ingestion ]
                  │
                  ▼
┌────────────────────────────────────────────────────────┐
│  STAGE 1: EDGE ACOUSTIC PRE-PROCESSING                 │
│  • Automated Welch PSD Noise-Floor Profiling           │
│  • Bandpass Filtering (60 Hz – 4.2 kHz / Low-Power)    │
│  • Dynamic STFT Spectral Subtraction                   │
│  • Frame Energy Threshold Gating (Dormant Drop)        │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│  STAGE 2: ACOUSTIC FEATURE EXTRACTION                  │
│  • Spectral Centroid (Hz) & Zero-Crossing Rate (ZCR)   │
│  • Impulsive Kurtosis & Peak-to-RMS Crest Factor       │
│  • Combustion Motor Band Ratio (250 Hz – 2200 Hz)      │
│  • Percussive Timber Impact Ratio (50 Hz – 900 Hz)     │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│  STAGE 3: AUTONOMOUS AGENT REASONING ENGINE            │
│  • STEP 1 (OBSERVE): Ingest Telemetry, Weather & SNR   │
│  • STEP 2 (REASON) : Physics & Frequency-Gate Rules    │
│  • STEP 3 (ADAPT)  : Dynamic Battery Envelope Policy   │
│  • STEP 4 (ACT)    : Dispatch Packet Generation        │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│  STAGE 4: SPATIAL 3D RADAR & COMMAND DASHBOARD         │
│  • Tab 1: Edge DSP & Multi-Stage Spectral Visualizer   │
│  • Tab 2: Autonomous Cognitive Trace & Threat Radar    │
│  • Tab 3: Tactical Ranger Interdiction Console         │
└────────────────────────────────────────────────────────┘
```

---

## 🔬 Acoustic Discrimination Matrix

| Threat / Event Type | Primary Acoustic Signatures | Mathematical & Frequency Gates | Action Directive |
| :--- | :--- | :--- | :--- |
| **Mechanized Chainsaw** | Periodic internal-combustion whine, continuous motor harmonics | $\text{Motor Ratio} \ge 0.38$, $\text{Centroid} \in [300, 2200]\text{ Hz}$, $\text{ZCR} < 0.22$ | Priority Interdiction: Dispatch rapid response unit to intercept active mechanized logging. |
| **Tree Felling / Axe Strikes** | Low-frequency structural wood crack, percussive ground impacts | $\text{Impact Ratio} \ge 0.22$, $\text{Crest Factor} \ge 3.2$, $\text{Centroid} \le 1600\text{ Hz}$ | Priority Alert: Dispatch local forestry response team to investigate active tree felling. |
| **Ballistic Gunshot** | Low-frequency shockwave, abrupt explosive peak, high kurtosis | $\text{Kurtosis} > 8.0$, $\text{Crest Factor} > 6.0$, $\text{Centroid} \le 1600\text{ Hz}$ | CODE RED: Armed poaching detected. Dispatch armed tactical rangers immediately. |
| **Canopy Biophony** | High-frequency bird vocalizations, chirp transients, wind rustle | $\text{Centroid} \ge 2100\text{ Hz}$ OR $\text{ZCR} \ge 0.24$ | Maintain passive listening cycle. Benign forest soundscape confirmed. |

---

## 📁 Repository Directory Structure

```text
EVE-Node-AI/
├── app.py                      # Main Streamlit dashboard with 3D Three.js spatial radar
├── agent_controller.py         # 4-stage autonomous cognitive reasoning controller
├── benchmark.py                # Pipeline execution benchmark & verification suite
├── requirements.txt            # Python dependencies (Streamlit, SoundFile, SciPy, NumPy)
├── packages.txt                # System-level dependencies for cloud deployment (libsndfile1, ffmpeg)
├── signal_processing/
│   ├── main.py                 # Pipeline entrypoint and processing controller
│   ├── pipeline.py             # Denoising, filtering, STFT spectral subtraction
│   ├── feature_extraction.py   # Mathematical acoustic DSP feature extraction
│   ├── outputs/                # Generated spectrogram comparisons and JSON payloads
│   └── processed/              # Cleaned acoustic output files
├── evidence/                   # Recorded agent reasoning trace logs
└── outputs/                    # Ranger incident tactical dispatch packets
```

---

## 🚀 Quickstart Guide

### 1. Local Setup
```bash
# Clone the repository
git clone https://github.com/dheeraj62811/EVE-Node-AI.git
cd EVE-Node-AI

# Install Python dependencies
pip install -r requirements.txt
```

### 2. Launch the Web Console
```bash
python3 -m streamlit run app.py
```

Open `http://localhost:8501` to access the interactive spatial radar and mission console.

---

## 🛠️ Technology Stack
- **Audio Processing & DSP:** `NumPy`, `SciPy` (Signal, STFT, Welch PSD), `SoundFile`
- **Agent Intelligence:** Autonomous Rule-Gated Multi-Candidate Probabilistic Engine
- **Spatial UI & Visualization:** `Streamlit`, `Three.js` (WebGL Holographic Radar)
- **Edge Deployment Target:** Low-power embedded hardware running Debian / Ubuntu with `libsndfile1`