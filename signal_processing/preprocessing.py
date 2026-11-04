import numpy as np
import scipy.signal as signal

def preprocess_signal(data, sr, downsample_factor=1):
    # Remove DC offset (zero-mean centering)
    centered = data - np.mean(data)
    
    # Optional signal reduction via decimation (saves memory/compute in low-power mode)
    if downsample_factor > 1:
        centered = signal.decimate(centered, downsample_factor)
        sr = sr // downsample_factor
        
    # Peak normalization to [-1, 1]
    max_val = np.max(np.abs(centered)) + 1e-10
    normalized = centered / max_val
    return normalized, sr
