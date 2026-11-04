"""
STFT Spectral Subtraction Noise Gating for Rain and Broadband Hiss
"""

import numpy as np
import scipy.signal as signal

def spectral_denoise(audio: np.ndarray, sample_rate: int = 16000, gate_mult: float = 1.8, nperseg: int = 512) -> np.ndarray:
    """
    Suppresses stationary rain/wind clutter using short-time Fourier transform spectral gating.
    """
    f, t, Zxx = signal.stft(audio, fs=sample_rate, nperseg=nperseg, noverlap=nperseg // 2)
    magnitude = np.abs(Zxx)
    phase = np.angle(Zxx)

    # Estimate noise spectrum from initial silent/ambient frames
    noise_estimate = np.median(magnitude[:, :6], axis=1, keepdims=True)

    # Spectral subtraction with residual spectral floor to prevent musical noise
    cleaned_magnitude = np.maximum(magnitude - (gate_mult * noise_estimate), 0.02 * magnitude)

    _, denoised_audio = signal.istft(cleaned_magnitude * np.exp(1j * phase), fs=sample_rate)
    return denoised_audio[:len(audio)]
