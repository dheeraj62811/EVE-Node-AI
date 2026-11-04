import numpy as np
import librosa

def energy_gate_segmentation(data, sr, frame_length=1024, hop_length=512, percentile_thresh=60):
    """Drops silent/ambient frames to reduce downstream AI compute and battery drain."""
    rms = librosa.feature.rms(y=data, frame_length=frame_length, hop_length=hop_length)[0]
    threshold = np.percentile(rms, percentile_thresh)
    active_frames = rms > threshold
    
    # Reconstruct reduced signal containing only high-energy segments
    active_samples_mask = np.repeat(active_frames, hop_length)[:len(data)]
    if len(active_samples_mask) < len(data):
        active_samples_mask = np.pad(active_samples_mask, (0, len(data) - len(active_samples_mask)))
        
    active_only_signal = data[active_samples_mask]
    data_reduction_pct = (1.0 - (len(active_only_signal) / len(data))) * 100.0
    
    return active_only_signal, active_samples_mask, rms, threshold, data_reduction_pct
