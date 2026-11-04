import numpy as np
import librosa

def extract_features(active_signal, sr):
    if len(active_signal) < 1024:
        active_signal = np.pad(active_signal, (0, 1024 - len(active_signal)))
        
    centroid = float(np.mean(librosa.feature.spectral_centroid(y=active_signal, sr=sr)))
    bandwidth = float(np.mean(librosa.feature.spectral_bandwidth(y=active_signal, sr=sr)))
    zcr = float(np.mean(librosa.feature.zero_crossing_rate(y=active_signal)))
    onset_env = librosa.onset.onset_strength(y=active_signal, sr=sr)
    spectral_flux = float(np.mean(onset_env))
    mfccs = np.mean(librosa.feature.mfcc(y=active_signal, sr=sr, n_mfcc=5), axis=1).tolist()
    
    return {
        "spectral_centroid_hz": round(centroid, 2),
        "spectral_bandwidth_hz": round(bandwidth, 2),
        "zero_crossing_rate": round(zcr, 4),
        "spectral_flux": round(spectral_flux, 3),
        "mfcc_vector": [round(float(m), 2) for m in mfccs]
    }
