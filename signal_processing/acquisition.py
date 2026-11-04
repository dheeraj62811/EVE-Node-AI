import os
import numpy as np
import soundfile as sf
import librosa

def acquire_signal(filepath="recordings/forest_sample.wav", duration=6.0, sr=16000):
    os.makedirs("recordings", exist_ok=True)
    
    # Generate synthetic forest recording if file doesn't exist
    if not os.path.exists(filepath):
        t = np.linspace(0, duration, int(sr * duration), endpoint=False)
        
        # 1. Target Threat: Chainsaw harmonic burst (between 2.0s and 4.5s)
        clean_target = np.zeros_like(t)
        mask = (t >= 2.0) & (t <= 4.5)
        clean_target[mask] = (
            0.6 * np.sin(2 * np.pi * 440 * t[mask]) +
            0.4 * np.sin(2 * np.pi * 880 * t[mask]) +
            0.25 * np.sin(2 * np.pi * 1320 * t[mask])
        )
        
        # 2. Environmental Clutter: Wind (<120Hz) + Cicada Chorus (4200Hz) + Rain (White Noise)
        wind = 0.7 * np.sin(2 * np.pi * 65 * t) + 0.5 * np.sin(2 * np.pi * 105 * t)
        cicadas = 0.5 * np.sin(2 * np.pi * 4200 * t)
        rain = np.random.normal(0, 0.35, len(t))
        
        noisy_signal = clean_target + wind + cicadas + rain
        sf.write(filepath, noisy_signal, sr)
        sf.write("recordings/clean_reference.wav", clean_target, sr)
        return noisy_signal, clean_target, sr
    else:
        noisy_signal, sr = librosa.load(filepath, sr=sr)
        clean_path = "recordings/clean_reference.wav"
        clean_target = librosa.load(clean_path, sr=sr)[0] if os.path.exists(clean_path) else noisy_signal
        return noisy_signal, clean_target, sr
