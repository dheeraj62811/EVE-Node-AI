"""
IIR Notch Filtering & Butterworth Bandpass Extraction
"""

import numpy as np
import scipy.signal as signal

def apply_insect_notch(audio: np.ndarray, sample_rate: int = 16000, f_notch: float = 4200.0, Q: float = 30.0) -> np.ndarray:
    """
    2nd-order IIR notch filter targeting the high-energy 4.2 kHz cicada frequency.
    """
    b, a = signal.iirnotch(f_notch, Q, sample_rate)
    return signal.filtfilt(b, a, audio)

def apply_bandpass(audio: np.ndarray, sample_rate: int = 16000, lowcut: float = 250.0, highcut: float = 3500.0, order: int = 4) -> np.ndarray:
    """
    Butterworth bandpass filter isolating acoustic threat bands while attenuating rumble.
    """
    nyq = 0.5 * sample_rate
    low = max(0.005, lowcut / nyq)
    high = min(0.995, highcut / nyq)
    b, a = signal.butter(order, [low, high], btype='band')
    return signal.filtfilt(b, a, audio)
