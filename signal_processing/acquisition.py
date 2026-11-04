"""
Audio Acquisition & Synthetic Forest Stream Generation
"""

import os
import numpy as np
import scipy.signal as signal
import soundfile as sf

def acquire_or_synthesize_audio(
    file_path: str = None, 
    sample_rate: int = 16000, 
    duration: float = 2.0, 
    target_snr_db: float = -4.12
) -> tuple[np.ndarray, int]:
    """
    Loads raw audio from recordings/ if available, or synthesizes a 
    physically accurate cluttered rainforest audio stream.
    """
    if file_path and os.path.exists(file_path):
        audio, sr = sf.read(file_path)
        if len(audio.shape) > 1:
            audio = np.mean(audio, axis=1)
        if sr != sample_rate:
            num_samples = int(len(audio) * sample_rate / sr)
            audio = signal.resample(audio, num_samples)
        return audio, sample_rate

    # Synthetic Cluttered Forest Audio
    num_samples = int(sample_rate * duration)
    t = np.linspace(0, duration, num_samples, endpoint=False)

    # 1. Environmental Noise (Wind rumble + broadband monsoon rain)
    white = np.random.normal(0, 1, num_samples)
    b, a = signal.butter(2, 150.0 / (0.5 * sample_rate), btype='low')
    rumble = signal.lfilter(b, a, white)
    rain = np.random.normal(0, 0.35, num_samples)
    ambient_noise = 0.08 * (rumble + rain)

    # 2. Continuous 4.2 kHz Cicada / Insect Chorus
    cicada_mod = 0.5 * (1.0 + np.sin(2 * np.pi * 8.0 * t))
    cicada = 0.12 * np.sin(2 * np.pi * 4200.0 * t) * cicada_mod

    total_noise = ambient_noise + cicada

    # 3. Chainsaw Acoustic Signature (Comb spectrum: 125 Hz fundamental)
    chainsaw = np.zeros(num_samples)
    for h in range(1, 15):
        freq = 125.0 * h
        if 250.0 <= freq <= 2500.0:
            jitter = 1.0 + 0.012 * np.sin(2 * np.pi * 4.0 * t)
            amp = 1.0 / (h ** 0.75)
            chainsaw += amp * np.sin(2 * np.pi * (freq * jitter) * t)
    chainsaw = chainsaw / (np.max(np.abs(chainsaw)) + 1e-9)

    # Scale to target SNR
    noise_power = np.mean(total_noise ** 2)
    sig_power = np.mean(chainsaw ** 2)
    scale = np.sqrt((noise_power * (10 ** (target_snr_db / 10.0))) / (sig_power + 1e-12))
    
    raw_stream = (chainsaw * scale) + total_noise
    raw_stream = raw_stream / (np.max(np.abs(raw_stream)) + 1e-9)
    
    return raw_stream, sample_rate
