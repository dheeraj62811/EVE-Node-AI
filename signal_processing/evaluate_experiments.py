import time
import numpy as np
from preprocessing import preprocess_signal
from filtering import apply_bandpass, apply_insect_notch
from noise_reduction import spectral_denoise
from segmentation import energy_gate_segmentation
from signal_analysis import compute_snr

def run_benchmark_suite(sr=16000, duration=5.0):
    t = np.linspace(0, duration, int(sr * duration), endpoint=False)
    
    # Clean target (Chainsaw harmonics)
    clean = np.zeros_like(t)
    mask = (t >= 1.5) & (t <= 3.5)
    clean[mask] = (0.6 * np.sin(2 * np.pi * 440 * t[mask]) + 
                   0.4 * np.sin(2 * np.pi * 880 * t[mask]) + 
                   0.25 * np.sin(2 * np.pi * 1320 * t[mask]))
    
    noise_conditions = [
        ("Light Wind + Cicadas", 0.2),
        ("Moderate Rain + Wind", 0.4),
        ("Heavy Monsoon Storm", 0.7),
        ("Extreme Clutter Stress-Test", 1.1)
    ]
    
    print("\n### EXPERIMENTAL EVALUATION TABLE (Copy into Report & Slides)\n")
    print("| Test Condition | Baseline SNR (dB) | Cleaned SNR (dB) | SNR Gain (dB) | Frames Dropped (Battery Saved) | Latency (ms) |")
    print("| :--- | :---: | :---: | :---: | :---: | :---: |")
    
    for name, noise_std in noise_conditions:
        start_time = time.time()
        
        # Add wind + 4.2kHz insects + variable rain noise
        wind = 0.6 * np.sin(2 * np.pi * 70 * t)
        insects = 0.5 * np.sin(2 * np.pi * 4200 * t)
        rain = np.random.normal(0, noise_std, len(t))
        noisy = clean + wind + insects + rain
        
        # Run pipeline
        norm_noisy, _ = preprocess_signal(noisy, sr)
        notched = apply_insect_notch(norm_noisy, sr)
        bandpassed = apply_bandpass(notched, sr)
        cleaned = spectral_denoise(bandpassed, sr)
        _, active_mask, _, _, reduction_pct = energy_gate_segmentation(cleaned, sr)
        
        latency_ms = (time.time() - start_time) * 1000
        snr_base = compute_snr(clean, norm_noisy, mask=active_mask)
        snr_clean = compute_snr(clean, cleaned, mask=active_mask)
        gain = snr_clean - snr_base
        
        print(f"| {name} | {snr_base:.2f} dB | {snr_clean:.2f} dB | **+{gain:.2f} dB** | **{reduction_pct:.1f}%** | {latency_ms:.1f} ms |")

if __name__ == "__main__":
    run_benchmark_suite()
