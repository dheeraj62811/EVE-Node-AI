import numpy as np

def compute_snr(clean_ref, test_signal, mask=None):
    if mask is not None and np.any(mask):
        clean_ref = clean_ref[mask]
        test_signal = test_signal[mask]
        
    # Align scale for fair SNR comparison
    scale = np.dot(clean_ref, test_signal) / (np.dot(clean_ref, clean_ref) + 1e-10)
    scaled_clean = scale * clean_ref
    
    noise = test_signal - scaled_clean
    sig_power = np.mean(scaled_clean ** 2) + 1e-10
    noise_power = np.mean(noise ** 2) + 1e-10
    return float(10 * np.log10(sig_power / noise_power))
