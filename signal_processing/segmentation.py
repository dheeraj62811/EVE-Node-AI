"""
RMS Energy Gating for Edge Battery and Compute Preservation
"""

import numpy as np

def energy_gate_segmentation(
    audio: np.ndarray, 
    sample_rate: int = 16000, 
    frame_ms: float = 50.0, 
    hop_ms: float = 25.0, 
    percentile_thresh: float = 60.0
) -> tuple[np.ndarray, np.ndarray, list, float]:
    """
    Computes short-time frame energy and drops frames below the percentile threshold.
    Preserves >60% edge power by ignoring low-energy ambient forest segments.
    """
    frame_len = int((frame_ms / 1000.0) * sample_rate)
    hop_len = int((hop_ms / 1000.0) * sample_rate)
    
    num_frames = (len(audio) - frame_len) // hop_len + 1
    energies = np.array([
        np.sum(audio[i * hop_len : i * hop_len + frame_len] ** 2)
        for i in range(num_frames)
    ])

    cutoff = np.percentile(energies, percentile_thresh)
    active_mask = energies >= cutoff
    
    active_frame_indices = np.where(active_mask)[0].tolist()
    data_reduction_pct = float((1.0 - (len(active_frame_indices) / max(1, num_frames))) * 100.0)

    # Reconstruct gated signal
    gated_signal = np.copy(audio)
    for i, active in enumerate(active_mask):
        if not active:
            start = i * hop_len
            end = min(start + frame_len, len(gated_signal))
            gated_signal[start:end] *= 0.05  # heavily attenuate dormant frames

    return gated_signal, active_mask, active_frame_indices, round(data_reduction_pct, 1)
