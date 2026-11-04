import numpy as np
import scipy.signal as signal

def estimate_weather_condition(audio: np.ndarray, sample_rate: int = 16000) -> str:
    audio = np.asarray(audio, dtype=np.float64)
    if len(audio) == 0:
        return "CLEAR_CALM"

    frame_len = int(0.1 * sample_rate)
    num_frames = len(audio) // frame_len
    if num_frames < 4:
        return "CLEAR_CALM"

    frames = audio[:num_frames * frame_len].reshape(num_frames, frame_len)
    frame_rms = np.sqrt(np.mean(frames ** 2, axis=1))

    # Evaluate the quietest 25% background frames
    quiet_idx = np.argsort(frame_rms)[:max(2, int(0.25 * num_frames))]
    bg = frames[quiet_idx].flatten()

    freqs, psd = signal.welch(bg, fs=sample_rate, nperseg=min(len(bg), 1024))
    total_power = np.sum(psd) + 1e-12

    wind_p = np.sum(psd[(freqs >= 20) & (freqs <= 120)]) + 1e-12
    rain_p = np.sum(psd[(freqs >= 1800) & (freqs <= 5000)]) + 1e-12

    wind_ratio = wind_p / total_power
    rain_ratio = rain_p / total_power

    if wind_ratio > 0.52:
        return "HIGH_WIND"
    elif rain_ratio > 0.42:
        return "HEAVY_MONSOON" if wind_ratio > 0.22 else "CALM_RAIN"
    else:
        return "CLEAR_CALM"

def extract_features(audio: np.ndarray, sample_rate: int = 16000) -> dict:
    audio = np.asarray(audio, dtype=np.float64)
    if len(audio) == 0:
        return {
            "spectral_centroid_hz": 0.0,
            "zero_crossing_rate": 0.0,
            "rms_energy": 0.0,
            "crest_factor": 0.0,
            "kurtosis": 0.0,
            "motor_harmonic_ratio": 0.0,
            "impact_energy_ratio": 0.0,
            "detected_weather": "CLEAR_CALM"
        }

    # Isolate energetic event segments (transient foreground vs background)
    frame_len = int(0.05 * sample_rate)
    num_frames = len(audio) // frame_len
    if num_frames > 4:
        frames = audio[:num_frames * frame_len].reshape(num_frames, frame_len)
        frame_rms = np.sqrt(np.mean(frames ** 2, axis=1))
        # Top 40% active frames capture the chops, motor hum, and impacts
        top_k = max(2, int(0.40 * num_frames))
        active_idx = np.argsort(frame_rms)[-top_k:]
        analysis_audio = frames[active_idx].flatten()
    else:
        analysis_audio = audio

    # PSD on active frames
    freqs, psd = signal.welch(analysis_audio, fs=sample_rate, nperseg=min(len(analysis_audio), 1024))
    psd_sum = np.sum(psd) + 1e-12
    event_centroid = float(np.sum(freqs * psd) / psd_sum)

    # Time-domain metrics
    rms = float(np.sqrt(np.mean(audio ** 2))) + 1e-9
    peak = float(np.max(np.abs(audio)))
    crest_factor = round(peak / rms, 2)

    centered = audio - np.mean(audio)
    kurt = float(round(np.mean(centered ** 4) / ((np.mean(centered ** 2) + 1e-9) ** 2), 2))
    zcr = float(np.mean(np.abs(np.diff(np.sign(audio)))) / 2.0)

    # Energy sub-bands in event frames
    motor_p = np.sum(psd[(freqs >= 250) & (freqs <= 2200)]) + 1e-12
    impact_p = np.sum(psd[(freqs >= 50) & (freqs <= 900)]) + 1e-12

    return {
        "spectral_centroid_hz": round(event_centroid, 2),
        "zero_crossing_rate": round(zcr, 4),
        "rms_energy": round(rms, 4),
        "crest_factor": crest_factor,
        "kurtosis": kurt,
        "motor_harmonic_ratio": round(float(motor_p / psd_sum), 3),
        "impact_energy_ratio": round(float(impact_p / psd_sum), 3),
        "detected_weather": estimate_weather_condition(audio, sample_rate)
    }
