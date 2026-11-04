"""
Exports Cleaned Audio (.wav), JSON Contracts, and PNG Spectrogram Plots
"""

import os
import json
import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt

def export_results(
    raw_audio: np.ndarray,
    filtered_audio: np.ndarray,
    cleaned_audio: np.ndarray,
    sample_rate: int,
    metrics: dict,
    features: dict,
    evaluation: dict,
    base_dir: str
) -> None:
    """
    Exports audio files, data contract JSON, and 3-stage spectrogram comparison.
    """
    proc_dir = os.path.join(base_dir, "processed")
    out_dir = os.path.join(base_dir, "outputs")
    os.makedirs(proc_dir, exist_ok=True)
    os.makedirs(out_dir, exist_ok=True)

    # 1. Export Clean Audio
    wav_path = os.path.join(proc_dir, "cleaned_forest_signal.wav")
    sf.write(wav_path, cleaned_audio, sample_rate)

    # 2. Export Contract Payload for Agent & Dashboard
    payload = {
        "metrics": metrics,
        "extracted_features": features,
        "agent_evaluation": evaluation
    }
    payload_path = os.path.join(out_dir, "agent_payload.json")
    with open(payload_path, "w") as f:
        json.dump(payload, f, indent=4)

    # 3. Export 3-Stage Visual Evidence Spectrogram
    fig, axs = plt.subplots(3, 2, figsize=(14, 10))
    t = np.linspace(0, len(raw_audio) / sample_rate, len(raw_audio))

    # Time Domain
    axs[0, 0].plot(t[:1600], raw_audio[:1600], color='#d9534f')
    axs[0, 0].set_title(f"Stage 1: Raw Captured Stream (SNR: {metrics.get('snr_before_db')} dB)")
    axs[0, 0].set_ylabel("Amplitude")
    axs[0, 0].grid(True, alpha=0.3)

    axs[1, 0].plot(t[:1600], filtered_audio[:1600], color='#f0ad4e')
    axs[1, 0].set_title("Stage 2: Fixed Filtering (Notch + Broad Bandpass)")
    axs[1, 0].set_ylabel("Amplitude")
    axs[1, 0].grid(True, alpha=0.3)

    axs[2, 0].plot(t[:1600], cleaned_audio[:1600], color='#5cb85c')
    axs[2, 0].set_title(f"Stage 3: Agentic Reconfigured Filter + STFT Gating (SNR: {metrics.get('snr_after_db')} dB)")
    axs[2, 0].set_xlabel("Time (s)")
    axs[2, 0].set_ylabel("Amplitude")
    axs[2, 0].grid(True, alpha=0.3)

    # Frequency Domain (Spectrograms)
    axs[0, 1].specgram(raw_audio, Fs=sample_rate, NFFT=512, noverlap=256, cmap='inferno')
    axs[0, 1].set_title("Spectrogram: Raw Cluttered Signal (Cicadas & Monsoon)")
    axs[0, 1].set_ylabel("Frequency (Hz)")

    axs[1, 1].specgram(filtered_audio, Fs=sample_rate, NFFT=512, noverlap=256, cmap='inferno')
    axs[1, 1].set_title("Spectrogram: Cicada Notch Filtered (4.2 kHz Excised)")
    axs[1, 1].set_ylabel("Frequency (Hz)")

    axs[2, 1].specgram(cleaned_audio, Fs=sample_rate, NFFT=512, noverlap=256, cmap='inferno')
    axs[2, 1].set_title("Spectrogram: Isolated Chainsaw Comb Spectrum")
    axs[2, 1].set_xlabel("Time (s)")
    axs[2, 1].set_ylabel("Frequency (Hz)")

    plt.tight_layout()
    img_path = os.path.join(out_dir, "pipeline_results.png")
    plt.savefig(img_path, dpi=300)
    plt.close()
