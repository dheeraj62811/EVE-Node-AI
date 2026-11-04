import os
import json
import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt
import librosa

def save_all_outputs(raw_sig, clean_sig, sr, rms, thresh, payload):
    os.makedirs("processed", exist_ok=True)
    os.makedirs("outputs", exist_ok=True)
    
    # 1. Save cleaned audio
    sf.write("processed/cleaned_forest_signal.wav", clean_sig, sr)
    
    # 2. Save JSON payload for Agent/Report
    with open("outputs/agent_payload.json", "w") as f:
        json.dump(payload, f, indent=4)
        
    # 3. Generate high-res visual evidence plot
    t = np.linspace(0, len(raw_sig) / sr, len(raw_sig), endpoint=False)
    plt.figure(figsize=(11, 7))
    
    plt.subplot(3, 1, 1)
    plt.plot(t, raw_sig, color='slategray', alpha=0.8)
    plt.title(f"1. Raw Forest Sensor Input (Rain + Wind + 4.2kHz Cicadas) | Baseline SNR: {payload['metrics']['snr_before_db']} dB")
    plt.ylabel("Amplitude")
    
    plt.subplot(3, 1, 2)
    plt.plot(t, clean_sig, color='teal')
    plt.title(f"2. After Notch + Bandpass + Spectral Denoising | Cleaned SNR: {payload['metrics']['snr_after_db']} dB (+{payload['metrics']['snr_gain_db']} dB Gain)")
    plt.ylabel("Amplitude")
    
    plt.subplot(3, 1, 3)
    frame_times = librosa.frames_to_time(np.arange(len(rms)), sr=sr, hop_length=512)
    plt.plot(frame_times, rms, color='darkorange', label="Frame RMS Energy")
    plt.axhline(thresh, color='crimson', linestyle='--', label="Wake-up Gate Threshold")
    plt.title(f"3. Energy Gating Segmentation | Dropped {payload['metrics']['data_reduction_pct']}% Ambient Frames to Save Battery")
    plt.xlabel("Time (seconds)")
    plt.ylabel("RMS Energy")
    plt.legend(loc="upper right")
    
    plt.tight_layout()
    plt.savefig("outputs/pipeline_results.png", dpi=150)
    plt.close()
