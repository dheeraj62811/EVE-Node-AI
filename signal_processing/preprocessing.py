"""
Audio Preprocessing: DC-Offset Removal and Peak Normalization
"""

import numpy as np

def preprocess_signal(audio: np.ndarray, sample_rate: int = 16000) -> tuple[np.ndarray, dict]:
    """
    Removes DC bias and normalizes dynamic range to [-1.0, 1.0].
    """
    dc_offset = float(np.mean(audio))
    zero_mean_audio = audio - dc_offset
    
    peak = float(np.max(np.abs(zero_mean_audio)))
    if peak > 1e-6:
        normalized_audio = zero_mean_audio / peak
    else:
        normalized_audio = zero_mean_audio

    metadata = {
        "dc_offset_removed": round(dc_offset, 6),
        "peak_amplitude": round(peak, 4),
        "sample_rate": sample_rate
    }
    return normalized_audio, metadata
